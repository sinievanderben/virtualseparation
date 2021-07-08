# This dataset uses A (conditional input) and B (desired output) imagefolders

import random 
import shutil
import numpy as np
import os
from skimage import io

# Change filenames to interest
filenames = os.listdir('A_paxsixdapi')

filenames.sort()  # make sure that the filenames have a fixed order before shuffling
random.seed(210)
random.shuffle(filenames) # shuffles the ordering of filenames (deterministic given the chosen seed)

stop = len(filenames)

split_1 = int(0.8 * stop)
split_2 = int(0.9 * stop)
train_filenames = filenames[:split_1]
print('train', len(train_filenames))
dev_filenames = filenames[split_1:split_2]
print('val', len(dev_filenames))
test_filenames = filenames[split_2:stop]
print('test', len(test_filenames))

print('train')
for i in train_filenames:
    print(i)
    original = io.imread('/hpc/pmc_rios/Brain/2dunet/A_paxsixdapi/{0}'.format(i))

    og_B = io.imread('/hpc/pmc_rios/Brain/2dunet/B_paxsixdapi/{0}'.format(i))

    new = np.concatenate([original, og_B],1)
    io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_paxsixdapi/train/{0}'.format(i), new)

print('test')
for j in test_filenames:
    og_test= io.imread('/hpc/pmc_rios/Brain/2dunet/A_paxsixdapi/{0}'.format(j))

    og_test_B = io.imread('/hpc/pmc_rios/Brain/2dunet/B_paxsixdapi/{0}'.format(j))

    new = np.concatenate([og_test, og_test_B],1)
    io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_paxsixdapi/test/{0}'.format(j), new)
    
print('val')
for g in dev_filenames:
    og_dev= io.imread('/hpc/pmc_rios/Brain/2dunet/A_paxsixdapi/{0}'.format(g))

    og_dev_B = io.imread('/hpc/pmc_rios/Brain/2dunet/B_paxsixdapi/{0}'.format(g))
    
    new = np.concatenate([og_dev, og_dev_B],1)
    io.imsave('/hpc/pmc_rios/Brain/2dunet/AB_paxsixdapi/val/{0}'.format(g), new)


