#!/usr/bin/python3
# -*- coding: utf-8 -*-
from collections import deque
import pprint
import itertools

import exporters.c_lang_export.c_strings


class LinguisticVar:
    def __init__(self, name, x, y):
        self.name = name
        self.y = y
        self.x = x
        self.dx = 1
    
    def to_dict(self):
        return {'name': self.name,
                'x': self.x,
                'y': self.y,
                'dx': self.dx}
    
    def y_as_list_of_str(self):
        return [str(n) for n in self.y]
    
    def x_as_list_of_str(self):
        return [str(n) for n in self.x]
    
    def len_x(self):
        return len(self.x)

    @staticmethod
    def from_dict(dic):
        lv = LinguisticVar(dic['name'], dic['x'], dic['y'])
        lv.dx = dic['dx']
        return lv


class FuzzyVar:
    def __init__(self, name, *ling_vars, dx=1):
        self.name = name
        self.ling_vars = list(ling_vars)
        self._dx = dx
        self.dy = 0.1
    
    # def num_x_pts(self):
    #     if len(self.ling_vars) > 0:
    #         var = self.ling_vars[0]
    #         n = (var.x[-1] - var.x[0]) / var.dx + 1
    #         return len(var.x)
    #     return None
    
    # def num_y_pts(self):
    #     if len(self.ling_vars) > 0:
    #         var = self.ling_vars[0]
    #         n = (var.y[-1] - var.x[0]) / var.dx
    #         return n
    #     return None
    
    def ling_var_names(self):
        return [n.name for n in self.ling_vars]
    
    @property
    def dx(self):
        return self._dx
    
    @dx.setter
    def dx(self, value):
        self._dx = value
        for each in self.ling_vars:
            each.dx = self._dx
    
    def remove_ling_var(self, name):
        ref = None
        for each in self.ling_vars:
            if name == each.name:
                ref = each
        
        if ref is not None:
            self.ling_vars.remove(ref)
    
    def add_ling_var(self, name, x, y):
        lv = LinguisticVar(name, x, y)
        lv.dx = self._dx
        self.ling_vars.append(lv)
        return lv
    
    def reorder_ling_var(self, from_idx, to_idx):
        it = self.ling_vars.pop(from_idx)
        self.ling_vars.insert(to_idx, it)
    
    def change_ling_var_name(self, old_name, new_name):
        for each in self.ling_vars:
            if each.name == old_name:
                each.name = new_name
                break
    
    def __len__(self):
        return len(self.ling_vars)
    
    def __repr__(self):
        return (f'<FuzzyVar {self.name} : 0x{id(self):x}'
                f'{[n.name for n in self.ling_vars]}>')
    
    def to_dict(self):
        return {'name': self.name,
                'dy': self.dy,
                'dx': self._dx,
                'ling_vars': {n.name: n.to_dict() for n in self.ling_vars}}
    
    @staticmethod
    def from_dict(dic):
        fv = FuzzyVar(dic['name'],
                      *[LinguisticVar.from_dict(d) for d in dic['ling_vars'].values()],
                      dx=dic['dx'])
        fv.dy = dic['dy']
        return fv


