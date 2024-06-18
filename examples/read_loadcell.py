import numpy as np
import time
import matplotlib.pyplot as plt

from opensourceleg.osl import OpenSourceLeg
from opensourceleg.hardware.sensors import Loadcell, StrainAmp

LOADCELL_MATRIX = np.array(
    [
        (-35.44949, -1408.27600, 5.28557, -14.07667, 19.88193, 1413.95837),
        (-3.48398, 821.60516, -51.38681, 1630.13098, 42.46563, 823.29095),
        (-817.61768, -2.21026, -840.11005, -8.60509, -831.32318, -3.53086),
        (17.09737, 0.17497, 0.22292, -0.58087, -16.93312, -0.05286),
        (-9.28386, -0.30000, 20.22296, -0.07903, -9.65388, 0.34513),
        (-0.61599, -21.24456, -0.50275, 21.10707, -0.80625, -23.02333),
    ]
)

osl = OpenSourceLeg(frequency=200, file_name="getting_started.log")
osl.add_loadcell(dephy_mode=False, offline_mode=False, loadcell_matrix=LOADCELL_MATRIX)

with osl:

    # Calibrate the load cell
    osl.loadcell.calibrate()
    print("Load cell zero:", osl.loadcell._loadcell_zero)
    loadcell_zero = osl.loadcell._loadcell_zero

    # Lists to store time and force data
    timestamps = []
    fx_values = []
    fy_values = []
    fz_values = []
    data0 = []
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    data7 = []
    data8 = []
    data9 = []
    gen0 = []
    gen1 = []
    gen2 = []
    gen3 = []
    gen4 = []
    gen5 = []

    # Define a function to read and print load cell data
    # def read_loadcell_data(duration: int = 10, read_interval: float = 0.5, loadcell_zero: np = np.zeros(shape=(1, 6), dtype=np.double)):
    def read_loadcell_data(duration: int = 10, loadcell_zero: np = np.zeros(shape=(1, 6), dtype=np.double)):
        start_time = time.time()
        while time.time() - start_time < duration:
            current_time = time.time() - start_time
            osl.loadcell.update(loadcell_zero)
            if osl.has_loadcell:
                fx = osl.loadcell.fx
                fy = osl.loadcell.fy
                fz = osl.loadcell.fz
                timestamps.append(current_time)
                fx_values.append(fx)
                fy_values.append(fy)
                fz_values.append(fz)
                data0.append(osl.loadcell._lc.data[0])
                data1.append(osl.loadcell._lc.data[1])
                data2.append(osl.loadcell._lc.data[2])
                data3.append(osl.loadcell._lc.data[3])
                data4.append(osl.loadcell._lc.data[4])
                data5.append(osl.loadcell._lc.data[5])
                data6.append(osl.loadcell._lc.data[6])
                data7.append(osl.loadcell._lc.data[7])
                data8.append(osl.loadcell._lc.data[8])
                data9.append(osl.loadcell._lc.data[9])
                gen0.append(osl.loadcell._lc.genvars[0])
                gen1.append(osl.loadcell._lc.genvars[1])
                gen2.append(osl.loadcell._lc.genvars[2])
                gen3.append(osl.loadcell._lc.genvars[3])
                gen4.append(osl.loadcell._lc.genvars[4])
                gen5.append(osl.loadcell._lc.genvars[5])
                # print(osl.loadcell._lc.data)
                # print(osl.loadcell._lc.genvars)
                # print(f"Time: {current_time:.2f}s, fx: {fx}, fy: {fy}, fz: {fz}")
            # time.sleep(read_interval)
            time.sleep(0.5)

    # Read and print load cell data for 10 seconds with a 1-second interval
    # read_loadcell_data(duration=10, read_interval=0.5, loadcell_zero = osl.loadcell._loadcell_zero)
    read_loadcell_data(duration=10, loadcell_zero = osl.loadcell._loadcell_zero)

    # Plot the results
    plt.figure(figsize=(10, 6))
    
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, fx_values, label='fx', color='r')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Load Cell Force - fx')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(timestamps, fy_values, label='fy', color='g')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Load Cell Force - fy')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(timestamps, fz_values, label='fz', color='b')
    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')
    plt.title('Load Cell Force - fz')
    plt.legend()

    plt.tight_layout()
    plt.savefig('/home/pi/loadcell_forcedata_plot.png')
    plt.close()

    # Plot the results
    plt.figure(figsize=(12, 8))

    # Plot Load Cell Data
    plt.subplot(2, 1, 1)
    plt.plot(timestamps, data0, label='0')
    plt.plot(timestamps, data1, label='1')
    plt.plot(timestamps, data2, label='2')
    plt.plot(timestamps, data3, label='3')
    plt.plot(timestamps, data4, label='4')
    plt.plot(timestamps, data5, label='5')
    plt.plot(timestamps, data6, label='6')
    plt.plot(timestamps, data7, label='7')
    plt.plot(timestamps, data8, label='8')
    plt.plot(timestamps, data9, label='9')
    plt.xlabel('Time (s)')
    plt.ylabel('Load Cell Data')
    plt.title('Load Cell Data over Time')
    plt.legend()

    # Plot General Variables
    plt.subplot(2, 1, 2)
    plt.plot(timestamps, gen0, label='0')
    plt.plot(timestamps, gen1, label='1')
    plt.plot(timestamps, gen2, label='2')
    plt.plot(timestamps, gen3, label='3')
    plt.plot(timestamps, gen4, label='4')
    plt.plot(timestamps, gen5, label='5')
    plt.xlabel('Time (s)')
    plt.ylabel('Generated Variables')
    plt.title('Generated Variables over Time')
    plt.legend()

    plt.tight_layout()
    plt.savefig('/home/pi/loadcell_rawdata_plot.png')
    plt.close()

