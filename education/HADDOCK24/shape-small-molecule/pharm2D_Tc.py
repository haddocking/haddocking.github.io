import pandas as pd
import math
import rdkit
from rdkit import rdBase
from rdkit import RDConfig
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem import rdDepictor
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.Pharm2D import Generate
from rdkit.Chem.Pharm2D.SigFactory import SigFactory
from rdkit.Chem.Pharm2D import Gobbi_Pharm2D
import sys
import os, glob

def pharm2D_Tc(dicTarget, dicTemplates):

    # DEFINE PHARMACOPHORE FEATURES
    fdefName = os.path.join(RDConfig.RDDataDir,'BaseFeatures.fdef')
    factory = ChemicalFeatures.BuildFeatureFactory(fdefName)
    sigFactory = SigFactory(factory, minPointCount=2, maxPointCount=3, trianglePruneBins=False)   # replace to False and the error will disappear (True is a default value)
    sigFactory.SetBins([(0,2),(2,5),(5,8)]) # Define the distance bins; Ex. (0,2) : between 0A and 2A - [(0,2),(2,5),(5,8)]
    
    output= open("sim.Tc", 'w')
    
    for molTarget in dicTarget :
        simTemplates = []
        simVal = []

        # Get the Pharm2D fingerprint for the target molecule
        targetPharm2D = Generate.Gen2DFingerprint(dicTarget[molTarget], sigFactory)

        for molTemplates in dicTemplates :
            try :
                # Get the Pharm2D fingerprint for the template molecule
                templatePharm2D = Generate.Gen2DFingerprint(dicTemplates[molTemplates], sigFactory)

                # Calculate the Tanimoto coefficient between the target and template fingerprint
                sim = DataStructs.FingerprintSimilarity(targetPharm2D, templatePharm2D, metric = DataStructs.TanimotoSimilarity)
                simVal.append(sim)
                simTemplates.append(molTemplates)
                output.write(f"{molTarget} {dicTarget[molTarget].GetNumAtoms()} {molTemplates} {round(sim,3)} {dicTemplates[molTemplates].GetNumAtoms()} \n")
            except : 
                continue

        # Find the index of the best template (highest tanimoto coefficient)
        best = sorted(range(len(simVal)), key=lambda k: simVal[k], reverse=True)[0]

        # Save it (Target Target_atom_number Template Tc Template_atom_number)
        output.write(f"{molTarget} {dicTarget[molTarget].GetNumAtoms()} {simTemplates[best]} {round(simVal[best],3)} {dicTemplates[simTemplates[best]].GetNumAtoms()} best\n")
        
    output.close()


if __name__ == "__main__":
    if len(sys.argv) != 3 :
        print ("""\n
This computes the RDKIT pharm2D Tanimoto coefficient between a set of molecules to dock (targets) and a set of potential templates.
All molecule files must be provided in SDF format to ensure correct 2D pharmacophore descriptor computation.
Usage: 
        python pharm2D_Tc.py [target(s)_dir] [templates_dir]
""")
    
    inputDirTarget = sys.argv[1]
    inputDirTemplates = sys.argv[2]
    
    # Stores all target in a dictionnary {name=mol}
    dicTarget = {}
    for molFile in glob.glob("{}/*.sdf".format(inputDirTarget)):
        try :
            fName = molFile.split("/")[-1].split(".")[0]
            SDFsupp = [m for m in Chem.SDMolSupplier(molFile)]
        except : 
            print('could not read target(s)')
            continue 
        dicTarget[fName] = SDFsupp[0]
    
    # Stores all template in a dictionnary {name=mol}
    dicTemplates = {}
    for molFile in glob.glob("{}/*.sdf".format(inputDirTemplates)):
        try :
            fName = molFile.split("/")[-1].split(".")[0]
            SDFsupp = [m for m in Chem.SDMolSupplier(molFile)]
        except : 
            print('could not read the template(s)')
            continue 
        dicTemplates[fName] = SDFsupp[0]

    # Compute the Pharm2D pharmacophore fingerprints Tanimoto coefficient
    pharm2D_Tc(dicTarget, dicTemplates)
