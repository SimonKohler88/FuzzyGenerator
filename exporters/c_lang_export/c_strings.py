#!/usr/bin/python3
# -*- coding: utf-8 -*-


h_str_start = """
#ifndef {nm}_H_INCLUDED
#define {nm}_H_INCLUDED

# include "fuzzy_math.h"
# include "{p_name}_interface.h"

/* Common typedefs / global defines */
"""

h_if_str_start = """
#ifndef {nm}_INTERFACE_H_INCLUDED
#define {nm}_INTERFACE_H_INCLUDED

# include "stdint.h"

/* Data definitions */
# define FLOAT float
# define UINT8 uint8_t
# define UINT16 uint16_t

"""

def get_lv_name(prj_name, io_name, lv_name):
    s = '_'.join([prj_name, io_name.replace(' ', '_'), 'LV',
                  lv_name.replace(' ', '_')])
    return s


def get_io_name(prj_name, io_name):
    return '_'.join([prj_name, io_name.replace(' ', '_')])


def get_io_num_lv(prj_name, io_name):
    nm = get_io_name(prj_name, io_name)
    return f'{nm}_NUM_LINVARS'


def get_io_data_len(prj_name, io_name):
    nm = get_io_name(prj_name, io_name)
    return f'{nm}_DATA_LEN'


def get_io_num_logic_el(prj_name, io_name):
    nm = get_io_name(prj_name, io_name)
    return f'{nm}_NUM_LOGIC_ELEMENTS'


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
    def_num_len = get_io_data_len(prj_name, io.name)
    st = f'/* Typedefs for {nm} */\n# define {def_lv} {num_lin_vars}\n'
    
    n = io.num_x_len()
    st += f'# define {def_num_len} {n}\n'
    
    st += 'enum {\n'
    
    for lv in io.ling_vars:
        lv_nm = get_lv_name(prj_name, io.name, lv.name)
        st += f'    {lv_nm},\n'
    
    st += '}; typedef UINT8 ' + f'{get_io_linvars_e(prj_name, io.name)};\n\n'
    st += 'typedef struct {\n\t'
    st += f'{get_io_linvars_e(prj_name, io.name)} name;\n\t'
    st += f'FLOAT y[{def_num_len}];\n\tFLOAT value;\n'
    st += '}\n'
    st += f'{get_io_linvar_t(prj_name, io.name)};\n\n'
    
    st += 'typedef struct {\n\t'
    st += f'{get_io_linvar_t(prj_name, io.name)} linvars[{def_lv}];'
    st += f'\n\tFLOAT x[{def_num_len}];\n'
    st += '\tuint8_t num_linvars;\n'
    
    st += '\n} '
    st += f'{get_io_t(prj_name, io.name)};\n\n'
    return st


def get_logic_el_name_t(i, project_name):
    return f'{project_name}_FUZZY_LOGIC_ELEMENT_{i:02d}_t'


def get_logic_el_name(i, project_name):
    return f'{project_name}_FUZZY_LOGIC_ELEMENT_{i:02d}'


def make_logic_h(num, logic_el, project_name):
    st = 'typedef struct {\n'
    
    in1_short_nm = logic_el.in1.name
    io1_t = get_io_t(project_name, in1_short_nm)
    st += f'\t{io1_t}* in1_ptr;\n'
    
    in2_short_nm = logic_el.in2.name
    io2_t = get_io_t(project_name, in2_short_nm)
    st += f'\t{io2_t}* in2_ptr;\n'
    
    out_short_nm = logic_el.out.name
    out_t = get_io_t(project_name, out_short_nm)
    st += f'\t{out_t}* out_ptr;\n'
    
    in1_lv = get_io_num_lv(project_name, logic_el.in1.name)
    in2_lv = get_io_num_lv(project_name, logic_el.in2.name)
    out_e = get_io_linvars_e(project_name, logic_el.out.name)
    st += f'\tconst {out_e} logic[{in2_lv}][{in1_lv}];\n'
    st += f'\tconst INFERENCE_e logic_inference[{in2_lv}][{in1_lv}];\n'
    
    st += '\tconst INFERENCE_e inference;\n'
    
    nm = get_logic_el_name_t(num, project_name)
    st += '} ' + nm + ';\n\n'
    return st


