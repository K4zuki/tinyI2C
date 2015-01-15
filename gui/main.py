# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import os
from PyQt4 import QtCore, QtGui

from tinyI2Cgen import Ui_Form, _fromUtf8

from serial.tools.list_ports import comports as serial_comports
#sys.path.append('..\\python')
sys.path.append('../python')
import tinyI2C
import time
import serial

class gui_local(object):
    def __init__(self, gui):
        self.gui=gui
        if os.name == 'posix':
            _port = "/dev/ttyS0"
        else:
            _port = "COM1"
        self.i2c=serial2i2c.serial2i2c(port=_port)
        self.ports=[]

    def list(self):
        _ports=[]
        self.gui.portList.clear()
        for port in serial_comports():
            _ports.append( ": ".join(port[:-1]))
            self.ports.append( port[0])
    
        _ports.sort()
        self.ports.sort()
        self.gui.portList.addItems(_ports)
        self.setup(0)
    
    def null(self):
        pass
    
    def setup(self, _port = 0):
        self.i2c._ser.close()
        self.i2c=serial2i2c.serial2i2c(port=self.ports[_port])

class MyWidget(QtGui.QWidget):

    # SIGNAL definition
    readI2C_signal = QtCore.pyqtSignal(object)
    writeI2C_signal = QtCore.pyqtSignal(object)

    isUI = False
    ports=[]
    i2c=None
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
    
    def getUI(self, gui):
        self.gui = gui
        self.isUI = True
        if os.name == 'posix':
            self.i2c=tinyI2C.serial2i2c(port="/dev/ttyS0")
        else:
            self.i2c=tinyI2C.serial2i2c()

    def _list(self):
        if(self.isUI):
            _ser=0
            _dummy=[0,0,0]
            _ports=[]
            self.ports=[]
            self.gui.portList.clear()
            for port in serial_comports():
                _dummy[0], _dummy[1], _dummy[2], = port
#                print _dummy[0]
                try:
                    _ser=serial.Serial(port=_dummy[0])
                except:
#                    print _ser
                    pass
                else:
                    _ser.close()
                    _ports.append( ": ".join(_dummy[:-1]))
                    self.ports.append( port[0])
        
#            _ports.sort()
#            self.ports.sort()
            self.gui.portList.addItems(_ports)
#            self._setup(0)
#            print _ports
#            print self.ports

    def _setup(self, _port = 0):
        if(self.isUI):
            self.i2c._ser.close()
            self.i2c=tinyI2C.serial2i2c(port=self.ports[_port])
    #        print i2c._ser._isOpen

    def _null(self):
        pass

    def readSlot(self, arg):
        _slave,_channel,_register,_dest = arg
#        print "read from channel %d, slave= %02X, register= %02X" % (_channel,_slave,_register)
        read=self.i2c.setChannel(_channel)
#        print read
        read=self.regRead(_slave,_register)
#        print read
        _dest.setValue(int(read,16))

    def writeSlot(self, arg):
        _slave,_channel,_register,_data = arg
        self.i2c.setChannel(_channel)
        self.regWrite(_slave,_register,_data)
#        print "write to %s" % arg

    def regRead(self, slave=0x90, reg=0x00):
        packet=[]
        slave=self.i2c._hex2ascii(slave,mask=0xa0)
        reg=self.i2c._hex2ascii(reg,mask=0xb0)
        length=self.i2c._hex2ascii(len(reg)/2,mask=0xd0)

        slave.reverse()
        length.reverse()
        reg.reverse()

        packet.extend(slave)
        packet.extend(length)
        packet.extend(reg)
        packet.insert(0,'S')
        packet.append('S')

        slave[1]=chr(ord(slave[1]) | 1)
        length=self.i2c._hex2ascii(1,mask=0xd0)
        
        length.reverse()

        packet.extend(slave)
        packet.extend(length)
        packet.append('P')

#        print "".join(packet)
        self.i2c.raw_write("".join(packet))
        time.sleep(self.i2c._wait * 2)
        read= self.i2c.raw_read()
#        print self.i2c.raw_read()
        read = read.split(",")[0]
