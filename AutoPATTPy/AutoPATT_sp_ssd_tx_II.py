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
                ID = re.findall('C\d\d\d', f)[0]
                phase = re.findall('Pre|Post', f)[0]
                lang = re.findall('Spanish|English', f)[0]
                autopatt_objs[ID+phase+lang] = AutoPATT(f, legacy=False)
    return autopatt_objs


def compare_all_SpTx(directory):
    """imports and compares a directory of AutoPATT outputs.
    
    This is intended only for use with Spanish SSD Tx data folders."""
    
    data = import_files_SpTx(directory)
    for variable in ['phonetic_inv', 'phonemic_inv', 'cluster_inv']:
        data['C101PreEnglish'].compare(data['C101PostEnglish'], variable)
        data['C102PreEnglish'].compare(data['C102PostEnglish'], variable)
        data['C101PreSpanish'].compare(data['C101PostSpanish'], variable)
        data['C102PreSpanish'].compare(data['C102PostSpanish'], variable)
    return data

directory = r'D:\Data\test'
Sp_data = compare_all_SpTx(directory)