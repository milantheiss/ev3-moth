#!/usr/bin/env python3
import logging
import threading
from time import sleep

from ev3dev2.motor import Motor, MoveJoystick, MoveTank
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")
logger = logging.getLogger('EV3 CONTROLLER')
logger.setLevel(logging.DEBUG)

#motors = MoveJoystick("outD", "outA")
#movetank = MoveTank("outD", "outA")

#motorD = Motor("outD")
#motorA = Motor("outA")

lightsensor1 = ColorSensor(INPUT_1)
lightsensor2 = ColorSensor(INPUT_2)

lightsensor1.MODE_COL_AMBIENT
lightsensor1.MODE_COL_AMBIENT 

def followTheLight():
    value1 = lightsensor1.ambient_light_intensity
    value2 = lightsensor2.ambient_light_intensity

    logger.info('Links: {}'.format(value1))
    logger.info('Rechts: {}'.format(value2))


if __name__ == '__main__':
    while True:
        followTheLight()
        sleep(1)

    # Change checking for inputs to false to stop handleing --> bei Command