class FuzzyLogicElement:
    def __init__(self, in1: FuzzyVar, in2: FuzzyVar, out: FuzzyVar):
        self.in1 = in1
        self.in2 = in2
        self.out = out
        o_var = self.out.ling_vars[0].name
        # col = in1, row = in2
        self.logic = [[o_var for i in range(len(self.in2.ling_vars))] for n
                      in range(len(self.in1.ling_vars))]
        self.logic_inference = [['min' for i in range(len(
            self.in2.ling_vars))] for n
                                in range(len(self.in1.ling_vars))]
        self.out_inference = 'Max'
    
    def is_corresponding_element(self, in1, in2, out):
        if out != self.out.name:
            return False
        if ((in1 == self.in1.name and in2 == self.in2.name) or
                (in1 == self.in2.name and in2 == self.in1.name)):
            return True
        return False
    
    def iterator(self):
        for i, row in enumerate(self.logic):
            for j, el in enumerate(row):
                yield i, j, el, self.logic_inference[i][j]
    
    def update_matrix_names(self, new_name, old_name):
        inx_2_change = []
        for i, row in enumerate(self.logic):
            for j, el in enumerate(row):
                if el == old_name:
                    inx_2_change.append([i, j])
        
        for i, j in inx_2_change:
            self.logic[i][j] = new_name
    
    def reevaluate_matrix(self):
        names = [n.name for n in self.out.ling_vars]
        inx_2_change = []
        for i, row in enumerate(self.logic):
            for j, el in enumerate(row):
                if el not in names:
                    inx_2_change.append([i, j])
        for i, j in inx_2_change:
            self.logic[i][j] = 'None'
    
    def to_dict(self):
        d = {'in1': self.in1.name,
             'in2': self.in2.name,
             'out': self.out.name,
             'logic': self.logic,
             'logic_inference': self.logic_inference,
             'out_inference': self.out_inference
             }
        return d
    
    @staticmethod
    def from_dict(dic):
        pass
    
    def __repr__(self):
        return (f'<FuzzyLogic 0x{id(self):x}, '
                f'in1:0x{id(self.in1):x}, in2:0x{id(self.in2):x}, out'
                f':0x{id(self.out):x}>')


data = {
    'inputs': {
    },
    'outputs': {
    },
    'logic': deque(),
    'logic_inference': 'Min',
    'general': {
    }
}


# +++++++++++++++++++++++++++++++++ Save/Load +++++++++++++++++++++++++++++++
def dictify():
    d = {}
    for k, v in data.items():
        if k == 'general':
            d[k] = v
        elif k in ['inputs', 'outputs']:
            d[k] = {k2: v2.to_dict() for k2, v2 in v.items()}
        elif k == 'logic':
            d[k] = [n.to_dict() for n in v]
        elif k == 'logic_inference':
            d[k] = v
    return d


def undictify(dic):
    d = {}
    for k, v in dic.items():
        if k == 'general':
            d[k] = v
        elif k in ['inputs', 'outputs']:
            d[k] = {k2: FuzzyVar.from_dict(v2) for k2, v2 in v.items()}
    
    d['logic'] = deque()
    
    for each in dic['logic']:
        fle = FuzzyLogicElement(
            d['inputs'][each['in1']],
            d['inputs'][each['in2']],
            d['outputs'][each['out']]
        )
        fle.logic = each['logic']
        if 'logic_inference' in each:
            fle.logic_inference = each['logic_inference']
        if 'out_inference' in each:
            fle.out_inference = each['out_inference']
        d['logic'].append(fle)
    
    if 'logic_inference' in dic:
        d['logic_inference'] = dic['logic_inference']
    return d


# +++++++++++++++++++++++++++++++++ Fuzzy Logic +++++++++++++++++++++++++++++++

def get_fuzzy_logic_element(in1, in2, out):
    for each in data['logic']:
        if each.is_corresponding_element(in1, in2, out):
            return each
    return None


def _dev_print_logic_possibilities():
    num_ins = len(list(data['inputs']))
    num_outs = len(list(data['outputs']))
    possibilities = num_outs * (num_ins * (num_ins - 1)) / 2
    print(num_ins, num_outs, possibilities)


def get_existing_logic_pairings():
    res = {}
    for fz in data['logic']:
        if not fz.out.name in res:
            res[fz.out.name] = []
        res[fz.out.name].append([fz.in1.name, fz.in2.name])
    return res


def _copy_logic(in1, in2, out):
    return FuzzyLogicElement(in1, in2, out)


def remove_fuzzy_logic_by_name(in_out):
    """Remove all Elements with in_out occurence of in1, in2 or out"""
    to_remove = []
    for each in data['logic']:
        if (each.in1.name == in_out or each.in2.name == in_out or
                each.out.name == in_out):
            to_remove.append(each)
    for each in to_remove:
        data['logic'].remove(each)


def remove_fuzzy_logic(in1, in2, out):
    """Remove Element corresponding with in1, in2 and out"""
    to_remove = []
    for each in data['logic']:
        if (((each.in1.name == in1 and each.in2.name == in2) or
             (each.in1.name == in2 and each.in2.name == in1))
                and
                each.out.name == out):
            to_remove.append(each)
    for each in to_remove:
        data['logic'].remove(each)


