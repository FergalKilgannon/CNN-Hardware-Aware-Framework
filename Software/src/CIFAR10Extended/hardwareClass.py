import torch
import numpy as np
import pandas as pd

class hardware:
    def __init__(self, model, num_bits, stride, ncol, nrow, device, array_choice, mac_choice, mac_constants):
        self.device = device                # Device used (CPU)
        self.model = model                  # Trained model
        self.num_bits = num_bits            # Quantization level
        self.stride = stride                # Convolutional stride
        self.ncol = ncol                    # Hardware matrix-vector-multiplication (MVM) columns (corresponds to number of output ADCs)
        self.nrow = nrow                    # Hardware MVM rows (corresponds to number of input DACs)
                                            # In-memory computing hardware therefore has ncol*nrow weights.

        # One-off generations (non-ideality look-up table/mismatched grid)
        self.nl_mult = self.read_non_idealities(mac_constants)
        self.gain_mismatch, self.offset_mismatch = self.gen_mismatch_grid(mac_constants)

        self.array_fn = getattr(self, array_choice)     # Array function to be used
        self.mac_fn = getattr(self, mac_choice)         # MAC function to be used
        self.mac_constants = mac_constants              # Constants associated with chosen MAC


    # Generate mismatched grid (called once upon initialisation of hardware class)
    def gen_mismatch_grid(self, mismatch):
        if not isinstance(mismatch, str) and not isinstance(mismatch, list):
            gain = torch.transpose(torch.from_numpy(np.zeros((self.nrow, 1)) + (np.random.normal(0, mismatch/100, (self.ncol)) + 1)), 0, 1)
            offset = torch.transpose(torch.from_numpy(np.zeros((self.nrow, 1)) + np.random.normal(0, mismatch/100, (self.ncol))), 0, 1)
            return gain, offset
        return 0, 0

    # Read non-ideality table frome excel
    def read_non_idealities(self, file_name):
        if not isinstance(file_name, str):
            return 0
        return pd.read_excel(file_name, index_col=0).values
    

    ### ----------------------------------------------------------###
    ###                   HARDWARE DESCRIPTIONS                   ###
    ### ----------------------------------------------------------###

    # -------------------- CONVOLUTIONAL LAYER -------------------- #

    def conv2d(self, x, batch, conv, s_in, idim, ifmap, ofmap, knl, padding=0):
        # Scale input image, conv weight and bias to bits used
        sw_conv, filters_conv = self.scale_quant(conv.weight.cpu(), self.num_bits)
        bias_conv = conv.bias / (s_in * sw_conv)

        # CONV layer (WSAB dataflow - see convolve2D_wsab function)
        out_conv = self.convolve2D_wsab(x, filters_conv, bias_conv, padding, self.stride, batch, ifmap, ofmap, idim, knl, self.ncol, self.nrow)
        out_conv = torch.from_numpy(out_conv)
        out_conv = out_conv.to(self.device)

        # Applying scaling normalization s_in*sw_conv (convert back to float)
        return out_conv * s_in * sw_conv

    # Convolutional layer on array with WS mapping
    def convolve2D_wsab(self, image, kernel, bias, padding, strides, batch, ifmap, ofmap, idim, knl, ncol, nrow):
        xKernShape = knl
        yKernShape = knl
        xImgShape = idim
        yImgShape = idim

        # Shape of Output Convolution
        xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
        yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
        output = np.zeros((batch, ofmap, xOutput, yOutput))

        # Number of weight block partitions to fit into hardware
        block_col = int(np.ceil(ofmap/ncol))
        block_row = int(np.ceil(knl*knl*ifmap/nrow))
        kernel_flat = np.zeros((block_col*ncol, block_row*nrow))
        
        kernel_flat[0:ofmap,0:ifmap*knl*knl] = torch.reshape(kernel, [ofmap, ifmap*knl*knl]).cpu().numpy()
        # Process image by image
        for b in range(batch):
            # Apply Equal Padding to All Sides
            if padding != 0:
                imagePadded = torch.zeros(ifmap, idim + padding * 2, idim + padding * 2)
                imagePadded[:, int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image[b]
            else:
                imagePadded = image[b]

            # Iterate through image
            image_block = np.zeros((block_row * nrow, xOutput, yOutput))
            otemp = torch.zeros(block_row, block_col*ncol, xOutput, yOutput)
            for bc in range(block_col):
                for br in range(block_row):
                    ktemp = torch.zeros(ncol,nrow)
                    ktemp = kernel_flat[ncol*bc:(bc+1)*ncol, nrow*br:(br+1)*nrow]
                    ktemp = torch.from_numpy(ktemp)

                    for y in range(yOutput):
                        for x in range(xOutput):
                            # Fetch image section x,y, bc,br
                            image_block[0:knl * knl * ifmap, x, y] = imagePadded[0:ifmap,
                                                                        strides * x: strides * x + xKernShape,
                                                                        strides * y: strides * y + yKernShape].reshape(
                                knl * knl * ifmap).cpu().numpy()

                            itemp = image_block[br*nrow:(br+1)*nrow, x, y].reshape(nrow)
                            itemp = torch.from_numpy(itemp)
                            # Replace this line with Arduino SPI function call
                            otemp[br, bc*ncol:(bc+1)*ncol, x, y] = self.array_fn(ktemp, itemp, dim=1)
                            # print("Batch:%d,BROW:%d,BCOL:%d,X:%d,Y:%d" % (b,br,bc,x,y))

            output[b] = torch.sum(otemp[:, 0:ofmap, :, :], dim=0) + (bias.reshape(ofmap, 1, 1).cpu()*torch.ones(xOutput, yOutput)).detach().numpy()
        return output



    # -------------------- RELU LAYER -------------------- #

    def relu6(self, x, min_val, max_val, relu_module):
        i = (x >= min_val) * x
        out_relu = (i <= max_val) * (i - max_val) + max_val
        so_relu = relu_module.output_scale

        # Apply fake quantization to relu1 output.
        out_relu = self.noscale_quant(out_relu, so_relu, 0, self.num_bits)
        return self.dequantize(out_relu, so_relu, 0)



    # -------------------- MAXPOOL LAYER -------------------- #

    def maxpool2d(self, x, batch, idim, ofmap, knl, padding=0):
        # Maxpool layer - downsample by knl x knl with maxpool (no quantization required for max function)
        return torch.from_numpy(self.maxpool2D_wsa(batch, x, idim, ofmap, knl, padding))


    # Maxpool layer on digital hardware
    def maxpool2D_wsa(self, batch, image, idim, ofmap, knl, padding):
        xKernShape = knl
        yKernShape = knl
        xImgShape = idim
        yImgShape = idim
        strides = knl
        # Shape of Output Convolution
        xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
        yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
        output = np.zeros((batch, ofmap, xOutput, yOutput))

        for b in range(batch):
            # Apply Equal Padding to All Sides
            if padding != 0:
                imagePadded = torch.zeros(ofmap, idim + padding * 2, idim + padding * 2)
                imagePadded[:, int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image[b]
            else:
                imagePadded = image[b]

            # Iterate through image
            for y in range(yOutput):
                for x in range(xOutput):
                    output[b, :, x, y] = torch.amax(
                            imagePadded[:, strides * x: strides * x + xKernShape, strides * y: strides * y + yKernShape], dim=(1,2)).detach().cpu().numpy()
        return output



    # -------------------- AVERAGE-POOL LAYER -------------------- #

    def avgpool2d(self, x, batch, idim, ofmap, knl, padding=0):
        # Avgpool layer - downsample by knl x knl with avgpool (no quantization required for max function)
        return torch.from_numpy(self.avgpool2D_wsa(batch, x, idim, ofmap, knl, padding))
  

    # Average-Pool layer on array with WS mapping
    def avgpool2D_wsa(self, batch, image, idim, ofmap, knl, padding):
        xKernShape = knl
        yKernShape = knl
        xImgShape = idim
        yImgShape = idim
        strides = knl

        # Shape of Output Convolution
        xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
        yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
        output = np.zeros((batch, ofmap, xOutput, yOutput))

        for b in range(batch):
            # Apply Equal Padding to All Sides
            if padding != 0:
                imagePadded = torch.zeros(ofmap, idim + padding * 2, idim + padding * 2)
                imagePadded[:, int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image[b]
            else:
                imagePadded = image[b]

            # Iterate through image
            for y in range(yOutput):
                for x in range(xOutput):
                    for channel in range(ofmap):
                        output[b, channel, x, y] = self.array_fn(imagePadded[channel, strides * x: strides * x + xKernShape, strides * y: strides * y + yKernShape].reshape(knl*knl),
                                                                        torch.ones(xKernShape*yKernShape))/(knl*knl)
        return output



    # -------------------- FULLY-CONNECTED LAYER -------------------- #

    def fc(self, x, batch, module, odim):
        sin_fc = module.input_scale.cpu()
        in_fcs = self.noscale_quant(x, sin_fc, 0, self.num_bits)
        sw_fc, filters_fc = self.scale_quant(module.weight.cpu(), self.num_bits)
        bias_fc = module.bias.cpu() / (sw_fc * sin_fc)


        # FC layer using (WS dataflow)
        out_fc = torch.from_numpy(self.fc_on_array(in_fcs, filters_fc, bias_fc, batch, odim, self.ncol, self.nrow))

        # FC output scaling
        out_fcs = out_fc * sin_fc * sw_fc

        so_fc = module.output_scale.cpu()
        # FC output fake quantization
        return self.dequantize(self.noscale_quant(out_fcs, so_fc, 0, self.num_bits), so_fc, 0).to(self.device)
  

    # Fully-Connected layer on array with WS mapping
    def fc_on_array(self, fc_input, filters, bias, batch, ofmap, ncol, nrow):
        output = np.zeros((batch, ofmap))
        for b in range(batch):
            # Iterate through image
            block_col = int(np.ceil(ofmap/ncol))
            block_row = int(np.ceil(fc_input.size()[1]/nrow))

            filters_flat = np.zeros((block_col*ncol, block_row*nrow), dtype='int64')
            image_col = np.zeros((block_row*nrow), dtype='int64')

            filters_flat[0:ofmap,0:fc_input.size()[1]] = torch.reshape(filters, [ofmap, fc_input.size()[1]]).cpu().numpy()
            image_col[0:fc_input.size()[1]] = fc_input[b, :]

            otemp = torch.zeros(block_row, block_col*ncol)

            for bc in range(block_col):
                for br in range(block_row):
                    ftemp = torch.zeros(ncol,nrow)
                    ftemp = filters_flat[ncol*bc:(bc+1)*ncol, nrow*br:(br+1)*nrow]
                    ftemp = torch.from_numpy(ftemp)

                    itemp = image_col[br*nrow:(br+1)*nrow].reshape(nrow)
                    itemp = torch.from_numpy(itemp)

                    for col in range(ncol):
                    # Replace this line with Arduino SPI function call
                        otemp[br, (bc*ncol)+col] = self.array_fn(ftemp[col, :], itemp)
                    # print("Batch:%d,BROW:%d,BCOL:%d,X:%d,Y:%d" % (b,br,bc,x,y))
            output[b] = torch.sum(otemp[:, 0:ofmap], dim=0) + (bias.reshape(ofmap).cpu()*torch.ones(ofmap)).detach().numpy()
        return output
    


    # -------------------- QUANTIZATION NODES -------------------- #
    
    # 'Fake' Quantization function [Jacob et. al]
    def quantize(self, real_value, scale, zero_point, qmin, qmax):
        transformed_val = zero_point + real_value / scale
        clamped_val = torch.clamp(transformed_val, qmin, qmax)
        quantized_val = torch.round(clamped_val)
        return quantized_val


    # 'Fake' Dequantization function [Jacob et. al]
    def dequantize(self, quantized_val, scale, zero_point):
        real_val = scale * (quantized_val - zero_point)
        return real_val


    # Quantize with scaling function (Jacob et. al)
    def scale_quant(self, real_value, num_bits):
        qmin = -(2 ** (num_bits - 1) - 1)
        qmax = 2 ** (num_bits - 1) - 1
        abs_max = torch.abs(real_value).max()
        scale = abs_max / (float(qmax - qmin) / 2)
        zero_point = 0
        quant = self.quantize(real_value, scale, zero_point, qmin, qmax)
        return scale, quant


    # Quantize with no scaling function (Jacob et. al)
    def noscale_quant(self, real_value, scale, zero_point, num_bits):
        qmin = -(2 ** (num_bits - 1) - 1)
        qmax = 2 ** (num_bits - 1) - 1
        quant = self.quantize(real_value, scale, zero_point, qmin, qmax)
        return quant



    # -------------------- TYPES OF MACS -------------------- #

    # Linear
    def linear(self, kernel, image, col=0, dim=0):
        return torch.sum(kernel*image, dim=dim, dtype=torch.int64)


    # Non-linear look-up
    def from_table(self, kernel, image):
        output = np.empty(len(kernel))
        if len(kernel.shape) == 2:
            for i in range(len(kernel)):
                output[i] = self.lookup_table(kernel[i, :].tolist(), image.tolist())
            return torch.from_numpy(output)
        else:
            output = self.lookup_table(kernel.tolist(), image.tolist())
            return output
        
    # Excel lookup table
    def lookup_table(self, kernel, image, col=0, dim=0):
        sum = 0
        if self.num_bits == 9 or self.num_bits == 8:
            bit = 9
        else:
            bit = 5
        for i in range(len(kernel)):
            sum = sum + self.nl_mult[int(kernel[i]+(2**(bit-1))-1)][int(image[i]+(2**(bit-1))-1)]
        return sum


    # Gain/Non-linear
    def gain_nl(self, kernel, image, col=0, dim=0):
        a1 = self.mac_constants[0]
        a3 = self.mac_constants[1]
        return torch.sum(image*((a1*kernel) + a3*(kernel**3)), dim=dim, dtype=torch.int64)
    

    # Thermal Noise
    def noise(self, kernel, image, col=0, dim=0):
        sigma = self.mac_constants
        noise = torch.from_numpy(np.random.normal(0, 1, kernel.shape))*torch.sqrt(torch.abs(kernel))*sigma
        return torch.sum(image * (kernel + noise), dim=dim, dtype=torch.int64)
    


    # -------------------- TYPES OF ARRAYS -------------------- #

    # Regular array
    def array(self, kernel, image, col=0, dim=0):
        return self.mac_fn(kernel, image, col, dim)
        

    # PPQ array
    def ppq_array(self, kernel, image, col=0, dim=0):
        if len(kernel.shape) == 2:
            kernel_l = torch.empty((kernel.shape[0], kernel.shape[1]))
            kernel_u = torch.empty((kernel.shape[0], kernel.shape[1]))
            i = 0
            for channel in kernel:
                kernel_u[i], kernel_l[i] = self.slice_input(channel)
            i += 1
        else:
            kernel_u, kernel_l = self.slice_input(kernel)
            image_u, image_l = self.slice_input(image)
        
        result = torch.add(torch.add(self.mac_fn(kernel_l, image_l, dim=dim), (self.mac_fn(kernel_u, image_l, dim=dim)
                                                        + self.mac_fn(kernel_l, image_u, dim=dim))<<4), (self.mac_fn(kernel_u, image_u, dim=dim))<<8)
        return result
    

    # Slice input for PPQ
    def slice_input(self, array):
        array = array.int()
        up_array = np.sign(array)*(abs(array)&np.int16(240))>>4
        low_array = np.sign(array)*(abs(array)&np.int16(15))
        return up_array, low_array
        

    # Mismatched array
    def mismatched_array(self, kernel, image, col=0, dim=0):
        if len(kernel.shape) == 2:
            return torch.sum(image * (self.gain_mismatch*kernel + self.offset_mismatch*kernel), dim=dim, dtype=torch.int64)
        else:
            return torch.sum(image * (self.gain_mismatch[col]*kernel + self.offset_mismatch[col]*kernel), dim=dim, dtype=torch.int64)
    