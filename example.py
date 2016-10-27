# -*- encoding: utf-8 -*-
from miplant import MiPlant

for plant in MiPlant.discover(interface_index=1, timeout=5):
    print('--------------------------')
    print('Address: %s' % plant.address)
    print('Temperature: %.01f °C' % plant.temperature)
    print('Light: %i lx' % plant.light)
    print('Moisture: %i%%' % plant.moisture)
    print('Conductivity: %i µS/cm' % plant.conductivity)
