"""
A basic motion script that moves the osl knee through their range of motion.
This script can be helpful when getting started to make sure the OSL is functional.

Kevin Best
Neurobionics Lab
Robotics Department
University of Michigan
October 26, 2023
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from opensourceleg.osl import OpenSourceLeg
from opensourceleg.tools import units

osl = OpenSourceLeg(frequency=200)
osl.add_joint("ankle", gear_ratio=9 * 83 / 18)


def make_periodic_traj_func(period, minimum, maximum):
    amplitude = (maximum - minimum) / 2
    mean = amplitude + minimum
    return lambda t: amplitude * np.cos(t * 2 * np.pi / period) + mean


ankle_traj = make_periodic_traj_func(10, -20, 20)

time_list = []
desired_ankle_list = []
actual_ankle_list = []
error_ankle_list = []

with osl:
    osl.home()
    osl.ankle.set_mode(osl.ankle.control_modes.position)
    osl.ankle.set_position_gains(kp=15)
    osl.ankle.set_output_position(np.deg2rad(20))
    osl.update()
    osl.ankle.set_position_gains(kp=100)
    input("Homing complete: Press enter to continue")

    for t in osl.clock:
        osl.update()
        ankle_setpoint = units.convert_to_default(ankle_traj(t), units.position.deg)
        osl.ankle.set_output_position(ankle_setpoint)

        time_list.append(t)
        desired_ankle_list.append(ankle_setpoint)
        actual_ankle_list.append(osl.ankle.output_position)
        error_ankle_list.append(ankle_setpoint - osl.ankle.output_position)

        print(
            "Ankle Desired {:+.2f} rad, Ankle Actual {:+.2f} rad".format(
                ankle_setpoint,
                osl.ankle.output_position,
            ),
            end="\r",
        )

print("\n")

# Plot the results
plt.figure(figsize=(10, 8))

# Plot ankle positions
plt.subplot(2, 1, 1)
plt.plot(time_list, desired_ankle_list, label='Desired Ankle Position')
plt.plot(time_list, actual_ankle_list, label='Actual Ankle Position')
plt.plot(time_list, error_ankle_list, label='Ankle Error')
plt.xlabel('Time (s)')
plt.ylabel('Ankle Position (rad)')
plt.legend()
plt.title('Ankle Position vs. Time')

plt.tight_layout()
plt.savefig('/home/pi/ankle_model_errors.png')
plt.close()
