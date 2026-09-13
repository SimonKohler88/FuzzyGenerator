#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QBrush, QGradient, QPixmap
from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget, QGroupBox,
                             QSizePolicy, QDialog, QSplitter, QFrame,
                             QSplitterHandle)

from .plot_widget import UIInputLingVarEditWidget
from .list_widget import ListWidget
# from ui.fuzzy_logic_widget.fuzzy_logic import FuzzyLogicWidget

from ui.fuzzy_logic.fuzzy_logic_widget import FuzzyLogicWidget

import data
from .simulation_dialog import FuzzyLogicSimulatorDialog
from .my_splitter import MySplitter


class Ui_Base(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._splitter_h = MySplitter(Qt.Orientation.Horizontal)
        
        self.in_out_groupbox = QGroupBox()
        self.in_out_groupbox.setSizePolicy(QSizePolicy.Policy.Preferred,
                                           QSizePolicy.Policy.Preferred)
        v_box_g = QVBoxLayout()
        self.in_out_groupbox.setTitle('Fuzzyfication/Defuzzyfication')
        self.in_out_groupbox.setLayout(v_box_g)
        self._splitter_h.addWidget(self.in_out_groupbox)
        self._splitter_v = MySplitter(Qt.Orientation.Vertical)
        self._splitter_h.addWidget(self._splitter_v)
        
        self.inputs = ListWidget('Inputs')
        self.inputs.sig_item_selection_changed.connect(
            self._input_item_sel_changed)
        self.inputs.sig_item_destroyed.connect(self._input_item_destroyed)
        self.inputs.sig_new_item_created.connect(self._input_item_created)
        self.inputs.sig_item_changed.connect(self._input_item_changed)
        
        v_box_g.addWidget(self.inputs)
        
        self.outputs = ListWidget(label='Outputs')
        self.outputs.sig_item_selection_changed.connect(
            self._output_item_sel_changed)
        self.outputs.sig_item_destroyed.connect(self._output_item_destroyed)
        self.outputs.sig_new_item_created.connect(self._output_item_created)
        self.outputs.sig_item_changed.connect(self._output_item_changed)
        
        v_box_g.addWidget(self.outputs)
        
        h_box = QHBoxLayout()
        h_box.addWidget(self._splitter_h)
        
        self.ling_var_editor = UIInputLingVarEditWidget()
        self.ling_var_editor.sig_ling_var_name_changed.connect(self._lin_var_name_change)
        self.ling_var_editor.sig_ling_var_destroyed.connect(
            self._lin_var_destroyed)
        self.ling_var_editor.sig_ling_var_created.connect(
            self._lin_var_created)
        self.ling_var_editor.sig_ling_var_order_changed.connect(
            self._lin_var_order_changed
        )
        self._splitter_v.addWidget(self.ling_var_editor)
        
        self.fuzzy_logic = FuzzyLogicWidget(
            self.inputs.model(),
            self.outputs.model())
        
        self._splitter_v.addWidget(self.fuzzy_logic)
        # v_box.addWidget(self.fuzzy_logic)
        
        for i in range(1):
            name = f'Output {i}'
            fv = data.add_generic_fuzzy_var(name, isinput=False)
            self.add_output(fv, name)
        
        for i in range(2):
            name = f'Input {i}'
            fv = data.add_generic_fuzzy_var(name)
            self.add_input(fv, name)
        
        self.fuzzy_logic.add_initial_logic_element('Input 0', 'Input 1',
                                                   'Output 0')
        
        # h_box.addLayout(v_box)
        self.setLayout(h_box)
    
    def clear_all(self):
        self.inputs.clear()
        self.outputs.clear()
        self.fuzzy_logic.clear()
        self.ling_var_editor.clear()
        self.outputs.disallowed_labels = []
        self.inputs.disallowed_labels = []
    
    def add_input(self, fv, name):
        self.inputs.add_item(fv, new_name=name)
        self.outputs.disallowed_labels.append(name)
    
    def add_output(self, fv, name):
        self.outputs.add_item(fv, new_name=name)
        self.inputs.disallowed_labels.append(name)
    
    def add_logic_element(self, logic_el):
        self.fuzzy_logic.add_logic_element(logic_el)
    
    def _lin_var_order_changed(self):
        self.fuzzy_logic.reload_table()
    
    def _lin_var_created(self):
        self.fuzzy_logic.reload_table()
    
    def _lin_var_destroyed(self, fz_name, lbl):
        self.fuzzy_logic.reload_table()
    
    def _lin_var_name_change(self, new_lbl, old_lbl):
        self.fuzzy_logic.update_ling_vars(new_lbl, old_lbl)
    
    def _input_item_changed(self, it, old_name):
        it.user_storage.name = it.text()
        self.outputs.disallowed_labels.remove(old_name)
        self.outputs.disallowed_labels.append(it.text())
        self.ling_var_editor.update_current_name()
        data.change_fuzzy_var_name(old_name, it.text())
        self.fuzzy_logic.fuzzy_var_name_changed(old_name, it.text())
    
    def _input_item_destroyed(self, it):
        lbl = it.text()
        data.remove_fuzzy_var(lbl)
        self.outputs.disallowed_labels.remove(lbl)
    
    def _input_item_created(self, it):
        name = it.text()
        fv = data.add_generic_fuzzy_var(name)
        it.user_storage = fv
        self.outputs.disallowed_labels.append(name)
    
    def _input_item_sel_changed(self, it):
        self.outputs.unselect()
        self.ling_var_editor.set_fuzzy_var(it.user_storage)
    
    def _output_item_changed(self, it, old_name):
        it.user_storage.name = it.text()
        self.inputs.disallowed_labels.remove(old_name)
        self.inputs.disallowed_labels.append(it.text())
        self.ling_var_editor.update_current_name()
        data.change_fuzzy_var_name(old_name, it.text())
        self.fuzzy_logic.fuzzy_var_name_changed(old_name, it.text())
    
    def _output_item_destroyed(self, it):
        lbl = it.text()
        data.remove_fuzzy_var(lbl, isinput=False)
        self.inputs.disallowed_labels.remove(lbl)
    
    def _output_item_created(self, it):
        name = it.text()
        fv = data.add_generic_fuzzy_var(name, isinput=False)
        it.user_storage = fv
        self.inputs.disallowed_labels.append(name)
    
    def _output_item_sel_changed(self, it):
        self.inputs.unselect()
        self.ling_var_editor.set_fuzzy_var(it.user_storage)
    
    def simulate(self):
        d = FuzzyLogicSimulatorDialog(parent=self)
        result = d.exec()
        if result == QDialog.DialogCode.Accepted:
            pass
