#!/usr/bin/env python3
# coding=utf-8

import time
import pigpio
# tolle abkürzungen für die gpios:
# http://abyz.me.uk/rpi/pigpio/python.html#callback

gpio = 7  # where the switch is connected



def intCallback(g, level, tick):
    global pressTick
    if level == 0:
        # button press
        pressTick = tick
    elif level == 1:
        # button release
        diff = pigpio.tickDiff(pressTick, tick)
        if diff < 3000:
            # Switch pressed under 3 seconds
            print("Short")
        elif diff >= 3000:
            # Switch pressed over 3 second
            print("Long")



pi = pigpio.pi()
pressTick = pi.get_current_tick()  # initializing var
pi.set_mode(gpio, pigpio.INPUT)
pi.set_pull_up_down(gpio, pigpio.PUD_UP)  # this depends on how the switch is connected
pi.set_glitch_filter(gpio, 300)
#cb = pi.callback(gpio, pigpio.RISING_EDGE, intCallback)
cb = pi.callback(gpio, pigpio.FALLING_EDGE, intCallback)



try:
    while True:
        time.sleep(1)

except (KeyboardInterrupt, SystemExit) as e:
    print("Clean exit")

except Exception as e:
    print("Bad exit")

finally:
    cb.cancel()
    pi.stop()