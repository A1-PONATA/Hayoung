import threading
import time
import random
from keras.models import load_model
from keras.models import model_from_json
import json
import cv2
import h5py

counter = 1

def getVideo():
    global counter,model
    cap = cv2.VideoCapture(0)

    while(True):
        # Captrue frame-by-frame
        ret, frame = cap.read()

        # frame resize
        frame = cv2.resize(frame,(64,64), None, interpolation=cv2.INTER_AREA)
        # Our operations on the frame come here

        gray = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
        gray=gray.reshape(1,64,64,3)


        #print(model)
        #prediction=model.predict(gray)
        #print(prediction)

        # Display the resulting frame-+
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the captrue
    cap.release()
    cv2.destroyAllWindows()

def predict():
    global counter
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
    with open('/home/pirl/A1-PONATA/Hayoung/motion_model_test/model_test.json','r') as f:
        model_json = json.load(f)
        s1 = json.dumps(model_json)
        model_json = json.loads(s1)
        model_json=json.dumps(model_json)
    model = model_from_json(model_json)
    model.load_weights('/home/pirl/A1-PONATA/Hayoung/motion_model_test/model_test.h5')


    main()