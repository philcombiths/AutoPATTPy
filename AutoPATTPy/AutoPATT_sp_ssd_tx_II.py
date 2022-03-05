"""
Uses AutoPATTPy classes to extract AutoPATT information from a folder of output
for the Spanish SSD Tx Study II. Compares pre/post analyses.

@author: Philip Combiths

# Example use:
directory = SET DIRECTORY PATH
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
                ID = re.findall(r'C\d\d\d', f)[0] # Participant ID format
                phase = re.findall(r'_Pre_|_Post_|_2moPost_|_2wkPost_', f)[0] # list all phases in filenames
                lang = re.findall(r'Spanish|English', f)[0] # list all languages in filenames
                autopatt_objs[ID+phase+lang] = AutoPATT(f, legacy=False) # matching
    return autopatt_objs


def compare_all_SpTx(directory):
    """imports and compares a directory of AutoPATT outputs.
    
    This is intended only for use with Spanish SSD Tx data folders."""
    
    data = import_files_SpTx(directory)
    for variable in ['phonetic_inv', 'phonemic_inv', 'cluster_inv']:
        data['C101_Pre_English'].compare(data['C101_Post_English'], variable)
        data['C102_Pre_English'].compare(data['C102_Post_English'], variable)
        data['C101_Pre_Spanish'].compare(data['C101_Post_Spanish'], variable)
        data['C102_Pre_Spanish'].compare(data['C102_Post_Spanish'], variable)
        data['C101_Post_English'].compare(data['C101_2wkPost_English'], variable)
        data['C101_2wkPost_English'].compare(data['C101_2moPost_English'], variable)
        data['C101_Post_Spanish'].compare(data['C101_2wkPost_Spanish'], variable)
        data['C101_2wkPost_Spanish'].compare(data['C101_2moPost_Spanish'], variable)
        data['C102_Post_English'].compare(data['C102_2wkPost_English'], variable)
        data['C102_2wkPost_English'].compare(data['C102_2moPost_English'], variable)
        data['C102_Post_Spanish'].compare(data['C102_2wkPost_Spanish'], variable)
        data['C102_2wkPost_Spanish'].compare(data['C102_2moPost_Spanish'], variable)
    return data

directory = r'C:\Users\Philip\OneDrive - University of Iowa\Documents - Clinical Linguistics and Disparities Lab\CLD Lab\projects\spanishSSDTx\Phase II Su21\data\autoPATT\02_analysis_20220305\tes'
Sp_data = compare_all_SpTx(directory)