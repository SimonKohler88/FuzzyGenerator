#!/usr/bin/python3
# -*- coding: utf-8 -*-

def _generate_outp_func_from_fuzzy_var(outp):
    s = f'def _calc_output_{outp.name.replace(" ", "_")}(value):\n'
    s += f'\tling_vals = ' + '{\n'
    for each in outp.ling_vars:
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


def generate_outputs(outp_dict):
    f = ''
    for each in outp_dict.values():
        f += _generate_outp_func_from_fuzzy_var(each)

    return f, ''