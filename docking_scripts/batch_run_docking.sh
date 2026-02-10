#!/bin/bash

# Loop through each item in the current directory
for dir in */; do
    # Check if 'docking.sh' exists in the subdirectory
    if [[ -f "${dir}docking.sh" ]]; then
        echo "Entering ${dir}"
        # Navigate into the subdirectory
        cd "$dir" || { echo "Failed to enter ${dir}"; exit 1; }
        # Execute the docking script
        ./docking.sh
        # Navigate back to the parent directory
        cd ..
    else
        echo "No docking.sh found in ${dir}, skipping."
    fi
done
