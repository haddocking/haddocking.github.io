---
layout: page
title: "BioExcel Summer School on Biomolecular Simulations 2020"
tags: [HADDOCK, docking, covalent docking, CPMD, metadynamics, molecular simulations, tutorials, BioExcel, summer school]
image:
  feature: pages/banner_education-thin.jpg
---
<figure align="center">
<a href="http://www.bioexcel.eu"><img src="/images/Bioexcel_logo.png"></a>
</figure>

On this page, you can find the links to the [**HADDOCK**](/education/HADDOCK24/HADDOCK24-antibody-antigen) and [**metadynamics**](/education/biomolecular-simulations-2019/Metadynamics_tutorial) (using Gromacs) tutorials given during the [2020 BioExcel Online Summerschool on Biomolecular Simulations](https://bioexcel.eu/events/bioexcel-summer-school-on-biomolecular-simulations-2020/). 

The first tutorial demonstrates how to model antibody-antigen complexes using various information in HADDOCK. It is based on the approach described in the following publications:

* F. Ambrosetti, Zuzana Jandova and A.M.J.J. Bonvin. [A protocol for information-driven antibody-antigen modelling with the HADDOCK2.4 webserver](http://arxiv.org/abs/2005.03283). _ArXiv_, 2005.03283 (2020).

* F. Ambrosetti, B. Jiménez-García, J. Roel-Touris and A.M.J.J. Bonvin. [Modeling Antibody-Antigen Complexes by Information-Driven Docking](https://doi.org/10.1016/j.str.2019.10.011). _Structure_, *28*, 119-129 (2020). Preprint freely available from [here](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3362436).


The second tutorial illustrates how metadynamics can be used to sample conformations of a binding pocket; those are subsequently used for docking a ligand using HADDOCK. The conformational sampling approach is following the EDES approach described in the following publication:

* A. Basciu,  G. Malloci,  F. Pietrucci,  A.M.J.J. Bonvin and A.V. Vargiu.
[Holo-like and druggable protein conformations from enhanced-sampling of binding pocket shape](http://dx.doi.org/10.1021/acs.jcim.8b00730). _J. Chem. Inf. and Mod._ *59*, 1515-1528 (2019).


## Tutorials

* [**Metadynamics**](/education/biomolecular-simulations-2020/Metadynamics_tutorial):
  This tutorial highlights the benefits of enhanced sampling using metadynamics to improve the predictive power of molecular docking for protein-small molecule targets, in the case of binding sites undergoing conformational changes. For this, we will first generate an ensemble of conformers for the target protein using [GROMACS](http://www.gromacs.org/) and [PLUMED](http://www.plumed.org/), before proceeding with the docking using [HADDOCK](http://www.bonvinlab.org/software/haddock2.2/).

  **NOTE** that there is an updated version of this tutorial [**here**](https://molmod.dsf.unica.it/edes){:target="_blank"}) which we are recommending to follow instead. 

* [**HADDOCK2.4 antibody-antigen**](/education/HADDOCK24/HADDOCK24-antibody-antigen):
  This tutorial demonstrates how to use HADDOCK for the prediction of the three dimensional structure of antibody-antigen complexes.

