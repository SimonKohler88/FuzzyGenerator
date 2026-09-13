#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QDialog, QTabWidget, QHBoxLayout)

from .tab_2d_tf import FuzzyLogicTransferFunc2dTab
from .tab_3d_tf import FuzzyLogicTransferFunc3dTab
from .tab_heigh_tf import FuzzyLogicTransferFuncHeightTab


class FuzzyLogicTransferFuncDialog(QDialog):
    def __init__(self, fuzzy_logic_element, parent=None):
        super().__init__(parent)
        self.logic_el = fuzzy_logic_element
        self.tab = QTabWidget()

        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(self.tab)

        self.tf_2d_tab = FuzzyLogicTransferFunc2dTab(self.logic_el)
        self.tab.addTab(self.tf_2d_tab, '2d Transfer Function')

        self.tf_3d_tab = FuzzyLogicTransferFunc3dTab(self.logic_el)
        self.tab.addTab(self.tf_3d_tab, '3d Transfer Function')

        x = self.tf_3d_tab.X
        y = self.tf_3d_tab.Y
        z = self.tf_3d_tab.Z
        x_label = self.logic_el.in1.name
        y_label = self.logic_el.in2.name
        z_label = self.logic_el.out.name
        self.tf_heat_tab = FuzzyLogicTransferFuncHeightTab(x, y, z, x_label,
            y_label, z_label)

        self.tab.addTab(self.tf_heat_tab, 'Height Map')
