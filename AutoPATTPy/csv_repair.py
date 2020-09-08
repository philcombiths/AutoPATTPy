# -*- coding: utf-8 -*-
"""
Auxiliar functions for AutoPATTPy which repair edited or manually generated 
output to match format of AutoPATT.

Created on Tue Sep  8 15:31:49 2020
@author: Philip   
"""

from tempfile import NamedTemporaryFile
import os
import shutil
import csv
from contextmanager import enter_dir, change_dir


def csv_repair(source_path):
    """Adds an empty minimal pairs section to an AutoPATT output csv."""
    tempfile = NamedTemporaryFile('w+t', newline='', encoding='utf-8', delete=False)
    with open(source_path, mode='r', encoding='utf-8') as file, tempfile:
        reader = csv.reader(file, delimiter=',', )
        writer = csv.writer(tempfile, delimiter=',')        
        phonetic_inv_passed=False
        blanks_passed=0
        rows_added=False
        for i, row in enumerate(reader):
            # Get number of columns
            if i == 0:
                num_cols = len(row)
            if row[0] == 'PHONETIC INVENTORY:':
                phonetic_inv_passed=True
            # Identify row immediately prior to insertion point
            if row[0] == '' and phonetic_inv_passed:
                blanks_passed+=1
                writer.writerow(row)
                continue
            if blanks_passed == 2 and not rows_added:
                # Check for existence of 'Minimal Pairs' row
                if row[0] == 'Minimal Pairs:':
                    tempfile.close()
                    os.remove(tempfile.name)
                    return
                # Add inserted rows
                else:
                    writer.writerow(['Minimal Pairs:']+['']*(num_cols-1))
                    writer.writerow(['']*num_cols)
                    writer.writerow(['']*num_cols)
                    rows_added=True
                    writer.writerow(row)
                    continue
            writer.writerow(row)        
        tempfile.close()
        shutil.move(tempfile.name, source_path)        
    return   
    pass


def dir_csv_repair(directory):
    """runs csv_repair() on all csv files in a directory."""
    with change_dir(directory):
        for f in os.listdir(directory):
            if f.endswith('.csv'):
                csv_repair(f)
    return