import numpy as np 
import os 
import h5py
from skimage import io

d = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc_nucl-dapi_shifted.ims", "r")
m = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc_memb-mean.ims", "r")

#13312_13824_27_3584

start_x = 13312
end_x = 13824
start_y = 3584
end_y = start_y + 512


for i in range(112):
    dapi_slice = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, start_x:end_x, start_y:end_y]
    memb_slice = m['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, start_x:end_x, start_y:end_y]

    dapi_slice = (dapi_slice.astype(np.float64) / 25000) * 255 #TODO: change value  pax8
    dapi_slice[dapi_slice > 255] = 255 # clipping 
                            
    memb_slice = (memb_slice.astype(np.float64) / 7000) * 255 #ncam1
    memb_slice[memb_slice > 255] = 255 # clipping
            
    # Combined image    
    inputs = (dapi_slice + memb_slice)  / 2 # TODO: need division by 2?
                            
                            
    # Normalize values from float to uint, because io.imsave jpg goes to uint8
                            
    ### Input
    inputs = inputs.astype(np.uint8)
    full_input = np.zeros((512, 512, 3))
                            
    # Stack the input 3 times 
    full_input[:,:,0] = inputs
    full_input[:,:,1] = inputs
    full_input[:,:,2] = inputs
                            
    full_input = full_input.astype(np.uint8)

    ### Output 
                            
    # Convert float to int
    dapi_slice = dapi_slice.astype(np.uint8)
    memb_slice = memb_slice.astype(np.uint8)
                            
    # Empty array
    empt = np.zeros((512, 512), dtype = 'uint8')
                            
    # Stack the slices and the empty array above each other
    output = np.stack((dapi_slice, memb_slice, empt), axis=2)

    ### Combine A and B
    new_slice = np.concatenate([full_input, output], 1)

    io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_3D_stack_2/test/{0}_{1}_{2}_{3}_input_nuclmemb.png'.format(start_x, end_x, i, start_y), new_slice)
