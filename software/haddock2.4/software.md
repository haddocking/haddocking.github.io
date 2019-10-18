---
layout: page
title: "HADDOCK 2.4 manual"
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---



# <font color="RED">S</font>oftware <font color="RED">L</font>inks

* * *

HADDOCK consists of a collection of  [python](http://www.python.org)  and  [CNS](http://cns.csb.yale.edu)  scripts and some other additional programs and scripts (csh, awk, perl, c++).

* table of contents
{:toc}


### Needed:

*  **[CNS (http://cns-online.org)](http://cns-online.org)**: MANDATORY to run HADDOCK, TO BE OBTAINED AND INSTALL SEPARATELY

### Also recommended are:

*  **[NACCESS](http://wolf.bms.umist.ac.uk/naccess)**: Naccess is a stand alone program that calculates the accessible area of a molecule from a PDB format file. It can calculate the atomic and residue accessibilities for both proteins and nucleic acids, and is available for free of charge for researchers at academic and non profit-making institutions. We make use of NACCESS in HADDOCK to filter active and passive residues based on their solvent accessible area (see section  [AIR restraints](/software/haddock2.4/generate_air_help) ).
*  **[ProFit](http://www.bioinf.org.uk/software)**: ProFit is designed to be the ultimate protein least squares fitting program. Some of the provided analysis tools in HADDOCK make use of Profit. Profit can be obtained free of charge for academics at http://www.bioinf.org.uk/software
*  **[Pales](http://spin.niddk.nih.gov/bax/software/PALES/index.html)**: PALES is a software for analysis of residual dipolar couplings. Pales provides features for analysis of experimental dipolar couplings and dipolar coupling tensors, such as best-fitting a dipolar coupling tensor to its corresponding 3D structure. Pales can thus be used to derive the tensor components (Dxx, Dyy, Dzz or Da and R) needed for the use of dipolar couplings as restraints for docking.
*  **[Module](http://www.ibs.fr/science-213/scientific-output/software/module/?lang=en)**: Modules is another useful software for analysis of residual dipolar couplings with a nice graphical interface. Modules allows the determination of alignment tensor parameters for individual or multiple domains in macromolecules from residual dipolar couplings and facilitates their manipulation to construct low-resolution models of macromolecular structure.
*  **[Tensor](http://www.ibs.fr/science-213/scientific-output/software/tensor/?lang=en)**: Tensor is another useful software for analysis of diffusion anisotropy data (NMR relaxation) with a nice graphical interface. Tensor2 allows the determination of alignment tensor parameters for individual or multiple domains in macromolecules from diffusion anisotropy data and facilitates their manipulation to construct low-resolution models of macromolecular structure.
*  **[3DNA](https://x3dna.org)**: 3DNA is a versatile package for the analysis, rebuilding, and visualization of three-dimensional nucleic acid structures, based on a standard reference frame (Olson _et al._, _J. Mol. Biol._**313**, 229-237, 2001). It is the software we are using to generate libraries of pre-bent DNA conformations for protein-DNA docking in our  [3D-DART web server](http://haddock.science.uu.nl/enmr/services/3DDART) .

### Here are a few links to other useful software:

*  **[PSVS](http://psvs-1_5-dev.nesg.org)**: Another nice structure validation server which integrates analyses from several widely-used structure quality evaluation tools, including RPF, PROCHECK, MolProbity, Verify3D, Prosa II, the PDB validation software, and various structure-validation tools.
*  **[LIGPLOT](https://www.ebi.ac.uk/thornton-srv/software/LIGPLOT/)**: LIGPLOT is a program for automatically plotting protein-ligand interactions or protein-protein interactions (use for that dimplot). It automatically generates schematic diagrams of protein-ligand interactions for a given PDB file. The interactions shown are those mediated by hydrogen bonds and by hydrophobic contacts.
*  **[NUCPLOT](http://www.ebi.ac.uk/thornton-srv/software/NUCPLOT)**: NUCPLOT is a program for automatically plotting protein-nucleic acid interactions. NUCPLOT can generate schematic diagrams automatically - directly from the 3D coordinates of the complex as found in a given PDB file. The program works for any single- or double-stranded protein-DNA, DNA-ligand and protein-RNA complexes.
*  **[WhatIF](http://swift.cmbi.ru.nl/whatif)**: This is a program for protein structure analysis, validation and repair. It is available as a  [webserver](http://swift.cmbi.ru.nl/servers/html/index.html) .
*  **[Xmgr/Grace](http://plasma-gate.weizmann.ac.il/Grace/)**: A very nice graphing tool for UNIX.
*  **[Rasmol](http://www.umass.edu/microbio/rasmol/index2.htm)**: This molecular graphics program displays your PDB structures on screen using X graphics and enables you to rotate, display and color the structure in a number of ways. Very convenient for a Quick look at a structure. We use it for example to display, select and color active and passive residues for HADDOCK (see section  [AIR restraints](/software/haddock2.4/generate_air_help) )
*  **[Pymol](http://www.pymol.org/)**: This is a very nice visualization (and much more) program for high-quality display of 3D molecular structures.
*  **[Molscript](http://avatar.se/molscript/)**: This is a script-driven program for high-quality display of molecular 3D structures in both schematic and detailed representations. You can get an academic license for free from  [Avatar](http://avatar.se/molscript/) .

### Here are a few links to scoring-related software:

*  **[MOLPROBITY](http://molprobity.biochem.duke.edu/)**: MOLPROBITY can be used to assess the packing and hydrogen-bonding quality of an interface.
*  **[CCHarPPI](http://life.bsc.es/pid/ccharppi)**: CCharPPI integrates many binding affinity and scoring functions into a single web server. It calculates up to 108 parameters, including models of electrostatics, desolvation and hydrogen bonding, as well as interface packing and complementarity scores, empirical potentials at various resolutions, docking potentials and composite scoring functions.
*  **[FastContact](http://structure.pitt.edu/software/FastContact)**: FastContact is a free energy scoring tool for protein-protein complex structures based on electrostatic and desolvation energies.
*  **[DComplex](http://compbio.iupui.edu/group/4/pages/downloads)**: DComplex uses the DFIRE energy function for the prediction of binding affinities.
*  **[FoldX](http://foldx.crg.es/)**: FoldX is a program for calculating the folding pathways of proteins and for calculating the effect of a point mutation on the stability of a protein.
*  **[PISA](http://www.ebi.ac.uk/msd-srv/prot_int/pistart.html)**: PISA is an interactive tool for the exploration of macromolecular (protein, DNA/RNA and ligand) interfaces, prediction of probable quaternary structures (assemblies), database searches of structurally similar interfaces and assemblies, as well as searches on various assembly and PDB entry parameters.

* * *
