import numpy as np 
import matplotlib.pyplot as plt
import h5py
import sys
import argparse
import os 
import time 
from skimage.filters import gaussian
from random import randint
from skimage import io

class IntensityFinder:

    def __init__(self, data, names, layers, image_size=512, image_width=16128, image_height=16896):
        
        # Data should be the file path of a H5 file in between " "
        # I assume here path_in_file is resolution level 0 / timepoint 0, also between  " " 

        file_5 = h5py.File(data, "r")
        self.file_5 = file_5
        self.data = data
        #self.path_in_file = path_in_file  # ResolutionLevel 0 / TimePoint 0 
        self.names = names  # A list of all names of the nuclei and membrane markers 
        self.image_size = image_size
        self.image_width = image_width
        self.image_height = image_height
        self.layers = layers

        
        # Set these to False for the nuclei markers 
        self.dapi_bool = False
        self.ki67_bool = False
        self.pax8_bool = False
        self.six2_bool = False
    
    def get_patches(self):
        
        # Get the patches of the image
        # Image patches of 512 by 512 by default 
        # Also works for images of 128, 256 etc

        quotent_x, remainder_x = divmod(self.image_width, self.image_size)

        if remainder_x == 0:
            self.x_grids = quotent_x - 1
        else:
            if remainder_x!= 0:
                self.x_grids = quotent_x - 1
            else:
                print('Insert an image width which can be divided by 128')
        
        quotent_y, remainder_y = divmod(self.image_height, self.image_size)

        if remainder_y == 0:
            self.y_grids = int(quotent_y) - 1
        else:
            if remainder_y != 0:
                self.y_grids = int(quotent_y) - 1
            else:
                print('Insert an image height which can be divided by 128')
        
        self.remainder_x = remainder_x
        self.remainder_y = remainder_y

    def mask_per_channel(self, segment, layer):
    
        start_time = time.time()

        # Segment is a whole 16000 x 16000 image of the channel
        
        print('99 non mask ', np.percentile(segment[layer,:,:],99))
        print('mean mask', np.mean(segment[layer,:,:]))

        self.mask = gaussian(segment[layer,:,:], sigma=50, preserve_range = True)
        
        print('99 percentile mask ', np.percentile(self.mask, 99))
        print('mean mask ', np.mean(self.mask))
        
        mask = np.where(self.mask > 3000, True, False)

        print("--- %s seconds ---" % (time.time() - start_time))
        return mask

    def percentages(self, mask):

        # Get percentages that fall within the mask 
        totals = np.sum(mask)
        percentage = (totals/(self.image_size * self.image_size)) * 100

        return percentage

    def percentage_check(self, mask, patch_values):

        # Calculate the percentage of the patch that falls under the white mask 
        temp_mask = mask[patch_values[1]:patch_values[2], patch_values[3]:patch_values[4]]

        percentage = self.percentages(temp_mask)
        print(percentage)

        return percentage

    def get_mask(self, i, j):
        start_x = i * 512
        end_x = (i*512) + 512
        start_y = j * 512
        end_y = (j *512) + 512
        
        new_mask = self.mask[start_x:end_x, start_y:end_y]
        
        return new_mask 
    

    def create_array(self):

        # Create an array of the given grids

        if self.remainder_x != 0 and self.remainder_y != 0:
            patch_array=np.zeros((self.x_grids+1, self.y_grids+1))
        elif self.remainder_x == 0 and self.remainder_y != 0:
            patch_array=np.zeros((self.x_grids, self.y_grids+1))
        elif self.remainder_x != 0 and self.remainder_y == 0:
            patch_array=np.zeros((self.x_grids+1, self.y_grids))
        else:
            patch_array=np.zeros((self.x_grids, self.y_grids))
        
        return patch_array
    
    def create_names_array(self):

        # Create an array for every marker 
        # And set booleans to true 
        
        print(self.names) 

        for i in self.names:

            if i == 'DAPI':
                self.dapi_array=self.create_array()
                self.dapi_bool = True
            if i == 'PAX8':
                self.pax8_array = self.create_array()
                self.pax8_bool = True
            if i == 'SIX2':
                self.six2_array = self.create_array()
                self.six2_bool = True 
            if i == 'NCAM1':
                self.ncam1_array = self.create_array()
            else:
                return print('wrong nuclei marker')
                


    def patch_loop(self):
        
        self.get_patches()

        # Create an array for every nuclei and membrane marker 
        self.create_names_array()

        extra_loop_x = False
        extra_loop_y = False
            
        # Extra loop if there are remainders

        if self.remainder_x != 0:
            extra_loop_x = True
            
        if self.remainder_y != 0:
            extra_loop_y = True
        
        # Create arrays for every name
        for n in self.names:

            if n == 'DAPI':
                array = self.dapi_array
                segment = self.file_5['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data']
                #mask = self.mask_per_channel(segment)
            if n == 'PAX8':
                array = self.pax8_array
                segment = self.file_5['DataSet/ResolutionLevel 0/TimePoint 0/Channel 2/Data']
                #mask = self.mask_per_channel(segment)
            if n == 'SIX2':
                array = self.six2_array
                segment = self.file_5['DataSet/ResolutionLevel 0/TimePoint 0/Channel 4/Data']
                #mask = self.mask_per_channel(segment)
            if n == 'NCAM1':
                array = self.ncam1_array
                segment = self.file_5['DataSet/ResolutionLevel 0/TimePoint 0/Channel 3/Data']
                #mask = self.mask_per_channel(segment)
        
            for layer in range(self.layers[0], self.layers[1]):
                print('Layer {0} of {1}'.format(layer, self.layers))
                
                layer = int(layer)
                # Get the number of possible patches 
                
                start_x=0
                end_x=512
                
                mask = self.mask_per_channel(segment, layer)
                
                # Loop over x
                for i in range(self.x_grids):
                    print('Loop {0} of {1}'.format(i, self.x_grids))
                
                    start_y=0
                    end_y=512
                    
                    # Loop over y 
                    for j in range(self.y_grids):
        
                        new_list= [layer, start_x, end_x, start_y, end_y]
    
                        # Percentage check 
                        percentage=self.percentage_check(mask, new_list) 
                        
                        # Save the percentage in the array
                        array[i, j] = percentage 
        
                        # Change pixel coordinates for the next round 
                        start_y = end_y
        
                        if extra_loop_y and (j == self.y_grids-1):
                            end_y=end_y + round(self.remainder_y)
                        else:
                            end_y=end_y + 512
                        
                    # Change pixel coordinates for the next round
                    start_x=end_x
        
                    if extra_loop_x and (i == self.x_grids-1):
                        end_x=end_x + round(self.remainder_x)
                    else:
                        end_x=end_x + 512
                  
                self.find_max_patches(array, n, layer)
            
        
    def find_max_patches(self, slice_array, name, layer, num=100):
        # To find indices of patches with enough percentage of mask

        # Default is return the top 100 patches with high values.
        # Slice array is the array of interest:

        root_dir = os.path.dirname(os.path.abspath(self.data))
        
        # Create a txt file to save all indices that can be read later 
        f = open(root_dir + '/' + str(name) + 'mask' + str(layer) + '.txt', "w+")
        
        # Account for nan values 
        slice_array = np.nan_to_num(slice_array)
        i = 0 
        
        print('start finding values')
	
        while (i != num):
        
            x = randint(0, self.x_grids-1)
            y = randint(0, self.y_grids-1)
            
            # Check if the percentage that falls under the mask is higher than 40%
            patch_check = slice_array[x, y]
            if patch_check > 30:
            
              print(patch_check)
              
              f.write(str(x) + ", " + str(y) + '\n')
              slice_array[x,y] = 0
              
              # Save the filtered image
              mask = self.get_mask(x,y)
              io.imsave("2dunet/B_test/{0}_{1}_{2}_{3}_mask_50.png".format(str(x*512), str((x*512)+512), layer, str(y*512)), mask)
              
              i = i + 1
              
            else:
              i = i 

        f.close()


parser = argparse.ArgumentParser()
parser.add_argument("--data", "-d", help = "path to h5py file")
parser.add_argument("--names", "-n", nargs = '+', help = "names of wanted membranes and nuclei", type = str)
parser.add_argument("--layers", "-l", nargs = '+', help ="the range of layers of interest")
parser.add_argument("--image_size", "-is", default = 512, help="size of the image, square")
parser.add_argument("--image_width", "-iw", default = 16128, help="the width of the image, default is 16128")
parser.add_argument("--image_height", "-ih", default = 16896, help="the height of the image, default is 16896")



# add image size? 112 x 16896 x 16128
#TODO: make it work for multiple layers, average the arrays?
# Loop per layer, add nuclei intensities and divide in find max to get an average

args = parser.parse_args()

if __name__ == "__main__":
    start_time = time.time()
    intensity_finder = IntensityFinder(args.data, args.names, args.layers, args.image_size, args.image_width, args.image_height)
    intensity_finder.patch_loop()
    print("--- %s seconds ---" % (time.time() - start_time))
