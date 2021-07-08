import os 
import numpy as np 
import h5py
from skimage import io
import glob 

# Read H5 file

# pax and six
d = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc.ims", "r")

# mean memb
m = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc_memb-mean.ims", "r")

# Get all txt files with signal from PAX8 and SIX2
fileslist = glob.glob('/hpc/pmc_rios/Brain/*.txt')

image_size = 512

# automatic way of detecting slice?


for fil in fileslist:
    f = open(fil, 'r+')

    slices = int(''.join(filter(lambda i: i.isdigit(), fil)))
    print(slices)

    for i in f.readlines():
        i = i.replace(',', " ")

        coords = [int(s) for s in i.split() if s.isdigit()]

        x_start = coords[0] * image_size
        x_end = x_start + image_size
        y_start = coords[1] * image_size
        y_end = y_start + image_size

        # generate images 

        pax_slice = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 2/Data'][slices, x_start:x_end, y_start:y_end] #pax
        six_slice = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 4/Data'][slices, x_start:x_end, y_start:y_end] #pax


        meanmemb_slice = m['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][slices, x_start:x_end, y_start:y_end] #meanmemb 
                        
        # Normalize separate channels
        if pax_slice.shape != (512,512): 
            pass
            
        else:           
            # pax
            pax_slice = (pax_slice.astype(np.float64) / 12000) * 255 #TODO: change value 
            pax_slice[pax_slice > 255] = 255 # clipping 
    
            # six
            six_slice = (six_slice.astype(np.float64) / 16000) * 255 #TODO: change value 
            six_slice[six_slice > 255] = 255 # clipping 
                            
            # memb
            meanmemb_slice = (meanmemb_slice.astype(np.float64) / 30000) * 255
            meanmemb_slice[meanmemb_slice > 255] = 255 # clipping
            
            # Combined image    
            inputs = (pax_slice + six_slice + meanmemb_slice)  / 3 # TODO: need division by 2?                        
                            
            # Normalize values from float to uint, because io.imsave jpg goes to uint8
                            
            ### Input
            inputs = inputs.astype(np.uint8)
            full_input = np.zeros((512, 512, 3))
                            
            # Stack the input 3 times 
            full_input[:,:,0] = inputs
            full_input[:,:,1] = inputs
            full_input[:,:,2] = inputs
                            
            full_input = full_input.astype(np.uint8)
                                      
            # Save image 
            io.imsave("/hpc/pmc_rios/Brain/2dunet/A_paxsixmeanmemb/{0}_{1}_{2}_{3}_input_paxsix_meanmemb.png".format(x_start, x_end, slices, y_start), full_input)
                            
            ### Output 
                            
            # Convert float to int
            pax_slice = pax_slice.astype(np.uint8)
            six_slice = six_slice.astype(np.uint8)
            meanmemb_slice = meanmemb_slice.astype(np.uint8)
                            
                            
            # Stack the slices and the empty array above each other
            output = np.stack((pax_slice, six_slice, meanmemb_slice), axis=2)
            
                      
            # Save image 
            io.imsave("/hpc/pmc_rios/Brain/2dunet/B_paxsixmeanmemb/{0}_{1}_{2}_{3}_input_paxsix_meanmemb.png".format(x_start, x_end, slices, y_start), output)
        
# This code can be extended to directly insert combined images (AB) into train, test and val sets. 



