from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)


def control(dir):
    if dir == 0:
        # Forward(Straight)
        kit.servo[1].angle = 107
        kit.continuous_servo[0].throttle = 0.18
        return kit
    elif dir == 1:
        # Right
        kit.servo[1].angle = 85
        kit.continuous_servo[0].throttle = 0.18
        return kit
    elif dir == 2:
        # Left
        kit.servo[1].angle = 145
        kit.continuous_servo[0].throttle = 0.18
        return kit

    elif dir == 3:
        # BackWard
        kit.servo[1].angle = 113
        kit.continuous_servo[0].throttle = -0.18
        return kit

def init():
    kit.continuous_servo[0].throttle = 0
    kit.servo[1].angle = 113

    return kit