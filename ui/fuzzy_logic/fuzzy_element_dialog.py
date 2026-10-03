#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt6.QtWidgets import (QVBoxLayout, QComboBox, QDialog, QFormLayout,
                             QDialogButtonBox, QMessageBox)


class NewFuzzyElementDialog(QDialog):
    def __init__(self, inp_mod, outp_mod, pairs, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add New Fuzzy Logic Element')
        lay = QFormLayout()
        self.inp1 = QComboBox()
        self.inp1.setModel(inp_mod)
        
        self.inp2 = QComboBox()
        self.inp2.setModel(inp_mod)
        
        self.out = QComboBox()
        self.out.setModel(outp_mod)
        
        self.pairs = pairs
        
        lay.addRow('Input 1:', self.inp1)
        lay.addRow('Input 2:', self.inp2)
        lay.addRow('Output:', self.out)
        
        v_box = QVBoxLayout()
        v_box.addLayout(lay)
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel)
        v_box.addWidget(self.buttonBox)
        self.setLayout(v_box)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    
    def accept(self):
        in1 = self.inp1.currentText()
        in2 = self.inp2.currentText()
        out = self.out.currentText()
        if in1 == in2:
            msg = QMessageBox(QMessageBox.Icon.Critical, 'No.',
                              'Same Inputs are not allowed', parent=self)
            msg.exec()
            return
        
        if out in self.pairs:
            for a, b in self.pairs[out]:
                if (a == in1 and b == in2) or (a == in2 and b == in1):
                    msg = QMessageBox(QMessageBox.Icon.Critical, 'No.',
                                      'Combination already existing', parent=self)
                    msg.exec()
                    return
        
        super().accept()
