#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import binascii
from TinyI2c import TinyI2c
from colorama import init
from colorama import Fore, Back, Style
init()


class MyParser(object):

    def __init__(self):
        self._parser = argparse.ArgumentParser(description="TinyI2C test script")
        self._parser.add_argument('--port',
                                  '-p',
                                  help='number or name of serial port',
                                  default='com1'
                                  )
        self._parser.add_argument('--baud',
                                  '-b',
                                  help='baudrate of serial port',
                                  default='115200'
                                  )
        self.args = self._parser.parse_args(namespace=self)


def main(parser):
    port = parser.args.port
    baud = parser.args.baud
    dev = TinyI2c(port, baud)

    input("I2C: use channel 0")
    print(Fore.CYAN + Style.BRIGHT + "\tdev.setChannel(0)" + Style.RESET_ALL +
          " -> " + dev.setChannel(0))

    s = """
    I2C: on each channel:
    to slave 0x00 - 0xFE write single byte 0x00
    then get and list ACK/NAK
    """
    if False:
        input(s)
        for ch in range(4):
            print (ch)
            dev.setChannel(ch)
            print("--, 00, 02, 04, 06, 08, 0A, 0C, 0E")
            for msb in range(0x00, 0x100, 0x10):
                print("%02X," % (msb), end="")
                for lsb in range(0, 0x10, 0x02):
                    if (dev.write(msb | lsb, 0x00).split(",")[0] == "ACK"):
                        print(">A<", end=" ")
                    else:
                        print(" N ", end=" ")
                print ("")

    input("Registers: read registers 0/1/2/3/4 by API")
    print (Fore.CYAN + Style.BRIGHT + "\tdev.reg_read('01234')" + Style.RESET_ALL +
           " -> " + dev.reg_read('01234'))

    input("Registers: write single data `0x55` to registers 1/3 by API")
    print (Fore.CYAN + Style.BRIGHT +
           "\tdev.reg_write([[dev.GPIO0_STAT, 0x55], [dev.GPIO0_CONF, 0x55]])" +
           Style.RESET_ALL +
           " -> " + dev.reg_write([[dev.GPIO0_STAT, 0x55], [dev.GPIO0_CONF, 0x55]]))

    input("GPIO status: reads registers 0/1/2/3/4 " +
          "(where 0/3/4 returns 0xAA) by 'I' command using low level API")
    dev.raw_write('I01234P')
    print (Fore.CYAN + Style.BRIGHT + "\tdev.raw_write('I01234P')" +
           Style.RESET_ALL + " -> " + dev.raw_read())

    input("Registers: reads registers 0/1/2/3/4 again")
    print (Fore.CYAN + Style.BRIGHT + "\tdev.reg_read('01234')" + Style.RESET_ALL +
           " -> " + dev.reg_read('01234'))

    input("Registers: reads register 'GPIO0_CONF' by low level API")
    dev.raw_write('R' + dev.GPIO0_CONF + 'P')
    print (Fore.CYAN + Style.BRIGHT +
           "\tdev.raw_write('R' + dev.GPIO0_CONF + 'P'); dev.raw_read()" +
           Style.RESET_ALL + " -> " + dev.raw_read())

    input("Registers: writes single data '0x08' to register 'SPI_CONF' by" +
          " low level API")
    print (Fore.CYAN + Style.BRIGHT + "\tdev.reg_write([(dev.SPI_CONF, 0x08)])" +
           Style.RESET_ALL + " -> " + dev.reg_write([(dev.SPI_CONF, 0x08)]))

    input("Registers: writes single data '0x80' to register 'GPIO0_CONF' by" +
          " low level API")
    print (Fore.CYAN + Style.BRIGHT + "\tdev.reg_write([[dev.GPIO0_CONF, 0x80]])" +
           Style.RESET_ALL + " -> " + dev.reg_write([(dev.GPIO0_CONF, 0x80)]))

    input("Registers: writes single data '0x80' to register 'GPIO0_STAT' by" +
          " low level API")
    print (Fore.CYAN + Style.BRIGHT + "\tdev.reg_write([(dev.GPIO0_STAT, 0x80)])" +
           Style.RESET_ALL + " -> " + dev.reg_write([(dev.GPIO0_STAT, 0x80)]))

    input("SPI: writes 2byte data '0x6000' to SPI device by API")
    print (Fore.CYAN + Style.BRIGHT + "\tdev.write_and_read_SPI(2, 0, 0x6000)" +
           Style.RESET_ALL + " -> " + dev.write_and_read_SPI(2, 0, 0x6000))


if __name__ == '__main__':
    parser = MyParser()
    main(parser)
