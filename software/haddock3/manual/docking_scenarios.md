---
layout: page
title: ""
excerpt: ""
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, manual, usage]
image:
  feature: pages/banner_software.jpg
---

* table of contents
{:toc}

<hr>

# Examples of docking scenario

As creating a new workflow can be complex at the beginning, we are providing a set of pre-defined haddock3 scenarios.
These examples are encompassing a wide range of applications, such as:

- [Protein-protein docking](#protein-protein-docking)
- [Protein-DNA docking](#protein-dna-docking)
- [Antibody-antigen docking](#antibody-antigen-docking)
- [Small-molecule docking](#small-molecule-docking)
- [Complexes refinement protocols](#refinement-protocols)
- [Scoring workflow](#scoring-workflow)
- [Comparison to an experimental reference](#comparison-to-a-reference-structure)
- [Analysis pipelines](#analysis-pipeline)

Alternatively, upto date examples can also be found:
- in your local installation of haddock3: `haddock3/examples/`.
- online on our [GitHub repository `haddock3/examples/`](https://github.com/haddocking/haddock3/tree/main/examples).


Please note the extension scheme we are using in the provided configuration file examples:
- __*-full.cfg__: we are using the `*-full.cfg` suffix on protocols that have proper sampling, and therefore could be used in production. These are nice baseline workflow with appropriate parameters, but will obviously require more time to terminate the run.
- __*-test.cfg__: we are using the `*-test.cfg` suffix on protocols that have low sampling, allowing for fast test of the functionalities present in the workflow. Of note, on a daily basis, we are running most of the `*-test.cfg` configuration files to make sure the `main` branch of haddock3 is functional.


## Protein-protein docking

### Two body docking

blabla


### Symmetrical homotrimer docking 

The homotimer docking scenario, [available here](https://github.com/haddocking/haddock3/tree/main/examples/docking-protein-homotrimer), is first performing `[rigidbody]` docking, followed by `[flexref]` refinement and a final `[emref]` energy minimisation step of the complexe.
It also makes use of two types of symmetry restraints:
- [non-crystallographic symmetry restraints](/software/haddock3/manual/symmetry_restraints.md#non-crystallographic-symmetry): to make sure the three chains are having the same conformation.
- [C3 symmetry restraints](/software/haddock3/manual/symmetry_restraints.md#rotational-symmetry): to obtain solutions respecting the C3 symmetry.


### Multiple ambiguous files

In some case, restraints could be obtained from various sources; different experimental methods or multiple predictions.
In this case, knowing which AIR file will be leading to the correct complex can only be assessed once the docking is performed, and maybe some of them will lead to the same solutions.

It is possible to input multiple ambiguous restraints files in a single `.tgz` archive.
When providing the kind of input, each sampled docking solution will use an other AIR file contained in the archive.
A particular parameter should later be set in the downstream protocol, `previous_ambig = true`, enabling to use the AIR file used at the `[rigidbody]` stage and so on.

An example is [provided here](https://github.com/haddocking/haddock3/tree/main/examples/docking-multiple-ambig).


## Protein DNA docking

protein-DNA

## Antibody-antigen docking

Multiple antibody - antigen docking configuration files are [available here](https://github.com/haddocking/haddock3/tree/main/examples/docking-antibody-antigen).
They encompass various aspects of docking, mainly related to the information available to guide the docking:

- [No information about the paratop](#no-information-about-the-paratop): No information is known about the paratop, therefore tagetting the entire surface accessible resiude of the antigen.
- [Experimental knowledge of the paratop resiudes](#nmr-infomred-paratop): NMR data was aquired and allowed to obtain information about residues involded in the binding on the antigen side.


### No information about the paratop

When no information is known about the paratop on the antigen side, our only solution is to rely on the CDR loops of the antibody, as we know that a least a subset of the resiudes on those loops will be part of the interaction.
Two appoaches can then be used:
- One where a distance restraints file is generated, where CDR loops resiudes are targetting all surface residues on the antigen side.
- The other one defining random distance restraints between the CDR loops and random patches on the antigen side.

#### Using surface accessible resiudes

Generating restraints guiding the antibody CDR loops towards surface resiudes on the antigen side is a solution that will sample the entire surface of the antigen. For this, two major information must be extracted:

- The residue indices of the antibody CDR loops: can be predicted using bioinformatics tools such as [proABC2](https://wenmr.science.uu.nl/proabc2).
- The surface residue indices of the antigen: can be predicted computed using `haddock3-restraints calc_accessibility antigen.pdb`.

Defining the CDR loops as `active` residues and all surface residues on the antigen as `passive`, we can create an ambiguous restraints file `ambig.tbl`, that will guide the docking sampling the entire surface of the antigen while making sure the CDR loops are interacting. For more details on how to generate restraints, please refere to the [`haddock3-restraints` documention](/software/haddock3/manual/restraints_cli.md).

For such kind of naive approach, increasing the sampling at the `[rigidbody]` level is important.

Various examples are available:

- standard HADDOCK workflow: [docking-antibody-antigen-CDR-accessible-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-full.cfg)
- with intermediate clustering steps: [docking-antibody-antigen-CDR-accessible-clt-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-clt-full.cfg)
- using MPI to spread the workload:
  - [docking-antibody-antigen-CDR-accessible-full-mpi.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-full-mpi.cfg)
  - [docking-antibody-antigen-CDR-accessible-full-mpi.job](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-full-mpi.job)



#### Using random distance restraints

An other alternative for pseudo-naive antibody-antigen docking is to define random restraints.
In this case, we will define segments on the antibody CDR loops to limit the search on the antibody side, and do not provide any definition on the antigen side.
By doing so, random residues on the CDR loops will be restraints to random patches on the antigen surface accessible residues.
This is performed in the `[rigidbody]` module by:
- turning on the `randair` parameter
- defining 6 segments to define what are the CDR loops residues
- increasing the sampling

```toml
# Turning on the randair parameter
randair = true
# About to define 6 random segments for the antigen
nrair_1 = 6
# Start and end of first CDR loop
rair_sta_1_1 = 26
rair_end_1_1 = 32
# Start and end of second CDR loop
rair_sta_1_2 = 55
rair_end_1_2 = 57
# Start and end of third CDR loop
rair_sta_1_3 = 101
rair_end_1_3 = 108
# Start and end of fourth CDR loop
rair_sta_1_4 = 146
rair_end_1_4 = 152
# Start and end of fifth CDR loop
rair_sta_1_5 = 170
rair_end_1_5 = 172
# Start and end of sixth CDR loop
rair_sta_1_6 = 212
rair_end_1_6 = 215

# Increasing the sampling
sampling = 10000

###
# Insert other modules here if you want
###

[flexref]
contactairs = true
```

In this case, no AIR restraints files can be accepted (nor `unambig` and `hbond` ones).

Note that after random air definition, we will use `contactairs = true` in later stage modules such as `[flexref]` and `[emref]`, generating restraints based on resiudes already in contact, ensuring the complex will not detach.


Here are some examples:
- standard HADDOCK workflow: [docking-antibody-antigen-ranairCDR-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-full.cfg)
- with intermediate clustering steps: [docking-antibody-antigen-ranairCDR-clt-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-clt-full.cfg)
- using MPI to spread the workload:
  - [docking-antibody-antigen-ranairCDR-full-mpi.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-full-mpi.cfg)
  - [docking-antibody-antigen-ranairCDR-full-mpi.job](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-full-mpi.job)


### NMR infomred paratop

An ideal case would be to have information about the antigen paratop.
Coming from experimental methods or bioinformatic predictions, this information is extremly valuable as it will focus the  search by sampling comformations near key residues involed in the interaction.
By generating a dedicated ambiguous restraint file (`ambig-CDR-NMR-CSP.tbl`), only antigen CDR residues and few residues on the antigen side will be interacting.

Here is an  example: [docking-antibody-antigen-CDR-NMR-CSP-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-NMR-CSP-full.cfg)



## Small molecule docking

Small molecule docking can also be performed using haddock3.
It requires the use of custom topology and paramter files for the ligand, as it they are out of the scope of the OPLS force-field.
To generate them, please refere to the section: [How to generate topology and parameters for my ligand ?](/software/haddock3/manual/structure_requirements.md#How-to-generate-topology-and-parameters-for-my-ligand)

Two protocols have been proposed:
- [By homology docking using experimental template]():
- [By defining a binding site]():

### Homologuous shape docking

The use of experimental structure as template for docking have been shown to provide helpful information to guide the conformation of the ligand towards both the binding site and an adequate conformation (see: D3R, CAPRI16 and Atom3.)
Examples on how to 

### Using binding site definition

Restraints files guiding towards resiudes in the binding site.



## Refinement protocols

All refinements examples can be found [here](https://github.com/haddocking/haddock3/tree/main/examples/refine-complex).

### Energy minimisation

`[emref]`

### Short molecular dynamics symulation in explicit solvent

Using the `[mdref]`, you can start from an initial model and use CNS to run multiple MD simulations in parallel with different initial seeds to refine a complex.
This simple procedure requires the use of two modules only and the tuning of the `sampling_factor` parameter in `[mdref]`.

Here is an example:
```toml
run_dir = "mdref_complex_5replicas"
molecules = "model.pdb"
[topoaa]
[mdref]
# Setting sampling factor to 5 will generate 5 replicas with different initial seeds to set the velocities
sampling_factor = 5
```

[Here is a full example](https://github.com/haddocking/haddock3/blob/main/examples/refine-complex/refine-complex-test.cfg) with provided input file and also using an experimental reference to track the evolution of the refinement.


### OpenMM MD simulation

The OpenMM molecular dynamics engine has its own module in haddock3, where users can setup short molecular dynamics similation using openMM.
It can be used as a refinement module, in implicit or explicit solvent.
Note that the use of the `[openmm]` module is a thirdparty module that requires its own installation procedure that is not part of the standard haddock3 suite.

#### As refinement module

Simple MD simulation, without restraints !

#### As quality assessment of a docking pose

Zusanna, MD to the rescue.

Using the `[openmm]` module allows to run unbiased molecular dynamics simulations in explicit solvent.
Previous work of [Zusanna et, al., MD to the rescue.](), showed that near-native complexes have less deviation from their input structure after 10 ns of simulation.
Setting up such kind of experiment with haddock3 is extremely easy, as it simply requires to use the `[openmm]` module with an input complex, followed by the `[caprieval]` using the same input complex as reference structure.
This will allow to track how far from the original pose the final frame reached.

Here is an example configuration file:
```toml
# General parameters
run_dir = "md_to_the_rescue"
molecules = "model_1.pdb"

[topoaa]
[openmm]
# Define the timesteps
timestep_ps = 0.002
# Increase the simulation timesteps (500000 * 0.002 = 10 ns)
simulation_timesteps = 5000000
# Save 100 intermediate frames
save_intermediate = 100
# Define force-field
forcefield = 'amber14-all.xml'
# Use TIP3P explicit water model
explicit_solvent_model = 'amber14/tip3p.xml'
# Keep HBonds rigid
constraints = 'HBonds'
# Generate a final ensemble composed of all the frames
generate_ensemble = true

[topoaa]
# Compare the generated ensemble with the initial model
[caprieval]
reference_fname = "model_1.pdb"
sort_by = "dockq"
```

This protocol has been used during CAPRI round 55 for target 231, to validate the docking poses of the FLAG-peptide on the antibody (see: [CAPRIpaper]()).


## Scoring workflow

### Energy minimised scoring

`[emscoring]`

### Short molecular dynamics in explicit solvent

`[mdscoring]`


### Using scoring command line


Haddock3 also contain a simple command line interface that allows you to score a single pdb file.
To do so, just run:
```bash
haddock3-score complex.pdb
```

This command is a short-cut to the following parameter file, and therefore can be really handy, as it simplify a lot the procedure, but is limitted to the scoring of a single model.
```toml
run_dir = "tmp_score"
molecules = "complex.pdb"
[topoaa]
[emscoring]
```

For more details on the `haddock3-score` CLI, please refere to [this section](/software/haddock3/module/clis.md#haddock3-score).

### Hot spot detection

`[alascan]`

## Comparison to a reference structure


## Analysis pipeline

The addition and inclusion of analysis modules in haddock3 is one of its major new strength, as it allows to perform various kind of analysis directly during the workflow.
For the complete list of analysis modules and their capabilities, please refere to the [Analysis Modules section](software/haddock3/manual/modules/analysis.md).


### Fine tuning clustering parameters

Finding the appropriate threshold for the clustering parameters can be quite tricky, and often requires a first trial, followed by manual inspection to understand the content of the dataset.
We are providing examples (for `clustrmsd` and `clustfcc`) fine tuning of the parameters with visualisation of the matrices, to help you understand how to investigate the results you obtained after clustering.

Here are the two important step to analyse the structural diversity of you set of complexes in a clustering module:
- turn on the `plot_matrix` parameter to obtain a visual representation of the distance matrix.
- set the `min_population` to 1, so even singloton complexes will be forwarded to the next module and displayed on the plot.

Here are some examples:
- [fine tuning of the `clustrmsd` parameters](https://github.com/haddocking/haddock3/blob/main/examples/analysis/plot-finetune-ilrmsdmatrix-clustrmsd.cfg).
- [fine tuning of the `clustfcc` parameters](https://github.com/haddocking/haddock3/blob/main/examples/analysis/plot-finetune-clustfcc.cfg).


Note that fine tuning of clustering parameters can also be performed with the `haddock3-re` command, as both `[clustfcc]` and `[clustrmsd]` handle this `re`-computation approach.


# Web-application pre-defined scenario


*comming soon...*
