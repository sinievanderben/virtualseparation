import pickle 
import glob
import os
import torch 

models = [r'E:\virtualseparation2\Experiment1\Trainsize\Models']
parameterModels = r'E:\virtualseparation2\Experiment1\Parameters\Models'

paxandsixModels = r'E:\virtualseparation2\Experiment2\Models'

paxsixmeanModels = r'E:\virtualseparation2\Experiment3\Models'

for i in models:
    print(i)
    modelList = os.listdir(i)
    for j in modelList:
        place = i + '\\' + j 
        print(place)
        getObjects = os.listdir(place)
        new_place = r'E:\virtualseparation\Experiment1\Trainsize\Models' + '\\' + j
        print(new_place)
        for x in getObjects:
            if x == 'latest_net_D.pth':
                with open(new_place + '\\' + 'latest_net_D.pickle', "wb") as f:
                    pretrained = torch.load(place + '\\' + x)
                    pickle.dump(pretrained, f)
                    f.close()
            if x == 'latest_net_G.pth':
                with open(new_place + '\\' + 'latest_net_G.pickle', "wb") as f2:
                    pretrained = torch.load(place + '\\' + x)
                    pickle.dump(pretrained, f2)
                    f.close()
                       
