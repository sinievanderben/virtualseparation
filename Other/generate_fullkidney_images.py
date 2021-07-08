# Generate images of the entire kidney to predict the whole kidney 
import numpy as np
import h5py
from skimage import io

d = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc_nucl-dapi_shifted.ims", "r")
m = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc_memb-mean.ims", "r")

count = 0 

image_width=16128
image_height=16896

step = 400
image_size = 512

extraLoopX = False
extraLoopY = False

quotentX, remainderX = divmod((image_width-image_size), step)
xGrids = quotentX 
if remainderX != 0:
    extraLoopX = True


quotentY, remainderY = divmod((image_height-image_size), step)
yGrids = quotentY 
if remainderY != 0:
    extraLoopY = True


# Loop over all slices 
for i in range(112):

    #images of 512 x 512
    #images of 400 x 400

    x_start = 0
    x_end = 512
    # Loop over the x axis
    
    image_size_x = 512

    for x in range(0, xGrids):

        y_start = 0
        y_end = 512

        image_size_y = 512

        if (x == xGrids) and (extraLoopX == True):
            x_end = remainderX 

        for y in range(0, yGrids):

            nuclei = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]
            membrane = m['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]

            nuclei = (nuclei.astype(np.float64) / 30000) * 255 #TODO: change value 
            nuclei[nuclei > 255] = 255 # clipping 
                            
            # memb
            membrane = (membrane.astype(np.float64) / 8000) * 255
            membrane[membrane > 255] = 255 # clipping
            
            # Combined image    
            inputs = (nuclei + membrane)  / 2 # TODO: need division by 2?              
                            
            # Normalize values from float to uint, because io.imsave jpg goes to uint8
                            
            ### Input
            inputs = inputs.astype(np.uint8)
            full_input = np.zeros((image_size_x, image_size_y, 3))
                            
            # Stack the input 3 times 
            full_input[:,:,0] = inputs
            full_input[:,:,1] = inputs
            full_input[:,:,2] = inputs
                            
            full_input = full_input.astype(np.uint8)

            ### Output 
                            
            # Convert float to int
            nuclei = nuclei.astype(np.uint8)
            membrane = membrane.astype(np.uint8)
                            
            # Empty array
            empt = np.zeros((image_size_x, image_size_y), dtype = 'uint8')
                            
            # Stack the slices and the empty array above each other
            output = np.stack((nuclei, membrane, empt), axis=2)

            new_slice = np.concatenate([full_input, output], 1)
                
            # Save image 
            io.imsave("/hpc/pmc_rios/Brain/2dunet/AB_dmm_fullkidney_test/test/{0}_{1}_{2}_{3}_input_dmm.png".format(x_start, x_end, i, y_start), new_slice)

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





