# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 08:08:20 2020
@author: Philip
"""
import os

id_list = input('Enter ID list:').split('\n')

os.chdir(r'C:\Users\Philip\Documents\DPA Excel')

print(os.getcwd())

save_file_list = []
for id in id_list:
    for fname in os.listdir():
        if id in fname:
            print(fname)
            save_file_list.append(fname)

delete_list = []
for fname in os.listdir():
    if fname not in save_file_list:
        delete_list.append(fname)
        
for fname in delete_list:
    pass
    os.remove(fname)

os.close()
