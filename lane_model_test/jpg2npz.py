import numpy as np
import os
import cv2
#from scipy.misc import imrea, imresize
#import xml.etree.ElemntTree as ET

print("Package loaded")
labels={"st":0, "lane_right":1, "lane_left":2}
cwd = os.getcwd()



#print("Current folder is %s"%cwd)

imgpath = "/home/pirl/A1-PONATA/Hayoung/lane_model_test/data/lane"
savePath = "/home/pirl/A1-PONATA/Hayoung/lane_model_test/data/lane_npz"
idx=0
print(labels['st'])

for dir in os.listdir(imgpath):
    #print(imgpath+'/'+dir)
    if not os.path.exists(savePath+'/'+dir):

        os.mkdir(savePath+'/'+dir)

    origin_path = imgpath+'/'+dir
    save_path = savePath+'/'+dir

    savePath2 = "/home/pirl/A1-PONATA/Hayoung/lane_model_test/data/lane_npz/training_data"

    for original_file in os.listdir(origin_path):
        label = labels[dir]
        #print(label)
        #print(save_path+"/"+original_file.split('.')[0]+".npz")
        img = cv2.imread(origin_path+'/'+original_file, cv2.IMREAD_GRAYSCALE)
        shrink = cv2.resize(img,(64,64), None, interpolation=cv2.INTER_AREA)
        print(shrink.shape)
        encoding = np.eye(3)[labels[dir]]
        print(encoding)
        np.savez(savePath2+"/"+str(10000+idx)+".npz", train=shrink, training_labels=encoding )
        idx+=1
