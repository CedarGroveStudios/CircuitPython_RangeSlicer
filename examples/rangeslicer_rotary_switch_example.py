# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`rangeslicer_rotary_switch_example`
================================================================================
rangeslicer_rotary_switch_example.py 2022-08-16 v3.01 02:38PM

Reads one potentiometer input and produces an indexed output,
simulating a 5-position rotary selection switch.

* Author(s): JG for Cedar Grove Maker Studios

Implementation Notes
--------------------
** Software and Dependencies: **
  * Adafruit CircuitPython firmware for the supported boards:
    https://github.com/adafruit/circuitpython/releases
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/CedarGroveStudios/CircuitPython/RangeSlicer.git"


import time
import board
import cedargrove_range_slicer as rs
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

print("Rotary Switch: Range_Slicer example 02")

"""Establish a range_slicer instance for the analog potentiometer input.
Input range is adjusted for unique potentiometer inaccuracies and noise.
Slice size divides the output into 5 slices (switch positions 0 through 4).
Hysteresis factor is 25% of a slice (adjust this for switch feel)."""

pot = rs.Slicer(400, 65000, 0, 4, 1, 0.25, True, debug=False)

# set up analog potentiometer input pin
pot_input = AnalogIn(board.A0)

# set up led digital output
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
led.value = False  # turn off led

# list of switch positions
position = ["Off", "Sine Wave", "Square Wave", "Triangle Wave", "Sawtooth Wave"]

old_index = -1  # initialize the switch index value

while True:
    new_index = int(
        pot.range_slicer(pot_input.value)
    )  # read pot and determine the index value

    if new_index != old_index:  # compare old and new; did the index value change?
        print(new_index, position[new_index])  # print switch selection name
        old_index = new_index

        led.value = True  # flash the LED when index value changes
        time.sleep(0.1)
        led.value = False

    time.sleep(0.1)  # pause for 0.1 second
