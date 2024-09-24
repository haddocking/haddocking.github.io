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

- [Protein-protein docking](#protein-protein-docking):
- [Protein-DNA docking](#protein-dna-docking):
- [Antibody-antigen docking](#antibody-antigen-docking):
- [Small-molecule docking](#small-molecule-docking):
- [Complexes refinement protocols](#refinement-protocols):
- [Scoring workflow](#scoring-workflow):
- [Comparison to an experimental reference](#comparison-to-a-reference-structure):
- [Analysis pipelines](#analysis-pipeline):

Alternatively, upto date examples can also be found on our [GitHub repository `haddock3/examples/`](https://github.com/haddocking/haddock3/tree/main/examples).


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



#### Using random distance restraints




### NMR infomred paratop




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

### Energy minimisation

`[emref]`

### Short molecular dynamics symulation in explicit solvent

`[mdref]`

### OpenMM MD simulation

#### As refinement module

Simple MD simulation, without restraints !

#### As quality assessment of a docking pose

Zusanna, MD to the rescue.

## Scoring workflow

### Energy minimised scoring

### Short molecular dynamics in explicit solvent

### Hot spot detection


## Comparison to a reference structure


## Analysis pipeline



# Web-application pre-defined scenario

*comming soon...*