def get_linvar_var_name(lv_name):
    return f'linvar_{lv_name.replace(" ", "_")}'


def get_out_result_name_t(project_name, out_name):
    nm = get_io_name(project_name, out_name)
    return f'{nm}_ELEMENT_RESULTS_t'


def get_out_result_name(project_name, out_name):
    nm = get_io_name(project_name, out_name)
    return f'{nm}_ELEMENT_RESULTS'


def get_out_result_len(project_name, io_name):
    nm = get_io_name(project_name, io_name)
    return f'{nm}_NUM_OUT_ELEMENTS'


def make_logic_results_h(project_name, out, num):
    nm = get_io_name(project_name, out.name)
    define = get_out_result_len(project_name, out.name)
    st = f'# define {define} {num}\n'
    st += 'typedef struct {\n'
    for each in out.ling_vars:
        lv_nm = get_linvar_var_name(each.name)
        st += f'\tFLOAT {lv_nm}[{define}];\n'
    st += '} ' + f'{get_out_result_name_t(project_name, out.name)};\n\n'
    return st


def make_io_static_instance(project_name, io):
    nm = get_io_name(project_name, io.name)
    io_t = get_io_t(project_name, io.name)
    c_str = f'static {io_t} {nm}' + '= {\n\t.linvars = {\n'
    for ln_v in io.ling_vars:
        lv_nm = get_lv_name(project_name, io.name, ln_v.name)
        c_str += '\t\t{\n\t\t\t.name = ' + f'{lv_nm},'
        y = io.get_y(ln_v)
        y = ",".join([f'{val:.2f}f' for val in y])
        c_str += f'\n\t\t\t.y = {{{y}}}\n'
        c_str += '\n\t\t},'
    c_str += '\n\t},'
    def_name = get_io_num_lv(project_name, io.name)
    c_str += f'\n\t.num_linvars = {def_name},'
    x = io.ling_vars[0].x_as_list_of_str()
    
    c_str += f'\n\t.x = {{{",".join(x)}}}\n'
    c_str += '};\n'
    return c_str


def make_fuzzylogic_static_instance(project_name, nr, logic):
    nm_t = get_logic_el_name_t(nr, project_name)
    inst_name = get_logic_el_name(nr, project_name)
    st = f'static {nm_t} {inst_name} = ' + '{\n'
    
    # fuzzy element: pointer to inputs and outputs
    in1_short_nm = logic.in1.name
    io1_t = get_io_name(project_name, in1_short_nm)
    st += f'\t.in1_ptr = &{io1_t},\n'
    
    in2_short_nm = logic.in2.name
    io2_t = get_io_name(project_name, in2_short_nm)
    st += f'\t.in2_ptr = &{io2_t},\n'
    
    out_short_nm = logic.out.name
    out_t = get_io_name(project_name, out_short_nm)
    st += f'\t.out_ptr = &{out_t},\n'
    
    # fuzzy element: logic matrix
    st += '\t.logic = {\n'
    
    for row in logic.logic:
        st += '\t\t{'
        for col in row:
            lv_nm = get_lv_name(project_name, out_short_nm, col)
            st += f'{lv_nm},'
        st += '},\n'
    st += '\t},\n'
    
    # fuzzy element: inference matrix
    st += '\t.logic_inference = {\n'
    for row in logic.logic:
        st += '\t\t{'
        for col in row:
            inf = 'INF_MIN' if col.lower() == 'min' else 'INF_MAX'
            st += f'{inf},'
        st += '},\n'
    st += '\t},\n'
    
    # fuzzy element: output inference
    inf = 'INF_MIN' if logic.out_inference.lower() == 'min' else 'INF_MAX'
    st += f'\t.inference = {inf}\n'
    
    st += '};\n'
    return st


