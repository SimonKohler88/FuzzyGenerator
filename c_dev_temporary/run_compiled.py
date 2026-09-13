#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import ctypes as ct
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

_dll_path = os.path.abspath('./fuzzy_c/fuzzy_c/bin/Debug/libfuzzy_c.dll')


class IO_Struct(ct.Structure):
    _fields_ = [
        ('input01', ct.c_float),
        ('input02', ct.c_float),
        ('output01', ct.c_float),
    ]


def print_3d():
    tst_dll = ct.CDLL(_dll_path)

    io_struct = IO_Struct()
    ptr = ct.pointer(io_struct)

    in1_r = np.arange(0, 100 + 1, 1)
    in2_r = np.arange(0, 100 + 1, 1)

    x, y = np.meshgrid(in1_r, in2_r)
    z = np.zeros(x.shape)

    for i, in1 in enumerate(in1_r):
        for j, in2 in enumerate(in2_r):
            io_struct.input01 = in1
            io_struct.input02 = in2

            ret = tst_dll.calculate_fuzzy(ptr)
            z[i][j] = io_struct.output01
            # print('loop', i, j, ' in1: ', io_struct.input01, ' in2: ',
            #     io_struct.input02, ' out01: ', io_struct.output01)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.plot_surface(x, y, z, cmap=cm.RdBu_r)
    ax.set_xlabel('in1')
    ax.set_ylabel('in2')
    plt.show()


def calc_single():
    tst_dll = ct.CDLL(_dll_path)

    io_struct = IO_Struct()
    ptr = ct.pointer(io_struct)

    io_struct.input01 = 90
    io_struct.input02 = 91
    ret = tst_dll.calculate_fuzzy(ptr)
    print('in1: ', io_struct.input01)
    print('in2: ', io_struct.input02)
    print('out1: ', io_struct.output01)


if __name__ == '__main__':
    # calc_single()
    print_3d()
