import threading
#import public.Camera.face_detect as face_detect
import real_time_camera
import webcam_conn
import face_detect
from queue import Queue

def creator():
    print("Createing data and putting it on the queue")
    print("\n")
    real_time_camera.show_camera()
    #face_detect.faceDetect()
    # for item in data:
    #     evt = threading.Event()
    #     #q.put((item, evt))
    #     print('creator')
    #     #evt.wait()

def consumer():
    webcam_conn.human_detect()
    #data, evt = q.get()
    print('~')
    #processed = data * 5
    print('~~')
    print('\n')
    #evt.set()
    #q.task_done()

if __name__ == '__main__':
    q = Queue()

    data=[7, 14, 39, 59, 77, 1, 109, 99, 167, 920, 1035]

    thread_one = threading.Thread(target=creator)
    thread_two = threading.Thread(target=consumer)
    thread_one.start()
    thread_two.start()
    #q.join()qqqqweqwe
    #1123123qqqqweqw