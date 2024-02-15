import torch
import torch.nn.functional as F


# Simple convolutional neural network architecture for MNIST (>98% accuracy)

# Pytorch NaiveModel class
# CONV1: 16 5x5 filters
# RELU1
# MAXPOOL1: 2x2
# CONV2: 32 5x5 filters
# RELU2: 2x2
# MAXPOOL2

# FC1: 512 -> 50 
# RELU3
# FC2: 50 -> 10

# SOFTMAX

class NaiveModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(1, 16, 5, 1)
        self.conv2 = torch.nn.Conv2d(16, 32, 5, 1)
        self.fc1 = torch.nn.Linear(4 * 4 * 32, 50)
        self.fc2 = torch.nn.Linear(50, 10)
        self.relu1 = torch.nn.ReLU6()
        self.relu2 = torch.nn.ReLU6()
        self.relu3 = torch.nn.ReLU6()
        self.avg_pool1 = torch.nn.AvgPool2d(2, 2)
        self.avg_pool2 = torch.nn.AvgPool2d(2, 2)

    def forward(self, x):
        x = self.relu1(self.conv1(x))
        x = self.avg_pool1(x)
        x = self.relu2(self.conv2(x))
        x = self.avg_pool2(x)
        x = x.view(-1, x.size()[1:].numel())
        x = self.relu3(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
