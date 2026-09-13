#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Date: 24.01.2024
Author: S_Kohler
"""
import os
import pprint
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QWidget, QFrame, QComboBox, QGridLayout,
                             QVBoxLayout,
                             QTableWidget, QTableWidgetItem, QLabel, QGroupBox,
                             QListWidget, QAbstractItemView, QSizePolicy,
                             QHBoxLayout, QPushButton, QListWidgetItem,
                             QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal

from .fuzzy_logic_table import FuzzyLogicTable
from .fuzzy_element_widget import FuzzyLogicElementsWidget
from ui.transfer_func_dialog import FuzzyLogicTransferFuncDialog
import icons
# from ..list_widget import ListItem
from ui.my_splitter import MySplitter


class FuzzyLogicWidget(QGroupBox):
    def __init__(self, inp_model, outp_model, parent=None):
        super().__init__(parent)
        
        self.setTitle('Fuzzy Logic')
        lay = QHBoxLayout()
        self.setLayout(lay)
        
        self._splitter_h = MySplitter(Qt.Orientation.Horizontal)
        lay.addWidget(self._splitter_h)
        
        self.fuzzy_elements = FuzzyLogicElementsWidget(inp_model, outp_model)
        self._splitter_h.addWidget(self.fuzzy_elements)
        # lay.addWidget(self.fuzzy_elements)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        self.out_label = QLabel('Output')
        self.out_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.out_label.setMinimumWidth(80)
        
        self.hor_label = QLabel('Input A')
        self.hor_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.vert_label = QLabel('Input B')
        self.vert_label.setAlignment(Qt.AlignmentFlag.AlignRight |
                                     Qt.AlignmentFlag.AlignVCenter)
        
        self._table_container = QWidget()
        g_lay = QGridLayout()
        g_lay.addWidget(self.out_label, 0, 0)
        g_lay.addWidget(self.hor_label, 0, 1)
        g_lay.addWidget(self.vert_label, 1, 0)
        
        self.table = FuzzyLogicTable()
        g_lay.addWidget(self.table, 1, 1)
        self._table_container.setLayout(g_lay)
        self._splitter_h.addWidget(self._table_container)
        # lay.addLayout(g_lay)
        
        self._out_container = QWidget()
        self._out_container.setFixedWidth(150)
        v_box = QVBoxLayout()
        self._out_container.setLayout(v_box)
        self._splitter_h.addWidget(self._out_container)
        # lay.addLayout(v_box)
        out_var_lbl = QLabel('Output Vars')
        out_var_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        v_box.addWidget(out_var_lbl)
        
        self.ling_var_list = QListWidget()
        self.ling_var_list.setFixedWidth(150)
        v_box.addWidget(self.ling_var_list)
        
        self.ling_var_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        
        self.inference_list = QListWidget()
        self.inference_list.setFixedWidth(150)
        self.inference_list.setFixedHeight(50)
        self.inference_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        
        v_box.addWidget(self.inference_list)
        self.tf_btn = QPushButton('Transfer Function')
        v_box.addWidget(self.tf_btn)
        
        self.ling_var_list.itemClicked.connect(self._ling_var_item_clicked)
        self.fuzzy_elements.sig_invalid_selection.connect(self.clear)
        self.fuzzy_elements.sig_item_selection_changed.connect(
            self.load_logic_element)
        self.tf_btn.clicked.connect(self._on_tf)
        
        self.inference_list.itemClicked.connect(self._inference_item_clicked)
        
        self.inference_list_choices = [[icons.icons.and_pic, 'Min'],
                                       [icons.icons.or_pic, 'Max']]
        for ic, nm in self.inference_list_choices:
            it = QListWidgetItem(nm)
            it.setIcon(QIcon(ic))
            self.inference_list.addItem(it)
        
        self.fuzzy_elements.inference_model = self.inference_list.model()
        self._current_fzzy_el = None
    
    def reload_table(self):
        self._current_fzzy_el.reevaluate_matrix()
        self.load_logic_element(self._current_fzzy_el)
    
    def _on_tf(self):
        if self._current_fzzy_el is None:
            return
        dia = FuzzyLogicTransferFuncDialog(self._current_fzzy_el)
        dia.exec()
    
    def add_initial_logic_element(self, in1, in2, out):
        # for initial display of 1 element
        self.fuzzy_elements.add_initial(in1, in2, out)
    
    def fuzzy_var_name_changed(self, old_lbl, new_lbl):
        self.fuzzy_elements.fuzzy_var_name_changed(old_lbl, new_lbl)
    
    def add_logic_element(self, le):
        self.fuzzy_elements.add_element(le)
    
    def load_logic_element(self, fz):
        self._current_fzzy_el = fz
        self.table.set_fuzzy_element(fz)
        self.ling_var_list.clear()
        lst = ['None']
        lst.extend([lv.name for lv in fz.out.ling_vars])
        out_ling = lst
        self.ling_var_list.addItems(out_ling)
    
    def update_ling_vars(self, new_lbl, old_lbl):
        if self._current_fzzy_el is None:
            print('No fuzzy Element to update')
            return
        print('Update Vars')
        self._current_fzzy_el.update_matrix_names(new_lbl, old_lbl)
        self.table.update_header_labels()
    
    def clear(self):
        self._current_fzzy_el = None
        self.table.clear()
        self.fuzzy_elements.clear()
        self.ling_var_list.clear()
    
    def _ling_var_item_clicked(self, it):
        txt = it.text()
        self.table.setSelected(txt, self._current_fzzy_el)
    
    def _inference_item_clicked(self, it):
        txt = it.text()
        self.table.setSelectedInference(txt, self._current_fzzy_el)
