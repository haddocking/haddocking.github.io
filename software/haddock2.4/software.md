---
layout: page
title: "HADDOCK 2.4 manual"
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
title: HADDOCK required and recommended third party software
image:
  feature: pages/banner_software.jpg
---


HADDOCK consists of a collection of  [python](https://www.python.org){:target="_blank"}  and  [CNS](http://cns-online.org/v1.3/){:target="_blank"}  scripts and some other additional programs and scripts (csh, awk, perl, c++).

* table of contents
{:toc}


### Required


#### CNS 

[CNS version 1.3](http://cns-online.org){:target="_blank"}: MANDATORY to run HADDOCK, TO BE OBTAINED AND INSTALL SEPARATELY, AND RECOMPILED WITH THE ADDITIONAL CODE PROVIDED WITH HADDOCK.


* * *

### Required for using coarse graining


#### Python.2.7

[python](https://www.python.org){:target="_blank"} version 2.7 is required in order to be able to convert the atomistic models into coarse grained models (see [coarse graining PDB files for docking](/software/haddock2.4/pdb-cg){:target="_blank"}.


#### Biopython 1.72

[Biopython](https://biopython.org/wiki/Download){:target="_blank"} version 1.72 is required in order to be able to convert the atomistic models into coarse grained models (see [coarse graining PDB files for docking](/software/haddock2.4/pdb-cg){:target="_blank"}.


#### DSSP

[DSSP](https://swift.cmbi.umcn.nl/gv/dssp){:target="_blank"} is required to define the secondary structure, an information required to select the proper backbone parameter for the Martini coarse grained model (see [coarse graining PDB files for docking](/software/haddock2.4/pdb-cg){:target="_blank"}.


* * *

### Recommended (depending on the type of data used)


#### NACCESS

[NACCESS](http://wolf.bms.umist.ac.uk/naccess){:target="_blank"} is a stand alone program that calculates the accessible area of a molecule from a PDB format file. It can calculate the atomic and residue accessibilities for both proteins and nucleic acids, and is available for free of charge for researchers at academic and non profit-making institutions. We make use of NACCESS in HADDOCK to filter active and passive residues based on their solvent accessible area (see section  [AIR restraints](/software/haddock2.4/generate_air){:target="_blank"} ).


#### FreeSASA

[FreeSASA](http://freesasa.github.io){:target="_blank"} offers the same functionality as NACCESS and can be installed without any license requirements.


#### ProFit

[ProFit](http://www.bioinf.org.uk/software/profit/){:target="_blank"} is designed to be the ultimate protein least squares fitting program. Some of the provided analysis tools in HADDOCK make use of Profit. Profit can be obtained free of charge for academics.


#### Pales

[Pales](http://spin.niddk.nih.gov/bax/software/PALES/index.html){:target="_blank"} is a software for analysis of residual dipolar couplings. Pales provides features for analysis of experimental dipolar couplings and dipolar coupling tensors, such as best-fitting a dipolar coupling tensor to its corresponding 3D structure. Pales can thus be used to derive the tensor components (Dxx, Dyy, Dzz or Da and R) needed for the use of dipolar couplings as restraints for docking.


#### Module

[Module](http://www.ibs.fr/science-213/scientific-output/software/module/?lang=en){:target="_blank"} is a software for analysis of residual dipolar couplings with a nice graphical interface. Modules allows the determination of alignment tensor parameters for individual or multiple domains in macromolecules from residual dipolar couplings and facilitates their manipulation to construct low-resolution models of macromolecular structure.


#### Tensor

[Tensor](http://www.ibs.fr/science-213/scientific-output/software/tensor/?lang=en){:target="_blank"} is software for analysis of diffusion anisotropy data (NMR relaxation) with a nice graphical interface. Tensor2 allows the determination of alignment tensor parameters for individual or multiple domains in macromolecules from diffusion anisotropy data and facilitates their manipulation to construct low-resolution models of macromolecular structure.


#### X3DNA

[X3DNA](https://x3dna.org){:target="_blank"} is a versatile package for the analysis, rebuilding, and visualization of three-dimensional nucleic acid structures, based on a standard reference frame (Olson _et al._, _J. Mol. Biol._**313**, 229-237, 2001). It is the software we are using to generate libraries of pre-bent DNA conformations for protein-DNA docking in our  [3D-DART web server](http://haddock.science.uu.nl/enmr/services/3DDART){:target="_blank"}.



* * *

### Other useful software

#### PSVS

[PSVS](https://montelionelab.chem.rpi.edu/PSVS/){:target="_blank"} is a structure validation server which integrates analyses from several widely-used structure quality evaluation tools, including RPF, PROCHECK, MolProbity, Verify3D, Prosa II, the PDB validation software, and various structure-validation tools.

#### LIGPLOT

[LIGPLOT](https://www.ebi.ac.uk/thornton-srv/software/LIGPLOT/){:target="_blank"} is a program for automatically plotting protein-ligand interactions or protein-protein interactions (use for that dimplot). It automatically generates schematic diagrams of protein-ligand interactions for a given PDB file. The interactions shown are those mediated by hydrogen bonds and by hydrophobic contacts.

#### NUCPLOT

[NUCPLOT](http://www.ebi.ac.uk/thornton-srv/software/NUCPLOT){:target="_blank"} is a program for automatically plotting protein-nucleic acid interactions. NUCPLOT can generate schematic diagrams automatically - directly from the 3D coordinates of the complex as found in a given PDB file. The program works for any single- or double-stranded protein-DNA, DNA-ligand and protein-RNA complexes.

#### WhatIF

[WhatIF](http://swift.cmbi.ru.nl/whatif){:target="_blank"} is a program for protein structure analysis, validation and repair. It is available as a [webserver](http://swift.cmbi.ru.nl/servers/html/index.html){:target="_blank"}. Can  be handy to repair/debump a model.

#### Grace

[Xmgr/Grace](http://plasma-gate.weizmann.ac.il/Grace/){:target="_blank"} is a graphing tool for UNIX.

#### PyMol

[Pymol](http://www.pymol.org/){:target="_blank"} is a very nice visualization (and much more) program for high-quality display of 3D molecular structures.


* * *
