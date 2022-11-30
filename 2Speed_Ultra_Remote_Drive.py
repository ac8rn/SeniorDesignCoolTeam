import time
from rpi_hardware_pwm import HardwarePWM
from getkey import getkey, keys
import serial
from speedultasonic import distance
from threading import Thread
from statistics import mean 

import RPi.GPIO as GPIO


if __name__ == '__main__':
    try:
        f = open("GlitchySpeed.txt", "a")
        f.write("Glitchy Speed Run: ")
        f.write("\n")
        servo = HardwarePWM(pwm_channel = 0, hz = 480)
        servoDuty = 76
        servo.start(servoDuty)
        #left max turn 64
        #right max turn 87
        
        motor = HardwarePWM(pwm_channel = 1, hz = 480)
        motorDuty = 0
        motor.start(motorDuty)
        #PWM Range 75-85


        speed = 80
        turn = 0.4 #How long it turn - 0.4 (78)
        straight = 0.1 #How long straight - 0.3 (78)
       
        def moveRight(dist):
            if dist == 1000:
                servo.change_duty_cycle(servoDuty-10)
                motor.change_duty_cycle(speed)
                print("TURN RIGHT")
                time.sleep(turn) 
                servo.change_duty_cycle(servoDuty)
                time.sleep(straight) 
            elif dist <= 10: #6
                backUp(-8)
            elif dist <= 19:
                servo.change_duty_cycle(servoDuty-10) 
                print("move right - A LOT")
                time.sleep(turn)
                servo.change_duty_cycle(servoDuty)
            else:
                servo.change_duty_cycle(servoDuty-7) 
                print("move right - correction")
                time.sleep(straight)
                servo.change_duty_cycle(servoDuty)
        def moveLeft(dist):
            if dist == 1000:
                servo.change_duty_cycle(servoDuty+10)
                motor.change_duty_cycle(speed)
                print("TURN LEFT")
                time.sleep(turn)
                servo.change_duty_cycle(servoDuty)
                motor.change_duty_cycle(speed)
                time.sleep(straight)
            elif dist <= 10: #6
                backUp(8)
            elif dist <= 19:
                servo.change_duty_cycle(servoDuty+8)
                print("move left - A LOT")
                time.sleep(0.2) #special
                servo.change_duty_cycle(servoDuty) 
            else:
                servo.change_duty_cycle(servoDuty+7) #9
                print("move left - correction")
                time.sleep(0.1) #special
                servo.change_duty_cycle(servoDuty)    
        def backUp(dir):
            servo.change_duty_cycle(servoDuty)
            motor.change_duty_cycle(motorDuty)
            motor.change_duty_cycle(50)
            time.sleep(1.2)
            servo.change_duty_cycle(servoDuty+dir)
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

        turnDistance = 24 #22old 
        rightAvg = []
        leftAvg = []
        frontAvg = []
        turnIncrement = 0
        
        backUpFlag = False

        for i in range(4):
            rightDist = (distance(rightTrig, rightEcho))
            frontDist = (distance(frontTrig, frontEcho))
            leftDist = (distance(leftTrig, leftEcho))
            time.sleep(0.05)


        while True:
            servo.change_duty_cycle(servoDuty)
            motor.change_duty_cycle(speed)
            rightDist = (distance(rightTrig, rightEcho))
            print("Right Dist: %0.1f" % rightDist)
            f.write("Right Dist: %0.1f" % rightDist)

            frontDist = (distance(frontTrig, frontEcho))
            print("Front Dist: %0.1f" % frontDist)
            f.write("Front Dist: %0.1f" % frontDist)

            leftDist = (distance(leftTrig, leftEcho))
            print("Left Dist: %0.1f" % leftDist)
            f.write("Left Dist: %0.1f" % leftDist)
            
            f.write("\n")            

            if turnIncrement == False:
                turnIncrement -= 1
                if frontDist <= 15: #Increasing was not so good
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
                    
                    #Backup straight less than 16
                    #Prevents car from backing up more than once
            else:           #6
                if (frontDist <= turnDistance-7) and backUpFlag != True: #frontDist <= turnDistance-6:
                    if rightDist < leftDist:
                        backUp(0)
                    if leftDist < rightDist:
                        backUp(0)
                    print("Extreme backup")
                    backUpFlag = True
                    
                    #handles distances of 22
                elif frontDist <= turnDistance:
                    backUpFlag = False
                    motor.change_duty_cycle(motorDuty)
                    motor.change_duty_cycle(50)
                    time.sleep(0.01)
                    motor.change_duty_cycle(motorDuty)
                    print("stopping")
                    
                    if rightDist <= 7: #no room to right side backup with turn - 5
                        backUp(8)
                    elif leftDist <= 6: # was 7
                        backUp(-8)

                    elif rightDist < leftDist:
                        # moveLeft(1000)  Flag value
                        t3 = Thread(target=moveLeft, args=(1000,))
                        t3.run()
                    elif leftDist < rightDist:
                        # moveRight(1000)  Flag value
                        t4 = Thread(target=moveRight, args=(1000,))
                        t4.run()
                    turnIncrement = 12
                    
                    #handles distances above 23
                elif frontDist >= turnDistance+1:
                    backUpFlag = False
                    print("time to GO STRAIGHT")

                    if leftDist <= 40:  #checking small corrections
                        t1 = Thread(target=moveRight, args=(leftDist,))
                        t1.run()
                    elif rightDist <= 44:
                        t2 = Thread(target=moveLeft, args=(rightDist,))
                        t2.run()
                    
                else:
                    print("not enough")
                
            rightDistPrev = rightDist
            leftDistPrev = leftDist
            time.sleep(0.07)   #how quickly it is trying to refresh sensor DON'T CHANGE!

    except KeyboardInterrupt:   # Reset by pressing CTRL + C
        print("Measurement stopped by User")
        servo.change_duty_cycle(servoDuty)
        motor.change_duty_cycle(motorDuty)
        f.write("\n\n************ End of DATA ************\n\n")
        f.close()
