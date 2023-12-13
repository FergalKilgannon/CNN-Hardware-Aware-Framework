# Software

Directory containing all the Training and Forward-Pass end of the Hardware-Software Structure

## Training

Both the MNIST and CIFAR-10 CNNs share a similar structure: two convolutional layers, each with a ReLU and Maxpool layer, followed by two Fully Connected layers. The only difference is the CIFAR-10 CNN also has Dropout layers after each Maxpool layer. This structure is contained in the naive_\*.py files.

![MNIST and CIFAR-10 CNN Structures](../Figures/CNNstructComp.png?raw=true)

NNI is used to quantize the trained network (using QAT). Be sure to select the appropriate bit quantization by changing the "num_bits" variable. For now, there are also mentions of input image sizes hardcoded in, I'm looking to generalize the code not to need these. For the timebeing, instances of (1, 1, 28, 28) in MNIST (1 input channel, 28x28 images) are changed to (1, 3, 32, 32) for CIFAR-10 (3 input channels, 32x32 images). You'll need to account for input dimensions if testing with another dataset.

The datasets are trained for 10 epochs, again changeable if required in each notebook. The trained model will be outputted as \*_model.pth. This model is what will be read in by the Forward Pass.
