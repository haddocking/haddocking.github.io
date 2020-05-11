---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
title: HADDOCK2.4 manual - Coarse graining PDB files
image:
  feature: pages/banner_software.jpg
---

### Introduction

In order to use the [Martini](http://cgmartini.nl){:target="_blank"} coarse graining option of HADDOCK2.4 you first have to convert your atomistic PDB structures into coarse grained versions and also generate the distance restraint files that will allow HADDOCK to convert back the models to atomistic ones in the final refinement stage.

For this purpose a script is provided in the HADDOCK ***CGtools*** directory, called *aa2cg-prot_xna.py*.

Details of the implementation in HADDOCK can be found in the following publications:

* R.V. Honorato, J. Roel-Touris and A.M.J.J. Bonvin. [MARTINI-based protein-DNA coarse-grained HADDOCKing](https://doi.org/10.3389/fmolb.2019.00102){:target="_blank"}. _Frontiers in Molecular Biosciences_, *6*, 102 (2019).

* J. Roel-Touris, C.G. Don, R.V. Honorato, J.P.G.L.M Rodrigues and A.M.J.J. Bonvin. [Less is more: Coarse-grained integrative modeling of large biomolecular assemblies with HADDOCK](https://doi.org/10.1021/acs.jctc.9b00310){:target="_blank"}. _J. Chem. Theo. and Comp._, *15*, 6358-6367 (2019).


* * *

### Software requirements

The following software are required in order to be able to run this script (see [Installation](/software/haddock2.4/installation){:target="_blank"} and [Software](/software/haddock2.4/software){:target="_blank"}):

* Python 2.7.x
* BioPython 1.72
* DSSP (dssp should be in your path)

The DSSP software is required to define the secondary structure, which is encoded in the B-factor field of the CG model. This information is used by HADDOCK to select the proper secondary structure-dependent Martini parameters for the backbone.

Before converting your PDB files, make sure that they contain the chainID information you are going to use for the docking. This is important in order to generate correct distance restraints for the back-mapping. You can easily add or modify a chainID using our [pdb-tools](/software/haddock2.4/installation/#pdb-tools){:target="_blank"}, or instead using our new [PDB-tools webserver](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.

* * *

### Usage

As an illustration of converting PDB files to a Martini coarse grained representation we will use here the `protein-tetramer-CG` example distributed with HADDOCK.

<pre style="background-color:#DAE4E7">
python2.7 $HADDOCK/CGtools/aa2cg-prot_xna.py chainA.pdb
python2.7 $HADDOCK/CGtools/aa2cg-prot_xna.py chainB.pdb
python2.7 $HADDOCK/CGtools/aa2cg-prot_xna.py chainC.pdb
python2.7 $HADDOCK/CGtools/aa2cg-prot_xna.py chainD.pdb
</pre>

This will generate for each model two new files:

* *chainX_cg.pdb* - contains the Martini-converted coarse grained model

<pre style="background-color:#DAE4E7">
ATOM      1  BB  GLN A  32      -2.754 -10.531   1.060  1.00  1.00
ATOM      2  SC1 GLN A  32       0.211  -9.054  -0.038  1.00  1.00           S
ATOM      3 SCD2 GLN A  32      -0.011  -8.931   0.081  1.00  1.00
ATOM      4 SCD1 GLN A  32       0.322  -9.115  -0.098  1.00  1.00
ATOM      5  BB  ALA A  33      -0.615 -13.325   1.328  1.00  4.00
ATOM      6  BB  PHE A  34       1.213 -11.866   3.789  1.00  4.00
ATOM      7  SC1 PHE A  34       3.198 -10.002   3.616  1.00  4.00           S
ATOM      8  SC2 PHE A  34       4.956 -10.867   4.822  1.00  4.00           S
ATOM      9  SC3 PHE A  34       4.674  -8.993   5.655  1.00  4.00           S
...
</pre>

* *chainX_cg-to-aa.tbl* - a distance restraints file for the conversion from CG to AA at the final refinement stage

<pre style="background-color:#DAE4E7">
assign (segid ACG and resid 32 and name BB) (segid A and resid 32 and (name CA or name C or name N or name O)) 0 0 0
assign (segid ACG and resid 32 and name SC1) (segid A and resid 32 and (name CB or name CG or name CD or name OE1 or name NE2)) 0 0 0
assign (segid ACG and resid 33 and name BB) (segid A and resid 33 and (name CA or name C or name N or name O or name CB)) 0 0 0
assign (segid ACG and resid 34 and name BB) (segid A and resid 34 and (name CA or name C or name N or name O)) 0 0 0
assign (segid ACG and resid 34 and name SC1) (segid A and resid 34 and (name CB or name CG or name CD1)) 0 0 0
assign (segid ACG and resid 34 and name SC2) (segid A and resid 34 and (name CD2 or name CE2)) 0 0 0
assign (segid ACG and resid 34 and name SC3) (segid A and resid 34 and (name CE1 or name CZ)) 0 0 0
...
</pre>

The `cg_to_aa` distance restraints files of the various molecules must be combined into one for the docking, e.g.:

<pre style="background-color:#DAE4E7">
cat chainA_cg_to_aa.tbl chainB_cg_to_aa.tbl chainC_cg_to_aa.tbl chainD_cg_to_aa.tbl > cg-to-aa.tbl
</pre>

To make use of the coarse graining option, both the atomistic and CG models must be defined in `run.param`, together with the `cg_to_aa.tbl` restraints file, e.g.:

<pre style="background-color:#DAE4E7">
CGTOAA_TBL=./cg-to-aa.tbl
N_COMP=4
PDB_FILE1=./chainA.pdb
PDB_FILE2=./chainB.pdb
PDB_FILE3=./chainC.pdb
PDB_FILE4=./chainD.pdb
CGPDB_FILE1=./chainA_cg.pdb
CGPDB_FILE2=./chainB_cg.pdb
CGPDB_FILE3=./chainC_cg.pdb
CGPDB_FILE4=./chainD_cg.pdb
PROJECT_DIR=./
PROT_SEGID_1=A
PROT_SEGID_2=B
PROT_SEGID_3=C
PROT_SEGID_4=D
RUN_NUMBER=1
HADDOCK_DIR=/home/software/haddock2.4
</pre>


**Note** that the script can also handle DNA and RNA (the latter experimental). In that case the `--skipss` option should be given to skip DSSP.





