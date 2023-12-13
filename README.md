# CNN Hardware Software Codesign
 Fergal Kilgannon ME Thesis Project 23-24
 
 Repository is split into "Software" and "Hardware":
 
 ## SOFTWARE
 
 Within the software source, there is the MNIST CNN (handwritten greyscale numbers) and the CIFAR-10 CNN (coloured objects) directories. Each of these has a training notebook, and a forward pass notebook. Each also has a trained model and a CNN structure python file. Note that when running locally, the data will be downloaded to these directories, but not included in the GIT repo.
 
 A third directory named "HardwareSpec" contains spreadsheets mapping the outputs for the 4x4 and 8x8 MAC results. Any further results should be placed in this folder, and referenced in the notebooks.