#        print read
        return read

    ## writes data to register address in selected slave address
    # copy and modify from tempcommand/instr_local.serial_i2c
    # @param slave slave address in HEX
    # @param reg register address in HEX
    # @param data data in HEX
    # @return created packet
    def regWrite(self, slave=0x90, reg=0x00, data=0x00):
        packet=[]
        slave=self.i2c._hex2ascii(slave,mask=0xa0)
        reg=self.i2c._hex2ascii(reg,mask=0xb0)
        data=self.i2c._hex2ascii(data,mask=0xc0)
        length=self.i2c._hex2ascii(len(reg)/2+len(data)/2,mask=0xd0)
        
        slave.reverse()
        length.reverse()
        reg.reverse()
        data.reverse()

        packet.extend(slave)
        packet.extend(length)
        packet.extend(reg)
        packet.extend(data)

        packet.insert(0,'S')
        packet.append('P')

        self.i2c.raw_write("".join(packet))
        _read= self.i2c.raw_read()
#        print packet
        return packet

    def readClick(self):
        _sender = self.sender()
        _channel = 0
        if(_sender == self.gui.readbtn_CH1):
            _slave = self.gui.base_CH1.value()
            _register = self.gui.reg_CH1.value()
            _channel = 0
            _dest = self.gui.read_CH1
        elif(_sender == self.gui.readbtn_CH2):
            _slave = self.gui.base_CH2.value()
            _register = self.gui.reg_CH2.value()
            _channel = 1
            _dest = self.gui.read_CH2
        elif(_sender == self.gui.readbtn_CH3):
            _slave = self.gui.base_CH3.value()
            _register = self.gui.reg_CH3.value()
            _channel = 2
            _dest = self.gui.read_CH3
        elif(_sender == self.gui.readbtn_CH4):
            _slave = self.gui.base_CH4.value()
            _register = self.gui.reg_CH4.value()
            _channel = 3
            _dest = self.gui.read_CH4
        else:
            pass
        self.readI2C_signal.emit([_slave, _channel, _register, _dest])

    def writeClick(self):
        _sender = self.sender()
        _channel = 0
        if(_sender == self.gui.writebtn_CH1):
            _slave = self.gui.base_CH1.value()
            _register = self.gui.reg_CH1.value()
            _channel = 0
            _data = self.gui.write_CH1.value()
        elif(_sender == self.gui.writebtn_CH2):
            _slave = self.gui.base_CH2.value()
            _register = self.gui.reg_CH2.value()
            _channel = 1
            _data = self.gui.write_CH2.value()
        elif(_sender == self.gui.writebtn_CH3):
            _slave = self.gui.base_CH3.value()
            _register = self.gui.reg_CH3.value()
            _channel = 2
            _data = self.gui.write_CH3.value()
        elif(_sender == self.gui.writebtn_CH4):
            _slave = self.gui.base_CH4.value()
            _register = self.gui.reg_CH4.value()
            _channel = 3
            _data = self.gui.write_CH4.value()
        else:
            pass
        self.writeI2C_signal.emit([_slave, _channel, _register, _data])

if __name__=='__main__':

    app=QtGui.QApplication(sys.argv)
    window = MyWidget()
    ui=Ui_Form()
    ui.setupUi(window)
    window.getUI(ui)

    window._list()
    ui.portList.currentIndexChanged.connect(window._setup)
    ui.getPortBtn.clicked.connect(window._list)
    ui.readbtn_CH1.clicked.connect(window.readClick)
    ui.readbtn_CH2.clicked.connect(window.readClick)
    ui.readbtn_CH3.clicked.connect(window.readClick)
    ui.readbtn_CH4.clicked.connect(window.readClick)
    ui.writebtn_CH1.clicked.connect(window.writeClick)
    ui.writebtn_CH2.clicked.connect(window.writeClick)
    ui.writebtn_CH3.clicked.connect(window.writeClick)
    ui.writebtn_CH4.clicked.connect(window.writeClick)
    ui.base_CH1.editingFinished.connect(window._null)
    ui.base_CH2.editingFinished.connect(window._null)
    ui.reg_CH1.editingFinished.connect(window._null)
    ui.reg_CH2.editingFinished.connect(window._null)
    ui.base_CH3.editingFinished.connect(window._null)
    ui.reg_CH3.editingFinished.connect(window._null)
    ui.base_CH4.editingFinished.connect(window._null)
    ui.reg_CH4.editingFinished.connect(window._null)
    QtCore.QMetaObject.connectSlotsByName(window)
    window.readI2C_signal.connect(window.readSlot)
    window.writeI2C_signal.connect(window.writeSlot)

    
    window.show()
    sys.exit(app.exec_())
