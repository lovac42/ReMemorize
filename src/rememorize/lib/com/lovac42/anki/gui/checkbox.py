# -*- coding: utf-8 -*-
# Copyright (c) 2020 Lovac42
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from aqt.qt import *
from anki.lang import _


class TristateCheckbox(QCheckBox):
    _descriptions = {
        Qt.Unchecked:        "Disabled",
        Qt.PartiallyChecked: "Partial",
        Qt.Checked:          "Full"
    }

    def __init__(self, parent):
        super(TristateCheckbox, self).__init__(parent)
        self.setTristate(True)
        self.stateChanged.connect(self.onStateChanged)

    def onStateChanged(self, state):
        assert Qt.Unchecked <= state <= Qt.Checked
        desc = self._descriptions[state]
        self.setText(_(desc))

    def getDescriptions(self):
        return self._descriptions

    def setDescriptions(self, desc):
        assert len(desc) == 3
        self._descriptions = desc

    def setCheckState(self, state):
        assert Qt.Unchecked <= state <= Qt.Checked
        super(TristateCheckbox, self).setCheckState(state)
        if not state:
            self.onStateChanged(Qt.Unchecked)
