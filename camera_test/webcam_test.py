import numpy as np
import cv2
from keras.utils import np_utils
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Activation
from numpy import argmax


def getVideo():

    cap = cv2.VideoCapture(0)

    while(True):
        # Captrue frame-by-frame
        ret, frame = cap.read()


        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the captrue
    cap.release()
    cv2.destroyAllWindows()

if __name__=="main":
    getVideo()