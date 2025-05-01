import os
import pandas as pd
from object_detection.utils import dataset_util
from collections import namedtuple

"""
    matches with label_map.pbtxt
"""
def class_to_int(row_label):
    if row_label == 'enemy':
        return 1
    elif row_label == 'enemy_head':
        return 2
    else:
        print("couldn't convert {row_label}")
        return None
    
def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    grouped = df.groupby(group)
    matched = []
    for filename, obj in zip(grouped.groups.keys(), grouped.groups):
        matched.append(data(filename, obj))
    return matched

