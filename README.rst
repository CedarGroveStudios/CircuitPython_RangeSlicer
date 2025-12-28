Introduction
============




.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_RangeSlicer/workflows/Build%20CI/badge.svg
    :target: https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_RangeSlicer/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

RangeSlicer is a general-purpose CircuitPython analog value converter that linearly scales the input then quantizes it into a collection of precise output slice values. The class detects input value changes and applies selectable hysteresis when slice edge thresholds are reached to eliminate dead-zone noise issues without filtering delays. Applications include converting rotary knob position to discrete ranges of MIDI values, analog signal noise processing, level detection, rotary switch emulation, and signal display.

.. image:: https://github.com/CedarGroveStudios/CircuitPython_RangeSlicer/blob/master/media/range_slicer_models.png
   :alt: RangeSlicer Signal Models


The effect of using hysteresis to clean up a noisy signal:

.. image:: https://github.com/CedarGroveStudios/CircuitPython_RangeSlicer/blob/master/media/range_slicer_noise_models.png
   :alt: RangeSlicer Noise Models



Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.


Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install cedargrove_rangeslicer

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: Python

    """Reads two potentiometer inputs and produces -1.0 to +1.0 normalized outputs,
    one with an inverted output range."""

    import time
    import board
    from analogio import AnalogIn
    import cedargrove_rangeslicer as rs

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
        out_0 = ctrl_0.range_slicer(control_0)[0]
        out_1 = ctrl_1.range_slicer(control_1)[0]
        print( (control_0 / 65535, control_1 / 65535, out_0, out_1) )

        time.sleep(0.1)  # pause for 0.1 second


Documentation
=============
`RangeSlicer CircuitPython Driver API Class Description <https://github.com/CedarGroveStudios/CircuitPython_RangeSlicer/blob/master/media/pseudo_readthedocs_rangeslicer.pdf>`_

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_RangeSlicer/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
