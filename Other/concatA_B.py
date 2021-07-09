import random 
import shutil
import numpy as np
import os
from skimage import io

filenames = os.listdir('A_test_dmm')

for i in filenames:
    original = io.imread('/hpc/pmc_rios/Brain/2dunet/A_test_dmm/{0}'.format(i))
    print(original.shape)

    og_B = io.imread('/hpc/pmc_rios/Brain/2dunet/B_test_dmm/{0}'.format(i))
    print(og_B.shape)
    
    new = np.concatenate([original, og_B],1)
    io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_test_dmm/test/{0}'.format(i), new)
