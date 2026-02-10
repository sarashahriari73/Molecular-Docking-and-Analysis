# Original script developed by Dr.  Tâp Ha-Duong 
# Adapted and modified by Sara Shahriari for Smoothened receptor and its ligands interaction analysis
# Modifications include: input handling, figure formatting, data selection

import matplotlib.pyplot as plt

residues = []
values = []

with open("occurrences.dat") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            resname, resid, count = parts
            label = f"{resname}{resid}"
            residues.append(label)
            values.append(float(count))

# Sort by frequency
top = sorted(zip(residues, values), key=lambda x: x[1], reverse=True)[:15]
labels, freqs = zip(*top)

plt.figure(figsize=(10, 5))
plt.bar(labels, freqs, color="skyblue", edgecolor="black")
plt.title("Top 15 Contacting Residues")
plt.ylabel("Frequency of Contact")
plt.xlabel("Residue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_residues.png")
plt.show()
