# -*- coding: utf-8 -*-
"""


Created on Thu Jul  2 14:43:03 2020
@author: Philip

Various functions for use with AutoPATT output

# Use example: AutoPATT class
source_path = 'path_to_an_AutoPATT output'
AutoPATT(source_path, legacy=False)

# Use example: 
data = import_files(directory_of_outputs, legacy=False)

# Use example: csv_repair and older AutoPATT versions
# For use with edited or manually generated output to match format of AutoPATT
# generated output
data = import_files(directory_needing_repair, legacy=True)

"""

from ntpath import basename
import io
import os
import pandas as pd
import regex as re
from contextmanager import enter_dir, change_dir
from csv_repair import dir_csv_repair


# Class AutoPATT Session
class AutoPATT(object):
    """
    Represents an AutoPATT csv output file in Python
    """
    def __init__(self, source_path, legacy=False, robust=False):
        """Instantiates an AutoPATT object with relevant data from the output.
        
        Parameters:
            source_path : str, path to source AutoPATT output file
            legacy : bool, set to True for compatibility with AutoPATT output
                 < v0.7. Set to to False for compatibility with >= v0.7. 
                 Default = False
            robust : bool, set to True to coerce some nonstandard IPA elements 
                     to standard IPA. Default=False
        
        Note: Output data are stored as attributes within the object. To access 
              attributes, use AUTOPATT-OBJECT.ATTR-NAME. For example: 
              myAutoPATTsession.out_phones
        
        Attributes:
            source: (str) absolute path to source AutoPATT output file
            name: (str) source output file name
            file_location: (str) absolute path to source file directory
            output: string containing contents of AutoPATT output file
            version: (str) AutoPATT version number
            lang: (str) language of AutoPATT analysis
            session: list of session in AutoPATT analysis
            corpus: list of corpora in AutoPATT analysis
            total_records: (int) number of Phon records in AutoPATT analysis
            records: (list) of numbers of Phon records in AutoPATT analysis
            analysis_date: (str) date of AutoPATT analysis
            analysis_time: (str) time of AutoPATT analysis
            phonetic_inv: list of phones as strings in phonetic inventory
            minimal_pairs: list of list of strings containing minimal pairs
            phonemic_inv: list of phones as strings in phonemic inventory
            cluster_inv: list of clusters as strings in cluster inventory
            targets: list of targets as strings
            out_phones: list of phones (str) missing from phonetic inventory
            out_phonemes: list of phonemes (str) missing from phonemic 
                inventory
            out_clusters: list of clusters (str) missing from cluster inventory
        """               
        # Attributes stored in the AutoPATT object
        self.source = os.path.abspath(source_path)
        self.name = basename(source_path)[:basename(source_path).rfind(".")]
        self.file_location = '\\'.join(os.path.abspath(
            source_path).split('\\')[:-1])                       
        with io.open(self.source, mode='r', encoding='utf-8') as infile:            
            # Read source AutoPATT output file as a list of strings
            output = infile.readlines()
            output = [i.strip().strip(',\n') for i in output]
            output = [i.replace('"', '') for i in output]
            output = [i for i in output if i]           
            # Use anchor rows to get row indices
            if legacy:
                pass
            else:
                i_sesrow_end = output.index('Analysis date:')-2
                i_date = output.index('Analysis date:')+1
                i_ver = output.index('Analysis date:')-2
                i_lang = output.index('Analysis date:')-1
            if self.name == '1049':
                print('got it)')
                print('got it')
                pass
            i_pt_inv_start = output.index('PHONETIC INVENTORY:')+2
            i_mp_start = output.index('Minimal Pairs:')+1
            i_pm_inv_start = output.index('PHONEMIC INVENTORY:')+2
            i_cl_inv = output.index('CLUSTER INVENTORY:')+1
            i_targ = [
                x.startswith('TARGETS') for x in output].index(True)+1           
            i_pt_out = output.index('Phones to monitor:')+1
            i_pm_out = output.index('Phonemes to monitor:')+1
            i_cl_out = output.index('Clusters to monitor:')+1           
            # Derive attributes from AutoPATT output string            
            self.output = output            
            if legacy:
                pass
            else:
                self.version = float(output[i_ver].split(' ')[2])
                self.lang = output[i_lang][output[i_lang].rfind(':')+2:]
                # Separate rows with session information
                sesrows = output[:i_sesrow_end]
                sesrows = sesrows[1::2]
                self.session = [x.split(',')[0] for x in sesrows]
                self.corpus = [x.split(',')[1] for x in sesrows]
                self.total_records = sum([int(x.split(',')[2]) for x in sesrows])            
                self.records = [int(x.split(',')[2]) for x in sesrows]
                self.analysis_date = output[i_date].split(' ')[0]
                self.analysis_time = output[i_date].split(' ')[1]
            # Get phonetic inventory
            phonetic_inv_rows = output[i_pt_inv_start:i_mp_start-1]
            self.phonetic_inv = [x.split(',')[1:] for x in phonetic_inv_rows]
            self.phonetic_inv = [j for i in self.phonetic_inv for j in i]
            self.phonetic_inv = [x for x in self.phonetic_inv if x.strip() != '']
            # Get minimal pairs
            self.minimal_pairs = output[i_mp_start:i_pm_inv_start-2]
            self.minimal_pairs = [x.split(',') for x in self.minimal_pairs]
            # Get phonemic inventory
            phonemic_inv_rows = output[i_pm_inv_start:i_cl_inv-1]
            self.phonemic_inv = [x.split(',')[1:] for x in phonemic_inv_rows]
            self.phonemic_inv = [j for i in self.phonemic_inv for j in i]
            self.phonemic_inv = [x for x in self.phonemic_inv if x.strip() != '']
            # Get cluster inventory
            self.cluster_inv = output[i_cl_inv].split(',')
            # Get targets
            self.targets = output[i_targ].split(',')
            # Get out phones to monitor
            self.out_phones = output[i_pt_out].split(',')
            # Get out phonemes to monitor
            self.out_phonemes = output[i_pm_out].split(',')
            # Get out clusters to monitor
            self.out_clusters = output[i_cl_out].split(',')            
            # Robust setting coerces nonstandard IPA elements to standard IPA
            if robust:
                att_list = [self.phonetic_inv, self.minimal_pairs, 
                            self.phonemic_inv, self.cluster_inv, self.targets,
                            self.out_phones, self.out_phonemes, self.out_clusters]
                for i, att in enumerate(att_list):
                    for num, x in enumerate(att_list[i]):
                        try:                                              
                            att_list[i][num] = att_list[i][num].replace('g', 'ɡ')
                # Replacements for minimal pairs
                        except AttributeError: 
                            for ix, word in enumerate(att_list[i][num]):
                                att_list[i][num][ix] = att_list[i][num][ix].replace('g', 'ɡ')
                            
    
    def __repr__(self):
        return f'AutoPATT object {self.name}'
    
    
    def var_to_df(self, var, label=None):
        """Converts a variable to a pandas dataframe from an AutoPATT object,
        
        Args: 
            var: a string representing an AutoPATT attribute variable. See AutoPATT
                Class for available variables.
            label: optional string name for Series. Default self.name
        
        Returns:
            dataframe
        """
        if not label:
            label = self.name   
            
        attribute = getattr(self, var)
        if isinstance(attribute, list):
            df = pd.Series(attribute, name=label)
        return df


    def compare(self, other, var):
        """
        Compares inventories of two AutoPATT objects.
        Parameters:
            other : AutoPATT object to compare with self.
            var : AutoPATT object variable to be compared.
        """
        attr_left = getattr(self, var)
        attr_right = getattr(other, var)
        
        result_dict = {'overlap':[], 
                       self.name+' L unique':[], 
                       other.name+' R unique':[]}
        for x in attr_left:
            if x in attr_right:
                result_dict['overlap'].append(x)
            else:
                result_dict[self.name+' L unique'].append(x)
        for x in attr_right:
            if x not in attr_left:
                result_dict[other.name+' R unique'].append(x)                
        print('Overlap:')
        print(result_dict['overlap'])
        print(f'Unique L {self.name}:')
        print(result_dict[self.name+' L unique'])
        print(f'Unique R {other.name}:')
        print(result_dict[other.name+' R unique'])
        return result_dict
    
  
