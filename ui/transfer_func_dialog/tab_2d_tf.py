#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QWidget, QFormLayout, QHBoxLayout, QComboBox,
                             QDoubleSpinBox, QPushButton,
                            QVBoxLayout, QLineEdit,
                             QRadioButton, QMessageBox, QSpinBox)

from .tf_plot import FuzzyTFPlot
from calculation import calculate, interpolate
import numpy as np
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from data import data

last_multiple = None
last_single = None
last_range = None

class FuzzyLogicTransferFunc2dTab(QWidget):
    def __init__(self, fuzzy_logic_element, parent=None):
        super().__init__(parent)
        self.logic_el = fuzzy_logic_element
        hbox = QHBoxLayout()
        v_box = QVBoxLayout()
        f_lay = QFormLayout()
        v_box.addLayout(f_lay)
        hbox.addLayout(v_box)
        self.setLayout(hbox)
        self.combobox = QComboBox()
        self.combobox.addItem(self.logic_el.in1.name)
        self.combobox.addItem(self.logic_el.in2.name)
        self.combobox.currentTextChanged.connect(self._on_combo_changed)
        f_lay.addRow('Static Input', self.combobox)

        self._check_static = QRadioButton('Static Input Value')
        self._check_static.clicked.connect(self._on_checkbox_checked)
        self.static_x = QDoubleSpinBox()
        self._check_multiple = QRadioButton('Multiple Input Values')
        self._check_multiple.clicked.connect(self._on_checkbox_checked)
        self._check_range = QRadioButton('Evenly Spread Values')
        self._check_range.setChecked(True)
        self._check_range.clicked.connect(self._on_checkbox_checked)
        self.multi_x = QLineEdit()
        self.range_x = QSpinBox()
        self.range_x.setRange(0, 10)
        self.range_x.setValue(5)

        f_lay.addRow(self._check_static, self.static_x)
        f_lay.addRow(self._check_multiple, self.multi_x)
        f_lay.addRow(self._check_range, self.range_x)
        self.static_x.setSingleStep(1)

        self.calc_btn = QPushButton('Calculate')
        v_box.addWidget(self.calc_btn)
        self.calc_btn.clicked.connect(self._calc)

        v_box2 = QVBoxLayout()
        self.plot = FuzzyTFPlot()
        self.nav_bar = NavigationToolbar2QT(self.plot)

        v_box2.addWidget(self.nav_bar)
        v_box2.addWidget(self.plot)
        hbox.addLayout(v_box2)

        self.setMinimumSize(600, 400)
        hbox.setStretchFactor(v_box2, 3)

        self._on_combo_changed()
        self._on_checkbox_checked()

        if last_multiple is not None:
            self.multi_x.setText(','.join([str(n) for n in last_multiple]))
        if last_range is not None:
            self.range_x.setValue(last_range)
        if last_single is not None:
            self.static_x.setValue(last_single)

    def _on_checkbox_checked(self):
        if self._check_static.isChecked():
            self._check_multiple.setChecked(False)
            self._check_range.setChecked(False)

        elif self._check_range.isChecked():
            self._check_multiple.setChecked(False)
            self._check_static.setChecked(False)

        elif self._check_multiple.isChecked():
            self._check_range.setChecked(False)
            self._check_static.setChecked(False)

    def _get_static_variable_input(self):
        cur_txt = self.combobox.currentText()
        if self.logic_el.in1.name == cur_txt:
            static = self.logic_el.in1
            variable = self.logic_el.in2
        else:
            static = self.logic_el.in2
            variable = self.logic_el.in1
        return static, variable

    def _eval_multi_static(self):
        txt = self.multi_x.text()
        try:
            spl = txt.split(',')
            vals = []
            for each in spl:
                t = each.strip()
                if t != '':
                    vals.append(float(t))

        except BaseException:
            msg = QMessageBox(QMessageBox.Icon.Critical, 'No.',
                'Shitty Input. Must be in form:\n 0, 2.5,4 ', parent=self)
            msg.exec()
            return None
        return vals

    def _on_combo_changed(self):
        stat_inp, _ = self._get_static_variable_input()
        self.static_x.setMinimum(stat_inp.ling_vars[0].x[0])
        self.static_x.setMaximum(stat_inp.ling_vars[0].x[-1])

    def _calc(self):
        global last_single, last_multiple, last_range

        stat_inp, var_inp = self._get_static_variable_input()

        min_x = var_inp.ling_vars[0].x[0]
        max_x = var_inp.ling_vars[0].x[-1]

        x_range = list(np.linspace(min_x, max_x, 100))

        glob_inf = data['logic_inference']
        data_d = {
            'inputs': {
                stat_inp.name: stat_inp,
                var_inp.name: var_inp,
            },
            'outputs': {
                self.logic_el.out.name: self.logic_el.out
            },
            'logic': [self.logic_el],
            'logic_inference': glob_inf}

        if self._check_static.isChecked():
            value = self.static_x.value()
            stat_vals = [value]
            last_single = value

        elif self._check_multiple.isChecked():
            value = self._eval_multi_static()
            if value is None:
                return
            else:
                stat_vals = value
                last_multiple = value

        elif self._check_range.isChecked():
            val_min = stat_inp.ling_vars[0].x[0]
            val_max = stat_inp.ling_vars[0].x[-1]
            r = val_max - val_min
            n_vals = self.range_x.value()
            dx = r / (n_vals - 1)
            stat_vals = [val_min + n * dx for n in range(n_vals)]
            last_range = n_vals
        else:
            return

        self.plot.clear()
        self.plot.prep(var_inp.name, self.logic_el.out.name)
        for value in stat_vals:
            stat_d = {n.name: interpolate(value, n.x, n.y) for n in
                      stat_inp.ling_vars}
            inp_d = {stat_inp.name: stat_d}
            out = []
            for x in x_range:
                var_d = {n.name: interpolate(x, n.x, n.y) for n in
                         var_inp.ling_vars}
                inp_d[var_inp.name] = var_d

                res = calculate(inp_d, data_d)# , verbose=True)
                out.append(res[self.logic_el.out.name])

            # self.plot.set_x_y(x_range, out, var_inp.name, self.logic_el.out.name)
            self.plot.add_line(x_range, out, f'static: {value:.2f}')

        self.plot.finish()