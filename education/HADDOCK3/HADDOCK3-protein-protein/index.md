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

As an indication, running locally on an Apple M2 laptop using 12 cores, this workflow completed in less than 3 minutes, while the full runs takes about 21 minutes to complete.

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
model   md5     caprieval_rank  score   irmsd   fnat    lrmsd   ilrmsd  dockq   rmsd    cluster_id      cluster_ranking model-cluster_ranking   air     angles    bonds   bsa     cdih    coup    dani    desolv  dihe    elec    improper        rdcs    rg      sym     total   vdw     vean    xpcs
../10_seletopclusts/cluster_1_model_1.pdb       -       1       -148.148        1.030   0.889   1.472   1.672   0.846   0.927   1       1       1       6.170     241.843 37.056  1702.360        0.000   0.000   0.000   -13.126 1283.440        -496.737        47.899  0.000   0.000   0.000   -526.858        -36.292   0.000   0.000
../10_seletopclusts/cluster_1_model_2.pdb       -       2       -144.448        1.039   0.861   1.481   1.712   0.836   0.934   1       1       2       12.376    224.041 34.946  1659.740        0.000   0.000   0.000   -8.098  1291.960        -499.715        47.404  0.000   0.000   0.000   -524.983        -37.644   0.000   0.000
../10_seletopclusts/cluster_1_model_3.pdb       -       3       -144.433        1.070   0.861   1.505   1.761   0.831   0.959   1       1       3       12.586    234.166 37.464  1647.550        0.000   0.000   0.000   -10.129 1295.290        -514.186        49.351  0.000   0.000   0.000   -534.325        -32.725   0.000   0.000
../10_seletopclusts/cluster_1_model_4.pdb       -       4       -144.132        0.929   0.889   1.442   1.437   0.861   0.862   1       1       4       11.926    240.560 37.771  1564.810        0.000   0.000   0.000   -17.454 1294.750        -427.513        50.907  0.000   0.000   0.000   -457.955        -42.368   0.000   0.000
...
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
1       1       10      -       -145.291        1.655   1.017   0.053   0.875   0.014   1.475   0.022   0.844   0.012   1.646   0.125   0.920   0.036   10.765    2.663   1643.615        49.842  -12.202 3.521   -484.538        33.578  -511.030        30.842  -37.257 3.455   1
2       2       10      -       -104.588        5.104   7.967   0.362   0.125   0.069   15.246  0.938   0.133   0.031   14.405  0.552   8.271   0.392   38.880    9.265   1401.525        77.410  -14.119 0.968   -339.316        28.112  -326.929        17.229  -26.494 8.879   2
3       3       6       -       -88.298 4.646   3.016   0.265   0.326   0.030   8.303   1.830   0.350   0.052   7.289   0.855   2.997   0.436   28.868  21.272    1240.365        112.271 -16.524 4.943   -270.877        44.513  -262.493        33.887  -20.485 2.141   3
</pre>


In this file you find the cluster rank (which corresponds to the naming of the clusters in the previous `seletop` directory), the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (n) in the cluster and the corresponding statistics (averages + standard deviations). The corresponding cluster PDB files will be found in the preceeding `09_seletopclusts` directory.

While these simple text files can be easily checked from the command line already, they might be cumbersome to read.
For that reason, we have developed a post-processing analysis that automatically generates html reports for all `caprieval` steps in the workflow.
These are located in the respective `analysis/XX_caprieval` directories and can be viewed using your favorite web browser.


<hr>

### Analysis scenario 1: 

Let us now analyze the docking results for this scenario. Use for that either your own run or a pre-calculated run provided in the `runs` directory.



<hr>

#### Cluster statistics

First of all let us check the final cluster statistics using the full run results from `runs/run1-full`.

Go into the `analysis/10_caprieval_analysis` directory of the respective run directory  (if needed copy the run or that directory to your local computer) and open in a web browser the `report.html` file. Be patient as this page contains interactive plots that may take some time to generate.

