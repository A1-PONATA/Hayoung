import numpy as np
import os
import cv2
#from scipy.misc import imrea, imresize
#import xml.etree.ElemntTree as ET

print("Package loaded")
labels={"fastpass":0, "left2right":1, "right2left":2}
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
            movie_data = np.empty((0,320, 320, 3))
            for real_file in os.listdir(origin_path + '/' + original_file):

                # Grayscale(0) vs COLOR(1)
                if IMREAD_TYPE == 0:
                    img = cv2.imread(origin_path + "/" + original_file + "/" + real_file, cv2.IMREAD_GRAYSCALE)
                else:
                    img = cv2.imread(origin_path + "/" + original_file + "/" + real_file, cv2.IMREAD_COLOR)

                shrink = cv2.resize(img, (size[0], size[1]))
                #print(img.shape,shrink.shape)
                shrink=np.reshape(shrink,[-1,320,320,3])

                movie_data=np.vstack([movie_data,shrink])


            encoding = np.eye(3)[label]

                # save numpy files
            print(movie_data.shape, encoding)
            break
            #np.savez(path[1] + "/" + str(10000 + idx) + ".npz", train=shrink, training_labels=encoding)

            idx += 1


imgpath = "/home/pirl/Documents/splited_action_data"
savePath = "/home/pirl/Pictures/save_img"

jpg2npz((320, 320), (imgpath,savePath), 1, refDir=['fastpass', 'left2right', 'right2left'])