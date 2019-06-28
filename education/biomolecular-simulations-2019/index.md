---
layout: page
title: "BioExcel Summer School on Biomolecular Simulations 2019"
tags: [HADDOCK, docking, covalent docking, CPMD, metadynamics, molecular simulations, tutorials, BioExcel, summer school]
image:
  feature: pages/banner_education-thin.jpg
---
<figure align="center">
<a href="http://www.bioexcel.eu"><img src="/images/Bioexcel_logo.png"></a>
</figure>

On this page, you can find the links to the [**metadynamics**](/education/biomolecular-simulations-2019/Metadynamics_tutorial) (using Gromacs) and [**HADDOCK**](/education/biomolecular-simulations-2019/HADDOCK_tutorial) tutorials given during the [BioExcel Summer School on Biomolecular Simulations 2019](https://bioexcel.eu/events/bioexcel-summer-school-on-biomolecular-simulations-2019/) in Pula, Italy. These illustrate how metadynamics can be used to sample conformation of a binding pocket, and those conformation are subsequently used for docking a covalent ligand using HADDOCK. The conformational sampling approach is following the EDES approach described in the following publication:

* A. Basciu,  G. Malloci,  F. Pietrucci,  A.M.J.J. Bonvin and A.V. Vargiu.
[Holo-like and druggable protein conformations from enhanced-sampling of binding pocket shape](http://dx.doi.org/10.1021/acs.jcim.8b00730). _J. Chem. Inf. and Mod._ *59*, 1515-1528 (2019).

The [**Metadynamics**](/education/biomolecular-simulations-2019/Metadynamics_tutorial) tutorial highlights the benefits of enhanced sampling using metadynamics to improve the predictive power of molecular docking for protein-small molecule targets, in the case of binding sites undergoing conformational changes. For this, we will first generate an ensemble of conformers for the target protein using [GROMACS](http://www.gromacs.org/) and [PLUMED](http://www.plumed.org/), before proceeding with the docking using [HADDOCK](http://www.bonvinlab.org/software/haddock2.2/)

The [**HADDOCK covalent docking**](/education/biomolecular-simulations-2019/HADDOCK_tutorial) protocol shall not be seen, *yet*, as a well-established protocol for the modelling of covalently bound ligands but rather as a preliminary work to address this particular challenge in protein-small molecules docking. The 2019 version of this tutorial is based on our new HADDOCK2.4 web portal. The [2018](/education/biomolecular-simulations-2018) version of this tutorial describes the use of the HADDOCK2.2 portal.


## Tutorials

* [**Metadynamics**](/education/biomolecular-simulations-2019/Metadynamics_tutorial):
  This tutorial explains how to perform metadynamics simulations to enhance the comformational sampling of a binding site on a protein to improve molecular docking predictions.

* [**HADDOCK2.4 covalent binding**](/education/biomolecular-simulations-2019/HADDOCK_tutorial):
  This tutorial demonstrates how to use HADDOCK for the prediction of the three dimensional structure of a covalently bound ligand onto a receptor.

* [**HADDOCK2.4 MS cross-links tutorial**](/education/biomolecular-simulations-2019/HADDOCK24-Xlinks):
  This tutorial demonstrates the use of cross-linking data from mass spectrometry to guide the docking in HADDOCK. This tutorial builds on our DisVis tutorial and illustrates various scenarios of using cross-linking data in HADDOCK.