def make_outp_element_static_instances(project_name, logic):
    # not in bsp code. bsp code can only claculate 1 logic element per output
    # this instance is to buffer the different output results
    st = ''
    
    logic_el_by_outs = {}
    for each in logic:
        if not each.out in logic_el_by_outs:
            logic_el_by_outs[each.out] = []
        logic_el_by_outs[each.out].append(each)
    
    for k, v in logic_el_by_outs.items():
        t_nm = get_out_result_name_t(project_name, k.name)
        nm = get_out_result_name(project_name, k.name)
        st += f'static {t_nm} {nm};\n'
    
    return st


def make_fuzzy_element_calculation_function(project_name, logic):
    logic_el_by_outs = {}  # to keep track of used fuzzy elements
    for each in logic:
        if not each.out in logic_el_by_outs:
            logic_el_by_outs[each.out] = []
        logic_el_by_outs[each.out].append(each)
    
    st = ''
    for i, fuzzy_el in enumerate(logic):
        num = f'{i:02d}'
        st += f'static void calculate_fuzzy_element{num}(void)' + '{\n'
        st += '\tuint8_t row, col;\n'
        out_linvars = [ln.name for ln in fuzzy_el.out.ling_vars]
        for each in out_linvars:
            st += f'\tFLOAT out_{each} = -1;\n'
        st += '\tFLOAT temp = 0;\n\n'
        in_1_num_lingvars = get_io_num_lv(project_name, fuzzy_el.in1.name)
        in_2_num_lingvars = get_io_num_lv(project_name, fuzzy_el.in2.name)
        
        st += f'\tfor (row = 0; row < {in_2_num_lingvars}; row++)' + ' {\n'
        st += f'\t\tfor (col = 0; col < {in_1_num_lingvars}; col++)' + ' {\n'
        
        st += '\t\t\ttemp = 0;\n'
        logic_el_name = get_logic_el_name(i, project_name)
        in1_instance = get_io_name(project_name, fuzzy_el.in1.name)
        in2_instance = get_io_name(project_name, fuzzy_el.in2.name)
        
        st += f'\t\t\tif ({logic_el_name}.logic_inference[row][col] == INF_IGNORE) continue;\n'
        st += f'\t\t\tif ({logic_el_name}.logic_inference[row][col] == INF_MIN)\n'
        st += f'\t\t\t\ttemp = minf({in1_instance}.linvars[col].value, {in2_instance}.linvars[row].value);\n'
        st += f'\t\t\telse\n'
        st += f'\t\t\t\ttemp = maxf({in1_instance}.linvars[col].value, {in2_instance}.linvars[row].value);\n'
        
        st += '\n'
        
        for j, out_lingvar in enumerate(fuzzy_el.out.ling_vars):
            name = fuzzy_el.out.name
            lv_nm = get_lv_name(project_name, name, out_lingvar.name)
            if j == 0:
                st += '\t\t\tif '
            else:
                st += '\t\t\telse if '
            
            local_out_Var = f'out_{out_linvars[j]}'
            st += f'({logic_el_name}.logic[row][col] == {lv_nm})' + '{\n'
            st += f'\t\t\t\tif ({local_out_Var} < 0) {local_out_Var} = temp;\n'
            st += f'\t\t\t\telse if ({logic_el_name}.inference == INF_MIN) {local_out_Var} = minf(temp, {local_out_Var});\n '
            
            # st += f'\t\t\t\telse if ({logic_el_name}.inference == INF_MAX) {local_out_Var} = maxf(temp, {local_out_Var});\n'
            st += f'\t\t\t\telse {local_out_Var} = maxf(temp, {local_out_Var});\n'
            st += '\t\t\t}\n'
        
        st += '\t\t}\n'
        st += '\t}\n'
        
        for each in out_linvars:
            st += f'\tif (out_{each} <0) out_{each} = 0;\n'
        # figure out current position in output element --> its the place of fuzzy el. in logic_el_by_outs
        num = 0
        for out, fuzzys in logic_el_by_outs.items():
            for i, fuzzy in enumerate(fuzzys):
                if fuzzy == fuzzy_el:
                    num = i
                    break
        
        out_result_name = get_out_result_name(project_name, fuzzy_el.out.name)
        for each in out_linvars:
            st += f'\t{out_result_name}.linvar_{each}[{num}] = out_{each};\n'
        st += '}\n'
    return st


