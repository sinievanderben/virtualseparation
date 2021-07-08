import numpy as np 
import os 
import cv2
import glob
import re

filepaths = ['dmm_reslg_10_pix2pix_last', 'dmm_reslg_5_pix2pix_last', 'dmm_reslg_20_pix2pix_last', 'dmm_reslg_30_pix2pix_last', 'dmm_reslg_15_pix2pix', 'dmm_reslg_8_pix2pix', 'dmm_reslg_50_pix2pix']

f2 = open("/hpc/pmc_rios/Brain/2dunet/all_traintimes.txt", "a")

for files in filepaths:

    # Change this with the path where the test images are
    filepath = '/hpc/pmc_rios/Brain/2dunet/checkpoints/{0}/loss_log.txt'.format(files)
    
    train_time = 0

    with open(filepath, 'r') as f:
        next(f)
        for line in f:
            count = 0 
            for word in line.split():
                count = count + 1
                if count == 6:
                    traintime = float(word[:-1])
                    train_time = train_time + traintime
    
    print(files, file = f2)
    print('hours', train_time/60, file = f2)
                

