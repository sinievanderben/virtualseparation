# File to generate the whole kidney in images of PAX8 and NCAM1

import numpy as np
import h5py
from skimage import io
import random

d = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc.ims", "r")

count = 0 
image_width=16128
image_height=16896

# Account for the overlap
step = 400
image_size = 512

extraLoopX = False
extraLoopY = False

quotentX, remainderX = divmod((image_width-image_size), step)
xGrids = quotentX 
if remainderX != 0:
    extraLoopX = True
    #xGrids = xGrids + 1

quotentY, remainderY = divmod((image_height-image_size), step)
print('quotentY', quotentY)
yGrids = quotentY 
if remainderY != 0:
    extraLoopY = True
    #yGrids = yGrids + 1

# Loop over all slices 
for i in range(112):

    x_start = 0
    x_end = 512
    # Loop over the x axis
    
    image_size_x = 512
    
    for x in range(0, xGrids):

        y_start = 0
        y_end = 512

        if (x == xGrids) and (extraLoopX == True):
            x_end = remainderX 
        
        image_size_y = 512

        for y in range(0, yGrids):

            pax8 = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 2/Data'][i, x_start:x_end, y_start:y_end]
            ncam1 = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 3/Data'][i, x_start:x_end, y_start:y_end]

            pax8 = (pax8.astype(np.float64) / 12000) * 255 #TODO: change value 
            pax8[pax8 > 255] = 255 # clipping 
                            
            # memb
            ncam1 = (ncam1.astype(np.float64) / 22000) * 255
            ncam1[ncam1 > 255] = 255 # clipping
            
            # Combined image    
            inputs = (pax8 + ncam1)  / 2 # TODO: need division by 2?              
                            
            # Normalize values from float to uint, because io.imsave jpg goes to uint8
                            
            ### Input
            inputs = inputs.astype(np.uint8)
            full_input = np.zeros((image_size_x, image_size_y, 3))
                         
            # Stack the input 3 times 
            full_input[:,:,0] = inputs
            full_input[:,:,1] = inputs
            full_input[:,:,2] = inputs
                                
            full_input = full_input.astype(np.uint8)
    
            io.imsave("/hpc/pmc_rios/Brain/2dunet/A_whole_paxncam/{0}_{1}_{2}_{3}_input_paxncam.png".format(x_start, x_end, i, y_start), full_input)

            ### Output 
                            
            # Convert float to int
            pax8 = pax8.astype(np.uint8)
            ncam1 = ncam1.astype(np.uint8)
                            
            # Empty array
            empt = np.zeros((image_size_x, image_size_y), dtype = 'uint8')
                    
            # Stack the slices and the empty array above each other
            output = np.stack((pax8, ncam1, empt), axis=2)
                    
            # Save image 
            io.imsave("/hpc/pmc_rios/Brain/2dunet/B_whole_paxncam/{0}_{1}_{2}_{3}_input_paxncam.png".format(x_start, x_end, i, y_start), output)

            y_start = y_start + step
            if (y == yGrids-1) and (extraLoopY == True):
                y_end = y_end + remainderY
                image_size_y = remainderY
            else:
                y_end = y_end + step


        x_start = x_start + step

        if (x == xGrids-1) and (extraLoopX == True):
            x_end = x_end + remainderX 
            image_size_x = remainderX
        else:
            x_end = x_end + step

f.close()




