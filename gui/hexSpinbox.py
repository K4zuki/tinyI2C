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

# Regex adapted from Mark Pilgrim's "Dive Into Python" book
class HexSpinBox(QtGui.QSpinBox):

    def __init__(self, parent=None):
        super(HexSpinBox, self).__init__(parent)
#        regex = QtCore.QRegExp(r"(^[ ]*0[xX][0-9A-Fa-f][0-9A-Fa-f]*)|(^[ ]*-?[0-9][0-9]*)")
        regex = QtCore.QRegExp(r"(^[ ]*[0-9A-Fa-f][0-9A-Fa-f])|(^[ ]*-?[0-9][0-9])")
        self.validator = QtGui.QRegExpValidator(regex, self)
        self.setMaximum(255)
        self.connect(self.lineEdit(), QtCore.SIGNAL("textEdited(QString)"),
                     self.fixCase)

    def validate(self, text, pos):
        return self.validator.validate(text, pos)

    def fixCase(self, text):
        self.lineEdit().setText(text.toUpper())

    def valueFromText(self, text):
        text = unicode(text.toLower())
        chars = text.split()
        text = "".join(chars[:1])
        return int(unicode(text),16)

    def textFromValue(self, value):
        return self._hex2ascii(value)

    def _hex2ascii(self, h, mask = 0xa0):
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

if __name__ == "__main__":
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

    def report(value):
        print "%4d %s" % (value, _hex2ascii(value))

    app = QtGui.QApplication(sys.argv)
    spinbox = HexSpinBox()
    spinbox.show()
    spinbox.setWindowTitle("Roman")
    spinbox.connect(spinbox, QtCore.SIGNAL("valueChanged(int)"), report)
    app.exec_()
