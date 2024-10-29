# Generating restraints with Haddock3

Ambiguous (or not) restraint files must comply with the CNS syntax.
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
- [calc_accessibility](#calc-accessibility): Compute solvent-accessible residues from an input PDB file.
- [passive_from_active](#passive-form-active): Generates a list of solvent-accessible residues near a list of residues.
- [active_passive_to_ambig](#active-passive-to-ambig): Generates a ambiguous/unambiguous restraints file from two *active/passive* residue selections.
- [restrain_bodies](#restrain-bodies): Generates restraints within the same chain. Useful when chain breaks are present or multiple proteins are defined as a single chain.
- [z_surface_restraints](#z-surface-restraints): Generates surfaces and restraints selected residues to it.
- [validate_tbl](#validate-tbl): Validate the content of an ambiguous/unambiguous restraints file.


## Calc Accessibility

Given a PDB file, `calc_accessibility` will calculate the relative accessibility of
the side chains and return a list of surface-exposed residues.

Nucleic acid bases are considered to be always accessible.

This command is particularly useful when little interface information is available for one biomolecule and one wants to identify (and then target) all the surface exposed residues on a certain protein.

**Usage:**

```bash
haddock3-restraints calc_accessibility <input_pdb_file> [-c <cutoff>] [--log_level <log_level>] [--export_to_actpass]
```

**Arguments**:
```bash
positional arguments:
  input_pdb_file        input PDB structure.

options:
  -h, --help            show this help message and exit
  -c CUTOFF, --cutoff CUTOFF
                        Relative cutoff for sidechain accessibility
  --log_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level
  --export_to_actpass   Export the exposed residues as passive to an actpass file
```

## Passive from active

Given a list of active_residues and a PDB structure, `passive_from_active` will return a list of
surface exposed passive residues within a 6.5A radius from the active residues.

When provided with a list of surface residues, `passive_from_active` will filter the list for those
that are within 6.5A from the active residues.

**Usage:**

```bash
haddock3-restraints passive_from_active <pdb_file> <active_list> [-c <chain_id>] [-s <surface_list>]
```

**Arguments**:
```bash
positional arguments:
  structure             input PDB structure.
  active_list           List of active residues IDs (int) separated by commas

options:
  -h, --help            show this help message and exit
  -c CHAIN_ID, --chain-id CHAIN_ID
                        Chain id to be used in the PDB file (default: All)
  -s SURFACE_LIST, --surface-list SURFACE_LIST
                        List of surface residues IDs (int) separated by commas
```

This command is useful if few active residues are known and you want to enlarge the possible interface by adding passive residues.


## Active passive to ambig

Given two files containing active (in the first line) and passive (second line) residues to be used by HADDOCK, `active_passive_to_ambig` gives in output the corresponding `ambig.tbl` file.

**Usage:**
```bash 
haddock3-restraints active_passive_to_ambig file_actpass_one file_actpass_two [--segid-one] [--segid-two]
```

Here `file_actpass_one` and `file_actpass_two` are the files containing the active and passive residues for the first and second molecule, respectively. The two optional arguments (`--segid-one` and `--segid-two`) are used to specify the segment ID of the residues in the output `ambig.tbl` file.


**Arguments**:
```bash
positional arguments:
  actpass_one           First actpass file
  actpass_two           Second actpass file

options:
  -h, --help            show this help message and exit
  --segid-one SEGID_ONE
                        Segid to use for the first model
  --segid-two SEGID_TWO
                        Segid to use for the second model
```

## Restrain bodies

The `restrain_bodies` subcommand creates distance restraints to lock several 
chains together. It is useful to avoid unnatural flexibility or movement due to
sequence/numbering gaps.

As an example, this subcommand is crucial when docking an antibody to its cognate antigen (see for example [this tutorial](www.bonvinlab.org/education/HADDOCK3/HADDOCK3-antibody-antigen/#additional-restraints-for-multi-chain-proteins)), as the hypervariable region of an antibody is formed by two chains that are not covalently linked.

**Usage:**
```bash
haddock3-restraints restrain_bodies <structure> [--exclude] [--verbose]
```

**Arguments**:
```bash
positional arguments:
  structure             The PDB structure to be restrained.

options:
  -h, --help            show this help message and exit
  -e EXCLUDE, --exclude EXCLUDE
                        Chains to exclude from the calculation.
  -v VERBOSE, --verbose VERBOSE
                        Tune verbosity of the output.
```

One can exclude some chains from this calculation using the `--exclude` option.

## Z surface restraints

The `z_surface_restraints` subcommand generates both z-surfaces (x,y plans at a given z coordinate) 
and corresponding based on input PDB structure and residue selection.
This is useful to mimic membranes and make sure the protein will stay in the plan.

**Usage:**
```bash
haddock3-restraints z_surface_restraints --pdb <structure> --residues 7,50,53,71 --output z_restraints
```

This command will generate a plan at x,y plan at z==0 (`z_restraints_beads.pdb`), and a restraint file (`z_restraints.tbl`).

Note that you can have multiple sets of comma-separated residues (e.g: `7,50,53,71 1,2,3`) by separating them by spaces.
If you do so, multiple surfaces will be generated and each residue selections will be restraints to a plan.


**Arguments**:
```bash
options:
  -h, --help            show this help message and exit
  --pdb PDB, -p PDB     Path to a pdb file.
  --residues RESIDUES [RESIDUES ...], -r RESIDUES [RESIDUES ...]
                        List of comma-separated residues (can be multiple selections). Example 1,2,3 7,8,9 for two selections.
  --output OUTPUT, -o OUTPUT
                        Base output path. This script will generate two files, therefore no extension needed here
  --spacing SPACING, -s SPACING
                        Spacing between two beads (A)
  --x-size X_SIZE, -x X_SIZE
                        Size of the plan in X dimension (A)
  --y-size Y_SIZE, -y Y_SIZE
                        Size of the plan in Y dimension
  --z-padding Z_PADDING, -z Z_PADDING
                        Additional padding between two external plans.
```

## Validate tbl

A simple subcommand to validate the content of a tbl file.

**Usage:**
```bash
haddock3-restraints validate_tbl <tbl_file> [--silent] [--quick]
```

**Arguments**:
```bash
positional arguments:
  tbl_file    TBL file to be validated

options:
  -h, --help  show this help message and exit
  --pcs       PCS mode
  --quick     Check global formatting before going line by line (opening/closing parenthesis and quotation marks
  --silent    Only output errors, do not output TBL file at the end
```

The `--silent` option will suppress the output of the validation (in case of success), while the `--quick` option will first check the global formatting first, before getting into the context.


# New version of the haddock-restraints

A new version of the haddock3-restraints is currently being developed.
This new implementation using *rust* will allow better maintainability as well as its deployment on various operating systems as well as on web-browser using WebAssembly.
Not yet part of the haddock3 intallation, you can already find it in its dedicated repository at [https://github.com/haddocking/haddock-restraints](https://github.com/haddocking/haddock-restraints).
