"""
This script makes the knee and ankle mimic sitting and standing

Grace Cordle
FAMU-FSU College of Engineering
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from opensourceleg.osl import OpenSourceLeg
from opensourceleg.tools import units

osl = OpenSourceLeg(frequency=200)
osl.add_joint("knee", gear_ratio=9 * 83 / 18)
osl.add_joint("ankle", gear_ratio=9 * 83 / 18)

# Read Excel File
ss_data = pd.read_excel('/home/pi/SitStandOSL.xlsx')

# Knee Positions
ref_pos_knee_deg = ss_data['Right Knee Angle']
ref_pos_knee = ref_pos_knee_deg * np.pi / 180

# Ankle Positions
ref_pos_ankle_deg = ss_data['Right Ankle Angle']
ref_pos_ankle = ref_pos_ankle_deg * np.pi / 180

# Initialize lists to store time, desired positions, actual positions, and errors
time_list = []
desired_ankle_list = []
actual_ankle_list = []
error_ankle_list = []
desired_knee_list = []
actual_knee_list = []
error_knee_list = []

with osl:
    # Home the joints
    osl.home()
    osl.ankle.set_mode(osl.ankle.control_modes.position)
    osl.knee.set_mode(osl.knee.control_modes.position)
    osl.ankle.set_position_gains(kp=15)
    osl.ankle.set_output_position(np.deg2rad(5))
    osl.knee.set_position_gains(kp=15)
    osl.knee.set_output_position(np.deg2rad(10))
    osl.update()

    # Set position gains for the joints
    osl.knee.set_position_gains(kp=20, ki=0, kd=0)
    osl.ankle.set_position_gains(kp=20, ki=0, kd=0)
    input("Homing complete: Press enter to continue")

    # Initialize variables to track the last update time and the current index
    last_update_time = 0
    index = 0

    for t in osl.clock:
        osl.update()

        if t - last_update_time >= 0.005:
            # Update the joint positions based on current index
            desired_ankle = ref_pos_ankle[index]
            desired_knee = ref_pos_knee[index]
            osl.ankle.set_output_position(desired_ankle)
            osl.knee.set_output_position(desired_knee)
            osl.update()

            # Record time, desired positions, actual positions, and errors
            time_list.append(t)
            desired_ankle_list.append(np.rad2deg(desired_ankle))
            actual_ankle_list.append(np.rad2deg(osl.ankle.output_position))
            error_ankle_list.append(np.rad2deg(desired_ankle) - np.rad2deg(osl.ankle.output_position))
            desired_knee_list.append(np.rad2deg(desired_knee))
            actual_knee_list.append(np.rad2deg(osl.knee.output_position))
            error_knee_list.append(np.rad2deg(desired_knee) - np.rad2deg(osl.knee.output_position))
            
            # Print the current time and joint positions
            print(
                "Time: {:+.3f}, Ankle Desired: {:+.3f} rad, Ankle Actual: {:+.3f} rad, Knee Desired: {:+.3f} rad, Knee Actual: {:+.3f} rad".format(
                t,
                desired_ankle,
                osl.ankle.output_position,
                desired_knee,
                osl.knee.output_position)
                )
            
            index =(index + 1) % len(ref_pos_ankle)
            last_update_time = t
        

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

# Plot knee positions
plt.subplot(2, 1, 2)
plt.plot(time_list, desired_knee_list, label='Desired Knee Position')
plt.plot(time_list, actual_knee_list, label='Actual Knee Position')
plt.plot(time_list, error_knee_list, label='Knee Error')
plt.xlabel('Time (s)')
plt.ylabel('Knee Position (rad)')
plt.legend()
plt.title('Knee Position vs. Time')

plt.tight_layout()
plt.savefig('/home/pi/gait_model_errors.png')
plt.close()