def add_fuzzy_logic(in1_lbl, in2_lbl, out_lbl):
    in1 = data['inputs'][in1_lbl]
    in2 = data['inputs'][in2_lbl]
    out = data['outputs'][out_lbl]
    fz = FuzzyLogicElement(in1, in2, out)
    data['logic'].append(fz)
    return fz


def remove_ling_var_from_fuzzy_logic(in_out_lbl, ling_var_lbl):
    for each in data['logic']:
        k = 0
        if in_out_lbl == each.in1.name:
            in_out = each.in1
            k = 1
        elif in_out_lbl == each.in2.name:
            in_out = each.in2
            k = 2
        else:
            return
        
        lv = in_out.ling_var_names()
        lv_idx = lv.index(ling_var_lbl)
        match k:
            case 1:  # horizontal var
                for row in range(len(each.logic)):
                    each.logic[row].pop(lv_idx)
            case 2:  # vertical var
                each.logic.pop(lv_idx)


def add_ling_var_to_fuzzy_logic(in_out_lbl, ling_var_lbl):
    for each in data['logic']:
        k = 0
        if in_out_lbl == each.in1.name:
            in_out = each.in1
            k = 1
        elif in_out_lbl == each.in2.name:
            in_out = each.in2
            k = 2
        else:
            return
        lv = in_out.ling_var_names()
        lv_idx = lv.index(ling_var_lbl)
        match k:
            case 1:  # horizontal var
                for row in range(len(each.logic)):
                    each.logic[row].insert(lv_idx, 'None')
            case 2:  # vertical var
                each.logic.insert(lv_idx, ['None'] * len(each.logic[0]))


def change_ling_var_order_in_fuzzy_logic(in_out_lbl, from_idx, to_idx):
    for each in data['logic']:
        if in_out_lbl == each.in1.name:  # horizontal var
            for row in range(len(each.logic)):
                it = each.logic[row].pop(from_idx)
                each.logic[row].insert(to_idx, it)
        
        elif in_out_lbl == each.in2.name:  # vertical var
            it = each.logic.pop(from_idx)
            each.logic.insert(to_idx, it)


# +++++++++++++++++++++++++++++++++ Fuzzy Vars +++++++++++++++++++++++++++++++
def remove_fuzzy_var(name, isinput=True):
    kind = 'outputs'
    if isinput:
        kind = 'inputs'
    
    remove_fuzzy_logic_by_name(name)
    del data[kind][name]


def add_fuzzy_var(fuzzy_instance, isinput=True):
    kind = 'outputs'
    if isinput:
        kind = 'inputs'
    data[kind][fuzzy_instance.name] = fuzzy_instance


def change_fuzzy_var_name(in_out_old, in_out_new):
    ref = None
    if in_out_old in data['inputs']:
        ref = data['inputs'][in_out_old]
        data['inputs'][in_out_new] = ref
        del data['inputs'][in_out_old]
        ref.name = in_out_new
    elif in_out_old in data['outputs']:
        ref = data['outputs'][in_out_old]
        data['outputs'][in_out_new] = ref
        del data['outputs'][in_out_old]
        ref.name = in_out_new


def add_generic_fuzzy_var(name, isinput=True):
    kind = 'outputs'
    if isinput:
        kind = 'inputs'
    fv = get_generic_fuzzy_var(name)
    
    data[kind][fv.name] = fv
    return fv


def get_generic_fuzzy_var(name):
    """standard values for new Fuzzy Vars"""
    fv = FuzzyVar(name,
                  LinguisticVar(
                      'Low',
                      [0, 50, 100],
                      [1, 0, 0]
                  ),
                  LinguisticVar(
                      'Mid',
                      [0, 50, 100],
                      [0, 1, 0]
                  ),
                  LinguisticVar(
                      'High',
                      [0, 50, 100],
                      [0, 0, 1, ]
                  )
                  )
    return fv


def pretty_print_data():
    pprint.pprint(data)


def get_available_inputs():
    return list(data['inputs'].keys())


def get_available_outputs():
    return list(data['outputs'].keys())


def set_loaded_data(dat):
    global data
    data = dat
