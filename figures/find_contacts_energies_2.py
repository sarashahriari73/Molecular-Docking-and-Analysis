# Original script developed by Dr.  Tâp Ha-Duong 
# Adapted and modified by Sara Shahriari for Smoothened receptor and its ligands interaction analysis
# Modifications include: input handling, figure formatting, data selection

import sys
import math
import numpy as np

def read_nrj(file_name): 
    energies = [] 
    with open(file_name, "r") as f: 
        for l in f: 
            if "REMARK VINA RESULT:" in l: 
                energy = float(l.split()[3]) 
                energies.append(energy) 
    return energies 

def read_lig(file_name): 
    lig_xyz = [] 
    current_model = None
    with open(file_name, "r") as f: 
        for l in f: 
            if l.startswith("MODEL"):
                current_model = l.split()[1]  # e.g., '1'
            if l.startswith("HETATM") or l.startswith("ATOM"): 
                atom_name = l[12:16].strip()
                if atom_name.startswith("H"):  # skip hydrogens
                    continue
                x = float(l[30:38].strip())
                y = float(l[38:46].strip())
                z = float(l[46:54].strip())
                lig_xyz.append([current_model, x, y, z])
    return lig_xyz 

def read_rec(file_name): 
    rec_xyz = [] 
    with open(file_name, "r") as g: 
        for l in g: 
            if l.startswith("ATOM") or l.startswith("HETATM"): 
                resname = l[17:20].strip()
                resnum  = l[22:26].strip()
                resid = resname + resnum
                x = float(l[30:38].strip())
                y = float(l[38:46].strip())
                z = float(l[46:54].strip())
                rec_xyz.append([resid, x, y, z]) 
    return rec_xyz 

def comput_dist(lig_xyz, rec_xyz): 
    model_res_dist = [] 
    good_model_res = [] 

    for coord_prot in rec_xyz: 
        for coord_lig in lig_xyz:
            dist = math.sqrt(
                (coord_lig[1] - coord_prot[1])**2 + 
                (coord_lig[2] - coord_prot[2])**2 + 
                (coord_lig[3] - coord_prot[3])**2
            )
            model_res_dist.append([coord_lig[0], coord_prot[0], dist]) 
            if dist < 4.0:
                good_model_res.append([coord_lig[0], coord_prot[0]]) 

    if good_model_res:
        good_model_res = np.array(good_model_res) 
        good_model_res = np.core.records.fromarrays(good_model_res.T, names='i,r', formats='U3,U6') 
        good_model_res = np.unique(good_model_res) 
    else:
        print("No interacting residues found.")

    residues = [e[1] for e in good_model_res]
    return residues 

# ============ MAIN ==============
lig_file_name = sys.argv[1] 
rec_file_name = sys.argv[2] 

energies = read_nrj(lig_file_name) 
lig_xyz = read_lig(lig_file_name) 
rec_xyz = read_rec(rec_file_name) 
interacting_residues = comput_dist(lig_xyz, rec_xyz) 

with open("residues.dat", "a") as f: 
    for elem in interacting_residues: 
        f.write(f'{elem} ')
    f.write("\n")

with open("energies.dat", "a") as h:
    for i, elem in enumerate(energies, 1): 
        h.write(f"Model {i} energy: {elem}\n")