def make_output_calculation_functions(project_name, data):
    logic = data['logic']
    logic_el_by_outs = {}  # to keep track of used fuzzy elements
    for each in logic:
        if not each.out in logic_el_by_outs:
            logic_el_by_outs[each.out] = []
        logic_el_by_outs[each.out].append(each)
    
    st = ''
    global_inference = 'INF_MIN' if data['logic_inference'] == 'Min' else 'INF_MAX'
    for out, fuzzys in logic_el_by_outs.items():
        out_result_name = get_out_result_name(project_name, out.name)
        st += f'static FLOAT calculate_{out_result_name}(void)' + '{\n'
        
        out_linvars = [ln.name for ln in out.ling_vars]
        data_len = get_io_data_len(project_name, out.name)
        for each in out_linvars:
            st += f'\tFLOAT cutoff_{each}[{data_len}] = ' + '{0};\n'
        
        st += f'\tFLOAT area[{data_len}] = ' + '{0};\n'
        st += '\tFLOAT result = 0;\n'
        
        st += f'\t//output inference: {data['logic_inference']}\n'
        
        io_nm = get_io_name(project_name, out.name)
        num_elem = get_out_result_len(project_name, out.name)
        
        if data['logic_inference'] == 'Min':
            for each in out_linvars:
                ln_nm = get_lv_name(project_name, out.name, each)
                cmp_linvar = f'{out_result_name}.linvar_{each}'  # from result container
                st += f'\t{io_nm}.linvars[{ln_nm}].value = min_array({cmp_linvar},{num_elem});\n'
                """
                out01.linvars[OUT01_LV_LOW].value = min_array(fuzzy_ctrl.out01_results.linvar_low, NUM_OUTPUT01_ELEMENTS);
                out01.linvars[OUT01_LV_MID].value = min_array(fuzzy_ctrl.out01_results.linvar_mid, NUM_OUTPUT01_ELEMENTS);
                out01.linvars[OUT01_LV_HIGH].value = min_array(fuzzy_ctrl.out01_results.linvar_high, NUM_OUTPUT01_ELEMENTS);
                """
        else:
            for each in out_linvars:
                ln_nm = get_lv_name(project_name, out.name, each)
                cmp_linvar = f'{out_result_name}.linvar_{each}'  # from result container
                st += f'\t{io_nm}.linvars[{ln_nm}].value = max_array({cmp_linvar},{num_elem});\n'
                """
                out01.linvars[OUT01_LV_LOW].value = max_array(fuzzy_ctrl.out01_results.linvar_low, NUM_OUTPUT01_ELEMENTS);
                out01.linvars[OUT01_LV_MID].value = max_array(fuzzy_ctrl.out01_results.linvar_mid, NUM_OUTPUT01_ELEMENTS);
                out01.linvars[OUT01_LV_HIGH].value = max_array(fuzzy_ctrl.out01_results.linvar_high, NUM_OUTPUT01_ELEMENTS);
                """
        
        """
        min_array_value(out01.linvars[OUT01_LV_LOW].y, out01.linvars[OUT01_LV_LOW].value, cutoff_low, NUM_DATA_ARRAY);
        min_array_value(out01.linvars[OUT01_LV_MID].y, out01.linvars[OUT01_LV_MID].value, cutoff_mid, NUM_DATA_ARRAY);
        min_array_value(out01.linvars[OUT01_LV_HIGH].y, out01.linvars[OUT01_LV_HIGH].value, cutoff_high, NUM_DATA_ARRAY);
        """
        st += '\n'
        for each in out_linvars:
            ln_nm = get_lv_name(project_name, out.name, each)
            st += f'\tmin_array_value({io_nm}.linvars[{ln_nm}].y, {io_nm}.linvars[{ln_nm}].value, cutoff_{each},{data_len});\n'
        
        """
        max_array_array(cutoff_low, area, area, NUM_DATA_ARRAY);
        max_array_array(cutoff_mid, area, area, NUM_DATA_ARRAY);
        max_array_array(cutoff_high, area, area, NUM_DATA_ARRAY);
        """
        st += '\n'
        for each in out_linvars:
            # ln_nm = get_lv_name(project_name, out.name, each)
            st += f'\tmax_array_array(cutoff_{each}, area,area ,{data_len});\n'
        
        """
        //print_array(area, NUM_DATA_ARRAY);
        result = centre_of_gravity(out01.x, area, NUM_DATA_ARRAY);
        return result;
        """
        st += '\n'
        st += f'\tresult = centre_of_gravity({io_nm}.x, area, {data_len});\n'
        st += '\treturn result;\n'
        st += '}\n'
    
    return st


