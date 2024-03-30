import torch
import torch.nn.functional as F
from hardwareClass import hardware
from naive_mnist import NaiveModel
from nni.algorithms.compression.pytorch.quantization import QAT_Quantizer
from nni.compression.pytorch.quantization.settings import set_quant_scheme_dtype

class forwardPass(hardware):
    def __init__(self, device, idim, ifmap, array_choice, mac_choice, mac_constants, trained_model_path):
        self.num_bits = 8               # Chosen quantization level
        stride = 1                      # Convolutional stride
        ncol = 16                       # Number of hardware columns
        nrow = 32                       # Number of hardware rows
        self.knl = 5                    # Kernel size (declared here to automate layer output image sizes below)

        self.idim = idim                # Input image dimensions (found from data) 
        self.ifmap = ifmap              # Input image channels (found from data)
        self.device = device
        self.model = self.quantize_model(trained_model_path)

        super().__init__(self.model, self.num_bits, stride, ncol, nrow, self.device, array_choice, mac_choice, mac_constants)

    def forward_pass(self, data, batch):
        # Scale input
        s_in, x = self.scale_quant(data, self.num_bits)
        
        # Convolutional layer 1
        x = self.conv2d(x, batch, self.model.conv1.module, s_in, self.idim, 1, 16, self.knl)

        # ReLU 1
        x = self.relu6(x, 0, 6, self.model.relu1.module)

        # Maxpool layer 1
        x = self.maxpool2d(x, batch, self.idim - self.knl + 1, 16, 2)
        
        # Scale for convolutional layer 2
        sin_conv2 = self.model.conv2.module.input_scale
        x = self.noscale_quant(x, sin_conv2.cpu(), 0, self.num_bits)
        x = self.conv2d(x, batch, self.model.conv2.module, sin_conv2, (self.idim-self.knl+1)/2, 16, 32, self.knl)

        # ReLU 2
        x = self.relu6(x, 0, 6, self.model.relu2.module)

        # Maxpool layer 2
        x = self.maxpool2d(x, batch, ((self.idim - self.knl+1)/2) - self.knl + 1, 32, 2)

        # Fully connected layer 1
        x = x.view(-1, x.size()[1:].numel())  # Flatten outputs of out_maxpool2 layer to feed to FC layers.
        x = self.fc(x, batch, self.model.fc1.module, 50)

        # ReLU 3
        x = self.relu6(x, 0, 6, self.model.relu3.module)

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
            'op_names': ['conv1', 'conv2']
        }, {
            'quant_types': ['output'],
            'quant_bits': {'output': self.num_bits},
            'quant_start_step': 2,
            'op_names': ['relu1', 'relu2', 'relu3']
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