#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, \
    QToolButton, QFormLayout, QListWidget, QListWidgetItem, QFrame, QLineEdit, \
    QLabel, QSpinBox, QFrame, QGroupBox, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal

from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class FuzzyTFPlot(FigureCanvas):
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
        self.axes = self.fig.add_subplot(1, 1, 1)
        self._x_min = None
        self._y_min = None
        self._x_max = None
        self._y_max = None

        self.axes.grid()

    def prep(self, x_label, y_label):
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)

    def finish(self):
        self.axes.set_ylim(self._y_min, self._y_max * 1.1)
        self.axes.set_xlim(self._x_min, self._x_max)
        self.axes.legend()
        self.fig.tight_layout()
        self.fig.canvas.draw_idle()

    def add_line(self, x, y, label):
        if self._x_min is None:
            self._x_min = min(x)
        else:
            self._x_min = min(self._x_min, min(x))

        if self._y_min is None:
            self._y_min = min(y)
        else:
            self._y_min = min(self._y_min, min(y))

        if self._x_max is None:
            self._x_max = max(x)
        else:
            self._x_max = max(self._x_max, max(x))

        if self._y_max is None:
            self._y_max = max(y)
        else:
            self._y_max = max(self._y_max, max(y))

        self.axes.plot(x, y, label=label)

    def remove_line(self, label):
        for each in list(self.axes.lines):
            if each.get_label() == label:
                each.remove()

    def clear(self):
        for each in self.axes.lines:
            self.remove_line(each.get_label())
        self.axes.set_prop_cycle(None)