def make_fuzzy_function(project_name, data):
    st = '/* calculation function */\n'
    st += f'uint8_t {project_name}_calculate_fuzzy({project_name}_IO_STRUCT_t *io_struct) ' + '{\n'
    # st += '\tERROR_CODE_e err = ERR_NONE;\n'
    
    for in_name, in_io in data['inputs'].items():
        io_name = get_io_name(project_name, in_io.name)
        
        linvars = [ln.name for ln in in_io.ling_vars]
        data_len = get_io_data_len(project_name, in_io.name)
        for each in linvars:
            lv_name = get_lv_name(project_name, in_io.name, each)
            st += f'\t{io_name}.linvars[{lv_name}].value = '
            st += f'interpolate(io_struct->{io_name}, {io_name}.x, {io_name}.linvars[{lv_name}].y, {data_len});\n'
    
    for i, fuzzy_el in enumerate(data['logic']):
        num = f'{i:02d}'
        st += f'\tcalculate_fuzzy_element{num}();\n'
    
    for out_name, out_io in data['outputs'].items():
        io_name = get_io_name(project_name, out_io.name)
        out_result_name = get_out_result_name(project_name, out_io.name)
        st += f'\tio_struct->{io_name} = calculate_{out_result_name}();\n'
        
    st += '\treturn 0;\n}'
    
    return st


"""

/* calculation function */
uint8_t calculate_fuzzy(IO_STRUCT_t *io_struct) {
    ERROR_CODE_e err = ERR_NONE;
    //printf("Inputs given: in1: %f, in2: %f\n", io_struct->input01, io_struct->input02);
    /* calculate linguistic vars for in 1 */
    in01.linvars[INP01_LV_LOW].value = interpolate(io_struct->input01, in01.x, in01.linvars[INP01_LV_LOW].y,
                                                   NUM_DATA_ARRAY);
    in01.linvars[INP01_LV_MID].value = interpolate(io_struct->input01, in01.x, in01.linvars[INP01_LV_MID].y,
                                                   NUM_DATA_ARRAY);
    in01.linvars[INP01_LV_HIGH].value = interpolate(io_struct->input01, in01.x, in01.linvars[INP01_LV_HIGH].y,
                                                    NUM_DATA_ARRAY);

    /* calculate linguistic vars for in 2 */
    in02.linvars[INP02_LV_LOW].value = interpolate(io_struct->input02, in02.x, in02.linvars[INP02_LV_LOW].y,
                                                   NUM_DATA_ARRAY);
    in02.linvars[INP02_LV_MID].value = interpolate(io_struct->input02, in02.x, in02.linvars[INP02_LV_MID].y,
                                                   NUM_DATA_ARRAY);
    in02.linvars[INP02_LV_HIGH].value = interpolate(io_struct->input02, in02.x, in02.linvars[INP02_LV_HIGH].y,
                                                    NUM_DATA_ARRAY);

    //printf("in1_low: %f, in1_mid: %f, in1_high: %f\n", in01.linvars[INP01_LV_LOW].value, in01.linvars[INP01_LV_MID].value, in01.linvars[INP01_LV_HIGH].value);
    //printf("in2_low: %f, in2_mid: %f, in2_high: %f\n", in02.linvars[INP02_LV_LOW].value, in02.linvars[INP02_LV_MID].value, in02.linvars[INP02_LV_HIGH].value);
    calculate_fuzzy_element01();

    io_struct->output01 = calculate_output_01();

    return err;
}
"""
