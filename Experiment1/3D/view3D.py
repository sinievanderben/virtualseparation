from skimage import io
import matplotlib as plt
import napari
import numpy as np 
import os 
import cv2
import glob
import re


# Get location of the test images 
filepath = r'E:\Stage\test_latest_stack3d\images'

filenames = os.listdir(filepath)
print(filenames)

x = 0 

for img in sorted(glob.glob(r'E:\Stage\test_latest_stack3d\images\13312_13824_*_3584_input_nuclmemb_fake_B.png'), key=numericalSort):
    print("Current File Being Processed is: ", img)

    if 'fake' in img:
        

        x = x + 1   

        imageA = cv2.imread('{0}'.format(img))

        # Transform the images for the stacking 
        dapi = imageA[:, :, 2]  
        dapi = dapi[np.newaxis, :, :]
        memb = imageA[:, :, 1]
        memb = memb[np.newaxis,:, :]

        z = img.replace('_fake_B', '_real_B')

        imageB = cv2.imread('{0}'.format(z))

        true_dapi = imageB[:, :, 2] 
        true_dapi = true_dapi[np.newaxis, :, :] 
        true_memb = imageB[:, :, 1]
        true_memb = true_memb[np.newaxis,:, :]

        if x == 1:
            dapi_array = dapi
            memb_array = memb
            true_dapi_array = true_dapi
            true_memb_array = true_memb

            output_t_m = np.stack((true_memb_array, true_memb_array, true_memb_array), axis=3)
            output_f_m = np.stack((memb_array, memb_array, memb_array), axis=3)

            
        else:
            dapi_array = np.concatenate((dapi_array, dapi), axis = 0)
            memb_array = np.concatenate((memb_array, memb), axis = 0)
            true_dapi_array = np.concatenate((true_dapi_array, true_dapi), axis =0)
            true_memb_array = np.concatenate((true_memb_array, true_memb), axis = 0)


print(dapi_array.shape)
print(memb_array.shape)
print(true_dapi_array.shape)
print(true_memb_array.shape)

name = 'DMM'

# Open napari viewer
with napari.gui_qt():
    viewer = napari.Viewer()
    viewer.title = name
    viewer.dims.order = (1, 3, 2, 0)

    viewer.add_image(dapi_array, name='dapi fake B')
    viewer.add_image(true_dapi_array, name = 'dapi real B')
    viewer.add_image(memb_array, name='memb fake B')
    viewer.add_image(true_memb_array, name = 'memb real B')

    clim = [5000, 40000]
    for lay in viewer.layers:
        lay.scale = [3.6,1, 1] # or 11 3 --> look at resolution lay.scale to resolution of the image  [0.33, 0.33, 1.21]
        lay.contrast_limits #= clim
    
