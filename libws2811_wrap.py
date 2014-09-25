#!/usr/bin/env python

import ctypes

# ===========================================================================
# Library import
# ===========================================================================
_lib = ctypes.CDLL("./libws2811.so")

# ===========================================================================
# Type definitions
# ===========================================================================
WS2811_LED_T = ctypes.c_uint32
WS2811_DEVICE_T = ctypes.c_void_p

class WS2811_T(ctypes.Structure):
    _fields_ = [("device", WS2811_DEVICE_T),
                ("freq", ctypes.c_uint32),
                ("dmanum", ctypes.c_int),
                ("gpionum", ctypes.c_int),
                ("invert", ctypes.c_int),
                ("count", ctypes.c_int),
                ("leds", ctypes.POINTER(WS2811_LED_T)),]

# ===========================================================================
# Exported functions
# ===========================================================================
ws2811_init = _lib.ws2811_init
ws2811_init.argtypes = [ctypes.POINTER(WS2811_T)]
ws2811_init.restype = ctypes.c_int

ws2811_fini = _lib.ws2811_fini
ws2811_fini.argtypes = [ctypes.POINTER(WS2811_T)]
ws2811_fini.restype = None

ws2811_render = _lib.ws2811_render
ws2811_render.argtypes = [ctypes.POINTER(WS2811_T)]
ws2811_render.restype = ctypes.c_int

ws2811_wait = _lib.ws2811_wait
ws2811_wait.argtypes = [ctypes.POINTER(WS2811_T)]
ws2811_wait.restype = ctypes.c_int
