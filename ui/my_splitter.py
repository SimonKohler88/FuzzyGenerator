#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QSplitter, \
    QSplitterHandle


class MySplitter(QSplitter):
    def __init__(self, parent=None, *args):
        super().__init__(parent)
        self.setChildrenCollapsible(False)
        self.setHandleWidth(20)

    def createHandle(self):
        return MyHandle(self.orientation(), self)

class MyHandle(QSplitterHandle):
    def __init__(self,orientation, parent=None, *args):
        super().__init__(orientation, parent)
        layout = QVBoxLayout() if orientation == Qt.Orientation.Horizontal \
            else QHBoxLayout()

        dots = 3
        self.frames = []
        st = QFrame.Shape.VLine if orientation == Qt.Orientation.Horizontal \
            else QFrame.Shape.HLine

        for i in range(dots + 2):
            fr = QFrame()

            fr.setFrameStyle(st)
            fr.setLineWidth(1)
            fr.setFrameShadow(QFrame.Shadow.Sunken)
            if i not in [0, dots+1]:
                fr.setFixedWidth(3)
                fr.setFixedHeight(3)
            self.frames.append(fr)
            layout.addWidget(fr)

        self.setLayout(layout)
