import numpy as np
import os
import cv2
#from scipy.misc import imrea, imresize
#import xml.etree.ElemntTree as ET

print("Package loaded")
labels={"fp":0, "lr":1, "rl":2}
cwd = os.getcwd()



#print("Current folder is %s"%cwd)

imgpath = "/home/pirl/Documents/splited_action_data2"
savePath = "/home/pirl/Documents/splited_action_data2/npz_data15"
idx=0

dirList=['fp','lr','rl']
for dir in dirList:

    origin_path = imgpath+'/'+dir
    print(dir)
    for original_file in os.listdir(origin_path):
        label = labels[dir]
        #print(label)
        for real_file in os.listdir(origin_path+'/'+original_file):
            #print(origin_path + "/" + original_file+"/"+real_file)
            #print(savePath+"/"+original_file.split('.')[0]+".npz")
            img = cv2.imread(origin_path + "/" + original_file+"/"+real_file, cv2.IMREAD_COLOR)
            shrink = cv2.resize(img,(64,64), None, interpolation=cv2.INTER_AREA)
            #print(shrink.shape)
            encoding = np.eye(3)[labels[dir]]
            #print(encoding)
            #print(savePath+"/"+str(10000+idx)+".npz")
            np.savez(savePath+"/"+str(10000+idx)+".npz", train=shrink, training_labels=encoding )
            idx+=1

