import numpy as np
import h5py
from skimage import io
import random

# The files of the markers 
d = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc_nucl-dapi_shifted.ims", "r")
m = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc_memb-mean.ims", "r")

count = 0 

image_width=16128
image_height=16896

image_size = 512

extraLoopX = False
extraLoopY = False

quotentX, remainderX = divmod(image_width, image_size)
xGrids = quotentX 
XGrids = xGrids -1 
if remainderX != 0:
    xGrids = xGrids -1

quotentY, remainderY = divmod(image_height, image_size)
yGrids = quotentY 
yGrids = yGrids -1
if remainderY != 0:
    yGrids = yGrids -1

# Set the size of the test set 
while count != 500:
    count = count + 1

    # Generate coordinates at random 
    x_start_cor = random.randint(1,xGrids-1)
    x_end = x_start_cor * 512
    x_start = x_end - 512

    y_start_cor = random.randint(1, yGrids-1)
    y_end = y_start_cor * 512
    y_start = y_end - 512
    
    # i is a random number of a layer 
    i = random.randint(20,50)

    nuclei = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]
    memb = m['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]

    nuclei = (nuclei.astype(np.float64) / 30000) * 255 #TODO: change value 
    nuclei[nuclei > 255] = 255 # clipping 
                            
    memb = (memb.astype(np.float64) / 8000) * 255
    memb[memb > 255] = 255 # clipping
   
    inputs = (nuclei + memb)  / 2 # TODO: need division by 2?              
                                         
    ### Input
    inputs = inputs.astype(np.uint8)
    full_input = np.zeros((image_size, image_size, 3))
            
    n = 10
            
    if count%10 == 0: 
        n = random.randint(0,1)
        if n == 0:
                    
            # Stack the input 3 times 
            full_input[:,:,0] = memb.astype(np.uint8)
            full_input[:,:,1] = memb.astype(np.uint8)
            full_input[:,:,2] = memb.astype(np.uint8)
                                
            full_input = full_input.astype(np.uint8)
    
        
        else:
            # Stack the input 3 times 
            full_input[:,:,0] = nuclei.astype(np.uint8)
            full_input[:,:,1] = nuclei.astype(np.uint8)
            full_input[:,:,2] = nuclei.astype(np.uint8)
                                
            full_input = full_input.astype(np.uint8)
    
                
    else:                 
        # Stack the input 3 times 
        full_input[:,:,0] = inputs
        full_input[:,:,1] = inputs
        full_input[:,:,2] = inputs
                                
        full_input = full_input.astype(np.uint8)
    


    ### Output 
                            
    # Convert float to int
    nuclei = nuclei.astype(np.uint8)
    memb = memb.astype(np.uint8)
                            
    # Empty array
    empt = np.zeros((image_size, image_size), dtype = 'uint8')
            
    if n == 0:

        # Stack the slices and the empty array above each other
        output = np.stack((empt, memb, empt), axis=2)
                     
        new = np.concatenate([full_input, output],1)
        io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_test_dmm/test/{0}_{1}_{2}_{3}_input_memb.png'.format(x_start, x_end, i, y_start), new)

    if n == 1:
        # Stack the slices and the empty array above each other
        output = np.stack((nuclei, empt, empt), axis=2)
                                
        new = np.concatenate([full_input, output],1)
        io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_test_dmm/test/{0}_{1}_{2}_{3}_input_nucl.png'.format(x_start, x_end, i, y_start), new)

    else:             
        # Stack the slices and the empty array above each other
        output = np.stack((nuclei, memb, empt), axis=2)
                    
        new = np.concatenate([full_input, output],1)
        io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_test_dmm/test/{0}_{1}_{2}_{3}_input_nuclmemb.png'.format(x_start, x_end, i, y_start), new)