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


## GLOBAL VARIABLES...

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

with tf.Session(config=config) as session:
    init = tf.compat.v1.global_variables_initializer()
    graph = tf.compat.v1.get_default_graph()

    session.run(init)
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

    def show_camera():
        global q
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
                #img = cv2.imread(img)
                img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
                #print(img.shape)
                img = img.reshape(-1,320,120,1)
                keyCode = cv2.waitKey(30) & 0xFF
                # Stop the program on the ESC key
                if keyCode == 27:
                    break
                q.put(img)

                time.sleep(0.05)

                break
            cap.release()

            #cv2.destroyAllWindows()
        else:
            print("Unable to open camera")

    def drive_control(dir):
        if dir == 0:
            # Forward(Straight)
            kit.servo[1].angle = 107
            kit.continuous_servo[0].throttle = 0.18
            return
        elif dir ==1:
            # Right
            kit.servo[1].angle = 85
            kit.continuous_servo[0].throttle = 0.18
            return
        elif dir ==2:
            # Left
            kit.servo[1].angle = 145
            kit.continuous_servo[0].throttle = 0.18
            return

        elif dir ==3:
            # BackWard
            kit.servo[1].angle = 113
            kit.continuous_servo[0].throttle = -0.18
            return

    def predict():
        global lane_model,q
        X = q.get()

        with graph.as_default():
            set_session(session)

            pred_raw=lane_model.predict(X)
            if np.argmax(pred_raw)<0.5 : # threashold : 가장 높은 확률로 예측된 class의 확률이 50% 미만이면 go straight
                pred=0
            else:
                pred=np.argmax(pred_raw)
            #print("predicted value is ",np.argmax(lane_model.predict(X)))

            drive_control(pred)

    def main():
        t0 = time.time()
        thread1 = threading.Thread(target=show_camera)
        thread2 = threading.Thread(target=predict)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        t1 = time.time()

        print("Execution Time {}".format(t1-t0))


    if __name__ == "__main__":
        kit, gamepad,q=[None,None,None]

        BUF_SIZE = 4096
        q = queue.Queue(BUF_SIZE)

        kit = ServoKit(channels=16)
        #gamepad =InputDevice('/dev/input/event4')

        # target = ['Forward', 'Right', 'Left']
        # labels ={'Forward':0, 'Right':1, 'Left':2}

        # Initialize Donkey car,..
        kit.continuous_servo[0].throttle = 0
        kit.servo[1].angle = 113

        # Initialize Model...
        yaml_file = open('/home/ponata/A1-PONATA/Hayoung/lane_model_test/lane_model_v1.yaml', 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        lane_model = model_from_yaml(loaded_model_yaml)

        # load weights into new model
        lane_model.load_weights("/home/ponata/A1-PONATA/Hayoung/lane_model_test/lane_model_v1.h5")
        lane_model._make_predict_function()

        print("Initail Settings are done.\n")


        # START THREAD
        while True:
            main()