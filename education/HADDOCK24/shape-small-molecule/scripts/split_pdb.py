#!/usr/bin/python

import sys

'''
Split multi-pdb files into individual files
USAGE : python split_pdb.py XX.pdb
'''

def split_file(pdbfile, name):
		
        new_molecule = True
        count = 0
        line_nb = 0

        for line in pdbfile:
                if new_molecule and line.strip() != 'END':
                        count += 1
                        output = open("%s_%s.pdb"%(name,str(count)),"w")
                        new_molecule = False

                if 'ATOM' in line or 'HETATM' in line:
                        line_nb += 1
                        output.write(line)

                if (line.strip() == "END" or line.strip() == "ENDMDL") and line_nb > 0:
                        output.write('END\n')
                        new_molecule = True
                        line_nb = 0
                        output.close()
                        
						
						
						
if __name__ == "__main__":

        if len(sys.argv) < 2:
                sys.exit("require two arguments: python split_pdb.py XX.pdb")

        pdbs = open(sys.argv[1],"r").readlines()
        name = sys.argv[1].split('/')[-1].split(".")[0]
        split_file(pdbs, name)
