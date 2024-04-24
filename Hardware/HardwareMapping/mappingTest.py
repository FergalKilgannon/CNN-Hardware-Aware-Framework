import numpy as np

class mappingTests:
    def __init__(self, iX, iY, iChannels, bitAccuracy, ppq=False):
        self.iX = iX
        self.iY = iY
        self.iChannels = iChannels
        self.bitAccuracy = bitAccuracy
        self.ppq = ppq

    ## ------------ ONLY CLASS NEED TO CHANGE IF USING DIFFERENT NETWORK ------------ ##
    # Forward Pass designed for MNIST (2 convolutional layers)
    def forward_pass(self, testFunction, nrow, ncol, ndepth):
        chosenFunction = getattr(self, testFunction)

        count = 0

        # Convolutional layer 1 (16 kernels, 5x5)
        count += chosenFunction(nrow, ncol, ndepth, self.iX, self.iY, self.iChannels, 16, 5, 5)

        # Rescale (5x5 kernels, 2x2 maxpooling)
        nextX, nextY = self.rescale(self.iX, self.iY, 5, 5, 2) 
        
        # Convolutional layer 2 (32 kernels, 5x5)
        count += chosenFunction(nrow, ncol, ndepth, nextX, nextY, 16, 32, 5, 5)

        return count

    # Counts for weight stationary
    def ws_counts(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding, strides):
        if self.ppq:
            nrow = nrow/4
            ncol = ncol/4
            ppqDigital = 6
            bitAccuracy = self.bitAccuracy/2
        else:
            ppqDigital = 0
            bitAccuracy = self.bitAccuracy

        MBytesPerData = bitAccuracy/(8*(1*10**6))

        # Shape of Output Convolution
        xOutput = int(((image_x_size - kernel_x_size + 2 * padding) / strides) + 1)
        yOutput = int(((image_y_size - kernel_y_size + 2 * padding) / strides) + 1)

        # Number of weight block partitions to fit into hardware
        block_col = int(np.ceil(kernels/(ncol*ndepth)))
        block_row = int(np.ceil(kernel_x_size*kernel_y_size*image_channels/(nrow)))

        data_moved_count = 0
        mac_completed_count = 0
        digital = 0

        block_loop = block_col*block_row
        output_loop = yOutput*xOutput

        # Load new data onto block
        data_moved_count += nrow*ncol*ndepth*MBytesPerData*block_loop
        
        # Fetch image section
        data_moved_count += kernel_x_size*kernel_y_size*image_channels*MBytesPerData*block_loop*output_loop

        # Complete MAC
        data_moved_count += ncol*ndepth*((bitAccuracy*2)-1)/(8*(1*10**6))*block_loop*output_loop
        mac_completed_count += ncol*ndepth*block_loop*output_loop
        digital += ppqDigital*block_loop*output_loop

        digital += block_loop
        return data_moved_count, mac_completed_count, digital

    # Counts for output stationary
    def os_counts(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding, strides):
        if self.ppq:
            nrow = nrow/4
            ncol = ncol/4
            ppqDigital = 6
            bitAccuracy = self.bitAccuracy/2
        else:
            ppqDigital = 0
            bitAccuracy = self.bitAccuracy

        MBytesPerData = self.bitAccuracy/(8*(1*10**6))

        # Shape of Output Convolution
        xOutput = int(((image_x_size - kernel_x_size + 2 * padding) / strides) + 1)
        yOutput = int(((image_y_size - kernel_y_size + 2 * padding) / strides) + 1)

        
        # Number of weight block partitions to fit into hardware
        block_col = int(np.ceil(xOutput/ncol))
        block_row = int(np.ceil(kernel_x_size*kernel_y_size*image_channels/(nrow)))

        data_moved_count = 0
        mac_completed_count = 0
        digital = 0

        block_loop = block_col*block_row*yOutput
        output_loop = yOutput*xOutput

        # Load new data onto block
        data_moved_count += nrow*ncol*ndepth*MBytesPerData*block_loop

        # Fetch kernels
        data_moved_count += nrow*ndepth*MBytesPerData*block_loop*kernels

        # Complete MAC
        mac_completed_count += 1*block_loop*kernels*output_loop
        data_moved_count += ((bitAccuracy*2)-1)/(8*(1*10**6))*block_loop*kernels*output_loop
        digital += ppqDigital*block_loop*kernels*output_loop

        digital += block_row*block_col
        return data_moved_count, mac_completed_count, digital

    # Speed of inference for weight stationary
    def ws_speed(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding=0, strides=1):
        if self.ppq:
            nrow = nrow/4
            ncol = ncol/4

        # Shape of Output Convolution
        xOutput = int(((image_x_size - kernel_x_size + 2 * padding) / strides) + 1)
        yOutput = int(((image_y_size - kernel_y_size + 2 * padding) / strides) + 1)

        # Number of weight block partitions to fit into hardware
        block_col = int(np.ceil(kernels/ncol))
        block_row = int(np.ceil(kernel_x_size*kernel_y_size*image_channels/nrow))

        return block_col*block_row*xOutput*yOutput/ndepth

    # Speed of inference for output stationary
    def os_speed(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding=0, strides=1):
        if self.ppq:
            nrow = nrow/4
            ncol = ncol/4

        # Shape of Output Convolution
        xOutput = int(((image_x_size - kernel_x_size + 2 * padding) / strides) + 1)
        yOutput = int(((image_y_size - kernel_y_size + 2 * padding) / strides) + 1)

        
        # Number of weight block partitions to fit into hardware
        block_col = int(np.ceil(xOutput/ncol))
        block_row = int(np.ceil(kernel_x_size*kernel_y_size*image_channels/nrow))
        block_depth = int(np.ceil(yOutput/ndepth))

        return block_col*block_row*block_depth*kernels
    
    # Rescale after convolutional layer, options for padding and pooling
    def rescale(self, iX, iY, kernel_x_size, kernel_y_size, pool, padding=0, strides=1):
        return int(((iX - kernel_x_size + 2 * padding) / strides) + 1)/pool, int(((iY - kernel_y_size + 2 * padding) / strides) + 1)/pool
    
    # Data, MAC, and digital counts for both WS and OS mappings
    def ws_data_count(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding=0, strides=1):
        return self.ws_counts(nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding, strides)[0]
    
    def os_data_count(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding=0, strides=1):
        return self.os_counts(nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding, strides)[0]
    
    def ws_mac_count(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding=0, strides=1):
        return self.ws_counts(nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding, strides)[1]
    
    def os_mac_count(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding=0, strides=1):
        return self.os_counts(nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding, strides)[1]
    
    def ws_digital_count(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding=0, strides=1):
        return self.ws_counts(nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding, strides)[2]
    
    def os_digital_count(self, nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding=0, strides=1):
        return self.os_counts(nrow, ncol, ndepth, image_x_size, image_y_size, image_channels, kernels, kernel_x_size, kernel_y_size, padding, strides)[2]