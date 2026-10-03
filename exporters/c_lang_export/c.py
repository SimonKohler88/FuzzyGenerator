#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import shutil

import data

from . import c_strings

def c_export(data, path):
    this_path = os.path.dirname(__file__)
    working_dir = os.path.join(this_path, 'working_dir')
    #
    # # cleanup workspace
    # if os.path.exists(working_dir):
    #     shutil.rmtree(working_dir)
    # os.mkdir(working_dir)
    #
    # # copy standard math files
    # _copy_common(this_path, working_dir,'fuzzy_math.h')
    # _copy_common(this_path, working_dir,'fuzzy_math.c')
    # _copy_common(this_path, working_dir,'fuzzy_interface.h')
    
    # project_name = data['general']['prj_name'].replace(' ', '_')
    project_name = 'tst_prj_name'
    
    file_h = os.path.join(working_dir, project_name + '.h')
    file_h_if = os.path.join(working_dir, project_name + '_interface.h')
    file_c = os.path.join(working_dir, project_name + '.c')
    
    # make .h
    h_str = make_h_file_string(data, project_name)
    print(file_h)
    with open(file_h, 'w') as f:
        f.write(h_str)
    
    h_if_str = make_h_if_file_string(data, project_name)
    with open(file_h_if, 'w') as f:
        f.write(h_if_str)
    
    c_str = make_c_file_string(data, project_name)
    with open(file_c, 'w') as f:
        f.write(c_str)


def make_c_file_string(data, project_name):
    c_str = f'#include "{project_name}.h"\n'
    
    for each in data['inputs'].values():
        c_str += c_strings.make_io_static_instance(project_name, each)
    
    for each in data['outputs'].values():
        c_str += c_strings.make_io_static_instance(project_name, each)
    
    # make instance for fuzzy logic: elements and inference
    
    for i, each in enumerate(data['logic']):
        c_str += c_strings.make_fuzzylogic_static_instance(project_name, i, each)
    
    c_str += c_strings.make_outp_element_static_instances(project_name, data['logic'])
    
    c_str += c_strings.make_fuzzy_element_calculation_function(project_name, data['logic'])
    
    c_str += c_strings.make_output_calculation_functions(project_name, data)
    
    c_str += c_strings.make_fuzzy_function(project_name, data)
    
    return c_str

def make_h_if_file_string(data, project_name):
    h_str = c_strings.h_if_str_start.format(nm=project_name.upper())
    
    io_vars = [c_strings.get_io_name(project_name, io.name) for io in data['inputs'].values()]
    io_vars.extend([c_strings.get_io_name(project_name, io.name) for io in data['outputs'].values()])
    
    h_str += 'typedef struct {\n'
    for each in io_vars:
        h_str += f'\tFLOAT {each};\n'
    h_str += '} ' + f'{project_name}_IO_STRUCT_t;\n\n'
    
    h_str += f'uint8_t {project_name}_calculate_fuzzy({project_name}_IO_STRUCT_t* io_struct);\n'
    
    h_str += f'\n\n# endif // {project_name.upper()}_INTERFACE_H_INCLUDED\n'
    return h_str
    
    

def make_h_file_string(data, project_name):
    print(data)
    
    h_str = c_strings.h_str_start.format(nm=project_name.upper(), p_name=project_name)
    h_str += 'enum {\n\tINF_MIN = 0,\n\tINF_MAX,\n\tINF_IGNORE\n'
    h_str += '}; typedef UINT8 INFERENCE_e;\n\n'
    
    io_vars = []
    
    for each in data['inputs'].values():
        h_str += c_strings.make_io_h(each, project_name)
        io_vars.append(c_strings.get_io_name(project_name, each.name))
    
    for each in data['outputs'].values():
        h_str += c_strings.make_io_h(each, project_name)
        io_vars.append(c_strings.get_io_name(project_name, each.name))
    
    h_str += '/* Typedef for Logic elements */\n'
    for i, each in enumerate(data['logic']):
        h_str += c_strings.make_logic_h(i, each, project_name)
    
    h_str += '/* Typedef for Logic element results */\n'
    logic_el_by_outs = {}
    for each in data['logic']:
        if not each.out in logic_el_by_outs:
            logic_el_by_outs[each.out] = []
        logic_el_by_outs[each.out].append(each)
    
    for k, v in logic_el_by_outs.items():
        h_str += c_strings.make_logic_results_h(project_name, k, len(v))
    
   
    # h_str += 'ERROR_CODE_e calculate_fuzzy('
    # h_str += f'{project_name}_IO_STRUCT_t* input_struct);'
    h_str += f'\n\n# endif // {project_name.upper()}_H_INCLUDED\n'
    return h_str


def _copy_common(dir_src, dir_dst, name: str):
    shutil.copy(
        os.path.join(dir_src, name),
        os.path.join(dir_dst, name),
    )
