import gattlib
import logging
from math import isnan


class MiPlant(object):
    def __init__(self, address, device='hci0'):
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
        requester = gattlib.GATTRequester(self.address, True, self.device)
        try:
            received_bytes = bytearray(requester.read_by_handle(0x35)[0])
            self._temperature = float(received_bytes[1] * 256 + received_bytes[0]) / 10
            self._light = float(received_bytes[4] * 256 + received_bytes[3])
            self._moisture = received_bytes[7]
            self._conductivity = received_bytes[9] * 256 + received_bytes[8]
        except RuntimeError:
            self.log.exception('Failed to read sensor.')
        requester.disconnect()

    @property
    def temperature(self):
        if isnan(self._temperature):
            self.read()
        return self._temperature

    @property
    def light(self):
        if isnan(self._light):
            self.read()
        return self._light

    @property
    def moisture(self):
        if isnan(self._moisture):
            self.read()
        return self._moisture

    @property
    def conductivity(self):
        if isnan(self._conductivity):
            self.read()
        return self._conductivity

    @staticmethod
    def discover(device='hci0', timeout=2):
        return [
            MiPlant(address, device=device)
            for address, name in gattlib.DiscoveryService(device).discover(timeout).items()
            if name == 'Flower mate'
        ]
