#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QGroupBox,
                             QTreeWidget, QTreeWidgetItem,
                             QVBoxLayout, QProgressBar, QHBoxLayout,
                             QSizePolicy)
from PyQt6.QtCore import pyqtSignal

import data
from .sim_plot import FuzzySimPlotList
from ui.my_splitter import MySplitter

class FuzzySimOutputs(QGroupBox):
    sig_input_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('Outputs')
        h_box = QHBoxLayout()
        self.setLayout(h_box)

        self._h_splitter = MySplitter()
        h_box.addWidget(self._h_splitter)

        self.tree = FuzzySimOutputTreeWidget()
        self._h_splitter.addWidget(self.tree)

        for each in data.data['outputs'].values():
            it = FuzzySimOutProgressBar()
            it.setMinimum(int(each.ling_vars[0].x[0]*100))
            it.setMaximum(int(each.ling_vars[0].x[-1]*100))
            it.setTextVisible(False)

            top_it = FuzzySimOutputTopTreeItem(it)
            top_it.setText(0, each.name)
            self.tree.addTopLevelItem(top_it)
            self.tree.setItemWidget(top_it, 1, it)

            for l_var in each.ling_vars:
                val_it = FuzzySimOutputTreeItem(l_var)
                top_it.addChild(val_it)
            top_it.setExpanded(True)

        self.plots = FuzzySimPlotList(data.data['outputs'])
        self._h_splitter.addWidget(self.plots)

    def set_output_area(self, valdict):
        for k, v in valdict.items():
            self.plots.plots[k].set_area(v)

    def set_output_value(self, valdict):
        for k, v in valdict.items():

            self.plots.plots[k].set_v_line(v)
            for i in range(self.tree.topLevelItemCount()):
                out_it = self.tree.topLevelItem(i)
                if out_it.text(0) == k:
                    out_it.bar.setValue(v)
                    out_it.setText(2, f'{v:.2f}')

    def set_output_values(self, val_dict):
        for k, v in val_dict.items():
            for i in range(self.tree.topLevelItemCount()):
                out_it = self.tree.topLevelItem(i)
                if out_it.text(0) == k:
                    for j in range(out_it.childCount()):
                        ch_it = out_it.child(j)
                        ch_it.setText(1, str(v[ch_it.text(0)]))

class FuzzySimOutProgressBar(QProgressBar):
    def __init__(self,parent=None):
        super().__init__(parent)

    def setValue(self, val):
        try:
            super().setValue(int(val * 100))
        except ValueError:
            pass

class FuzzySimOutputTreeWidget(QTreeWidget):
    sig_input_changed = pyqtSignal(dict)

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setColumnCount(3)
        self.setHeaderHidden(True)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred)


class FuzzySimOutputTopTreeItem(QTreeWidgetItem):
    def __init__(self, bar, parent=None):
        super().__init__(parent)
        self.bar = bar
        # self.bar.valueChanged.connect(self._value_changed)

    def _value_changed(self):
        val = self.bar.value()
        for i in range(self.childCount()):
            self.child(i).set_var(val)

class FuzzySimOutputTreeItem(QTreeWidgetItem):
    def __init__(self,ling_var, parent=None):
        super().__init__(parent)
        self.ling_var = ling_var
        self.setText(0, self.ling_var.name)
        self.set_var(0)

    def set_var(self, val):
        self.setText(1, f'{val:.2f}')
