from evdev import InputDevice, categorize, ecodes, KeyEvent
from adafruit_servokit import ServoKit

camera = []
list_set = []

kit = ServoKit(channels=16)
gamepad = InputDevice('/dev/input/event4')

print("initial setting")

kit.continuous_servo[0].throttle = 0
kit.servo[1].angle = 113

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        kit.continuous_servo[0].throttle = 0
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
            if keyevent.keycode[0] == 'BTN_A':
                print("Back")
                kit.continuous_servo[0].throttle = -0.22

            elif keyevent.keycode[1] == 'BTN_Y':
                print("Forward")
                kit.servo[1].angle = 110
                kit.continuous_servo[0].throttle = 0.22


            elif keyevent.keycode[0] == 'BTN_B':
                print("Right")
                kit.servo[1].angle = 80
                kit.continuous_servo[0].throttle = 0.18


            elif keyevent.keycode[1] == 'BTN_X':
                print("Left")
                kit.servo[1].angle = 150
                kit.continuous_servo[0].throttle = 0.18
