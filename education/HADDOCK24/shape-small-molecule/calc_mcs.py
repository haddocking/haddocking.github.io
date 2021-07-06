#!/usr/bin/env python

import argparse

from rdkit import Chem
from rdkit.Chem import rdFMCS


def _process_input():
    """Define and parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-target',
        '--target_file',
        required=True,
        help='Path to the file containing the target SMILES',
        nargs='?'
    )
    parser.add_argument(
        '-templates',
        '--template_file',
        required=True,
        help='Path to the file containing the template SMILES',
        nargs='?'
    )

    args = parser.parse_args()
    return args


def _read_single_smiles_from_file(filepath):
    """Read single SMILES strings from file"""
    with open(filepath) as input_file:
        for line in input_file:
            smiles, _id = line.split()
            break

    return smiles


def _read_multi_smiles_from_file(filepath):
    """Read multiple SMILES strings from file"""
    smiles = []

    with open(filepath) as input_file:
        for line in input_file:
            _smiles, _id = line.split()
            smiles.append(_smiles)

    return smiles


def calc_mcs_atoms(mol1, mol2):
    """Finds the maximum common substructure between two molecules"""
    mcs = rdFMCS.FindMCS(
        (mol1, mol2),
        ringMatchesRingOnly=True,
        completeRingsOnly=True,
        bondCompare=rdFMCS.BondCompare.CompareOrder
    )

    return mcs.numAtoms


def calc_similarity(target, templates, mcs_areas, tversky_weight=0.8):
    """Calculates tanimoto and tversky coefficients between molecules"""
    def _calc_tanimoto_coefficient(mol1_atoms, mol2_atoms, mcs_atoms):
        """Calculate the tanimoto coefficient"""
        return ((mcs_atoms) / (mol1_atoms + mol2_atoms - mcs_atoms))

    def _calc_tversky_coefficient(mol1_atoms, mol2_atoms, mcs_atoms, weight):
        """Calculate the tversky coefficient"""
        weight1 = weight
        weight2 = 1 - weight

        mol1_weighted = weight1 * (mol1_atoms - mcs_atoms)
        mol2_weighted = weight2 * (mol2_atoms - mcs_atoms)

        return ((mcs_atoms) / (mol1_weighted + mol2_weighted + mcs_atoms))

    target_atoms = target.GetNumAtoms()

    tanimoto = []
    tversky = []

    for template, mcs_area in zip(templates, mcs_areas):
        template_atoms = template.GetNumAtoms()
        tanimoto.append(_calc_tanimoto_coefficient(
            target_atoms,
            template_atoms,
            mcs_area
        ))
        tversky.append(_calc_tversky_coefficient(
            target_atoms,
            template_atoms,
            mcs_area,
            tversky_weight
        ))

    return tanimoto, tversky


def main():
    """Run everything"""
    args = _process_input()
    target = _read_single_smiles_from_file(args.target_file)
    templates = _read_multi_smiles_from_file(args.template_file)

    target_mol = Chem.MolFromSmiles(target)
    template_mols = [Chem.MolFromSmiles(_) for _ in templates]
    mcs_atoms = [calc_mcs_atoms(target_mol, _) for _ in template_mols]
    # print(target_mol.GetNumAtoms(), template_mols[0].GetNumAtoms(), mcs_atoms[0])

    tanimoto_sim, tversky_sim = calc_similarity(
        target_mol,
        template_mols,
        mcs_atoms,
    )

    for tan, tve in zip(tanimoto_sim, tversky_sim):
        print(f"{tan:0.3f} {tve:0.3f}")

if __name__ == "__main__":
    main()
