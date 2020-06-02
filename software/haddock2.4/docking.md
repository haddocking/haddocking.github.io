---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
title: HADDOCK2.4 manual - Setting up a docking run
image:
  feature: pages/banner_software.jpg
---

* table of contents
{:toc}


**Note:** Refer also to our online [HADDOCK local installation tutorial](/education/HADDOCK24/HADDOCK24-local-tutorial){:target="_blank"} for detailed examples of setting up a docking run.


<hr>

## Defining the input data - run.param

In version 2.4 of HADDOCK the way the input data are defined has changed. Instead of the old `new.html` file used in HADDOCK2.2, we switched to **run.param** which is a simple ASCII text file with a list of keywords and associated files. Examples for various scenarios are provided in the `examples` directory. These can be used as starting point and adapted to your needs.

An example of such a **run.param** file taken from the protein-protein example is:

<pre style="background-color:#DAE4E7">
  AMBIG_TBL=./e2a-hpr_air.tbl
  HADDOCK_DIR=../../
  N_COMP=2
  PDB_FILE1=./e2aP_1F3G.pdb
  PDB_FILE2=./hpr/hpr_1.pdb
  PDB_LIST2=./hpr-files.list
  PROJECT_DIR=./
  PROT_SEGID_1=A
  PROT_SEGID_2=B
  RUN_NUMBER=1
</pre>

Each line contains a specific keyword and its associated value.


#### Defining the installation location of HADDOCK

When setting a new docking run, all protocols, parameter files and various scripts will be copied from the local installation of HADDOCK into a newly created run directory. For this the `HADDOCK_DIR` keyword must be defined that specifies the location of HADDOCK2.4 on disk, e.g.:

<pre style="background-color:#DAE4E7">
  HADDOCK_DIR=/home/software/haddock2.4
</pre>

The path can be absolute or relative to the current directory.


#### Defining the location of the run

The location where the docking run will be performed should be defined in the `PROJECT_DIR` keyword. 
It can be a relative or absolute path, e.g.:

<pre style="background-color:#DAE4E7">
  PROJECT_DIR=./
</pre>


#### Defining input PDBs

The current version of HADDOCK supports the docking of up to 20 different molecules.

Each molecule is defined by its own **PDB_FILEX** keyword where `X` corresponds to the molecule number. The paths to the files on disk can be absolute or relative.

For each molecule you can also associate a segment ID to be used for the docking.
These are specified in the **PROT_SEGID_X** keywords.

Further HADDOCK supports docking from an ensemble of conformations. To enable this option, an additional keyword **PDB_LISTX** must be defined pointing to a text file containing a list of PDB files to be used.

An example of the corresponding keywords (taken from the `protein-protein` example in haddock2.4) is:

<pre style="background-color:#DAE4E7">
  PDB_FILE1=./e2aP_1F3G.pdb
  PDB_FILE2=./hpr/hpr_1.pdb
  PDB_LIST2=./hpr-files.list
  PROT_SEGID_1=A
  PROT_SEGID_2=B
</pre>

And the corresponding ensemble list file would look like:

<pre style="background-color:#DAE4E7">
"./hpr/hpr_1.pdb"
"./hpr/hpr_2.pdb"
"./hpr/hpr_3.pdb"
"./hpr/hpr_4.pdb"
"./hpr/hpr_5.pdb"
"./hpr/hpr_6.pdb"
"./hpr/hpr_7.pdb"
"./hpr/hpr_8.pdb"
"./hpr/hpr_9.pdb"
"./hpr/hpr_10.pdb"
</pre>

**Note:** The path to the ensemble of structures can be relative or absolute. Importantly, those should be defined between double quotes.


#### Defining input coarse grained PDBs


