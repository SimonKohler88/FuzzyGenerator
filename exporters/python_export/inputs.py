#!/usr/bin/python3
# -*- coding: utf-8 -*-

def _generate_inp_func_from_fuzzy_var(inp):
    s = f'def _calc_input_{inp.name.replace(" ", "_")}(value):\n'
    s += f'\tling_vals = ' + '{\n'
    for each in inp.ling_vars:
        s += f'\t\t"{each.name.replace(" ","_")}": ' + '{\n'
        s +=f'\t\t\t "x": {each.x},\n'
        s +=f'\t\t\t "y": {each.y},\n'
        s +='\t\t},\n'
    s += '\t}\n'
    s += '\tret = {}\n'
    s += '\tfor k, v in ling_vals.items():\n'
    s += '\t\tret[k] = _interpolate(value, v["x"], v["y"])\n'
    s += '\treturn ret\n\n'
    return s.replace('\t', '    ')

def generate_inputs(inp_dict):
    f = ''
    for each in inp_dict.values():
        f += _generate_inp_func_from_fuzzy_var(each)

    s = 'input_results = {\n'
    for k, v in inp_dict.items():
        inp_name = k.replace(" ", "_")
        s+= f'\t"{k}": _calc_input_{inp_name}(in_{inp_name}),\n'
    s += '}\n\n'
    return f, s
