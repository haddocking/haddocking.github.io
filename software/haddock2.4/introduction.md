---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK2.4</font> manual

## <font color="RED">I</font>ntroduction




HADDOCK (High Ambiguity Driven biomolecular DOCKing) is an information-driven flexible docking approach for the modelling of biomolecular complexes (Dominguez et al. 2003). Docking is defined as the modelling of the structure of a complex based on the known three-dimensional structures of its constituents. HADDOCK distinguishes itself from other docking methods by incorporating a wide variety of experimental and/or bioinformatics data to drive the modelling (Melquiond and Bonvin, 2010). This allows concentrating the search to relevant portions of the interaction space using a more sophisticated treatment of conformational flexibility.  

Interface regions can be identified by mutagenesis, H/D exchange and chemical modifications (e.g. by cross-linkers or oxidative agents) detected by mass spectrometry, nuclear magnetic resonance, chemical shift perturbations and cross-saturation transfer. When experimental data are unavailable or scarce, this information can be supplemented by bioinformatics predictions (de Vries and Bonvin, 2008). These diverse information sources typically only identify or predict interfacial regions, but do not define the contacts across an interface. HADDOCK deals with this by implementing them as ambiguous interaction restraints (AIRs) that will force the interfaces to come together without imposing a particular orientation.  

HADDOCK can also incorporate classical NMR restraints such as distances from nuclear Overhauser effects and paramagnetic relaxation enhancement measurements, pseudo-contact shift, dihedral angles, residual dipolar coupling and diffusion anisotropy restraints, the latter two providing valuable information about the relative orientation of the components in a complex. In addition, symmetry restraints can be defined in the case of symmetrical homomeric systems. Other valuable information can be obtained from low-to-medium resolution techniques such as small angle X-ray scattering, cryo-electron microscopy and ion mobility mass spectrometry that can provide valuable information about the shape of a complex.  

The docking protocol in HADDOCK, which makes use of the Crystallography and NMR System (CNS) package as computational engine, consists of three successive steps:

*   rigid-body energy minimization
*   semi-flexible refinement in torsion angle space
*   final refinement in explicit solvent refinement.

By allowing for explicit flexibility during the molecular dynamics refinement HADDOCK can account for small conformational changes occurring upon binding. Larger and more challenging conformational changes can be dealt with by starting the docking from ensembles of conformations and/or treating the molecules as a collection of domains. The latter approach makes use of the unique multi-body docking ability of HADDOCK, which can handle up to 6 separate domains or molecules at the same time. The selection of the final models is based on a weighted sum of electrostatics, desolvation and van der Waals energy terms, along with the energetic contribution of the restraints used to drive the docking. HADDOCK has been extensively applied to a large variety of systems, including protein-protein, protein-nucleic acids and protein-small molecule docking and has shown a very strong performance in the blind critical assessment of the prediction of interactions (CAPRI). A considerable number of experimental structures of complexes calculated using HADDOCK have been deposited into the Protein Data Bank (PDB). HADDOCK is available as a web server ([http://haddock.chem.uu.nl/services/HADDOCK](http://haddock.chem.uu.nl/services/HADDOCK)) (de Vries et al. 2010) offering a user-friendly interface to the structural biology community.  

A list of HADDOCK-related publications is availble [here](/software/haddock2.2/publications).  

On our HADDOCK home page you will find:

*   general information on HADDOCK
*   tools to generate AIR restraint files and to setup projects
*   instructions to obtain HADDOCK
*   links to the various softwares required to run HADDOCK
*   a manual describing the use of HADDOCK
*   a frequently asked questions section
*   various tutorials

* * *
