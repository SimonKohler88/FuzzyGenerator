#!/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = '1.0.0'

import os
import pprint
import sys

from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenuBar,
                             QFileDialog)
from PyQt6.QtGui import QKeySequence, QAction

from ui.uibasic import Ui_Base

#  Workaround to show correct Icon in Taskbar
import ctypes
import data
import save_reload
import exporters
import json

myappid = 'FuzzyCtrl'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class Application(QMainWindow):
    def __init__(self, **kw):
        super().__init__()
        self.setWindowTitle('FuzzyControl Generator')
        
        self.menu_bar = QMenuBar()
        self.file_menu = self.menu_bar.addMenu('File')
        self.export_menu = self.menu_bar.addMenu('Export')
        
        # File Menu Entries
        self.save_act = QAction('Save')
        self.save_act.triggered.connect(self._on_save)
        self.save_act.setShortcut(QKeySequence.StandardKey.Save)
        
        self.save_as_act = QAction('Save as')
        self.save_as_act.triggered.connect(self._on_save_as)
        self.save_as_act.setShortcut(QKeySequence.StandardKey.SaveAs)
        
        self.load_act = QAction('Load')
        self.load_act.triggered.connect(self._on_load)
        self.file_menu.addActions([self.save_act, self.save_as_act,
                                   self.load_act])
        # Export Menu Entries
        self.exp_python_act = QAction('Export to Python Code')
        self.exp_python_act.triggered.connect(self.exp_to_python)
        
        self.exp_c_act = QAction('Export to C Code')
        self.exp_c_act.triggered.connect(self.exp_to_c)
        self.export_menu.addActions([self.exp_python_act, self.exp_c_act])
        self.setMenuBar(self.menu_bar)
        
        self.data = data.data
        self.data['general']['version'] = __version__
        
        self.ui = Ui_Base(self)
        
        self.setCentralWidget(self.ui)
        
        self.dev_menu = self.menu_bar.addMenu('Dev')
        self.dev_1_act = QAction('Print Data')
        self.dev_1_act.triggered.connect(self.pprint_data)
        self.dev_menu.addAction(self.dev_1_act)
        
        self.simul_act = QAction('Simulate Logic')
        self.simul_act.triggered.connect(self.on_simulate)
        self.dev_menu.addAction(self.simul_act)
        
        self.current_file = None
    
    def on_simulate(self):
        self.ui.simulate()
    
    def _on_save(self):
        if self.current_file is None:
            self._on_save_as()
        else:
            save_reload.save_to_file_pickle(self.current_file, data.data)
    
    def _on_save_as(self):
        filt = 'JSON (*.json);;Pickle (*.pkl)'
        p, f = QFileDialog.getSaveFileName(self, 'Save Project',
                                           # os.path.expanduser('~\\Documents'))
                                           os.path.expanduser('~\\Downloads'), filter=filt)
        
        if p != '':
            if not p.endswith('.pkl') and not p.endswith('.json'):
                p += '.json'
            if p.endswith('.pkl'):
                save_reload.save_to_file_pickle(p, data.data)
            elif p.endswith('.json'):
                d = data.dictify()
                save_reload.save_to_file_json(p, d)
            self.current_file = p
    
    def _on_load(self):
        filt = 'JSON (*.json);;Pickle (*.pkl) '
        p, f = QFileDialog.getOpenFileName(self, 'Open Project',
                                           # os.path.expanduser('~\\Documents'))
                                           os.path.expanduser('~\\Downloads'), filter=filt)
        
        if p != '':
            if p.endswith('.pkl'):
                d = save_reload.load_from_file_pickle(p)
                data.set_loaded_data(d)
            
            elif p.endswith('.json'):
                d_j = save_reload.load_from_file_json(p)
                d = data.undictify(d_j)
                data.set_loaded_data(d)
            
            else:
                print('Dataformat not supported')
                return
            ld_ver = self.data['general']['version']
            
            if ld_ver != __version__:
                print(f'Not same version: this->{__version__}, loaded->'
                      f'{ld_ver}')
            
            self.current_file = p
            self.ui.clear_all()
            for nm, fv in data.data['inputs'].items():
                self.ui.add_input(fv, nm)
            for nm, fv in data.data['outputs'].items():
                self.ui.add_output(fv, nm)
            for f_el in data.data['logic']:
                self.ui.add_logic_element(f_el)
    
    def pprint_data(self):
        d = data.dictify()
        print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        # j = json.dumps(d, indent=4)
        # print(j)
        pprint.pprint(d, sort_dicts=False)
        # data.pretty_print_data()
    
    def exp_to_python(self):
        exporters.py_export(data.data)
        print('Py export')
    
    def exp_to_c(self):
        print('C export')
        exporters.c_export(data.data, '')
    
    def closeEvent(self, event):
        print('closeEvent')
    
    def quit(self):
        self.close()


def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = Application()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec())


def catch_exceptions(t, val, tb):
    raise Exception(val) from t


if __name__ == '__main__':
    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions
    main()
