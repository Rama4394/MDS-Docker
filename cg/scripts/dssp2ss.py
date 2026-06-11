#!/usr/bin/env python3

import sys
import subprocess
import tempfile
import os

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} protein.pdb", file=sys.stderr)
    sys.exit(1)

pdb_file = sys.argv[1]

# 1. Extract the exact, ordered sequence of residues from the PDB
pdb_residues = []
with open(pdb_file) as f:
    for line in f:
        # Use CA atoms to identify unique residues, just like Vermouth does
        if line.startswith("ATOM  ") and line[12:16].strip() == "CA":
            chain = line[21].strip()
            resnum = line[22:26].strip()
            inscode = line[26].strip()
            pdb_residues.append(f"{chain}_{resnum}_{inscode}")

with tempfile.NamedTemporaryFile(suffix=".dssp", delete=False) as tmp:
    dssp_file = tmp.name

try:
    subprocess.run(
        ["mkdssp", pdb_file, dssp_file],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # 2. Parse DSSP and map SS to the explicit residue IDs
    dssp_map = {}
    with open(dssp_file) as f:
        start = False
        for line in f:
            if line.startswith("  #  RESIDUE"):
                start = True
                continue
            
            if not start or len(line) < 17 or line[13] == '!':
                continue

            # Extract standard DSSP columns and normalize spacing
            resnum = line[5:10].strip()
            inscode = line[10].strip()
            chain = line[11].strip()
            res_key = f"{chain}_{resnum}_{inscode}"

            ss = line[16]
            if ss in ("H", "G", "I"):
                dssp_map[res_key] = "H"
            elif ss in ("E", "B"):
                dssp_map[res_key] = "E"
            else:
                dssp_map[res_key] = "C"

    # 3. Build the final string aligning 1-to-1 with the PDB sequence
    # If DSSP dropped a residue, it safely defaults to "C" (Coil)
    ss_string = "".join([dssp_map.get(res, "C") for res in pdb_residues])

    print(ss_string)

finally:
    if os.path.exists(dssp_file):
        os.remove(dssp_file)