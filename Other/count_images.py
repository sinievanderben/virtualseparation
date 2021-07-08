# Count how many images in a folder there are
import os
import glob

# The folder of interest 
fileslist1 = glob.glob("/hpc/pmc_rios/Brain/2dunet/AB_input_dapi_meanmemb_3/test/*.png")

# Open txt file to get the number 
f = open('/hpc/pmc_rios/Brain/2dunet/number_of_instances_dataset1.txt', 'a')

count = 0

for i in fileslist1:
    count = count +1

print('Dataset 1 test: ', count, file =f)

# Other folder of interest   
fileslist2 = glob.glob("/hpc/pmc_rios/Brain/2dunet/AB_input_dapi_meanmemb_3/train/*.png")

count = 0

for i in fileslist2:
    count = count +1
    
print('Dataset 1 train: ', count, file =f)
    
# Other folder of interest 
fileslist3 = glob.glob("/hpc/pmc_rios/Brain/2dunet/AB_input_dapi_meanmemb_3/val/*.png")

count = 0

for i in fileslist3:
    count = count + 1
    
print('Dataset 1 val', count, file =f)





