#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
# [X] I 0x49 read GPIO port
# [X] O 0x4F write to GPIO port
# [X] C 0x43 change channel
# [X] E 0x45 SPI transfer start

# "C| '0'| P"
# "C| '1'| P"
# "C| '2'| P"
# "C| '3'| P"
# "S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| P"
# "S| 0x_8 _0| 0x_0 _4| 0x_D _E _A _D _B _E _A _F| S| 0x_8 _1| 0x_0 _4| P"
# "S| 0x_8 _1| 0x_0 _4| P"
# "R| '0'| P"
# "R| '0'| '1'| ...| P"
# "W| '0' 0x_a _a| P"
# "W| '0' 0x_a _a| '1' 0x_b _b| ...| P"
# "I| '0'| P"
# "O| '0'| 0x_a _a| P"


class TinyI2C(object):
    """ RS232C to I2C converter using mbed
    Example:
       dev = serial2i2c(port = 'com8', baud = '115200')

       for reg in range(0x050, 0x300, 0x10):
           print "%03X," %(reg),
           print dev.write_and_read((0xD0|((reg&0x300)>>7)), reg&0xFF, 16)

    Keyword Args:
        port (str): COM port where device is conected
        baud (str): baudrate

    """
    bus = None
    channel = 0
    wait = 1e-3

    CHIP_ID = '0'
    """ Register 0

    Read only

    Returns:
        chip ID to identify device
    """

    GPIO0_STAT = '1'
    """ Register 1

    Readable / Writable

    Args:
        status 1 to set 'H' or 0 to set 'L' on each corresponding GPIO0 pin
    Returns:
        status of GPIO0
    """

    GPIO1_STAT = '2'
    """ Register 2

    Readable / Writable

    Returns:
        Status of GPIO1 if enabled, 0xAA if disabled
    """
    GPIO0_CONF = '3'
    """register 3

    Readable / Writable
    """

    GPIO1_CONF = '4'
    # register 4; rw;

    I2C_CONF = '5'
    # register 5; rw;

    SPI_CONF = '6'
    # register 6; rw;

    def __init__(self, port='com1', baud='115200'):
        try:
            self.bus = serial.Serial(port, baudrate=baud, timeout=0.1)
        except SerialException:
            raise

    def setChannel(self, channel=0):
        """ sets channel by sending "C" command packet

        Args:
            channel (int): I2C bus channel

        Returns:
            str: response from module
        """
        assert(isinstance(channel, int))
        self.channel = channel
        packet = ["C",
                  str(self.channel),
                  "P"]
        self.raw_write("".join(packet))
        time.sleep(self.wait)
        return self.raw_read()

    def read(self, address, length=1):
        """ reads multi byte data

        Args:
            address (int): 8bit I2C slave address in HEX
            length (int): bytes to read

        Returns:
            str: ACK/NAK + response string from device
        """

        packet = ['S', 'P']

        address = self.hex2ascii(address, 0x30)
        alength = len(address) / 2
        packet.insert(1, chr(ord(address[0]) | 1))
        packet.insert(1, address[1])

        for l in self.hex2ascii(length, 0x30):
            packet.insert(3, l)

        self.raw_write("".join(packet).encode(ascii))

        time.sleep(self.wait * length * 2)
        return self.raw_read().decode('utf-8')

    def write(self, address, data=0):
        """ writes multi byte data

        Args:
            address(int) 8bit I2C slave address in HEX
            data(int): data to send

        Returns:
            str: ACK/NAK + response string from device
        """
        packet = ['S', 'P']

        address = self.hex2ascii(address, 0x30)
        alength = len(address) / 2
        [packet.insert(1, addr) for addr in address]

        data = self.hex2ascii(data, 0x30)
        length = len(data) / 2

        [packet.insert(3, l) for l in self.hex2ascii(length, 0x30)]

        [packet.insert(5, d) for d in data]

        self.raw_write("".join(packet))

        time.sleep(self.wait * length * 2)
        return self.raw_read()

    def write_and_read(self, address, wdata=0, rlength=1):
        """ writes data and then reads from same slave device

        Args:
            address(int): I2C slave address in HEX
            wdata(int): data to send in HEX
            rlength(int): bytes to read

        Returns:
            str: ACK/NAK + response string from device
        """
        packet = ['S', 'S', 'P']

        address = self.hex2ascii(address, 0x30)
        alength = len(address) / 2
        [packet.insert(1, addr) for addr in address]

        wdata = self.hex2ascii(wdata, 0x30)
        wlength = len(wdata) / 2

        [packet.insert(3, wlen) for wlen in self.hex2ascii(wlength, 0x30)]

        [packet.insert(5, wd) for wd in wdata]

        packet.insert(6 + wlength * 2, chr(ord(address[0]) | 1))
        packet.insert(6 + wlength * 2, address[1])

        for rlen in self.hex2ascii(rlength, 0x30):
            packet.insert(8 + wlength * 2, rlen)

        self.raw_write("".join(packet))

        time.sleep(self.wait * rlength * 2)
        return self.raw_read().decode('utf-8')

    def write_and_read_SPI(self, wlength=1, rlength=0, data=0xC4FEE0CA):
        """ writes data and then reads from same SPI device

        Args:
            wlength(int): length to write
            rlength(int): length to read
            data(int): data to send

        Returns:
            str: ACK/NAK + response string from device
        """

        _wlength = self.hex2ascii(wlength, 0x30)
        _rlength = self.hex2ascii(rlength, 0x30)
        _data = self.hex2ascii(data, 0x30)

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

        time.sleep(self.wait * rlength * 2)
        return self.raw_read()

    def raw_write(self, data="C4FEE0CA"):
        # sends raw data on serial port
        self.bus.write(data.encode('ascii'))

    def raw_read(self):
        # reads raw data from serial port
        return (self.bus.readline().strip().decode('utf-8'))

    def start(self):
        # sends 'S' command packet to make start condition
        self.bus.write("S")

    def stop(self):
        # sends 'P' command packet to make stop condition
        self.bus.write("P")
        time.sleep(self.wait)

    def reg_read(self, registers="012"):
        """ reads data from device's own register

        Args:
            registers(str): register addresses

        Returns:
            str: response string from device
        """
        packet = "".join(["R",
                          registers,
                          "P"])

        self.raw_write(packet)
        return self.raw_read()

    def reg_write(self, pair=[('1', 0xFF), ]):
        """ writes data into device's own register

        Args:
            pair(list): register list of number and data list

        Returns:
            str: response string from device
        """
        packet = ['W', 'P']

        for _p in pair:
            reg, data = _p
            data = self.hex2ascii(data, 0x30)
            data.reverse()

            packet.insert(1, reg)
            packet.insert(2, "".join(data))

        length = len(packet)
        # print "".join(packet)
        self.raw_write("".join(packet))

        time.sleep(self.wait * length)

        return self.raw_read()

    def hex2ascii(self, h, mask=0x30):
        """ converts hex data to string
        Args:
            h(int): data in HEX
            mask(int): mask data in HEX, LSB must be 0, MSB must not be 0 (0x?0, ?>8)

        Returns:
            list: converted format in list
        """
        h = int(h)
        assert isinstance(h, int)
        chars_in_reverse = []
        chars_in_reverse.append(chr(mask | (h & 0x0F)))
        chars_in_reverse.append(chr(mask | ((h >> 4) & 0x0F)))
        h = h >> 8
        while h != 0x0:
            chars_in_reverse.append(chr(mask | (h & 0x0F)))
            chars_in_reverse.append(chr(mask | ((h >> 4) & 0x0F)))
            h = h >> 8

        return (chars_in_reverse)


if __name__ == "__main__":
    print ("please try test.py")
