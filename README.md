# Virtual Separation 
## Project to separate immunofluorescent markers 


This repository contains the code for the project 'Virtual separation of cellular markers wuth overlapping fluorescent spectra'

It contains:
- A few example datasets
- Codes to generate images
- ✨Deep learning using [pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)✨

## Structure

- Experiment 1
- Experiment 2
- Experiment 3
- General files 
- Others

Images or dataset are sometimes called AB. This means that it contains images that are a combination of A (conditional input) and B(target output)

### Experiment 1
Experiment 1 contains files related to separation of a nuclear (DAPI) and a membranal signal. 

- Train set size
- Parameters
- 3D
- Other files 

The Train set size folder contains the models trained on various train sets with a few example train sets (10.000, 15.000 and 20.000 images). Also the code to generate the test set for DAPI + mean membrane signal. 

The Parameter folder contains models trained with different parameters

The 3D folder contains a used 3D stack and scripts used for the 3D metrics.

Other files are the test set used for the parameters. 

### Experiment 2
Experiment 2 contains files and folders related to separation of a different nuclear signal and a membranal signal. 

- Dataset 4
- Dataset 5
- Models 

Dataset 4 is a set with the signal of PAX8+NCAM1 and Dataset 5 is a set with the signal of SIX2+NCAM1. The models contains the trained models for both datasets

### Experiment 3
Experiment 3 contains files and folders related to separation of 2 nuclear signals and a membranal signal. 

- Dataset 6
- Models
- Code to generate the set 

### General 
The 'General' folder contains files used for multiple experiments, such as the coordinate finder and the metrics calculations.

#### Get intensities
The original dataset contains multiple layers with differing intensities. To find the intensities necessary to normalize pixel values a loop over all layers and all pixels was needed. 

#### Get coordinates
Not all images were generated completely random, because in some cases certainty of signal was needed. This file calculates the mask of every layer of interest and generates a desired amount of coordinates of that layer with a minimum amount of signal. This file has a few parameters 

```sh
"--data", "-d", help = "path to h5py file"
"--names", "-n", nargs = '+', help = "names of wanted membranes and nuclei", type = str
"--layers", "-l", nargs = '+', help ="the range of layers of interest"
parser.add_argument("--image_size", "-is", default = 512, help="size of the image, square")
"--image_width", "-iw", default = 16128, help="the width of the image, default is 16128"
"--image_height", "-ih", default = 16896, help="the height of the image, default is 16896"
```

Some remarks: 'names' have to be capitals. 

Inside the file you can adjust the threshold of minimum pixel value (link) or the relative path within the h5 file (link). 

This file outputs txt files with 'random' coordinates above a certain threshold for the signals of interest. One txt file per layer.  

Other files to generate images depend on the output of this file. 

#### Create images
#### Split datasets
Sometimes images are directly outputted as combined AB images, but sometimes in separate sets of A and B. When this happens, they have to be combined and split into train, test and val. 

#### Random generation of images 
#### Generate dataset of the whole kidney 
#### Pix2pix folder 
Where all the deep learning magic happens. Not developed by me. 

### Others
Files that came in handy for tasks or are not part of the experiments (e.g. version of pix2pix to output numpy arrays). 

## Tech

Dillinger uses a number of open source projects to work properly:

- [AngularJS] - HTML enhanced for web apps!
- [Ace Editor] - awesome web-based text editor
- [markdown-it] - Markdown parser done right. Fast and easy to extend.
- [Twitter Bootstrap] - great UI boilerplate for modern web apps
- [node.js] - evented I/O for the backend
- [Express] - fast node.js network app framework [@tjholowaychuk]
- [Gulp] - the streaming build system
- [Breakdance](https://breakdance.github.io/breakdance/) - HTML
to Markdown converter
- [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

## Installation

Download the repository or only the code you're interested in. The environment.yml file contains the necessary packages. 

Install the dependencies using conda 

```sh
conda env create -f environment.yml
```

This creates an environment called 'virtsep'

## Remarks
Some datasets are way too large to download, such as images of the whole kidney or the dataset of 50.000 images. These can be found on the HPC.


## License

MIT


