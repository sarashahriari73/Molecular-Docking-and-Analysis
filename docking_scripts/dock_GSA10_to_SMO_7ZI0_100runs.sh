#!/bin/bash

# Define ligand file and receptor config
ligand_file="GSA10-ligand.pdbqt"  # Ligand filename
name=`basename $ligand_file .pdbqt`

for i in {1..100}  # Run docking 100 times
do
    # Create a unique config file for each run
    sed "s|7zi0-receptor.pdbqt|7zi0-receptor.pdbqt|; s|out = GSA10-7zi0.pdbqt|out = GSA10-7zi0_run$i.pdbqt|" GSA10-7zi0.conf > ${name}_run$i.conf

    # Run docking
    vina --config ${name}_run$i.conf

    # Move the output to a specific directory with unique names
    mv GSA10-7zi0.pdbqt ./100 docking GSA10-7zi0/GSA10-7zi0_run$i.pdbqt

    # Clean up temporary files
    rm ${name}_run$i.conf
done

echo "Docking completed 100 times for ligand: $name"
