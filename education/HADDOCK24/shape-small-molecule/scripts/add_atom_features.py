import pandas as pd
import math
import rdkit
from rdkit.ML.Cluster import Butina
from rdkit import Chem
from rdkit.Chem import PyMol
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem.Pharm3D import Pharmacophore, EmbedLib
from rdkit import rdBase
from rdkit import RDConfig
from rdkit.Chem import rdDepictor
import sys
import os, glob

def get_atom_features(mol):
    
    # Define features
    fdef = AllChem.BuildFeatureFactory(os.path.join(RDConfig.RDDataDir,'BaseFeatures.fdef'))

    rawFeats = fdef.GetFeaturesForMol(mol)
    features = [feature.GetFamily() for feature in rawFeats]
    atomsID = [feature.GetAtomIds() for feature in rawFeats]
    
    # create dictionary atomID = associated feature
    atomFeatures = {}
    for idx in range(0,len(features)) :
        for atomID in atomsID[idx] :
            if atomID in atomFeatures.keys() :
                # never replace an existing feature by LumpedHydrophobe
                if features[idx] == 'LumpedHydrophobe' :
                    continue
                # never replace an existing feature by ZnBinder
                elif features[idx] == 'ZnBinder' :
                    continue
                # favor aromatic over Hydrophobic and LumpedHydrophobe :
                elif atomFeatures[atomID] == 'Aromatic' and  (features[idx] == 'LumpedHydrophobe' or features[idx] == 'Hydrophobe'):
                    continue
                # never replace a donor or an acceptor feature 
                elif atomFeatures[atomID] == 'Donor' or atomFeatures[atomID] == "Acceptor" :
                    continue
                else : 
                    atomFeatures[atomID] = features[idx]
            else : 
                atomFeatures[atomID] = features[idx]

    return atomFeatures
    


def update_pdb(atomFeatures, fName, atomDict):

    atomTypeConv = {'Donor':0.10, 'Acceptor':0.20, 'NegIonizable':0.30, 'PosIonizable' : 0.40, \
                        'ZnBinder' : 0.50, 'Aromatic' : 0.60, 'Hydrophobe' : 0.70, \
                        'LumpedHydrophobe' : 0.80}

    # Read original pdb file 
    input = open('{}.pdb'.format(fName), 'r')
    
    # Write the output file 
    output = open('{}_features.pdb'.format(fName), 'w')
    
    # update the occupancy factor with features info
    count_H = 0
    for line in input :
        if line.split(" ")[0] == "HETATM" or line.split(" ")[0] == "ATOM":
            if 'H' not in line.split()[2][0] :

                atomID = int(line.split()[1]) - 1 - count_H  # first atom set to 0 with RDKIT

                # Use the following option only is the atom order differ in input files
                #converted_atomID = atomDict[atomID]
                converted_atomID = atomID

                if converted_atomID in atomFeatures.keys() :
                    output.write('{}{: 4.2f}{}'.format(line[0:55], atomTypeConv[atomFeatures[converted_atomID]],  line[60:]))
                else :
                    output.write('{}{: 4.2f}{}'.format(line[0:55], 0.00,  line[60:]))

    print("Features generated for : {}".format(fName))
    output.close()


if __name__ == "__main__":

    
    if len(sys.argv) != 3 :
        print ("""\n
This scripts maps pharmaophore features into the q-factor columns of PDB files.
It requires 2 inputs:
        - The molecule in an SDF format (missing connection in the PDB format lead to wrong feature detection)
        - The path to the directory containing the same molecule in PDB format (single of multiple files)
Usage:
        python add_atom_features.py [sdf] [path_to_pdb(s)]
""")

    ref_sdf = sys.argv[1]
    molFile = sys.argv[2]

    # Read and store molecules 
    SDFsupp = [m for m in Chem.SDMolSupplier(ref_sdf)]
    mol = SDFsupp[0]

    # Get pharmacophore features from the molecule SDF file
    features = get_atom_features(mol)
    
    # Get the rank of the atom in the canonical smiles for the sdf file 
    csmiles_atID_sdf = list(Chem.CanonicalRankAtoms(mol, breakTies=True, includeChirality=False))
    index_sdf = sorted(range(len(csmiles_atID_sdf)), key=lambda k: csmiles_atID_sdf[k])

    first_pdb = True
    
    molpdb = Chem.MolFromPDBFile(molFile)
    print(f"SDF smiles: {Chem.MolToSmiles(mol)} \nPDB smiles: {Chem.MolToSmiles(molpdb)}")
    
    # Get the rank of the atom in the canonical smiles for the pdb file(s)
    csmiles_atID_pdb = list(Chem.CanonicalRankAtoms(molpdb, breakTies=True, includeChirality=False))
    index_pdb = sorted(range(len(csmiles_atID_pdb)), key=lambda k: csmiles_atID_pdb[k])
    
    # Use the following option only if the atom order differ in input files
    # Otherwise, make sure the atom numbering starts at 1 in the PDB file(s)
    atomDict = dict(zip(index_pdb, index_sdf))
    first_pdb = False

    fName = molFile.split(".pdb")[0]
    update_pdb(features, fName, atomDict)
    
        
        
