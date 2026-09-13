#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pprint

import save_reload
import exporters
import matplotlib.pyplot as plt

import numpy as np


def interpolate(val, x, y):
    if val <= min(x):
        return y[0]
    if val >= max(x):
        return y[-1]
    return np.interp(val, x, y)


# if __name__ == '__main__':
#     data = save_reload.load_from_file_pickle('./test.pkl')
#     pprint.pprint(data)
#     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
#     print('+++++++++++++++++++++++++++++++++++++++++++++++++++++')
#     p = './py_export.py'
#     exporters.py_export(data, p)

if __name__ == '__main__':
    x = np.arange(0, 110, 10)

    y_prot = [0, 0, 1]
    x_prot = [0, 50, 100]
    print(len(x))
    y = np.interp(x, x_prot, y_prot)
    print()
    print('{' + ','.join([f'{n:.02f}' for n in y]) + '}')
