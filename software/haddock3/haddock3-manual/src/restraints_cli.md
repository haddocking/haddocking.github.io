# Generating restraints with Haddock3

Ambiguous (or not) restraints file must comply with the CNS syntax.
Generating them can be quite difficult, and for this reason we added a dedicated command line interface `haddock3-restraints`, allowing to perform several maniputation to generate restraints files to be used later in your docking experiment.

Usage:
```bash
haddock3-restraints <TASK_NAME> <TASK_ARGS>
```

For the list of available tasks, run:
```bash
haddock3-restraints -h
```

For the list of arguments for a given task, run:
```bash
haddock3-restraints <TASK_NAME> -h
```


This CLI holds multiple sub-commands, listed and explained below:
- [calc_accessibility](#calc-accessibility):
- [passive_from_active](#passive-form-active):
- [active_passive_to_ambig](#active-passive-to-ambig):
- [restrain_bodies](#restrain-bodies):
- [z_surface_restraints](#z-surface-restraints):
- [validate_tbl](#validate-tbl):


## Calc Accessibility

Given a pdb file, `calc_accessibility` will calculate the relative accessibility of
the side chains and return a list of surface exposed residues.

Nucleic acids bases are considered to be always accessible.

This command is particularly useful when little interface information is available for one biomolecule and one wants to identify (and then target) all the surface exposed residues on a certain protein.

**Usage:**

    haddock3-restraints calc_accessibility <input_pdb_file> [-c <cutoff>] [--log_level <log_level>] [--export_to_actpass]

## Passive from active

Given a list of active_residues and a PDB structure, `passive_from_active` will return a list of
surface exposed passive residues within a 6.5A radius from the active residues.

When provided with a list of surface residues, `passive_from_active` will filter the list for those
that are within 6.5A from the active residues.

**Usage:**

    haddock3-restraints passive_from_active <pdb_file> <active_list> [-c <chain_id>] [-s <surface_list>]

This command is useful if few active residues are known and you want to enlarge the possible interface by adding passive residues.

## Active passive to ambig

Given two files containing active (in the first line) and passive (second line)
 residues to be used by HADDOCK, `active_passive_to_ambig` gives in output the corresponding
 `ambig.tbl` file.

**Usage:**
    
    haddock3-restraints active_passive_to_ambig file_actpass_one file_actpass_two [--segid-one] [--segid-two]

Here `file_actpass_one` and `file_actpass_two` are the files containing the active and passive residues for the first and second molecule, respectively. The two optional arguments (`--segid-one` and `--segid-two`) are used to specify the segment ID of the residues in the output `ambig.tbl` file.

## Restrain bodies

The `restrain_bodies` subcommand creates distance restraints to lock several 
chains together. It is useful to avoid unnatural flexibility or movement due to
sequence/numbering gaps.

As an example, this subcommand is crucial when docking an antibody to their cognate antigen (see for example [this tutorial](www.bonvinlab.org/education/HADDOCK3/HADDOCK3-antibody-antigen/#additional-restraints-for-multi-chain-proteins)), as the hypervariable region of an antibody is formed by two chains that are not covalently linked.

**Usage:**

	haddock3-restraints restrain_bodies <structure> [--exclude] [--verbose]

One can exclude some chains from this calculation using the `--exclude` option.

## Z surface restraints

`z-surface-restraints` generate both z-restraints and corresponding z-surfaces based on
input pdb structure and residue selection.

## Validate tbl

A simple subcommand to validate the content of a tbl file.

**Usage:**

    haddock3-restraints validate_tbl <tbl_file> [--silent] [--quick]

The `--silent` option will suppress the output of the validation (in case of success), while the `--quick` option will first check the global formatting first, before getting into the context.

# New version of the haddock-restraints

A new version of the haddock3-restraints is currently being developped.
This new implementation using *rust* will allow better maintainability as well as its deployment on various operating systems as well as on web-browser using WebAssembly.
Not yet part of the haddock3 intallation, you can already find it in its dedicated repository at [https://github.com/haddocking/haddock-restraints](https://github.com/haddocking/haddock-restraints).