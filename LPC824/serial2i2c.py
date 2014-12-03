import serial
import argparse
import struct
import os.path
import binascii
import time

# Table 3. ASCII commands supported by SC18IM700
# ASCII command Hex value Command function
# S 0x53 I2C-bus START
# P 0x50 I2C-bus STOP
# R 0x52 read SC18IM700 internal register
# W 0x57 write to SC18IM700 internal register
# I 0x49 read GPIO port
# O 0x4F write to GPIO port
# Z 0x5A power down

class serial2i2c(object):
    ser=0
    channel='0'
    address=0x80
    wait=1e-3
    
    def __init__(self,port='com1',baud='115200'):
        self.ser=serial.Serial(port,baudrate=baud,timeout=1)
        
    def setChannel(self,channel=0):
        self.channel=channel
        self.ser.write("C"+str(self.channel)+"P")
        time.sleep(self.wait)
        return (self.ser.readline().strip())
        pass
        
    def read(self,address,length=1):
        self.ser.write("S"+chr(address|0x01)+chr(length)+"P")
        time.sleep(self.wait)
        return(self.ser.readline().strip())
        pass
        
    def write(self,address,data=0):
        data=self.convert_hex_to_ascii(data)
        length=len(data)
        format=">"+str(length)+"s"
        self.ser.write("S"+chr(address|0x00)+chr(length)\
                        +struct.pack(format,data)+"P")
        time.sleep(self.wait*length)
        return(self.ser.readline().strip())
        pass
        
    def write_and_read(self,address,wdata=0,rlength=1):
        wdata=self.convert_hex_to_ascii2(wdata)
        length=len(wdata)
        format=">"+str(length)+"s"
        print struct.pack(format,wdata)
        packet="S"+chr(address|0x00)+chr(length)+struct.pack(format,wdata)+"S"+chr(address|0x01)+chr(rlength)+"P"
#        print packet
        self.ser.write(packet)
##        self.ser.write("S"+chr(address|0x00)+chr(length)+struct.pack(format,wdata)\
##                        +"S"+chr(address|0x01)+chr(rlength)\
##                        +"P")
        time.sleep(self.wait*rlength)
        return(self.ser.readline().strip())

    def write_and_read2(self,address,wdata=0,rlength=1):
        packet=['S','S','P']
        
        address=self.convert_hex_to_ascii2(address,0xa0)
        alength=len(address)/2
        for hoge in address:
            packet.insert(1,hoge)

        wdata=self.convert_hex_to_ascii2(wdata,0xb0)
        wlength=len(wdata)/2

        for hoge in self.convert_hex_to_ascii2(wlength,0xc0):
            packet.insert(3,hoge)

        for hoge in wdata:
            packet.insert(5,hoge)
        
        print packet
        print "%2X"%(ord(address[0])|1)
        packet.insert(6+wlength*2,chr(ord(address[0])|1))
        packet.insert(6+wlength*2,address[1])

        for hoge in self.convert_hex_to_ascii2(rlength,0xd0):
            packet.insert(8+wlength*2,hoge)
            
#        rlength=self.convert_hex_to_ascii2(rlength)
        
##        print packet
##        print address,alength
##        print wdata,wlength
##        print rlength
##        print len(packet),(1+alength+wlength+1)
##        packet.insert(1+alength+wlength+1,address[0])
##        packet.insert(1+alength+wlength+1,address[1])
##        packet.insert(1+alength+wlength+alength+1,rlength[0])
##        packet.insert(1+alength+wlength+alength+1,rlength[1])
        print packet
