# Hardware

Directory containing all the Training and Forward-Pass end of the Hardware-Software Structure

## Verilog

The grid of MACs is to be created in Verilog, where the MAC can be tested in Cadence within the context of a convolutional layer hardware, or different data-mapping strategies can be tested for power usage.

![Block Diagram of Convolutional Layer Hardware](Figures/rtlLayout.png?raw=true)

The aim is to keep the grid hardware fixed, and vary the co-processor hardware for different usage.

## PYNQ

The real-world test case will be controlled by a Xilinx PYNQ-ZU board. The board will hold the forward-pass code, and will ideally pass SPI calls out to the taped-out MAC, and take in user input (through mouse, trackpad, or camera).