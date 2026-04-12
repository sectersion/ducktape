from machine import Pin
import neopixel
from pinlayout import RGB_LED
from arm import arm_shorted

np = neopixel.NeoPixel(RGB_LED, 1)

def update_led():
    if arm_shorted():
        np[0] = (50, 0, 0)   # red
    else:
        np[0] = (0, 50, 0)   # green
    np.write()