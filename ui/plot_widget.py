#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from PyQt6.QtWidgets import QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, \
    QToolButton, QFormLayout, QListWidget, QListWidgetItem, QFrame, QLineEdit, \
    QLabel, QSpinBox, QFrame, QGroupBox, QDoubleSpinBox
from PyQt6.QtCore import Qt, pyqtSignal

from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from .list_widget import ListWidget

import data


class UIInputLingVarEditWidget(QGroupBox):
    sig_ling_var_name_changed = pyqtSignal(str, str)
    sig_ling_var_destroyed = pyqtSignal(str, str)
    sig_ling_var_created = pyqtSignal()
    sig_ling_var_order_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        f_lay = QFormLayout()
        
        v_box = QVBoxLayout()
        h_box = QHBoxLayout()
        
        v_box.addLayout(h_box)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        self.ling_var_list = ListWidget(label='')
        h_box.addWidget(self.ling_var_list)
        self.plot = FuzzyPlot(0, 100)
        h_box.addWidget(self.plot)
        h_box.addLayout(f_lay)
        
        self.setLayout(v_box)
        
        self.x_min_sb = QSpinBox()
        self.x_max_sb = QSpinBox()
        
        self.x_max_sb.setMaximum(10000)
        self.x_min_sb.setMaximum(10000)
        
        self.x_max_sb.setMinimum(-10000)
        self.x_min_sb.setMinimum(-10000)
        
        self.x_min_sb.setValue(0)
        self.x_max_sb.setValue(100)
        
        f_lay.addRow('X Min', self.x_min_sb)
        f_lay.addRow('X Max', self.x_max_sb)
        
        self.x_grid_sb = QDoubleSpinBox()
        self.y_grid_sb = QDoubleSpinBox()
        
        self.x_grid_sb.setMaximum(100)
        self.x_grid_sb.setMinimum(0.01)
        self.x_grid_sb.setSingleStep(0.01)
        
        self.y_grid_sb.setMaximum(0.1)
        self.y_grid_sb.setMinimum(0.01)
        self.y_grid_sb.setSingleStep(0.1)
        
        self.y_grid_sb.setValue(0.1)
        self.x_grid_sb.setValue(1)
        
        f_lay.addRow('X Grid', self.x_grid_sb)
        f_lay.addRow('Y Grid', self.y_grid_sb)
        
        self.ling_var_list.sig_item_selection_changed.connect(self._sel_change)
        self.ling_var_list.sig_item_destroyed.connect(self._it_destroyed)
        self.ling_var_list.sig_new_item_created.connect(self._create_ling_var)
        self.ling_var_list.sig_item_changed.connect(self._item_changed)
        self.ling_var_list.sig_item_order_changed.connect(self._order_changed)
        
        self.x_min_sb.valueChanged.connect(self._on_range_min_changed)
        self.x_max_sb.valueChanged.connect(self._on_range_max_changed)
        self.x_grid_sb.valueChanged.connect(self._on_range_changed)
        self.y_grid_sb.valueChanged.connect(self._on_range_changed)
        
        self._current_fuzzy_var: data.FuzzyVar | None = None
        
        self.setTitle('Fuzzy Sets')
    
    def _order_changed(self, from_idx, to_idx):
        self._current_fuzzy_var.reorder_ling_var(from_idx, to_idx)
        data.change_ling_var_order_in_fuzzy_logic(
            self._current_fuzzy_var.name, from_idx, to_idx)
        self.plot.clear()
        for ling_var in self._current_fuzzy_var.ling_vars:
            self.plot.add_line(ling_var.name, ling_var.x, ling_var.y)
        self.sig_ling_var_order_changed.emit()
    
    def _on_range_max_changed(self):
        if self._current_fuzzy_var is None:
            return
        x_min = self.x_min_sb.value()
        x_max = self.x_max_sb.value()
        min_r_allowed = 10 * self._current_fuzzy_var.dx
        if x_max < x_min + min_r_allowed:
            self.x_max_sb.blockSignals(True)
            self.x_max_sb.setValue(x_min + min_r_allowed)
            self.x_max_sb.blockSignals(False)
        print('max change')
        self._rescale_x()
    
    def _on_range_min_changed(self):
        if self._current_fuzzy_var is None:
            return
        x_min = self.x_min_sb.value()
        x_max = self.x_max_sb.value()
        min_r_allowed = 10 * self._current_fuzzy_var.dx
        if x_max < x_min + min_r_allowed:
            self.x_min_sb.blockSignals(True)
            self.x_min_sb.setValue(x_max - min_r_allowed)
            self.x_min_sb.blockSignals(False)
        print('min change')
        self._rescale_x()
    
    def _rescale_x(self):
        if self._current_fuzzy_var is None:
            return
        x_min = self.x_min_sb.value()
        x_max = self.x_max_sb.value()
        n_r = x_max - x_min
        cur_min_x = self._current_fuzzy_var.ling_vars[0].x[0]
        cur_max_x = self._current_fuzzy_var.ling_vars[0].x[-1]
        cur_r = cur_max_x - cur_min_x
        
        for ling_var in self._current_fuzzy_var.ling_vars:
            # normalize
            n_x = [(x - cur_min_x) / cur_r for x in ling_var.x]
            # stretch
            s_x = [x * n_r for x in n_x]
            # move
            m_x = [x + x_min for x in s_x]
            ling_var.x = m_x
            self.plot.update_line(ling_var.name, ling_var.x, ling_var.y)
        self.plot.set_start_end(x_min, x_max)
    
    def _on_range_changed(self):
        if self._current_fuzzy_var is None:
            return
        x_min = self.x_min_sb.value()
        x_max = self.x_max_sb.value()
        if x_max < x_min + 10 * self._current_fuzzy_var.dx:
            pass
        x_space = self.x_grid_sb.value()
        y_space = self.y_grid_sb.value()
        r = x_max - x_min
        grid_p = r / x_space
        if grid_p < 10:
            self.x_grid_sb.blockSignals(True)
            self.x_grid_sb.setValue(r / 10)
            x_space = self.x_grid_sb.value()
            self.x_grid_sb.blockSignals(False)
        
        self._current_fuzzy_var.dx = x_space
        self._current_fuzzy_var.dy = y_space
        self.plot.re_lim(x_min, x_max, x_space, y_space)
    
    def _item_changed(self, it, old_name):
        self.plot.change_label(old_name, it.text())
        self._current_fuzzy_var.change_ling_var_name(old_name, it.text())
        self.sig_ling_var_name_changed.emit(it.text(), old_name)
    
    def _it_destroyed(self, it):
        lbl = it.text()
        data.remove_ling_var_from_fuzzy_logic(self._current_fuzzy_var.name,
                                              lbl)
        self._current_fuzzy_var.remove_ling_var(lbl)
        self.plot.remove_line(lbl)
        self.sig_ling_var_destroyed.emit(self._current_fuzzy_var.name, lbl)
    
    def _create_ling_var(self, it):
        x, y = self.plot.get_standard_x_y_vals()
        lv = self._current_fuzzy_var.add_ling_var(it.text(), x, y)
        data.add_ling_var_to_fuzzy_logic(self._current_fuzzy_var.name,
                                         it.text())
        it.user_storage = lv
        self.plot.add_line(it.text(), x, y)
        self.sig_ling_var_created.emit()
    
    def update_current_name(self):
        self.ling_var_list.name.setText(self._current_fuzzy_var.name)
    
    def _sel_change(self, it):
        nm = it.text()
        self.plot.set_pick_line(nm, it.user_storage)
    
    def set_fuzzy_var(self, fuzzy_var):
        self.ling_var_list.clear()
        self.plot.clear()
        self._current_fuzzy_var = fuzzy_var
        self.ling_var_list.name.setText(fuzzy_var.name)
        for each in fuzzy_var.ling_vars:
            self._add_ling_var(each)
        
        min_x = fuzzy_var.ling_vars[0].x[0]
        max_x = fuzzy_var.ling_vars[0].x[-1]
        dx = fuzzy_var.dx
        dy = fuzzy_var.dy
        self._set_spinb_no_signals(min_x, max_x, dx, dy)
        self.plot.re_lim(min_x, max_x, dx, dy)
    
    def _set_spinb_no_signals(self, min_x, max_x, dx, dy):
        self.x_min_sb.blockSignals(True)
        self.x_min_sb.setValue(int(min_x))
        self.x_min_sb.blockSignals(False)
        
        self.x_max_sb.blockSignals(True)
        self.x_max_sb.setValue(int(max_x))
        self.x_max_sb.blockSignals(False)
        
        self.x_grid_sb.blockSignals(True)
        self.x_grid_sb.setValue(dx)
        self.x_grid_sb.blockSignals(False)
        
        self.y_grid_sb.blockSignals(True)
        self.y_grid_sb.setValue(dy)
        self.y_grid_sb.blockSignals(False)
    
    def _add_ling_var(self, ling_var):
        self.ling_var_list.add_item(ling_var, new_name=ling_var.name)
        self.plot.add_line(ling_var.name, ling_var.x, ling_var.y)
    
    def clear(self):
        self.ling_var_list.clear()
        self.ling_var_list.name.setText('')
        self.plot.clear()
        self._current_fuzzy_var = None


