from re import X
import os
import glob
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Insert filepath of the test images here
filepath = r'E:\Stage\test_latest_stack3d\images'

filenames = os.listdir(filepath)

# Absolute error of the two arrays
def _error(actual: np.ndarray, predicted: np.ndarray):

    return np.sum(abs(actual - predicted))

# Absolute error in percentages 
def _percentage_error_all_division(actual: np.ndarray, predicted: np.ndarray):
    
    return (_error(actual,predicted) / (512*512*255)) * 100

count = 0 

for img in filenames:

    if 'fake' in img:
        # Print layer number 
        print(count)

        imageA = cv2.imread('{0}/{1}'.format(filepath, img))

        dapi = imageA[:, :, 2]  # third channel, cv2 reads as BGR
        memb = imageA[:, :, 1]  # second channel 

        dapi = dapi[:, :, np.newaxis]
        memb = memb[:, :, np.newaxis]

        z = img.replace('_fake_B', '_real_B')

        # Extract the layer number 
        count = z.replace('13312_13824_', '')
        count = count.replace('_3584_input_nuclmemb_real_B.png', '')
        count = int(count)

        imageB = cv2.imread('{0}/{1}'.format(filepath, z))

        true_dapi = imageB[:, :, 2]  
        true_memb = imageB[:, :, 1]

        true_dapi = true_dapi[:, :, np.newaxis]
        true_memb = true_memb[:, :, np.newaxis]

        dapi = dapi.astype(np.float64)
        true_dapi = true_dapi.astype(np.float64)
        memb = memb.astype(np.float64)
        true_memb = true_memb.astype(np.float64)

        if count == 0:
            dapi_array = dapi
            true_dapi_array = true_dapi
            memb_array = memb
            true_memb_array = true_memb
        

        if count > 19 and count < 103 :
            dapi_array = np.concatenate((dapi_array, dapi), axis = 2)
            true_dapi_array = np.concatenate((true_dapi_array, true_dapi), axis = 2)
            memb_array = np.concatenate((memb_array, memb), axis =2 )
            true_memb_array = np.concatenate((true_memb_array, true_memb), axis =2 )


        count = count + 1
        
# Print final shapes for a check 
print(dapi_array.shape)
print(true_dapi_array.shape)
print(memb_array.shape)
print(true_memb_array.shape)

dapi_ssim = ssim(dapi_array, true_dapi_array, gaussian_weights=True, sigma=1.5, use_sample_covariance=False, win_size=11, data_range = 255)
memb_ssim = ssim(memb_array, true_memb_array, gaussian_weights=True, sigma=1.5, use_sample_covariance=False, win_size=11, data_range = 255)

print('dapi 3d ssim: ', dapi_ssim)
print('memb 3d ssim: ', memb_ssim)



