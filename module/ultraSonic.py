import Jetson.GPIO as gpio
import time


def distance(measure='cm'):
    det1=False
    det2=False
    try:
        gpio.setmode(gpio.BOARD)
        gpio.setup(11, gpio.OUT)
        gpio.setup(13, gpio.IN)

        gpio.output(11, gpio.HIGH)
        time.sleep(0.00001)
        gpio.output(11, gpio.LOW)


        while gpio.input(13) == False:

            if det1==False:
                t1 = time.time()
                det1=True
            # print(t1)
            nosig =time.time()
            if((nosig-t1)>0.1):
                print("break 당했습니다.")
                break
        while gpio.input(13) == True:
            if ~det2:
                t2=time.time()
                det2=True
            sig = time.time()
            # if(sig-t2>2):
            #     break
            # print(sig - t2)

        tl = sig - nosig

        if measure == 'cm':
            distance = round((tl / 0.000058),2)
        else:
            print('improper choice of measurement: cm')
            distance = None
        gpio.cleanup()

        return distance
    except:
        distance = 100
        gpio.cleanup()
        return distance


if __name__ == "__main__":

     while 1:
        print("Distance: {0}cm".format(distance('cm')))