You can also view this report online [here](plots/scenario1/report.html){:target="_blank"}


On the top of the page, you will see a table that summarises the cluster statistics (taken from the `capri_clt.tsv` file).
The columns (corresponding to the various clusters) are sorted by default on the cluster rank, which is based on the HADDOCK score (found on the 4th row of the table).
As this is an interactive table, you can sort it as you wish by using the arrows present in the first column.
Simply click on the arrows of the term you want to use to sort the table (and you can sort it in ascending or descending order).
A snapshot of this table is shown below:

*__Note__* that in case the PDB files are still compressed (gzipped) the download links will not work. Also online visualisation is not enabled.


<a class="prompt prompt-info">Inspect the final cluster statistics</a>

<a class="prompt prompt-question">How many clusters have been generated?</a>

<a class="prompt prompt-question">Look at the score of the first few clusters: Are they significantly different if you consider their average scores and standard deviations?</a>

Since for this tutorial we have at hand the crystal structure of the complex, we provided it as reference to the `caprieval` modules.
This means that the iRMSD, lRMSD, Fnat and DockQ statistics report on the quality of the docked model compared to the reference crystal structure.

<a class="prompt prompt-question">How many clusters of acceptable or better quality have been generate according to CAPRI criteria?</a>

<a class="prompt prompt-question">What is the rank of the best cluster generated?</a>

<a class="prompt prompt-question">What is the rank of the first acceptable of better cluster generated?</a>


We are also providing in the `scripts` directory a simple script that extract some cluster statistics for acceptable or better clusters from the `caprieval` steps.
To use is simply call the script with as argument the run directory you want to analyze, e.g.:

<a class="prompt prompt-cmd">
   ./scripts/extract-capri-stats-clt.sh ./runs/run1-full
</a>

<details style="background-color:#DAE4E7">
 <summary>
  <i>View the output of the script</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1-full//02_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  0  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:   i-RMSD:   Fnat:   DockQ:
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  5.163  Fnat:  0.292  DockQ:  0.339
==============================================
== run1-full//04_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  0  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:   i-RMSD:   Fnat:   DockQ:
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  5.970  Fnat:  0.174  DockQ:  0.222
==============================================
== run1-full//06_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  0  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:   i-RMSD:   Fnat:   DockQ:
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  5.846  Fnat:  0.174  DockQ:  0.223
==============================================
== run1-full//08_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  0  out of  1
Total number of medium or better clusters:      0  out of  1
Total number of high quality clusters:          0  out of  1

First acceptable cluster - rank:   i-RMSD:   Fnat:   DockQ:
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  -  i-RMSD:  5.814  Fnat:  0.201  DockQ:  0.231
==============================================
== run1-full//11_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  2  out of  3
Total number of medium or better clusters:      1  out of  3
Total number of high quality clusters:          0  out of  3

First acceptable cluster - rank:  1  i-RMSD:  1.017  Fnat:  0.875  DockQ:  0.844
First medium cluster     - rank:  1  i-RMSD:  1.017  Fnat:  0.875  DockQ:  0.844
Best cluster             - rank:  1  i-RMSD:  1.017  Fnat:  0.875  DockQ:  0.844
</pre>
</details>

<br>

<hr>

#### Visualizing the scores and their components


Next to the cluster statistic table shown above, the `report.html` file also contains a variety of plots displaying the HADDOCK score 
and its components against various CAPRI metrics (i-RMSD, l-RMSD,  Fnat, Dock-Q) with a color-coded representation of the clusters.
These are interactive plots. A menu on the top right of the first row (you might have to scroll to the rigth to see it) 
allows you to zoom in and out in the plots and turn on and off clusters. 

As a reminder, you can view this report online [**here**](plots/scenario1/report.html){:target="_blank"}

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>

