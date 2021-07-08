from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import cv2
import os

# Open a txt file to save the correlations 
f = open(r'C:\Users\sinie\Documents\Utrecht_Universiteit\Stage\correlations.txt', "a")

# Get the filepath of the images 
filepath = r'C:\Users\sinie\Documents\Utrecht_Universiteit\Stage\images_resnet_lsg' 
filenames = os.listdir(r'C:\Users\sinie\Documents\Utrecht_Universiteit\Stage\images_resnet_lsg')

count = 0

avg_cor_nuclei = []
avg_cor_memb = []

for img in filenames:

    if 'fake' in img:

        count = count + 1

        imageA = cv2.imread('{0}/{1}'.format(filepath, img))

        dapi = imageA[:, :, 1]  #  second channel 
        memb = imageA[:, :, 2]

        z = img.replace('_fake_B', '_real_B')
        print(z)

        imageB = cv2.imread('{0}/{1}'.format(filepath, z))

        true_dapi = imageB[:, :, 1]  #  second channel 
        true_memb = imageB[:, :, 2]
        
        dapi = dapi.astype(np.float64)
        dapi = dapi.flatten()
        true_dapi = true_dapi.astype(np.float64)
        true_dapi = true_dapi.flatten()
        memb = memb.astype(np.float64)
        memb = memb.flatten()
        true_memb = true_memb.astype(np.float64)
        true_memb = true_memb.flatten()

        print(z, file=f)
        print('nuclei:', scipy.stats.pearsonr(dapi, true_dapi), file = f)
        print('memb:', scipy.stats.pearsonr(memb, true_memb), file = f)

        print( scipy.stats.pearsonr(dapi, true_dapi))

    
    else:
        pass


f.close()
