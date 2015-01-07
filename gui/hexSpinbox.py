#!/usr/bin/env python
# Copyright (c) 2007-8 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import sys
from PyQt4 import QtCore, QtGui
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *

def _hex2ascii(h, mask = 0xa0):
    chars_in_reverse = []
    chars_in_reverse.append("%X"%( (h & 0x0F)))
    chars_in_reverse.append("%X"%( ((h >> 4) & 0x0F)))
    h = h >> 8
    while h != 0x0:
        chars_in_reverse.append("%X"%( (h & 0x0F)))
        chars_in_reverse.append("%X"%( ((h >> 4) & 0x0F)))
        h = h >> 8

    chars_in_reverse.reverse()
    return "".join(chars_in_reverse)

# Regex adapted from Mark Pilgrim's "Dive Into Python" book
class HexSpinBox(QtGui.QSpinBox):

    def __init__(self, parent=None):
        super(HexSpinBox, self).__init__(parent)
#        regex = QRegExp(r"^M?M?M?(?:CM|CD|D?C?C?C?)" r"(?:XC|XL|L?X?X?X?)(?:IX|IV|V?I?I?I?)$")
        regex = QtCore.QRegExp(r"(^[ ]*0[xX][0-9A-Fa-f][0-9A-Fa-f]*)|(^[ ]*-?[0-9][0-9]*)")
#        regex.setCaseSensitivity(Qt.CaseInsensitive)
        self.validator = QtGui.QRegExpValidator(regex, self)
        self.setMaximum(255)
#        self.lineEdit.textEdited.connect(self.fixCase)
        self.connect(self.lineEdit(), QtCore.SIGNAL("textEdited(QString)"),
                     self.fixCase)

    def validate(self, text, pos):
        return self.validator.validate(text, pos)

    def fixCase(self, text):
        self.lineEdit().setText(text.toUpper())

    def valueFromText(self, text):
        text = unicode(text.toLower())
        chars = text.split("0x")
        text = "".join(chars[1:])
        return int(unicode(text),16)

    def textFromValue(self, value):
        return _hex2ascii(value)

if __name__ == "__main__":
    def report(value):
        print "%4d %s" % (value, _hex2ascii(value))

    app = QApplication(sys.argv)
    spinbox = HexSpinBox()
    spinbox.show()
    spinbox.setWindowTitle("Roman")
    spinbox.connect(spinbox, SIGNAL("valueChanged(int)"), report)
    app.exec_()
