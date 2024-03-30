# Software

Directory containing all the Training and Forward-Pass end of the Hardware-Software Structure

## Training

Both the MNIST and CIFAR-10 CNNs share a similar structure: two convolutional layers, each with a ReLU and Maxpool layer, followed by two Fully Connected layers. The only difference is the CIFAR-10 CNN also has Dropout layers after each Maxpool layer. This structure is contained in the naive_.\*.py files.

![MNIST and CIFAR-10 CNN Structures](Figures/CNNstructComp.png?raw=true)

The code is mostly generalized for ease of switching between datasets, but note a few small changes may be present if you decide to extend to a different dataset. For  instance, the targets for the MNIST dataset are held in a tensor, while for CIFAR-10 they are held in a list.

The datasets are trained for 10 epochs, again changeable if required in each notebook. The trained model will be outputted as .\*_model.pth. This model is what will be read in by the Forward Pass.

## Forward Pass Classes

The notebooks for the forward pass contains reference to a forwardPass class: This is an inherited class of the hardware class. 

<p align="center">
  <img src="Figures/classStructure.png?raw=true"  width=600">
</p>

The hardware class contains functions to mimic hardware: CNN Layers mapped to an array, quantize and dequantize nodes, non-ideal MACs and arrays. This class should be changed if you want to remodel the hardware functions, create new layers, or model new non-idealities.

The forwardPass class contains a description of the network structure (similar to naive_.\*.py): The layer logic and the placement of quantization nodes. This is the class to change quantization level, hardware dimensions, or layer logic.

<p align="center">
  <img src="Figures/analogNonLinearity.png?raw=true"  width=600">
</p>

The forward pass notebooks provide testing capability for the Hardware Aware Evaluation. The hardware class provides ability to test linear, PPQ, and mismatched arrays, with linear, gain-limited/non-linear, noisy, and custom datasheet MACs. Comments instruct the user on how to choose the setup they require, and feed in values.

Note the files prefixed with "SINGLE_NB_", these are old versions of the forward pass which contain all the classes in one file. While less structured and more cluttered, these files are entirely self-contained. The disadvantage to the class structure is seen if one is modifying either class file: The notebook's kernel must be restarted each time to implement the changes. Using a single file, the kernel does not need to be reset, speeding up debugging.

## Using Google Colab

When using [Google Colab](https://colab.research.google.com/drive/1vEENyFYD09R2yWCXvbNjc2Sqhw4Rlqbs?usp=sharing), it is important to run the forward pass on a CPU runtime (GPUs will not work with the hardware class). 

<p align="center">
  <img src="Figures/colabRuntime.png?raw=true"  width=600">
</p>

Be sure to begin the notebook with a cell containing "*!pip install nni==2.10.1*" to install the correct version of NNI. Using the Files tab on the left side of the screen, upload the files needed (hardware class, forward pass class, quantized network model, naive model).

<p align="center">
  <img src="Figures/colabFiles.png?raw=true"  width=600">
</p>
