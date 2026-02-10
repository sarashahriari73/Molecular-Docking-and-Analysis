# Original script developed by Dr.  Tâp Ha-Duong 
# Adapted and modified by Sara Shahriari for Smoothened receptor and its ligands interaction analysis
# Modifications include: input handling, figure formatting, data selection

################################################################################
# This script computes the occurrences of the residues inside the residues.dat file and prints them in a file called 'occurences.dat'
################################################################################

import sys

def read_pdb(file_name): 
    residues = []    
    with open(file_name, "r") as g:
        lines = g.readlines()
        for l in lines:
            if "ATOM" in l or "HETATM" in l: 
                splitted_line = l.split()
                resid = splitted_line[3] + splitted_line[4]
                if len(residues) == 0 or resid != residues[-1]:
                    residues.append(resid)
        g.close()
    return residues

def count_occ(a_list): 
    occ = {}
    for res in resi:
        occ[res] = 0  
    for res in a_list:
        if res in a_list:
            occ[res] += 1
    with open('occurences.dat', 'w') as g:
        for elem in occ:
            g.write(f'{elem[:3]} {elem[3:6]}   {occ[elem]}\n')
        g.close()

rec_file_name = sys.argv[1] 
resi = read_pdb(rec_file_name)

# we calculate the occurrencies by first opening the residues file
with open("residues.dat", "r") as f:
    count_occ(f.readline().split())
    f.close()

