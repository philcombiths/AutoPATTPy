"""
Uses AutoPATTPy classes to extract AutoPATT information from a folder of output
for the Spanish SSD Tx Study II. Compares pre/post analyses.

@author: Philip Combiths
@created: 2024-01-07
@modified: 2024-01-07

# Example use:
directory = SET DIRECTORY PATH
Sp_data = compare_all_SpTx(directory)
"""

import itertools
import os
import re

from AutoPATTPy import AutoPATT, change_dir

###
###
### Specialized functions for Spanish SSD Tx Study Phase III.
###
###


def import_files_SpTx(directory):
    """Imports a directory of AutoPATT outputs as a dict of AutoPATT objects.
    
    This is intended only for use with Spanish SSD Tx data folders."""
    
    autopatt_objs = {}
    ID_set = []
    phase_set = []
    lang_set = []
    
    with change_dir(directory):
        for f in os.listdir(directory):
            if f.endswith('.csv'):
                ID = re.findall(r'S\d\d\d', f)[0] # Participant ID format
                phase = re.findall(r'_Pre_|_Post_|_2moPost_|_2wkPost_|_1moPost_', f)[0] # list all phases in filenames
                lang = re.findall(r'EFE|LittlePEEP|English|Spanish', f)[0] # list all languages in filenames
                autopatt_objs[ID+phase+lang] = AutoPATT(f, legacy=False) # matching
                ID_set.append(ID)
                phase_set.append(phase.strip("_"))
                lang_set.append(lang)
    return [autopatt_objs, [set(ID_set), set(phase_set), set(lang_set)]]


def compare_all_SpTx(directory):
    """imports and compares a directory of AutoPATT outputs.
    
    This is intended only for use with Spanish SSD Tx data folders."""
    
    data_list = import_files_SpTx(directory)
    data = data_list[0]
    comparison_list = []
    for variable in ['phonetic_inv', 'phonemic_inv', 'cluster_inv']:
        for info in itertools.product(data_list[1][0], data_list[1][2]):
            id = info[0]
            lang = info[1]
            comparison = data[f'{id}_Pre_{lang}'].compare(data[f'{id}_Post_{lang}'], variable)
            comparison_list.append((f'{id}_{lang}_{variable}_Pre-Post', comparison))
            pass
    return [data, comparison_list]

directory = "/Users/pcombiths/Library/CloudStorage/OneDrive-UniversityofIowa/Offline Work/SSD Tx III - BHL/analysis/autopatt"

# res = import_files_SpTx(directory)
Sp_data = compare_all_SpTx(directory)
pass