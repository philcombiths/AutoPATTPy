# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:29:06 2020

@author: Philip
"""
import os
from AutoPATTPy import change_dir


def file_rename(directory, filetypes=None, filetypes_exclude=('.ini'), 
                filename_splitter='_', truncate_index=0):
    """
    Truncates filenames, preserving extension.
    
    Parameters:
        directory : directory of files to be renamed
        filetypes : str or tuple of extensions to be included in renaming (optional).
        filetypes_excluded : str or tuple of extensions to be excluded in renaming. Default = '.ini'
        filename_splitter : str of splitter to use for truncating.
        truncate_index : int index of splitter to use for truncating.
    """    
    with change_dir(directory):
        for file in os.listdir(directory):
            # Skip excluded filetypes
            if file.endswith(filetypes_exclude):
                continue
            # Rename all files if filetypes not specified
            if filetypes==None:
                if filename_splitter in file:
                    file_rev = f"{file.split('_')[truncate_index]}.{file.split('.')[-1]}"
                    print(f"{file} --> {file_rev}")
                    os.rename(file, file_rev)                
            # Rename only filetypes specified
            else:                
                if file.endswith(filetypes):
                    if filename_splitter in file:
                        file_rev = f"{file.split('_')[truncate_index]}.{file.split('.')[-1]}"
                        print(f"{file} --> {file_rev}")
                        os.rename(file, file_rev)
    print('Done.')
    return


if __name__=='__main__':
    directory = r'G:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\AutoPATT Data'
    file_rename(directory, '.csv')