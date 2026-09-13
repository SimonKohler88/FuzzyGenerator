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


class FuzzyTF3dPlot(FigureCanvas):
    def __init__(self, parent=None, w_h=2,
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
        self.axes = self.fig.add_subplot(1, 1, 1, projection='3d')
        self.axes.grid()

    def prep(self, x_label, y_label, z_label):
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.axes.set_zlabel(z_label)

    def finish(self):
        self.fig.tight_layout()
        self.fig.canvas.draw_idle()

    def set_surface(self, x, y, z):
        min_z = z.min()
        max_z = z.max()
        levels = np.linspace(min_z, max_z, 12)
        ln = self.axes.plot_surface(x, y, z, cmap=cm.RdBu_r, alpha=0.9)
        cont = self.axes.contour(x, y, z, colors='k',
            linestyles="solid", levels=levels)
        col_b = self.fig.colorbar(ln, fraction=0.046, pad=0.15)
        col_b.add_lines(cont)

    def resizeEvent(self, event):
        self.fig.tight_layout()
        self.fig.canvas.draw_idle()
        super().resizeEvent(event)
