import numpy as np  
import h5py

f = h5py.File('/hpc/pmc_rios/Brain/190910_rl57_fungi_16bit_25x_125um_corr-stitching_bfc.ims', "r")

save_file = open("/hpc/pmc_rios/Brain/2dunet/intensity_channels.txt", "a")

start_layer = 0
end_layer = 111

arrays = False

for i in range(start_layer, end_layer+1):
    # Take layer per channel
    dapi = f['DataSet/ResolutionLevel 4/TimePoint 0/Channel 0/Data'][i] 

    ki67 = f['DataSet/ResolutionLevel 4/TimePoint 0/Channel 1/Data'][i] 

    pax8 = f['DataSet/ResolutionLevel 4/TimePoint 0/Channel 2/Data'][i] 

    ncam1 = f['DataSet/ResolutionLevel 4/TimePoint 0/Channel 3/Data'][i] 

    six2 = f['DataSet/ResolutionLevel 4/TimePoint 0/Channel 4/Data'][i] 

    chd1 = f['DataSet/ResolutionLevel 4/TimePoint 0/Channel 5/Data'][i] 

    chd6 = f['DataSet/ResolutionLevel 4/TimePoint 0/Channel 6/Data'][i] 

    factin = f['DataSet/ResolutionLevel 4/TimePoint 0/Channel 7/Data'][i] 


    if not arrays:
        arrays = True
        d_array = dapi
        k_array = ki67
        p_array = pax8
        n_array = ncam1
        s_array = six2
        c1_array = chd1
        c6_array = chd6
        f_array = factin
    
    else:
        d_array = np.concatenate((d_array, dapi))
        print(d_array.shape)
        k_array = np.concatenate((k_array, ki67))
        p_array = np.concatenate((p_array, pax8))
        n_array = np.concatenate((n_array, ncam1))
        s_array = np.concatenate((s_array, six2))
        c1_array = np.concatenate((c1_array, chd1))
        c6_array = np.concatenate((c6_array, chd6))
        f_array = np.concatenate((f_array, factin))

print('dapi 99 percentile: ', np.percentile(d_array, 99), file = save_file)
print('dapi 95 percentile: ', np.percentile(d_array, 95), file = save_file)
print('ki67 99 percentile: ', np.percentile(k_array, 99), file = save_file)
print('ki67 95 percentile: ', np.percentile(k_array, 95), file = save_file)
print('pax8 99 percentile: ', np.percentile(p_array, 99), file = save_file)
print('pax8 95 percentile: ', np.percentile(p_array, 95), file = save_file)
print('ncam1 99 percentile: ', np.percentile(n_array, 99), file = save_file)
print('ncam1 95 percentile: ', np.percentile(n_array, 95), file = save_file)
print('six2 99 percentile: ', np.percentile(s_array, 99), file = save_file)
print('six2 95 percentile: ', np.percentile(s_array, 95), file = save_file)
print('chd1 99 percentile: ', np.percentile(c1_array, 99), file = save_file)
print('chd1 95 percentile: ', np.percentile(c1_array, 95), file = save_file)     
print('chd6 99 percentile: ', np.percentile(c6_array, 99), file = save_file)
print('chd6 95 percentile: ', np.percentile(c6_array, 95), file = save_file)    
print('factin 99 percentile: ', np.percentile(f_array, 99), file = save_file)
print('factin 95 percentile: ', np.percentile(f_array, 95), file = save_file)    
