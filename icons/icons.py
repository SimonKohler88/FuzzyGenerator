#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os




class Icons:
    def __init__(self):
        p = os.path.abspath(__file__)
        self.path = os.path.dirname(p)

        self._icons = []
        for each in os.listdir(self.path):
            f, ext = os.path.splitext(each)
            if ext in ['.png', '.jpg', '.ico', '.svg']:
                self._icons.append(each)

    def __getattr__(self, item):
        for each in self._icons:
            if item.lower() in each.lower():
                return os.path.join(self.path, each)


icons = Icons()