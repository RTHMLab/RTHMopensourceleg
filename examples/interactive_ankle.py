"""
This script moves the ankle forwards and backwards depending on the user's input

Grace Cordle
FAMU-FSU College of Engineering
"""

import numpy as np
import time

from opensourceleg.osl import OpenSourceLeg
from opensourceleg.tools import units

osl = OpenSourceLeg(frequency=200)
osl.add_joint("ankle", gear_ratio=9 * 83 / 18)

with osl:

    osl.home()
    input("Homing complete: Press enter to continue")
    osl.ankle.set_mode(osl.ankle.control_modes.position)
    osl.ankle.set_position_gains(kp=5)

    current_position = -30 * np.pi / 180
    increment = units.convert_to_default(10, units.position.deg)

    while True:
        response = input("Press f to move the ankle forward, press b to move the ankle backward, press c to center the ankle, and press any other key to stop: ")

        if response == "f":
            new_position = current_position + increment
            osl.ankle.set_output_position(new_position)
            current_position = new_position
            osl.update()
            time.sleep(2)
            osl.update()
            print(osl.ankle.output_position)
        elif response == "b":
            new_position = current_position - increment
            osl.ankle.set_output_position(new_position)
            current_position = new_position
            osl.update()
            time.sleep(2)
            osl.update()
            print(osl.ankle.output_position)
        elif response == "c":
            new_position = 0
            osl.ankle.set_output_position(new_position)
            current_position = new_position
            osl.update()
            time.sleep(2)
            osl.update()
            print(osl.ankle.output_position)
        else:
            break
    
    osl.update()
    current_position_deg = osl.ankle.output_position * 180 / np.pi
    print(osl.ankle.output_position)
    print(current_position_deg)