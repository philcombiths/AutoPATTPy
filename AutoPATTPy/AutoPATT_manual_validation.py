# -*- coding: utf-8 -*-
"""
AutoPATT Validation Project-specific function using AutoPATTPy functions to extract and compare
AutoPATT data to manual PATT data.


Created on Thu Oct  1 15:37:51 2020
@author: Philip Combiths

"""
import pandas as pd
import ast
from AutoPATTPy import import_files, compare_all

def validation_proj_data(dir_manual_data, dir_auto_data): 

    """
    Exports comparison data in three formats as csv files to this file's directory.
    """
    
    # Set data directories
    dir_manual = dir_manual_data
    dir_auto = dir_auto_data
    
    # Compare AutoPATT Results
    data_manual = import_files(dir_manual, legacy=True, robust=True)
    data_auto = import_files(dir_auto, legacy=True)
    # Manual = L, Auto = R
    
    all_results = compare_all(data_manual, data_auto)
    
    # Create full empty DF      
    results_df = pd.DataFrame(index=[i for i in all_results.keys()], columns=[i for i in all_results['phonetic_inv'].keys()])
    for type_key in all_results.keys():
        for ID_key in all_results[type_key].keys():            
            results_df.at[type_key, ID_key] = all_results[type_key][ID_key]
            
    # Create mismatch DF
    mismatch_df = pd.DataFrame(index=[i for i in all_results.keys()], columns=[i for i in all_results['phonetic_inv'].keys()])
    for type_key in all_results.keys():
        for ID_key in all_results[type_key].keys():            
            # Skip items with no errors
            if len(all_results[type_key][ID_key][f"{ID_key} L unique"]) == 0:
                if len(all_results[type_key][ID_key][f"{ID_key} R unique"]) == 0:
                    continue
            L_mismatch = all_results[type_key][ID_key][f"{ID_key} L unique"]
            R_mismatch = all_results[type_key][ID_key][f"{ID_key} R unique"]
            mismatch_df.at[type_key, ID_key] = [L_mismatch, R_mismatch]
            
    # Create wider DF
    index_names = []
    for tri in zip([i for i in all_results.keys()], 
                    [i+'_AUTO_omit' for i in all_results.keys()],
                    [i+'_AUTO_add' for i in all_results.keys()]):
        index_names += tri        
    wider_df = pd.DataFrame(index=index_names, columns=[i for i in all_results['phonetic_inv'].keys()])
    for type_key in all_results.keys():
        for append in ['', '_AUTO_omit', '_AUTO_add']:            
            for ID_key in all_results[type_key].keys():       
                if append == '':
                    index = 'overlap'
                if append == '_AUTO_omit':
                    index = f'{ID_key} L unique'
                if append == '_AUTO_add':
                    index = f'{ID_key} R unique'
                wider_df.at[type_key+append, ID_key] = all_results[type_key][ID_key][index]
    # Export to CSV
    results_df.to_csv('results_data.csv',encoding='utf-8')
    mismatch_df.to_csv('mismatch_data.csv',encoding='utf-8')
    wider_df.to_csv('wider_data.csv',encoding='utf-8')
    return all_results, data_manual, data_auto

def intake_comparison_overlap(comparison_overlap_path):
    """
    imports a csv with analyses overlap labels as index and participant IDs
    as column labels. Data are lists of elements overlapping across manual
    and AutoPATT data.
    """
    # Import raw data
    raw_df = pd.read_csv(comparison_overlap_path, encoding='utf-8', index_col=0)
    
    # Convert
    long_tuples = []
    for col in raw_df.iteritems():
        for cell in col[1].iteritems():           
            pass
            try:    
                overlap = ast.literal_eval(cell[1])
            except ValueError:
                error_col = col
                error_cell = cell
                print(f"ERROR: {cell[1]}")
            for element in overlap:
                cur_tuple = (col[0], cell[0], element)
                long_tuples.append(cur_tuple)

    new_df = pd.DataFrame(long_tuples, columns=['ID', 'analysis', 'IPA'])
    new_df.set_index(['ID', 'analysis'], inplace=True)
    new_df.to_csv('overlap_data_long.csv', encoding='utf-8')
    return new_df
    
###
# Use Case
###

# dir_manual_data = r'E:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\Manual PATT Data\Manual PATT Data - Corrected'
# dir_auto_data = r'E:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\AutoPATT Data'
# all_results, data_manual, data_auto = validation_proj_data(dir_manual_data, dir_auto_data)

# test1 = data_auto['1676']
# test3 = data_auto['1713']

comparison_overlap_path = "E:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\Processed Data\manual_edits\overlap_comparison_data.csv"
overlap_data_long = intake_comparison_overlap(comparison_overlap_path)