<a class="prompt prompt-question">For this antibody-antigen case, which of the score components correlates best with the quality of the models?</a>


Finally, the report also shows at the bottom of the page plots of the cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank).

<hr>

#### Some single structure analysis


Single structure statistics can also be visualised in an html report if you would open a file from a caprieval step prior to clustering (e.g. `08_caprieval` after the final energy minimisation).

Some simple statistics can be extracted from the single model `caprieval` `capri_ss.tsv` files with the `extract-capri-stats.sh` script:


<a class="prompt prompt-cmd">
   ./scripts/extract-capri-stats.sh ./runs/run1-full
</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script:</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1-full//02_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  401  out of  1000
Total number of medium or better models:      221  out of  1000
Total number of high quality models:          0  out of  1000

First acceptable model - rank:  1  i-RMSD:  2.788  Fnat:  0.306  DockQ:  0.385
First medium model     - rank:  7  i-RMSD:  1.148  Fnat:  0.556  DockQ:  0.711
Best model             - rank:  9  i-RMSD:  1.145  Fnat:  0.556  DockQ:  0.713
==============================================
== run1-full//04_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  159  out of  200
Total number of medium or better models:      155  out of  200
Total number of high quality models:          0  out of  200

First acceptable model - rank:  1  i-RMSD:  2.788  Fnat:  0.306  DockQ:  0.385
First medium model     - rank:  7  i-RMSD:  1.148  Fnat:  0.556  DockQ:  0.711
Best model             - rank:  9  i-RMSD:  1.145  Fnat:  0.556  DockQ:  0.713
==============================================
== run1-full//06_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  161  out of  200
Total number of medium or better models:      141  out of  200
Total number of high quality models:          41  out of  200

First acceptable model - rank:  1  i-RMSD:  1.034  Fnat:  0.833  DockQ:  0.827
First medium model     - rank:  1  i-RMSD:  1.034  Fnat:  0.833  DockQ:  0.827
Best model             - rank:  62  i-RMSD:  0.885  Fnat:  0.806  DockQ:  0.841
==============================================
== run1-full//08_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  161  out of  200
Total number of medium or better models:      141  out of  200
Total number of high quality models:          49  out of  200

First acceptable model - rank:  1  i-RMSD:  1.030  Fnat:  0.889  DockQ:  0.846
First medium model     - rank:  1  i-RMSD:  1.030  Fnat:  0.889  DockQ:  0.846
Best model             - rank:  91  i-RMSD:  0.846  Fnat:  0.806  DockQ:  0.843
==============================================
== run1-full//11_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  16  out of  26
Total number of medium or better models:      10  out of  26
Total number of high quality models:          5  out of  26

First acceptable model - rank:  1  i-RMSD:  1.030  Fnat:  0.889  DockQ:  0.846
First medium model     - rank:  1  i-RMSD:  1.030  Fnat:  0.889  DockQ:  0.846
Best model             - rank:  10  i-RMSD:  0.922  Fnat:  0.833  DockQ:  0.841
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


<hr>

#### Contacts analysis

The contactmap analysis module of HADDOCK3 generates for each cluster both a contact matrix of the entire system showing all contacts within a 4.5Å cutoff and a chord chart representation of intermolecular contacts.

In the current workflow we run, those files can be found in the `12_contactmap` directory.
These are again html files with interactive plots (hover with your mouse over the plots).

<a class="prompt prompt-info">
Open in your favorite web browser the _cluster1_rank1_chordchart.html_ file to analyse the intermolecular contacts of the best-ranked cluster.
</a>

This file taken from the pre-computed run can also directly be visualized [**here**](cluster1_rank1_chordchart.html){:target="_blank"}

<a class="prompt prompt-question">
Can you identify which residue(s) make(s) the most intermolecular contacts?
</a>


<hr>

### Analysis scenario 2: 

