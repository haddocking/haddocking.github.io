#!/usr/bin/env python

import re
import sys
import argparse
from multiprocessing import cpu_count
from os.path import splitext, basename

from rdkit import Chem
from rdkit.Chem import AllChem, rdFMCS


def _process_input():
    """Define and parse the command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input_file',
        required=True,
        help='Path to the input file. Format is inferred by file ending',
        nargs='?'
    )
    parser.add_argument(
        '-o',
        '--output_file',
        required=False,
        help=(
            'Path to the output file. Optional. If not specified will create'
            ' a file named after the input file with the suffix _conformers.'
            'pdb in the current directory'
        ),
        nargs='?'
    )
    parser.add_argument(
        '-b',
        '--benchmark_file',
        required=False,
        help=(
            'Path to the reference file. Optional. Simplifies benchmarking of'
            ' a particular combination of parameters. Prints the RMSD values '
            ' to STDOUT'
        ),
        nargs='?'
    )
    parser.add_argument(
        '-m',
        '--minimise',
        required=False,
        action='store_true',
        help='Minimise generated conformers. Disabled by default'
    )
    parser.add_argument(
        '-r',
        '--random',
        required=False,
        action='store_true',
        help=(
            'Use random coordinates for the conformer generation. Disabled by '
            'default'
        )
    )
    parser.add_argument(
        '-v',
        '--verbose',
        required=False,
        action='store_true',
        help=(
            'Print the number of conformers that were generated. Disabled by '
            'default'
        )
    )
    parser.add_argument(
        '-t',
        '--threads',
        required=False,
        help=(
            'Number of threads to use for the conformer generation. Defaults'
            ' to the number of logical cores of the host'
        ),
        type=int,
        nargs='?'
    )
    parser.add_argument(
        '-p',
        '--parameters',
        required=False,
        help=(
            'ETKDG parameters to use for the conformer generation. Allowed'
            ' options are "1", "2", "3", "3sr", "3mc". Default is "2". "1"'
            ' and "2" correspond to the respective parameters, while "3", '
            '"3sr", "3mc" correspond to the 2020 parameters when applied to'
            ' small rings and macrocycles, only small rings and macrocycles,'
            ' respectively.'
        ),
        choices=['1', '2', '3', '3sr', '3mc'],
        default='2',
        nargs='?'
    )
    parser.add_argument(
        '-c',
        '--conformers',
        required=False,
        help=('Number of conformers to generate. Defaults to 100'),
        default=100,
        type=int,
        nargs='?'
    )

    args = parser.parse_args()
    return args


def __etkdg_params(cmd_args):
    """Return the appropriate params for the conformer generation."""
    version = cmd_args.parameters
    if version == "1":
        params = AllChem.ETKDG()
    elif version == "2":
        params = AllChem.ETKDGv2()
    elif version == "3":
        params = AllChem.ETKDGv3()
        params.useSmallRingTorsions = True
    elif version == "3sr":
        params = AllChem.srETKDGv3()
    else:
        params = AllChem.ETKDGv3()

    if cmd_args.threads is not None:
        params.numThreads = cmd_args.threads
    else:
        params.numThreads = cpu_count()

    params.randomSeed = 917

    params.pruneRmsThresh = 0.5
 
    params.clearConfs = True

    return params


def _determine_input_file_format(file_path):
    """Determines the format of the input file based on file ending."""
    _, s_ext = splitext(basename(file_path))
    s_ext = s_ext.lower()

    if s_ext in {'.pdb', '.ent'}:
        return 'PDB'
    elif s_ext in {'.sdf'}:
        return 'SDF'
    elif s_ext in {'.smi', '.ism', '.can'}:
        return 'SMILES'
    else:
        raise RuntimeError("Only PDB and SMILES input files accepted.")


def _determine_output_file(file_path):
    """Determines the name of the output file."""
    fname, _ = splitext(basename(file_path))
    return fname + '_conformers.pdb'


def _parse_input_file(file_path, iformat=None):
    """Return an RDKIT molecule from the input file."""
    iformat = (
        iformat
        if iformat is not None
        else _determine_input_file_format(file_path)
    )

    if iformat == 'SMILES':
        with open(file_path) as in_file:
            for line in in_file:
                line = line.rstrip()

                match = re.match('^(\S+)\s*\S*', line)
                if match:
                    groups = match.groups()
                    smiles = match.group(1)
                break  # Only read a single line since this is SMILES
        return Chem.MolFromSmiles(smiles)
    elif iformat == "PDB":
        return Chem.MolFromPDBFile(file_path)
    elif iformat == "SDF":
        suppl = Chem.SDMolSupplier(file_path)
        return list(suppl)[0]


def benchmark(path_to_ref, query, num_of_confs, compute_mcs=False):
    """Compute symmetry-corrected RMSDs between reference and conformers."""
    ref_mol = _parse_input_file(path_to_ref)

    if compute_mcs:
        mcs = rdFMCS.FindMCS([ref_mol, query])

        if ((mcs.numAtoms == len(list(query.GetAtoms()))) and
            (mcs.numAtoms == len(list(ref_mol.GetAtoms())))):
            pattern = Chem.MolFromSmarts(mcs.smartsString)

            query_indices = query.GetSubstructMatch(pattern)
            ref_indices = ref_mol.GetSubstructMatch(pattern)

            maps = []
            for mapping in zip(query_indices, ref_indices):
                maps.append(mapping)
            maps = [maps]
        else:
            raise RuntimeError("Couldn't match molecules. Will not benchmark")

    rmsd_values = []
    for i in range(num_of_confs):
        if compute_mcs:
            rmsd_values.append(
                AllChem.GetBestRMS(query, ref_mol, i, 0, map=maps)
            )
        else:
            rmsd_values.append(AllChem.GetBestRMS(query, ref_mol, i, 0))

    return rmsd_values


def main():
    """Run all the things."""
    args = _process_input()

    mol = _parse_input_file(args.input_file)
    mol_h = Chem.AddHs(mol)

    parameters = __etkdg_params(args)
    conformer_ids = AllChem.EmbedMultipleConfs(
        mol_h,
        numConfs=args.conformers,
        params=parameters
    )

    if args.minimise is True:
        AllChem.MMFFOptimizeMoleculeConfs(
            mol_h,
            numThreads=parameters.numThreads
        )

    mol = Chem.RemoveHs(mol_h)

    if args.benchmark_file is not None:
        rmsd_values = benchmark(args.benchmark_file, mol, len(conformer_ids))
        for rmsd_value in rmsd_values:
            print(f"{rmsd_value:.3f}")

    Chem.MolToPDBFile(
        mol,
        (
            args.output_file
            if args.output_file is not None
            else _determine_output_file(args.input_file)
        ),
        flavor=2
    )

    if args.verbose is True:
        print(
            f"{len(conformer_ids)} / {args.conformers} conformers generated"
        )

if __name__ == "__main__":
    main()
