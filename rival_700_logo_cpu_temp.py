import rivalcfg
import psutil
import time
import sys

# Set config for Rival 700
VENDOR_ID = 0x1038
PRODUCT_ID = 0x1700
mouse = rivalcfg.get_mouse(VENDOR_ID, PRODUCT_ID)

update_speed = 200
lastcolor = "#000000"

mincpu_temp = 22
maxcpu_temp = 65

def colortorgb(color):
    return "#"+color[2:]+"0000"


def valuetorange(value, oldmax, oldmin, newmax, newmin):
    oldrange = (oldmax - oldmin)
    newRange = (newmax - newmin)
    return int((((value - oldmin) * newRange) / oldrange) + newmin)


while True:
    temps = psutil.sensors_temperatures()
    if not temps:
        sys.exit("can't read any temperature")
    for name, entries in temps.items():
        for entry in entries:
            if entry.label == "Core 0":
                update_speed = valuetorange(int(entry.current), maxcpu_temp, mincpu_temp, 40, 300)
                cpu_temp = valuetorange(int(entry.current), maxcpu_temp, mincpu_temp, 255, 0)
                temp_str = str(hex(cpu_temp))
                endcolor = colortorgb(temp_str)
                print(entry.current, temp_str[2:], update_speed)
                startcolor = lastcolor
                mouse.set_logo_colorshift([startcolor, endcolor],["1","50"],str(update_speed))
    time.sleep(update_speed/100)