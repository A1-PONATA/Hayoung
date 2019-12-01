import threading
import urllib.request
import time

def downloadImage(imagePath, fileName):
    print("Downloading Image from ", imagePath)
    urllib.request.urlretrieve(imagePath, fileName)
    print("Completed Download")

def executeTrehad(i):
    imageName = "temp/image-"+str(i)+".jpg"
    downloadImage("http://lorempixel.com/400/200/sports",imageName)


def main():
    t0 = time.time()
    # 모든 스레드 형태를 저장하는 배열을 생성한다.
    threads=[]
    # 10개의 스레드를 생성하고, 배열에 추가하며, 실행해본다.

    for i in range(10):
        thread = threading.Thread(target=executeTrehad, args=(i,))
        threads.append(thread)
        thread.start()

    # 배열 내의 모든 스레드는 전체 종료 시간을 기록하기 전
    # 모든 실행을 마친다.

    for i in threads:
        i.join()

    # 전체 실행 시간을 계산한다.
    t1 = time.time()
    totalTime = t1-t0
    print("Total Execution Time {}"/format(totalTime))

if __name__=="__main__":
    main()