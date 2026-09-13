#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, \
    QToolButton, QFormLayout, QListWidget, QListWidgetItem, QFrame, QLineEdit, \
    QLabel, QSpinBox, QFrame, QGroupBox, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal

from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.cm as cm
import numpy as np


class FuzzyTFHeightPlot(FigureCanvas):
    def __init__(self, x, y, z, x_label, y_label, z_label, parent=None, w_h=2,
            dpi=100):
        # matplotlib figure initialising
        self.fig = Figure(figsize=(w_h, w_h), dpi=dpi)

        # Qt5-Backend
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)
        # set some Qt-Things
        self.setParent(parent)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setFocus()

        # Make the Plot
        self.axes = self.fig.add_subplot(1, 1, 1)

        min_z = z.min()
        max_z = z.max()
        levels = np.linspace(min_z, max_z, 20)

        cont = self.axes.contourf(x, y, z, cmap=cm.RdBu_r,
            linestyles="solid", levels=levels)

        col_b = self.fig.colorbar(cont, fraction=0.046, pad=0.04)
        for each in levels:
            col_b.ax.axhline(each, color='k')
        col_b.ax.set_ylabel(z_label)
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)

    def finish(self):
        self.fig.tight_layout()
        self.fig.canvas.draw_idle()

    def resizeEvent(self, event):
        self.finish()
        super().resizeEvent(event)
