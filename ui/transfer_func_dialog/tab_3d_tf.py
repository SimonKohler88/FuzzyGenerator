#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QWidget, QVBoxLayout)

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from ui.transfer_func_dialog.tf_3d_plot import FuzzyTF3dPlot
from calculation import calculate, interpolate
import numpy as np

from data import FuzzyLogicElement, data


class FuzzyLogicTransferFunc3dTab(QWidget):
    def __init__(self, fuzzy_logic_element: FuzzyLogicElement, parent=None):
        super().__init__(parent)
        self.logic_el = fuzzy_logic_element
        vbox = QVBoxLayout()

        self.setLayout(vbox)

        self.plot = FuzzyTF3dPlot()
        self.nav_bar = NavigationToolbar2QT(self.plot)
        vbox.addWidget(self.nav_bar)
        vbox.addWidget(self.plot)
        self.setMinimumSize(600, 400)

        self.X = None
        self.Y = None
        self.Z = None
        self._calc()

    def _calc(self):

        inp1 = self.logic_el.in1
        min_1 = inp1.ling_vars[0].x[0]
        max_1 = inp1.ling_vars[0].x[-1]
        x_range_1 = list(np.linspace(min_1, max_1, 50))

        inp2 = self.logic_el.in2
        min_2 = inp2.ling_vars[0].x[0]
        max_2 = inp2.ling_vars[0].x[-1]
        x_range_2 = list(np.linspace(min_2, max_2, 50))

        glob_inf = data['logic_inference']
        data_d = {
            'inputs': {
                inp1.name: inp1,
                inp2.name: inp2,
            },
            'outputs': {
                self.logic_el.out.name: self.logic_el.out
            },
            'logic': [self.logic_el],
            'logic_inference': glob_inf}

        self.plot.prep(inp1.name, inp2.name, self.logic_el.out.name)
        self.X, self.Y = np.meshgrid(x_range_1, x_range_2)
        self.Z = np.zeros(self.X.shape)

        for i, x_val1 in enumerate(x_range_1):
            inp1_d = {n.name: interpolate(x_val1, n.x, n.y) for n in
                      inp1.ling_vars}
            inp_d = {inp1.name: inp1_d}
            out = []
            for j, x_val2 in enumerate(x_range_2):
                var_d = {n.name: interpolate(x_val2, n.x, n.y) for n in
                         inp2.ling_vars}
                inp_d[inp2.name] = var_d

                res = calculate(inp_d, data_d)  # , verbose=True)
                self.Z[i][j] = res[self.logic_el.out.name]
                out.append(res[self.logic_el.out.name])

        self.plot.set_surface(self.X, self.Y, self.Z)

        self.plot.finish()
