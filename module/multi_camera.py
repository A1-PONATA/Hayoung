import threading
#import public.Camera.face_detect as face_detect
import real_time_camera
import webcam_conn
from queue import Queue

cnt=0
def creator():
    global cnt
    real_time_camera.show_camera(cnt)
    cnt+=1

def consumer():
    global cnt
    webcam_conn.human_detect(cnt)
    cnt+=1

if __name__ == '__main__':
    q = Queue()


    thread_one = threading.Thread(target=creator)
    thread_two = threading.Thread(target=consumer)
    thread_one.start()
    thread_two.start()

