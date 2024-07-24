"""
This script makes the knee and ankle follow the standard gait cycle defined by Winter Biomechanics.

Grace Cordle
FAMU-FSU College of Engineering
"""
import numpy as np
import matplotlib.pyplot as plt
from opensourceleg.osl import OpenSourceLeg
from opensourceleg.tools import units

osl = OpenSourceLeg(frequency=200)
osl.add_joint("knee", gear_ratio=9 * 83 / 18)
osl.add_joint("ankle", gear_ratio=9 * 83 / 18)

ref_pos_ankle_deg = np.array([-0.4, -2.5, -4.7, -6.5, -7.6, -7.8, -7.2, -6, -4.6, -3.1, -1.8, -0.6, 0.4, 1.2, 2.1, 2.8, 3.4, 3.9, 4.2,
                  4.6, 4.9, 5.3, 5.9, 6.4, 6.7, 6.9, 6.9, 6.9, 6.8, 6.8, 6.8, 6.5, 5.9, 4.8, 3.2, 1.2, -1.4, -4.4, -8, -11.8,
                  -15.4, -18.3, -20.1, -20.5, -19.8, -18.2, -16.2, -14, -11.8, -9.9, -8.1, -6.5, -5.2, -4.1, -3.2, -2.5, -2,
                  -1.6, -1.3, -1.1, -0.8, -0.4, 0.1, 0.7, 1.3, 1.7, 1.7, 1.2, 0])
ref_pos_ankle = ref_pos_ankle_deg * np.pi / 180
ref_pos_knee_deg = np.array([0.2, 1.1, 3, 5.1, 7.4, 9.8, 12.1, 14, 15.4, 16.2, 16.3, 15.9, 15.2, 14.2, 13.2, 12.3, 11.4, 10.7, 10.1, 
                    9.4, 8.8, 8.2, 7.6, 7, 6.4, 5.9, 5.4, 5.2, 5.1, 5.5, 6.2, 7.3, 8.9, 10.9, 13.3, 16.2, 19.6, 23.5, 27.8,
                    32.4, 37.4, 42.5, 47.6, 52.4, 56.7, 60.4, 63.4, 65.4, 66.5, 66.6, 65.7, 63.9, 61.3, 58, 54.2, 49.9, 45.2,
                    40, 34.5, 28.6, 22.6, 16.5, 10.9, 5.8, 2.8, 1.2, 0.6, 0.2, 0.6])
ref_pos_knee = ref_pos_knee_deg * np.pi / 180
ref_time = np.linspace(0, 1.02, 69)

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
    osl.ankle.set_output_position(np.deg2rad(0))
    osl.update()

    # Set position gains for the joints
    osl.knee.set_position_gains(kp=100, ki=1, kd=0)
    osl.ankle.set_position_gains(kp=150, ki=1, kd=0)
    input("Homing complete: Press enter to continue")

    # Initialize variables to track the last update time and the current index
    last_update_time = 0
    index = 0

    for t in osl.clock:
        osl.update()

        if t - last_update_time >= 0.015:
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
