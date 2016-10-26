# -*- encoding: utf-8 -*-
import gattlib
import logging
from math import isnan


class MiPlant(object):
    def __init__(self, address, device='hci0'):
        '''
        Initializes the MiPlant -object.

        Parameters
        ----------
        address : string
            The MAC-address of the device.
        device : string
            The bluetooth device to use for reading, defaults to 'hci0'.
        '''
        self.address = address
        self.device = device
        self._log = logging.getLogger('MiPlant')
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
        success = False

        requester = gattlib.GATTRequester(self.address, True, self.device)
        try:
            received_bytes = bytearray(requester.read_by_handle(0x35)[0])
            self._temperature = float(received_bytes[1] * 256 + received_bytes[0]) / 10
            self._light = received_bytes[4] * 256 + received_bytes[3]
            self._moisture = received_bytes[7]
            self._conductivity = received_bytes[9] * 256 + received_bytes[8]
            success = True
        except RuntimeError:
            self.log.exception('Failed to read sensor.')
        requester.disconnect()

        return success

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
    def discover(device='hci0', timeout=2):
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
            MiPlant(address, device=device)
            for address, name in gattlib.DiscoveryService(device).discover(timeout).items()
            if name == 'Flower mate'
        ]
