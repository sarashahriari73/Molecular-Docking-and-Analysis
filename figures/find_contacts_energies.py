################################################################################
# This script reads a set of docking results (pdbqt) and a receptor (pdbqt) file and outputs a residues.dat file containing the receptor residues interacting with the docking results
################################################################################

import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt

def read_nrj(file_name): 
    energies = [] 
    with open(file_name, "r") as f: 
        lines = f.readlines() 
        for l in lines: 
            if "REMARK VINA RESULT:" in l: 
                good_line_splitted = l.split() 
                energy = float(good_line_splitted[3]) 
                energies.append(energy) 
    f.close() 
    return energies 

def read_lig(file_name): 
    lig_xyz = [] 
    with open(file_name, "r") as f: 
        lines = f.readlines() 
        for l in lines: 
            if "MODEL" in l: 
                splitted_line = l.split() 
                n = splitted_line[1] 
            if "ATOM" in l or "HETATM" in l: 
                if "H" not in l.split()[2]: 
                    splitted_line = l.split() 
                    x = float(splitted_line[5]) 
                    y = float(splitted_line[6]) 
                    z = float(splitted_line[7]) 
                    lig_xyz.append([n, x, y, z]) 
    f.close() 
    return lig_xyz 

def read_rec(file_name): 
    rec_xyz = [] 
    with open(file_name, "r") as g: 
        lines = g.readlines() 
        for l in lines: 
            if "ATOM" in l or "HETATM" in l: 
                splitted_line = l.split() 
                x = float(splitted_line[5]) 
                y = float(splitted_line[6])
                z = float(splitted_line[7])
                resid = splitted_line[3] + splitted_line[4]
                rec_xyz.append([resid, x, y, z]) 
    g.close() 
    return rec_xyz 
 
def comput_dist(lig_xyz, rec_xyz): 
    model_res_dist = [] 
    good_model_res = [] 
    for coord_prot in rec_xyz: 
        for coord_lig in lig_xyz: 
                dist = math.sqrt((coord_lig[1] - coord_prot[1])**2 + (coord_lig[2] - coord_prot[2])**2 + (coord_lig[3] - coord_prot[3])**2) 
                model_res_dist.append([coord_lig[0], coord_prot[0], dist]) 
    for distance in model_res_dist: 
        if float(distance[2]) < 4.0: 
            good_model_res.append([distance[0], distance[1]]) 
    good_model_res = np.array(good_model_res) 
    good_model_res = np.core.records.fromarrays(good_model_res.T, names='i,r', formats='U3,U6') 
    good_model_res = np.unique(good_model_res) 
    residues = [] 
    for e in good_model_res:
        residues.append(e[1])
    return residues 

lig_file_name = sys.argv[1] 
rec_file_name = sys.argv[2] 

energies = read_nrj(lig_file_name) 
lig_xyz = read_lig(lig_file_name) 
rec_xyz = read_rec(rec_file_name) 

interacting_residues = comput_dist(lig_xyz, rec_xyz) 

with open("residues.dat", "a") as f: 
    for elem in interacting_residues: 
        f.write(f'{elem} ')
    f.close()

count = 1 
with open("energies.dat", "a") as h:
    for elem in energies: 
        h.write(f"Model {count} energy: {str(elem)}\n")
        count = count + 1
    h.close()

