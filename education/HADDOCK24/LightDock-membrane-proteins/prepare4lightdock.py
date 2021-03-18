#!/usr/bin/env python3

import sys
from os import linesep
from pathlib import Path


if __name__ == "__main__":

    if len(sys.argv[1:]) != 2:
        raise SystemExit("Usage: prepare4lightdock.py input_cg.pdb output.pdb")
    
    cg_pdb_file_name = sys.argv[1]
    output_pdb_file_name = sys.argv[2]

    if not Path(cg_pdb_file_name).exists():
        raise SystemExit(f"Error: Input CG PDB file {cg_pdb_file_name} does not exist")

    with open(cg_pdb_file_name) as ih:
        with open(output_pdb_file_name, "w") as oh:
            for line in ih:
                if line.startswith("ATOM  "):
                    line = line.rstrip(linesep)
                    if "PO4" in line:
                        line = line.replace("PO4", " BJ").replace("DPPC", " MMB")
                        oh.write(f"{line}{linesep}")
                    else:
                        res_name = line[12:16]
                        if res_name in ["0BTN", "0BEN", "0BHN"] or res_name[0] == "B" or res_name[:2] == "5B":
                            line = line.replace(res_name, "CA  ")
                            oh.write(f"{line}{linesep}")
