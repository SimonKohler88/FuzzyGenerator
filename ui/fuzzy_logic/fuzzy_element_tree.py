#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import (pyqtSignal, Qt, QObject)
from PyQt6.QtGui import (QAction)
from PyQt6.QtWidgets import (QSizePolicy, QAbstractScrollArea, QMenu,
                             QDialog, QTreeWidgetItem, QTreeWidget,
                             QMessageBox, QComboBox)

from .fuzzy_element_dialog import NewFuzzyElementDialog
import data


class FuzzyElementsTreeWidget(QTreeWidget):
    sig_fuzzy_logic_changed = pyqtSignal(object)
    sig_no_selection = pyqtSignal()
    
    def __init__(self, inp_mod, outp_mod, parent=None, *args, **kw):
        super().__init__(parent)
        self.setColumnCount(4)
        
        # self.header().stretchLastSection()
        self.setHeaderLabels(['Output', 'Input A', 'Input B',
                              'Output Inference'])
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Preferred)
        self.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        
        self.inp_mod = inp_mod
        self.outp_mod = outp_mod
        
        self.setSortingEnabled(True)
        
        self.element_contx_menu = QMenu()
        self.ac_add_element = QAction('Add Logic Element')
        self.ac_add_element.triggered.connect(self.add_new_fz_logic)
        self.ac_remove_element = QAction('Remove Logic Element')
        self.ac_remove_element.triggered.connect(self.remove_selected_fz_logic)
        
        self.acExpandAll = QAction('Expand All')
        self.acExpandAll.triggered.connect(self.on_expand_all)
        self.acCollapseAll = QAction('Collapse All')
        self.acCollapseAll.triggered.connect(self.on_collapse_all)
        
        self.element_actions = [self.ac_add_element, self.ac_remove_element]
        self.tree_actions = [self.acExpandAll, self.acCollapseAll]
        
        for i, lst in enumerate([self.element_actions]):
            for each in lst:
                self.element_contx_menu.addAction(each)
        
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__context_menu)
        self.itemSelectionChanged.connect(self._item_sel_changed)
        
        self._inference_model = None
    
    @property
    def inference_model(self):
        return self._inference_model
    
    @inference_model.setter
    def inference_model(self, value):
        self._inference_model = value
    
    def add_existing_element(self, logic_el):
        # for repopulating after reloading
        in1 = logic_el.in1.name
        in2 = logic_el.in2.name
        out = logic_el.out.name
        it = self._make_and_add_new_top_level_item(in1, in2, out)
        it.inf_combo.setCurrentText(logic_el.out_inference)
    
    def fuzzy_var_name_changed(self, old_lbl, new_lbl):
        for idx in range(self.topLevelItemCount()):
            it = self.topLevelItem(idx)
            
            in1 = it.text(1)
            in2 = it.text(2)
            out = it.text(0)
            
            if in1 == old_lbl:
                it.setText(1, new_lbl)
                continue
            if in2 == old_lbl:
                it.setText(2, new_lbl)
                continue
            if out == old_lbl:
                it.setText(0, new_lbl)
    
    def _item_sel_changed(self, *args):
        ind = self.currentIndex()
        it = self.itemFromIndex(ind)
        if it is None:
            self.sig_no_selection.emit()
            return
        in1 = it.text(1)
        in2 = it.text(2)
        out = it.text(0)
        fz = data.get_fuzzy_logic_element(in1, in2, out)
        self.sig_fuzzy_logic_changed.emit(fz)
    
    def on_expand_all(self):
        for idx in range(self.topLevelItemCount()):
            self.topLevelItem(idx).setExpanded(True)
    
    def on_collapse_all(self):
        for idx in range(self.topLevelItemCount()):
            self.topLevelItem(idx).setExpanded(False)
    
    def remove_selected_fz_logic(self):
        if self.topLevelItemCount() == 1:
            msg = QMessageBox(QMessageBox.Icon.Critical, 'No.',
                              'Cannot Remove last Logic Element', parent=self)
            msg.exec()
            return
        ind = self.currentIndex()
        it = self.itemFromIndex(ind)
        it.signals.sig_current_text_changed.disconnect()
        out = it.text(0)
        in1 = it.text(1)
        in2 = it.text(2)
        self.takeTopLevelItem(ind.row())
        data.remove_fuzzy_logic(in1, in2, out)
    
    def _on_inference_changed(self, it):
        # Not Firing multiple times
        out = it.text(0)
        in1 = it.text(1)
        in2 = it.text(2)
        fz = data.get_fuzzy_logic_element(in1, in2, out)
        print('_on_inference_changed  0:' , fz.out_inference)
        # it.signals.blockSignals(True)
        fz.out_inference = it.inf_combo.currentText()
        print('_on_inference_changed  1:' , fz.out_inference)
    
    def _make_and_add_new_top_level_item(self, in1, in2, out):
        # Not Firing multiple times
        it = LogicElementTopTreeItem()
        # it.signals.blockSignals(True)
        it.setText(0, out)
        it.setText(1, in1)
        it.setText(2, in2)
        # it.signals.blockSignals(False)
        it.inf_combo.setModel(self._inference_model)
        it.signals.sig_current_text_changed.connect(self._on_inference_changed)
        
        self.addTopLevelItem(it)
        self.setItemWidget(it, 3, it.inf_combo)
        self.setCurrentItem(it)
        return it
    
    def add_initial(self, in1, in2, out):
        fz = data.add_fuzzy_logic(in1, in2, out)
        fz.logic = [['High', 'High', 'Mid'],
                    ['High', 'Mid', 'Low'],
                    ['Mid', 'Low', 'Low']]
        
        it = self._make_and_add_new_top_level_item(in1, in2, out)
        it.inf_combo.setCurrentText(fz.out_inference)
    
    def add_new_fz_logic(self):
        pairs = data.get_existing_logic_pairings()
        d = NewFuzzyElementDialog(self.inp_mod, self.outp_mod,
                                  pairs, parent=self)
        result = d.exec()
        if result == QDialog.DialogCode.Accepted:
            in1 = d.inp1.currentText()
            in2 = d.inp2.currentText()
            out = d.out.currentText()
            #TODO: new element always with output inf == Min
            # --> make standard Max and disable output inference
            fz = data.add_fuzzy_logic(in1, in2, out)
            it = self._make_and_add_new_top_level_item(in1, in2, out)
            it.signals.blockSignals(True)
            print(fz.out_inference)
            it.inf_combo.setCurrentText(fz.out_inference)
            it.signals.blockSignals(False)
            return it
    
    def __context_menu(self, e):
        item = self.itemAt(e)
        if item is None:
            self.element_contx_menu.exec(self.mapToGlobal(e))
            return
        self.setCurrentItem(item)
        if item.parent() is None:
            self.element_contx_menu.exec(self.mapToGlobal(e))


class Signals(QObject):
    sig_current_text_changed = pyqtSignal(object)


class LogicElementTopTreeItem(QTreeWidgetItem):
    signals = Signals()
    
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.inf_combo = QComboBox()
        self.inf_combo.currentTextChanged.connect(self._on_combo_changed)
        self.inf_combo.setEnabled(False)
    
    def _on_combo_changed(self):
        print('on inf changed:', self.inf_combo.currentText())
        self.signals.sig_current_text_changed.emit(self)
