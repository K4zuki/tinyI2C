# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import os
from PyQt4 import QtCore, QtGui
#from PyQt4.
#from QtCore import *
#from PyQt4.
#from QtGui  import *

from tinyI2Cgen import Ui_Form, _fromUtf8

from serial.tools.list_ports import comports as serial_comports
sys.path.append('..\\tempcommand')
import serial2i2c

class gui_local(object):
    def __init__(self, gui):
        self.gui=gui
        if os.name == 'posix':
            _port = "/dev/ttyS0"
        self.i2c=serial2i2c.serial2i2c(port=_port)
        self.ports=[]

    def read(self):
        pass
    
    def write(self):
        pass
    
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

    #  シグナルの定義
    readI2C_signal = QtCore.pyqtSignal(object)
    writeI2C_signal = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
    
    def getUI(self, gui):
        self.gui = gui

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

    def list():
        _ports=[]
        ui.portList.clear()
        for port in serial_comports():
            _ports.append( ": ".join(port[:-1]))
            ports.append( port[0])
    
        _ports.sort()
        ports.sort()
        ui.portList.addItems(_ports)
        setup(0)
    
    def null():
        pass
    
    def setup( _port = 0):
        global i2c
        i2c._ser.close()
        i2c=serial2i2c.serial2i2c(port=ports[_port])

    def readSlot(arg):
        global i2c
        _slave,_channel,_register,_dest = arg
#        print "read from channel %d, slave= %02X, register= %02X" % (_channel,_slave,_register)
        i2c.setChannel(_channel)
        read=regRead(_slave,_register)
        _dest.setValue(int(unicode(read),16))
        

    def writeSlot(arg):
        global i2c
        _slave,_channel,_register,_data = arg
        i2c.setChannel(_channel)
        regWrite(_slave,_register,_data)
#        print "write to %s" % arg

    def regRead(slave=0x90, reg=0x00):
        global i2c
        packet=[]
        slave=i2c._hex2ascii(slave,mask=0xa0)
        reg=i2c._hex2ascii(reg,mask=0xb0)
        length=i2c._hex2ascii(len(reg)/2,mask=0xd0)

        slave.reverse()
        length.reverse()
        reg.reverse()

        packet.extend(slave)
        packet.extend(length)
        packet.extend(reg)
        packet.insert(0,'S')
        packet.append('S')

        slave[1]=chr(ord(slave[1]) | 1)
        length=i2c._hex2ascii(1,mask=0xd0)
        
        length.reverse()

        packet.extend(slave)
        packet.extend(length)
        packet.append('P')

#        print packet
        i2c.raw_write("".join(packet))
        read= i2c.raw_read()
        read = read.split(",")[0]
#        print read
        return read

    ## writes data to register address in selected slave address
    # copy and modify from tempcommand/instr_local.serial_i2c
    # @param slave slave address in HEX
    # @param reg register address in HEX
    # @param data data in HEX
    # @return created packet
    def regWrite(slave=0x90, reg=0x00, data=0x00):
        global i2c
        packet=[]
        slave=i2c._hex2ascii(slave,mask=0xa0)
        reg=i2c._hex2ascii(reg,mask=0xb0)
        data=i2c._hex2ascii(data,mask=0xc0)
        length=i2c._hex2ascii(len(reg)/2+len(data)/2,mask=0xd0)
        
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

        i2c.raw_write("".join(packet))
        _read= i2c.raw_read()
        return packet

    if os.name == 'posix':
        i2c=serial2i2c.serial2i2c(port="/dev/ttyS0")
    else:
        i2c=serial2i2c.serial2i2c()
    ports=[]

    app=QtGui.QApplication(sys.argv)
#    window=QWidget()
    window = MyWidget()
    ui=Ui_Form()
    ui.setupUi(window)
    window.getUI(ui)
#    gui=gui_local(ui)

#    ui.portList.currentIndexChanged.connect(gui.setup)
    ui.portList.currentIndexChanged.connect(setup)
    ui.getPortBtn.clicked.connect(list)
    ui.readbtn_CH1.clicked.connect(window.readClick)
    ui.readbtn_CH2.clicked.connect(window.readClick)
    ui.readbtn_CH3.clicked.connect(window.readClick)
    ui.readbtn_CH4.clicked.connect(window.readClick)
    ui.writebtn_CH1.clicked.connect(window.writeClick)
    ui.writebtn_CH2.clicked.connect(window.writeClick)
    ui.writebtn_CH3.clicked.connect(window.writeClick)
    ui.writebtn_CH4.clicked.connect(window.writeClick)
    ui.base_CH1.editingFinished.connect(null)
    ui.base_CH2.editingFinished.connect(null)
    ui.reg_CH1.editingFinished.connect(null)
    ui.reg_CH2.editingFinished.connect(null)
    ui.base_CH3.editingFinished.connect(null)
    ui.reg_CH3.editingFinished.connect(null)
    ui.base_CH4.editingFinished.connect(null)
    ui.reg_CH4.editingFinished.connect(null)
    QtCore.QMetaObject.connectSlotsByName(window)
    window.readI2C_signal.connect(readSlot)
    window.writeI2C_signal.connect(writeSlot)

    list()
    
    window.show()
    sys.exit(app.exec_())
