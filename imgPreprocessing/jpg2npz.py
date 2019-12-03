import numpy as np
import os
import cv2
#from scipy.misc import imrea, imresize
#import xml.etree.ElemntTree as ET

print("Package loaded")
labels={"fp":0, "lr":1, "rl":2}
cwd = os.getcwd()

#print("Current folder is %s"%cwd)

def jpg2npz(size=(), filepath=(), IMREAD_TYPE = 0, refDir=[]):


    idx = 0

    path = {0:filepath[0], 1:filepath[1]}


    for dir in refDir:
        origin_path = path[0] + '/' + dir
        print(dir)
        for original_file in os.listdir(origin_path):
            label = labels[dir] # print: 0,1,2

            for real_file in os.listdir(origin_path + '/' + original_file):

                # Grayscale(0) vs COLOR(1)
                if IMREAD_TYPE == 0:
                    img = cv2.imread(origin_path + "/" + original_file + "/" + real_file, cv2.IMREAD_GRAYSCALE)
                else:
                    img = cv2.imread(origin_path + "/" + original_file + "/" + real_file, cv2.IMREAD_COLOR)

                shrink = cv2.resize(img, (size[0], size[1]), None, interpolation=cv2.INTER_AREA)

                encoding = np.eye(3)[label]

                # save numpy files
                np.savez(path[1] + "/" + str(10000 + idx) + ".npz", train=shrink, training_labels=encoding)
                idx += 1


imgpath = "/home/pirl/Pictures/new_img"
savePath = "/home/pirl/Pictures/save_img"
jpg2npz((64, 64), (imgpath,savePath), 0, refDir=['fp', 'lr', 'rl'])