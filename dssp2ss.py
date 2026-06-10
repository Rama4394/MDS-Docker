#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} protein.dssp")
    sys.exit(1)

dssp_file = sys.argv[1]

ss_string = ""

with open(dssp_file) as f:
    start = False

    for line in f:
        if line.startswith("  #  RESIDUE"):
            start = True
            continue

        if not start:
            continue

        if len(line) < 17:
            continue

        if line[13] == '!':
            continue

        dssp_ss = line[16]

        if dssp_ss in ("H", "G", "I"):
            ss_string += "H"
        elif dssp_ss in ("E", "B"):
            ss_string += "E"
        else:
            ss_string += "C"

print(ss_string)
