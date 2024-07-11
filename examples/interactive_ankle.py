"""
This script moves the ankle forwards and backwards depending on the user's input

Grace Cordle
FAMU-FSU College of Engineering
"""

import numpy as np

from opensourceleg.osl import OpenSourceLeg
from opensourceleg.tools import units

osl = OpenSourceLeg(frequency=200)
osl.add_joint("ankle", gear_ratio=9 * 83 / 18)

while True:
    with osl:
        osl.home()
        input("Homing complete: Press enter to continue")
        osl.ankle.set_mode(osl.ankle.control_modes.position)
        osl.ankle.set_position_gains(kp=5)

        current_position = osl.ankle.output_position
        increment = units.convert_to_default(5, units.position.deg)

        response = input("Press f to move the ankle forward, press b to move the ankle backward, press c to center the ankle, and press any other key to stop: ")

        if response == "f":
            new_position = current_position + increment
            osl.ankle.set_output_position(new_position)
            current_position = osl.ankle.output_position
            osl.update()
        elif response == "b":
            new_position = current_position - increment
            osl.ankle.set_output_position(new_position)
            current_position = osl.ankle.output_position
            osl.update()
        elif response == "c":
            osl.home()
            current_position = osl.ankle.output_position
        else:
            break
