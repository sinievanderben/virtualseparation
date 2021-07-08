import numpy as np
import h5py
from skimage import io
import random

d = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc_nucl-nuclei_shifted.ims", "r")
m = h5py.File("/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc_memb-mean.ims", "r")

trainsize = 1000
testsize = 100
valsize = 100

image_width=16128
image_height=16896

image_size = 512

empt = np.zeros((image_size, image_size), dtype = 'uint8')

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

coord_list = []

#Choose number of interest 
while count != trainsize: 

    x_start_cor = random.randint(1,xGrids-1)
    x_end = x_start_cor * 512
    x_start = x_end - 512

    y_start_cor = random.randint(1, yGrids-1)
    y_end = y_start_cor * 512
    y_start = y_end - 512

    i = random.randint(1,110)

    if (x_start_cor, y_start_cor, i) is not in coord_list: 
        # Input baselayer
        nuclei = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]
        memb = m['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]

        nuclei = (nuclei.astype(np.float64) / 30000) * 255 #TODO: change value 
        nuclei[nuclei > 255] = 255 # clipping 

        memb = (memb.astype(np.float64) / 8000) * 255
        memb[memb > 255] = 255 # clipping
    
        inputs = (nuclei + memb)  / 2 # TODO: need division by 2?              

        inputs = inputs.astype(np.uint8)

        # Combine the inputs 
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
                
            if n ==1:
                # Stack the input 3 times 
                full_input[:,:,0] = nuclei.astype(np.uint8)
                full_input[:,:,1] = nuclei.astype(np.uint8)
                full_input[:,:,2] = nuclei.astype(np.uint8)
                                    
                full_input = full_input.astype(np.uint8)
                        
        if count%10 != 0:                 
            # Stack the input 3 times 
            full_input[:,:,0] = inputs
            full_input[:,:,1] = inputs
            full_input[:,:,2] = inputs
                                    
            full_input = full_input.astype(np.uint8)

        ### Output 
                                
        # Convert float to int
        nuclei = nuclei.astype(np.uint8)
        memb = memb.astype(np.uint8)
           
                
        if n == 0:

            # Stack the slices and the empty array above each other
            output = np.stack((empt, memb, empt), axis=2)
                        
            # Save image 
            new = np.concatenate([full_input, output],1)
            io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_nuclei_meanmemb/train/{0}_{1}_{2}_{3}_input_memb.png'.format(x_start, x_end, i, y_start), new)

        if n == 1:
            # Stack the slices and the empty array above each other
            output = np.stack((nuclei, empt, empt), axis=2)
                        
            # Save image 
            new = np.concatenate([full_input, output],1)
            io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_nuclei_meanmemb/train/{0}_{1}_{2}_{3}_input_nuclei.png'.format(x_start, x_end, i, y_start), new)

        if count%10 != 0:             
            # Stack the slices and the empty array above each other
            output = np.stack((nuclei, memb, empt), axis=2)
                        
            # Save image 
            new = np.concatenate([full_input, output],1)
            io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_nuclei_meanmemb/train/{0}_{1}_{2}_{3}_input_nuclmemb.png'.format(x_start, x_end, i, y_start), new)
        
        
        coord_list.append((x_start_cor, y_start_cor, i)) 
        count = count + 1
    
    else:
        pass

test_count = 0 

while test_count != testsize:
    print(test_count)

    x_start_cor = random.randint(1,xGrids-1)
    x_end = x_start_cor * 512
    x_start = x_end - 512

    y_start_cor = random.randint(1, yGrids-1)
    y_end = y_start_cor * 512
    y_start = y_end - 512

    i = random.randint(1,110)

    if (x_start_cor, y_start_cor, i) is not in coord_list:
        # Input baselayer
        nuclei = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]
        memb = m['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]

        nuclei = (nuclei.astype(np.float64) / 30000) * 255 #TODO: change value 
        nuclei[nuclei > 255] = 255 # clipping 

        memb = (memb.astype(np.float64) / 8000) * 255
        memb[memb > 255] = 255 # clipping
    
        inputs = (nuclei + memb)  / 2 # TODO: need division by 2?              

        inputs = inputs.astype(np.uint8)

        # Combine the inputs 
        full_input = np.zeros((image_size, image_size, 3))
                
        n = 10
                
        if test_count%10 == 0: 
            n = random.randint(0,1)
            if n == 0:
                        
                # Stack the input 3 times 
                full_input[:,:,0] = memb.astype(np.uint8)
                full_input[:,:,1] = memb.astype(np.uint8)
                full_input[:,:,2] = memb.astype(np.uint8)
                                    
                full_input = full_input.astype(np.uint8)

                
            if n ==1:
                # Stack the input 3 times 
                full_input[:,:,0] = nuclei.astype(np.uint8)
                full_input[:,:,1] = nuclei.astype(np.uint8)
                full_input[:,:,2] = nuclei.astype(np.uint8)
                                    
                full_input = full_input.astype(np.uint8)
                        
        if test_count%10 != 0:                 
            # Stack the input 3 times 
            full_input[:,:,0] = inputs
            full_input[:,:,1] = inputs
            full_input[:,:,2] = inputs
                                    
            full_input = full_input.astype(np.uint8)

        ### Output 
                                
        # Convert float to int
        nuclei = nuclei.astype(np.uint8)
        memb = memb.astype(np.uint8)
                                
                
        if n == 0:

            # Stack the slices and the empty array above each other
            output = np.stack((empt, memb, empt), axis=2)
                        
            # Save image 
            new = np.concatenate([full_input, output],1)
            io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_nuclei_meanmemb/test/{0}_{1}_{2}_{3}_input_memb.png'.format(x_start, x_end, i, y_start), new)

        if n == 1:
            # Stack the slices and the empty array above each other
            output = np.stack((nuclei, empt, empt), axis=2)
                        
            # Save image 
            new = np.concatenate([full_input, output],1)
            io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_nuclei_meanmemb/test/{0}_{1}_{2}_{3}_input_nuclei.png'.format(x_start, x_end, i, y_start), new)

        else:             
            # Stack the slices and the empty array above each other
            output = np.stack((nuclei, memb, empt), axis=2)
                        
            # Save image 
            new = np.concatenate([full_input, output],1)
            io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_nuclei_meanmemb/test/{0}_{1}_{2}_{3}_input_nuclmemb.png'.format(x_start, x_end, i, y_start), new)
        
        
        coord_list.append((x_start_cor, y_start_cor, i)) 
        test_count = test_count + 1
    
    else:
        pass

val_count = 0

while val_count != valsize:

    x_start_cor = random.randint(1,xGrids-1)
    x_end = x_start_cor * 512
    x_start = x_end - 512

    y_start_cor = random.randint(1, yGrids-1)
    y_end = y_start_cor * 512
    y_start = y_end - 512

    i = random.randint(1,110)

    if (x_start_cor, y_start_cor, i) is not in coord_list:
        # Input baselayer
        nuclei = d['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]
        memb = m['DataSet/ResolutionLevel 0/TimePoint 0/Channel 0/Data'][i, x_start:x_end, y_start:y_end]

        nuclei = (nuclei.astype(np.float64) / 30000) * 255 #TODO: change value 
        nuclei[nuclei > 255] = 255 # clipping 
                                
        memb = (memb.astype(np.float64) / 8000) * 255
        memb[memb > 255] = 255 # clipping
    
        inputs = (nuclei + memb)  / 2 # TODO: need division by 2?              

        inputs = inputs.astype(np.uint8)

        # Combine the inputs 
        full_input = np.zeros((image_size, image_size, 3))
                
        n = 10
                
        if count%10 == 0: 
            n = random.randint(0,2)
            if n == 0:
                        
                # Stack the input 3 times 
                full_input[:,:,0] = memb.astype(np.uint8)
                full_input[:,:,1] = memb.astype(np.uint8)
                full_input[:,:,2] = memb.astype(np.uint8)
                                    
                full_input = full_input.astype(np.uint8)
                
            if n ==1:
                # Stack the input 3 times 
                full_input[:,:,0] = nuclei.astype(np.uint8)
                full_input[:,:,1] = nuclei.astype(np.uint8)
                full_input[:,:,2] = nuclei.astype(np.uint8)
                                    
                full_input = full_input.astype(np.uint8)
                        
        if count%10 != 0:                 
            # Stack the input 3 times 
            full_input[:,:,0] = inputs
            full_input[:,:,1] = inputs
            full_input[:,:,2] = inputs
                                    
            full_input = full_input.astype(np.uint8)

        ### Output 
                                
        # Convert float to int
        nuclei = nuclei.astype(np.uint8)
        memb = memb.astype(np.uint8)
                                
                
        if n == 0:

            # Stack the slices and the empty array above each other
            output = np.stack((empt, memb, empt), axis=2)
                        
            # Save image 
            new = np.concatenate([full_input, output],1)
            io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_nuclei_meanmemb/val/{0}_{1}_{2}_{3}_input_memb.png'.format(x_start, x_end, i, y_start), new)
        if n == 1:
            # Stack the slices and the empty array above each other
            output = np.stack((nuclei, empt, empt), axis=2)
                        
            # Save image 
            new = np.concatenate([full_input, output],1)
            io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_nuclei_meanmemb/val/{0}_{1}_{2}_{3}_input_nuclei.png'.format(x_start, x_end, i, y_start), new)

        else:             
            # Stack the slices and the empty array above each other
            output = np.stack((nuclei, memb, empt), axis=2)
                        
            # Save image 
            new = np.concatenate([full_input, output],1)
            io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_nuclei_meanmemb/val/{0}_{1}_{2}_{3}_input_nuclmemb.png'.format(x_start, x_end, i, y_start), new)
        
        
        coord_list.append((x_start_cor, y_start_cor, i)) 
        val_count = val_count + 1
    
    else:
        pass

