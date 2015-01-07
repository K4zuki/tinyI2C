#!/usr/bin/env/pythonw

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication,QWidget

from tinyI2Cgen import Ui_Form, _fromUtf8

from serial.tools.list_ports import comports as serial_comports
sys.path.append('W:\\Tokyo\\Home\\kyamamot\\common\\GitHub\\tempcommand')
import serial2i2c


class gui_local(object):
    def __init__(self, gui):
        self.gui=gui
        self.i2c=serial2i2c.serial2i2c()
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
    
    def null(self):
        pass
    
    def setup(self, _port = 0):
        self.i2c._ser.close()
        self.i2c=serial2i2c.serial2i2c(port=self.ports[_port])
#        pass
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    window=QWidget()
    ui=Ui_Form()
    ui.setupUi(window)
    gui=gui_local(ui)

#    QtCore.QObject.connect(ui.getPortBtn,     QtCore.SIGNAL(_fromUtf8("clicked()")),  ui.portList.clear)
    QtCore.QObject.connect(ui.portList,     QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")),  gui.setup)
    QtCore.QObject.connect(ui.getPortBtn,  QtCore.SIGNAL(_fromUtf8("clicked()")),  gui.list)
    QtCore.QObject.connect(ui.readbtn_CH1, QtCore.SIGNAL(_fromUtf8("clicked()")), ui.read_CH1.clear)
    QtCore.QObject.connect(ui.readbtn_CH2, QtCore.SIGNAL(_fromUtf8("clicked()")), ui.read_CH2.clear)
    QtCore.QObject.connect(ui.readbtn_CH3, QtCore.SIGNAL(_fromUtf8("clicked()")), ui.read_CH3.clear)
    QtCore.QObject.connect(ui.readbtn_CH4, QtCore.SIGNAL(_fromUtf8("clicked()")), ui.read_CH4.clear)
    QtCore.QObject.connect(ui.writebtn_CH1, QtCore.SIGNAL(_fromUtf8("clicked()")), ui.write_CH1.clear)
    QtCore.QObject.connect(ui.writebtn_CH2, QtCore.SIGNAL(_fromUtf8("clicked()")), ui.write_CH2.clear)
    QtCore.QObject.connect(ui.writebtn_CH3, QtCore.SIGNAL(_fromUtf8("clicked()")), ui.write_CH3.clear)
    QtCore.QObject.connect(ui.writebtn_CH4, QtCore.SIGNAL(_fromUtf8("clicked()")), ui.write_CH4.clear)
    QtCore.QObject.connect(ui.base_CH1, QtCore.SIGNAL(_fromUtf8("editingFinished()")), gui.null)
    QtCore.QObject.connect(ui.base_CH2, QtCore.SIGNAL(_fromUtf8("editingFinished()")), gui.null)
    QtCore.QObject.connect(ui.reg_CH1, QtCore.SIGNAL(_fromUtf8("editingFinished()")),  gui.null)
    QtCore.QObject.connect(ui.reg_CH2, QtCore.SIGNAL(_fromUtf8("editingFinished()")),  gui.null)
    QtCore.QObject.connect(ui.base_CH3, QtCore.SIGNAL(_fromUtf8("editingFinished()")), gui.null)
    QtCore.QObject.connect(ui.reg_CH3, QtCore.SIGNAL(_fromUtf8("editingFinished()")),  gui.null)
    QtCore.QObject.connect(ui.base_CH4, QtCore.SIGNAL(_fromUtf8("editingFinished()")), gui.null)
    QtCore.QObject.connect(ui.reg_CH4, QtCore.SIGNAL(_fromUtf8("editingFinished()")),  gui.null)
    QtCore.QMetaObject.connectSlotsByName(window)

    gui.list()
    
    window.show()
    sys.exit(app.exec_())