def compare_text(inv_left, inv_right):
    """
    Compares two string/text inventories. 
    Inventories must be in format: 'element, element, element, ...'
    """
    inv_left = inv_left.replace(' ', '').split(',')
    inv_right = inv_right.replace(' ', '').split(',')
    result_dict = {'overlap':[], 'L unique':[], 'R unique':[]}
    for x in inv_left:
        if x in inv_right:
            result_dict['overlap'].append(x)
        else:
            result_dict['L unique'].append(x)
    for x in inv_right:
        if x not in inv_left:
            result_dict['R unique'].append(x)                
    print('Overlap:')
    print(result_dict['overlap'])
    print('Unique L:')
    print(result_dict['L unique'])
    print('Unique R:')
    print(result_dict['R unique'])
    return result_dict


def compare_all(dict_left, dict_right):
    """
    Compares all AutoPATT analysis results for two dictionaries of AutoPATT
    objects. Compared dictionaries must have identical keys.
    
    Returns dictionary of compared results.
    """
    
    analysis_list = ['phonetic_inv', 'phonemic_inv', 'cluster_inv', 
                     'out_phones', 'out_phonemes', 'out_clusters', 'targets']
    all_results = {}
    
    for analysis in analysis_list:        
        comparison_result = {}    
        for key in dict_left.keys():
            result = dict_left[key].compare(dict_right[key], analysis)
            comparison_result[key] = result
        all_results[analysis] = comparison_result
    return all_results


