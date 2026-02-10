#!/bin/bash

# Loop through each item in the current directory
for dir in */; do
    # Check if 'extract_scores.sh' exists in the subdirectory
    if [[ -f "${dir}extract_scores.sh" ]]; then
        echo "Entering ${dir}"
        # Navigate into the subdirectory
        cd "$dir" || { echo "Failed to enter ${dir}"; exit 1; }
        # Execute the docking script
        ./extract_scores.sh
        # Navigate back to the parent directory
        cd ..
    else
        echo "No extract_scores.sh found in ${dir}, skipping."
    fi
done