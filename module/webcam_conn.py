import cv2


def human_detect():
    print(cv2.__version__)
    dispW = 640
    dispH = 480
    flip = 2
    # Uncomment These next Two Line for Pi Camera
    camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    cam= cv2.VideoCapture(camSet)

    # Or, if you have a WEB cam, uncomment the next line
    # (If it does not work, try setting to '1' instead of '0')
    #cam = cv2.VideoCapture(1)

    while True:
        ret, frame = cam.read()
        # frame is input images'data

        cv2.imshow('nanoCam', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    human_detect()
