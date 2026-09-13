#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QWidget, QVBoxLayout)

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from ui.transfer_func_dialog.tf_height_plot import FuzzyTFHeightPlot


class FuzzyLogicTransferFuncHeightTab(QWidget):
    def __init__(self, x, y, z, x_label, y_label, z_label, parent=None):
        super().__init__(parent)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        self.plot = FuzzyTFHeightPlot(x, y, z, x_label, y_label, z_label)
        self.nav_bar = NavigationToolbar2QT(self.plot)
        vbox.addWidget(self.nav_bar)
        vbox.addWidget(self.plot)
        self.setMinimumSize(600, 400)

        self.plot.finish()


