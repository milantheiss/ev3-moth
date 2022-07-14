#!/usr/bin/env python3
from cmath import log
import logging
import threading
from time import sleep

from ev3dev2.motor import MoveTank
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.button import Button

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")
logger = logging.getLogger('EV3 CONTROLLER')
logger.setLevel(logging.DEBUG)

# Linker Motor --> outB
# Rechte Motor --> outA
movetank = MoveTank(OUTPUT_B, OUTPUT_A)

# Rechter Sensor --> in1
lightsensor1 = ColorSensor(INPUT_1)
# Linker Sensor --> in2
lightsensor2 = ColorSensor(INPUT_2)

# Ultraschallsensor nach vorne --> in3
ultrasonicSensor1= UltrasonicSensor(INPUT_3)
# Ultraschallsensor nach unten --> in4
ultrasonicSensor2 = UltrasonicSensor(INPUT_4)

lightsensor1.MODE_COL_AMBIENT
lightsensor2.MODE_COL_AMBIENT

ultrasonicSensor1.MODE_US_SI_CM
ultrasonicSensor2.MODE_US_SI_CM

button = Button()

# True --> Licht folgen ; False --> Licht meiden
seeklight = True

move_forward = False

def _on_enter(state):
    global move_forward
    if state:
        move_forward = not move_forward
        logger.debug(move_forward)

button.on_enter = _on_enter

def calcDifference():
    # Get Light Intensity
    valueRight = lightsensor1.ambient_light_intensity
    valueLeft = lightsensor2.ambient_light_intensity

    # Calc Difference
    valueDiff = valueRight - valueLeft
    
    # Licht folgen / meiden modus umschalten
    if not seeklight:
        valueDiff = -valueDiff

    """
    logger.debug('Links: %d', valueRight)
    logger.debug('Rechts: %d', valueLeft)
    logger.debug('Value Diff: %d', valueDiff)
    """

    return valueDiff


def followTheLight():
    while True:
        # Wenn mehr Licht auf der rechten Seite ist, dreht sich der EV3 nach rechts
        while calcDifference() > 6:
            movetank.on(35, -35)
            sleep(0.15)

        # Wenn mehr Licht auf der linken Seite ist, dreht sich der EV3 nach links
        while calcDifference() < -6:
            movetank.on(-35, 35)
            sleep(0.15)
      
        # Wenn Licht vor EV3, dann fahre vorwärts
        if -5 <= calcDifference() <= 5 and ultrasonicSensor1.distance_centimeters > 20.0 and move_forward and ultrasonicSensor2.distance_centimeters < 9:
            movetank.on(55, 55)
        else:
           # Motoren werden ausgeschaltet
            movetank.off()

def _button_update(): 
    while True:
        button.process()

if __name__ == '__main__':
    threading.Thread(target=followTheLight).start()
    threading.Thread(target=_button_update, daemon=True).start()
