# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:29:06 2020

@author: Philip
"""
import os
from AutoPATTPy import change_dir


def file_rename(directory):
    """Truncates filenames in directory up to first "_" only, preserving extension."""
    with change_dir(directory):
        for file in os.listdir(directory):
            if file.endswith('.csv'):
                if '_' in file:
                    file_rev = f"{file.split('_')[0]}.{file.split('.')[-1]}"
                    print(f"{file} --> {file_rev}")
                    os.rename(file, file_rev)
    print('Done.')
    return


if __name__=='__main__':
    directory = r'G:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\AutoPATT Data'
    file_rename(directory)    