Version 2.4 of HADDOCK supports the use of coarse grained models for the docking. Those are based on the [MARTINI2.2p](http://cgmartini.nl){:target="_blank"} force field with an average 4:1 ratio of all atoms to coarse grained particules.

To use coarse graining in HADDOCK you will need to define additional keywords **CGPDB_FILEX** for each input PDB.
In addition, for the final transformation from coarse grained to all atom models, you will need to define one additional restraint file that contains distance restraints between each coarse grained particle and the atoms that belong to it. This file is specified by the **CGTOAA_TBL** keyword. 

An example entry (taken from the `protein-tetramer-CG` example in haddock2.4) is:

<pre style="background-color:#DAE4E7">
PDB_FILE1=./chainA.pdb
PDB_FILE2=./chainB.pdb
PDB_FILE3=./chainC.pdb
PDB_FILE4=./chainD.pdb
CGPDB_FILE1=./chainA_cg.pdb
CGPDB_FILE2=./chainB_cg.pdb
CGPDB_FILE3=./chainC_cg.pdb
CGPDB_FILE4=./chainD_cg.pdb
</pre>

As for the atomistic models, an ensemble of coarse grained models can be defined using as keyword **CGPDB_LISTX**

#### Defining restraints

The following type of restraints with their associated keywords can be defined:


* Ambiguous distance restraints **AMBIG_TBL**: The corresponding restraint file should contain distance restraints. Those can be ambiguous and/or unambiguous. 50% will be randomly deleted by default (can be turned off)

* Unambiguous distance restraints **UNAMBIG_TBL**: The corresponding restraint file should contain distance restraints. Those can be ambiguous and/or unambiguous. Those will always be used.

* Hydrogen bond distance restraints **HBOND_FILE**: The corresponding restraint file can contain in principle any type of distance restraints. Those will however not be used in it0. Typically we use this type of restraints to specify intramolecular restraints.

* CG to AA distance restraints **CGTOAA_TBL**: This file should contain the distance restraints to transform back the CG model into an all atom model.

* Dihedral angle restraints **DIHED_FILE**: The file should contain dihedral angle restraints. Those can be used to restraint the conformation of the backbone for example.

* Diffusion anisotropy restraints **DANIX_FILE**: Up to five different restraints files can be defined (X should be a number between 1 and 5)

* Residual dipolor coupling restraints **RDCX_FILE**: Up to five different restraints files can be defined (X should be a number between 1 and 5)

* Pseudo contact shift restraints **PCSX_FILE**: Up to ten different restraints files can be defined (X should be a number between 1 and 10)

* Distance restraints to restrain the tensor for PCS restraints **TENSOR_FILE**: This file should contain distance restraints to restrain the position of the tensor for PCS restraints

* CryoEM map **CRYO-EM_FILE**: This file should contain a cryo-EM map in XPlor format.


<HR>

## Creating the run directory

Once the `run.param` file has been properly defined, simply call haddock2.4 (defined upon sourcing the `haddock_configuration` file from the installation directory by typing at the command line:

<pre style="background-color:#DAE4E7">
   haddock2.4
</pre>

Make sure that the PYTHONPATH system variable contains the path of the HADDOCK installation (see [installation](/software/haddock2.4/installation){:target="_blank"}).  

HADDOCK will create a directory **runX** (where X is the run number defined in the `run.param` file - note that this can also contain characters, e.g. `1-test`). In this directory, a **run.cns** file will be created. You will have to edit this file to start the docking (see "[Defining the docking parameters](#definingthedockingparameters)" section).  

In the runX directory some subdirectories are created containing:

*   **runX/begin**: This directory will contain the topologies and begin PDB files processed by HADDOCK to add any missing atoms.

*   **runX/begin-aa**: This directory will contain the all atoms topologies and begin PDB files processed by HADDOCK to add any missing atoms in case where coarse-grained docking is enabled

*   **runX/data**: This directory contains all your input data organised into:

	*   **runX/data/run.param**: The original `run.param` file you defined
	*  	**runXdata/cryo-em/**: Cryo-EM map
	*	**runX/data/dani/**: Diffusion anisotropy restraints
	*	**runX/data/dihedrals/**: Dihedral angle restraints
	*	**runX/data/distances/**: The ambiguous and unambiguous distance restraints
	*	**runX/data/ensemble-models/** : In case of an ensemble of starting structures, HADDOCK copies all pdb files of the two molecules to this directory.
	*	**runX/data/hbonds/**: The hydrogen bond restraints
	* 	**runX/data/pcs/**: The pseudo contact shift restraints
	*   **runX/data/rdcs/**: The residual dipolar coupling restraints
	*   **runX/data/sequence/**: HADDOCK copies the pdb files of the two molecules and the list files for ensembles in this directory.
	*	**runX/data/tensor**: The tensor restraints for the PCS tensors


*   **runX/packages/**: Only used for the grid submission mode of HADDOCK

*   **runX/protocols/**: Contains all the CNS scripts for docking and analysis

*   **runX/tools/**: Scripts used for the analysis of the solutions will be stored in this directory

*   **runX/toppar/**: This directory contains all the topology and parameters files


<hr>


## Defining the docking parameters

Having created the run directory for your docking run, you should now edit the **run.cns** file and check/modify a number of parameters to your specific needs, such as:
*   The number of structures to generate and refine
*   Histidine protonation state (default is an automatic mode)
*   Flexible segments (default is an automatic mode)
*   Which kind of restraints to use and associated parameters
*   Type of molecule to dock (e.g. DNA)
*	Fixing of a molecule in its original position
*	Number of models to calculate simultaneously and queue submission command (depends on the way you will run HADDOCK, e.g. on local resources or using a batch system).
*   Scoring parameters 
*   Clustering method and cutoff
*   Post-analysis options
*   ...

Many of those have default values which you do not need to change.  

For a description of the various parameters in **run.cns**, refer to the [run.cns file](/software/haddock2.4/run){:target="_blank"} section.  

**Note:** If you have turned on the use of DNA/RNA restraints in **run.cns** HADDOCK expects to find a file called **dna-rna_restraints.def** in the **data/sequence** directory. This files allows you to define standard A-, B- or custom restraints for DNA such as base-pairing, puckering and backbone dihedral angles. You can edit a template file that can be found in the **protocols** directory and save it as **dna-rna_restraint.def** into the **data/sequence** directory. 

<hr>


## Launching the docking

When all necessary files and parameters have been properly edited and saved then start HADDOCK in the run directory by typing:

<pre style="background-color:#DAE4E7" >
    haddock2.4
</pre>

You can also redirect the output of HADDOCK to a file and send the process in background by typing instead:

<pre style="background-color:#DAE4E7" >
    haddock2.4 >&haddock2.4.out &
</pre>

The entire protocol consists of five stages:

1.  Topologies and structures generation
2.  Randomization of the starting orientation and rigid body energy minimization
3.  Semi-flexible simulated annealing
4.  Final refinement (optionally in explicit solvent (water or DMSO))
5.  Post-processing / analysis  

For details refer to the [Docking protocol](/software/haddock2.4/protocol){:target="_blank"} section of the online manual.

<hr>


## Monitoring your docking run

As the docking proceeds HADDOCK will output information about the status of the run, telling you which models are currently being calculated. The process can get however stuck if some stages are failing. There are mechanisms built in to detect failures but we can not guarantee to catch all problems. 

Note that errors can sometimes be caused by missing quotes or punctuations in the edited `run.cns` file.

A few typical problems are:


* **Failure to submit to your batch system**: If you are using a queueing/batch system, make sure that the queue command defined in `run.cns` by the `queue_1=` parameter is correct.

* **Failure to generate the topologies**: It can be that the generation of the starting PDBs and associated topologies is failing. This is for example the case when hetero atoms are defined in the starting PDBs (as HETATM) for which no topologies and parameters are provided (refer to our [FAQ section](/software/haddock2.4/faq.md){:target="_blank"} when docking small ligands). There could also be missing parameters for a particular molecule.

Always check in such a case the content of the generated `.out` files in the `begin` directory. Start looking at the bottom of the file for error messages.

* **Failure in the rigid body docking stage (it0)**: A possible reason for failure at this stage is a wrong definition of the restraints. Check for error messages the output files created in the run directory with a name matching `*it0_refine_X.out.gz` where `X` is the model number. Search for error messages starting from the bottom of the file. Error are often reported by CNS with an `ERR` string.

* **Failure in the semi flexible refinement stage (it1)**: While bad restraints can be the potential cause of failures, often the quality of the starting models can also be the problem. While in the ridig body docking the intramolecular interactions are not calculated (the molecules are treated as rigid bodies), these are calculated in it1. Bad internal geometries, with clashes between atoms, can cause the system to 'explode'. Check again for error messages the output files created in the run directory with a name matching `*it1_refine_X.out.gz` . Search for error messages starting from the bottom of the file. Error are often reported by CNS with an `ERR` string. Possible solutions for this problem are to reduce the temperature for the simulated annealing, or remove the high temperature parts by setting the corresponding number of steps to 0 (refer for this to the [run.cns file](/software/haddock2.4/run){:target="_blank"} section).


<hr>
