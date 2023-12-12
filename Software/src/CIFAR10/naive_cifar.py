import torch
import torch.nn.functional as F


# Simple convolutional neural network architecture for CIFAR-10 (>68% accuracy)

# Pytorch NaiveModel class
# CONV1: 32 5x5 filters
# RELU1
# MAXPOOL1: 2x2
# DROPOUT1: 0.5
# CONV2: 64 5x5 filters
# RELU2: 2x2
# MAXPOOL2
# DROPOUT2: 0.5

# FC1: 1600 -> 100 
# RELU3
# FC2: 100 -> 10

# SOFTMAX

class NaiveModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(3, 32, 5)
        self.conv2 = torch.nn.Conv2d(32, 64, 5)
        self.fc1 = torch.nn.Linear(5 * 5 * 64, 100)
        self.fc2 = torch.nn.Linear(100, 10)
        self.relu1 = torch.nn.ReLU6()
        self.relu2 = torch.nn.ReLU6()
        self.relu3 = torch.nn.ReLU6()
        self.max_pool1 = torch.nn.MaxPool2d(2, 2)
        self.max_pool2 = torch.nn.MaxPool2d(2, 2)
        self.dropout1 = torch.nn.Dropout(0.5)
        self.dropout2 = torch.nn.Dropout(0.5)

    def forward(self, x):
        x = self.relu1(self.conv1(x))
        x = self.max_pool1(x)
        x = self.dropout1(x)
        x = self.relu2(self.conv2(x))
        x = self.max_pool2(x)
        x = self.dropout2(x)
        x = x.view(-1, x.size()[1:].numel())
        x = self.relu3(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
