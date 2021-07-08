# Virtual Separation 
## Project to separate immunofluorescent markers 


This repository contains the code for the project 'Virtual separation of cellular markers wuth overlapping fluorescent spectra'

It contains:
- A few example datasets
- Codes to generate images
- ✨Deep learning using [pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)✨

The deep learning part is done through a different repository on Github. You can download the necessary files from there. 

## Structure

- Experiment 1
- Experiment 2
- Experiment 3
- General files 
- Others

Images or dataset are sometimes called AB. This means that it contains images that are a combination of A (conditional input) and B(target output). 

### Experiment 1
Experiment 1 contains files related to separation of a nuclear (DAPI) and a membranal signal. 

- Train set size
- Parameters
- 3D
- Other files 

The Train set size folder contains the models trained on various train sets. Also the code to generate the test set for DAPI + mean membrane signal. 

The Parameter folder contains models trained with different parameters, such as different lambda values, adapted learning rate and a ResNet generator. 

The 3D folder contains a used 3D stack and scripts used for the 3D metrics.

Other files are the test set used for the parameters. 

### Experiment 2
Experiment 2 contains files and folders related to separation of a different nuclear signal and a membranal signal. 

- File to make images from PAX8+NCAM1 and SIX2+NCAM1
- File to generate the whole kidney with PAX8 or SIX2 signal
- Models 

### [Experiment 3](https://github.com/sinievanderben/VirtualSeparation-/tree/main/Experiment3)
Experiment 3 contains files and folders related to separation of 2 nuclear signals and a membranal signal. 

- Models
- Code to generate the set 

### General 
The 'General' folder contains files used for multiple experiments, such as the coordinate finder and the metrics calculations.

#### [Get intensities](https://github.com/sinievanderben/VirtualSeparation-/blob/main/General/intensity_all_8_channels.py)
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

#### [Make images](https://github.com/sinievanderben/VirtualSeparation-/blob/main/General/make_images.py)
With the coordinate finder file you'll get txt files per layer with coordinates of images with signal. With this file you create the images reading the txt files. You do have to adjust [lines](https://github.com/sinievanderben/VirtualSeparation-/blob/main/General/make_images.py#L46) when using different signals, as the default is DAPI and the mean membrane signal

#### [Split datasets](https://github.com/sinievanderben/VirtualSeparation-/blob/main/General/split_datasets_general.py)
Sometimes images are directly outputted as combined AB images, but sometimes in separate sets of A and B. When this happens, they have to be combined and split into train, test and val. 

#### [Random](https://github.com/sinievanderben/VirtualSeparation-/blob/main/General/random_image_generation.py) generation of images 
The first file 'make images' is to generate images from the txt files. This file is to generate random images from all over the kidney. 

#### [Metrics](https://github.com/sinievanderben/VirtualSeparation-/blob/main/General/metrics.py)
This is the file where the SSIM, the absolute error percentage and the Pearson correlation are calculated. There is also a separate [file](https://github.com/sinievanderben/VirtualSeparation-/blob/main/General/correlation_metric.py) for the Pearson correlation only

### Others
Files that came in handy for tasks or are not part of the experiments (e.g. version of pix2pix to output numpy arrays). 

- File to concatenate separate A and B images to an AB image
- File to generate the whole kidney in images of 512 x 512
- File to count how many images there are in a folder 

## Installation

Download the repository or only the code you're interested in. The environment.yml file contains the necessary packages. 

Install the dependencies using conda 

```sh
conda env create -f environment.yml
```

This creates an environment called 'virtsep'

As said before, you also need to download the Github repository of the [pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).

## Remarks
The datasets are not included in this repository. They are very large and Github was not happy to upload them. 


## License

MIT


