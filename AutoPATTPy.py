# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:43:03 2020

@author: Philip

Various functions for use with AutoPATT output
"""

from ntpath import basename
import io
import re
import os


# Class AutoPATT Session
class AutoPATT(object):
    """
    Represents an AutoPATT csv output file in Python
    """
    def __init__(self, sourcePath):
        """
        Instantiates an AutoPATT object with relevant data from the output
        stored to instance variables within the object.
        
        To access instance variables, use AUTOPATT-OBJECT.VAR-NAME
            For example: myAutoPATTsession.out_phones
        """
                
        # Instance variables stored in the AutoPATT object
        self.source = os.path.abspath(sourcePath)
        self.name = basename(sourcePath)[:basename(sourcePath).rfind(".")]
        self.fileLocation = '\\'.join(os.path.abspath(
                                        sourcePath).split('\\')[:-1])        
        self.output = None
        self.version = None
        self.lang = None
        self.session = None
        self.corpus = None
        self.total_records = None
        self.records = None
        self.analysis_date = None
        self.analysis_time = None
        self.phonetic_inv = None
        self.minimal_pairs = None
        self.phonemic_inv = None
        self.targets = None
        self.out_phones = None
        self.out_phonemes = None
        self.out_clusters = None
               
        with io.open(self.source, mode='r', encoding='utf-8') as inFile:
            
            # Read source AutoPATT output file as a list of strings
            output = inFile.readlines()
            output = [i.strip().strip(',\n') for i in output]
            output = [i.replace('"', '') for i in output]
            output = [i for i in output if i]
            
            # Use anchor rows to get row indices
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
            
            # Derive instance variables from AutoPATT output string            

            self.output = output
            self.version = output[i_ver]
            self.lang = output[i_lang][output[i_lang].rfind(':')+2:]
            # Separate rows with session information
            sesrows = output[:i_sesrow_end]
            sesrows = sesrows[1::2]
            self.session = [x.split(',')[0] for x in sesrows]
            self.corpus = [x.split(',')[1] for x in sesrows]
            self.total_records = sum([int(x.split(',')[1]) for x in sesrows])
            self.records = [int(x.split(',')[1]) for x in sesrows]
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
            # Get targets
            self.targets = output[i_targ].split(',')
            # Get out phones to monitor
            self.out_phones = output[i_pt_out].split(',')
            # Get out phonemes to monitor
            self.out_phonemes = output[i_pm_out].split(',')
            # Get out clusters to monitor
            self.out_clusters = output[i_cl_out].split(',')
            
            # Warn user if unrecognized AutoPATT version
            if self.version != 'AutoPATT version 0.7':
                print('*********************************************')
                print(f'WARNING: {self.version} output file detected.')
                print('\Intended for use with AutoPATT version 0.7')
                print('*********************************************')
    
    def __repr__(self):
        return f'AutoPATT object {self.name}'

                    
                    
                