import threading
import time
import random
import cv2
from tensorflow.python.keras.models import model_from_yaml
from tensorflow.python.keras.backend import set_session
from keras import backend as K
import tensorflow as tf
import numpy as np



counter = 1
loaded_model=''
config = tf.ConfigProto(
    device_count={'GPU': 1},
    intra_op_parallelism_threads=1,
    allow_soft_placement=True
)
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.6

with tf.Session(config=config) as session:
    init = tf.global_variables_initializer()
    graph = tf.get_default_graph()

    session.run(init)


    def getVideo():
        global counter,loaded_model,session, graph,init

        counter+=1
        cap = cv2.VideoCapture(0)
        while(True):
            # Captrue frame-by-frame
            ret, frame = cap.read()

            # frame resize
            frame = cv2.resize(frame,(120,320), None, interpolation=cv2.INTER_AREA)
            # Our operations on the frame come here

            gray = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
            gray=gray.reshape(1,120,320,3)

            # print(gray.shape)
            # print(loaded_model.summary())
            # prediction=loaded_model.predict(gray)
            # print(prediction)

            print(tf.test.is_gpu_available())

            with graph.as_default():
                set_session(session)
                #print(loaded_model.summary())
                prediction=loaded_model.predict(gray, verbose=1)
                print(prediction,np.argmax(prediction))
            # with session.as_default():
            #     with session.graph.as_default():
            #         predicted_labels = loaded_model.predict(gray, verbose=1)
            #         print(predicted_labels)


            # Display the resulting frame-
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the captrue
        cap.release()
        cv2.destroyAllWindows()

    def predict():
        global counter
        counter-=1
        print(counter)





    def workerA():
        global counter
        while counter <1000:
            counter+=1
            print("Worker A is incrementing counter to {}".format(counter))
            sleepTime = random.randint(0,1)
            time.sleep(sleepTime)

    def workerB():
        global counter
        while counter > -1000:
            counter -=1
            print("Worker B is decrementing counter to {}".format(counter))
            sleepTime = random.randint(0,1)
            time.sleep(sleepTime)

    def main():
        t0=time.time()
        thread1 = threading.Thread(target=getVideo)
        thread2 = threading.Thread(target=predict)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        t1 = time.time()

        print("Execution Time {}".format(t1-t0))

    if __name__=="__main__":

        # model = tensorflow.Model.loadLayersModel('/home/pirl/A1-PONATA/Hayoung/motion_model_test/model_test.h5')
        #
        # with open('/home/pirl/A1-PONATA/Hayoung/motion_model_test/model_test.json','r') as f:
        #     model_json = json.load(f)
        #     s1 = json.dumps(model_json)
        #     model_json = json.loads(s1)
        #     model_json=json.dumps(model_json)
        # model = tf.import_graph_def(model_json)
        # model.load_weights('/home/pirl/A1-PONATA/Hayoung/motion_model_test/model_test.h5')
        #

        #global loaded_model

        # load YAML and create model
        yaml_file = open('model.yaml', 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        loaded_model = model_from_yaml(loaded_model_yaml)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        loaded_model._make_predict_function()
        #print(loaded_model)

        main()