##        length=self.convert_hex_to_ascii2(len(wdata))
##        format=">"+str(length)+"s"
##        print struct.pack(format,wdata)
##        packet="S"+self.convert_hex_to_ascii2(chr(address|0x00))+chr(length)+struct.pack(format,wdata)+"S"+chr(address|0x01)+chr(rlength)+"P"
##        self.ser.write(packet)
##        self.ser.write("S"+chr(address|0x00)+chr(length)+struct.pack(format,wdata)\
##                        +"S"+chr(address|0x01)+chr(rlength)\
##                        +"P")
        time.sleep(self.wait*rlength*2)
        return(self.ser.readline().strip())

    def raw_write(self,data="DEADBEAF"):
        self.ser.write(data)
        pass
    
    def start(self):
        self.ser.write("S")
        pass
        
    def stop(self):
        self.ser.write("P")
        time.sleep(self.wait)
        pass
    
    def convert_hex_to_ascii(self,h):
        chars_in_reverse = []
        chars_in_reverse.append(chr(h & 0xFF))
        h = h >> 8
        while h != 0x0:
            chars_in_reverse.append(chr(h & 0xFF))
            h = h >> 8
    
        chars_in_reverse.reverse()
        return ''.join(chars_in_reverse)

    def convert_hex_to_ascii2(self,h,mask=0xa0):
        chars_in_reverse = []
        chars_in_reverse.append(chr(mask|h & 0x0F))
        chars_in_reverse.append(chr(mask|(h>>4) & 0x0F))
        h = h >> 8
        while h != 0x0:
            chars_in_reverse.append(chr(mask|h & 0x0F))
            chars_in_reverse.append(chr(mask|(h>>4) & 0x0F))
            h = h >> 8
    
##        chars_in_reverse.reverse()
        print chars_in_reverse
        return (chars_in_reverse)
        
#    def send(self,data="Sx4hogeP"):
#        self.ser.write(data)
#        pass
        
        

class MyParser(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="hogeeee")
        self.parser.add_argument('--port','-p', help='number or name of serial port', default='com1')
#        self.parser.add_argument('--port','-p', help='number or name of serial port', default='/dev/ttyACM0')
#        self.parser.add_argument('--mon','-m', help='number or name of serial port', default='/dev/ttyACM0')
        self.parser.add_argument('--baud','-b', help='baudrate of serial port', default='115200')#460800
        self.args=self.parser.parse_args(namespace=self)        
      
if __name__=="__main__":
#    parser.print_help()
    parser=MyParser()
#    args=parser.parse_args()
#    print args
#    print args.port, args.baud
    
    port=parser.args.port # port number, different in OSes
    baud=parser.args.baud
    dev=serial2i2c(port,baud)
##    channel="C0P"
##    i2cw="S"+chr(0x80)+chr(0x04)+struct.pack(">4B",0xde,0xad,0xbe,0xaf)+"P"
##    i2crw="S"+chr(0x80)+chr(0x04)+struct.pack(">4B",0xde,0xad,0xbe,0xaf)+"S"+chr(0x81)+chr(0x04)+"P"
#    print channel,i2cw

#    raw_input("wait, press enter to set channel 0")
    raw_input("wait, press enter to transferring data")
    print dev.setChannel(0)
    print dev.setChannel(1)
#    print dev.setChannel(2)
#    print dev.setChannel(3)
#    print dev.setChannel(0)
#    print dev.ser.write(channel)
#    print dev.ser.readline().strip()
#    raw_input("wait, press enter to set channel 1")
#    print dev.ser.write("C1P")
#    print dev.ser.readline().strip()

#    raw_input("wait, press enter to send write command")
##    print dev.write(0xD0,0xdeadbeaf)
##    ser.write(i2cw)
    dev.start()
#    dev.raw_write(chr(0xd0))
    dev.stop()
    print dev.ser.readline().strip()
    print dev.write_and_read2(0xD0,0x50,16)
#    print dev.write_and_read(0xD0,0x50,16)
    while False:
        print dev.write_and_read(0xD0,0x50,16)
        print dev.write_and_read(0xD0,0xD0,16)
        print dev.write_and_read(0xD2,0x01,15)
        print dev.write_and_read(0xD2,0x40,16)
##    print "%02X"%(int(dev.write_and_read(0x90,0xdeadbeaf,50).split(',')[0],16))
#    print dev.ser.readline().strip()

##    raw_input("wait, press enter to send repeated start command")
##    dev.ser.write(i2crw)
##    print dev.ser.readline()

##    raw_input("wait, press enter to send 'R' command")
##    dev.ser.write('RP')
##    print dev.ser.readline()
##    neroaddr=0xD0
##    nerodata=[
##        [0xD8,0x00],
##        [0xD8,0x46],
##        [0xD8,0x7F],
##    ]
##    nerodata2=""
##    for hoge in nerodata:
##        print dev.convert_hex_to_ascii(hoge),
##    
###    print dev.convert_hex_to_ascii(nerodata)
##    
##    print dev.write(neroaddr,nerodata)
    

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
