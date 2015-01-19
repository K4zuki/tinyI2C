# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import os
from PyQt4 import QtCore, QtGui

#from tinyI2Cgen import Ui_Form, _fromUtf8
from tinyI2Cgui import Ui_Form, _fromUtf8

from serial.tools.list_ports import comports as serial_comports
#sys.path.append('..\\python')
sys.path.append('../python')
import tinyI2C
import time
import serial


class MyWidget(QtGui.QWidget):

    # SIGNAL definition
    readI2C_signal = QtCore.pyqtSignal(object)
    writeI2C_signal = QtCore.pyqtSignal(object)
    readGPIO_signal = QtCore.pyqtSignal(object)
    writeGPIO_signal = QtCore.pyqtSignal(object)

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

    def _search(self):
        self._list()

    def _list(self):
        _ser=0
        _dummy=[0,0,0]
        _ports=[]
        _idx=len(self.ports)

        if(self.isUI):
            self.gui.portList.clear()
            self.i2c._ser.close()
            for port in serial_comports():
                _dummy[0], _dummy[1], _dummy[2], = port
                print "_list()",_dummy[0]
                try:
                    _ser=serial.Serial(port=_dummy[0])
                except:
                    pass
                else:
                    _ser.close()
                    _ports.append( ": ".join(_dummy[:-1]))
                    self.ports.append( port[0])
                    print "_list()",self.ports
                    
            self.ports=self.ports[_idx:]
        
            self.gui.portList.addItems(_ports)
            self._setup(0)

    def _setup(self, _port = 0):
        if(self.isUI):
            if(self.i2c._ser.isOpen()):
                self.i2c._ser.close()
            print "_setup()",self.ports
            self.i2c=tinyI2C.serial2i2c(port=self.ports[_port])

    def _null(self):
        pass

    def readI2CSlot(self, arg):
        _slave,_channel,_register,_dest = arg
        read=self.i2c.setChannel(_channel)
        read=self.I2CregRead(_slave,_register)
        _dest.setValue(int(read,16))

    def writeI2CSlot(self, arg):
        _slave,_channel,_register,_data = arg
        self.i2c.setChannel(_channel)
        self.I2CregWrite(_slave,_register,_data)

#        CHIP_ID = '0',
#        GPIO0_STAT = '1',
#        GPIO1_STAT = '2',
#        GPIO0_CONF = '3',
#        GPIO1_CONF = '4',
#        REG5,
#        REG6,
#        REG7,
#        REG8,
#        REG9,
#"R| '0'| P"
#"R| '0'| '1'| ...| P"
#    def reg_read(self, registers = "012"):

    def readGPIOSlot(self, arg):
        _register,_dest = arg
        read=self.i2c.reg_read(_register).split(",")[0]
        read=int(read,16)
        for _bit in range(8):
            if (read&(1<<_bit)):
                _dest[_bit].setCheckState( QtCore.Qt.Checked )
            else:
                _dest[_bit].setCheckState( QtCore.Qt.Unchecked )
        _dest[8].setValue(read)

    def writeGPIOSlot(self, arg):
        _slave,_channel,_register,_data = arg
        self.i2c.setChannel(_channel)
        self.regWrite(_slave,_register,_data)

    def I2CregRead(self, slave=0x90, reg=0x00):
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

        self.i2c.raw_write("".join(packet))
        time.sleep(self.i2c._wait * 2)
        read= self.i2c.raw_read()
        read = read.split(",")[0]
        return read

    ## writes data to register address in selected slave address
    # copy and modify from tempcommand/instr_local.serial_i2c
    # @param slave slave address in HEX
    # @param reg register address in HEX
    # @param data data in HEX
    # @return created packet
    def I2CregWrite(self, slave=0x90, reg=0x00, data=0x00):
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

    def I2CreadClick(self):
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

    def I2CwriteClick(self):
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

    def GPIOreadClick(self):
        _sender = self.sender()
        if(_sender == self.gui.readbtn_reg0):
            self.gui.reg07.checked = True
            _register = self.i2c.CHIP_ID
            _dest = [   self.gui.reg00,
                        self.gui.reg01,
                        self.gui.reg02,
                        self.gui.reg03,
                        self.gui.reg04,
                        self.gui.reg05,
                        self.gui.reg06,
                        self.gui.reg07,
                        self.gui.read_reg0
                    ]
        elif(_sender == self.gui.readbtn_reg1):
            _register = self.i2c.GPIO0_STAT
            _dest = [   self.gui.reg10,
                        self.gui.reg11,
                        self.gui.reg12,
                        self.gui.reg13,
                        self.gui.reg14,
                        self.gui.reg15,
                        self.gui.reg16,
                        self.gui.reg17,
                        self.gui.read_reg1
                    ]
        elif(_sender == self.gui.readbtn_reg2):
            _register = self.i2c.GPIO1_STAT
            _dest = [   self.gui.reg20,
                        self.gui.reg21,
                        self.gui.reg22,
                        self.gui.reg23,
                        self.gui.reg24,
                        self.gui.reg25,
                        self.gui.reg26,
                        self.gui.reg27,
                        self.gui.read_reg2
                    ]
        elif(_sender == self.gui.readbtn_reg3):
            _register = self.i2c.GPIO0_CONF
            _dest = [   self.gui.reg30,
                        self.gui.reg31,
                        self.gui.reg32,
                        self.gui.reg33,
                        self.gui.reg34,
                        self.gui.reg35,
                        self.gui.reg36,
                        self.gui.reg37,
                        self.gui.read_reg3
                    ]
        elif(_sender == self.gui.readbtn_reg4):
            _register = self.i2c.GPIO1_CONF
            _dest = [   self.gui.reg40,
                        self.gui.reg41,
                        self.gui.reg42,
                        self.gui.reg43,
                        self.gui.reg44,
                        self.gui.reg45,
                        self.gui.reg46,
                        self.gui.reg47,
                        self.gui.read_reg4
                    ]
