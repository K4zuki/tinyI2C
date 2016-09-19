#-*- coding: utf-8 -*-
#!/usr/bin/env python
# MIT License (c) K4ZUKI <https://github.com/K4zuki>

import serial
import os.path
import time

# Table 3. ASCII commands supported by SC18IM700
# ASCII command Hex value Command function
# [X] S 0x53 I2C-bus START
# [X] P 0x50 I2C-bus STOP
# [X] R 0x52 read SC18IM700 internal register
# [X] W 0x57 write to SC18IM700 internal register
# [_] I 0x49 read GPIO port
# [_] O 0x4F write to GPIO port
# [_] Z 0x5A power down
# [X] C 0x43 change channel
# [_] E 0x45 SPI transfer start

##@brief RS232C to I2C converter using \e mbed
#@code register dump
#    dev = serial2i2c(port = 'com8', baud = '115200')
#
#    for hoge in range(0x050, 0x300, 0x10):
#        print "%03X," %(hoge),
#        print dev.write_and_read((0xD0|((hoge&0x300)>>7)), hoge&0xFF, 16)
#@endcode
class serial2i2c(object):
    """
    serial2i2c: RS232C to I2C converter using mbed
    "C| '0'| P"
    "C| '1'| P"
    "C| '2'| P"
    "C| '3'| P"
    "S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| P"
    "S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| S| 0x_8 _1| 0x_0 _4| P"
    "S| 0x_8 _1| 0x_0 _4| P"
    "R| '0'| P"
    "R| '0'| '1'| ...| P"
    "W| '0' 0x_a _a| P"
    "W| '0' 0x_a _a| '1' 0x_b _b| ...| P"
    "I| '0'| P"
    "O| '0'| 0x_a _a| P"
    """
    _ser = 0
    _channel = 0
    _wait = 1e-3
    ## register 0; ro; returns chip ID to identify device
    CHIP_ID = '0'

    ## register 1
    #@brief Readable / Writable
    #@param status 1 to set 'H' or 0 to set 'L' on each corresponding GPIO0 pin
    #@return status of GPIO0
    GPIO0_STAT = '1'
    ## register 2; rw; returns status of GPIO1 if enabled, 0xAA if disabled
    GPIO1_STAT = '2'
    ## register 2; rw; returns status of GPIO1 if enabled
    GPIO0_CONF = '3'
    GPIO1_CONF = '4'
    I2C_CONF = '5'
    SPI_CONF = '6'

    ## constructor
    # @param port COM port which device is conected
    # @param baud baudrate
    def __init__(self, port = 'com1', baud = '115200'):
        try:
            self._ser = serial.Serial(port, baudrate = baud, timeout = 0.1)
        except:
            raise

    ## sets channel by sending "C" command packet
    # @param channel I2C bus channel
    # @return response from module
    def setChannel(self, channel = 0):
        self._channel = channel
        self.raw_write("C" + str(self._channel) + "P")
        time.sleep(self._wait)
        return self.raw_read()

    ## reads multi byte data
    # @param address 8bit I2C slave address in HEX
    # @param length bytes to read
    # @return ACK/NAK + response string from device
    def read(self, address, length = 1):
        packet = ['S', 'P']

        address = self._hex2ascii(address, 0x30)
        alength = len(address) / 2
        packet.insert(1, chr(ord(address[0]) | 1))
        packet.insert(1, address[1])

        for _l in self._hex2ascii(length, 0x30):
            packet.insert(3, _l)

        self.raw_write("".join(packet))

        time.sleep(self._wait * length * 2)
        return self.raw_read()

    ## writes multi byte data
    # @param address 8bit I2C slave address in HEX
    # @param data data to send
    # @return ACK/NAK + response string from device
    def write(self, address, data = 0):
        packet = ['S', 'P']

        address = self._hex2ascii(address, 0x30)
        alength = len(address) / 2
        for _a in address:
            packet.insert(1, _a)

        data = self._hex2ascii(data, 0x30)
        length = len(data) / 2

        for _l in self._hex2ascii(length,0x30):
            packet.insert(3, _l)

        for _d in data:
            packet.insert(5, _d)

        self.raw_write("".join(packet))

        time.sleep(self._wait * length * 2)
        return self.raw_read()

    ## writes data and then reads from same slave device
    # @param address I2C slave address in HEX
    # @param wdata data to send in HEX
    # @param rlength bytes to read
    # @return ACK/NAK + response string from device
    def write_and_read(self, address, wdata = 0, rlength = 1):
        packet = ['S', 'S', 'P']

        address = self._hex2ascii(address, 0x30)
        alength = len(address) / 2
        for _a in address:
            packet.insert(1, _a)

        wdata = self._hex2ascii(wdata, 0x30)
        wlength = len(wdata) / 2

        for _wl in self._hex2ascii(wlength, 0x30):
            packet.insert(3, _wl)

        for _wd in wdata:
            packet.insert(5, _wd)

        packet.insert(6 + wlength * 2, chr(ord(address[0]) | 1))
        packet.insert(6 + wlength * 2, address[1])

        for _rl in self._hex2ascii(rlength, 0x30):
            packet.insert(8 + wlength * 2, _rl)

        self.raw_write("".join(packet))

        time.sleep(self._wait * rlength * 2)
        return self.raw_read()

    def write_and_read_SPI(self, wlength = 1, rlength = 0, data = 0xC4FEE0CA):

        _wlength = self._hex2ascii(wlength, 0x30)
        _rlength = self._hex2ascii(rlength, 0x30)
        _data = self._hex2ascii(data, 0x30)

        _wlength.reverse()
        _rlength.reverse()
        _data.reverse()

        packet = []
        packet.append('E')
        packet.extend(_wlength)
        packet.extend(_rlength)
        packet.extend(_data)
        packet.append('P')
        self.raw_write("".join(packet))

        time.sleep(self._wait * rlength * 2)
        return self.raw_read()

    ## sends raw data on serial port
    def raw_write(self, data="C4FEE0CA"):
        self._ser.write(data)

    ## reads raw data from serial port
    def raw_read(self):
        return (self._ser.readline().strip())

    ## sends 'S' command packet to make start condition
    def start(self):
        self._ser.write("S")

    ## sends 'P' command packet to make stop condition
    def stop(self):
        self._ser.write("P")
        time.sleep(self._wait)

    ## reads data from device's own register
    # @param registers register addresses
    # @return response string from device
    def reg_read(self, registers = "012"):
        packet = ['R', 'P']

        packet.insert(1, registers)

        self.raw_write("".join(packet))
        return self.raw_read()

    ## writes data into device's own register
    # @param register list of number and data list
    # @return response string from device
    def reg_write(self, pair = [ ('1', 0xFF), ]):
        packet = ['W', 'P']

        for _p in pair:
            reg, data = _p
            data = self._hex2ascii(data, 0x30)
            data.reverse()

            packet.insert(1, reg)
            packet.insert(2, "".join(data))

        length=len(packet)
        self.raw_write("".join(packet))

        time.sleep(self._wait * length)

        return self.raw_read()

    ## converts hex data to string
    # @param h data in HEX
    # @param mask mask data in HEX, LSB must be 0, MSB must not be 0 (0x?0, ?>8)
    # @return converted format in list
    def _hex2ascii(self, h, mask = 0x30):
        chars_in_reverse = []
        chars_in_reverse.append(chr(mask | (h & 0x0F)))
        chars_in_reverse.append(chr(mask | ((h >> 4) & 0x0F)))
        h = h >> 8
        while h != 0x0:
            chars_in_reverse.append(chr(mask | (h & 0x0F)))
            chars_in_reverse.append(chr(mask | ((h >> 4) & 0x0F)))
            h = h >> 8

        return (chars_in_reverse)

if __name__=="__main__":
    print "please try test.py"
