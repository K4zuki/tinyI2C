# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from hexSpinbox import *

class MyWidget(QWidget):

    #  シグナルの定義
    readI2C_signal = pyqtSignal(object)
    writeI2C_signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        
        font = QtGui.QFont()
        font.setPointSize(12)

        self.read_button = QPushButton("read", self)
        self.read_button.setFont(font)

        self.write_button = QPushButton("write", self)
        self.write_button.setFont(font)

        self.slaveSpin = HexSpinBox(self)
        self.slaveSpin.setFont(font)

        self.registerSpin = HexSpinBox(self)
        self.registerSpin.setFont(font)

        self.readSpin = HexSpinBox(self)
        self.readSpin.setFont(font)
        self.readSpin.setEnabled(False)

        self.writeSpin = HexSpinBox(self)
        self.writeSpin.setFont(font)
        
        layout = QHBoxLayout()
        layout.addWidget(self.read_button)
        layout.addWidget(self.write_button)
        layout.addWidget(self.slaveSpin)
        layout.addWidget(self.registerSpin)
        layout.addWidget(self.readSpin)
        layout.addWidget(self.writeSpin)
        self.setLayout(layout)

        self.read_button.clicked.connect(self.readClick)
        self.write_button.clicked.connect(self.writeClick)
        
        self.readI2C_signal.connect(self.readSlot)
        self.writeI2C_signal.connect(self.writeSlot)
    
    def readClick(self):
        _sender = self.sender()
        _channel = 0
        if(_sender == self.read_button):
            _slave = self.slaveSpin.value()
            _register = self.registerSpin.value()
            _channel = 1
            _dest = self.readSpin
        else:
            pass
        self.readI2C_signal.emit([_slave, _channel, _register, _dest])

    def writeClick(self):
        _sender = self.sender()
        if(_sender == self.write_button):
            _slave = self.slaveSpin.value()
            _register = self.registerSpin.value()
            _channel = 1
            _data = self.writeSpin.value()
        else:
            pass
        self.writeI2C_signal.emit([_slave, _channel, _register, _data])

    def readSlot(self,arg):
        print "read from %s" % arg

    def writeSlot(self,arg):
        print "write to %s" % arg

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MyWidget()
    win.show()
    sys.exit( app.exec_() )
