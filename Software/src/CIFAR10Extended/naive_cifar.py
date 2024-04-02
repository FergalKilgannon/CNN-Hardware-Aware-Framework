import torch
import torch.nn.functional as F


# Simple convolutional neural network architecture for CIFAR-10 (>64% accuracy)

# Pytorch NaiveModel class
# CONV1: 32 5x5 filters
# RELU1
# MAXPOOL1: 2x2
# DROPOUT1: 0.5
# CONV2: 64 5x5 filters
# RELU2: 2x2
# MAXPOOL2
# DROPOUT2: 0.5

# FC1: 1600 -> 128 
# RELU3
# FC2: 128 -> 10

# SOFTMAX

class NaiveModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(3, 32, 3, padding='same')
        self.conv2 = torch.nn.Conv2d(32, 32, 3, padding='same')
        self.conv3 = torch.nn.Conv2d(32, 64, 3, padding='same')
        self.conv4 = torch.nn.Conv2d(64, 64, 3, padding='same')
        self.conv5 = torch.nn.Conv2d(64, 128, 3, padding='same')
        self.conv6 = torch.nn.Conv2d(128, 128, 3, padding='same')

        self.fc1 = torch.nn.Linear(4 * 4 * 128, 128)
        self.fc2 = torch.nn.Linear(128, 10)

        self.relu1 = torch.nn.ReLU6()
        self.relu2 = torch.nn.ReLU6()
        self.relu3 = torch.nn.ReLU6()
        self.relu4 = torch.nn.ReLU6()
        self.relu5 = torch.nn.ReLU6()
        self.relu6 = torch.nn.ReLU6()
        self.relu7 = torch.nn.ReLU6()

        self.max_pool1 = torch.nn.MaxPool2d(2, 2)
        self.max_pool2 = torch.nn.MaxPool2d(2, 2)
        self.max_pool3 = torch.nn.MaxPool2d(2, 2)

        self.dropout1 = torch.nn.Dropout(0.3)
        self.dropout2 = torch.nn.Dropout(0.5)
        self.dropout3 = torch.nn.Dropout(0.5)
        self.dropout4 = torch.nn.Dropout(0.5)

    def forward(self, x):
        x = self.relu1(self.conv1(x))
        x = self.relu2(self.conv2(x))
        x = self.max_pool1(x)
        x = self.dropout1(x)

        x = self.relu3(self.conv3(x))
        x = self.relu4(self.conv4(x))
        x = self.max_pool2(x)
        x = self.dropout2(x)

        x = self.relu5(self.conv5(x))
        x = self.relu6(self.conv6(x))
        x = self.max_pool3(x)
        x = self.dropout3(x)

        x = x.view(-1, x.size()[1:].numel())
        x = self.relu7(self.fc1(x))
        x = self.dropout4(x)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
