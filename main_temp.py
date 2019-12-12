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
import tensorflow as tf
from tensorflow.python.keras.models import model_from_yaml
from tensorflow.python.keras.backend import set_session
from merge_ver import ultraSonic
from merge_ver import drive_control as drive_control
from merge_ver import load_model as lm
from merge_ver import picam
import logging
from merge_ver import webcam

## GLOBAL VARIABLES...

LOGGING_lEVELS={'critical':logging.CRITICAL,
                'error':logging.ERROR,
                'warning': logging.WARNING,
                'info':logging.INFO,
                'debug': logging.DEBUG}

camera = []
list_set = []
count = 0
#kit,gamepad,loaded_model,q=[None,None,None,None]


config = tf.ConfigProto(
device_count={'GPU': 1},
intra_op_parallelism_threads=1,
allow_soft_placement=True
)

os.environ['CUDA_VISIBLE_DEVICES'] = '1'
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.6

def get_lane_view():
    # using picam
    global q
    while True:
        q.put(picam.show_camera())
    return

def get_motion_view():
    # using webcam
    global q2
    q2.put(webcam.get_frame())

    print('current size of motion queue is  ',q2.qsize())

def predict():
    global lane_model,motion_model,q,ir, q2, session, mylogger
    while True:
        X = q.get()
        IR = ir.get()

        with graph.as_default():
            set_session(session)
            if IR:
                pred_raw = lane_model.predict(X)

                kit.servo[1].angle, kit.continuous_servo[0].throttle=drive_control.control(np.argmax(pred_raw))
                kit.continuous_servo[0].throttle, t=drive_control.sleep()
                time.sleep(t)
                mylogger.info('Lane model prediction value is '+str(np.argmax(pred_raw)))
                #print("LANE MODEL PREDICTION IS ", np.argmax(pred_raw), "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            else:
                get_motion_view() # first, get web cam frame
                if not q2.empty():
                    motion = q2.get()
                    print("MOTION MODEL IS CALLED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                       # kit.continuous_servo[0].throttle = 0
                    # kit.servo[1].angle = 107
                    pred = np.argmax(motion_model.predict(motion))
                    mylogger.info('Motion model prediction value is '+str(np.argmax(pred)))

                    kit.servo[1].angle, kit.continuous_servo[0].throttle = drive_control.control(np.argmax(pred))
                    kit.continuous_servo[0].throttle, t = drive_control.sleep()
                    time.sleep(t+0.5)


def check_dist():
    global ir
    while True:
        disList=[]

        # Sometimes it measured anomaly distance, so we must median value of 10 times measurement.
        for i in range(10):
            disList.append(ultraSonic.distance())

        dist = np.median(np.array(disList))

        print("Detected distance is ",dist)

        if dist < 40: # stop
            ir.put(False)

        else: # keep run
            ir.put(True)

def main():
    t0 = time.time()
    thread1 = threading.Thread(target=get_lane_view)
    thread2 = threading.Thread(target=predict)
    thread3 = threading.Thread(target=check_dist)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    t1 = time.time()

    print("Execution Time {}".format(t1-t0))

if __name__ == "__main__":
    kit, gamepad, q, ir, q2=[None, None,None,None,None]
    mylogger = logging.getLogger("my")
    mylogger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    mylogger.addHandler(stream_handler)

    #mylogger.info('server start!!')

    BUF_SIZE = 4096
    q = queue.Queue(BUF_SIZE)
    q2 = queue.Queue(BUF_SIZE)
    ir = queue.Queue(BUF_SIZE)


    kit = ServoKit(channels=16)
    #gamepad =InputDevice('/dev/input/event4')

    # target = ['Forward', 'Right', 'Left']
    # labels ={'Forward':0, 'Right':1, 'Left':2}

    # Initialize Donkey car,..
    kit.continuous_servo[0].throttle = 0
    kit.servo[1].angle = 107

    # Load lane model...
    lane_model_path=['/home/ponata/A1-PONATA/Hayoung/lane_model_test/lane_model_v3-03.yaml',
                     "/home/ponata/A1-PONATA/Hayoung/lane_model_test/lane_model_v3-03.h5"]
    lane_model = lm.load_model(lane_model_path)

    #Load motion model...
    motion_model_path=['/home/ponata/A1-PONATA/Hayoung/motion_model_test/motion_model_demoV0.yaml',
                       "/home/ponata/A1-PONATA/Hayoung/motion_model_test/motion_model_demoV0.h5"]
    motion_model = lm.load_model(motion_model_path)

    print("Initial Settings are done.\n")

    # START THREAD

    with tf.Session(config=config) as session:
        init = tf.compat.v1.global_variables_initializer()
        graph = tf.compat.v1.get_default_graph()

        session.run(init)
        main()
        # while True:
        #     main()