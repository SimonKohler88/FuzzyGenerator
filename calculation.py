#!/usr/bin/python3
# -*- coding: utf-8 -*-


import numpy as np


def interpolate(val, x, y):
    if val <= min(x):
        return y[0]
    if val >= max(x):
        return y[-1]
    return np.interp(val, x, y)


def c_step1(logic_dict):
    # sort logic elements for outputs
    step1 = {}
    for each in logic_dict:
        if not each.out.name in step1:
            step1[each.out.name] = []
        step1[each.out.name].append(each)
    return step1


def c_step2(step1, inp_d):
    # compare all input-lingvars with each other
    step2 = {}
    for k, v in step1.items():
        if k not in step2:
            # must look like {out:{linvar1:[], linvar2:[]}}
            step2[k] = {k2.name: [] for k2 in v[0].out.ling_vars}

        for l_elem in v:
            tmp = {k2.name: [] for k2 in v[0].out.ling_vars}
            for i, lin1 in enumerate(l_elem.in1.ling_vars):
                for j, lin2 in enumerate(l_elem.in2.ling_vars):
                    # if ((inp_d[l_elem.in1.name][lin1.name] > 0) and
                    #         (inp_d[l_elem.in2.name][lin2.name] > 0)):
                    o_ling = l_elem.logic[j][i]
                    inf = l_elem.logic_inference[j][i]
                    if o_ling != 'None':
                        if inf.lower() == 'min':
                            fn = min
                        else:
                            fn = max
                        tmp[o_ling].append(fn(inp_d[l_elem.in1.name][lin1.name],
                                inp_d[l_elem.in2.name][lin2.name]))

            for k2, v2 in tmp.items():
                step2[k][k2].append(v2)

    return step2


def c_step3(step2, glob_inference, step1):
    step3_5 = {}
    for k, v in step1.items():
        if k not in step3_5:
            step3_5[k] = {k2.name: [] for k2 in v[0].out.ling_vars}

        for i in range(len(v)):
            out_inf = v[i].out_inference
            fn = min if out_inf.lower() == 'min' else max
            for k2, v2 in step2[k].items():
                step3_5[k][k2].append(fn(v2[i]))

    fn = min if glob_inference.lower() == 'min' else max
    step3 = {}
    for k, v in step1.items():
        if k not in step3:
            step3[k] = {k2: fn(v2) if len(v2) > 0 else 0 for k2, v2 in
                                step3_5[k].items()}
    # maximum of each val

    # for k, v in step2.items():
    #     if k not in step3:
    #         step3[k] = {k2: max(v2) if len(v2) > 0 else 0 for k2, v2 in
    #                     step2[k].items()}
    return step3


def c_step4(output_d):
    # map ling vars of outputs
    step4 = {}
    for k, v in output_d.items():
        if k not in step4:
            step4[k] = {lv.name: lv for lv in v.ling_vars}
    return step4


def c_step5(step3, step4):
    step5 = {}
    for k, v in step4.items():
        if k not in step5:
            step5[k] = {}

        for k2, v2 in v.items():
            val = step3[k][k2]

            n_x = np.arange(v2.x[0], v2.x[-1] + v2.dx, v2.dx)
            n_y = np.interp(n_x, v2.x, v2.y)

            step5[k][k2] = {
                'y': np.where(n_y < val, n_y, val),
                'x': n_x
            }
    return step5


def c_step6(step5):
    step6 = {}

    for k, v in step5.items():
        if k not in step6:
            step6[k] = {}
        x_arr = []
        y_arr = []
        for k2, v2 in v.items():
            if len(x_arr) == 0:
                x_arr = v2['x']
                y_arr = v2['y']
                continue
            if sum(v2['y']) == 0:
                continue

            y_arr = np.where(v2['y']> y_arr, v2['y'], y_arr)
        step6[k]['x'] = x_arr
        step6[k]['y'] = y_arr

    return step6



def c_step7(step6):
    # calculate Centre of gravity
    step7 = {}
    for k, v in step6.items():
        y_sum = sum(v['y'])
        if y_sum == 0:
            print('Division by Zero in step 7: result is 0')
            x = 0
        else:
            w_sum = 0

            for i in range(0, len(v['x'])):
                dx = v['x'][i]
                m_y = (v['y'][i])
                w_sum += m_y * dx

            x = w_sum / y_sum
        step7[k] = x
    return step7


def calculate_yield(inp_d, data_dict, verbose=False):
    if verbose:
        print('+++++++++++++++++++++++++++++++++++++++')
        print(inp_d)

    # sort logic elements for outputs
    step1 = c_step1(data_dict['logic'])
    if verbose:
        print('step1', step1)
    yield step1

    # compare all input-lingvars with each other
    step2 = c_step2(step1, inp_d)
    if verbose:
        print('step2', step2)
    yield step2

    # step 3: minimum of each val
    step3 = c_step3(step2, data_dict['logic_inference'], step1)
    if verbose:
        print('step3', step3)
    yield step3

    # map ling vars of outputs
    step4 = c_step4(data_dict['outputs'])
    if verbose:
        print('step4', step4)
    yield step4

    # min of val and output array (cut off the head)
    step5 = c_step5(step3, step4)
    if verbose:
        print('step5', step5)
    yield step5

    # merge lingvars together
    step6 = c_step6(step5)
    if verbose:
        print('step6', step6)
    yield step6

    # step 7: calculate Centre of gravity of area
    step7 = c_step7(step6)

    if verbose:
        print('step7', step7)
    yield step7


def calculate(inp_d, data_dict, verbose=False):
    if verbose:
        print('+++++++++++++++++++++++++++++++++++++++')
        print(inp_d)

    # sort logic elements for outputs
    step1 = c_step1(data_dict['logic'])
    if verbose:
        print('step1', step1)

    # compare all input-lingvars with each other
    step2 = c_step2(step1, inp_d)
    if verbose:
        print('step2', step2)

    # step 3: minimum of each val
    step3 = c_step3(step2, data_dict['logic_inference'], step1)
    if verbose:
        print('step3', step3)

    # map ling vars of outputs
    step4 = c_step4(data_dict['outputs'])
    if verbose:
        print('step4', step4)

    # min of val and output array (cut off the head)
    # step5 = c_step5(step3, step4)
    step5 = c_step5(step3, step4)
    if verbose:
        print('step5', step5)

    # merge lingvars together
    step6 = c_step6(step5)
    if verbose:
        print('step6', step6)

    # step 7: calculate Centre of gravity of area
    step7 = c_step7(step6)

    if verbose:
        print('step7', step7)
    return step7

