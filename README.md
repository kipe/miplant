# MiPlant #

A Python-library for reading cheap plant monitoring sensors manufactured by Xiaomi.


## Usage

Scripts using the library need to be run as `root`, as using BLE typically requires it.
```python
from miplant import MiPlant

for plant in MiPlant.discover():
    print(plant.temperature)
```

## Overview

The sensors read 4 values:

- temperature in degrees Celsius (float, with 1 decimal precision)
- light level in lux (integer)
- moisture level in percent (integer)
- conductivity in µS/cm (integer)
    - presented as "fertility" in many places, even the official app

The values are only read when the `MiPlant.read()` -function is called, or
when one of the values is requested for the first time.

## Notes

- The scripts using this library need to be (at least typically) run as `root`,
  as `gattlib` requires setting up some options for Bluetooth Low Energy.
- Currently only tested with Python 2.7, but should work if `gattlib` works...
- The sensors seem to have some kind of internal cache, so don't even bother reading them too frequently.

## Thanks

Big thanks goes to
[Reverse engineering the Mi flora plant sensor](https://www.open-homeautomation.com/2016/08/23/reverse-engineering-the-mi-plant-sensor/)!
I wouldn't have bothered with reverese engineering the messages myself :P
