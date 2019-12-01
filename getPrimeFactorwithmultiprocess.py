import time
import random
from multiprocessing import Process

def calculatePrimeFactors(n):
    primfac=[]
    d=2

    while d*d <=n:
        while(n % d )==0:
            primfac.append(d)
            n//=d
        d+=1

    if n>1:
        primfac.append(n)

    return primfac

def executeProc():
    for i in range(1000):
        rand = random.randint(2000, 100000000)
        print(calculatePrimeFactors(rand))


def main():
    print("Starting number crunching")
    t0 = time.time() # starting time

    procs=[]

    for i in range(10):
        proc = Process(target=executeProc, args=())
        procs.append(proc)
        proc.start()

    # 모든 프로세스가 종료할 때까지 대기하고자,
    # 다시한번, .join() 메소드를 사용한다.

    for proc in procs:
        proc.join()

    t1=time.time() # end time
    totalTime = t1-t0

    print("Execution Time : {}".format(totalTime))

if __name__=="__main__":
    main()