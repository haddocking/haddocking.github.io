---
layout: page
title: "Advanced refinement of molecular complexes"
tags: [Jekyll, HADDOCK, Tips, Tricks, Refinement, Water, Advanced, Docking, Simulation, Computational Biology, Modelling, Protein Structure]
modified: 2017-02-24T14:44:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

HADDOCK2.2 provides a dedicated web interface to run a refinement on a molecular complex. This nice feature is accessible 
via the [refinement interface][refinement_page] of HADDOCK2.2 and required a [registered account][register_page] with 
Expert level access.

As input, only a PDB file for each partner of the complex (for a unique PDB file, you need to specify two different chain 
IDs). You can optionally change the weight of the different energy terms used in the HADDOCK score to assess the 
quality of your models.
A fine-tuned set of parameters will be then used by HADDOCK to perform the water refinement.

However, it is sometimes interesting to tune this default set of parameters to cope with particular cases like unusual histidine
protonation states, multibody docking, ensemble and/or cross-docking, etc.
To do so, it is possible to use the HADDOCK [Guru interface][guru_page] (needs Guru access level) and change few parameters to only 
use the refinement capability of HADDOCK:

In the **"Distance Restraints"** section:

* _Define center of mass restraints to enforce contact between the molecules_ → **True**
* _Define surface contact restraints to enforce contact between the molecules_ → **True**

In then **"Sampling parameters"** section:

* _Number of structures for rigid body docking (it0)_ → Same as the number of models you want HADDOCK to generate in water
* _Number of structures for rigid body docking (it1)_ → Same as the number of models you want HADDOCK to generate in water
* _Sample 180 degrees rotated solutions during rigid body EM_ → **False**

In then **"Advanced Sampling Parameters"** section:

* _Perform cross-docking_ → **False**
* _Multiply the number of calculated structures by all combinations_ → **True**
* _Randomize starting orientations_ → **False**
* _Perform initial rigid body minimisation_ → **False**
* _Allow translation in rigid body minimisation_ → **False**
* _Number of MD steps ..._*4 → **0** for the 4 values (respectively 500/500/1000/1000 by default)

Those few changes will force HADDOCK to only perform a water refinement as if you would have submitted your run via the
[refinement interface][refinement_page]. You can then change any other parameters to suit your needs and submit your run
in the [guru interface][guru_page].



[refinement_page]: https://alcazar.science.uu.nl/services/HADDOCK2.2/haddockserver-refinement.html "HADDOCK refinement interface"
[guru_page]: https://alcazar.science.uu.nl/services/HADDOCK2.2/haddockserver-guru.html "HADDOCK guru interface"
[register_page]: https://wenmr.science.uu.nl/auth/register"HADDOCK registration page"
