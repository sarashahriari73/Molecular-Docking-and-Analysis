# Original script developed by Dr.  Tâp Ha-Duong 
# Adapted and modified by Sara Shahriari for Smoothened receptor and its ligands interaction analysis
# Modifications include: input handling, figure formatting, data selection

################################################################################
# This script computes the occurrences of residues listed in residues.dat
# It reads a receptor PDBQT file to extract residue names and prints the counts
# to a file called 'occurences.dat'
################################################################################

import sys

def read_pdb(file_name): 
    """
    Reads a PDBQT file and extracts unique residue identifiers in the format RESNAME + RESNUM (e.g., ARG104).
    """
    residues = set()
    with open(file_name, "r") as g:
        for line in g:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                resname = line[17:20].strip()
                resnum = line[22:26].strip()
                resid = resname + resnum
                residues.add(resid)
    return list(residues)


def count_occ(residue_list): 
    """
    Counts how many times each residue from the receptor appears in the residue list.
    Writes the result to 'occurences.dat'
    """
    occ = {res: 0 for res in resi}  # Initialize counts for all known residues
    
    for res in residue_list:
        if res in occ:
            occ[res] += 1

    with open('occurrences.dat', 'w') as g:
        for elem in occ:
            # Separate residue name and number
            g.write(f'{elem[:3]} {elem[3:]}   {occ[elem]}\n')

# --------------------------- MAIN EXECUTION ---------------------------

if len(sys.argv) < 2:
    print("Usage: python compute_occurrences.py <receptor_file.pdbqt>")
    sys.exit(1)

rec_file_name = sys.argv[1]  # receptor file should be passed as an argument

# Extract residues from the receptor file
resi = read_pdb(rec_file_name)

# Read the residues of interest and count their occurrences
with open("residues.dat", "r") as f:
    residue_list = f.readline().split()
    count_occ(residue_list)
