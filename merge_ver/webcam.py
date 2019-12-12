import time
import cv2

def get_frame():


    # VideoCapture :: If it does not work, try setting to '1' instead of '0'
    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FPS, 10)
    cam.set(3, 180)  # 3 : width
    cam.set(4, 240)  # 4 : height
    # time.sleep(0.1)
    ret, frame = cam.read()
    t1 = time.time()
    while True:
        if time.time() - t1 > 3 :
            break
        ret, frame = cam.read()
        time.sleep(0.1)

    cam.release()
    cv2.destroyAllWindows()

    return frame