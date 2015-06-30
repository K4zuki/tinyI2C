#-*- coding: utf-8 -*- 
#!/usr/bin/env python
import argparse
from tinyI2C import serial2i2c

class MyParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description="hogeeee")
        self._parser.add_argument('--port','-p', help='number or name of serial port', default='com1')
        self._parser.add_argument('--baud','-b', help='baudrate of serial port', default='115200')#460800
        self.args=self._parser.parse_args(namespace=self)        

#    parser.print_help()
parser = MyParser()
#    args=parser.parse_args()
#    print args
#    print args.port, args.baud

port = parser.args.port # port number, different in OSes
baud = parser.args.baud
dev = serial2i2c(port, baud)
##    channel="C0P"

#    raw_input("wait, press enter to set channel 0")
raw_input("wait, press enter to transferring data")
print dev.setChannel(0)
dev.write(0xD2,0x4100) 
dev.write(0xD2,0x42d2) 
dev.write(0xD2,0x42b0) 
dev.write(0xD2,0x42a9) 
dev.write(0xD2,0x428a) 
dev.write(0xD2,0x42a7) 
dev.write(0xD2,0x42a8) 
dev.write(0xD2,0x42b1) 
print dev.write(0xD2,0x4701) 
print dev.write_and_read(0x90, 0x50, 1)
raw_input("wait, press enter to transferring data")
if False:
    for hoo in range(4):
        print hoo
        dev.setChannel(hoo)
        print "--, 00, 02, 04, 06, 08, 0A, 0C, 0E"
        for hoge in range(0x00, 0x100, 0x10):
            print "%02X," %(hoge),
            for foo in range(0,0x10,0x02):
#                print "%02X," %(hoge|foo),
                if (dev.write(hoge|foo,0x00).split(",")[0] == "ACK"):
                    print ">A<",
                else:
                    print " N ",
#                print dev.write(hoge|foo,0x00).split(",")[0],
            print ""

    dev.setChannel(0)
    print ""
    print "---, ACK,00,01,02,03,04,05,06,07,08,09,0A,0B,0C,0D,0E,0F"
    for hoge in range(0x000, 0x100, 0x10):
        print "%03X," %(hoge),
        print dev.write_and_read((0x34|((hoge&0x100)>>7)), hoge&0xFF, 16)


###    raw_input("wait, press enter to transferring data")
###    print dev.setChannel(1)
###    print dev.write_and_read(0xD0,0xD0,16)
###    raw_input("wait, press enter to transferring data")
###    print dev.setChannel(2)
###    print dev.write_and_read(0xD0,0xD0,16)
###    raw_input("wait, press enter to transferring data")
###    print dev.setChannel(3)
###    print dev.write_and_read(0xD0,0xD0,16)

# 0x141,0x00
# 0x142,0xd2
# 0x142,0xb0
# 0x142,0xa9
# 0x142,0x8a
# 0x142,0xa7
# 0x142,0xa8
# 0x142,0xb1
##    print dev.write(0xD2,0x4100) 
##    print dev.write(0xD2,0x42d2) 
##    print dev.write(0xD2,0x42b0) 
##    print dev.write(0xD2,0x42a9) 
##    print dev.write(0xD2,0x428a) 
##    print dev.write(0xD2,0x42a7) 
##    print dev.write(0xD2,0x42a8) 
##    print dev.write(0xD2,0x42b1) 
##    time.sleep(0.1)
##    print dev.write(0xD2,0x4701)
##    time.sleep(0.1)
##    print dev.write_and_read(0xD0,0x50,16)
##    print dev.write_and_read(0xD0,0xD0,16)
#    print dev.write_and_read(0xD0,0x5D00,16)
##    print dev.write(0xD0,0x5D01)
##    time.sleep(0.1)
##    print dev.write(0xD0,0xD800)
##    print dev.write(0xD0,0xD846)
##    print dev.write(0xD0,0x5D00)

#    print dev.read(0xD0,1)
print dev.reg_read('01234')
print dev.reg_write([ [dev.GPIO0_STAT,0xFF],[dev.GPIO0_CONF,0xFF] ])
dev.raw_write('I01234P')
print dev.raw_read()
try:
    while False:
        for hoge in range(0,16):
            print dev.reg_write([[dev.GPIO0_STAT,hoge]]),
            print dev.write_and_read(0xD0, 0x50, 1)
except:
    print dev.raw_read()
    print dev.reg_write([[dev.GPIO0_STAT,0x00]])

print "reg_read = "+dev.reg_read('01234')
dev.raw_write('R'+dev.GPIO0_CONF+'P')
print "port_read = "+ dev.raw_read()
while False:
    print dev.write(0xD0, 0x5D00)

print dev.reg_write([[dev.SPI_CONF,0x08]])
print dev.reg_write([[dev.GPIO0_CONF,0x80]])
print dev.reg_write([[dev.GPIO0_STAT,0x80]])
print dev.write_and_read_SPI(2,0,0x6000)
_packet=[]
_head = str((0x80))
_line = str((0x00))
_data = str((0xC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CA))
_tail = str((0x0000))
_p = [_head,_line,_data,_tail,_tail]
_packet = "".join(_p)
raw_input(hex(_packet))
try:
    while True:
#            print dev.reg_write([[dev.SPI_CONF,0x00]])
#            print dev.reg_write([[dev.GPIO0_STAT,0x80]])
#            print dev.write_and_read_SPI(2,0,0xC4FE)
#            print dev.reg_write([[dev.GPIO0_STAT,0x00]])
        print dev.write_and_read_SPI(54,0,_packet)
#            print dev.write_and_read_SPI(54,0,0x8055C4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CA0000 )
#            print dev.write_and_read_SPI(54,0,0x80AAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CAC4FE30CA0000 )
#            print dev.reg_write([[dev.SPI_CONF,0x00]])
except:
    print dev.raw_read()

##    raw_input("wait, press enter to send repeated start command")
##    dev.ser.write(i2crw)
##    print dev.ser.readline()

##    raw_input("wait, press enter to send 'W' command")
##    ser.write('WP')
##    print dev.ser.readline()

##    raw_input("wait, press enter to send 'I' command")
##    ser.write('IP')
##    print dev.ser.readline()

##    raw_input("wait, press enter to send 'O' command")
##    ser.write('OP')
##    print dev.ser.readline()

##    raw_input("wait, press enter to send 'Z' command")
##    ser.write('ZP')
##    print dev.ser.readline()

##    raw_input("wait, press enter to send unknown command")
##    ser.write('XP')
##    print dev.ser.readline()

#    while(ser.inWaiting()>0):
#        print ser.readline()
#    dev.ser.close()
