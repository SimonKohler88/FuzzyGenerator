#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pprint

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QTableWidget, QAbstractItemView, QTableWidgetItem,
                             QAbstractScrollArea)

import icons


class FuzzyLogicTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.horin = None
        self.vertin = None
    
    def update_header_labels(self):
        if self.horin is not None:
            hr_labels = [lv.name for lv in self.horin.ling_vars]
            self.setHorizontalHeaderLabels(hr_labels)
        if self.vertin is not None:
            hr_labels = [lv.name for lv in self.vertin.ling_vars]
            self.setVerticalHeaderLabels(hr_labels)
    
    def set_fuzzy_element(self, fz):
        self.clear()
        
        self.horin = fz.in1
        self.vertin = fz.in2
        
        self.setRowCount(len(self.vertin))
        self.setColumnCount(len(self.horin))
        
        self.update_header_labels()
        
        for row, col, el, inf in fz.iterator():
            it = QTableWidgetItem(el)
            ic = icons.icons.and_pic if inf == 'min' else icons.icons.or_pic
            it.setIcon(QIcon(ic))
            self.setItem(row, col, it)
    
    def setSelected(self, txt, fz):
        sel = self.selectedIndexes()
        print(sel)
        
        for each in sel:
            r = each.row()
            c = each.column()
            
            it = self.item(r, c)
            it.setText(txt)
            
            if fz.in1 != self.horin:
                r = each.column()
                c = each.row()
            
            fz.logic[r][c] = txt
    
    def setSelectedInference(self, txt, fz):
        sel = self.selectedIndexes()
        for each in sel:
            r = each.row()
            c = each.column()
            
            it = self.item(r, c)
            ic = icons.icons.and_pic if txt == 'Min' else icons.icons.or_pic
            it.setIcon(QIcon(ic))
            
            if fz.in1 != self.horin:
                r = each.column()
                c = each.row()
            
            fz.logic_inference[r][c] = txt.lower()
