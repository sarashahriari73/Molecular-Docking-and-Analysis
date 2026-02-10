# Original script developed by Dr.  Tâp Ha-Duong 
# Adapted and modified by Sara Shahriari for Smoothened receptor and its ligands interaction analysis
# Modifications include: input handling, figure formatting, data selection

################################################################################
# This script reads a receptor.pdb and an occurences.dat files
# and outputs another pdb file containing the contacting residue occurence
################################################################################

import sys
import time
import math
import numpy as np

################################################################################

def read_rec(file_name): 
    recpdbfile = [] 
    with open(file_name, "r") as g: 
        lines = g.readlines() 
        for l in lines: 
            if "ATOM" in l or "HETATM" in l: 
                if "H" not in l.split()[2]: 
                   splitted_line = l.split() 
                   h = splitted_line[0]
                   n = int(splitted_line[1]) 
                   a = splitted_line[2]
                   r = splitted_line[3]
                   # Fix: account for chain ID in column 5
                   if splitted_line[4].isalpha():  # chain present
                       s = int(splitted_line[5])
                       x = float(splitted_line[6]) 
                       y = float(splitted_line[7])
                       z = float(splitted_line[8])
                       u = float(splitted_line[9])
                       b = float(splitted_line[10])
                   else:  # no chain ID
                       s = int(splitted_line[4]) 
                       x = float(splitted_line[5]) 
                       y = float(splitted_line[6])
                       z = float(splitted_line[7])
                       u = float(splitted_line[8])
                       b = float(splitted_line[9])
                   recpdbfile.append([h, n, a, r, s, x, y, z, u, b]) 
    g.close() 
    return recpdbfile 
 
################################################################################

def read_occ(file_name): 
    percentocc = [] 
    with open(file_name, "r") as f: 
        lines = f.readlines() 
        for l in lines: 
            line_splitted = l.split() 
            resid = int(line_splitted[1]) 
            occur = float(line_splitted[2]) 
            percentocc.append([resid, 100*occur/5000]) 
    f.close() 
    return percentocc

################################################################################

rec_file_name = sys.argv[1] 
occ_file_name = sys.argv[2] 

recpdbfile = read_rec(rec_file_name) 
percentocc = read_occ(occ_file_name) 

################################################################################

with open("receptor_contacts.pdb", "a") as h:
    for elem in recpdbfile: 
        ilis = elem[4]
        for occu in percentocc:
            if occu[0] == ilis:
                elem[9] = occu[1]
    for elem in recpdbfile: 
        h.write(f"{elem[0]:6s}{elem[1]:5d} {elem[2]:^4s} {elem[3]:3s}  {elem[4]:4d}    {elem[5]:8.3f}{elem[6]:8.3f}{elem[7]:8.3f}{elem[8]:6.2f}{elem[9]:6.2f} \n")
    h.close()
