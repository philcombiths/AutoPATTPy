# -*- coding: utf-8 -*-
"""
Uses AutoPATTPy classes to extract AutoPATT information from a folder of output
for the Spanish SSD Tx Study. Compares pre/post analyses.

@author: Philip Combiths

# Example use:
directory = r'E:\My Drive\Phonological Typologies Lab\Projects\Spanish SSD Tx\Data\Processed\ICPLA 2020_2021\AutoPATT'
Sp_data = compare_all_SpTx(directory)
"""

import os
import re
from AutoPATTPy import AutoPATT, change_dir

###
###
### Specialized functions for Spanish SSD Tx Study.
###
###


def import_files_SpTx(directory):
    """Imports a directory of AutoPATT outputs as a dict of AutoPATT objects.
    
    This is intended only for use with Spanish SSD Tx data folders."""
    
    autopatt_objs = {}
    with change_dir(directory):
        for f in os.listdir(directory):
            if f.endswith('.csv'):
                ID = re.findall('S\d\d\d', f)[0]
                phase = re.findall('Pre|Post', f)[0]
                autopatt_objs[ID+phase] = AutoPATT(f, legacy=True)
    return autopatt_objs


def compare_all_SpTx(directory):
    """imports and compares a directory of AutoPATT outputs.
    
    This is intended only for use with Spanish SSD Tx data folders."""
    
    data = import_files_SpTx(directory)
    for variable in ['phonetic_inv', 'phonemic_inv', 'cluster_inv']:
        data['S101Pre'].compare(data['S101Post'], variable)
        data['S102Pre'].compare(data['S102Post'], variable)
        data['S104Pre'].compare(data['S104Post'], variable)
        data['S107Pre'].compare(data['S107Post'], variable)
        data['S108Pre'].compare(data['S108Post'], variable)
    return data

directory = r'E:\My Drive\Phonological Typologies Lab\Projects\Spanish SSD Tx\Data\Processed\ICPLA 2020_2021\AutoPATT'
Sp_data = compare_all_SpTx(directory)