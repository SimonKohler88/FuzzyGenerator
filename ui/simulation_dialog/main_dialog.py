#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QVBoxLayout, QDialog, QDialogButtonBox,
                             QHBoxLayout, QRadioButton, QWidget, QCheckBox)

from .input_widget import FuzzySimInputs
from .output_widget import FuzzySimOutputs
from calculation import calculate_yield
from ui.my_splitter import MySplitter
import data


class FuzzyLogicSimulatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Fuzzy Simulator')
        self.setMinimumSize(1100, 500)
        v_box = QVBoxLayout()
        
        self._h_splitter = MySplitter()
        
        self._input_grp = FuzzySimInputs()
        self._h_splitter.addWidget(self._input_grp)
        
        self._output_grp = FuzzySimOutputs()
        self._h_splitter.addWidget(self._output_grp)
        v_box.addWidget(self._h_splitter)
        
        self._verbose_cb = QCheckBox('Verbose')
        v_box.addWidget(self._verbose_cb)
        
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close)
        v_box.addWidget(self.buttonBox)
        self.setLayout(v_box)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self._input_grp.sig_input_changed.connect(self._calculate)
    
    def keyPressEvent(self, a0):
        # stupid: enter and return always pressing "ok" and closing dialog
        # -> disable keys
        if (a0.key() == Qt.Key.Key_Enter) | (a0.key() == Qt.Key.Key_Return):
            return
        super().keyPressEvent(a0)
    
    def _calculate(self, inp_d, vals):
        verbose = self._verbose_cb.isChecked()
        self._input_grp.set_value(vals)
        for i, step in enumerate(calculate_yield(inp_d, data.data, verbose)):
            step_n = i + 1
            if step_n == 3:
                self._output_grp.set_output_values(step)
            elif step_n == 6:
                self._output_grp.set_output_area(step)
            elif step_n == 7:
                self._output_grp.set_output_value(step)
