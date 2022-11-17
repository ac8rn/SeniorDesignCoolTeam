import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Front
frontTrig = 5
frontEcho = 6

# Right
rightTrig = 27
rightEcho = 22

# Left
leftTrig = 23 
leftEcho = 24

GPIO.setup(frontTrig, GPIO.OUT)
GPIO.setup(frontEcho, GPIO.IN)
GPIO.setup(rightTrig, GPIO.OUT)
GPIO.setup(rightEcho, GPIO.IN)
GPIO.setup(leftTrig, GPIO.OUT)
GPIO.setup(leftEcho, GPIO.IN)

sensorDistance = []

def distanceRight():
    trig = rightTrig
    echo = rightEcho

    # set Trigger to HIGH
    GPIO.output(trig, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trig, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def distanceFront():
    trig = frontTrig
    echo = frontEcho

    # set Trigger to HIGH
    GPIO.output(trig, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trig, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def distance(trig,echo):
    #trig = frontTrig
    #echo = frontEcho

    # set Trigger to HIGH
    GPIO.output(trig, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trig, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = ((TimeElapsed * 34300) / 2)/2.54
 
    return distance

if __name__ == '__main__':
    try:

        while True:
            #dist = distanceFront()
            dist = distance(frontTrig,frontEcho)
            print ("Measured FRONT Distance = %.1f in" % dist)
            dist = distance(leftTrig,leftEcho)
            print ("Measured LEFT Distance = %.1f in" % dist)
            dist = distance(rightTrig,rightEcho)
            print ("Measured RIGHT Distance = %.1f in" % dist)
            #sensorDistance.append(dist)
            #print(sensorDistance)
            # if len(sensorDistance) == 5:
            #     temp = 0
            #     for i in sensorDistance:
            #         temp += sensorDistance
            #     temp = temp/5
            #     sensorDistance.clear()
            #     print("Average distance", temp)
            if dist > 30:
                print("Need to move Right")
            #distIn = dist/2.54
            #print ("Measured Distance = %.1f cm" % distIn)
            time.sleep(1.5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()