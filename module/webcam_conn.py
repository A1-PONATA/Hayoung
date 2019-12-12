import cv2
import time

def human_detect(cnt=1):
    dispW = 320
    dispH = 320
    flip = 2
    # Uncomment These next Two Line for Pi Camera
    # camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    # cam= cv2.VideoCapture(camSet)

    # Or, if you have a WEB cam, uncomment the next line
    # (If it does not work, try setting to '1' instead of '0')
    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FPS, 10)
    cam.set(3, 320) # 3 : width
    cam.set(4, 320) # 4 : height
    #time.sleep(0.1)
    ret,frame=cam.read()
    while True:
        ret, frame = cam.read()
        # frame is input images'data
        # time.sleep(1)
        # print('webcam')
        # print(frame)
        time.sleep(0.1)
        #if cnt % 5000 ==0:
            #print('******************Web-Cam**********************************',frame[0,0])
        cv2.imshow('nanoCam', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return frame


if __name__ == "__main__":
    human_detect()

