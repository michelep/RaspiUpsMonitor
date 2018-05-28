from smbus2 import SMBusWrapper
import struct 

from config import Config

class Max17034:
    def __init__(self,address,bus):
	# MAX17043
	self.address = address
	self.i2c_bus = bus

    def readVoltage(self):
	with SMBusWrapper(self.i2c_bus) as bus:
	    read = bus.read_byte_data(self.address, 2)

	swapped = struct.unpack ("<H", struct.pack(">H", read))[0]
	voltage = swapped * 78.125 / 1000000
	return voltage

    def readCapacity(self):
	with SMBusWrapper(self.i2c_bus) as bus:
	    read = bus.read_byte_data(self.address, 4)

	swapped  = struct.unpack("<H", struct.pack(">H", read))[0]
	capacity = swapped/256
	return capacity

if __name__ == '__main__':
    # 0 = /dev/i2c-0 (port I2C0)
    # 1 = /dev/i2c-1 (port I2C1)
    bus = 1
    # MAX17043
    address = 0x36

    max17034 = Max17034(address,bus)
    print ( '%(volt).2fV (%(cap)i%%)' % { 'volt': max17034.readVoltage(), 'cap': max17034.readCapacity() } )
