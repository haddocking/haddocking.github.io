#!/usr/bin/env python3

import sys
from os.path import splitext, basename


resid = []
features = []

if len(sys.argv) != 2:
    print("Usage: {} <input_file>".format(sys.argv[0]))
    sys.exit(1)

out_file = sys.argv[1].split(".")[0]

with open(sys.argv[1]) as in_file:
    for line in in_file:
        line = line.rstrip()
        columns = line.split()

        if line.split( )[0] == 'ENDMDL' : 
            break

        if len(columns) <= 6:
            continue

        if "H" not in columns[2] :
            resid.append(columns[2])
            features.append(float(columns[-3]))


for i in range(0, len(resid)):    
    
    print(
        "assi (segid S and (attr q =={: 4.2f})) (segid B and name {}) 1.0 1.0 0.0".format(
            features[i], resid[i]
        ),
        file=open('shape_restraints_pharm.tbl', 'a')
    )

