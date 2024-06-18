import numpy as np
import time

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
    #osl.calibrate_loadcell()
    osl.loadcell.initialize()
    print(osl.loadcell._loadcell_zero)
    loadcell_zero = osl.loadcell._loadcell_zero

    # Define a function to read and print load cell data
    def read_loadcell_data(duration: int = 10, read_interval: float = 1.0, loadcell_zero: np = np.zeros(shape=(1, 6), dtype=np.double)):
        start_time = time.time()
        while time.time() - start_time < duration:
            osl.loadcell.update(loadcell_zero)
            if osl.has_loadcell:
                fx = osl.loadcell.fx
                fy = osl.loadcell.fy
                fz = osl.loadcell.fz
<<<<<<< HEAD
                # print(f"fx: {fx}, fy: {fy}, fz: {fz}")
                print(osl.loadcell._lc.data)
=======
                #print(f"fx: {fx}, fy: {fy}, fz: {fz}")
>>>>>>> cb40a1c75c6273b6cd036cbf3847dcf0f72e73f6
                print(osl.loadcell._lc.genvars)
            time.sleep(read_interval)

    # Read and print load cell data for 10 seconds with a 1-second interval
    read_loadcell_data(duration=10, read_interval=1.0, loadcell_zero = osl.loadcell._loadcell_zero)
<<<<<<< HEAD

    print(f"Failed Reads: {osl.loadcell._lc.failed_reads}")

=======
>>>>>>> cb40a1c75c6273b6cd036cbf3847dcf0f72e73f6

