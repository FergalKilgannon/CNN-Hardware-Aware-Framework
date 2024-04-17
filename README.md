# CNN Hardware Software Codesign
Fergal Kilgannon ME Thesis Project 23-24
 
Repository is split into "Software" and "Hardware". More information on each is available in READMEs conatined in the respective directories.
 
## SOFTWARE

The software source contains code and notebooks to **train** and complete the **forward-pass** for three networks: a simple 6-layer MNIST CNN, simple 6-layer CIFAR-10 CNN, and extended 11-layer CIFAR-10 CNN. Note that when running locally, respective datasets will be downloaded to these directories, but not included in the GIT repo.
 
A third directory named "HardwareSpec" contains spreadsheets mapping the outputs for the 4x4 and 8x8 MAC results. Any further results should be placed in this folder, and referenced in the notebooks.

## HARDWARE

The hardware directory has a Hardware Mapping, Verilog, and PYNQ directory. The HardwareMapping directory contains a notebook with functions to test different mapping techniques, and plots the results.

The Verilog and PYNQ directories have starter code for further work: The former with .V files describing the grid hardware, and the latter with the Python notebooks to control the CNN on a PYNQ board. This latter contains a notebook *ForwardPass.ipynb* which can run a single MNIST forward-pass using input from the user, and is good for use in monitoring data movement of the network.
