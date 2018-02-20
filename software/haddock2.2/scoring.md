---
layout: page
title: "HADDOCK2.2 scoring function"
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---
The HADDOCK scoring function consists of a linear combination of various energies and buried surface area.
It differs for the various docking stages (rigid body (it0), semi-flexible refinement (it1) and explicit solvent refinement(water)).

The scoring is
performed according to the _weighted sum_ (HADDOCK score) of the following terms:

* _Evdw_: van der Waals intermolecular energy
* _Eelec_: electrostatic intermolecular energy
* _Eair_: distance restraints energy (only unambiguous and AIR (ambig) restraints)
* _Erg_: radius of gyration restraint energy
* _Esani_: direct RDC restraint energy
* _Evean_: intervector projection angle restraints energy
* _Epcs_: pseudo contact shift restraint energy
* _Edani_: diffusion anisotropy energy
* _Ecdih_: dihedral angle restraints energy
* _Esym_: symmetry restraints energy (NCS and C2/C3/C5 terms)
* _BSA_: buried surface area
* _dEint_: binding energy (Etotal complex - Sum[Etotal components] )
* _Edesol_: desolvation energy 


The default scoring function settings of HADDOCK are for protein-protein complexes and use the following weights:

<pre>
* HADDOCKscore-it0   = 0.01 Evdw + 1.0 Eelec + 1.0 Edesol + 0.01 Eair - 0.01 BSA
* HADDOCKscore-it1   =  1.0 Evdw + 1.0 Eelec + 1.0 Edesol +  0.1 Eair - 0.01 BSA
* HADDOCKscore-water =  1.0 Evdw + 0.2 Eelec + 1.0 Edesol +  0.1 Eair
</pre>

**Note:** Additional terms are used if other types of experimental restraints are used. Refer to values defined in `run.cns` (and accessible at the guru level of the [HADDOCK portal](http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-guru.html)) for their default settings.

**Note:** For protein-ligand (small molecule) docking we recommend to change the weight of Evdw(it0) to 1.0 and Eelec(water) to 0.1.

**Note:** For protein-nucleic acids docking we recommend to set the Edesol weight to 0 for all stages

The structure with the smallest weighted sum will be ranked first.
