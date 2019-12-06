import cv2


def gstreamer_pipeline(
        capture_width=120,  # 1280,
        capture_height=320,  # 720,
        display_width=120,  # 1280,
        display_height=320,  # 720,
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
            % (capture_width, capture_height, framerate, flip_method, display_width, display_height,))

def show_camera():

    idx = 1
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        # window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window

        while 1:
            ret_val, img = cap.read()  # img is input image's data
            # cv2.imshow("CSI Camera", img)
            # This also acts as
            # img = cv2.imread(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            # print(img.shape)
            img = img.reshape(-1, 320, 120, 1)
            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                break
            q.put(img)

            time.sleep(0.05)

            break
        cap.release()

        # cv2.destroyAllWindows()
    else:
        print("Unable to open camera")