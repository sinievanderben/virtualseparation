# Use metrics for the images
# Mean error: subtract image A from image B and see the absolute difference
# Structural Similarity Index Measure
# Pearson Correlation coefficient 

import os 
import csv 
from skimage import io
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_absolute_error
from scipy.stats import pearsonr
import image_similarity_measures.quality_metrics as qm
import cv2
import numpy as np

np.set_printoptions(threshold=np.inf)

# Absolute error of the two arrays
def _error(actual: np.ndarray, predicted: np.ndarray):

    return np.sum(abs(actual - predicted))

# Absolute error in percentages 
def _percentage_error_all_division(actual: np.ndarray, predicted: np.ndarray):
    
    return (_error(actual,predicted) / (512*512*255)) * 100


#filepaths = ['dapi_meanmemb_unet_lr_pix2pix', 'dapi_meanmemb_unet_pix2pix', 'dapi_meanmemb_unet_long_pix2pix', 'dapi_meanmemb_resnet_pix2pix', 'dapi_meanmemb_resnet_lsg_pix2pix', 'dapi_meanmemb_resnet_lr_pix2pix', 'dapi_meanmemb_resnet_lambda150_pix2pix', 'dapi_meanmemb_lambda_80_pix2pix', 'dapi_meanmemb_lambda_50_pix2pix', 'dapi_meanmemb_lambda_30_pix2pix', 'dapi_meanmemb_lambda_150_pix2pix', 'dapi_meanmemb_lambda_180_pix2pix', 'dapi_meanmemb_lambda_120_pix2pix']

# Filepaths of test images we want metrics on 
filepaths = ["dmm_reslg_30_pix2pix_last"]

# The test file inside the test images. Usually they are called 'test latest'
interest = 'test_latest_newB'

for filepath in filepaths:

    # Change this with the path where the test images are
    filenames = os.listdir('/hpc/pmc_rios/Brain/2dunet/checkpoints/{0}/{1}/images'.format(filepath, interest))
    
    
    with open("/hpc/pmc_rios/Brain/2dunet/csv_metrics_{}_{}.csv".format(interest, filepath), mode = 'w') as metrics_file: 
    
            metrics_writer = csv.writer(metrics_file, delimiter = ',') 
            
            # Keep a count 
            count = 0 
            
            if count == 0:
                #metrics_writer.writerow(['ssim nuclei', 'ssim nuclei2', 'ssim memb', 'abs nuclei', 'abs nuclei2', 'abs memb', 'pear nuclei', 'pear nuclei2', 'pear memb'])
                metrics_writer.writerow(['ssim nuclei', 'ssim memb', 'abs nuclei' , 'abs memb', 'pear nuclei', 'pear memb'])
            
            # Set everything to zero 
            # 'other channel' is for the combination of 3 channels (such as PAX8, SIX2 and mean membrane)
            mean_ssim_nuclei = 0
            mean_ssim_memb = 0
            mean_ssim_other_channel = 0
            mean_error_nuclei = 0
            mean_error_memb = 0
            mean_error_other_channel = 0 
            mean_pearsonr_nuclei = 0
            mean_pearsonr_memb = 0
            mean_percentage_error_nuclei_alldivision = 0
            mean_percentage_error_memb_alldivision = 0 
            mean_percentage_error_other_channel_alldivision = 0
            
            # Loop over images 
            for img in filenames:
            
                if 'fake' in img:
                    
                    if count % 10 == 0:
                        print(count)
            
                    count = count + 1
                    
                    if count == 101:
                        break 

                    
                    # Read in fake
                    imageA = cv2.imread('/hpc/pmc_rios/Brain/2dunet/checkpoints/{0}/{1}/images/{2}'.format(filepath, interest, img))
            
                    dapi = imageA[:, :, 2]  #  red channel 
                    memb = imageA[:, :, 1]
                    other_channel= imageA[:,:,0]
                    
                    io.imsave('/hpc/pmc_rios/Brain/2dunet/error_images/{}_nuclear.png'.format(img), dapi)
                    io.imsave('/hpc/pmc_rios/Brain/2dunet/error_images/{}_membranal.png'.format(img), memb)
            
                    z = img.replace('_fake_B', '_real_B')
                    
                    # Read in real 
                    imageB = cv2.imread('/hpc/pmc_rios/Brain/2dunet/checkpoints/{0}/{1}/images/{2}'.format(filepath, interest, z))
            
                    true_dapi = imageB[:, :, 2]  #  red channel 
                    true_memb = imageB[:, :, 1]
                    true_other_channel=imageB[:,:,0]
                    
                    io.imsave('/hpc/pmc_rios/Brain/2dunet/error_images/{}_nuclear.png'.format(z), true_dapi)
                    io.imsave('/hpc/pmc_rios/Brain/2dunet/error_images/{}_membranal.png'.format(z), true_memb)
            
                    end = z.replace('_real_B', '')
                    
                    # Convert to float 
                    dapi = dapi.astype(np.float64)
                    true_dapi = true_dapi.astype(np.float64)
                    memb = memb.astype(np.float64)
                    true_memb = true_memb.astype(np.float64)
                    other_channel = other_channel.astype(np.float64)
                    true_other_channel = true_other_channel.astype(np.float64)
                    
                    
                    pics = end.replace('.png', '')
            
            

                    ### Part for csv file
                    
                    # SSIM
                    ssim_nuclei = ssim(dapi, true_dapi, gaussian_weights=True, sigma=1.5, use_sample_covariance=False, win_size=11, data_range = 255)
                    ssim_memb = ssim(memb, true_memb, gaussian_weights=True, sigma=1.5, use_sample_covariance=False, win_size=11, data_range = 255)
                    ssim_other = ssim(other_channel, true_other_channel, gaussian_weights=True, sigma=1.5, use_sample_covariance=False, win_size=11, data_range = 255)
                    
                    # Absolute error
                    abs_nuclei = _percentage_error_all_division(true_dapi, dapi)
                    abs_memb = _percentage_error_all_division(true_memb, memb)
                    abs_other = _percentage_error_all_division(true_other_channel, other_channel)
                    
                    # Flatten for pearson
                    dapi = dapi.flatten()
                    true_dapi = true_dapi.flatten()
                    memb = memb.flatten()
                    true_memb = true_memb.flatten()
                    other_channel = other_channel.flatten()
                    true_other_channel = true_other_channel.flatten()  
                    
                    d_r, d_p = pearsonr(dapi, true_dapi) 
                    m_r, m_p = pearsonr(memb, true_memb)
                    o_r, o_p = pearsonr(other_channel, true_other_channel)
                    
                    
                    # Pearson correlation 
                    pear_nuclei = d_r
                    pear_memb = m_r
                    pear_other = o_r
                    
                    # Save all the values in a csv file 
                    #metrics_writer.writerow([ssim_nuclei, ssim_memb, ssim_other, abs_nuclei, abs_memb, abs_other, pear_nuclei, pear_memb, pear_other])
                    metrics_writer.writerow([ssim_nuclei, ssim_memb, abs_nuclei, abs_memb, pear_nuclei, pear_memb]) 
                    
                else:
                    pass
                    
    metrics_file.close()



