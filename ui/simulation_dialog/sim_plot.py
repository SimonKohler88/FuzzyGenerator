#!/usr/bin/python3
# -*- coding: utf-8 -*-


import numpy as np
from PyQt6.QtWidgets import QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, \
    QToolButton, QFormLayout, QListWidget, QListWidgetItem, QFrame, QLineEdit, \
    QLabel, QSpinBox, QFrame, QGroupBox, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal

from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class FuzzySimPlotList(QWidget):
    def __init__(self, in_out_dict, parent=None):
        super().__init__(parent)
        self._dummy_w = QWidget()
        self._scroll = QScrollArea()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.addWidget(self._scroll)
        g_grid = QGridLayout()
        self._dummy_w.setLayout(g_grid)

        self.plots = {}

        i = 0
        for k, v in in_out_dict.items():
            pl = FuzzySimPlot(v)
            self.plots[k] = pl
            g_grid.addWidget(QLabel(k), i, 0)
            g_grid.addWidget(pl, i, 1)
            i += 1

        self._scroll.setWidget(self._dummy_w)

    def set_value(self, valdict):
        for k, v in valdict.items():
            self.plots[k].set_v_line(v)


class FuzzySimPlot(FigureCanvas):
    def __init__(self, fuzzy_var, parent=None, width=2, height=1,
            dpi=100):
        # matplotlib figure initialising
        self.fig = Figure(figsize=(width, height), dpi=dpi)

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
        self.axes.set_ylim(-0.1, 1.1)
        self.axes.set(yticklabels=[])
        self.axes.set(xticklabels=[])
        # self.axes.set_xlim(min(x), max(x))

        self.v_line = self.axes.axvline(0, color='r')
        for each in fuzzy_var.ling_vars:
            self.axes.plot(each.x, each.y, label=each.name)
        self.area = None
        self.axes.grid()

    def set_v_line(self, x_val):
        self.v_line.set_xdata([x_val])
        self.fig.canvas.draw_idle()

    def set_area(self, dt):
        if self.area is not None:
            self.area.remove()
        self.area = self.axes.fill_between(dt['x'], dt['y'], color='C7',
            alpha=0.5)
        self.fig.canvas.draw_idle()
