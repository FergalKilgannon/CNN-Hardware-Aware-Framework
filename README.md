# CNN Hardware Software Codesign
Fergal Kilgannon ME Thesis Project 23-24
 
Repository is split into "Software" and "Hardware":
 
## SOFTWARE
 
Within the software source, there is the MNIST CNN (handwritten greyscale numbers) and the CIFAR-10 CNN (coloured objects) directories. Each of these has a training notebook, a forward pass notebook, forward pass and hardware classes, trained models, and CNN structure files.  Note that when running locally, the datasets will be downloaded to these directories, but not included in the GIT repo.
 
A third directory named "HardwareSpec" contains spreadsheets mapping the outputs for the 4x4 and 8x8 MAC results. Any further results should be placed in this folder, and referenced in the notebooks.

## HARDWARE

The hardware directory will have both a Verilog and PYNQ directory, the former with .V files describing the grid hardware, and the latter with the Python notebooks to control the CNN on a PYNQ board.