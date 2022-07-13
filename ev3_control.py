#!/usr/bin/env python3
import logging
from time import sleep

from ev3dev2.motor import MoveTank
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")
logger = logging.getLogger('EV3 CONTROLLER')
logger.setLevel(logging.DEBUG)

# Linker Motor --> outB
# Rechte Motor --> outA
movetank = MoveTank(OUTPUT_B, OUTPUT_A)

# Linker Sensor --> in2
lightsensor2 = ColorSensor(INPUT_2)
# Rechter Sensor --> in1
lightsensor1 = ColorSensor(INPUT_1)
# Ultraschallsensor --> in3
ultrasonicSensor = UltrasonicSensor(INPUT_3)

lightsensor1.MODE_COL_AMBIENT
lightsensor2.MODE_COL_AMBIENT

ultrasonicSensor.MODE_US_SI_CM

def followTheLight():
    # Get Light Intensity
    valueRight = lightsensor1.ambient_light_intensity
    valueLeft = lightsensor2.ambient_light_intensity

    # Calc Difference
    valueDiff = valueRight - valueLeft

    # Distanz zu Objekten im Raum
    distance = ultrasonicSensor.distance_centimeters

    # TODO Add Vorwärtsbewegung bei Drehung

    # Wenn mehr Licht auf der rechten Seite ist, dreht sich der EV3 nach rechts
    if valueDiff > 6:
        movetank.on(35, -35)
        logger.debug("Turning Right")
        sleep(0.5)

    # Wenn mehr Licht auf der linken Seite ist, dreht sich der EV3 nach links
    if valueDiff < -6:
        movetank.on(-35, 35)
        logger.debug("Turning Left")
        sleep(0.5)

    # Wenn Licht vor EV3, dann fahre vorwärts
    if -5 <= valueDiff <= 5 and distance > 10.0:
        movetank.on(70, 70)
        logger.debug("Moving to Light")
        sleep(0.5)

    # Motoren werden ausgeschaltet
    movetank.off()

    logger.debug('Links: %d', valueRight)
    logger.debug('Rechts: %d', valueLeft)
    logger.debug('Value Diff: %d', valueDiff)


if __name__ == '__main__':
    while True:
        followTheLight()
