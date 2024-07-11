from opensourceleg.hardware.sensors import StrainAmp
from opensourceleg.tools.utilities import SoftRealtimeLoop

amp = StrainAmp(bus=1, I2C_addr=0x66)
loop = SoftRealtimeLoop(dt=1/100, report=True)

for t in loop:
    amp.update()
    print(amp.data)
    