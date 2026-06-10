#!/usr/bin/env python3

import sys
import subprocess
import tempfile
import os

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} protein.pdb", file=sys.stderr)
    sys.exit(1)

pdb_file = sys.argv[1]

with tempfile.NamedTemporaryFile(
    suffix=".dssp",
    delete=False
) as tmp:

    dssp_file = tmp.name

try:

    subprocess.run(
        [
            "mkdssp", pdb_file, dssp_file
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

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

            ss = line[16]

            if ss in ("H", "G", "I"):
                ss_string += "H"

            elif ss in ("E", "B"):
                ss_string += "E"

            else:
                ss_string += "C"

    print(ss_string)

finally:

    if os.path.exists(dssp_file):
        os.remove(dssp_file)