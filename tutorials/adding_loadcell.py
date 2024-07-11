import numpy as np

from opensourceleg.osl import OpenSourceLeg

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
osl.add_joint(name="knee", gear_ratio=41.99, has_loadcell=False)
osl.add_joint(name="ankle", gear_ratio=41.99, has_loadcell=False)

osl.add_loadcell(dephy_mode=False, loadcell_matrix=LOADCELL_MATRIX)
