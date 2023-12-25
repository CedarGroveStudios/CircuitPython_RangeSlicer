# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`rangeslicer_example_01`
================================================================================
rangeslicer_example_01.py 2022-08-16 v3.01 02:38PM

Reads two potentiometer inputs and produces -1.0 to +1.0 normalized outputs,
one with an inverted output range.

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
import cedargrove_rangeslicer as rs
from analogio import AnalogIn

print("Two Normalized Outputs: RangeSlicer example 01")

"""Establish range_slicer instances, one for each analog potentiometer
input. Input ranges are adjusted for unique potentiometer inaccuracies and
noise. Slice size divides the output into 10 slices. Hysteresis factor is
25% of a slice."""

ctrl_0 = rs.Slicer(200, 65335, -1.0, +1.0, 0.2, 0.25)
ctrl_1 = rs.Slicer(375, 65520, +1.0, -1.0, 0.2, 0.25)

# establish analog inputs
pot_0 = AnalogIn(board.A0)
pot_1 = AnalogIn(board.A1)

while True:  # read potentiometer values
    control_0 = pot_0.value
    control_1 = pot_1.value

    # calculate output values and print (or plot in Mu)
    out_0 = ctrl_0.range_slicer(control_0)
    out_1 = ctrl_1.range_slicer(control_1)
    print((control_0 / 65535, control_1 / 65535, out_0, out_1))

    time.sleep(0.1)  # pause for 0.1 second