#        elif(_sender == self.gui.readbtn_reg5):
#            pass
#        elif(_sender == self.gui.readbtn_reg6):
#            pass
#        elif(_sender == self.gui.readbtn_reg7):
#            pass
        else:
            pass
        self.readGPIO_signal.emit([_register, _dest])

    def checkClick(self):
        _sender = self.sender()

if __name__=='__main__':

    app=QtGui.QApplication(sys.argv)
    window = MyWidget()
    ui=Ui_Form()
    ui.setupUi(window)
    window.getUI(ui)

    window._list()
    ui.portList.currentIndexChanged.connect(window._setup)
    ui.getPortBtn.clicked.connect(window._search)
    ui.readbtn_CH1.clicked.connect(window.I2CreadClick)
    ui.readbtn_CH2.clicked.connect(window.I2CreadClick)
    ui.readbtn_CH3.clicked.connect(window.I2CreadClick)
    ui.readbtn_CH4.clicked.connect(window.I2CreadClick)
    ui.readbtn_reg0.clicked.connect(window.GPIOreadClick)
    ui.readbtn_reg1.clicked.connect(window.GPIOreadClick)
    ui.writebtn_CH1.clicked.connect(window.I2CwriteClick)
    ui.writebtn_CH2.clicked.connect(window.I2CwriteClick)
    ui.writebtn_CH3.clicked.connect(window.I2CwriteClick)
    ui.writebtn_CH4.clicked.connect(window.I2CwriteClick)
    ui.base_CH1.editingFinished.connect(window._null)
    ui.base_CH2.editingFinished.connect(window._null)
    ui.reg_CH1.editingFinished.connect(window._null)
    ui.reg_CH2.editingFinished.connect(window._null)
    ui.base_CH3.editingFinished.connect(window._null)
    ui.reg_CH3.editingFinished.connect(window._null)
    ui.base_CH4.editingFinished.connect(window._null)
    ui.reg_CH4.editingFinished.connect(window._null)
    QtCore.QMetaObject.connectSlotsByName(window)
    window.readI2C_signal.connect(window.readI2CSlot)
    window.writeI2C_signal.connect(window.writeI2CSlot)
    window.readGPIO_signal.connect(window.readGPIOSlot)
    window.writeGPIO_signal.connect(window.writeGPIOSlot)

    window.show()
    sys.exit(app.exec_())
