---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
title: HADDOCK2.4 manual - Using cryoEM restraints
image:
  feature: pages/banner_software.jpg
---

* table of contents
{:toc}


* * *

### Introduction

When using cryo-EM data, however, HADDOCK needs to first convert the information provided by the EM map into distance restraints in order to drive the molecules to their potential location. This can be done by extracting centroids from the EM map. The centroids are provided as 3D coordinates to HADDOCK, and are automatically converted to unambiguous (or ambiguous in cases where circular symmetry is present or the identity between subunits is uncertain) distance restraints between the centroids and the center of mass of the subunits. These restraints draw, during the initial rigid-body step of HADDOCK, the molecules toward their location within the EM map. Once the rigid complex is formed and oriented correctly in the density, the cryo-EM density-based restraint energy term in HADDOCK is applied, and the refinement protocol proceeds through the various steps of HADDOCK.

* * *

### Extracting centroids information

HADDOCK relies on the concept of centroids to guide the initial docking and only uses the cryo-EM map once the molecules have been docked using the centroid restraints. The centroids define the most likely position of the center of mass of a molecule into the density. Their positions (x,y,z coordinates) must be defined [run.cns](/software/haddock2.4/run){:target="_blank"}. Those positions can be for example obtained using our [PowerFit webserver](https://mhaddock.science.uu.nlservices/POWERFIT){:target="_blank"}.

PowerFit fits atomic structures into density maps by performing a full-exhaustive 6-dimensional cross-correlation search between the atomic structure and the density. It takes as input an atomic structure in PDB- or mmCIF-format and a cryo-EM density with its resolution, and outputs positions and rotations of the atomic structure corresponding to high correlation values and the top 10 best scoring rigid poses. PowerFit uses the local cross-correlation function as its base score. The score is by default enhanced with an optional Laplace pre-filter, and a core-weighted version that minimizes the effect overlapping densities from neighboring subunits.
From the fitted structure one can extract the 3D coordinates of the centroids (their center of mass position into the map), an information required by HADDOCK-EM. This information is provided as one of PowerFit's output.

* * *

### Cryo-EM density map cropping

In order to reduce data noise and save computational time, we strongly advise to crop the cryo-EM map to the region of interest. Cropping can be straightforwardly performed using  UCSF Chimera. A step-by-step protocol to extract a subregion of a density map is available at [https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/midas/mask.html](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/midas/mask.html){:target="_blank"}). 

* * *

### Formatting the cryo-EM map for HADDOCK use

For use as restraint in HADDOCK2.4 the cryo-EM maps in MRC or CCP4 format must first be converted to XPLOR format, the latter being the only one read by CNS, the computational engine used by HADDOCK. We are providing for that a python script in the HADDOCK ***EMtools*** directory called: *em2xplor.py*. It allows to transform a cryo-EM density from CCP4 or MRC format to XPLOR/CNS format. In the process it might also extend the number of voxels in each direction to be a multiple of 2, 3 and 5, to be consistent with the fast Fourier transform in CNS.


<pre style="background-color:#DAE4E7">
> python2.7 $HADDOCK/EMtools/em2xplor.py -h
usage: em2xplor.py [-h] [-f {ccp4,map,mrc,xplor,cns}] infile outfile

Convert a cryo-EM density to the CNS/XPLOR-format, while expanding the number
of voxels in each direction to be a multiple of 2, 3 and 5

positional arguments:
  infile                Cryo-EM file to be converted.
  outfile               Name of output XPLOR-file

optional arguments:
  -h, --help            show this help message and exit
  -f {ccp4,map,mrc,xplor,cns}, --format {ccp4,map,mrc,xplor,cns}
                        Format of the input file.
</pre>

* * *

### Defining the EM restraints for HADDOCK

In order to make use of cryo-EM restraints in HADDOCK the map must be defined in the `run.param` file. Here is such an example taken from the `protein-protein-em` example provided with HADDOCK2.4:


<pre style="background-color:#DAE4E7">
HADDOCK_DIR=../../
N_COMP=2
PDB_FILE1=2ykr_F.pdb
PDB_FILE2=2ykr_R.pdb
PROJECT_DIR=./
PROT_SEGID_1=A
PROT_SEGID_2=B
RUN_NUMBER=1
CRYO-EM_FILE=1884_part.xplor
</pre>

The centroids positions have to be defined in [`run.cns`](/software/haddock2.4/run/#cryo-em-restraints){:target="_blank"}.

* * *

### EM scoring

The EM protocol introduces a new term to the HADDOCK score, namely the local cross-correlation value (LCC) computed for a given model which is added to the equation defining the score, with an optimal weight for the three stages:

<pre>
* HADDOCKscore-it0-EM   = 0.01 Evdw + 1.0 Eelec + 1.0 Edesol + 0.01 Eair - 0.01 BSA -   400*LCC 
* HADDOCKscore-it1-EM   =  1.0 Evdw + 1.0 Eelec + 1.0 Edesol +  0.1 Eair - 0.01 BSA - 10000*LCC
* HADDOCKscore-water-EM =  1.0 Evdw + 0.2 Eelec + 1.0 Edesol +  0.1 Eair - 10000*LCC
</pre>

For the meaning of the other terms refer to the [scoring](/software/haddock2.4/scoring){:target="_blank"} section.

* * *

### Additional reading

A detailed protocol to use cryo-EM restraint with the HADDOCK2.4 web portal is described in:

* M.E. Trellet, G. van Zundert and A.M.J.J. Bonvin. [Protein-protein modelling using cryo-EM restraints](https://dx.doi.org/10.1007/978-1-0716-0270-6_11){:target="_blank"}. In:  _Structural Bioinformatics. Methods in Molecular Biology_, vol 2112. Humana, New York, NY, (2020). A preprint is available [here](http://arxiv.org/abs/2005.00435){:target="_blank"}.

The implementation and use of cryo-EM restraints in HADDOCK is described in:

* G.C.P. van Zundert, A.S.J. Melquiond and A.M.J.J. Bonvin.
[Integrative modeling of biomolecular complexes: HADDOCKing with Cryo-EM data.](https://doi.org/10.1016/j.str.2015.03.014){:target="_blank"}
_Structure._ *23*, 949-960 (2015).

