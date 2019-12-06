import numpy as np
import os
import cv2
#from scipy.misc import imrea, imresize
#import xml.etree.ElemntTree as ET

print("Package loaded")
labels={"fastpass":0, "left2right":1, "right2left":2}
cwd = os.getcwd()



#print("Current folder is %s"%cwd)

imgpath = "/home/pirl/Documents/splited_action_data"
savePath = "/home/pirl/Documents/final_data120_320"
idx=0

dirList=['fastpass','left2right','right2left']
for dir in dirList:

    origin_path = imgpath+'/'+dir
    file_cnt=0
    for original_file in os.listdir(origin_path):
        label = labels[dir]
        #print(label)
        for real_file in os.listdir(origin_path+'/'+original_file):
            print(origin_path+'/'+original_file+'/'+real_file)
            img = cv2.imread(origin_path + "/" + original_file+"/"+real_file, cv2.IMREAD_COLOR)
            shrink = cv2.resize(img,(120,320), None, interpolation=cv2.INTER_AREA)
            encoding = np.eye(3)[labels[dir]]
            np.savez(savePath+"/"+str(10000+idx)+".npz", train=shrink, training_labels=encoding )
            idx+=1

        file_cnt+=1
        if file_cnt > 200:
            break

