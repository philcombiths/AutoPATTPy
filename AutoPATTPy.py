# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:43:03 2020

@author: Philip

Various functions for use with AutoPATT output
"""

from ntpath import basename
import io
import os
import pandas as pd
import re
from contextlib import contextmanager

@contextmanager
def enter_dir(newdir):
    prevdir = os.getcwd()
    try:
        yield os.chdir(newdir) 
    finally:
        os.chdir(prevdir)
        
        
@contextmanager
def change_dir(newdir):
    prevdir = os.getcwd()
    try:
        yield os.chdir(os.path.expanduser(newdir)) 
    finally:
        os.chdir(prevdir)

# Class AutoPATT Session
class AutoPATT(object):
    """
    Represents an AutoPATT csv output file in Python
    """
    def __init__(self, source_path, legacy=False):
        """Instantiates an AutoPATT object with relevant data from the output.
        
        Output data are stored asattributes within the object. To access 
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
            phonetic_inv_rows = output[i_pt_inv_start:i_mp_start-2]
            self.phonetic_inv = [x.split(',')[1:] for x in phonetic_inv_rows]
            self.phonetic_inv = [j for i in self.phonetic_inv for j in i]
            self.phonetic_inv = [x for x in self.phonetic_inv if x != ' ']
            # Get minimal pairs
            self.minimal_pairs = output[i_mp_start:i_pm_inv_start-3]
            self.minimal_pairs = [x.split(',') for x in self.minimal_pairs]
            # Get phonemic inventory
            phonemic_inv_rows = output[i_pm_inv_start:i_cl_inv-1]
            self.phonemic_inv = [x.split(',')[1:] for x in phonemic_inv_rows]
            self.phonemic_inv = [j for i in self.phonemic_inv for j in i]
            self.phonemic_inv = [x for x in self.phonemic_inv if x != ' ']
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
    
    def __repr__(self):
        return f'AutoPATT object {self.name}'
    
    
    def var_to_df(self, var, label=None):
        """Converts a variable to a pandas dataframe an AutoPATT object,
        
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
        """Compares inventories of two AutoPATT objects."""
        attr_left = getattr(self, var)
        attr_right = getattr(other, var)
        
        overlap_dict = {'overlap':set()}
        unique_dict = {self.name+' unique':set(), other.name+' unique':set()}
        for x in attr_left:
            if x in attr_right:
                overlap_dict['overlap'].add(x)
            else:
                unique_dict[self.name+' unique'].add(x)
        for x in attr_right:
            if x not in attr_left:
                unique_dict[other.name+' unique'].add(x)                
        print('Overlap:')
        print(overlap_dict['overlap'])
        print(f'Unique {self.name}:')
        print(unique_dict[self.name+' unique'])
        print(f'Unique {other.name}:')
        print(unique_dict[other.name+' unique'])
        return overlap_dict, unique_dict
    

def import_files(directory):
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


def compare_all():
    """imports and compares a directory of AutoPATT outputs.
    
    This is intended only for use with Spanish SSD Tx data folders."""
    
    data = import_files(directory)
    for variable in ['phonetic_inv', 'phonemic_inv', 'cluster_inv']:
        data['S101Pre'].compare(data['S101Post'], variable)
        data['S102Pre'].compare(data['S102Post'], variable)
        data['S104Pre'].compare(data['S104Post'], variable)
        data['S107Pre'].compare(data['S107Post'], variable)
        data['S108Pre'].compare(data['S108Post'], variable)
    return data
        
def compare_text(inv_left, inv_right):
    """Compares two text inventories."""
    inv_left = inv_left.replace(' ', '').split(',')
    inv_right = inv_right.replace(' ', '').split(',')
    overlap_dict = {'overlap':set()}
    unique_dict = {'L unique':set(),'R unique':set()}
    for x in inv_left:
        if x in inv_right:
            overlap_dict['overlap'].add(x)
        else:
            unique_dict['L unique'].add(x)
    for x in inv_right:
        if x not in inv_left:
            unique_dict['R unique'].add(x)                
    print('Overlap:')
    print(overlap_dict['overlap'])
    print(f'Unique L:')
    print(unique_dict['L unique'])
    print(f'Unique R:')
    print(unique_dict['R unique'])
    return overlap_dict, unique_dict        


directory = 'G:\My Drive\Phonological Typologies Lab\Projects\Spanish SSD Tx\Data\Processed\ICPLA 2020_2021\AutoPATT'

data = compare_all()


    
    
    
        
        

                    
                    
                