class FuzzyPlot(FigureCanvas):
    def __init__(self, start, end, parent=None, width=4, height=2, dpi=100):
        
        # matplotlib figure initialising
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
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
        self.axes.set_ylim(0, 1)
        
        # self._lines = []
        self.pickLn = None
        self._ling_ref = None  # Linguistic Var
        
        # Callbacks for events
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        self.fig.canvas.mpl_connect('pick_event', self._on_pick)
        self.fig.canvas.mpl_connect('button_release_event',
                                    self._on_button_release)
        self.fig.canvas.mpl_connect('motion_notify_event',
                                    self._on_mouse_motion)
        
        self._drag: Dragger | None = None
        self._drag_artist = None
        
        # Just for beauty
        self.axes.grid()
        
        self._x_min = start
        self._x_max = end
        self._grid_y = None
        self._grid_x = None
        self.dy = 0.1
        self.dx = 1
        self.set_start_end(start, end)
        
        # Transparent Background
        # self.fig.canvas.setStyleSheet("background-color:transparent;")
    
    def update_line(self, name, x, y):
        for each in self.axes.lines:
            if each.get_label() == name:
                each.set_data(x, y)
    
    def change_label(self, old_name, new_name):
        for each in self.axes.lines:
            if each.get_label() == old_name:
                each.set_label(new_name)
                break
        self._redraw_plot()
    
    def get_standard_x_y_vals(self):
        r = self._x_max - self._x_min
        
        x1 = self._grid_x[np.abs(self._grid_x - r * 0.4).argmin()]
        x2 = self._grid_x[np.abs(self._grid_x - r * 0.5).argmin()]
        x3 = self._grid_x[np.abs(self._grid_x - r * 0.6).argmin()]
        x4 = self._grid_x[np.abs(self._grid_x - r * 0.7).argmin()]
        x = [self._x_min, x1, x2, x3, x4, self._x_max]
        y = [0, 0, 1, 1, 0, 0]
        return x, y
    
    def redraw_idle(self):
        self.fig.canvas.draw_idle()
    
    def _redraw_plot(self):
        self.axes.set_ylim(-0.05, 1.05)
        self.set_start_end(self._x_min, self._x_max)
        self.axes.legend()
        self.fig.canvas.draw_idle()
    
    def set_pick_line(self, label, ling_ref):
        if ling_ref is None:
            raise ValueError('Ling Ref is None')
        self._ling_ref = ling_ref
        self._drag = None
        for each in self.axes.lines:
            if each.get_label() == label:
                self.pickLn = each
                self.pickLn.set_lw(3)
            else:
                each.set_lw(1)
        
        self._redraw_plot()
    
    def add_line(self, label, x, y):
        ln, = self.axes.plot(x, y, picker=5, marker='o', label=label, lw=1)
        self._redraw_plot()
    
    def remove_line(self, label):
        for each in list(self.axes.lines):
            if each.get_label() == label:
                each.remove()
        if len(list(self.axes.lines)) > 0:
            self._redraw_plot()
        else:
            self.fig.canvas.draw_idle()
    
    def clear(self):
        for each in self.axes.lines:
            self.remove_line(each.get_label())
        self.axes.set_prop_cycle(None)
        self._ling_ref = None
        self.fig.canvas.draw_idle()
    
    def set_start_end(self, start, end):
        """Resizes the width of the x-Axis"""
        self._x_min = start
        self._x_max = end
        self._grid_y = np.arange(0, 1 + self.dy, self.dy)
        self._grid_x = np.arange(start, end + self.dx, self.dx)
        r = abs(self._x_max - self._x_min)
        self.axes.set_xlim(self._x_min - r * 0.05, self._x_max + r * 0.05)
        self.fig.canvas.draw_idle()
    
    def re_lim(self, x_min, x_max, x_space, y_space):
        """Resizes the x- and the y-Axis"""
        self.dy = y_space
        self.dx = x_space
        self.set_start_end(x_min, x_max)
    
    def put_dot(self, event):
        """Puts a Dot at given Position"""
        data_x = self.pickLn.get_xdata()
        if not isinstance(data_x, list):
            d = data_x.tolist()
            data_x = d
        
        click_x, click_x_ind = self._get_grid_x(event.xdata)
        click_y, click_y_ind = self._get_grid_y(event.ydata)
        if click_x in data_x:
            return
        data_x.append(click_x)
        data_x.sort()
        idx = data_x.index(click_x)
        data_y = self.pickLn.get_ydata()
        if not isinstance(data_y, list):
            d = data_y.tolist()
            data_y = d
        data_y.insert(idx, click_y)
        self.pickLn.set_data(data_x, data_y)
        self._ling_ref.x = data_x
        self._ling_ref.y = data_y
        self.fig.canvas.draw_idle()
    
    def remove_dot(self, event):
        """Removes the closest Dot on the clicked Line"""
        line = event.artist
        
        x_data = line.get_xdata()
        if isinstance(x_data, np.ndarray):
            x_data = x_data.tolist()
        
        y_data = line.get_ydata()
        if isinstance(y_data, np.ndarray):
            y_data = y_data.tolist()
        
        rx = (self._x_max - self._x_min) * 0.05
        ry = (max(y_data) - min(y_data)) * 0.05
        xmin = event.mouseevent.xdata - rx
        xmax = event.mouseevent.xdata + rx
        ymin = event.mouseevent.ydata - ry
        ymax = event.mouseevent.ydata + ry
        
        idx = FuzzyPlot.find_nearest(x_data, event.mouseevent.xdata)
        
        if idx == 0 or idx == len(x_data) - 1:
            return
        
        if xmin < x_data[idx] < xmax:
            if ymin < y_data[idx] < ymax:
                x_data.pop(idx)
                y_data.pop(idx)
                line.set_data(x_data, y_data)
        
        self._ling_ref.x = x_data
        self._ling_ref.y = y_data
        self.fig.canvas.draw_idle()
    
    def _on_button_release(self, event):
        if self._drag is not None and self.pickLn is not None:
            pass
        self._drag = None
    
    def _on_mouse_motion(self, event):
        if self._drag is not None and self.pickLn is not None:
            
            if event.xdata is None or event.ydata is None:
                return
            if self._ling_ref is None:
                print('Ling ref is None')
                return
            
            x_data = list(self.pickLn.get_xdata())
            y_data = list(self.pickLn.get_ydata())
            
            click_x, click_x_ind = self._get_grid_x(event.xdata)
            click_y, click_y_ind = self._get_grid_y(event.ydata)
            if self._drag.delta == 0:
                x = click_x
                
                # check boundaries
                new_x = max(x, self._x_min + self.dx)
                new_x = min(new_x, self._x_max - self.dx)
                
                # check within other points
                if len(x_data) > 2:
                    if len(x_data) - 1 != self._drag.index:
                        new_x = min(new_x,
                                    x_data[self._drag.index + 1] - self.dx)
                    
                    new_x = max(new_x, x_data[self._drag.index - 1] + self.dx)
                
                if self._drag.index != len(
                        x_data) - 1 and self._drag.index != 0:
                    x_data[self._drag.index] = new_x
                # x_data[self._drag.index] = new_x
                
                new_y = min(click_y, 1)
                new_y = max(new_y, 0)
                y_data[self._drag.index] = new_y
            else:
                # line-drag:
                d_x = click_x - self._drag.old_event_x
                self._drag.old_event_x = click_x
                
                new_x = max(self._x_min, x_data[self._drag.index] + d_x)
                new_x = min(new_x, self._x_max)
                # check within other points
                if len(x_data) > 2:
                    new_x = max(new_x, x_data[self._drag.index - 1] + self.dx)
                    if len(x_data) - 1 != self._drag.index:
                        new_x = min(new_x,
                                    x_data[self._drag.index + 1] - self.dx)
                
                x_data[self._drag.index] = new_x
                
                idx_dd = self._drag.index + self._drag.delta
                x2check = x_data[idx_dd]
                new_x2 = max(self._x_min, x2check + d_x)
                new_x2 = min(new_x2, self._x_max)
                # check within other points
                if len(x_data) > 2:
                    new_x2 = max(new_x2, x_data[idx_dd - 1] + self.dx)
                    if len(x_data) - 1 != idx_dd:
                        new_x2 = min(new_x2, x_data[idx_dd + 1] - self.dx)
                x_data[idx_dd] = new_x2
                
                d_y = click_y - self._drag.old_event_y
                self._drag.old_event_y = click_y
                
                new_y = max(0, y_data[self._drag.index] + d_y)
                new_y = min(new_y, 1)
                y_data[self._drag.index] = new_y
                
                y2check = y_data[self._drag.index + self._drag.delta]
                new_y2 = max(0, y2check + d_y)
                new_y2 = min(new_y2, 1)
                y_data[self._drag.index + self._drag.delta] = new_y2
            
            self.pickLn.set_data(x_data, y_data)
            self._ling_ref.x = x_data
            self._ling_ref.y = y_data
            self.fig.canvas.draw_idle()
    
    def _on_click(self, event):
        """Callback from Buttonclick in Plot"""
        if self.pickLn is None:
            return
        
        if event.inaxes:
            if event.button == 1 and not self._drag:
                self.put_dot(event)
    
    def _get_grid_x(self, value):
        click_ind = np.abs(self._grid_x - value).argmin()
        return self._grid_x[click_ind], click_ind
    
    def _get_grid_y(self, value):
        click_ind = np.abs(self._grid_y - value).argmin()
        return self._grid_y[click_ind], click_ind
    
    def _on_pick(self, event):
        """Callback from Click on Line"""
        if self.pickLn is None:
            return
        
        if event.mouseevent.button == 3:
            self.remove_dot(event)
        elif event.mouseevent.button == 1:
            line = self.pickLn
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            self._drag = Dragger()
            self._drag.x_data = line.get_xdata()
            self._drag.y_data = line.get_ydata()
            
            eps_x = abs(self._x_max - self._x_min) * 0.05
            
            click_x, click_x_ind = self._get_grid_x(event.mouseevent.xdata)
            click_y, click_y_ind = self._get_grid_y(event.mouseevent.ydata)
            
            ind_x, isline_x = self._get_index_line_or_point(
                x_data, click_x, epsilon=eps_x)
            self._drag.index = ind_x
            
            ind_y, isline_y = self._get_index_line_or_point(
                y_data, click_y, epsilon=0.02)
            
            self._drag.old_event_x = click_x
            self._drag.old_event_y = click_y
            
            if isline_y != 0 or isline_x != 0:
                self._drag.delta = isline_x if isline_x != 0 else isline_y
            
            self._drag.artist = line
    
    def get_data(self):
        x, y = self.pickLn.get_data()
        return x, y
    
    def set_data(self, x, y):
        self.pickLn.set_data(x, y)
        self.fig.canvas.draw_idle()
    
    def _get_index_line_or_point(self, arr, value, epsilon=5.):
        """Returns the index of closest point in array to value.
        if value not within range epsilon to point, additionaly returns
        1 or -1 as offset to the closest point-> it's a line
        """
        _vals = np.asarray(arr)
        check = _vals - value
        index = np.argwhere((check >= -epsilon) & (check <= epsilon))
        index_2_off = 0
        if len(index) > 0:
            index = index.min()
        else:
            index = (np.abs(_vals - value)).argmin()
            if (value - _vals[index]) >= 0:
                index_2_off = 1
            else:
                index_2_off = -1
        return index, index_2_off
    
    @staticmethod
    def find_nearest(array, value):
        """Returns the index of the nearest Value of value in array"""
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx


class Dragger:
    """used as storage for drag-functionality"""
    
    def __init__(self):
        self.index = 0
        self.old_event_x = 0
        self.old_event_y = 0
        
        self.x_data = None
        self.y_data = None
        
        self.is_line = False
        self.delta = 0  # in case it's a line
        
        self.artist = None


if __name__ == '__main__':
    pass
