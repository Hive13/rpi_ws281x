#!/usr/bin/env python

from libws2811_wrap import *
import signal, time, sys

WIDTH=8
HEIGHT=8

ledstring = WS2811_T()
ledstring.count = WIDTH * HEIGHT
ledstring.freq = 800000
ledstring.dmanum = 5
ledstring.gpionum = 18
ledstring.invert = 0

matrix = ((WS2811_LED_T * WIDTH) * HEIGHT)()

def matrix_render():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            ledstring.leds[(y * WIDTH) + x] = matrix[x][y]

def matrix_raise():
    for y in range(HEIGHT - 1):
        for x in range(WIDTH):
            matrix[x][y] = matrix[x][y + 1]

dotspos = [0, 1, 2, 3, 4, 5, 6, 7]
dotcolors = (
    0x200000,  # red
    0x201000,  # orange
    0x202000,  # yellow
    0x002000,  # green
    0x002020,  # lightblue
    0x000020,  # blue
    0x100010,  # purple
    0x200010,  # pink
)

def matrix_bottom():
    for i in range(len(dotspos)):
        dotspos[i] += 1
        if (dotspos[i] > (WIDTH - 1)):
            dotspos[i] = 0
        matrix[dotspos[i]][HEIGHT - 1] = dotcolors[i]

def ctrl_c_handler(signum, frame):
    print("Received signal %d" % (signum,))
    ws2811_fini(ledstring)

def setup_handlers():
    signal.signal(signal.SIGINT, ctrl_c_handler)
    #signal.signal(signal.SIGKILL, ctrl_c_handler)

def main():
    ret = 0
    setup_handlers()
    if (ws2811_init(ledstring)):
        return -1
    
    while True:
        matrix_raise()
        matrix_bottom()
        matrix_render()
        if (ws2811_render(ledstring)):
            ret = -1
            break
        time.sleep(1 / 15.0)
        print(".")
    return ret

sys.exit(main())
