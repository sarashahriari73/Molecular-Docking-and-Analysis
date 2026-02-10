#!/bin/bash

# Temporary file
temp_file="temp_binding_scores.csv"

# Output files
csv_out="best_binding_scores.csv"
txt_out="best_binding_scores.txt"

# Header
echo "Filename,Binding_Energy" > "$temp_file"

# Loop over all .pdbqt files
for file in *.pdbqt; do
    # Extract the best binding score (first line with result)
    energy=$(grep "REMARK VINA RESULT" "$file" | head -n 1 | awk '{print $4}')
    echo "$file,$energy" >> "$temp_file"
done

# Sort the energies numerically in descending order (most negative to least)
(head -n 1 "$temp_file" && tail -n +2 "$temp_file" | LC_NUMERIC=C sort -t, -k2,2g) > "$csv_out"

# Also make a .txt version without header
tail -n +2 "$csv_out" > "$txt_out"

# Clean up
rm "$temp_file"

echo "✅ Sorted files saved:"
echo "  → $csv_out (with header)"
echo "  → $txt_out (no header)"
