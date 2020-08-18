---
layout: page
title: "Settings for running with bioinformatic predictions"
tags: [Jekyll, HADDOCK, Tips, Tricks, prediction, bioinformatics, Advanced, Docking, Simulation, Computational Biology, Modelling, Protein Structure]
modified: 2017-02-24T14:44:07.573882-04:00
comments: false4
image:
  feature: pages/banner_software.jpg
---

The previous version of the HADDOCK server (2.2) had a dedicated interface with custom settings for use with bioinformatics predictions. In HADDOCK2.4 [submission interface](https://wenmr.science.uu.nl/haddock2.4/submit/1){:target="_blank"} this is presented as an option in Step 2 (needs Expert access level). When selecting this option the following changes will automatically be applied:

In the **"Distance Restraints"** section:

* _Number of partitions for random exclusion_ → **1.1428**

In the **"Sampling parameters"** section:

* _Number of structures for rigid body docking_ → **10000**
* _Number of trials for rigid body minimisation_ → **1**
* _Number of structures for semi-flexible refinement_ → **400**
* _Number of structures for the final refinement_ → **400**
* _Number of structures to analyze_ -> **400**

