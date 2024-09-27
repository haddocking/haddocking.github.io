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

To tune modules parameters, you first need to define which module you will be using, then add the list of parameters and their new values.

Note that if a parameter is not defined, its default value will be used instead.

### Tuning a module parameter

In the configuration file, right after declaring which module you want to use, add the parameters and their new values in the subsequent lines.

Here is a synthetic example:
```TOML
[module]
parameter1 = new_value_1
parameter3 = new_value_3
```

### Definition of defaults parameter values

Each module is having its own default parameters values set in a file name `defaults.yaml`.
This file is not only used to check if the parameter name exists at execution time, but also as reference to know if the configuration file provided by the use respects the allowed value for a given parameter.

If the parameter range is not suited for your research, you can always tune the defaults values or the maximum values that can be adopted by this parameter (at your own risk).


## Set of available modules

Below is presented the list of available modules.
For detailed explannation of each modules and their respective parameters, please refere to [the online documentation]().
You can also use the `haddock3-cfg` command line to get information of each module and their parameters.


### Topology modules

- `[topoaa]`(/software/haddock3/manual/modules/topology.md#topoaa):
- `[topocg]`(/software/haddock3/manual/modules/topology.md#topocg): *comming soon*

### Sampling modules

- `[rigidbody]`(/software/haddock3/manual/modules/sampling.md#rigidbody):
- `[gdock]`(/software/haddock3/manual/modules/sampling.md#gdock):
- `[lightdock]`(/software/haddock3/manual/modules/sampling.md#lightdock):

### Refinement modules

- `[flexref]`(/software/haddock3/manual/modules/refinements.md#flexref):
- `[emref]`(/software/haddock3/manual/modules/refinements.md#emref):
- `[mdref]`(/software/haddock3/manual/modules/refinements.md#mdref):


### Scoring modules

- CNS scoring modules:
  - `[emscoring]`(/software/haddock3/manual/modules/scoring.md#emscoring):
  - `[mdscoring]`(/software/haddock3/manual/modules/scoring.md#mdscoring):


### Analysis modules

- Analysis:
  - `[caprieval]`(/software/haddock3/manual/modules/analysis.md#caprieval):
  - `[alascan]`(/software/haddock3/manual/modules/analysis.md#alascan):
  - `[contactmap]`(/software/haddock3/manual/modules/analysis.md#contactmap):
- Clustering:
  - `[clustfcc]`(/software/haddock3/manual/modules/analysis.md#clustfcc):
  - `[rmsdmatrix]`(/software/haddock3/manual/modules/analysis.md#rmsdmatrix):
  - `[clustrmsd]`(/software/haddock3/manual/modules/analysis.md#clustrmsd):
- Selection:
  - `[seletop]`(/software/haddock3/manual/modules/analysis.md#seletop):
  - `[seletopclusts]`(/software/haddock3/manual/modules/analysis.md#seletopclusts):


## Developping a new module

Haddock3 is a collaborative project, and researchers can contribute to it, increasing the scope and potential of the Haddock3 suite.
Information on how to contribute and setup a proper development environment are available on the GitHub repository:
- [**CONTRIBUTING.md**](https://github.com/haddocking/haddock3/blob/main/CONTRIBUTING.md), contains information on how to contribute.
- [**DEVELOPMENT.md**](https://github.com/haddocking/haddock3/blob/main/DEVELOPMENT.md), contains information on how to set up an adequate development environment.

