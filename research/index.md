---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_research-mini.jpg
---

Research within the computational structural biology group focuses on the development of reliable bioinformatics and computational 
approaches to predict, model and dissect biomolecular interactions at atomic level. For this, bioinformatics data, structural 
information and available biochemical or biophysical experimental data are combined to drive the modelling process. 
This is implemented and further developed in the widely used 
[HADDOCK software for the modelling of biomolecular complexes](/software/haddock2.2).
By following a holistic approach integrating various experimental information sources with computational structural biology methods 
we aim at obtaining a comprehensive description of the structural and dynamic landscape of complex biomolecular machines, adding 
the structural dimension to interaction networks and opening the route to systematic and genome-wide studies of biomolecular 
interactions.

### HADDOCK

[HADDOCK](/software/haddock2.4) is a pioneer software in data-driven (or integrative) modelling of protein interactions and our flagship project. 
Developed since 2003 in our lab, it has been cited more than 1500 times. A [user-friendly web server](https://wenmr.science.uu.nl/haddock2.4)
is also available. HADDOCK is well-known for its ability to integrate data in the modelling calculations, such as:

* *Nuclear Magnetic Resonance*: H/D Exchange, CSPs, RDCs (SANI, VEAN), PREs, PCSs, NOEs, Relaxation data (DANI)
* *Mutagenesis*
* *Mass Spectromety*: H/D Exchange, Cross-linking, scoring based on Ion Mobility-MS shape data
* *Small Angle X-ray Scattering*: Radius of Gyration, scoring based on experimental SAXS curves
* *Bioinformatics predictions*: evolutionary conservation and co-evolving amino acids

Other interesting features of HADDOCK include:

* Unambiguous Distance Restraints
* Ambiguous Interaction Restraints
* Flexibility of the backbone/sidechain atoms at the interface
* (Simultaneous) Multibody Docking (up to 6 molecules)
* Symmetry restraints (C2, C3, C4, C5, C6, D2, ...)
* Support for proteins, DNA, RNA, peptides, and small ligands (via PRODRG)
* Solvated Docking protocol to model _wet_ interfaces

### Binding Affinity Prediction

Interactions between proteins are a beautifully orchestrated event that underlie cellular function.
The binding affinity, as defined in physico-chemical terms by the dissociation constant (Kd), is what determines if a certain interaction occurs or not in solution.
Predicting binding affinity from structural models is an active field of research for more than 40 years, greatly because of its importance for drug development.
Current methodologies fail however to predict binding affinity of protein-protein complexes from their atomic structures. 
At the Bonvin lab, we investigate and develop new models to describe the descriptors behind the affinity of protein interactions, based mainly on biophysical properties
that can be derived from their structures (or models).

### CAPRI

The Bonvin lab participates in the Critical Assessment of Prediction of Interactions ([CAPRI](https://www.ebi.ac.uk/msd-srv/capri/)).
This is a fun experiment in which research groups are given the sequence (and sometimes partial structures) of an unknown biomolecular complex (e.g. protein-protein, protein-DNA, ...)
and are tasked with modelling it using their software. The results are then compared to the unreleased structures that only the CAPRI committee holds (and their authors obviously).
This serves not only as a perfect playground for HADDOCK but also as a medium for improvement and development of new features.
Currently, HADDOCK and the Bonvin Lab rank #1 in CAPRI, an achievement that makes us all proud!
