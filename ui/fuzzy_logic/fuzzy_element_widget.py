#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget,
                             QSizePolicy, QToolButton, QLabel, QComboBox)

from .fuzzy_element_tree import FuzzyElementsTreeWidget
from icons import icons
import data


class FuzzyLogicElementsWidget(QWidget):
    sig_new_item_created = pyqtSignal(object)
    sig_item_selection_changed = pyqtSignal(object)
    sig_item_changed = pyqtSignal(object, str)
    sig_item_destroyed = pyqtSignal(object)
    sig_invalid_selection = pyqtSignal()

    def __init__(self, inp_model, outp_model, parent=None):
        super().__init__(parent)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred)

        h_box = QHBoxLayout()
        self.name = QLabel('Fuzzy Logic Elements')
        h_box.addWidget(self.name)
        self.add_btn = QToolButton()
        self.add_btn.setIcon(QIcon(icons.plus))
        self.remove_btn = QToolButton()
        self.remove_btn.setIcon(QIcon(icons.minus))
        h_box.addWidget(self.add_btn)
        h_box.addWidget(self.remove_btn)

        v_box = QVBoxLayout()
        v_box.addLayout(h_box)

        self.inp_model = inp_model
        self.outp_model = outp_model

        self.table = FuzzyElementsTreeWidget(inp_model, outp_model)
        v_box.addWidget(self.table)

        h_box = QHBoxLayout()
        h_box.addWidget(QLabel('Elements Logic'))
        self.element_logic_combo = QComboBox()
        h_box.addWidget(self.element_logic_combo)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

        self.add_btn.clicked.connect(self._add_new_item)
        self.remove_btn.clicked.connect(self._remove_item)
        self.table.sig_fuzzy_logic_changed.connect(self._logic_elem_change)
        self.table.sig_no_selection.connect(self._on_invalid_sel)
        self.element_logic_combo.currentIndexChanged.connect(
            self._on_logic_inference_change)

        self._inference_model = None

    def _on_logic_inference_change(self):
        txt = self.element_logic_combo.currentText()
        data.data['logic_inference'] = txt
    @property
    def inference_model(self):
        return self._inference_model

    @inference_model.setter
    def inference_model(self, value):
        self._inference_model = value
        self.element_logic_combo.setModel(self._inference_model)
        self.table.inference_model = value

    def clear(self):
        self.table.clear()

    def add_element(self, logic_element):
        self.table.add_existing_element(logic_element)

    def fuzzy_var_name_changed(self, old_lbl, new_lbl):
        self.table.fuzzy_var_name_changed(old_lbl, new_lbl)

    def _logic_elem_change(self, fz):
        self.sig_item_selection_changed.emit(fz)

    def _on_invalid_sel(self):
        self.sig_invalid_selection.emit()

    def add_initial(self, in1, in2, out):
        self.table.add_initial(in1, in2, out)

    def _add_new_item(self):
        self.table.add_new_fz_logic()

    def _remove_item(self):
        self.table.remove_selected_fz_logic()
