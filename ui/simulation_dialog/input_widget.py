#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QGroupBox,
                             QSlider, QTreeWidget, QTreeWidgetItem,
                             QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QDoubleSpinBox)
from PyQt6.QtCore import pyqtSignal, QObject, Qt

import data
from calculation import interpolate
from .sim_plot import FuzzySimPlotList
from ui.my_splitter import MySplitter




class FuzzySimInputs(QGroupBox):
    sig_input_changed = pyqtSignal(dict, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('Inputs')
        h_box = QHBoxLayout()
        self.setLayout(h_box)

        self._h_splitter = MySplitter()
        h_box.addWidget(self._h_splitter)

        self.tree = FuzzySimInputTreeWidget()
        self._h_splitter.addWidget(self.tree)

        for each in data.data['inputs'].values():
            it = QSlider(Qt.Orientation.Horizontal)
            it.setMinimum(int(each.ling_vars[0].x[0]))
            it.setMaximum(int(each.ling_vars[0].x[-1]))

            spin = QDoubleSpinBox()
            spin.setMaximum(each.ling_vars[0].x[-1])
            spin.setMinimum(each.ling_vars[0].x[0])
            spin.setDecimals(2)

            top_it = FuzzySimInputTopTreeItem(it, spin)
            top_it.setText(0, each.name)
            top_it.signals.sig_input_changed.connect(self._input_changed)

            self.tree.addTopLevelItem(top_it)
            self.tree.setItemWidget(top_it, 1, it)
            self.tree.setItemWidget(top_it, 2, spin)

            for l_var in each.ling_vars:
                val_it = FuzzySimInputTreeItem(l_var)
                top_it.addChild(val_it)
            top_it.setExpanded(True)

        self.plots = FuzzySimPlotList(data.data['inputs'])
        self._h_splitter.addWidget(self.plots)


    def set_value(self, valdict):
        for k, v in valdict.items():
            self.plots.plots[k].set_v_line(v)
    def _input_changed(self, val):
        lin_vals = {}
        vals = {}
        for i in range(self.tree.topLevelItemCount()):
            top = self.tree.topLevelItem(i)
            nm = top.text(0)
            lin_vals[nm] = {}
            vals[nm] = top.value
            for n in range(top.childCount()):
                it = top.child(n)
                lin_vals[nm][it.text(0)] = float(it.text(1))
        self.sig_input_changed.emit(lin_vals, vals)



class FuzzySimInputTreeWidget(QTreeWidget):
    sig_input_changed = pyqtSignal(dict)

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setColumnCount(3)
        self.setHeaderHidden(True)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred)


class ItemSignal(QObject):
    sig_input_changed = pyqtSignal(float)


class FuzzySimInputTopTreeItem(QTreeWidgetItem):
    signals = ItemSignal()
    def __init__(self, slider:QSlider, spin:QDoubleSpinBox, parent=None):
        super().__init__(parent)
        self.slider = slider
        self.slider.valueChanged.connect(self._value_changed)

        self.spin = spin
        self.spin.valueChanged.connect(self._spinbox_val_changed)

        self.value = 0

    def _spinbox_val_changed(self):
        val = self.spin.value()

        for i in range(self.childCount()):
            self.child(i).set_var(val)

        self.value = float(val)
        self.slider.setValue(int(self.value))
        self.signals.sig_input_changed.emit(float(val))

    def _value_changed(self):
        val = self.slider.value()
        for i in range(self.childCount()):
            self.child(i).set_var(val)

        self.value = float(val)
        self.spin.setValue(self.value)
        self.signals.sig_input_changed.emit(float(val))

class FuzzySimInputTreeItem(QTreeWidgetItem):
    def __init__(self,ling_var, parent=None):
        super().__init__(parent)
        self.ling_var = ling_var
        self.setText(0, self.ling_var.name)
        self.set_var(0)

    def set_var(self, val):
        value = interpolate(val, self.ling_var.x, self.ling_var.y)
        self.setText(1, f'{value:.2f}')
