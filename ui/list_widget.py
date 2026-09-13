#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout,
                             QWidget, QListWidget, QInputDialog,
                             QLabel, QToolButton, QListWidgetItem,
                             QSizePolicy, QAbstractItemView, QMessageBox)

from icons.icons import icons


class ListWidget(QWidget):
    sig_new_item_created = pyqtSignal(object)
    sig_item_selection_changed = pyqtSignal(object)
    sig_item_changed = pyqtSignal(object, str)
    sig_item_destroyed = pyqtSignal(object)
    sig_item_order_changed = pyqtSignal(int, int)

    def __init__(self, label='NoLabel', parent=None):
        super().__init__(parent)

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred)

        h_box = QHBoxLayout()
        self.name = QLabel(label)
        h_box.addWidget(self.name)
        self.add_btn = QToolButton()
        self.add_btn.setIcon(QIcon(icons.plus))
        self.remove_btn = QToolButton()
        self.remove_btn.setIcon(QIcon(icons.minus))
        h_box.addWidget(self.add_btn)
        h_box.addWidget(self.remove_btn)

        v_box = QVBoxLayout()
        v_box.addLayout(h_box)

        self.list = QListWidget()
        self.list.setSizePolicy(QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred)
        v_box.addWidget(self.list)

        self.setLayout(v_box)

        self.add_btn.clicked.connect(self._add_item_with_textbox)
        self.remove_btn.clicked.connect(self._remove_item)
        self.list.itemDoubleClicked.connect(self._on_dbl_click)
        self.list.itemSelectionChanged.connect(self._curr_sel_change)
        self.list.model().rowsMoved.connect(self._drop_event)
        self.list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)

        self.disallowed_labels = []

    def _drop_event(self, s_par, s_row_start, s_row_end, d_par, d_row):
        self.sig_item_order_changed.emit(s_row_start, d_row)

    def model(self):
        return self.list.model()

    def _curr_sel_change(self):
        it = self.list.currentItem()
        self.sig_item_selection_changed.emit(it)

    def _check_name(self, name):
        allowed = True
        if name.strip() in self.disallowed_labels:
            allowed = False
        for i in range(self.list.count()):
            if self.list.item(i).text() == name.strip():
                allowed = False

        if not allowed:
            msg = QMessageBox(QMessageBox.Icon.Critical, 'No.',
                'Name Already exists', parent=self)
            msg.exec()
            return False
        return True

    def _on_dbl_click(self, it):
        old_name = it.text()
        new, ok = QInputDialog.getText(self, self.name.text(), 'New Label',
            text=it.text())
        if ok:
            new = new.strip()
            if self._check_name(new):
                it.setText(new)
                self.sig_item_changed.emit(it, old_name)

    def _add_item_with_textbox(self):
        it = ListItem('New Item')
        new, ok = QInputDialog.getText(self, self.name.text(), 'New Label',
            text=it.text())
        if ok:
            new = new.strip()
            if not self._check_name(new):
                return

            it.setText(new)

        self.list.addItem(it)
        self.sig_new_item_created.emit(it)
        self.list.setCurrentItem(it)

    def add_item(self, *args, new_name=None):
        it = ListItem('New Item')
        it.setText(new_name)
        it.user_storage = args[0]
        self.list.addItem(it)
        # self.sig_new_item_created.emit(it)

    def add_qitem(self, it):
        self.list.addItem(it)

    def _remove_item(self):
        sel = self.list.selectedItems()
        for each in sel:
            it = self.list.takeItem(self.list.row(each))
            self.sig_item_destroyed.emit(it)

    def clear(self):
        self.list.blockSignals(True)
        self.list.clear()
        self.list.blockSignals(False)

    def unselect(self):
        self.list.blockSignals(True)
        self.list.clearSelection()
        self.list.blockSignals(False)


class ListItem(QListWidgetItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_storage = None
