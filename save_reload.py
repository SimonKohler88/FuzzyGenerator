#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle
import json

def save_to_file_pickle(file, data):
    r = pickle.dumps(data)
    with open(file, 'wb') as f:
        f.write(r)

def load_from_file_pickle(file):
    with open(file, 'rb') as f:
        d = f.read()
    return pickle.loads(d)


def save_to_file_json(file, data_dict):
    r = json.dumps(data_dict, indent=4)
    with open(file, 'w') as f:
        f.write(r)

def load_from_file_json(file):
    with open(file, 'r') as f:
        d = f.read()
    return json.loads(d)
