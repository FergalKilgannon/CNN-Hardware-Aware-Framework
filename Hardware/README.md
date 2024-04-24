# Hardware

Directory containing all the Training and Forward-Pass end of the Hardware-Software Structure

## Mapping

A Python class named hardwareTests provides lightweight testing capabilities. The forward-pass for any network can be modelled in the class, and an example notebook is provided to demonstrate how this class can be used for testing. Note that the mapping techniques are only relevant for the convolutional layers, so the only modelling to be done in the class is for these layers, and rescaling between them (pooling, padding, etc.).

## Verilog

The grid of MACs is to be created in Verilog, where the MAC can be tested in Cadence within the context of a convolutional layer hardware, or different data-mapping strategies can be tested for power usage.

<p align="center">
  <img src="Figures/rtlLayout.png?raw=true"  width=400">
</p>


The aim is to keep the grid hardware fixed, and vary the co-processor hardware for different usage.

## PYNQ

The real-world test case will be controlled by a Xilinx PYNQ-ZU board. The board will hold the forward-pass code, and will ideally pass SPI calls out to the taped-out MAC, and take in user input (through mouse, trackpad, or camera).

For testing the PYNQ board, a modified version of the forward pass notebook is used, which asks the user to draw a number, and predicts what the user has drawn. With just one input, this is not used for hardware-aware evaluation, but has in mind a real use-case scenario to test the PYNQ board and taped-out MACs. Another advantage to using this single-data forward pass is to observe the data movement through layers. Looking at the convolutional layer, you will see tracking variables and print statements following the data movement to and from memory.

Installing NNI on the PYNQ board proved troublesome, so instead a notebook to retrieve model parameters is seen (FPgetModel) and a notebook to complete the forward pass without NNI using this obtained model (ForwardPassNoNNI).