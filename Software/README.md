# Software

Directory containing all the Training and Forward-Pass end of the Hardware-Software Structure

## Training

Both the MNIST and CIFAR-10 CNNs share a similar structure: two convolutional layers, each with a ReLU and Maxpool layer, followed by two Fully Connected layers. The only difference is the CIFAR-10 CNN also has Dropout layers after each Maxpool layer. This structure is contained in the naive_.\*.py files.

![MNIST and CIFAR-10 CNN Structures](Figures/CNNstructComp.png?raw=true)

NNI is used to quantize the trained network (using QAT). Be sure to select the appropriate bit quantization by changing the "num_bits" variable. The code is mostly generalized for ease of switching between datasets, but note a few small changes may be present if you decide to extend to a different dataset. For  instance, the targets for the MNIST dataset are held in a tensor, while for CIFAR-10 they are held in a list.

The datasets are trained for 10 epochs, again changeable if required in each notebook. The trained model will be outputted as .\*_model.pth. This model is what will be read in by the Forward Pass.

## Forward Pass

The Forward Pass notebooks are noticeably longer than the Training, as the hardware functions are now totally described. The forward pass is contained in a class, seen in second cell of the notebook. This class contains all the hyperparameters of the forward pass model. The first associated function of the class is where the layer structure is described. If you follow alongside the naive_.\*.py file, you'll see the structure is very similar, except with the QAT accounted for in some instances. This is where one would alter the structure if they decided upon a different network.

If one's aims instead were to test non-linear hardware components, the class functions following this all refer to the different layers, mimicking their hardware structure. This instance has a non-linear function (at the end of the cell), for Matrix-Vector-Multiplication. This function is called within the custom conv2d function. This can be taken out and the standard linear version swapped in easily (the linear alternative is commented out the line above the non-linear function call). Use this example as inspiration to chop-and-change wherever in the hardware.

Note that while using this look-up table method of modelling non-idealities, the code will run very slowly (one iteration takes roughly 6 minutes for MNIST and 25 minutes for CIFAR-10).