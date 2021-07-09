import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import glob
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Get location of the test images 
filepath = r'E:\Stage\test_latest\images'

filenames = os.listdir(filepath)


# Absolute error of the two arrays
def _error(actual: np.ndarray, predicted: np.ndarray):

    return np.sum(abs(actual - predicted))

# Absolute error in percentages 
def _percentage_error_all_division(actual: np.ndarray, predicted: np.ndarray):
    
    return (_error(actual,predicted) / (512*512*255)) * 100

count = 0 

dapiD_2 = dict()
membD_2 = dict()
dapiS_2 = dict()
membS_2 = dict()

for img in filenames:

    if 'fake' in img:
        imageA = cv2.imread('{0}/{1}'.format(filepath, img))

        dapi = imageA[:, :, 2]  #  third channel, cv2 reads as BGR
        memb = imageA[:, :, 1]

        z = img.replace('_fake_B', '_real_B')
        print(z, file = f)

        count = z.replace('13312_13824_', '')
        count = count.replace('_3584_input_nuclmemb_real_B.png', '')
        count = int(count)

        imageB = cv2.imread('{0}/{1}'.format(filepath, z))

        true_dapi = imageB[:, :, 2]  
        true_memb = imageB[:, :, 1]

        dapi = dapi.astype(np.float64)
        true_dapi = true_dapi.astype(np.float64)
        memb = memb.astype(np.float64)
        true_memb = true_memb.astype(np.float64)

        dapiD_2[count] = _percentage_error_all_division(true_dapi, dapi)
        print('dapi err: ', _percentage_error_all_division(true_dapi, dapi), file =f)

        dapiS_2[count] = ssim(dapi, true_dapi, gaussian_weights=True, sigma=1.5, use_sample_covariance=False, win_size=11, data_range = 255)

        membD_2[count] = _percentage_error_all_division(true_memb, memb)
        print('memb err: ', _percentage_error_all_division(true_memb, memb), file =f )

        membS_2[count] = ssim(memb, true_memb, gaussian_weights=True, sigma=1.5, use_sample_covariance=False, win_size=11, data_range = 255)
 

# Set style
mpl.style.use('ggplot')

# 30 dmm
dapiList2 = dapiS_2.items()
dapiList2 = sorted(dapiList2)[20:102]
x_d2, y_d2 = zip(*dapiList2)

membList2 = membS_2.items()
membList2 = sorted(membList2)[20:102]
x_m2, y_m2 = zip(*membList2)

# Abs err

# 30 dmm
dapiListE_2 = dapiD_2.items()
dapiListE_2 = sorted(dapiListE_2)[20:102]
x_de_2, y_de_2 = zip(*dapiListE_2)

membListE_2 = membD_2.items()
membListE_2 = sorted(membListE_2)[20:102]
x_me_2, y_me_2 = zip(*membListE_2)


fig, (axs1, axs2) = plt.subplots(1, 2, figsize=(15,5))

line_labels = ['DAPI dmm', 'mean membrane dmm']
ymin = 0
ymax = 1

# SSIM
l3 = axs1.plot(x_d2, y_d2, color = '#F8766D')[0]
l4 = axs1.plot(x_m2, y_m2, color = '#00BFC4')[0]
axs1.set_ylim([ymin,ymax])
#axs1.set_title("SSIM 3D")

# abs err 
axs2.plot(x_de_2, y_de_2, color = '#F8766D')
axs2.plot(x_me_2, y_me_2, color = '#00BFC4')
#axs2.set_title("Absolute error 3D")
axs2.set_ylim([0, 10])
axs2.sharex(axs2)

# legend
fig.legend([l3, l4],     # The line objects
           labels=line_labels,   # The labels for each line
           loc="center right",   # Position of legend
           borderaxespad=0.1    # Small spacing around legend box
           )
plt.subplots_adjust(right=0.80)

plt.savefig('3d_dmm_only_new.png')
plt.savefig('3d_dmm_only_new.pdf')





