import torch
import torch.nn.functional as F
from hardwareClass import hardware
from naive_cifar import NaiveModel
from nni.algorithms.compression.pytorch.quantization import QAT_Quantizer
from nni.compression.pytorch.quantization.settings import set_quant_scheme_dtype

class forwardPass(hardware):
    def __init__(self, device, idim, ifmap, array_choice, mac_choice, mac_constants, trained_model_path):
        self.num_bits = 16              # Chosen quantization level
        stride = 1                      # Convolutional stride
        ncol = 64                       # Number of hardware columns
        nrow = 64                       # Number of hardware rows
        self.knl = 3                    # Kernel size (declared here to automate layer output image sizes below)

        self.idim = idim                # Input image dimensions (found from data) 
        self.ifmap = ifmap              # Input image channels (found from data)
        self.device = device
        self.model = self.quantize_model(trained_model_path)

        super().__init__(self.model, self.num_bits, stride, ncol, nrow, self.device, array_choice, mac_choice, mac_constants)

    def forward_pass(self, data, batch):
        # Scale input
        s_in, x = self.scale_quant(data, self.num_bits)
        
        # Convolutional layer 1
        x = self.conv2d(x, batch, self.model.conv1.module, s_in, self.idim, 3, 32, self.knl, padding=1)
        # ReLU 1
        x = self.relu6(x, 0, 6, self.model.relu1.module)
        # Scale for convolutional layer 2
        sin_conv2 = self.model.conv2.module.input_scale
        x = self.noscale_quant(x, sin_conv2.cpu(), 0, self.num_bits)
        x = self.conv2d(x, batch, self.model.conv2.module, sin_conv2, self.idim, 32, 32, self.knl, padding=1)
        # ReLU 2
        x = self.relu6(x, 0, 6, self.model.relu2.module)
        # Maxpool layer 1
        x = self.maxpool2d(x, batch, self.idim, 32, 2)
        
        # Scale for convolutional layer 3
        sin_conv3 = self.model.conv3.module.input_scale
        x = self.noscale_quant(x, sin_conv3.cpu(), 0, self.num_bits)
        x = self.conv2d(x, batch, self.model.conv3.module, sin_conv3, int(self.idim/2), 32, 64, self.knl, padding=1)
        # ReLU 3
        x = self.relu6(x, 0, 6, self.model.relu3.module)
        # Scale for convolutional layer 4
        sin_conv4 = self.model.conv4.module.input_scale
        x = self.noscale_quant(x, sin_conv4.cpu(), 0, self.num_bits)
        x = self.conv2d(x, batch, self.model.conv4.module, sin_conv4, int(self.idim/2), 64, 64, self.knl, padding=1)
        # ReLU 4
        x = self.relu6(x, 0, 6, self.model.relu4.module)
        # Maxpool layer 2
        x = self.maxpool2d(x, batch, int(self.idim/2), 64, 2)

        # Scale for convolutional layer 5
        sin_conv5 = self.model.conv5.module.input_scale
        x = self.noscale_quant(x, sin_conv5.cpu(), 0, self.num_bits)
        x = self.conv2d(x, batch, self.model.conv5.module, sin_conv5, int(self.idim/4), 64, 128, self.knl, padding=1)
        # ReLU 5
        x = self.relu6(x, 0, 6, self.model.relu5.module)
        # Scale for convolutional layer 6
        sin_conv6 = self.model.conv6.module.input_scale
        x = self.noscale_quant(x, sin_conv6.cpu(), 0, self.num_bits)
        x = self.conv2d(x, batch, self.model.conv6.module, sin_conv6, int(self.idim/4), 128, 128, self.knl, padding=1)
        # ReLU 6
        x = self.relu6(x, 0, 6, self.model.relu6.module)
        # Maxpool layer 3
        x = self.maxpool2d(x, batch, int(self.idim/4), 128, 2)

        # Fully connected layer 1
        x = x.view(-1, x.size()[1:].numel())  # Flatten outputs of out_maxpool2 layer to feed to FC layers.
        x = self.fc(x, batch, self.model.fc1.module, 128)

        # ReLU 7
        x = self.relu6(x, 0, 6, self.model.relu7.module)

        # Fully connected layer 2
        x = self.fc(x.cpu(), batch, self.model.fc2.module, 10)

        # Softmax layer
        return F.log_softmax(x, dim=1)
    

    def quantize_model(self, trained_model_path):
        # Make sure this matches quantization config from MNIST_CNN_Training
        configure_list = [{
            'quant_types': ['weight', 'input'],
            'quant_bits': {'weight': self.num_bits, 'input': self.num_bits},
            'quant_start_step': 2,
            'op_names': ['conv1', 'conv2', 'conv3', 'conv4', 'conv5', 'conv6']
        }, {
            'quant_types': ['output'],
            'quant_bits': {'output': self.num_bits},
            'quant_start_step': 2,
            'op_names': ['relu1', 'relu2', 'relu3', 'relu4', 'relu5', 'relu6', 'relu7']
        }, {
            'quant_types': ['output', 'weight', 'input'],
            'quant_bits': {'output': self.num_bits, 'weight': self.num_bits, 'input': self.num_bits},
            'quant_start_step': 2,
            'op_names': ['fc1', 'fc2'],
        }]

        set_quant_scheme_dtype('weight', 'per_tensor_symmetric', 'int')
        set_quant_scheme_dtype('output', 'per_tensor_symmetric', 'int')
        set_quant_scheme_dtype('input', 'per_tensor_symmetric', 'int')

        # Create a NaiveModel object and apply QAT_Quantizer setup
        qmodel = NaiveModel().to(self.device)
        dummy_input = torch.randn(1, self.ifmap, self.idim, self.idim).to(self.device)
        optimizer = torch.optim.SGD(qmodel.parameters(), lr=0.01, momentum=0.5)
        # To enable batch normalization folding in the training process, you should
        # pass dummy_input to the QAT_Quantizer.
        quantizer = QAT_Quantizer(qmodel, configure_list, optimizer, dummy_input=dummy_input)
        quantizer.compress()

        # Load trained model (from MNIST_CNN_Training step).
        state = torch.load(trained_model_path, map_location=self.device)
        qmodel.load_state_dict(state, strict=True)
        return qmodel.eval()