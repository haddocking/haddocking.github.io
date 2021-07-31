#!/usr/bin/python3

import sys

'''
Script spliting multi-sdf file into multiple files
USAGE : python split_sdf.py XX.sdf
'''

def split_file(sdffile, name):

	new_molecule = True
	first = True
	pdblist=[]

	for line in sdffile:
		if new_molecule:
			pdbname = line.strip().split()[0]
			print(pdbname)
			if not pdbname in pdblist :
				output = open("{}.sdf".format(pdbname),"w")
				pdblist.append(pdbname)
			else : 
				occ = pdblist.count(pdbname)
				output = open("{}_{}.sdf".format(pdbname, occ),"w")
			new_molecule = False
			
		output.write(line)
		if line.strip() == "$$$$":
			new_molecule = True
			output.close()
		

        
if __name__ == "__main__":

        if len(sys.argv) < 2:
                sys.exit("require two arguments: python split_sdf.py XX.sdf")
        
        sdfs = open(sys.argv[1],"r").readlines()
        name = sys.argv[1].split(".")[0]
        split_file(sdfs, name)