Let us now analyse the docking results for this scenario, which implements a clustering step after the rigid-body docking stage. 
Use for that either your own run or a pre-calculated run provided in the `runs` directory.

<a class="prompt prompt-info">Look at the log file from the run (e.g. _runs/run2-full/log_)</a>

<a class="prompt prompt-question">How many clusters were generated after the rigid-body docking stage?</a>

<a class="prompt prompt-question">And in how many models this translated for the flexible refinement?</a>

<a class="prompt prompt-question">Considering that the default settings will select a max of 10 models per cluster, how can you explain that the number of models for flexible refinement might be less than 10 times the number of clusters?</a>


Open the `report.html` file found in _analysis/12_caprieval_ (or simply visualize the precalcuted one [**here**](plots/scenario2/report.html){:target="_blank"}

Or go into the _analysis/_caprieval_analysis_  directory of the respective run directory and inspect the final cluster statistics in _capri_clt.tsv_ file

<a class="prompt prompt-info">View the final cluster statistics in _capri_clt.tsv_ file </a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the pre-calculated _caprieval/capri_clt.tsv file</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
cluster_rank    cluster_id      n       under_eval      score   score_std       irmsdirmsd_std        fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std    ilrmsd   ilrmsd_std      air     air_std bsa     bsa_std desolv  desolv_std      elec elec_std total   total_std       vdw     vdw_std caprieval_rank
1       5       10      -       -125.359        4.388   3.086   1.251   0.444   0.243   5.081   1.934   0.486   0.210   5.430   2.196   2.786   1.069        32.048  22.948  1571.068        28.129  -9.514  3.821   -425.572        37.053  -427.459        35.932  -33.935 6.140   1
2       1       10      -       -123.194        8.135   0.981   0.044   0.806   0.028   2.184   0.304   0.814   0.015   1.778   0.162   1.033   0.049        13.946  5.260   1512.048        55.324  -14.070 3.982   -355.866        74.954  -381.265        63.589  -39.345 8.147   2
3       12      9       -       -113.938        3.437   10.571  0.039   0.062   0.012   18.283  0.177   0.087   0.005   17.648  0.108   10.195  0.028        24.749  14.446  1764.635        32.066  -8.174  2.757   -314.484        11.793  -335.077        7.399   -45.342 4.611   3
4       8       10      -       -110.012        6.398   6.667   1.272   0.215   0.041   12.111  2.232   0.204   0.051   11.792  2.259   6.712   1.253        45.220  27.328  1549.892        64.533  -5.661  5.224   -390.860        30.329  -376.341        47.099  -30.701 4.458   4
5       4       10      -       -108.676        5.869   10.499  0.129   0.069   0.014   17.298  0.172   0.095   0.005   17.197  0.207   10.293  0.108        11.946  15.401  1544.793        64.698  -2.523  4.998   -384.582        44.071  -403.067        53.117  -30.431 7.890   5
6       21      4       -       -102.620        23.209  1.649   0.524   0.681   0.140   4.128   1.761   0.654   0.140   3.513   1.386   1.672   0.562        31.928  23.111  1357.930        147.749 -12.666 4.195   -341.057        43.613  -334.063        74.936  -24.935 8.479   6
7       2       10      -       -102.124        1.874   8.709   0.505   0.076   0.053   16.364  0.337   0.106   0.019   15.418  0.657   9.065   0.469        33.207  17.921  1329.695        79.441  -12.247 1.007   -369.341        21.900  -355.464        12.401  -19.329 3.840   7
8       10      10      -       -101.907        3.082   9.371   0.165   0.090   0.012   15.797  0.261   0.113   0.003   16.570  0.220   8.647   0.174        8.097   3.210   1415.988        35.893  -6.841  0.611   -271.088        11.440  -304.651        11.812  -41.658 2.132   8
9       18      5       -       -98.092 5.846   10.738  0.030   0.132   0.023   19.525  0.698   0.104   0.006   17.449  0.101   11.122  0.149   34.083       3.478   1377.390        64.030  -20.159 2.582   -235.614        29.112  -235.750        29.647  -34.219 2.454   9
10      7       10      -       -94.360 4.046   10.858  0.034   0.111   0.028   18.439  0.384   0.102   0.011   17.808  0.240   10.684  0.070   43.394       27.139  1505.900        65.731  -15.427 1.135   -224.854        44.571  -219.762        48.090  -38.302 5.864   10
11      17      5       -       -93.344 2.375   9.295   0.130   0.069   0.014   15.673  0.269   0.107   0.006   15.506  0.175   8.965   0.082   48.231       24.425  1500.330        86.456  -10.426 4.687   -267.404        39.376  -253.434        32.297  -34.260 2.445   11
12      3       10      -       -93.174 2.214   7.066   0.716   0.083   0.056   12.460  1.736   0.151   0.006   13.150  1.720   6.607   0.728   41.548       22.209  1181.820        27.395  -11.433 2.031   -322.491        35.935  -302.340        40.530  -21.397 7.920   12
13      14      8       -       -92.717 9.474   4.740   0.956   0.278   0.115   15.360  3.199   0.211   0.085   11.538  2.537   5.285   0.978   14.441       21.804  1351.725        138.474 -2.305  4.295   -313.494        33.803  -328.210        52.151  -29.157 5.413   13
14      9       10      -       -92.512 2.704   6.006   0.705   0.132   0.030   13.310  1.341   0.162   0.028   11.059  1.234   6.347   0.699   36.390       4.506   1515.135        68.122  -4.445  4.691   -294.152        45.932  -290.638        45.787  -32.876 4.149   14
15      20      4       -       -87.091 14.312  6.080   0.056   0.007   0.012   9.910   0.394   0.163   0.008   12.295  0.666   5.170   0.228   36.574       21.213  1280.060        227.092 3.292   3.601   -354.703        42.910  -341.228        50.728  -23.100 7.777   15
16      19      4       -       -82.561 4.737   10.471  0.203   0.076   0.012   17.850  0.115   0.094   0.004   17.887  0.456   10.255  0.108   57.751       22.350  1456.233        47.296  2.020   3.524   -300.527        60.550  -273.027        45.767  -30.251 8.039   16
17      6       10      -       -78.096 1.276   8.664   0.310   0.097   0.031   14.559  0.423   0.127   0.013   15.264  0.157   8.073   0.465   25.747       19.256  1281.750        84.282  -2.103  3.681   -294.634        35.352  -288.529        15.213  -19.642 7.157   17
18      16      5       -       -77.001 14.086  10.444  0.226   0.083   0.020   18.519  1.216   0.093   0.005   17.777  0.581   9.910   0.296   56.060       14.408  1337.155        124.229 -1.707  3.567   -288.270        51.526  -255.455        68.193  -23.245 6.011   18
19      11      9       -       -71.077 9.704   4.883   0.281   0.125   0.057   10.033  0.449   0.210   0.026   8.851   0.651   4.978   0.290   71.689       25.649  1418.830        120.651 1.831   1.470   -235.329        27.016  -196.651        39.597  -33.011 7.464   19
20      15      6       -       -66.760 4.851   5.334   0.168   0.076   0.030   15.837  0.577   0.125   0.011   13.994  0.395   4.917   0.222   60.002       23.499  1302.927        47.402  -13.791 2.317   -179.987        19.337  -142.957        17.357  -22.972 7.125   20
21      13      8       -       -61.744 6.369   12.082  0.275   0.042   0.014   27.742  2.419   0.048   0.009   23.755  1.443   11.710  0.370   23.892       12.304  988.051 54.474  -1.164  4.633   -215.609        32.195  -211.565        22.347  -19.847 5.152   21
</pre>
</details>
<br>

<a class="prompt prompt-question">How many clusters of acceptable or better quality have been generate according to CAPRI criteria?</a>

<a class="prompt prompt-question">What is the rank of the best cluster generated?</a>

<a class="prompt prompt-question">What is the rank of the first acceptable of better cluster generated?</a>

<a class="prompt prompt-question">How different are the results from scenari1 above?</a>



In this run we also had a `caprieval` after the clustering of the rigid body models (step 5 of our workflow).

<a class="prompt prompt-info">Inspect the corresponding _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the pre-calculated 5_caprieval/capri_clt.tsv file</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
cluster_rank    cluster_id      n       under_eval      score   score_std       irmsdirmsd_std        fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std    ilrmsd   ilrmsd_std      air     air_std bsa     bsa_std desolv  desolv_std      elec elec_std total   total_std       vdw     vdw_std caprieval_rank
1       1       10      -       -32.085 0.532   1.569   0.704   0.493   0.108   3.261   1.920   0.626   0.139   3.239   1.899   1.371   0.630   163.741      5.130   1096.804        147.437 -15.091 1.814   -7.653  0.184   155.025 5.201   -1.064  3.432   1
2       4       10      -       -31.438 0.483   8.377   0.016   0.056   0.000   16.257  0.209   0.100   0.001   15.092  0.021   8.601   0.060   148.614      20.136  1083.170        10.831  -15.943 0.478   -6.143  0.052   141.809 21.538  -0.662  2.474   2
3       15      10      -       -30.142 2.812   8.789   0.367   0.056   0.000   17.178  0.424   0.094   0.003   15.609  0.429   9.206   0.377   85.840       24.724  977.613 55.919  -15.288 2.084   -5.892  1.039   75.478  26.318  -4.470  2.895   3
4       6       10      -       -29.262 0.574   6.284   0.094   0.056   0.000   10.770  0.167   0.164   0.003   11.372  0.164   5.926   0.099   204.351      42.538  895.455 34.659  -13.781 0.500   -8.598  0.913   198.583 48.041  2.830   6.676   4
5       12      10      -       -28.715 1.503   2.121   0.390   0.396   0.084   5.727   1.699   0.478   0.091   4.797   1.005   2.105   0.526   137.121      57.651  968.825 11.297  -12.596 1.112   -7.751  1.194   124.217 59.616  -5.153  4.592   5
6       23      5       -       -28.004 4.467   4.628   0.458   0.229   0.063   8.403   0.719   0.278   0.041   8.665   0.518   4.529   0.513   161.866      85.923  1107.378        53.522  -13.362 3.274   -5.086  0.903   146.704 96.226  -10.075 9.473   6
7       21      5       -       -27.112 0.545   10.707  0.023   0.125   0.014   19.763  0.277   0.100   0.005   17.409  0.037   11.161  0.069   146.469      20.528  1176.923        25.825  -14.032 0.326   -2.641  0.265   130.375 24.933  -13.453 4.243   7
8       2       10      -       -26.081 0.401   4.104   0.017   0.132   0.012   6.997   0.014   0.282   0.004   7.414   0.031   3.802   0.013   203.010      53.514  1010.929        13.658  -10.151 0.339   -7.781  0.182   188.218 54.768  -7.012  1.821   8
9       8       10      -       -24.831 1.483   10.609  0.066   0.049   0.012   18.508  0.445   0.081   0.006   17.736  0.217   10.229  0.081   101.918      63.948  1468.570        21.634  -8.022  0.931   -2.902  0.631   74.945  67.905  -24.071 5.641   9
10      14      10      -       -24.399 0.904   3.597   0.265   0.194   0.028   10.974  1.100   0.241   0.031   9.028   1.060   3.504   0.179   172.370      55.524  1158.146        121.901 -8.674  1.642   -5.801  1.277   159.977 66.010  -6.592  13.112  10
11      29      4       -       -24.070 1.736   8.664   0.807   0.042   0.014   18.290  1.080   0.083   0.012   15.566  1.230   9.000   0.716   448.512      126.983 988.570 106.410 -15.921 1.758   -2.762  0.407   447.092 130.529 1.341   9.436   11
12      3       10      -       -23.463 0.229   9.482   0.023   0.042   0.014   16.322  0.193   0.093   0.006   16.966  0.097   8.758   0.032   81.551       31.696  1141.702        19.289  -6.834  0.710   -5.973  0.141   70.159  34.564  -5.420  3.678   12
13      13      10      -       -23.357 1.305   7.302   0.161   0.139   0.020   12.910  0.299   0.161   0.007   13.105  0.169   7.214   0.205   268.147      121.404 1077.705        35.823  -5.623  0.736   -9.544  0.692   249.265 124.014 -9.337  5.642   13
14      20      5       -       -22.594 1.264   7.723   0.244   0.118   0.023   13.916  0.288   0.142   0.010   14.340  0.222   7.376   0.276   432.674      31.549  989.278 44.144  -9.032  1.016   -7.950  1.887   420.099 29.336  -4.625  4.581   14
15      18      10      -       -22.191 0.304   2.210   0.013   0.389   0.000   5.406   0.090   0.472   0.003   4.211   0.040   2.239   0.015   216.113      76.283  1131.940        15.150  -9.207  0.756   -3.663  0.095   196.226 79.057  -16.224 2.900   15
16      19      8       -       -21.866 0.498   10.867  0.021   0.090   0.012   18.900  0.121   0.092   0.005   18.103  0.072   10.696  0.013   163.911      67.272  1237.880        14.530  -10.461 0.439   -0.507  0.298   147.611 70.977  -15.793 5.107   16
17      17      10      -       -21.465 0.810   10.809  0.003   0.104   0.012   17.715  0.028   0.103   0.004   17.457  0.009   10.547  0.005   316.134      69.551  1366.262        24.712  -8.579  0.766   -2.305  0.238   305.960 72.442  -7.869  3.101   17
18      10      10      -       -21.031 0.307   5.682   0.108   0.083   0.083   17.768  1.211   0.112   0.020   14.388  0.256   5.741   0.641   148.855      92.373  1134.628        103.961 -5.281  3.162   -5.798  1.240   133.714 104.088 -9.343  10.550  18
19      7       10      -       -20.282 0.894   9.722   0.476   0.062   0.012   17.085  0.299   0.095   0.004   16.129  0.681   9.743   0.390   381.512      124.204 980.973 112.048 -6.725  1.139   -7.554  1.319   373.060 129.037 -0.898  6.137   19
20      24      5       -       -20.203 5.838   10.712  0.035   0.076   0.012   17.941  0.233   0.093   0.005   18.116  0.568   10.510  0.225   276.084      112.917 1081.205        117.863 -8.239  5.353   -3.851  1.334   266.101 114.799 -6.132  2.624   20
21      25      5       -       -17.992 4.221   9.166   0.204   0.056   0.000   15.726  0.889   0.103   0.007   15.404  0.312   8.899   0.282   318.210      136.576 1167.855        99.445  -6.764  3.757   -2.752  0.201   317.481 138.114 2.022   3.315   21
22      11      10      -       -14.627 2.778   11.930  0.214   0.035   0.012   26.403  0.784   0.048   0.006   22.691  0.873   11.695  0.143   108.4
65      73.961  883.253 62.138  -1.452  4.869   -5.347  2.179   95.114  84.827  -8.003  8.865   22
23      28      4       -       -13.956 1.434   9.248   0.062   0.069   0.014   15.172  0.121   0.111   0.006   15.871  0.037   8.812   0.087   333.032      163.288 900.703 18.410  -0.566  0.668   -7.739  0.067   327.877 173.691 2.584   10.899  23
24      5       10      -       -13.809 0.940   5.941   0.121   0.083   0.000   13.604  0.335   0.141   0.004   11.115  0.156   6.271   0.156   181.681      73.025  1115.750        29.267  0.965   2.118   -5.370  2.346   169.975 73.043  -6.336  1.947   24
25      22      5       -       -12.560 1.188   10.407  0.126   0.083   0.000   18.541  0.854   0.093   0.004   17.759  0.339   9.907   0.197   251.455      15.438  1063.331        79.801  -2.378  0.427   -2.031  0.309   246.143 17.820  -3.281  3.034   25
26      26      4       -       -11.288 1.665   6.107   0.030   0.000   0.000   9.984   0.158   0.159   0.003   12.762  0.154   4.959   0.028   285.194      179.389 981.991 27.029  2.056   0.255   -6.272  0.330   268.549 186.322 -10.373 7.384   26
27      16      10      -       -10.737 1.179   5.226   0.141   0.069   0.057   9.703   0.339   0.193   0.026   9.735   0.288   4.973   0.112   215.948      101.338 1188.425        107.307 4.567   1.022   -5.409  0.184   193.521 103.680 -17.019 3.000   27
28      9       10      -       -10.587 0.423   8.494   0.025   0.056   0.000   14.509  0.082   0.114   0.001   15.302  0.056   7.869   0.027   226.991      58.991  1067.017        22.014  4.837   0.263   -6.980  0.109   215.655 60.210  -4.356  1.585   28
29      27      4       -       -6.631  1.611   10.456  0.170   0.069   0.014   17.544  0.127   0.093   0.004   17.767  0.300   10.166  0.093   341.261      67.134  1170.100        84.016  7.085   2.274   -5.380  1.321   331.044 71.652  -4.837  6.069   29
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


<hr>
<hr>

## Visualisation of the models


We will now visualise the generated models. For this go for example to `runs/run1-full/10_seletopclusts/`. This directory contains the top10 models of each cluster.
For visualisation we can load in PyMol the best model of each cluseter (the ones ending with `_1.pdb`). By default the PDB files will be gzipped. 
PyMol should be able to directly read those.
In order to compare the various clusters we will however download the models and inspect them using PyMol.


Then start PyMOL and load each cluster representative:

<a class="prompt prompt-pymol">File menu -> Open -> select cluster_1_model_1.pdb.gz</a>

Repeat this for each cluster. 

Alternatively you could start PyMol from the command line (if available) and load all models at once:

<a class="prompt prompt-cmd">
pymol *_1.pdb.gz
</a>

Once all files have been loaded, type in the PyMOL command window:

<a class="prompt prompt-pymol">
show cartoon<br>
util.cbc<br>
hide lines<br>
</a>

Let's then superimpose all models on chain A of the first cluster:

<a class="prompt prompt-pymol">
select cluster_1_model_1 and chain A<br>
alignto sele<br>
</a>

This will align all clusters on chain A (E2A), maximizing the differences in the orientation of chain B (HPR).

<a class="prompt prompt-question">
Examine the various clusters. How does the orientation of HPR differ between them?
</a>

**Note:** You can turn on and off a cluster by clicking on its name in the right panel of the PyMOL window.

Let's now check if the active residues which we defined are actually part of the interface. In the PyMOL command window type:

<a class="prompt prompt-pymol">
select e2a_active, (resi 38,40,45,46,69,71,78,80,94,96,141) and chain A<br>
select hpr_active, (resi 15,16,17,20,48,49,51,52,54,56) and chain B<br>
color red, e2a_active<br>
color orange, hpr_active<br>
</a>

<a class="prompt prompt-question">
Are the active residues in the interface?
</a>


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
<img width="50%" src="/education/HADDOCK3/HADDOCK3-protein-protein/phosphorylated-histidine.png">
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

**_Note_** that based on the CAPRI analysis output discussed previously you should already know the answer to these questions.
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
