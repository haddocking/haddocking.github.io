---
layout: page
title: ""
excerpt: ""
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, manual, usage]
image:
  feature: pages/banner_software.jpg
---

# emscoring module

EM scoring module.

This module performs energy minimization and scoring of the models generated in
the previous step of the workflow. No restraints are applied during this step.

The default HADDOCK scoring function in the ``[emscoring]`` module is therefore the following:

![equ](https://latex.codecogs.com/gif.latex?HS=1.0E_{vdw}&plus;0.2E_{elec}&plus;0.0E_{air}&plus;1.0E_{desolv})

For a detailed explanation of the components of the scoring function, please have a look [here](../haddocking.md#haddock-scoring-function).

#### Notable parameters

The most important parameters for the ``[emscoring]`` module are:

- `nemsteps`: number of energy minimization steps
- `per_interface_scoring` : output per interface scores in the PDB header (default: False)


More information about ``[emscoring]`` parameters can be accessed [here](https://bonvinlab.org/haddock3/modules/scoring/haddock.modules.scoring.emscoring.html#default-parameters) or retrieved by running
```bash
haddock3-cfg -m emscoring
```
<hr>

# mdscoring module

MD scoring module.

This module will perform a short MD simulation on the input models and
score them. No restraints are applied during this step.

The same scoring function as in the ``[emscoring]`` module is used:

![equ](https://latex.codecogs.com/gif.latex?HS=1.0E_{vdw}&plus;0.2E_{elec}&plus;0.0E_{air}&plus;1.0E_{desolv})

#### Notable parameters

The most important parameters for the ``[mdscoring]`` module are:

- `nemsteps`: number of energy minimization steps
- `per_interface_scoring` : output per interface scores in the PDB header (default: False)
- `waterheatsteps`: number of MD steps for heating up the system
- `watersteps`: number of MD steps at 300K
- `watercoolsteps` : number of MD steps for cooling down the system

More information about ``[mdscoring]`` parameters can be accessed [here](https://bonvinlab.org/haddock3/modules/scoring/haddock.modules.scoring.mdscoring.html#default-parameters) or retrieved by running
```bash
haddock3-cfg -m mdscoring
```


