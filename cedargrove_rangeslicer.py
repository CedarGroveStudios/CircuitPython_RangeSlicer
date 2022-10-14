# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_rangeslicer`
================================================================================
cedargrove_rangeslicer.py 2022-09-14 v3.10 07:29PM
RangeSlicer is a CircuitPython class for scaling a range of input values into
indexed/quantized output values. Output slice hysteresis is used to provide
dead-zone squelching.

* Author(s): JG for Cedar Grove Maker Studios

Implementation Notes
--------------------
** Software and Dependencies: **
  * Adafruit CircuitPython firmware for the supported boards:
    https://github.com/adafruit/circuitpython/releases
"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/CircuitPython_RangeSlicer.git"


# pylint: disable=too-many-instance-attributes
class Slicer:
    """The primary RangeSlicer class."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        in_min=0,
        in_max=65535,
        out_min=0,
        out_max=65535,
        out_slice=1.0,
        hyst_factor=0.10,
        out_integer=False,
    ):
        """Instantiate the Slicer class.

        :param union(float, int) in_min: The minimum value of the range input.
          Can be a positive or negative floating point or integer value.
          Defaults to 0.
        :param union(float, int) in_max: The maximum value of the range input.
          Can be a positive or negative floating point or integer value.
          Defaults to 65535.
        :param union(float, int) out_min: The minimum value of the index output.
          Can be a positive or negative floating point or integer value.
          Defaults to 0.
        :param union(float, int) out_max: The maximum value of the index output.
          Can be a positive or negative floating point or integer value.
          Defaults to 65535.
        :param union(float, int) out_slice: The index output slice value. Must be a
          positive floating point or integer value greater than zero. Defaults
          to 1.0.
        :param float hyst_factor: The hysteresis factor as related to the span
          of the range input. For example, a factor of 0.50 is a hysteresis
          setting of 50%. Defaults to 0.10 (10% of the range input span).
        :parm bool out_integer: The index output data type; True to convert
          the index output value to an integer, False for floating point.
          Defaults to False."""

        self._in_min = in_min  # Range input min/max parameters
        self._in_max = in_max
        self._out_min = out_min  # Index output min/max parameters
        self._out_max = out_max
        self._slice = out_slice  # Index output slice size parameter
        self._hyst_factor = hyst_factor  # Hysteresis factor parameter
        self._out_integer = out_integer  # Index output data type parameter

        # Define variables for later us in the class
        self._in_zone = None
        self._index = None
        self._old_idx_mapped = None

        self._update_param()  # Establish the parameters for range_slicer helper

    @property
    def range_min(self):
        """The range input minimum floating or integer value."""
        return self._in_min

    @range_min.setter
    def range_min(self, in_min=0):
        self._in_min = in_min
        self._update_param()  # Update the parameters for range_slicer helper

    @property
    def range_max(self):
        """The range input maximum floating or integer value."""
        return self._in_max

    @range_max.setter
    def range_max(self, in_max=65535):
        self._in_max = in_max
        self._update_param()  # Update the parameters for range_slicer helper

    @property
    def index_min(self):
        """The index output minimum value."""
        return self._out_min

    @index_min.setter
    def index_min(self, out_min=0):
        self._out_min = out_min
        self._update_param()  # Update the parameters for range_slicer helper

    @property
    def index_max(self):
        """The index output maximum value."""
        return self._out_max

    @index_max.setter
    def index_max(self, out_max=65535):
        self._out_max = out_max
        self._update_param()  # Update the parameters for range_slicer helper

    @property
    def index_type(self):
        """The index output value integer data type."""
        return self._out_integer

    @index_type.setter
    def index_type(self, out_integer=False):
        self._out_integer = out_integer
        self._update_param()  # Update the parameters for range_slicer helper

    @property
    def slice(self):
        """The index output slice size value."""
        return self._slice

    @slice.setter
    def slice(self, size=1.0):
        if size <= 0:
            raise RuntimeError("Invalid Slice value; must be greater than zero")
        self._slice = size
        self._update_param()  # Update the parameters for range_slicer helper

    @property
    def hysteresis(self):
        """The hysteresis factor value."""
        return self._hyst_factor

    @hysteresis.setter
    def hysteresis(self, hyst_factor=0.10):
        self._hyst_factor = hyst_factor
        self._update_param()  # Update the parameters for range_slicer helper

    def range_slicer(self, range_in=0):
        """range_slicer() is the primary function of the Slicer class.
        Determines an index (output) value from the range_in input value.
        Returns new index value and a change flag (True/False) if the new index
        changed from the previous index. Index value can be optionally converted
        to integer data type."""

        if self._out_span_dir == 1:
            idx_mapped = self._mapper(range_in) + self._hyst_band
            slice_num = (
                (idx_mapped - self._out_span_min)
                - ((idx_mapped - self._out_span_min) % self._slice)
            ) / self._slice
            slice_thresh = (slice_num * self._slice) + self._out_span_min
        else:
            idx_mapped = self._mapper(range_in) + self._hyst_band
            slice_num = (
                (idx_mapped - self._out_span_max)
                - ((idx_mapped - self._out_span_max) % self._slice)
            ) / self._slice
            slice_thresh = (slice_num * self._slice) + self._out_span_max

        upper_zone_limit = slice_thresh + (2 * self._hyst_band)

        if upper_zone_limit >= idx_mapped >= slice_thresh:
            if self._in_zone != slice_thresh:
                self._in_zone = slice_thresh

                if idx_mapped > self._old_idx_mapped:
                    self._index = slice_thresh - self._slice
                if idx_mapped < self._old_idx_mapped:
                    self._index = slice_thresh
        else:
            self._in_zone = None
            self._index = slice_thresh

        if self._out_span_min <= self._out_span_max:
            self._index = max(min(self._index, self._out_span_max), self._out_span_min)
        else:
            self._index = min(max(self._index, self._out_span_max), self._out_span_min)

        change_flag = bool(self._index != self._old_idx_mapped)
        self._old_idx_mapped = idx_mapped

        if self._out_integer:
            return int(self._index), change_flag
        return self._index, change_flag

    def _mapper(self, map_in):
        """_mapper: Determines the linear output value based on the input value
        using the linear slope-intercept form y = mx + b ."""

        if (self._in_min == self._in_max) or (self._out_span_min == self._out_span_max):
            return self._out_span_min
        mapped = (
            ((self._out_span_max - self._out_span_min) / (self._in_max - self._in_min))
            * (map_in - self._in_min)
        ) + self._out_span_min
        if self._out_span_min <= self._out_span_max:
            return max(min(mapped, self._out_span_max), self._out_span_min)
        return min(max(mapped, self._out_span_max), self._out_span_min)

    def _update_param(self):
        """Recalculate spans and hysteresis value when parameters change."""

        # Update output span parameters
        if self._out_min > self._out_max:
            self._out_span_min = self._out_min + self._slice
            self._out_span_max = self._out_max
        else:
            self._out_span_min = self._out_min
            self._out_span_max = self._out_max + self._slice
        self._out_span = self._out_span_max - self._out_span_min

        if self._out_span >= 0:
            self._out_span_dir = 1
        else:
            self._out_span_dir = -1

        # Update slice size parameter
        if self._slice <= 0:
            raise RuntimeError("Invalid Slice value; must be greater than zero")

        # Update hysteresis band size; reset in-zone state
        self._hyst_band = self._hyst_factor * self._slice
        self._in_zone = None

        # Update index parameters
        self._index = 0
        self._old_idx_mapped = 0
