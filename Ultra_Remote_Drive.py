import time
from rpi_hardware_pwm import HardwarePWM
from getkey import getkey, keys
#import RPi.GPIO as GPIO
import serial
from ultasonic import distance
from threading import Thread
from statistics import mean 

import RPi.GPIO as GPIO


if __name__ == '__main__':
    try:
        servo = HardwarePWM(pwm_channel = 0, hz = 480)
        servoDuty = 76
        servo.start(servoDuty)
        #left 64
        #right 87
        
        motor = HardwarePWM(pwm_channel = 1, hz = 480)
        motorDuty = 0
        motor.start(motorDuty)
        #75-85

        turntime = 0
        frontDist = 0.0
        rightDistPrev = 10.0
        leftDistPrev = 10.0

        speed = 76
       
        def moveRight(dist):
            if dist == 1000:
                servo.change_duty_cycle(servoDuty-10)
                motor.change_duty_cycle(speed)
                print("TURN RIGHT")
                time.sleep(0.6)
                servo.change_duty_cycle(servoDuty)
                # motor.change_duty_cycle(speed)
                time.sleep(0.5)
            elif dist <= 6:
                backUp(-8)
            elif dist <= 19:
                servo.change_duty_cycle(servoDuty-10)
                print("move right - A LOT")
                time.sleep(0.6)
                servo.change_duty_cycle(servoDuty)
            else:
                servo.change_duty_cycle(servoDuty-9)
                print("move right - correction")
                time.sleep(0.5)
                servo.change_duty_cycle(servoDuty)
        def moveLeft(dist):
            if dist == 1000:
                servo.change_duty_cycle(servoDuty+10)
                motor.change_duty_cycle(speed)
                print("TURN LEFT")
                time.sleep(0.6)
                servo.change_duty_cycle(servoDuty)
                motor.change_duty_cycle(speed)
                time.sleep(0.5)
            elif dist <= 6:
                backUp(8)
            elif dist <= 19:
                servo.change_duty_cycle(servoDuty+8)
                print("move left - A LOT")
                time.sleep(0.4)
                servo.change_duty_cycle(servoDuty) 
            else:
                servo.change_duty_cycle(servoDuty+9)
                print("move left - correction")
                time.sleep(0.3)
                servo.change_duty_cycle(servoDuty)    
        def backUp(dir):
            servo.change_duty_cycle(servoDuty)
            motor.change_duty_cycle(motorDuty)
            motor.change_duty_cycle(50)
            time.sleep(1.2)
            servo.change_duty_cycle(servoDuty+dir)
            # motor.change_duty_cycle(motorDuty)
            # motor.change_duty_cycle(50)
            time.sleep(0.2)
            servo.change_duty_cycle(servoDuty)
            motor.change_duty_cycle(speed)

        # Front
        frontTrig = 5
        frontEcho = 6

        # Right
        rightTrig = 27
        rightEcho = 22

        # Left
        leftTrig = 23 
        leftEcho = 24

        turnDistance = 19
        rightAvg = []
        leftAvg = []
        frontAvg = []
        turnIncrement = 0

        for i in range(4):
            rightDist = (distance(rightTrig, rightEcho))
            #rightAvg.append(int(rightDist))
            #print("Initial Right Dist: %0.1f" % rightDist)

            frontDist = (distance(frontTrig, frontEcho))
            #frontAvg.append(int(frontDist))
            #print("Initial Front Dist: %0.1f" % frontDist)

            leftDist = (distance(leftTrig, leftEcho))
            #leftAvg.append(int(leftDist))
            #print("Initial Left Dist: %0.1f" % leftDist)
            time.sleep(0.05)


        while True:
            servo.change_duty_cycle(servoDuty)
            motor.change_duty_cycle(speed)
            rightDist = (distance(rightTrig, rightEcho))
            #rightAvg.append(int(rightDist))
            print("Right Dist: %0.1f" % rightDist)

            frontDist = (distance(frontTrig, frontEcho))
            #frontAvg.append(int(frontDist))
            print("Front Dist: %0.1f" % frontDist)

            leftDist = (distance(leftTrig, leftEcho))
            #leftAvg.append(int(leftDist))
            print("Left Dist: %0.1f" % leftDist)

            if turnIncrement == False:
                turnIncrement -= 1
                if frontDist <= 15:
                    if rightDist < leftDist:
                        backUp(8)
                    if leftDist < rightDist:
                        backUp(-8)               
                else:
                    if rightDist <= 43:
                        t2 = Thread(target=moveLeft, args=(rightDist,))
                        t2.run()
                    if leftDist <= 43:
                        t1 = Thread(target=moveRight, args=(leftDist,))
                        t1.run()
                    print("NOT TURNING LOOP")

            else:
                if frontDist <= turnDistance-6:
                    if rightDist < leftDist:
                        backUp(0)
                    if leftDist < rightDist:
                        backUp(0)
                    print("Extreme backup")

                elif frontDist <= turnDistance:
                    motor.change_duty_cycle(motorDuty)
                    motor.change_duty_cycle(50)
                    time.sleep(0.01)
                    motor.change_duty_cycle(motorDuty)
                    print("stopping")
                    
                    if rightDist <= 5:
                        backUp(8)
                    elif leftDist <= 5:
                        backUp(-8)

                    elif rightDist < leftDist:
                        # moveLeft(1000)
                        t3 = Thread(target=moveLeft, args=(1000,))
                        t3.run()
                    elif leftDist < rightDist:
                        # moveRight(1000)
                        t4 = Thread(target=moveRight, args=(1000,))
                        t4.run()
                    turnIncrement = 12

                elif frontDist >= turnDistance+1:
                    print("time to GO STRAIGHT")

                    if leftDist <= 40:
                        t1 = Thread(target=moveRight, args=(leftDist,))
                        t1.run()
                    elif rightDist <= 44:
                        t2 = Thread(target=moveLeft, args=(rightDist,))
                        t2.run()

                    duty=getkey
                    if (duty =="e"):
                        servo.change_duty_cycle(servoDuty)
                        motor.change_duty_cycle(motorDuty)
                        time.sleep(.01)
                        quit()
                else:
                    print("not enough")
                
            rightDistPrev = rightDist
            leftDistPrev = leftDist
            time.sleep(0.07)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        servo.change_duty_cycle(servoDuty)
        motor.change_duty_cycle(motorDuty)
        #GPIO.cleanup()   
