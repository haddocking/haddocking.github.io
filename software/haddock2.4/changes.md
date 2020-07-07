---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK2.4</font> manual

### Lastest changes - version July 2020

- Added support for glycosylated proteins
- Improved diagnostics
- Minor fixes and code cleaning
 

### Changes - version June 2020

- Adapted the CG-to-AA conversion script to allow to morph larger conformational changes
  and use secondary structure restraints
- Corrected an issue in automatic secondary structure definition leading failures for very large systems
- Exposed a new parameter in run.cns (flcut_nb) that allows to control the distance cutoff to automatically
  define semi-flexible regions


	
### Changes with respect to version 2.2

- Extension to up to 20 molecules docking
- Coarse grained docking implemented based on the Martini force field v2.2
  for both proteins and nucleic acids
- Z-restraining potential as implicit membrane restraining potential
- Cryo-EM restraints implementation
- Added option to turn off (partially) analysis (speeds up the overall running time)
  Default settings only perform clustering
- For refinement (randorien=false), missing atoms are now rebuilt in the context of the complex
- Added automatic identification of cyclic peptides
- Added automatic idenfification of D-amino acids
- Added support for C6 symmetry
- Added support for shapes
- Added option to automatically define HIS protonation states based on electrostatic energy
- Changed default dielectric treatment to distance dependent dielectric with eps=10 for it0 and 1 for it1
  (Note should not be used for nucleic acids and coarse graining)
- Turn off by default explicit solvent final refinement (only EM performed)
- Switched nucleic acid support to use 1/2 letter code for RNA/DNA
- Added option to fix molecules in their original position


* * *

<font size="-1">Please send any suggestions or enquiries to Alexandre Bonvin</font>
