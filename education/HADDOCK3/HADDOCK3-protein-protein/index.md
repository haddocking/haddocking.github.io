---
layout: page
title: "Protein-Protein modelling tutorial using a local version of HADDOCK3"
excerpt: "A tutorial describing the use of HADDOCK3 to model a Protein-Protein complex"
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>
<hr>

## Introduction

This tutorial demonstrates the use of the new modular HADDOCK3 version for predicting the structure of a protein-protein complex from NMR chemical shift perturbation (CSP) data. 
Namely, we will dock two E. coli proteins involved in glucose transport: the glucose-specific enzyme IIA (E2A) and the histidine-containing phosphocarrier protein (HPr). 
The structures in the free form have been determined using X-ray crystallography (E2A) (PDB ID [1F3G](https://www.ebi.ac.uk/pdbe/entry/pdb/1f3g){:target="_blank"}) 
and NMR spectroscopy (HPr) (PDB ID [1HDN](https://www.ebi.ac.uk/pdbe/entry/pdb/1hdn){:target="_blank"}). 
The structure of the native complex has also been determined with NMR (PDB ID [1GGR](https://www.ebi.ac.uk/pdbe/entry/pdb/1ggr){:target="_blank"}). 
These NMR experiments have also provided us with an array of data on the interaction itself 
(chemical shift perturbations, intermolecular NOEs, residual dipolar couplings, and simulated diffusion anisotropy data), which will be useful for the docking. 
For this tutorial, we will only make use of inteface residues identified from NMR chemical shift perturbation data as described 
in [Wang *et al*, EMBO J (2000)](https://onlinelibrary.wiley.com/doi/10.1093/emboj/19.21.5635/abstract){:target="_blank"}.

Throughout the tutorial, colored text will be used to refer to questions or instructions, and/or PyMOL commands.

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

<hr>
<hr>


## HADDOCK general concepts

HADDOCK (see [https://www.bonvinlab.org/software/haddock2.4](https://www.bonvinlab.org/software/haddock2.4){:target="_blank"})
is a collection of python scripts derived from ARIA ([https://aria.pasteur.fr](https://aria.pasteur.fr){:target="_blank"})
that harness the power of CNS (Crystallography and NMR System – [https://cns-online.org](https://cns-online.org){:target="_blank"})
for structure calculation of molecular complexes. What distinguishes HADDOCK from other docking software is its ability,
inherited from CNS, to incorporate experimental data as restraints and use these to guide the docking process alongside
traditional energetics and shape complementarity. Moreover, the intimate coupling with CNS endows HADDOCK with the
ability to actually produce models of sufficient quality to be archived in the Protein Data Bank.

A central aspect of HADDOCK is the definition of Ambiguous Interaction Restraints or AIRs. These allow the
translation of raw data such as NMR chemical shift perturbation or mutagenesis experiments into distance
restraints that are incorporated into the energy function used in the calculations. AIRs are defined through
a list of residues that fall under two categories: active and passive. Generally, active residues are those
of central importance for the interaction, such as residues whose knockouts abolish the interaction or those
where the chemical shift perturbation is higher. Throughout the simulation, these active residues are
restrained to be part of the interface, if possible, otherwise incurring a scoring penalty. Passive residues
are those that contribute to the interaction but are deemed of less importance. If such a residue does
not belong in the interface there is no scoring penalty. Hence, a careful selection of which residues are
active and which are passive is critical for the success of the docking.


<hr>
<hr>

## A brief introduction to HADDOCK3

HADDOCK3 is the next generation integrative modelling software in the
long-lasting HADDOCK project. It represents a complete rethinking and rewriting
of the HADDOCK2.X series, implementing a new way to interact with HADDOCK and
offering new features to users who can now define custom workflows.

In the previous HADDOCK2.x versions, users had access to a highly
parameterisable yet rigid simulation pipeline composed of three steps:
`rigid-body docking (it0)`, `semi-flexible refinement (it1)`, and `final refinement (itw)`.

<figure style="text-align: center;">
<img width="75%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/HADDOCK2-stages.png">
</figure>

In HADDOCK3, users have the freedom to configure docking workflows into
functional pipelines by combining the different HADDOCK3 modules, thus
adapting the workflows to their projects. HADDOCK3 has therefore developed to
truthfully work like a puzzle of many pieces (simulation modules) that users can
combine freely. To this end, the “old” HADDOCK machinery has been modularized,
and several new modules added, including third-party software additions. As a
result, the modularization achieved in HADDOCK3 allows users to duplicate steps
within one workflow (e.g., to repeat twice the `it1` stage of the HADDOCK2.x
rigid workflow).

Note that, for simplification purposes, at this time, not all functionalities of
HADDOCK2.x have been ported to HADDOCK3, which does not (yet) support NMR RDC,
PCS and diffusion anisotropy restraints, cryo-EM restraints and coarse-graining.
Any type of information that can be converted into ambiguous interaction
restraints can, however, be used in HADDOCK3, which also supports the
*ab initio* docking modes of HADDOCK.

<figure style="text-align: center;">
<img width="75%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/HADDOCK3-workflow-scheme.png">
</figure>

To keep HADDOCK3 modules organized, we catalogued them into several
categories. However, there are no constraints on piping modules of different
categories.

The main module categories are "topology", "sampling", "refinement",
"scoring", and "analysis". There is no limit to how many modules can belong to a
category. Modules are added as developed, and new categories will be created
if/when needed. You can access the HADDOCK3 documentation page for the list of
all categories and modules. Below is a summary of the available modules:

* **Topology modules**
    * `topoaa`: *generates the all-atom topologies for the CNS engine.*
* **Sampling modules**
    * `rigidbody`: *Rigid body energy minimization with CNS (`it0` in haddock2.x).*
    * `lightdock`: *Third-party glow-worm swam optimization docking software.*
* **Model refinement modules**
    * `flexref`: *Semi-flexible refinement using a simulated annealing protocol through molecular dynamics simulations in torsion angle space (`it1` in haddock2.x).*
    * `emref`: *Refinement by energy minimisation (`itw` EM only in haddock2.4).*
    * `mdref`: *Refinement by a short molecular dynamics simulation in explicit solvent (`itw` in haddock2.X).*
* **Scoring modules**
    * `emscoring`: *scoring of a complex performing a short EM (builds the topology and all missing atoms).*
    * `mdscoring`: *scoring of a complex performing a short MD in explicit solvent + EM (builds the topology and all missing atoms).*
* **Analysis modules**
    * `alascan`: *Performs a systematic (or user-define) alanine scanning mutagenesis of interface residues.*
    * `caprieval`: *Calculates CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ) with respect to the top-scoring model or reference structure if provided.*
    * `clustfcc`: *Clusters models based on the fraction of common contacts (FCC)*
    * `clustrmsd`: *Clusters models based on pairwise RMSD matrix calculated with the `rmsdmatrix` module.*
    * `contactmap`: *Generate contact matrices of both intra- and intermolecular contacts and a chordchart of intermolecular contacts.*
    * `rmsdmatrix`: *Calculates the pairwise RMSD matrix between all the models generated in the previous step.*
    * `ilrmsdmatrix`: *Calculates the pairwise interface-ligand-RMSD (il-RMSD) matrix between all the models generated in the previous step.*
    * `seletop`: *Selects the top N models from the previous step.*
    * `seletopclusts`: *Selects the top N clusters from the previous step.*

The HADDOCK3 workflows are defined in simple configuration text files, similar to the TOML format but with extra features.
Contrary to HADDOCK2.X which follows a rigid (yet highly parameterisable)
procedure, in HADDOCK3, you can create your own simulation workflows by
combining a multitude of independent modules that perform specialized tasks.


<hr>
<hr>

## Software and data setup

In order to follow this tutorial you will need to work on a Linux or MacOSX
system. We will also make use of [**PyMOL**](https://www.pymol.org/){:target="_blank"} (freely available for
most operating systems) in order to visualize the input and output data. We will
provide you links to download the various required software and data.

Further, we are providing pre-processed PDB files for docking and analysis (but the
preprocessing of those files will also be explained in this tutorial). The files have been processed
to facilitate their use in HADDOCK and to allow comparison with the known reference
structure of the complex. 

If you are running this tutorial on your own resources _download and unzip the following_
[zip archive](https://surfdrive.surf.nl/files/index.php/s/R7VHGQM9nx8QuQn){:target="_blank"}
_and note the location of the extracted PDB files in your system_. 

__If running as part of a BioExcel workshop or summerschool see the instructions in the next section.__

_Note_ that you can also download and unzip this archive directly from the Linux command line:

<a class="prompt prompt-cmd">
wget https://surfdrive.surf.nl/files/index.php/s/2RmROYLP4HcNZ1V/download -O HADDOCK3-protein-protein.zip<br>
unzip HADDOCK3-protein-protein.zip
</a>


Unziping the file will create the `HADDOCK3-protein-protein` directory which should contain the following directories and files:

* `pdbs`: a directory containing the pre-processed PDB files
* `restraints`: a directory containing the interface information and the corresponding restraint files for HADDOCK3
* `runs`: a directory containing pre-calculated results
* `scripts`: a directory containing various scripts used in this tutorial
* `workflows`: a directory containing configuration file examples for HADDOCK3

In case of a workshop of course, HADDOCK3 will usually have been installed on the system you will be using.

It this is not the case, you will have to install it yourself. To obtain and install HADDOCK3, navigate to [its repository][haddock-repo], fill the
registration form, and then follow the instructions under the **Local setup (on your own)** section below.


<hr>

### Local setup (on your own)

If you are installing HADDOCK3 on your own system, check the instructions and requirements below.


#### Installing HADDOCK3

To obtain HADDOCK3 navigate to [its repository][haddock-repo], fill the
registration form, and then follow the [installation instructions](https://www.bonvinlab.org/haddock3/INSTALL.html){:target="_blank"}.

**_Note_** that depending on the system you are installing HADDOCK3 on, you might have to recompile CNS if the provided executable is not working. See the [CNS troubleshooting section](https://github.com/haddocking/haddock3/blob/main/DEVELOPMENT.md#troubleshooting-the-cns-executable){:target="_blank"} on the HADDOCK3 GitHub repository for instructions.

#### Auxiliary software

[**PyMOL**](https://www.pymol.org/){:target="_blank"}: In this tutorial we will make use of PyMOL for visualization. If not
already installed on your system, download and install [**PyMOL**](https://www.pymol.org/){:target="_blank"}. Note that you can use your favorite visulation software but instructions are only provided here for PyMOL.


<hr>
<hr>

## Preparing PDB files for docking

In this section we will prepare the PDB files of the two proteins for docking.
Crystal and NMR structures are available from the [PDBe database](https://www.pdbe.org){:target="_blank"}. 
Throughout this step, we will use `pdb-tools` from the command line.

_**Note**_ that `pdb-tools` is also available as a [web service](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.

_**Note**_: Before starting to work on the tutorial, make sure to activate your haddock3 environment (how to do it depends on how you installed haddock3).


<hr>

### Inspecting and preparing E2A for docking

We will now inspect the E2A structure. For this start PyMOL and in the command line window of PyMOL (indicated by PyMOL>) type:

<a class="prompt prompt-pymol">
fetch 1F3G<br>
show cartoon<br>
hide lines<br>
show sticks, resn HIS<br>
</a>

You should see a backbone representation of the protein with only the histidine side-chains visible.
Try to locate the histidines in this structure.

<a class="prompt prompt-question">Is there any phosphate group present in this structure?</a>

Note that you can zoom on the histidines by typing in PyMOL:

<a class="prompt prompt-pymol">zoom resn HIS</a>

Revert to a full view with:

<a class="prompt prompt-pymol">zoom vis</a>

As a preparation step before docking, it is advised to remove any irrelevant water and other small molecules (e.g. small molecules from the crystallisation buffer), however do leave relevant co-factors if present. For E2A, the PDB file only contains water molecules. You can remove those in PyMOL by typing:

<a class="prompt prompt-pymol">remove resn HOH</a>

Now let us vizualize the residues affected by binding as identified by NMR. From [Wang *et al*, EMBO J (2000)](https://onlinelibrary.wiley.com/doi/10.1093/emboj/19.21.5635/abstract){:target="_blank"} the following residues of E2A were identified has having significant chemical shift perturbations:

<a class="prompt prompt-info">38,40,45,46,69,71,78,80,94,96,141</a>

We will now switch to a surface representation of the molecule and highlight the NMR-defined interface. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select e2a_active, (1F3G and resi 38,40,45,46,69,71,78,80,94,96,141)<br>
color red, e2a_active<br>
</a>

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/e2a-surface-airs.png">
</figure>

Inspect the surface.

<a class="prompt prompt-question">Do the identified residues form a well defined patch on the surface?</a>
<a class="prompt prompt-question">Do they form a contiguous surface?</a>

The answer to the last question should be no: We can observe residue in the center of the patch that do not seem significantly affected while still being in the middle of the defined interface. This is the reason why in HADDOCK we also define "*passive*" residues that correspond to surface neighbors of active residues. These can be selected manually, or more conveniently you can let the HADDOCK server do it for you (see [Setting up the docking run](#setting-up-the-docking-run) below).

As final step save the molecule as a new PDB file which we will call: *e2a_1F3G.pdb*<br>
For this in the PyMOL menu on top select:

<a class="prompt prompt-info">File -> Export molecule...</a>
<a class="prompt prompt-info">Click on the save button</a>
<a class="prompt prompt-info">Select as ouptut format PDB (*.pdb *.pdb.gz)</a>
<a class="prompt prompt-info">Name your file *e2a_1F3G.pdb* and note its location</a>

After saving the molecule delete it from the Pymol window or close Pymol. You can remove the molecule by typing this into the command line window of PyMOL:

<a class="prompt prompt-pymol">
delete 1F3G
</a>

In a terminal, make sure that E2A chain is A.

<a class="prompt prompt-cmd">
pdb_chain -A e2a_1F3G.pdb | pdb_chainxseg > e2a_1F3G_clean.pdb
</a>

This will be usefull in the docking phase, as HADDOCK3 needs different chain associated to each protein involved in the docking.

<hr>

### Adding a phosphate group

Since the biological function of this complex is to transfer a phosphate group from one protein to another, via histidines side-chains, it is relevant to make sure that a phosphate group be present for docking. As we have seen above none is currently present in the PDB files. HADDOCK does support a list of modified amino acids which you can find at the following link: [https://wenmr.science.uu.nl/haddock2.4/library](https://wenmr.science.uu.nl/haddock2.4/library){:target="_blank"}.

<a class="prompt prompt-question">Check the list of supported modified amino acids.</a>
<a class="prompt prompt-question">What is the proper residue name for a phospho-histidine in HADDOCK?</a>

In order to use a modified amino-acid in HADDOCK, the only thing you will need to do is to edit the PDB file and change the residue name of the amino-acid you want to modify. Don not bother deleting irrelevant atoms or adding missing ones, HADDOCK will take care of that. For E2A, the histidine that is phosphorylated has residue number 90. In order to change it to a phosphorylated histidine do the following:

<a class="prompt prompt-info">Edit the PDB file (*e2a_1F3G_clean.pdb*) in your favorite text editor</a>
<a class="prompt prompt-info">Change the name of histidine 90 to NEP </a>
<a class="prompt prompt-info">Save the file (as simple text file) under a new name, e.g. *e2aP_1F3G.pdb*</a>

Alternatively, this can also be done from the command line with the following command:

<a class="prompt prompt-cmd">
sed 's/HIS\ A\  90/NEP\ A\  90/g' e2a_1F3G_clean.pdb > e2aP_1F3G.pdb
</a>

**Note:** The same procedure can be used to introduce a mutation in an input protein structure.


<hr>

### Inspecting and preparing HPR for docking

We will now inspect the HPR structure. For this start PyMOL and in the command line window of PyMOL type:

<a class="prompt prompt-pymol">
fetch 1HDN<br>
show cartoon<br>
hide lines<br>
</a>

Since this is an NMR structure it does not contain any water molecules and we don't need to remove them.

Let's vizualize the residues affected by binding as identified by NMR. From [Wang *et al*, EMBO J (2000)](https://onlinelibrary.wiley.com/doi/10.1093/emboj/19.21.5635/abstract){:target="_blank"} the following residues were identified has having significant chemical shift perturbations:

<a class="prompt prompt-info">15,16,17,20,48,49,51,52,54,56</a>

We will now switch to a surface representation of the molecule and highlight the NMR-defined interface. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select hpr_active, (1HDN and resi 15,16,17,20,48,49,51,52,54,56)<br>
color red, hpr_active<br>
</a>

Again, inspect the surface.

<a class="prompt prompt-question">Do the identified residues form a well defined patch on the surface?</a>
<a class="prompt prompt-question">Do they form a contiguous surface?</a>

Now since this is an NMR structure, it actually consists of an ensemble of models. HADDOCK can handle such ensemble, using each conformer in turn as starting point for the docking. We however recommend to limit the number of conformers used for docking, since the number of conformer combinations of the input molecules might explode (e.g. 10 conformers each will give 100 starting combinations and if we generate 1000 ridig body models (see [HADDOCK general concepts](#haddock-general-concepts) above) each combination will only be sampled 10 times).

Now let's vizualise this NMR ensemble. In PyMOL type:

<a class="prompt prompt-pymol">
hide all<br>
show ribbon<br>
set all_states, on<br>
</a>

You should now be seing the 30 conformers present in this NMR structure. To illustrate the potential benefit of using an ensemble of conformations as starting point for docking let's look at the side-chains of the active residues:

<a class="prompt prompt-pymol">
show lines, hpr_active<br>
</a>

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/hpr-ensemble.png">
</figure>

You should be able to see the amount of conformational space sampled by those surface side-chains. You can clearly see that some residues do sample a large variety of conformations, one of which might lead to much better docking results.

**Note:** Pre-sampling of possible conformational changes can thus be beneficial for the docking, but again do limit the number of conformers used for the docking (or increase the number of sampled models, which is possible for users with expert- or guru-level access. The default access level is however only easy - for a higher level access do request it after registration).

As final step, save the molecule as a new PDB file which we will call: *hpr-ensemble.pdb*
For this in the PyMOL menu select:

<a class="prompt prompt-info">File -> Export molecule...</a>
<a class="prompt prompt-info">Select as State 0 (all states)</a>
<a class="prompt prompt-info">Click on Save...</a>
<a class="prompt prompt-info">Select as ouptut format PDB (*.pdb *.pdb.gz)</a>
<a class="prompt prompt-info">Name your file *hpr-ensemble.pdb* and note its location</a>


In a terminal, make sure that hpr chain is B.

<a class="prompt prompt-cmd">
pdb_chain -B hpr-ensemble.pdb | pdb_chainxseg > hpr-ensemble_clean.pdb
</a>

This will be usefull in the docking phase, as HADDOCK3 needs different chain associated to each protein involved in the docking.


<hr>
<hr>

## Defining restraints for docking

Before setting up the docking, we first need to generate distance restraint files in a format suitable for HADDOCK.
HADDOCK uses [CNS][link-cns]{:target="_blank"} as computational engine.
A description of the format for the various restraint types supported by HADDOCK can be found in our [Nature Protocol 2024][nat-pro]{:target="_blank"} paper, Box 1.

Distance restraints are defined as follows:

<pre style="background-color:#DAE4E7">
assign (selection1) (selection2) distance, lower-bound correction, upper-bound correction
</pre>

The lower limit for the distance is calculated as: distance minus lower-bound correction
and the upper limit as: distance plus upper-bound correction.

The syntax for the selections can combine information about:

* chainID - `segid` keyword
* residue number - `resid` keyword
* atom name - `name` keyword.

Other keywords can be used in various combinations of OR and AND statements. Please refer for that to the [online CNS manual][link-cns]{:target="_blank"}.

E.g.: a distance restraint between the CB carbons of residues 10 and 200 in chains A and B with an
allowed distance range between 10Å and 20Å would be defined as follows:

<pre style="background-color:#DAE4E7">
assign (segid A and resid 10 and name CB) (segid B and resid 200 and name CB) 20.0 10.0 0.0
</pre>

<a class="prompt prompt-question">
Can you think of a different way of defining the distance and lower and upper corrections while maintaining the same
allowed range?
</a>


<hr>

### Defining active and passive residues for E2A

As stated before, the following residues were identified has having significant chemical shift perturbations from [Wang *et al*, EMBO J (2000)](https://onlinelibrary.wiley.com/doi/10.1093/emboj/19.21.5635/abstract){:target="_blank"}:

<a class="prompt prompt-info">38,40,45,46,69,71,78,80,94,96,141</a>

Hence, we are using these residues as `active` residues for the docking run. However, we have to define `passive` residues before the run. 
These passive residues allows us to deal with potentially incomplete binding sites by defining surface neighbors as `passive` residues.
These are added to the definition of the interface but will not lead to any energetic penalty if they are not part of the
binding site in the final models, while the residues defined as `active` (typically the identified or predicted binding
site residues) will. When using the HADDOCK server, `passive` residues will be automatically defined. Here since we are
using a local version, we need to define those manually and create a file in which the active and passive residues will be listed.

This can easily be done using a haddock3 command line tool in the following way:

<a class="prompt prompt-cmd">
echo "38 40 45 46 69 71 78 80 94 96 141" > e2a.act-pass
haddock3-restraints passive_from_active e2a_1F3G.pdb 38,40,45,46,69,71,78,80,94,96,141 >> e2a.act-pass
</a>

The NMR-identified residues and their surface neighbors generated with the above command can be used to define ambiguous interactions restraints, either using the NMR identified residues as active in HADDOCK, or combining those with the surface neighbors and use this combination as passive only. Here we decided to treat the NMR-identified residues as active residues. 
Note the file consists of two lines, with the first one defining the `active` residues and
the second line the `passive` ones. We will use later these files to generate the ambiguous distance restraints for HADDOCK.

In general it is better to be too generous rather than too strict in the
definition of passive residues.

An important aspect is to filter both the active (the residues identified from
your mapping experiment) and passive residues by their solvent accessibility.
Our web service uses a default relative accessibility of 15% as cutoff. This is
not a hard limit. You might consider including even more buried residues if some
important chemical group seems solvent accessible from a visual inspection.

<hr>

### Defining active and passive residues for HPR

As stated before, the following residues were identified has having significant chemical shift perturbations from [Wang *et al*, EMBO J (2000)](https://onlinelibrary.wiley.com/doi/10.1093/emboj/19.21.5635/abstract){:target="_blank"}:

<a class="prompt prompt-info">15,16,17,20,48,49,51,52,54,56</a>

Using the same haddock3 command line tool: 

<a class="prompt prompt-cmd">
echo "15 16 17 20 48 49 51 52 54 56" > hpr.act-pass
haddock3-restraints passive_from_active hpr-ensemble.pdb 15,16,17,20,48,49,51,52,54,56 >> hpr.act-pass
</a>

<hr>

### Defining the ambiguous interaction restraints

Once you have defined your active and passive residues for both molecules, you
can proceed with the generation of the ambiguous interaction restraints (AIR) file for HADDOCK.
For this you can either make use of our online [haddock-restraints](https://rascar.science.uu.nl/haddock-restraints) web service, entering the
list of active and passive residues for each molecule, and saving the resulting
restraint list to a text file, or use our haddock3 command line tool.

To use our haddock3 command line tool you need to create for each molecule a file containing two lines:

* The first line corresponds to the list of active residues (numbers separated by spaces)
* The second line corresponds to the list of passive residues.

* For E2A (the file called `e2a.act-pass`):
<pre style="background-color:#DAE4E7">
38 40 45 46 69 71 78 80 94 96 141
35 37 39 42 43 44 47 48 64 66 68 70 72 74 81 82 83 84 86 88 97 98 99 100 105 109 110 131 132 133 142 143 144 145
</pre>

* and for HPR (the file called `hpr.act-pass`):
<pre style="background-color:#DAE4E7">
15 16 17 20 48 49 51 52 54 56
9 10 11 12 21 24 25 37 38 40 41 43 45 46 47 53 55 57 58 59 60 84 85
</pre>

Using those two files, we can generate the CNS-formatted AIR restraint files
with the following command:

<a class="prompt prompt-cmd">
haddock3-restraints active_passive_to_ambig restraints/e2a.act-pass restraints/hpr.act-pass \-\-segid-one A \-\-segid-two B > e2a-hpr_air.tbl
</a>

This generates a file called `ambig-prot-prot.tbl` that contains the AIR
restraints. The default distance range for those is between 0 and 2Å, which
might seem short but makes senses because of the 1/r^6 summation in the AIR
energy function that makes the effective distance be significantly shorter than
the shortest distance entering the sum.

The effective distance is calculated as the SUM over all pairwise atom-atom
distance combinations between an active residue and all the active+passive on
the other molecule: SUM[1/r^6]^(-1/6).

<hr>

### Restraints validation

If you modify manually this generated restraint files or create your own, it is possible to quickly check if the format is valid using the following `haddock3-restraints` sub-command:

<a class="prompt prompt-cmd">
haddock3-restraints validate_tbl e2a-hpr_air.tbl \-\-silent
</a>

No output means that your TBL file is valid.

*__Note__* that this only validates the syntax of the restraint file, but does not check if the selections defined in the restraints are actually existing in your input PDB files.


<hr>
<hr>

## Setting up the docking with HADDOCK3

<hr>

### HADDOCK3 workflow definition

Now that we have all required files at hand (PBD and restraints files) it is time to setup our docking protocol.
For this we need to create a HADDOCK3 configuration file that will define the docking workflow. In contrast to HADDOCK2.X,
we have much more flexibility in doing this. We will illustrate this flexibility by introducing a clustering step
after the initial rigid-body docking stage, select up to 10 models per cluster and refine all of those.

HADDOCK3 also provides an analysis module (`caprieval`) that allows
to compare models to either the best scoring model (if no reference is given) or a reference structure, which in our case
we have at hand. This will directly allow us to assess the performance of the protocol for the following two scenarios:

1. **Scenario 1**: 1000 rigidbody docking models, selection of top200 and flexible refinement + EM 
3. **Scenario 2**: 1000 rigidbody docking models, FCC clustering and selection of max 20 models per cluster followed by flexible refinement and EM

The basic workflow for the first scenario consists of the following modules:

1. **`topoaa`**: *Generates the topologies for the CNS engine and builds missing atoms*
2. **`rigidbody`**: *Performs rigid body energy minimisation (`it0` in haddock2.x)*
3. **`caprieval`**: *Calculates CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ) with respect to the top scoring model or reference structure if provided*
4. **`seletop`** : *Selects the top X models from the previous module*
5. **`flexref`**: *Preforms semi-flexible refinement of the interface (`it1` in haddock2.4)*
6. **`caprieval`**
7. **`emref`**: *Final refinement by energy minimisation (`itw` EM only in haddock2.4)*
8. **`caprieval`**
9. **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
10. **`seletopclusts`**: *Selects the top models of all clusters*
11. **`caprieval`** Cluster-based CAPRI statistics
12. **`contactmap`**: *Contacts matrix and a chordchart of intermolecular contacts*

In the second scenario a clustering step is introduced after rigid-body docking with the seletop module of scenario 1 (step4) replaced by:

* **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
* **`seletopclusts`**: *Selection of the top10 models of all clusters*

The input PDB and restraints files are the same for the two scenarios.


The corresponding toml configuration files are provided in the `workflows` directory. For scenario2 it looks like:

{% highlight toml %}
# ====================================================================
# Protein-protein docking example with NMR-derived ambiguous interaction restraints
# ====================================================================

# directory in which the scoring will be done
run_dir = "run2-full"

# execution mode
mode = "local"
# maximum of 50 cores (limited by the number of available cores)
ncores = 50

# molecules to be docked
molecules =  [
    "data/e2aP_1F3G.pdb",
    "data/hpr-ensemble_clean.pdb"
    ]

# ====================================================================
# Parameters for each stage are defined below, prefer full paths
# ====================================================================

[topoaa]
autohis = true

[rigidbody]
tolerance = 5
ambig_fname = "data/e2a-hpr_air.tbl"

[caprieval]
reference_fname = "data/e2a-hpr_1GGR.pdb"

[clustfcc]

[seletopclusts]

[caprieval]
reference_fname = "data/e2a-hpr_1GGR.pdb"

[flexref]
tolerance = 5
ambig_fname = "data/e2a-hpr_air.tbl"

[caprieval]
reference_fname = "data/e2a-hpr_1GGR.pdb"

[emref]
tolerance = 5
ambig_fname = "data/e2a-hpr_air.tbl"

[caprieval]
reference_fname = "data/e2a-hpr_1GGR.pdb"

[clustfcc]

[seletopclusts]

[caprieval]
reference_fname = "data/e2a-hpr_1GGR.pdb"

[contactmap]

# ====================================================================
{% endhighlight %}


**_Note_**: For making best use of the available CPU resources it is recommended to adapt the sampling parameter to be a multiple of the number of available cores when running in local mode.

**_Note_**: In case no reference is available (the usual scenario), the best ranked model is used as reference for each stage.
Including `caprieval` at the various stages even when no reference is provided is useful to get the rankings and scores and visualise the results (see Analysis section below).

**_Note_**: The default sampling would be 1000 models for `rigidbody` of which, for scenario1, 200 are passed to the flexible refinement in `seletop`. 

As an indication of the computational requirements, the default sampling worflow of scenario1 for this tutorial completes in about 37min using 12 cores on a MaxOSX M2 processor.

**_Note_**: To get a list of all possible parameters that can be defined in a specific module (and their default values) you can use the following command:

<a class="prompt prompt-cmd">
haddock3-cfg -m \<module\-name\>
</a>

Add the `-d` option to get a more detailed description of parameters and use the `-h` option to see a list of arguments and options.

Alternatively, you can consult the [developer's guide](https://www.bonvinlab.org/haddock3/){:target="_blank"}, where each parameter of each module is listed along with their default values, short and long descriptions, etc. Navigate to the [Modules](https://www.bonvinlab.org/haddock3/modules/index.html#){:target="_blank"} and select a module which parameters you want to display.

<a class="prompt prompt-question">
In the above workflow we see in three modules a *tolerance* parameter defined. Using the *haddock3-cfg* command try to figure out what this parameter does.
</a>


<hr>

### Running HADDOCK3

In in the first section of the workflow above we have a parameter `mode` defining the execution mode. HADDOCK3 currently supports three difference execution modes:

- **local** : In this mode, HADDOCK3 will run on the current system, using the defined number of cores (`ncores`) in the config file to a maximum of the total number of available cores on the system.
- **batch**: In this mode, HADDOCK3 will typically be started on your local server (e.g. the login node) and will dispatch jobs to the batch system of your cluster (slurm and torque are currently supported).
- **mpi**: HADDOCK3 also supports a pseudo parallel MPI implementation, which allows to harvest the power of multiple nodes to distribute the computations (functional but still very experimental at this stage).


<hr>

#### Learn more about the various execution modes of haddock3

<hr>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Local execution</i></b> <i class="material-icons">expand_more</i>
  </summary>

In this mode HADDOCK3 will run on the current system, using the defined number of cores (<i>ncores</i>) 
in the config file to a maximum of the total number of available cores on the system minus one. 
An example of the relevant parameters to be defined in the first section of the config file is:

{% highlight toml %}
# compute mode
mode = "local"
#  1 nodes x 50 ncores
ncores = 50
{% endhighlight %}

In this mode HADDOCK3 can be started from the command line with as argument the configuration file of the defined workflow.

{% highlight shell %}
haddock3 <my-workflow-configuration-file>
{% endhighlight %}

Alternatively redirect the output to a log file and send haddock3 to the background.


As an indication, running locally on an Apple M2 laptop using 10 cores, this workflow completed in 7 minutes.


{% highlight shell %}
haddock3 <my-workflow-configuration-file> > haddock3.log &
{% endhighlight %}

<b>Note</b>: This is also the execution mode that should be used for example when submitting the HADDOCK3 job to a node of a cluster, requesting X number of cores.

</details>

<hr>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Exection in batch mode using slurm</i></b> <i class="material-icons">expand_more</i>
  </summary>

  Here is an example script for submitting via the slurm batch system:

  {% highlight shell %}
  #!/bin/bash
  #SBATCH --nodes=1
  #SBATCH --tasks-per-node=50
  #SBATCH -J haddock3
  #SBATCH --partition=medium

  # activate the haddock3 conda environment
  source $HOME/miniconda3/etc/profile.d/conda.sh
  conda activate haddock3

  # go to the run directory
  cd $HOME/HADDOCK3-antibody-antigen

  # execute
  haddock3 <my-workflow-configuration-file>
  {% endhighlight %}
  <br>


  In this mode HADDOCK3 will typically be started on your local server (e.g. the login node) and will dispatch jobs to the batch system of your cluster. 
  Two batch systems are currently supported: <i>slurm</i> and <i>torque</i> (defined by the <i>batch_type</i> parameter). 
  In the configuration file you will have to define the <i>queue</i> name and the maximum number of concurrent jobs sent to the queue (<i>queue_limit</i>). 

  Since HADDOCK3 single model calculations are quite fast, it is recommended to calculate multiple models within one job submitted to the batch system. 
  he number of model per job is defined by the <i>concat</i> parameter in the configuration file. 
  You want to avoid sending thousands of very short jobs to the batch system if you want to remain friend with your system administrators...

  An example of the relevant parameters to be defined in the first section of the config file is:

  {% highlight toml %}
  # compute mode
  mode = "batch"
  # batch system
  batch_type = "slurm"
  # queue name
  queue = "short"
  # number of concurrent jobs to submit to the batch system
  queue_limit = 100
  # number of models to produce per submitted job
  concat = 10
  {% endhighlight %}

  In this mode HADDOCK3 can be started from the command line as for the local mode.
</details>

<hr>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Exection in MPI mode</i></b> <i class="material-icons">expand_more</i>
  </summary>


HADDOCK3 supports a parallel pseudo-MPI implementation. For this to work, the <i>mpi4py</i> library must have been installed at installation time. 
Refer to the (<a href="https://www.bonvinlab.org/haddock3/tutorials/mpi.html" target=new>MPI-related instructions</a>).

The execution mode should be set to `mpi` and the total number of cores should match the requested resources when submitting to the batch system.

An example of the relevant parameters to be defined in the first section of the config file is:

{% highlight toml %}
# compute mode
mode = "mpi"
#  5 nodes x 50 tasks = ncores = 250
ncores = 250
{% endhighlight %}

In this execution mode the HADDOCK3 job should be submitted to the batch system requesting the corresponding number of nodes and cores per node.


  {% highlight shell %}
  #!/bin/bash
  #SBATCH --nodes=5
  #SBATCH --tasks-per-node=50
  #SBATCH -J haddock3mpi

  # Make sure haddock3 is activated
  source $HOME/miniconda3/etc/profile.d/conda.sh
  conda activate haddock3

  # go to the run directory
  # edit if needed to specify the correct location
  cd $HOME/HADDOCK3-antibody-antigen

  # execute
  haddock3 \<my-workflow-configuration-file\>
  {% endhighlight %}
  <br>
</details>

<br>

<hr>

### Scenario 1: 1000 rigidbody docking models, selection of top 200 and flexible refinement + EM 

Now that we have all data ready, and know about execution modes of HADDOCK3 it is time to setup the docking for the first scenario. The restraint file to use for this is `e2a-hpr_air.tbl`. We proceed to produce 1000 rigidbody docking models, from which 200 will be selected and refined through flexible refinement and energy minimization. For the analysis following the docking results, we are using the solved complex [1GGR](https://www.rcsb.org/structure/1GGR), named e2a-hpr_1GGR.pdb.

The configuration file for this scenario is provided as `workflows/scenario1.cfg`

If you have everything ready, you can launch haddock3 either from the command line, or, better,
submitting it to the batch system requesting in this local run mode a full node (see local execution mode above).
Instead of running the full sampling scenario, you can run a shorter version (sampling reduced to 100/20) (the full run results are anyway provided in the `runs` directory):

<a class="prompt prompt-cmd">
haddock3 workflows/scenario1-short.cfg
</a>

As an indication, running locally on an Apple M2 laptop using 10 cores, this workflow completed in less than 3 minutes.

<hr>

### Scenario 2: 1000 rigidbody docking models, FCC clustering and selection of max 20 models per cluster followed by flexible refinement and EM 

In scenario 2, we proceed to produce 1000 rigidbody docking models, from which we proceed to do a first clustering analysis. From the top10 models of each clusters a flexible refinement then energy minization is done. This scenario illustrates the new flexibility of HADDOCK3, adding a clustering step after rigid-body docking, which is not possible in the HADDOCK2.X version.

The configuration file for this scenario is provided as `workflows/scenario2.cfg`

If you have everything ready, you can launch haddock3 either from the command line, or, better,
submitting it to the batch system requesting in this local run mode a full node (see local execution mode above).
Instead of running the full sampling scenario, you can run a shorter version (sampling reduced to 100) (the full run results are anyway provided in the `runs` directory):

<a class="prompt prompt-cmd">
haddock3 workflows/scenario2-short.cfg
</a>

As an indication, running locally on an Apple M2 laptop using 10 cores, this workflow completed in less than 4 minutes.


<hr>
<hr>

## Analysis of docking results


### General structure of a run directory

In case something went wrong with the docking (or simply if you do not want to wait for the results) you can find the following precalculated runs in the `runs` directory:
- `run1-full`: docking scenario1
- `run1-short`: docking scenario1-short (limited sampling)
- `run2-full`: docking scenario2
- `run2-short`: docking scenario2-short (limited sampling)


Once your run has completed inspect the content of the resulting directory. You will find the various steps (modules) of the defined workflow numbered sequentially, e.g. for scenario 2:

{% highlight shell %}
> ls runs/run2-full/
    00_topoaa/
    01_rigidbody/
    02_caprieval/
    03_clustfcc/
    04_seletopclusts/
    05_caprieval/
    06_flexref/
    07_caprieval/
    08_emref/
    09_caprieval/
    10_clustfcc/
    11_seletopclusts/
    12_caprieval/
    13_contactmaps
    analysis/
    data/
    log
    traceback/
{% endhighlight %}

In addition, there is a log file (text file) and four additional directories:

- the `analysis` directory contains various plots to visualize the results for each caprieval step and a general report (`report.html`) that provides all statistics with various plots. You can open this file in your preferred web browser
- the `data` directory contains the input data (PDB and restraint files) for the various modules, as well as an input workflow  (in `configurations` directory)
- the `toppar` directory contains the force field topology and parameter files (only present when running in self-contained mode)
- the `traceback` directory contains `traceback.tsv`, which links all models to see which model originates from which throughout all steps of the workflow.

You can find information about the duration of the run at the bottom of the log file. 

Each sampling/refinement/selection module will contain PDB files.
For example, the `09_seletopclusts` directory contains the selected models from each cluster. The clusters in that directory are numbered based
on their rank, i.e. `cluster_1` refers to the top-ranked cluster. Information about the origin of these files can be found in that directory in the `seletopclusts.txt` file.

The simplest way to extract ranking information and the corresponding HADDOCK scores is to look at the `XX_caprieval` directories (which is why it is a good idea to have it as the final module, and possibly as intermediate steps). This directory will always contain a `capri_ss.tsv` single model statistics file, which contains the model names, rankings and statistics (score, iRMSD, Fnat, lRMSD, ilRMSD and dockq score). E.g. for `run1-short/11_caprieval`:

<pre style="background-color:#DAE4E7">
model   md5     caprieval_rank  score   irmsd   fnat    lrmsd   ilrmsd  dockq   rmsd    cluster_id      cluster_ranking model-cluster_ranking   air       angles  bonds   bsa     cdih    coup    dani    desolv  dihe    elec    improper        rdcs    rg      sym     total   vdw     vean    xpcs
../10_seletopclusts/cluster_1_model_1.pdb       -       1       -144.590        0.968   0.833   1.773   1.596   0.832   0.925   1       1       1         11.352  0.000   0.000   1572.430        0.000   0.000   0.000   -8.787  0.000   -528.847        0.000   0.000   0.000   0.000   -548.663          -31.169 0.000   0.000
../10_seletopclusts/cluster_1_model_2.pdb       -       2       -144.369        0.969   0.833   1.764   1.677   0.833   0.917   1       1       2         3.578   0.000   0.000   1628.850        0.000   0.000   0.000   -4.135  0.000   -536.519        0.000   0.000   0.000   0.000   -566.229          -33.288 0.000   0.000
../10_seletopclusts/cluster_1_model_3.pdb       -       3       -143.590        1.001   0.861   1.465   1.623   0.841   0.920   1       1       3         9.963   0.000   0.000   1616.320        0.000   0.000   0.000   -11.809 0.000   -495.045        0.000   0.000   0.000   0.000   -518.850          -33.768 0.000   0.000
../10_seletopclusts/cluster_1_model_4.pdb       -       4       -142.554        1.083   0.861   2.156   1.981   0.819   1.039   1       1       4         10.613  0.000   0.000   1639.750        0.000   0.000   0.000   -6.181  0.000   -542.950        0.000   0.000   0.000   0.000   -561.182          -28.844 0.000   0.000
....
</pre>

If clustering was performed prior to calling the `caprieval` module, the `capri_ss.tsv` file will also contain information about to which cluster the model belongs to and its ranking within the cluster.

The relevant statistics are:

* **score**: *the HADDOCK score (arbitrary units)*
* **irmsd**: *the interface RMSD, calculated over the interfaces the molecules*
* **fnat**: *the fraction of native contacts*
* **lrmsd**: *the ligand RMSD, calculated on the ligand after fitting on the receptor (1st component)*
* **ilrmsd**: *the interface-ligand RMSD, calculated over the interface of the ligand after fitting on the interface of the receptor (more relevant for small ligands for example)*
* **dockq**: *the DockQ score, which is a combination of irmsd, lrmsd and fnat and provides a continuous scale between 1 (exactly equal to reference) and 0*

Various other terms are also reported including:

* **bsa**: *the buried surface area (in squared angstroms)*
* **elec**: *the intermolecular electrostatic energy*
* **vdw**: *the intermolecular van der Waals energy*
* **desolv**: *the desolvation energy*


The iRMSD, lRMSD and Fnat metrics are the ones used in the blind protein-protein prediction experiment [CAPRI](https://capri.ebi.ac.uk/){:target="_blank"} (Critical PRediction of Interactions).

In CAPRI the quality of a model is defined as (for protein-protein complexes):

* **acceptable model**: i-RMSD < 4Å or l-RMSD < 10Å and Fnat > 0.1 (0.23 < DOCKQ < 0.49)
* **medium quality model**: i-RMSD < 2Å or l-RMSD < 5Å and Fnat > 0.3 (0.49 < DOCKQ < 0.8)
* **high quality model**: i-RMSD < 1Å or l-RMSD < 1Å and Fnat > 0.5 (DOCKQ > 0.8)

<a class="prompt prompt-question">
Based on these CAPRI criteria, what is the quality of the best model listed above (_cluster_1_model_1.pdb_)?
</a>

In case where the `caprieval` module is called after a clustering step, an additional `capri_clt.tsv` file will be present in the directory.
This file contains the cluster ranking and score statistics, averaged over the minimum number of models defined for clustering
(4 by default), with their corresponding standard deviations. E.g.:

<pre style="background-color:#DAE4E7">
cluster_rank    cluster_id      n       under_eval      score   score_std       irmsd   irmsd_std       fnat    fnat_std        lrmsd   lrmsd_std         dockq   dockq_std       ilrmsd  ilrmsd_std      rmsd    rmsd_std        air     air_std bsa     bsa_std desolv  desolv_std      elec    elec_std  total   total_std       vdw     vdw_std caprieval_rank
1       1       10      -       -143.776        0.797   1.005   0.047   0.847   0.014   1.790   0.245   0.831   0.008   1.719   0.154   0.950   0.051     8.876   3.098   1614.337        25.576  -7.728  2.876   -525.840        18.467  -548.731        18.399  -31.767 1.951   1
2       2       10      -       -105.647        1.229   8.381   0.284   0.062   0.012   16.486  0.188   0.101   0.005   15.075  0.553   8.804   0.164     17.581  18.306  1345.355        73.378  -10.584 2.556   -380.353        22.927  -383.522        23.800  -20.750 3.583   2
3       4       4       -       -94.700 6.884   6.074   0.340   0.056   0.020   10.320  0.591   0.173   0.013   11.010  0.546   5.651   0.339   15
...
</pre>


In this file you find the cluster rank (which corresponds to the naming of the clusters in the previous `seletop` directory), the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (n) in the cluster and the corresponding statistics (averages + standard deviations). The corresponding cluster PDB files will be found in the preceeding `09_seletopclusts` directory.

While these simple text files can be easily checked from the command line already, they might be cumbersome to read.
For that reason, we have developed a post-processing analysis that automatically generates html reports for all `caprieval` steps in the workflow.
These are located in the respective `analysis/XX_caprieval` directories and can be viewed using your favorite web browser.


<hr>

### Analysis scenario 1: 

Let us now analyze the docking results for this scenario. Use for that either your own run or a pre-calculated run provided in the `runs` directory.

First of all let us check the final cluster statistics using the full run results from `runs/run1-full`.

<a class="prompt prompt-info">Inspect the _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the pre-calculated 11_caprieval/capri_clt.tsv file</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
cluster_rank    cluster_id      n       under_eval      score   score_std       irmsdirmsd_std        fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std    ilrmsd   ilrmsd_std      air     air_std bsa     bsa_std desolv  desolv_std      elec elec_std total   total_std       vdw     vdw_std caprieval_rank
1       1       132     -       -136.315        2.459   0.922   0.050   0.847   0.0501.497    0.158   0.848   0.022   1.577   0.100   17.510  10.499  1592.155        26.85-11.290  2.460   -477.868        20.524  -491.561        13.390  -31.203 1.856   1     
2       2       41      -       -118.410        9.418   7.843   0.237   0.194   0.00014.976   0.870   0.158   0.008   14.161  0.256   33.123  27.142  1525.405        19.48-11.788  2.649   -396.013        33.391  -393.621        55.889  -30.732 8.145   2     
3       3       8       -       -87.144 5.206   3.741   0.418   0.333   0.039   7.4090.410    0.348   0.025   7.643   0.422   41.435  13.967  1290.872        72.223  -15.930       4.468   -245.765        38.007  -230.535        31.740  -26.204 3.205   3     
4       4       4       -       -55.138 9.488   2.340   0.218   0.292   0.031   5.7850.727    0.424   0.019   5.334   0.773   42.306  19.922  960.189 142.370 -13.059 3.913-158.379 14.190  -130.707        26.432  -14.634 3.528   4
</pre>
</details>
<br>

<a class="prompt prompt-question">How many clusters are generated?</a>

<a class="prompt prompt-question">Look at the score of the first few clusters: Are they significantly different if you consider their average scores and standard deviations?</a>

Since for this tutorial we have at hand the crystal structure of the complex, we provided it as reference to the `caprieval` modules.
This means that the iRMSD, lRMSD, Fnat and DockQ statistics report on the quality of the docked model compared to the reference crystal structure.

<a class="prompt prompt-question">How many clusters of acceptable or better quality have been generate according to CAPRI criteria?</a>

<a class="prompt prompt-question">What is the rank of the best cluster generated?</a>

<a class="prompt prompt-question">What is the rank of the first acceptable of better cluster generated?</a>


We are providing in the `scripts` directory a simple script that extract some cluster statistics for acceptable or better clusters from the `caprieval` steps.
To use is simply call the script with as argument the run directory you want to analyze, e.g.:

<a class="prompt prompt-cmd">
   ./scripts/extract-capri-stats-clt.sh ./run1-full
</a>

<details style="background-color:#DAE4E7">
 <summary>
  <i>View the output of the script</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1-full/02_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  0  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:   i-RMSD:   Fnat:   DockQ: 
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  6.407  Fnat:  0.202  DockQ:  0.264      
==============================================
== run1-full/04_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  0  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:   i-RMSD:   Fnat:   DockQ: 
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  6.407  Fnat:  0.202  DockQ:  0.264      
==============================================
== run1-full/06_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  1  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:  -  i-RMSD:  2.976  Fnat:  0.611  DockQ:  0.601
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  2.976  Fnat:  0.611  DockQ:  0.601      
==============================================
== run1-full/08_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  1  out of  1
Total number of medium or better clusters:      1  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:  -  i-RMSD:  1.673  Fnat:  0.736  DockQ:  0.727
First medium cluster     - rank:  -  i-RMSD:  1.673  Fnat:  0.736  DockQ:  0.727      
Best cluster             - rank:  -  i-RMSD:  1.673  Fnat:  0.736  DockQ:  0.727      
==============================================
== run1-full/11_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  3  out of  4
Total number of medium or better clusters:      1  out of  4
Total number of high quality clusters:          1  out of  4

First acceptable cluster - rank:  1  i-RMSD:  0.922  Fnat:  0.847  DockQ:  0.848
First medium cluster     - rank:  1  i-RMSD:  0.922  Fnat:  0.847  DockQ:  0.848      
Best cluster             - rank:  1  i-RMSD:  0.922  Fnat:  0.847  DockQ:  0.848      
</pre>
</details>

<br>

Similarly some simple statistics can be extracted from the single model `caprieval` `capri_ss.tsv` files with the `extract-capri-stats.sh` script:


<a class="prompt prompt-cmd">
   ./scripts/extract-capri-stats.sh ./runs/run1-full
</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script:</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1-full/02_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  365  out of  1000
Total number of medium or better models:      199  out of  1000
Total number of high quality models:          0  out of  1000

First acceptable model - rank:  3  i-RMSD:  1.153  Fnat:  0.556  DockQ:  0.711
First medium model     - rank:  3  i-RMSD:  1.153  Fnat:  0.556  DockQ:  0.711        
Best model             - rank:  46  i-RMSD:  1.145  Fnat:  0.556  DockQ:  0.713       
==============================================
== run1-full/04_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  144  out of  200
Total number of medium or better models:      137  out of  200
Total number of high quality models:          0  out of  200

First acceptable model - rank:  3  i-RMSD:  1.153  Fnat:  0.556  DockQ:  0.711
First medium model     - rank:  3  i-RMSD:  1.153  Fnat:  0.556  DockQ:  0.711        
Best model             - rank:  46  i-RMSD:  1.145  Fnat:  0.556  DockQ:  0.713       
==============================================
== run1-full/06_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  147  out of  200
Total number of medium or better models:      118  out of  200
Total number of high quality models:          20  out of  200

First acceptable model - rank:  2  i-RMSD:  1.221  Fnat:  0.694  DockQ:  0.727
First medium model     - rank:  2  i-RMSD:  1.221  Fnat:  0.694  DockQ:  0.727        
Best model             - rank:  30  i-RMSD:  0.883  Fnat:  0.750  DockQ:  0.823       
==============================================
== run1-full/08_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  147  out of  200
Total number of medium or better models:      118  out of  200
Total number of high quality models:          34  out of  200

First acceptable model - rank:  1  i-RMSD:  1.219  Fnat:  0.833  DockQ:  0.787
First medium model     - rank:  1  i-RMSD:  1.219  Fnat:  0.833  DockQ:  0.787        
Best model             - rank:  39  i-RMSD:  0.807  Fnat:  0.833  DockQ:  0.862       
==============================================
== run1-full/11_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  141  out of  185
Total number of medium or better models:      116  out of  185
Total number of high quality models:          34  out of  185

First acceptable model - rank:  1  i-RMSD:  0.907  Fnat:  0.917  DockQ:  0.871
First medium model     - rank:  1  i-RMSD:  0.907  Fnat:  0.917  DockQ:  0.871        
Best model             - rank:  36  i-RMSD:  0.807  Fnat:  0.833  DockQ:  0.862          
</pre>
</details>

<br>

_**Note**_ that this kind of analysis only makes sense when we know the reference complex and for benchmarking / performance analysis purposes.

<a class="prompt prompt-info">Look at the single structure statistics provided by the script</a>

<a class="prompt prompt-question">How does the quality of the model changes after flexible refinement? Consider here the various metrics.</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
    In terms of iRMSD values we only observe very small differences in the best models, but the change in ranking is impressive!
    The fraction of native contacts and the DockQ scores are however improving much more after flexible refinement.
    All this will of course depend on how different are the bound and unbound conformations and the amount of data
    used to drive the docking process. In general, from our experience, the more and better data at hand,
    the larger the conformational changes that can be induced.
  </p>
  </details>

<br>

<a class="prompt prompt-question">Is the best model always rank as first?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
    This is clearly not the case. The scoring function is not perfect, but does a reasonable job in ranking models of acceptable or better quality on top in this case.
  </p>
</details>

<br>

#### Analysis scenario 1: visualising the scores and their components

We have precalculated a number of interactive plots to visualize the scores and their components versus ranks and model quality.

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>

Models statistics:

* [iRMSD versus HADDOCK score](plots/scenario1/irmsd_score.html){:target="_blank"}
* [DockQ versus HADDOCK score](plots/scenario1/dockq_score.html){:target="_blank"}

Cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank):

* [HADDOCK scores](plots/scenario1/score_clt.html){:target="_blank"}
* [iRMSD](plots/scenario1/irmsd_clt.html){:target="_blank"}
* [DockQ](plots/scenario1/dockq_clt.html){:target="_blank"}

<hr>

### Analysis scenario 2: 

Let us now analyse the docking results for this scenario. Use for that either your own run or a pre-calculated run provided in the `runs` directory.
Go into the _analysis/_caprieval_analysis_  directory of the respective run directory and

<a class="prompt prompt-info">Inspect the final cluster statistics in _capri_clt.tsv_ file </a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the pre-calculated _caprieval/capri_clt.tsv file</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
cluster_rank    cluster_id      n       under_eval      score   score_std       irmsdirmsd_std        fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std    ilrmsd   ilrmsd_std      air     air_std bsa     bsa_std desolv  desolv_std      elec elec_std total   total_std       vdw     vdw_std caprieval_rank
1       1       37      -       -124.658        10.252  3.857   0.922   0.319   0.0976.660    1.321   0.365   0.085   6.780   1.681   31.615  22.188  1616.990        119.623       -6.778  6.101   -437.724        75.263  -439.605        69.689  -33.496 10.191
2       3       26      -       -119.435        4.949   0.982   0.026   0.805   0.0522.058    0.408   0.816   0.026   1.781   0.120   29.748  11.990  1522.275        58.81-14.346  5.089   -383.147        87.371  -384.832        89.623  -31.434 9.369   2     
3       8       15      -       -117.501        8.381   10.507  0.012   0.049   0.02318.245   0.253   0.082   0.008   17.406  0.097   16.941  13.148  1695.840        65.32-11.683  2.440   -305.048        31.227  -334.610        34.942  -46.502 3.538   3     
4       10      12      -       -115.472        5.836   0.980   0.038   0.812   0.0532.062    0.443   0.819   0.020   1.762   0.114   19.993  10.271  1488.888        64.59-14.848  1.764   -351.208        32.914  -363.598        30.092  -32.382 8.809   4     
5       2       27      -       -106.389        2.683   9.379   0.146   0.125   0.01416.285   0.693   0.122   0.004   16.768  0.405   20.260  12.423  1359.715        23.92-10.242  1.447   -272.409        33.608  -295.839        37.474  -43.691 4.786   5     
6       4       25      -       -106.037        2.709   7.852   0.619   0.132   0.07715.047   1.787   0.139   0.042   14.277  0.588   43.187  10.734  1403.977        70.15-13.256  1.092   -361.058        57.590  -342.759        55.416  -24.888 11.965  6     
7       9       13      -       -105.524        8.380   10.273  0.355   0.076   0.01217.160   0.297   0.098   0.005   16.986  0.601   52.965  34.487  1493.557        88.840.241    1.661   -433.424        58.594  -404.836        36.296  -24.376 10.058  7     
8       13      11      -       -104.016        12.736  6.651   1.287   0.215   0.04112.319   2.028   0.201   0.046   11.777  2.166   67.269  34.762  1452.928        53.36-7.209   2.522   -367.069        36.068  -329.921        62.280  -30.121 8.255   8     
9       12      11      -       -100.932        9.238   10.829  0.016   0.132   0.01218.562   0.153   0.108   0.004   17.755  0.101   32.367  14.729  1645.305        104.797       -18.030 2.335   -232.574        32.271  -239.830        42.371  -39.624 7.4289
...
</pre>
</details>
<br>

<a class="prompt prompt-question">How many clusters of acceptable or better quality have been generate according to CAPRI criteria?</a>

<a class="prompt prompt-question">What is the rank of the best cluster generated?</a>

<a class="prompt prompt-question">What is the rank of the first acceptable of better cluster generated?</a>


In this run we also had a `caprieval` after the clustering of the rigid body models (step 5 of our workflow).

<a class="prompt prompt-info">Inspect the corresponding _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the pre-calculated 5_caprieval/capri_clt.tsv file</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
cluster_rank    cluster_id      n       under_eval      score   score_std       irmsdirmsd_std        fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std    ilrmsd   ilrmsd_std      air     air_std bsa     bsa_std desolv  desolv_std      elec elec_std total   total_std       vdw     vdw_std caprieval_rank
1       4       20      -       -32.647 0.718   8.443   0.050   0.056   0.000   16.670.440    0.098   0.003   15.142  0.029   103.171 30.153  1037.440        40.574  -16.600       0.384   -6.642  0.367   90.292  34.825  -6.237  4.862   1
2       1       20      -       -32.078 0.309   1.193   0.052   0.563   0.012   2.3440.382    0.701   0.015   2.241   0.176   144.927 37.448  1185.507        24.515  -14.154       0.495   -7.458  0.197   131.527 41.553  -5.942  4.909   2
3       11      15      -       -31.524 0.512   2.591   0.043   0.306   0.000   5.8830.150    0.411   0.006   5.951   0.125   238.270 90.904  838.533 10.610  -17.621 0.383-7.971   0.168   237.269 95.233  6.969   4.900   3
4       23      6       -       -31.175 0.237   4.180   0.009   0.285   0.012   7.7030.015    0.316   0.004   8.171   0.036   217.839 78.900  1071.035        16.129  -15.642       0.348   -6.892  0.257   199.998 83.806  -10.949 5.140   4
5       32      4       -       -30.152 1.356   7.126   0.074   0.069   0.024   16.690.938    0.106   0.014   12.952  0.455   286.907 150.515 1041.192        37.687  -13.618       0.880   -8.950  0.629   273.851 150.190 -4.106  4.566   5
6       33      4       -       -29.431 2.824   2.660   0.894   0.326   0.121   7.1353.087    0.407   0.141   6.418   2.586   124.179 48.395  917.899 78.204  -13.272 2.489-8.230   0.566   116.856 51.814  0.907   4.084   6
7       2       20      -       -27.915 0.952   4.133   0.017   0.139   0.020   7.0510.018    0.282   0.007   7.455   0.023   264.450 31.588  1014.276        17.755  -11.711       0.867   -8.673  0.226   252.511 36.667  -3.266  5.371   7
8       17      11      -       -27.474 1.291   6.676   0.703   0.063   0.012   11.461.246    0.157   0.014   12.049  1.207   303.023 57.328  963.135 62.068  -12.556 1.856-8.338   0.587   296.748 55.220  2.063   6.790   8
9       13      14      -       -27.374 0.754   10.733  0.011   0.083   0.000   18.250.037    0.094   0.000   17.522  0.031   134.468 43.797  1039.598        13.308  -13.613       0.558   -4.687  0.149   127.422 45.173  -2.360  2.548   9
...
</pre>
</details>
<br>

<a class="prompt prompt-question">How many clusters are generated?</a>

<a class="prompt prompt-question">Is this the same number that after refinement (see above)?</a>

<a class="prompt prompt-question">If not what could be the reason?</a>

<a class="prompt prompt-question">Consider again the rank of the first acceptable cluster based on iRMSD values. How does this compare with the refined clusters (see above)?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer </i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
    After rigid body docking the first acceptable cluster is at rank 3 and the same is true after refinement, but the iRMSD values have improved.
  </p>
</details>

<br>

Use the `extract-capri-stats-clt.sh` script to extract some simple cluster statistics for this run.

<a class="prompt prompt-cmd">
   ./scripts/extract-capri-stats-clt.sh runs/run2-full/
</a>


<details style="background-color:#DAE4E7">
<summary>
  <i>View the output of the script </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run2-full/02_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  0  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:   i-RMSD:   Fnat:   DockQ: 
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  6.407  Fnat:  0.202  DockQ:  0.264      
==============================================
== run2-full/05_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  6  out of  33
Total number of medium or better clusters:      1  out of  33
Total number of high quality clusters:          0  out of  33

First acceptable cluster - rank:  2  i-RMSD:  1.193  Fnat:  0.563  DockQ:  0.701
First medium cluster     - rank:  2  i-RMSD:  1.193  Fnat:  0.563  DockQ:  0.701      
Best cluster             - rank:  2  i-RMSD:  1.193  Fnat:  0.563  DockQ:  0.701      
==============================================
== run2-full/07_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  0  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:   i-RMSD:   Fnat:   DockQ: 
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  8.237  Fnat:  0.104  DockQ:  0.121      
==============================================
== run2-full/09_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  0  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:   i-RMSD:   Fnat:   DockQ: 
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  4.840  Fnat:  0.361  DockQ:  0.400      
==============================================
== run2-full/12_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  4  out of  25
Total number of medium or better clusters:      2  out of  25
Total number of high quality clusters:          2  out of  25

First acceptable cluster - rank:  1  i-RMSD:  3.857  Fnat:  0.319  DockQ:  0.365
First medium cluster     - rank:  2  i-RMSD:  0.982  Fnat:  0.805  DockQ:  0.816      
Best cluster             - rank:  4  i-RMSD:  0.980  Fnat:  0.812  DockQ:  0.819      
</pre>
</details>

<br>

Similarly some simple statistics can be extracted from the single model `caprieval` `capri_ss.tsv` files with the `extract-capri-stats.sh` script:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats.sh ./runs/run2-full
</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run2-full/02_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  365  out of  1000
Total number of medium or better models:      199  out of  1000
Total number of high quality models:          0  out of  1000

First acceptable model - rank:  3  i-RMSD:  1.153  Fnat:  0.556  DockQ:  0.711
First medium model     - rank:  3  i-RMSD:  1.153  Fnat:  0.556  DockQ:  0.711        
Best model             - rank:  46  i-RMSD:  1.145  Fnat:  0.556  DockQ:  0.713       
==============================================
== run2-full/05_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  62  out of  375
Total number of medium or better models:      22  out of  375
Total number of high quality models:          0  out of  375

First acceptable model - rank:  3  i-RMSD:  1.153  Fnat:  0.556  DockQ:  0.711
First medium model     - rank:  3  i-RMSD:  1.153  Fnat:  0.556  DockQ:  0.711        
Best model             - rank:  46  i-RMSD:  1.145  Fnat:  0.556  DockQ:  0.713       
==============================================
== run2-full/07_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  74  out of  375
Total number of medium or better models:      27  out of  375
Total number of high quality models:          1  out of  375

First acceptable model - rank:  6  i-RMSD:  1.081  Fnat:  0.750  DockQ:  0.771
First medium model     - rank:  6  i-RMSD:  1.081  Fnat:  0.750  DockQ:  0.771        
Best model             - rank:  36  i-RMSD:  0.930  Fnat:  0.778  DockQ:  0.822       
==============================================
== run2-full/09_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  74  out of  375
Total number of medium or better models:      27  out of  375
Total number of high quality models:          7  out of  375

First acceptable model - rank:  1  i-RMSD:  3.718  Fnat:  0.333  DockQ:  0.382
First medium model     - rank:  3  i-RMSD:  0.991  Fnat:  0.806  DockQ:  0.821        
Best model             - rank:  60  i-RMSD:  0.896  Fnat:  0.778  DockQ:  0.828       
==============================================
== run2-full/12_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  65  out of  317
Total number of medium or better models:      27  out of  317
Total number of high quality models:          7  out of  317

First acceptable model - rank:  1  i-RMSD:  3.718  Fnat:  0.333  DockQ:  0.382
First medium model     - rank:  3  i-RMSD:  0.991  Fnat:  0.806  DockQ:  0.821        
Best model             - rank:  54  i-RMSD:  0.896  Fnat:  0.778  DockQ:  0.828       
</pre>
</details>

<br>

_**Note**_ that this kind of analysis only makes sense when we know the reference complex and for benchmarking / performance analysis purposes.

<a class="prompt prompt-info">Look at the single structure statistics provided by the script</a>

<a class="prompt prompt-question">How does the quality of the model changes after flexible refinement? Consider here the various metrics.</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
    In this case we observe a small improvement in terms of iRMSD values as well as in the fraction of native contacts and the DockQ scores. Also the single model rankings have improved, but the top ranked model is not the best one.
  </p>
</details>

<br>

<a class="prompt prompt-question">Is the best model always rank as first?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
  This is clearly not the case. The scoring function is not perfect, but does a reasonable job in ranking models of acceptable or better quality on top in this case.
  </p>
</details>

<br>

#### Analysis scenario 2: visualising the scores and their components

We have precalculated a number of interactive plots to visualize the scores and their components versus ranks and model quality.

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>

Models statistics:

* [iRMSD versus HADDOCK score](plots/scenario2/irmsd_score.html){:target="_blank"}
* [DockQ versus HADDOCK score](plots/scenario2/dockq_score.html){:target="_blank"}

Cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank):

* [HADDOCK scores](plots/scenario2/score_clt.html){:target="_blank"}
* [iRMSD](plots/scenario2/irmsd_clt.html){:target="_blank"}
* [DockQ](plots/scenario2/dockq_clt.html){:target="_blank"}

<hr>

### Comparing the performance of the two scenarios

Clearly all three scenarios give good results with an acceptable cluster in all three cases ranked at the top:

{% highlight shell %}
==============================================
== scenario1-full/11_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  141  out of  185
Total number of medium or better models:      116  out of  185
Total number of high quality models:          34  out of  185

First acceptable model - rank:  1  i-RMSD:  0.907  Fnat:  0.917  DockQ:  0.871
First medium model     - rank:  1  i-RMSD:  0.907  Fnat:  0.917  DockQ:  0.871        
Best model             - rank:  36  i-RMSD:  0.807  Fnat:  0.833  DockQ:  0.862            

==============================================
== scenario2-cltsel-full/12_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  65  out of  317
Total number of medium or better models:      27  out of  317
Total number of high quality models:          7  out of  317

First acceptable model - rank:  1  i-RMSD:  3.718  Fnat:  0.333  DockQ:  0.382
First medium model     - rank:  3  i-RMSD:  0.991  Fnat:  0.806  DockQ:  0.821        
Best model             - rank:  54  i-RMSD:  0.896  Fnat:  0.778  DockQ:  0.828        

{% endhighlight %}

While the first two scenarios show similar results, we can observe that scenario 2 produces a higher count of clusters, i.e. a higher conformational diversity than the other scenarios. 
This difference is most probably a consequence of the clustering step carried out after the rigidbody docking. In fact, this additional step allowed us to select the best models of each clusters, retaining the diversity produced in the riigid body step, while selecting the overall best ranked models in the first two scenarios showed lower diversity.

<hr>
<hr>

## Biological insights

The E2A-HPR complex is involved in phosphate-transfer, in which a phosphate group attached to histidine 90 of E2A (which we named NEP) is transferred to a histidine of HPR. As such, the docking models should make sense according to this information, meaning that two histidines should be in close proximity at the interface. Using PyMOL, check the various cluster representatives (we are assuming here you have performed all PyMOL commands of the previous section):

<a class="prompt prompt-pymol">
select histidines, resn HIS+NEP<br>
show spheres, histidines<br>
util.cnc<br>
</a>

<a class="prompt prompt-question">First of all, has the phosphate group been properly generated?</a>

**Note:** You can zoom on the phosphorylated histidine using the following PyMOL command:

<a class="prompt prompt-pymol">
zoom resn NEP<br>
</a>

<figure align="center">
<img src="/education/HADDOCK3/HADDOCK3-protein-protein-basic/phosphorylated-histidine.png">
</figure>

Zoom back to all visible molecules with

<a class="prompt prompt-pymol">
zoom vis<br>
</a>

Now inspect each cluster in turn and check if histidine 90 of E2A is in close proximity to another histidine of HPR.
To facilitate this analysis, view each cluster in turn (use the right panel to activate/desactivate the various clusters by clicking on their name).

<a class="prompt prompt-question">Based on this analysis, which cluster does satisfy best the biolocal information?</a>

<a class="prompt prompt-question">Is this cluster also the best ranked one?</a>

<hr>

## Comparison with the reference structure

As explained in the introduction, the structure of the native complex has been determined by NMR (PDB ID [1GGR](https://www.ebi.ac.uk/pdbe/entry/pdb/1ggr){:target="_blank"}) using a combination of intermolecular NOEs and dipolar coupling restraints. We will now compare the docking models with this structure.

If you still have all cluster representative open in PyMOL you can proceed with the sub-sequent analysis, otherwise load again each cluster representative as described above. Then, fetch the reference complex by typing in PyMOL:

<a class="prompt prompt-pymol">
fetch 1GGR<br>
show cartoon<br>
color yellow, 1GGR and chain A<br>
color orange, 1GGR and chain B<br>
</a>

The number of chain B in this structure is however different from the HPR numbering in the structure we used: It starts at 301 while in our models chain B starts at 1. We can change the residue numbering easily in PyMol with the following command:

<a class="prompt prompt-pymol">
alter (chain B and 1GGR), resv -=300<br>
</a>

Then superimpose all cluster representatives on the reference structure, using the entire chain A (E2A):

<a class="prompt prompt-pymol">
select 1GGR and chain A<br>
alignto sele<br>
</a>

<a class="prompt prompt-question">
Does any of the cluster representatives ressemble the reference NMR structure?
</a>
<a class="prompt prompt-question">
In case you found a reasonable prediction, what is its cluster rank?
</a>

<hr>
<hr>

## Congratulations! 🎉

You have completed this tutorial. If you have any questions or suggestions, feel free to contact us via email or asking a question through our [support center](https://ask.bioexcel.eu){:target="_blank"}.

And check also our [education](/education) web page where you will find more tutorials!


<!-- Links -->
[air-help]: https://www.bonvinlab.org/software/haddock2.4/airs/ "AIRs help"
[haddock-restraints]: https://wenmr.science.uu.nl/haddock-restraints/ "haddock-restraints"
[haddock24protein]: /education/HADDOCK24/HADDOCK24-protein-protein-basic/
[haddock-repo]: https://github.com/haddocking/haddock3 "HADDOCK3 GitHub"
[haddock-tools]: https://github.com/haddocking/haddock-tools "HADDOCK tools GitHub"
[installation]: https://www.bonvinlab.org/haddock3/INSTALL.html "Installation"
[link-cns]: https://cns-online.org "CNS online"
[link-forum]: https://ask.bioexcel.eu/c/haddock "HADDOCK Forum"
[link-pdbtools]:http://www.bonvinlab.org/pdb-tools/ "PDB-Tools"
[link-pymol]: https://www.pymol.org/ "PyMOL"
[nat-pro]: https://www.nature.com/articles/s41596-024-01011-0.epdf?sharing_token=UHDrW9bNh3BqijxD2u9Xd9RgN0jAjWel9jnR3ZoTv0O8Cyf_B_3QikVaNIBRHxp9xyFsQ7dSV3t-kBtpCaFZWPfnuUnAtvRG_vkef9o4oWuhrOLGbBXJVlaaA9ALOULn6NjxbiqC2VkmpD2ZR_r-o0sgRZoHVz10JqIYOeus_nM%3D "Nature protocol"
[tbl-examples]: https://github.com/haddocking/haddock-tools/tree/master/haddock_tbl_validation "tbl examples"
