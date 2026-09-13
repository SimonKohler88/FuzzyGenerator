#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
from .inputs import generate_inputs
from .outputs import generate_outputs


_interpolate_func = """
def _interpolate(val, x, y):
    if val <= min(x):
        return y[0]
    if val >= max(x):
        return y[-1]
    return np.interp(val, x, y)

""".replace('\t', '    ')

def py_export(data_dict, file):
    gen_f = './res_py.py'
    if os.path.exists(gen_f):
        os.remove(gen_f)

    s = 'import numpy as np\n\n'
    # val = 5
    # inp_func, inp_call = generate_inputs(data_dict['inputs'])
    outp_func, outp_call = generate_outputs(data_dict['outputs'])

    s+=outp_func


    print(s)
    print(outp_call)

    # args = [n.name.replace(' ', '_') for n in data_dict['inputs'].values()]
    # args_s = ', '.join(args)
    # s = f'def calc_fuzzy({args_s}):'





