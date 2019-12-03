import multiprocessing
import threading
import time
import numpy as np
import cv2
from tensorflow.python.keras.models import load_model


def main():
    t0=time.time()
    threads=[]

    for i in range(2):
        if i==0:
            thread = threading.Thread(target=getVideo(), args=())
        else:
            thread = threading.Thread(target=getModel('video_model_3.h5'),args=())
        threads.append(thread)
        thread.start()


        for i in threads:
            i.join()

        t1=time.time()
        totalTime = t1-t0
        print("Total Execution Time {}".format(totalTime))




def myProcess():
    print("Currently Executing Child Process")
    print("This process has it's own instance of the GIL")
    print("Executing Main Process")
    print("Creating Child Process")
    getVideo()


def getModel(path):

    model =load_model(path)

    print(model)

def getVideo():

    cap = cv2.VideoCapture(0)

    while(True):
        # Captrue frame-by-frame
        ret, frame = cap.read()


        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame-+
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the captrue
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #getVideo()
#     getModel('video_model_3.h5')

    # myProcess=multiprocessing.Process(target=myProcess())
    # myProcess.start()
    # myProcess.join()
    # print('Chid Process has terminated, terminationg main process')
    #
    main()