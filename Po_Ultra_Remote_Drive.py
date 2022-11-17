import time
from datetime import datetime
from rpi_hardware_pwm import HardwarePWM
from getkey import getkey, keys
#import RPi.GPIO as GPIO
import serial
from ultasonic import distance
from threading import Thread
from statistics import mean 
from Pozyx_V3 import * #ReadyToLocalize
import RPi.GPIO as GPIO
from pypozyx import *
from pypozyx.structures.device_information import *
from pypozyx import (POZYX_POS_ALG_UWB_ONLY, POZYX_3D, Coordinates, POZYX_SUCCESS, PozyxConstants, version,
					 DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister, DeviceList, PozyxRegisters)



if __name__ == '__main__':
    try:
        f = open("GlitchyData.txt", "a")
        f.write("Glitchy Data Run: ")
        f.write(str(datetime.now()))
        f.write("\n")
        port = get_first_pozyx_serial_port()
        pozyx = PozyxSerial(port,print_output=True)
        sensors = SensorData()
        raw = RawSensorData()

        serial_port = get_first_pozyx_serial_port()
        if serial_port is None:
            print("No Pozyx connected. Check your USB cable or your driver!")
            quit()

        details = DeviceDetails()
        pozyx.getDeviceDetails(details)
        print(details.id)
        print(pozyx.getNetworkId(details))
        pozyx.printDeviceInfo()

        use_processing = False
        
        remote_id = None#0x7624

        # necessary data for calibration, change the IDs and coordinates yourself according to your measurement
        anchors = [DeviceCoordinates(0x7604, 1, Coordinates(5734,11275,1370)),
                DeviceCoordinates(0x7673, 1, Coordinates(9685,2300,1270)),
                DeviceCoordinates(0x761A, 1, Coordinates(5720,4730,830)),
                DeviceCoordinates(0x7616, 1, Coordinates(2145,2947,1250)),
                DeviceCoordinates(0x614A, 1, Coordinates(10865,12466,1400)),
                DeviceCoordinates(0x6A11, 1, Coordinates(2297,8453,1370))]

        # positioning algorithm to use, other is PozyxConstants.POSITIONING_ALGORITHM_TRACKING
        algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
        # positioning dimension. Others are PozyxConstants.DIMENSION_2D, PozyxConstants.DIMENSION_2_5D
        dimension = PozyxConstants.DIMENSION_2D
        # height of device, required in 2.5D positioning
        height = 1000

        pozyx = PozyxSerial(serial_port)
        r = ReadyToLocalize(pozyx, anchors, algorithm, dimension, height, remote_id)
        r.setup()
        pos = Coordinates()
        mag = Magnetic()
        head = EulerAngles()

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
                servo.change_duty_cycle(servoDuty-7)
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
                servo.change_duty_cycle(servoDuty+7)
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
        backUpFlag = False

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
            # print(r.loop())
            #print(location)
            print(printLoc())

            time.sleep(0.05)


        while True:
            servo.change_duty_cycle(servoDuty)
            motor.change_duty_cycle(speed)
            rightDist = (distance(rightTrig, rightEcho))
            #rightAvg.append(int(rightDist))
            print("Right Dist: %0.1f" % rightDist)
            f.write("Right Dist: %0.1f\n" % rightDist)

            frontDist = (distance(frontTrig, frontEcho))
            #frontAvg.append(int(frontDist))
            print("Front Dist: %0.1f" % frontDist)
            f.write("Front Dist: %0.1f\n" % frontDist)

            leftDist = (distance(leftTrig, leftEcho))
            #leftAvg.append(int(leftDist))
            print("Left Dist: %0.1f" % leftDist)
            f.write("Left Dist: %0.1f\n" % leftDist)

            t5 = Thread(target=r.loop)
            t5.run()

            locationFromPozyx = (printLoc())
            f.write(locationFromPozyx)
            f.write("\n")
            print(locationFromPozyx)

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
                if (frontDist <= turnDistance-6) and backUpFlag != True:
                    if rightDist < leftDist:
                        backUp(0)
                    if leftDist < rightDist:
                        backUp(0)
                    print("Extreme backup")
                    backUpFlag = True

                elif frontDist <= turnDistance:
                    backUpFlag = False
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
                    backUpFlag = False

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
        f.write("\n\n************ End of DATA ************\n\n")
        f.close()

        #GPIO.cleanup()   
