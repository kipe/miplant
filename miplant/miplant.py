# -*- encoding: utf-8 -*-
from bluepy import btle
import logging
from math import isnan


class MiPlant(object):
    def __init__(self, address, interface_index=0):
        '''
        Initializes the MiPlant -object.

        Parameters
        ----------
        address : string
            The MAC-address of the device.
        interface_index : string
            The bluetooth device index to use for reading, defaults to 0.
        '''
        self.address = address
        self.interface_index = interface_index
        self._log = logging.getLogger('MiPlant')
        self._battery = 0
        self._firmware = ''
        self._temperature = float('nan')
        self._light = float('nan')
        self._moisture = float('nan')
        self._conductivity = float('nan')

    def __repr__(self):
        return "<MiPlant '%s'>" % (self.address)

    def read(self):
        '''
        Read the sensor with gattlib.

        Returns
        -------

        success : boolean
            True if the data was successfully received, otherwise False.
        '''
        try:
            peripheral = btle.Peripheral(self.address, iface=self.interface_index)
            peripheral.writeCharacteristic(0x33, bytearray([0xA0, 0x1F]), withResponse=True)

            received_bytes = bytearray(peripheral.readCharacteristic(0x38))
            self._battery = received_bytes[0]
            self._firmware = ''.join([chr(x) for x in received_bytes[1:7]])

            received_bytes = bytearray(peripheral.readCharacteristic(0x35))
            self._temperature = float(received_bytes[1] * 256 + received_bytes[0]) / 10
            self._light = received_bytes[4] * 256 + received_bytes[3]
            self._moisture = received_bytes[7]
            self._conductivity = received_bytes[9] * 256 + received_bytes[8]
            return True
        except:
            return False

    @property
    def battery(self):
        ''' Get battery level in percents (?), calls read-function if read yet. '''
        if self._battery == 0:
            self.read()
        return self._battery

    @property
    def firmware(self):
        ''' Get firmware as a string, calls read-function if read yet. '''
        if self._firmware == '':
            self.read()
        return self._firmware

    @property
    def temperature(self):
        ''' Get temperature value in degrees Celsius, calls read-function if read yet. '''
        if isnan(self._temperature):
            self.read()
        return self._temperature

    @property
    def light(self):
        ''' Get light level in lux, calls read-function if read yet. '''
        if isnan(self._light):
            self.read()
        return self._light

    @property
    def moisture(self):
        ''' Get moisture level in percent, calls read-function if read yet. '''
        if isnan(self._moisture):
            self.read()
        return self._moisture

    @property
    def conductivity(self):
        ''' Get conductivity in µS/cm, calls read-function if read yet. '''
        if isnan(self._conductivity):
            self.read()
        return self._conductivity

    @staticmethod
    def discover(interface_index=0, timeout=2):
        '''
        Discover devices.
        Only does basic checking by comparing name of the device to the default name.

        Parameters
        ----------

        device : string
            The bluetooth device to use for discovery, defaults to 'hci0'.
        timeout : int
            Timeout for searching the devices, defaults to 2.


        Returns
        -------

        devices : list of MiPlant -objects
            A list of MiPlant -objects corresponding to the devices found.
        '''

        return [
            MiPlant(device.addr, interface_index=interface_index)
            for device in btle.Scanner(interface_index).scan(timeout)
            if device.addr.startswith('c4:7c') and len([[1 for x in device.getScanData() if x[1] == 'Complete Local Name' and x[2] == 'Flower mate']]) != 0
        ]
