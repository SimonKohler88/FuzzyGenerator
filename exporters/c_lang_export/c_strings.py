#!/usr/bin/python3
# -*- coding: utf-8 -*-



h_str_start = """
#ifndef {nm}_H_INCLUDED
#define {nm}_H_INCLUDED

# include "fuzzy_math.h"
# include "fuzzy_interface.h"

/* Common typedefs / global defines */
"""


def get_lv_name(prj_name, io_name, lv_name):
    s = '_'.join([prj_name, io_name.replace(' ', '_'), 'LV',
                  lv_name.replace(' ', '_')])
    return s


def get_io_name(prj_name, io_name):
    return '_'.join([prj_name, io_name.replace(' ', '_')])


# def get_io_var_name(io_name, inp=True):
#     in_out = 'input' if inp else 'output'
#     return f"{in_out}_{io_name.replace(' ', '_')}"

# def get_io_num_data(prj_name, io_name):
#     nm = get_io_name(prj_name, io_name)
#     return f'{nm}_NUM_DATA_LEN'


def get_io_num_lv(prj_name, io_name):
    nm = get_io_name(prj_name, io_name)
    
    return f'{nm}_NUM_LINVARS'


def get_io_linvars_e(prj_name, io_name):
    nm = get_io_name(prj_name, io_name)
    return f'{nm}_LINVARS_e'


def get_io_linvar_t(prj_name, io_name):
    nm = get_io_name(prj_name, io_name)
    return f'{nm}_LINVAR_t'


def get_io_t(prj_name, io_name):
    nm = get_io_name(prj_name, io_name)
    return f'{nm}_t'


def make_io_h(io, prj_name):
    nm = get_io_name(prj_name, io.name)
    num_lin_vars = len(io.ling_vars)
    def_lv = get_io_num_lv(prj_name, io.name)
    # def_num_len = get_io_num_data(prj_name, io.name)
    
    n = io.num_x_pts()
    
    # x_num_name  = f'NUM_DATA_ARRAY_{nm}'
    
    st = f'/* Typedefs for {nm} */\n# define {def_lv} {num_lin_vars}\n'
    # st += f'# define {def_num_len} {n}\n\n'
    
    for lv in io.ling_vars:
        lv_nm = get_lv_name(prj_name, io.name, lv.name)
    
    st += 'enum {\n'
    
    for lv in io.ling_vars:
        lv_nm = get_lv_name(prj_name, io.name, lv.name)
        st += f'    {lv_nm},\n'
    
    st += '}; typedef UINT8 ' + f'{get_io_linvars_e(prj_name, io.name)};\n\n'
    st += 'typedef struct {\n\t'
    st += f'{get_io_linvars_e(prj_name, io.name)} name;\n\t'
    st += f'FLOAT y[{def_num_len}];\n\tFLOAT value; ' + '}\n'
    st += f'{get_io_linvar_t(prj_name, io.name)};\n\n'
    
    st += 'typedef struct {\n\t'
    st += f'{get_io_linvar_t(prj_name, io.name)} linvars[{def_lv}];'
    st += f'\n\tFLOAT x[{def_num_len}];' + '\n} '
    st += f'{get_io_t(prj_name, io.name)};\n\n'
    return st


def get_logic_el_name_t(i, project_name):
    return f'{project_name}_FUZZY_LOGIC_ELEMENT_{i:02d}_t'


def make_logic_h(num, logic_el, project_name):
    st = 'typedef struct {\n'
    
    in1_lv = get_io_num_lv(project_name, logic_el.in1.name)
    in2_lv = get_io_num_lv(project_name, logic_el.in2.name)
    out_e = get_io_linvars_e(project_name, logic_el.out.name)
    st += f'\tconst {out_e} logic[{in2_lv}][{in1_lv}];\n'
    st += f'\tconst INFERENCE_e logic_inference[{in2_lv}][{in1_lv}];\n'
    nm = get_logic_el_name_t(num, project_name)
    st += '} ' + nm + ';\n\n'
    return st


def get_linvar_var_name(lv_name):
    return f'linvar_{lv_name.replace(" ", "_")}'


def get_out_result_name_t(project_name, out_name):
    nm = get_io_name(project_name, out_name)
    return f'{nm}_ELEMENT_RESULTS_t'


def make_logic_results_h(project_name, out, num):
    nm = get_io_name(project_name, out.name)
    define = f'NUM_{nm}_ELEMENTS'
    st = f'# define {define} {num}\n'
    st += 'typedef struct {\n'
    for each in out.ling_vars:
        lv_nm = get_linvar_var_name(each.name)
        st += f'\tFLOAT {lv_nm}[{define}];\n'
    st += '} ' + f'{get_out_result_name_t(project_name, out.name)};\n\n'
    return st


def make_io_static_instance(project_name, io):
    nm = get_io_name(project_name, io.name)
    
    c_str = 'static ' + nm + '= {\n\t.linvars = {\n'
    for ln_v in io.ling_vars:
        lv_nm = get_lv_name(project_name, io.name, ln_v.name)
        c_str += '\t\t{\n\t\t\t.name = ' + f'{lv_nm},'
        y = ",".join(ln_v.y_as_list_of_str())
        c_str += f'\n\t\t\t.y = {{{y}}}\n'
        c_str += '\n\t\t},'
    
    def_name = get_io_num_lv(project_name, io.name)
    c_str += f'\n\t.num_linvars = {def_name},'
    x = io.ling_vars[0].x_as_list_of_str()
    
    c_str += f'\n\t.x = {{{",".join(x)}}}\n'
    c_str += '};\n'
    return c_str



def make_c_str(data, project_name):
    pass
