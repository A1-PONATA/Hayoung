import cv2
from imutils.video import VideoStream


webcam = VideoStream(src=0).start()

#picam = VideoStream(usePiCamera=True).start()

while True:
    ret, frame = webcam.read()
    # frame is input images'data

    cv2.imshow('nanoCam', frame)
    if cv2.waitKey(1) == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()