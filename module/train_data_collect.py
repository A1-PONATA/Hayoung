from evdev import InputDevice, categorize, ecodes, KeyEvent
from adafruit_servokit import ServoKit
import inputs
import time
import threading
import queue
from time import sleep
import os
import cv2
import numpy as np

count = 0

def gstreamer_pipeline(
    capture_width=120,#1280,
    capture_height=320,#720,
    display_width=120,#1280,
    display_height=320,#720,
    framerate=15,
    flip_method=2,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (capture_width,capture_height,framerate,flip_method,display_width,display_height,))

def show_camera(name , q):
    idx = 1
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        #window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window

        while 1:
            ret_val, img = cap.read() # img is input image's data
            #cv2.imshow("CSI Camera", img)
            # This also acts as

            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break
            time.sleep(0.05)
            global count
            #cv2.imwrite('test%s.jpg' % count, img)
            q.put(img)
            count += 1
            break
        cap.release()

        #cv2.destroyAllWindows()
    else:
        print("Unable to open camera")



if __name__ == "__main__":
    BUF_SIZE = 1024
    q = queue.Queue(BUF_SIZE)

    kit = ServoKit(channels=16)
    #daily random value : event 0~4
    gamepad = InputDevice('/dev/input/event5')

    print("initial setting")
    target = ['Forward', 'Right', 'Left']
    labels ={'Forward':0, 'Right':1, 'Left':2}

    kit.continuous_servo[0].throttle = 0
    kit.servo[1].angle = 113
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            kit.continuous_servo[0].throttle = 0
            keyevent = categorize(event)
            #Back
            if keyevent.keystate == KeyEvent.key_down:
                if keyevent.keycode[0] == 'BTN_A':

                    kit.servo[1].angle = 113
                    kit.continuous_servo[0].throttle = -0.18
                #Forward
                elif keyevent.keycode[1] == 'BTN_Y':
                    t = threading.Thread(target=show_camera, args=("Thread-1", q))
                    t.start()
                    t.join()
                    print("Forward")

                    X = q.get()
                    file_name = str(int(time.time()))
                    directory = "training_data"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    try:
                        encoding=np.eye(3)[labels['Forward']]
                        np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=encoding)
                    except IOError as e:
                        print(e)
                    kit.servo[1].angle = 107#113
                    kit.continuous_servo[0].throttle = 0.2


                elif keyevent.keycode[0] == 'BTN_B':
                    t = threading.Thread(target=show_camera, args=("Thread-1", q))
                    t.start()
                    t.join()
                    print("Right")
                    X = q.get()
                    file_name = str(int(time.time()))
                    directory = "training_data"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    try:
                        encoding=np.eye(3)[labels['Right']]
                        np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=encoding)
                    except IOError as e:
                        print(e)

                    kit.servo[1].angle = 85
                    kit.continuous_servo[0].throttle = 0.18


                elif keyevent.keycode[1] == 'BTN_X':
                    t = threading.Thread(target=show_camera, args=("Thread-1", q))
                    t.start()
                    t.join()
                    print("Left")
                    X = q.get()
                    file_name = str(int(time.time()))
                    directory = "training_data"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    try:
                        encoding=np.eye(3)[labels['Left']]
                        np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=encoding)
                    except IOError as e:
                        print(e)

                    kit.servo[1].angle = 145
                    kit.continuous_servo[0].throttle = 0.18

