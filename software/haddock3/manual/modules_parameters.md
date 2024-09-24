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

# Modules in haddock3

Haddock3 has this particularity (compared to the pervious HADDOCK2.X versions), that there is not a single static workflow to be processed, but rather a custom one requiring the user to design its own workflows by placing `[modules]` one after the other, enabling to generate a sequence of events to solve their research question.

<figure align="center">
<img src="/software/haddock3/manual/images/hd3_custom_workflow.png">
</figure>

Various `[modules]` are available in Haddock3, and they are grouped together by types:
- [**Topology modules**](#topology-modules): these modules focus in the building of missing atoms and generation of approriate topology files enabling downstream use of molecular dynamics protocols.
- [**Sampling modules**](#sampling-modules): dedicated at performing sampling of initial conformations, such as rigidbody docking.
- [**Refinement modules**](#refinement-modules): these modules aim at refining interaction interface, using simulated annealing protocol, energy minimisation or molecular dynamics with an explicit solvent shell.
- [**Scoring modules**](#scoring-modules): these modules are evaluating provided complexes with dedicated scoring functions, such as the HADDOCK score.
- [**Analysis modules**](#analysis-modules): these modules focus on the analysis of docking models. It ranges from the clustering of docking models, to the selection of best ranked ones passing by the evaluation of the models with respect to a reference structure using CAPRI criteria.


<figure align="center">
<img src="/software/haddock3/manual/images/list_modules.png">
</figure>


## Defining module parameters




## Set of available modules

Below is presented the list of available modules.
For detailed explannation of each modules and their respective parameters, please refere to [the online documentation]().


### Topology modules


### Sampling modules


### Refinement modules


### Scoring modules


### Analysis modules




## Developping a new module

Haddock3 is a collaborative project, and researchers can contribute to it, increasing the scope and potential of the Haddock3 suite.
Information on how to contribute and setup a proper development environment are available on the GitHub repository:
- [**CONTRIBUTING.md**](https://github.com/haddocking/haddock3/blob/main/CONTRIBUTING.md), contains information on how to contribute.
- [**DEVELOPMENT.md**](https://github.com/haddocking/haddock3/blob/main/DEVELOPMENT.md), contains information on how to set up an adequate development environment.

