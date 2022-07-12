#!/usr/bin/env python3
import logging
import threading
from time import sleep

from ev3dev2.motor import Motor, MoveJoystick, MoveTank
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")
logger = logging.getLogger('EV3 CONTROLLER')
logger.setLevel(logging.DEBUG)

#Linker Motor --> outB
motorB = Motor(OUTPUT_B)
#Rechte Motor --> outA
motorA = Motor(OUTPUT_A)

motors = MoveJoystick(OUTPUT_B, OUTPUT_A)
movetank = MoveTank(OUTPUT_B, OUTPUT_A)

#Linker Sensor --> in2
lightsensor2 = ColorSensor(INPUT_2)
#Rechter Sensor --> in1
lightsensor1 = ColorSensor(INPUT_1)

lightsensor1.MODE_COL_AMBIENT
lightsensor2.MODE_COL_AMBIENT 

def followTheLight():
    #Get Light Intensity
    valueRight = lightsensor1.ambient_light_intensity
    valueLeft = lightsensor2.ambient_light_intensity

    #Calc Difference
    valueDiff = valueRight - valueLeft

    #Wenn mehr Licht auf der rechten Seite ist, dreht sich der EV3 nach rechts
    if valueDiff > 6:
        movetank.on(35, -35)
        logger.debug("Turning Right")
        sleep(0.5)

    #Wenn mehr Licht auf der linken Seite ist, dreht sich der EV3 nach links
    if valueDiff < -6:
        movetank.on(-35, 35)
        logger.debug("Turning Left")
        sleep(0.5)

    #Motoren werden ausgeschaltet
    movetank.off()
    
    logger.debug('Links: %d', valueRight)
    logger.debug('Rechts: %d', valueLeft)
    logger.debug('Value Diff: %d', valueDiff)


if __name__ == '__main__':
    while True:
        followTheLight()

    # Change checking for inputs to false to stop handleing --> bei Command