def import_files(directory, legacy=False, minimal_pairs_repair=False, robust=False):
    """
    Imports a directory of AutoPATT outputs as a dict of AutoPATT objects.
    
    Parameters:
        directory : path to directory of AutoPATT outputs
        legacy : bool, set to True for compatibility with AutoPATT output
                 < v0.7. Set to to False for compatibility with >= v0.7. 
                 Default = False
        minimal_pairs_repair : bool, set to True to execute dir_csv_repair, 
                               dummy minimal pairs section and other
                               adjustments for manually generated output. 
                               WARNING: THIS MODIFIES THE ORIGINAL FILES.
        robust : bool, set to True to coerce some nonstandard IPA elements 
                 to standard IPA. Default=False
    
    Returns dictionary of AutoPATT objects
    """    
    
    autopatt_objs = {}
    with change_dir(directory):
        # First repair output if minimual_pairs_repair specified
        if minimal_pairs_repair:
            print('WARNING: YOU ARE ABOUT TO MODIFY ORIGINAL FILES FOR COMPATIBILITY')
            if input("To proceed, input OK: ") == 'OK':
                dir_csv_repair(directory)
                'Original files modified for compatibility.'
            else:
                print('Proceeding without modifying original files.')
        # Generate AutoPATT objects
        for f in os.listdir(directory):
            if f.endswith('.csv'):
                ID = f.replace('.csv', '')                           
                autopatt_objs[ID] = AutoPATT(f, legacy=legacy, robust=robust)
    print('AutoPATT objects added to dictionary')
    return autopatt_objs    


def gen_output(autopatt_dict_left, autopatt_dict_right):
    """"Generates a dataframe with columns for two sets of AutoPATT data"""
    
    
###
###
### Testing
###
###
    
if __name__ == '__main__':
    
    #directory_repair = r'G:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\Manual PATT Data - Copy'
    #directory_test = r'G:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\test'
    #data = import_files(directory_repair, legacy=True)
    dir_manual = r'E:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\Manual PATT Data\Manual PATT Data - Corrected'
    dir_auto = r'E:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\AutoPATT Data'

    # Compare AutoPATT Results
    data_manual = import_files(dir_manual, legacy=True, robust=True)
    data_auto = import_files(dir_auto, legacy=True)
    # Manual = L, Auto = R
    all_results = compare_all(data_manual, data_auto)
    
    P1049_auto = AutoPATT(r"E:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\AutoPATT Data\1049.csv", legacy=True, robust=False)
    P1049 = AutoPATT(r"E:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\test\1049.csv", legacy=True, robust=True)
    P1007 = AutoPATT(r"E:\My Drive\Phonological Typologies Lab\Projects\AutoPATT\Manual PATT Validation\test\1007_PKP_Pre_AutoPATT_v1_4.csv", legacy=True)
    
    # TO Do
    # arrange comparison data in a format I can work with.
    
    # Create dataframe for each 
        
    # For each analysis
    
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
    # mismatch_df.to_csv('mismatch_data.csv',encoding='utf-8')

    
    
        
        

                    
                    
                