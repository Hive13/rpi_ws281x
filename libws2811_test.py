#!/usr/bin/env python

from ws2811 import *
import signal, time, sys
import random

WIDTH=16
HEIGHT=32

ledstring = WS2811_T()
ledstring.count = WIDTH * HEIGHT
ledstring.freq = 800000
ledstring.dmanum = 5
ledstring.gpionum = 18
ledstring.invert = 0

matrix = ((WS2811_LED_T * HEIGHT) * WIDTH)()

def matrix_render():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            ledstring.leds[(y * WIDTH) + x] = matrix[x][y]

def matrix_raise():
    for y in range(HEIGHT - 1):
        for x in range(WIDTH):
            matrix[x][y] = matrix[x][y + 1]

def encodeColor(r = 1.0, g = None, b = None):
    g = r if g is None else g
    b = r if b is None else b
    shiftAndTruncate = lambda val, sh: (int(val * 255) & 0xFF) << sh
    r_bits = shiftAndTruncate(r, 16)
    g_bits = shiftAndTruncate(g, 8)
    b_bits = shiftAndTruncate(b, 0)
    return r_bits | g_bits | b_bits

dotcolors = (
    (0.25, 0, 0),
    (0.25, 0.125, 0),
    (0.25, 0.25, 0),
    (0, 0.25, 0),
    (0, 0.25, 0.25),
    (0, 0, 0.25),
    (0.125, 0, 0.125),
    (0.25, 0, 0.125),
    (0.25, 0.25, 0.25),
    (0, 0, 0),
)
dotspos = list(range(len(dotcolors)))
#dotspos = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def matrix_bottom(rf = 1.0, gf = 1.0, bf = 1.0):
    for i in range(len(dotspos)):
        dotspos[i] += 1
        if (dotspos[i] > (WIDTH - 1)):
            dotspos[i] = 0
        r, g, b = dotcolors[i]
        matrix[dotspos[i]][HEIGHT - 1] = encodeColor(r * rf, g * gf, b * bf)

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
    
    rf, gf, bf = 0.0, 0.0, 0.0
    while True:
        rf = (rf + 0.001) % (random.random() * 10)
        gf = (gf + 0.0013) % (random.random() * 12)
        bf = (bf + 0.0009) % (random.random() * 14)
        matrix_raise()
        matrix_bottom(rf, gf, bf)
        matrix_render()
        if (ws2811_render(ledstring)):
            ret = -1
            break
        time.sleep(1 / 120.0)
    return ret

if __name__ == "__main__":
    sys.exit(main())
