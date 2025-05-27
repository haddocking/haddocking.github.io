---
layout: page
title: "Antibody-antigen modelling tutorial using a local version of HADDOCK3"
excerpt: "A tutorial describing the use of HADDOCK3 in the low-sampling scenario to model an antibody-antigen complex"
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, sampling]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>
<hr>

## Introduction

This tutorial demonstrates the use of the new modular HADDOCK3 version for predicting
the structure of an antibody-antigen complex using knowledge of the hypervariable loops
on the antibody (i.e., the most basic knowledge) and epitope information identified from NMR experiments for the antigen to guide the docking.

An antibody is a large protein that generally works by attaching itself to an antigen,
which is a unique site of the pathogen. The binding harnesses the immune system to directly
attack and destroy the pathogen. Antibodies can be highly specific while showing low immunogenicity (i.e. the ability to provoke an immune response),
which is achieved by their unique structure. **The fragment crystallizable region (Fc region)**
activates the immune response and is species-specific, i.e. the human Fc region should not
induce an immune response in humans. **The fragment antigen-binding region (Fab region**)
needs to be highly variable to be able to bind to antigens of various nature (high specificity).
In this tutorial, we will concentrate on the terminal **variable domain (Fv)** of the Fab region.

<figure style="text-align: center;">
  <img src="/education/HADDOCK3/HADDOCK3-antibody-antigen/antibody_described.png">
</figure>

The small part of the Fab region that binds the antigen is called **paratope**. The part of the antigen
that binds to an antibody is called **epitope**. The paratope consists of six highly flexible loops,
known as **complementarity-determining regions (CDRs)** or hypervariable loops whose sequence
and conformation are altered to bind to different antigens. CDRs are shown in red in the figure below:

<figure style="text-align: center;">
  <img src="/education/HADDOCK3/HADDOCK3-antibody-antigen/CDRs.png">
</figure>

In this tutorial we will be working with Interleukin-1β (IL-1β)
(PDB code [4I1B](https://www.ebi.ac.uk/pdbe/entry/pdb/4i1b){:target="_blank"}) as an antigen
and its highly specific monoclonal antibody gevokizumab
(PDB code [4G6K](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k){:target="_blank"})
(PDB code of the complex [4G6M](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6m){:target="_blank"}).


Throughout the tutorial, colored text will be used to refer to questions or
instructions, and/or PyMOL commands.

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
wget https://surfdrive.surf.nl/files/index.php/s/MuC8YogNPj9Ac31/download -O HADDOCK3-antibody-antigen.zip<br>
unzip HADDOCK3-antibody-antigen.zip
</a>


Unziping the file will create the `HADDOCK3-antibody-antigen` directory which should contain the following directories and files:

* `pdbs`: a directory containing the pre-processed PDB files
* `restraints`: a directory containing the interface information and the corresponding restraint files for HADDOCK3
* `runs`: a directory containing pre-calculated results
* `scripts`: a directory containing various scripts used in this tutorial
* `workflows`: a directory containing configuration file examples for HADDOCK3

In case of a workshop of course, HADDOCK3 will usually have been installed on the system you will be using.

It this is not the case, you will have to install it yourself. To obtain and install HADDOCK3, navigate to [its repository][haddock-repo], fill the
registration form, and then follow the instructions under the **Local setup (on your own)** section below.

This tutorial was last tested using HADDOCK3 version 2024.10.0b7. The provided pre-calculated runs were obtained on a Macbook Pro M2 processors with as OS Sequoia 15.3.1.



<hr>

### BioExcel HPC workshop, Sofia May 2025

We will be making use of the [Discoverer HPC CPU cluster](https://docs.discoverer.bg){:target="_blank"} for this tutorial. 
The software and data required for this tutorial have been pre-installed.
Please connect to the system using your credentials as instructed.

In order to run the tutorial, go into you scratch directory, then unzip the required data:

<a class="prompt prompt-cmd">
cd /discofs/\<my\-username\><br>
unzip /valhalla/projects/school-01/HADDOCK/HADDOCK3-antibody-antigen.zip<br>
cd HADDOCK3-antibody-antigen
</a>

This will create the `HADDOCK3-antibody-antigen` directory with all necessary data and scripts and job examples ready for submission to the batch system.

HADDOCK3 is part of the standard software supported on discoverer. To activate the HADDOCK3 environment load the following modules:


<a class="prompt prompt-cmd">
module load python/3/3.12<br>
module load haddock3/2025.5.0
</a>

You can then test that `haddock3` is indeed accessible with:

<a class="prompt prompt-cmd">
haddock3 -h
</a>

You should see a small help message explaining how to use the software.

<details style="background-color:#DAE4E7">
  <summary>
  <i>View output</i><i class="material-icons">expand_more</i>
 </summary>
<pre>
(haddock3)$ haddock3 -h
usage: haddock3 [-h] [--restart RESTART] [--extend-run EXTEND_RUN] [--setup]
                [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-v]
                recipe

positional arguments:
  recipe                The input recipe file path

optional arguments:
  -h, --help            show this help message and exit
  --restart RESTART     Restart the run from a given step. Previous folders from the
                        selected step onward will be deleted.
  --extend-run EXTEND_RUN
                        Start a run from a run directory previously prepared with the
                        `haddock3-copy` CLI. Provide the run directory created with
                        `haddock3-copy` CLI.
  --setup               Only setup the run, do not execute
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
  -v, --version         show version
</pre>
</details>
<br>

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

In this section we will prepare the PDB files of the antibody and antigen for docking.
Crystal structures of both the antibody and the antigen in their free forms are available from the
[PDBe database](https://www.pdbe.org){:target="_blank"}. 

*__Important:__ For a docking run with HADDOCK, each molecule should consist of a single chain with non-overlapping residue numbering within the same chain.

As an antibody consists of two chains (L+H), we will have to prepare it for use in HADDOCK. For this we will be making use of `pdb-tools` from the command line.

_**Note**_ that `pdb-tools` is also available as a [web service](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.


<hr>

### Preparing the antibody structure

Using PDB-tools we will download the unbound structure of the antibody from the PDB database (the PDB ID is [4G6K](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k){:target="_blank"}) 
and then process it to have a unique chain ID (A) and non-overlapping residue numbering by renumbering the merged pdb (starting from 1). For this we will concatenate the following PDB-tools commands:

1. fetch the PDB entry from the PDB database (`pdb_fetch`)
2. clean the PDB file (`pdb_tidy`)
3. select the chain (`pdb_selchain`),
4. remove any hetero atoms from the structure (e.g. crystal waters, small molecules from the crystallisation buffer and such) (`pdb_delhetatm`),
5. fix residue numbering insertion in the HV loops (often occuring in antibodies - see note below) (`pdb_fixinsert`)
6. remove any possible side-chain duplication (can be present in high-resolution crystal structures in case of multiple conformations of some side chains) (`pdb_selaltloc`)
7. keep only the coordinates lines (`pdb_keepcoord`),
8. select only the variable domain (FV) of the antibody (to reduce computing time) (`pdb_selres`)
9. clean the PDB file (`pdb_tidy`)

**_Note_** that the `pdb_tidy -strict` commands cleans the PDB file, add TER statements only between different chains). 
Without the -strict option TER statements would be added between each chain break (e.g. missing residues), which should be avoided.

**_Note_**: An important part for antibodies is the `pdb_fixinsert` command that fixes the residue numbering of the HV loops: 
Antibodies often follow the [Chothia numbering scheme](https://pubmed.ncbi.nlm.nih.gov/9367782/?otool=inluulib){:target="_blank"} 
and insertions created by this numbering scheme (e.g. 82A, 82B, 82C) cannot be processed by HADDOCK directly 
(if not done those residues will not be considered resulting effectively in a break in the loop).
As such, renumbering is necessary before starting the docking. 


This can be done from the command line with:

<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy \-strict | pdb_selchain \-H | pdb_delhetatm | pdb_fixinsert | pdb_selaltloc | pdb_keepcoord | pdb_selres \-1:120 | pdb_tidy -strict > 4G6K_H.pdb
</a>
<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy \-strict | pdb_selchain -L | pdb_delhetatm | pdb_fixinsert | pdb_selaltloc | pdb_keepcoord | pdb_selres \-1:107 | pdb_tidy \-strict > 4G6K_L.pdb
</a>

We then combined the heavy and light chain into one, renumbering the residues starting at 1 to avoid overlap in residue numbering between the chains and assigning a unique chainID/segID:

<a class="prompt prompt-cmd">
pdb_merge 4G6K_H.pdb 4G6K_L.pdb | pdb_reres \-1 | pdb_chain \-A | pdb_chainxseg | pdb_tidy \-strict > 4G6K_clean.pdb
</a>

_**Note**_ The ready-to-use file can be found in the `pdbs` directory of the provided tutorial data.


<hr>

### Preparing the antigen structure

Using PDB-tools, we will now download the unbound structure of Interleukin-1β from the PDB database (the PDB ID is [4I1B](https://www.ebi.ac.uk/pdbe/entry/pdb/4i1b){:target="_blank"}), 
remove the hetero atoms and then process it to assign it chainID B.

*__Important__: Each molecule given to HADDOCK in a docking scenario must have a unique chainID/segID.*

<a class="prompt prompt-cmd">
pdb_fetch 4I1B | pdb_tidy \-strict | pdb_delhetatm  | pdb_selaltloc | pdb_keepcoord | pdb_chain \-B | pdb_chainxseg | pdb_tidy \-strict > 4I1B_clean.pdb
</a>


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

### Identifying the paratope of the antibody

Nowadays several computational tools can identify the paratope (the residues of the hypervariable loops involved in binding) from the provided antibody sequence.
In this tutorial, we are providing you with the corresponding list of residue obtained using [ProABC-2](https://github.com/haddocking/proabc-2){:target="_blank"}.
ProABC-2 uses a convolutional neural network to identify not only residues which are located in the paratope region 
but also the nature of interactions they are most likely involved in (hydrophobic or hydrophilic).
The work is described in [Ambrosetti, *et al* Bioinformatics, 2020](https://academic.oup.com/bioinformatics/article/36/20/5107/5873593){:target="_blank"}.

The corresponding paratope residues (those with either an overall probability >= 0.4 or a probability for hydrophobic or hydrophilic > 0.3) are:

<pre style="background-color:#DAE4E7">
31,32,33,34,35,52,54,55,56,100,101,102,103,104,105,106,151,152,169,170,173,211,212,213,214,216
</pre>

The numbering corresponds to the numbering of the `4G6K_clean.pdb` PDB file.

Let us visualize those onto the 3D structure.
For this start PyMOL and load `4G6K_clean.pdb`

<a class="prompt prompt-pymol">
File menu -> Open -> select 4G6K_clean.pdb
</a>

Alternatively, if PyMOL is accessible from the command line, simply type:

<a class="prompt prompt-cmd">
pymol 4G6K_clean.pdb
</a>

We will now highlight the predicted paratope residues in red. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all<br>
select paratope, (resi 31+32+33+34+35+52+54+55+56+100+101+102+103+104+105+106+151+152+169+170+173+211+212+213+214+216)<br>
color red, paratope<br>
</a>

<a class="prompt prompt-question">
Can you identify the H3 loop? H stands for heavy chain (the first domain in our case with lower residue numbering). H3 is typically the longest loop.
</a>

Let us now switch to a surface representation to inspect the predicted binding site.

<a class="prompt prompt-pymol">
show surface<br>
</a>

Inspect the surface.

<a class="prompt prompt-question">
Do the identified paratope residues form a well-defined patch on the surface?
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See surface view of the paratope</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="60%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/antibody-paratope.png">
  </figure>
  <br>
</details>

<hr>

### Identifying the epitope of the antigen

The article describing the crystal structure of the antibody-antigen complex we are modeling also reports experimental NMR chemical shift titration experiments 
to map the binding site of the antibody (gevokizumab) on Interleukin-1β.
The residues affected by binding are listed in Table 5 of [Blech et al. JMB 2013](https://dx.doi.org/10.1016/j.jmb.2012.09.021){:target="_blank"}:

<figure style="text-align: center;">
  <img width="60%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/Table5-Blech.png">
</figure>

The list of binding site (epitope) residues identified by NMR is:

<pre style="background-color:#DAE4E7">
72,73,74,75,81,83,84,89,90,92,94,96,97,98,115,116,117
</pre>

We will now visualize the epitope on Interleukin-1β.
To do this, start PyMOL and open the provided PDB file of the antigen from the PyMOL File menu.

<a class="prompt prompt-pymol">
File menu -> Open -> select 4I1B_clean.pdb
</a>

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select epitope, (resi 72+73+74+75+81+83+84+89+90+92+94+96+97+98+115+116+117)<br>
color red, epitope<br>
</a>

Inspect the surface.

<a class="prompt prompt-question">
Do the identified residues form a well-defined patch on the surface?
</a>

The answer to that question should be yes, but we can see some residues not colored that might also be involved in the binding - there are some white spots around/in the red surface.

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See surface view of the epitope identified by NMR</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="60%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/antigen-epitope.png">
  </figure>
  <br>
</details>

<br>

In HADDOCK, we are dealing with potentially incomplete binding sites by defining surface neighbors as `passive` residues.
These passive residues are added in the definition of the interface but do not incur any energetic penalty if they are not part of the binding site in the final models. 
In contrast, residues defined as active (typically the identified or predicted binding site residues) will incur an energetic penalty.
When using the HADDOCK2.x webserver, `passive` residues will be automatically defined.
Here, since we are using a local version, we need to define those manually.

This can easily be done using a haddock3 command line tool in the following way:

<a class="prompt prompt-cmd">
haddock3-restraints passive_from_active 4I1B_clean.pdb 72,73,74,75,81,83,84,89,90,92,94,96,97,98,115,116,117
</a>

The command prints a list of solvent accessible passive residues, which you should save to a file for further use.

We can visualize the epitope and its surface neighbors using PyMOL:

<a class="prompt prompt-pymol">
File menu -> Open -> select 4I1B_clean.pdb
</a>

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select epitope, (resi 72+73+74+75+81+83+84+89+90+92+94+96+97+98+115+116+117)<br>
color red, epitope<br>
select passive, (resi 3+24+46+47+48+50+66+76+77+79+80+82+86+87+88+91+93+95+118+119+120)<br>
color green, passive<br>
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See the epitope and passive residues</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="60%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/antigen-active-passive.png">
  </figure>
  <br>
</details>
<br>

The NMR-identified residues and their surface neighbors generated with the above command can be used to define ambiguous interactions restraints, 
either using the NMR identified residues as active in HADDOCK, or combining those with the surface neighbors. 

The difference between `active` and `passive` residues in HADDOCK is as follows:

*__Active residues__*: These residues are "forced" to be at the interface. If they are not part of the interface in the final models, an energetic penalty will be applied. The interface in this context is defined by the union of active and passive residues on the partner molecules.

*__Passive residues__*: These residues are expected to be at the interface. However, if they are not, no energetic penalty is applied.


In general, it is better to be too generous rather than too strict in the definition of passive residues.
An important aspect is to filter both the active (the residues identified from your mapping experiment) and passive residues by their solvent accessibility.
This is done automatically when using the `haddock3-restraints passive_from_active` command: residues with less that 15% relative solvent accessibility (same cutoff as the default in the HADDOCK server) are discared.
This is, however, not a hard limit, and you might consider including even more buried residues if some important chemical group seems solvent accessible from a visual inspection.


<hr>

### Defining ambiguous restraints

Once you have identified your active and passive residues for both molecules, you can proceed with the generation of the ambiguous interaction restraints (AIR) file for HADDOCK.
For this you can either make use of our online [GenTBL][gentbl] web service, entering the list of active and passive residues for each molecule, 
the chainIDs of each molecule and saving the resulting restraint list to a text file, or use another `haddock3-restraints` sub-command.

To use our `haddock3-restraints active_passive_to_ambig` script, you need to
create for each molecule a file containing two lines:

* The first line corresponds to the list of active residues (numbers separated by spaces)
* The second line corresponds to the list of passive residues (numbers separated by spaces).

*__Important__*: The file must consist of two lines, but a line can be empty (e.g., if you do not want to define active residues for one molecule). 
However, there must be at least one set of active residue defined for one of the molecules.


* For the antibody we will use the predicted paratope as active and no passive residues defined. 
The corresponding file can be found in the `restraints` directory as `antibody-paratope.act-pass`:

<pre style="background-color:#DAE4E7">
1 32 33 34 35 52 54 55 56 100 101 102 103 104 105 106 151 152 169 170 173 211 212 213 214 216

</pre>

* For the antigen we will use the NMR-identified epitope as active and the surface neighbors as passive. 
The corresponding file can be found in the `restraints` directory as `antigen-NMR-epitope.act-pass`:

<pre style="background-color:#DAE4E7">
72 73 74 75 81 83 84 89 90 92 94 96 97 98 115 116 117
3 24 46 47 48 50 66 76 77 79 80 82 86 87 88 91 93 95 118 119 120
</pre>

Using those two files, we can generate the CNS-formatted Ambiguous Interaction Restraints (AIRs) file with the following command:

<a class="prompt prompt-cmd">
haddock3-restraints active_passive_to_ambig ./restraints/antibody-paratope.act-pass ./restraints/antigen-NMR-epitope.act-pass \-\-segid-one A \-\-segid-two B > ambig-paratope-NMR-epitope.tbl
</a>

This generates a file called `ambig-paratope-NMR-epitope.tbl` that contains the AIRs. 

<a class="prompt prompt-question">
Inspect the generated file and note how the ambiguous distances are defined.
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>View an extract of the AIR file</i></b> <i class="material-icons">expand_more</i>
  </summary>
<pre>
assign (resi 31 and segid A)
(
       (resi 72 and segid B)
        or
       (resi 73 and segid B)
        or
       (resi 74 and segid B)
        or
       (resi 75 and segid B)
        or
       (resi 81 and segid B)
        or
       (resi 83 and segid B)
        or
       (resi 84 and segid B)
        or
       (resi 89 and segid B)
        or
       (resi 90 and segid B)
        or
       (resi 92 and segid B)
        or
       (resi 94 and segid B)
        or
       (resi 96 and segid B)
        or
       (resi 97 and segid B)
        or
       (resi 98 and segid B)
        or
       (resi 115 and segid B)
        or
       (resi 116 and segid B)
        or
       (resi 117 and segid B)
        or
       (resi 3 and segid B)
        or
       (resi 24 and segid B)
        or
       (resi 46 and segid B)
        or
       (resi 47 and segid B)
        or
       (resi 48 and segid B)
        or
       (resi 50 and segid B)
        or
       (resi 66 and segid B)
        or
       (resi 76 and segid B)
        or
       (resi 77 and segid B)
        or
       (resi 79 and segid B)
        or
       (resi 80 and segid B)
        or
       (resi 82 and segid B)
        or
       (resi 86 and segid B)
        or
       (resi 87 and segid B)
        or
       (resi 88 and segid B)
        or
       (resi 91 and segid B)
        or
       (resi 93 and segid B)
        or
       (resi 95 and segid B)
        or
       (resi 118 and segid B)
        or
       (resi 119 and segid B)
        or
       (resi 120 and segid B)
) 2.0 2.0 0.0
...
</pre>
  <br>
</details>
<br>

<a class="prompt prompt-question">
Refering to the way the distance restraints are defined (see above), what is the distance range for the ambiguous distance restraints?
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See answer</i></b> <i class="material-icons">expand_more</i>
  </summary>
The default distance range for those is between 0 and 2Å, which 
might seem short but makes senses because of the 1/r^6 summation in the AIR
energy function that makes the effective distance to be significantly shorter than
the shortest distance entering the sum.
<br>
<br>
The effective distance is calculated as the SUM over all pairwise atom-atom
distance combinations between an active residue and all the active+passive on
the other molecule: SUM[1/r^6]^(-1/6).
</details>
<br>


<hr>

### Restraints validation

If you modify manually this generated restraint files or create your own, it is possible to quickly check if the format is valid using the following `haddock3-restraints` sub-command:

<a class="prompt prompt-cmd">
haddock3-restraints validate_tbl ambig-paratope-NMR-epitope.tbl \-\-silent
</a>

No output means that your TBL file is valid.

*__Note__* that this only validates the syntax of the restraint file, but does not check if the selections defined in the restraints are actually existing in your input PDB files.


<hr>

### Additional restraints for multi-chain proteins

As an antibody consists of two separate chains, it is important to define a few distance restraints
to keep them together during the high temperature flexible refinement stage of HADDOCK otherwise they might slightly drift appart. 
This can easily be done using the `haddock3-restraints restrain_bodies` sub-command.

<a class="prompt prompt-cmd">
haddock3-restraints restrain_bodies 4G6K_clean.pdb > antibody-unambig.tbl
</a>

The result file contains two CA-CA distance restraints with the exact distance measured between two randomly picked CA atoms pairs:

<pre style="background-color:#DAE4E7">
  assign (segid A and resi 110 and name CA) (segid A and resi 132 and name CA) 26.326 0.0 0.0
  assign (segid A and resi 97 and name CA) (segid A and resi 204 and name CA) 19.352 0.0 0.0
</pre>

This file is also provided in the `restraints` directory.


<hr>
<hr>

## Setting up and running the docking with HADDOCK3

Now that we have all required files at hand (PDB and restraints files), it is time to setup our docking protocol. 
In this tutorial, considering we have rather good information about the paratope and epitope, we will execute a fast HADDOCK3 docking workflow, 
reducing the non-negligible computational cost of HADDOCK by decreasing the sampling, without impacting too much the accuracy of the resulting models.



<hr>

### HADDOCK3 workflow definition

The first step is to create a HADDOCK3 configuration file that will define the docking workflow. 
We will follow a classic HADDOCK workflow consisting of rigid body docking, semi-flexible refinement and final energy minimisation followed by clustering.

We will also integrate two analysis modules in our workflow: 

- `caprieval` will be used at various stages to compare models to either the best scoring model (if no reference is given) or a reference structure, which in our case we have at hand (`pdbs/4G6M_matched.pdb`). This will directly allow us to assess the performance of the protocol. In the absence of a reference, `caprieval` is still usefull to assess the convergence of a run and analyse the results. 
- `contactmap` added as last module will generate contact matrices of both intra- and intermolecular contacts and a chordchart of intermolecular contacts for each cluster.


Our workflow consists of the following modules:

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
11. **`caprieval`**
12. **`contactmap`**: *Contacts matrix and a chordchart of intermolecular contacts*


The corresponding toml configuration file (provided in `workflows/docking-antibody-antigen.cfg`) looks like:

{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen 
# ====================================================================

# Directory in which the scoring will be done
run_dir = "run1"

# Compute mode
mode = "local"
ncores = 50

# Self contained rundir (to avoid problems with long filename paths)
self_contained = true

# Post-processing to generate statistics and plots
postprocess = true
clean = true

molecules =  [
    "pdbs/4G6K_clean.pdb",
    "pdbs/4I1B_clean.pdb"
    ]

# ====================================================================
# Parameters for each stage are defined below, prefer full paths
# ====================================================================
[topoaa]

[rigidbody]
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
# Reduced sampling (100 instead of the default of 1000)
sampling = 100

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[seletop]
# Selection of the top 50 best scoring complexes (instead of the default of 200)
select = 50

[flexref]
tolerance = 5
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[emref]
tolerance = 5
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[clustfcc]
plot_matrix = true

[seletopclusts]
# Selection of the top 4 best scoring complexes from each cluster
top_models = 4

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[contactmap]

# ====================================================================

{% endhighlight %}


In this case, since we have information for both interfaces we use a low-sampling configuration file, which takes only a small amount of computational resources to run. 
The initial `sampling` parameter at the rigid-body energy minimization (`rigidbody`) module is set to 100 models, of which only best the 40 are passed to the flexible refinement (`flexref`) module with the `seletop` module.
The subsequence flexible refinement (`flexref` module) and energy minimisation (*emref*) modules will use all models passed by the *seletop* module.
FCC clustering (`clustfcc`) is then applied to group together models sharing a consistent fraction of the interface contacts.
The top 4 models of each cluster are saved to disk (`seletopclusts`).

Multiple `caprieval` modules are executed at different stages of the workflow to check how the quality (and rankings) of the models change throughout the protocol. 
In this case we are providing the known crystal structure of the complex as reference.


**_Note_**: For making best use of the available CPU resources it is recommended to adapt the sampling parameter to be a multiple of the number of available cores when running in local mode. For this reason, for the ASEAN HPC school the sampling is set to be a multiple of 48.

**_Note_**: In case no reference is available (the usual scenario), the best ranked model is used as reference for each stage.
Including `caprieval` at the various stages even when no reference is provided is useful to get the rankings and scores and visualise the results (see Analysis section below).

**_Note_**: The default sampling would be 1000 models for `rigidbody` of which 200 are passed to the flexible refinement in `seletop`. 
As an indication of the computational requirements, the default sampling worflow for this tutorial completes in about 37min using 12 cores on a MaxOSX M2 processor.
In comparison, the reduced sampling run (100/40) takes about 7-8min.



**_Note_**: To get a list of all possible parameters that can be defined in a specific module (and their default values) you can use the following command:

<a class="prompt prompt-cmd">
haddock3-cfg -m \<module\-name\>
</a>

Add the `-d` option to get a more detailed description of parameters and use the `-h` option to see a list of arguments and options.

<a class="prompt prompt-question">
In the above workflow we see in three modules a *tolerance* parameter defined. Using the *haddock3-cfg* command try to figure out what this parameter does.
</a>


*__Note__* that, in contrast to HADDOCK2.X, we have much more flexibility in defining our workflow.
As an example, we could use this flexibility by introducing a clustering step after the initial rigid-body docking stage, selecting a given number of models per cluster and refining all of those.
For an example of this strategy see the  4 section about ensemble docking.


<hr>

### Running HADDOCK3

In in the first section of the workflow above we have a parameter `mode` defining the execution mode. HADDOCK3 currently supports three difference execution modes:

- **local** : In this mode, HADDOCK3 will run on the current system, using the defined number of cores (`ncores`) in the config file to a maximum of the total number of available cores on the system.
- **batch**: In this mode, HADDOCK3 will typically be started on your local server (e.g. the login node) and will dispatch jobs to the batch system of your cluster (slurm and torque are currently supported).
- **mpi**: HADDOCK3 also supports a pseudo parallel MPI implementation, which allows to harvest the power of multiple nodes to distribute the computations (functional but still very experimental at this stage).


<hr>

#### Execution of HADDOCK3 on DISCOVERER (BioExcel Sofia May 2025 workshop)

To execute the HADDOCK3 workflow on the computational resources provided for this workshop, 
you should create an execution script contain specific requirements for the queueing system and the HADDOCK3 configuration and execution. 
An example slurm script is provided with the data you unzipped:

{% highlight shell %}
run-haddock3-discoverer.sh
{% endhighlight %}


Here is an example of such an execution script (also provided in the `HADDOCK3-antibody-antigen` directory as `run-haddock3-discoverer.sh`):

{% highlight shell %}
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --account=school-01
#SBATCH --qos=school-01
#SBATCH --job-name "haddock3"
#SBATCH --tasks-per-node=50
#SBATCH --mem-per-cpu 1500
#SBATCH --time 04:00:00

module load python/3/3.12
module load haddock3/2025.5.0
haddock3 workflows/docking-antibody-antigen.cfg

{% endhighlight %}

This file should be submitted to the batch system using the `sbatch` command:

<a class="prompt prompt-cmd">
sbatch run-haddock3-discoverer.sh
</a>

And you can check the status in the queue using the `squeue`command.

This example run should take about 7 minutes to complete on a single node using 50 cores.


<hr>

#### Execution of HADDOCK3 on the TRUBA resources (EuroCC Istanbul April 2024 workshop)

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View execution instructions for running HADDOCK3 the TRUBA resources</i> <i class="material-icons">expand_more</i>
  </summary>

To execute the HADDOCK3 workflow on the computational resources provided for this workshop, 
you should create an execution script contain specific requirements for the queueing system and the HADDOCK3 configuration and execution. 
Two scripts are provided with the data you unzipped, one for execution on the hamsri cluster and one for the barbun cluster:

{% highlight shell %}
run-haddock3-barbun.sh
run-haddock3-hamsri.sh
{% endhighlight %}

Here is an example of such an execution script (also provided in the <i>HADDOCK3-antibody-antigen</i> directory as <i>run-haddock3-hamsri.sh</i>):
  
{% highlight shell %}
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=54
#SBATCH -C weka
#SBATCH -p hamsi
#SBATCH --time 00:30:00

source ~egitim/HADDOCK/haddock3/.venv/bin/activate
haddock3 workflows/docking-antibody-antigen.cfg
{% endhighlight %}

This file should be submitted to the batch system using the <i>sbatch</i> command:

{% highlight shell %}
sbatch run-haddock3-hamsri.sh
{% endhighlight %}

<b><i>Note</i></b> that batch submission is only possible from the <i>scratch</i> partition (<i>/arf/scratch/my-home-directory</i>)

And you can check the status in the queue using the <i>squeue</i>command.

This example run should take about 7 minutes to complete on a single node using 50 cores.

</details>


<hr>

#### Execution of HADDOCK3 on Fugaku (ASEAN 2025 HPC school)

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View execution instructions for running HADDOCK3 on Fugaku</i> <i class="material-icons">expand_more</i>
  </summary>

To execute the workflow on Fugaku, you can either start an interactive session or create a job file that will execute HADDOCK3 on a node, 
with HADDOCK3 running in local mode (the setup in the above configuration file with <i>mode="local"</i>) and harvesting all core of that node (<i>ncores=48</i>).
<br>
<br>
<b>Interactive session on a node:</b>
<br>
{% highlight shell %}
pjsub --interact -L "node=1" -L "rscgrp=int" -L "elapse=2:00:00"  --sparam "wait-time=600"  -g hp240465 -x PJM_LLIO_GFSCACHE=/vol0006:/vol0004
{% endhighlight %}

Once the session is active, activate HADDOCK3 with:

{% highlight shell %}
source /vol0601/data/hp240465/Materials/Life_Science/20250312_Bonvin/haddock3/.venv/bin/activate<br>
{% endhighlight %}

You can then run the workflow with:

{% highlight shell %}
haddock3 ./workflows/docking-antibody-antigen.cfg
{% endhighlight %}
<b>Job submission to the batch system:</b>
<br>
<br>
For this execution mode you should create an execution script contain specific requirements for the queueing system and the HADDOCK3 configuration and execution. 
Here is an example of such an execution script (also provided in the <i>HADDOCK3-antibody-antigen</i> directory as <i>run-haddock3-fugaku.sh</i>):

{% highlight shell %}
#!/bin/sh -x
#PJM -L  "node=1"                           # Assign node 1 node
#PJM -L  "rscgrp=small"                     # Specify resource group
#PJM -L  "elapse=02:00:00"                  # Elapsed time limit 1 hour
#PJM -g hp240465                            # group name
#PJM -x PJM_LLIO_GFSCACHE=/vol0004:/vol0006 # volume names that job uses
#PJM -s                                     # Statistical information output

source /vol0601/data/hp240465/Materials/Life_Science/20250312_Bonvin/haddock3/.venv/bin/activate
haddock3 ./workflows/docking-antibody-antigen.cfg

{% endhighlight %}

This file should be submitted to the batch system using the <i>pjsub</i> command:

{% highlight shell %}
pjsub run-haddock3-fugaku.sh
{% endhighlight %}

<br>

And you can check the status in the queue using <i>pjstat</i>.

This run should take about 20 minutes to complete on a single node using 48 arm cores.

</details>


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
<hr>

## Analysis of docking results

In case something went wrong with the docking (or simply if you do not want to wait for the results) you can find the following precalculated runs in the `runs` directory:
- `run1`: docking run created using the unbound antibody.
- `run1-af2`: docking run created using the Alphafold-multimer antibody (see  3).
- `run1-abb`: docking run created using the Immunebuilder antibody (see  3).
- `run1-ens`: docking run created using an ensemble of antibody models (see  4).
- `run-scoring`: scoring run created using various models obtained at the previous stages (see  6).


Once your run has completed - inspect the content of the resulting directory.
You will find the various steps (modules) of the defined workflow numbered sequentially starting at 0, e.g.:

{% highlight shell %}
> ls run1/
     00_topoaa/
     01_rigidbody/
     02_caprieval/
     03_seletop/
     04_flexref/
     05_caprieval/
     06_emref/
     07_caprieval/
     08_clustfcc/
     09_seletopclusts/
     10_caprieval/
     11_contactmap/
     analysis/
     data/
     log
     toppar/
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

The simplest way to extract ranking information and the corresponding HADDOCK scores is to look at the `XX_caprieval` directories (which is why it is a good idea to have it as the final module, and possibly as intermediate steps). This directory will always contain a `capri_ss.tsv` single model statistics file, which contains the model names, rankings and statistics (score, iRMSD, Fnat, lRMSD, ilRMSD and dockq score). E.g. for `10_caprieval`:

<pre style="background-color:#DAE4E7">
                                   model	md5	caprieval_rank	score	irmsd	fnat	lrmsd	ilrmsd	dockq	rmsd	cluster_id	cluster_ranking	model-cluster_ranking	air	angles	bonds	bsa	cdih	coup	dani	desolv	dihe	elec	improper	rdcs	rg	sym	total	vdw	vean	xpcs
../09_seletopclusts/cluster_1_model_1.pdb	-	1	-140.319	0.908	0.897	2.205	1.451	0.855	1.016	3	1	1	133.760	0.000	0.000	2010.880	0.000	0.000	0.000	7.010	0.000	-605.174	0.000	0.000	0.000	0.000	-511.084	-39.671	0.000	0.000
../09_seletopclusts/cluster_1_model_2.pdb	-	2	-137.507	0.879	0.948	1.951	1.354	0.881	0.989	3	1	2	189.059	0.000	0.000	1913.390	0.000	0.000	0.000	3.243	0.000	-521.143	0.000	0.000	0.000	0.000	-387.512	-55.428	0.000	0.000
../09_seletopclusts/cluster_1_model_3.pdb	-	3	-126.481	1.052	0.914	3.038	1.958	0.824	1.293	3	1	3	127.044	0.000	0.000	1816.780	0.000	0.000	0.000	-2.884	0.000	-426.677	0.000	0.000	0.000	0.000	-350.599	-50.966	0.000	0.000
../09_seletopclusts/cluster_1_model_4.pdb	-	4	-102.227	1.334	0.793	2.331	2.292	0.760	1.341	3	1	4	128.628	0.000	0.000	1837.970	0.000	0.000	0.000	12.344	0.000	-410.669	0.000	0.000	0.000	0.000	-327.341	-45.299	0.000	0.000
../09_seletopclusts/cluster_2_model_1.pdb	-	5	-102.077	14.789	0.103	23.359	22.787	0.077	14.405	2	2	1	163.844	0.000	0.000	1888.310	0.000	0.000	0.000	2.575	0.000	-348.025	0.000	0.000	0.000	0.000	-235.613	-51.431	0.000	0.000
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
cluster_rank    cluster_id  n   under_eval  score   score_std  irmsd   irmsd_std   fnat   fnat_std   lrmsd   lrmsd_std  dockq   dockq_std  ilrmsd  ilrmsd_std  rmsd    rmsd_std    air air_std bsa bsa_std desolv  desolv_std  elec    elec_std    total   total_std   vdw vdw_std caprieval_rank
           1    3           4   -          -126.634    15.010   1.044  0.180      0.888   0.058       2.381  0.403      0.830   0.045       1.764  0.382        1.160  0.159   144.623 25.775  1894.755    76.054  4.928   5.550   -490.916    78.318  -394.134    70.848  -47.841 5.927   1
           2    2           4   -           -98.425     2.624  14.572  0.524      0.095   0.009      23.293  0.233      0.074   0.002      22.593  0.371       14.300  0.194   159.227 8.415   1781.358    114.002 2.706   2.898   -340.312    32.395  -230.077    26.771  -48.992 5.015   2
           3    1           4   -           -91.137     1.918  10.249  0.530      0.056   0.007      19.692  0.505      0.078   0.005      18.190  0.649       10.554  0.495   173.598 42.201  1441.505    77.296  4.873   4.329   -389.212    18.467  -251.141    40.747  -35.527 5.170   3
...
</pre>


In this file you find the cluster rank (which corresponds to the naming of the clusters in the previous `seletop` directory), the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (n) in the cluster and the corresponding statistics (averages + standard deviations). The corresponding cluster PDB files will be found in the preceeding `09_seletopclusts` directory.

While these simple text files can be easily checked from the command line already, they might be cumbersome to read.
For that reason, we have developed a post-processing analysis that automatically generates html reports for all `caprieval` steps in the workflow.
These are located in the respective `analysis/XX_caprieval` directories and can be viewed using your favorite web browser.


<hr>

### Cluster statistics

Let us now analyse the docking results. Use for that either your own run or a pre-calculated run provided in the `runs` directory.
Go into the `analysis/10_caprieval_analysis` directory of the respective run directory  (if needed copy the run or that directory to your local computer) and open in a web browser the `report.html` file. Be patient as this page contains interactive plots that may take some time to generate.

On the top of the page, you will see a table that summarises the cluster statistics (taken from the `capri_clt.tsv` file).
The columns (corresponding to the various clusters) are sorted by default on the cluster rank, which is based on the HADDOCK score (found on the 4th row of the table).
As this is an interactive table, you can sort it as you wish by using the arrows present in the first column.
Simply click on the arrows of the term you want to use to sort the table (and you can sort it in ascending or descending order).
A snapshot of this table is shown below:

<figure style="text-align: center;">
    <img width="75%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/caprieval_analysis-table.png">
</figure>

You can also view this report online [here](plots/report.html){:target="_blank"}

*__Note__* that in case the PDB files are still compressed (gzipped) the download links will not work. Also online visualisation is not enabled. To overcome this disk space storge solution, consider adding the global parameter `clean = true` at the begining of your configuration file.


<a class="prompt prompt-info">Inspect the final cluster statistics</a>

<a class="prompt prompt-question">How many clusters have been generated?</a>

<a class="prompt prompt-question">Look at the score of the first few clusters: Are they significantly different if you consider their average scores and standard deviations?</a>

Since for this tutorial we have at hand the crystal structure of the complex, we provided it as reference to the `caprieval` modules.
This means that the iRMSD, lRMSD, Fnat and DockQ statistics report on the quality of the docked model compared to the reference crystal structure.

<a class="prompt prompt-question">How many clusters of acceptable or better quality have been generate according to CAPRI criteria?</a>

<a class="prompt prompt-question">What is the rank of the best cluster generated?</a>

<a class="prompt prompt-question">What is the rank of the first acceptable of better cluster generated?</a>


<hr>

### Visualizing the scores and their components


Next to the cluster statistic table shown above, the `report.html` file also contains a variety of plots displaying the HADDOCK score 
and its components against various CAPRI metrics (i-RMSD, l-RMSD,  Fnat, Dock-Q) with a color-coded representation of the clusters.
These are interactive plots. A menu on the top right of the first row (you might have to scroll to the rigth to see it) 
allows you to zoom in and out in the plots and turn on and off clusters. 

<figure style="text-align: center;">
    <img width="100%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/caprieval_analysis-plots.png">
</figure>

As a reminder, you can also view this report online [here](plots/report.html){:target="_blank"}

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>


Finally, the report also shows plots of the cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank):

<figure style="text-align: center;">
    <img width="100%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/caprieval_analysis-distributions.png">
</figure>

<a class="prompt prompt-question">For this antibody-antigen case, which of the score components correlates best with the quality of the models?</a>


<hr>

### Some single structure analysis


Going back to command line analysis, we are providing in the `scripts` directory a simple script that extracts some model statistics for acceptable or better models from the `caprieval` steps.
To use it, simply call the script with as argument the run directory you want to analyze, e.g.:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats.sh ./runs/run1
</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== runs/run1/02_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  25  out of  100
Total number of medium or better models:      15  out of  100
Total number of high quality models:          1  out of  100

First acceptable model - rank:  1  i-RMSD:  1.196  Fnat:  0.672  DockQ:  0.741
First medium model     - rank:  1  i-RMSD:  1.196  Fnat:  0.672  DockQ:  0.741
Best model             - rank:  17  i-RMSD:  0.982  Fnat:  0.759  DockQ:  0.774
==============================================
== runs/run1/05_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  14  out of  40
Total number of medium or better models:      14  out of  40
Total number of high quality models:          5  out of  40

First acceptable model - rank:  1  i-RMSD:  0.992  Fnat:  0.897  DockQ:  0.834
First medium model     - rank:  1  i-RMSD:  0.992  Fnat:  0.897  DockQ:  0.834
Best model             - rank:  11  i-RMSD:  0.789  Fnat:  0.776  DockQ:  0.842
==============================================
== runs/run1/07_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  14  out of  40
Total number of medium or better models:      14  out of  40
Total number of high quality models:          3  out of  40

First acceptable model - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
First medium model     - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
Best model             - rank:  11  i-RMSD:  0.841  Fnat:  0.897  DockQ:  0.875
==============================================
== runs/run1/10_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  4  out of  12
Total number of medium or better models:      4  out of  12
Total number of high quality models:          1  out of  12

First acceptable model - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
First medium model     - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
Best model             - rank:  3  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
</pre>
</details>
<br>

_**Note**_ that this kind of analysis only makes sense when we know the reference complex and for benchmarking / performance analysis purposes.

<a class="prompt prompt-info">Look at the single structure statistics provided by the script</a>

<a class="prompt prompt-question">How does the quality of the best model changes after flexible refinement? Consider here the various metrics.</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
  In terms of iRMSD values, we only observe very small differences in the best model.
  The fraction of native contacts and the DockQ scores are however improving much more after flexible refinement but increases again slightly after final minimisation.
  All this will of course depend on how different are the bound and unbound conformations and the amount of data used to drive the docking process.
  In general, from our experience, the more and better data at hand, the larger the conformational changes that can be induced.
  </p>
</details>
<br>

<a class="prompt prompt-question">Is the best model always ranked first?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
    This is not the case. The scoring function is not perfect, but does a reasonable job at ranking models of acceptable or better quality on top in this case.
  </p>
</details>
<br>

**_Note_**: A similar script to extract cluster statistics is available in the `scripts` directory as `extract-capri-stats-clt.sh`.
<hr>

### Contacts analysis

We have recently added a new contact analysis module to HADDOCK3 that generates for each cluster both a contact matrix of the entire system showing all contacts within a 4.5Å cutoff and a chord chart representation of intermolecular contacts.

In the current workflow we run, those files can be found in the `11_contactmap` directory.
These are again html files with interactive plots (hover with your mouse over the plots).

<a class="prompt prompt-info">
Open in your favorite web browser the _cluster1_contmap_chordchart.html_ file to analyse the intermolecular contacts of the best-ranked cluster.
</a>

This file taken from the pre-computed run can also directly be visualized [here](cluster1_contmap_chordchart.html){:target="_blank"}

<a class="prompt prompt-question">
Can you identify which residue(s) make(s) the most intermolecular contacts?
</a>


<hr>

### Visualization of the models

To visualize the models from the top cluster of your favorite run, start PyMOL and load the cluster representatives you want to view, e.g. this could be the top model of cluster 1, 2 or 3, located in `XX_seletopclusts` directory of the run. Precalcuated models can be found in the `runs/run1/09_seletopclusts/` directory.

<a class="prompt prompt-info">File menu -> Open -> select cluster_1_model_1.pdb</a>

*__Note__* that the PDB files are compressed (gzipped) by default at the end of a run. You can uncompress those with the `gunzip` command. PyMOL can directly read the gzipped files.

If you want to get an impression of how well-defined a cluster is, repeat this for the best N models you want to view (`cluster_1_model_X.pdb`).
Also load the reference structure from the `pdbs` directory, `4G6M-matched.pdb`.

<a class="prompt prompt-info">File menu -> Open -> select 4G6M-matched.pdb</a>

Once all files have been loaded, type in the PyMOL command window:

<a class="prompt prompt-pymol">
show cartoon<br>
util.cbc<br>
color yellow, 4G6M_matched<br>
</a>

Let us then superimpose all models onto the reference structure:

<a class="prompt prompt-pymol">
alignto 4G6M_matched
</a>

<a class="prompt prompt-question">
How close are the top4 models to the reference? Did HADDOCK do a good job at ranking the best in the top?
</a>

Let’s now check if the active residues which we have defined (the paratope and epitope) are actually part of the interface. In the PyMOL command window type:

<a class="prompt prompt-pymol">
select paratope, (resi 31+32+33+34+35+52+54+55+56+100+101+102+103+104+105+106+151+152+169+170+173+211+212+213+214+216 and chain A)<br>
color red, paratope<br>
select epitope, (resi 72+73+74+75+81+83+84+89+90+92+94+96+97+98+115+116+117 and chain B)<br>
color orange, epitope<br>
</a>

<a class="prompt prompt-question">
Are the residues of the paratope and NMR epitope at the interface?
</a>

**Note:** You can turn on and off a model by clicking on its name in the right panel of the PyMOL window.

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <b><i>See the overlay of the top ranked model onto the reference structure</i></b> <i class="material-icons">expand_more</i>
 </summary>
 <p> Top-ranked model of the top cluster (cluster1_model_1) superimposed onto the reference crystal structure (in yellow)</p>
 <figure style="text-align: center">
   <img width="75%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/results-best-model.png">
 </figure>
 <br>
</details>



<hr>
<hr>

## Conclusions

We have demonstrated the usage of HADDOCK3 in an antibody-antigen docking scenario making use of the paratope information on the antibody side (i.e. no prior experimental information, but computational predictions) and an NMR-mapped epitope for the antigen.
Compared to the static HADDOCK2.X workflow, the modularity and flexibility of HADDOCK3 allow to customise the docking protocols and to run a deeper analysis of the results.
HADDOCK3's intrinsic flexibility can be used to improve the performance of antibody-antigen modelling compared to the results we presented in our
[Structure 2020](https://doi.org/10.1016/j.str.2019.10.011){:target="_blank"} article and in the [related HADDOCK2.4 tutorial](/education/HADDOCK24/HADDOCK24-antibody-antigen){:target="_blank"}.


<hr>
<hr>

## BONUS 1: Dissecting the interface energetics: what is the impact of a single mutation? 

Mutations at the binding interfaces can have widely varying effects on binding affinity - some may be negligible, while others can significantly strengthen or weaken the interaction. Exploring these mutations helps identify critical amino acids for redesigning structurally characterized protein-protein interfaces, which paves the way for developing protein-based therapeutics to deal with a diverse range of diseases.
To pinpoint such amino acids positions, the residues across the protein interaction surfaces are either randomly or strategically mutated. Scanning mutations in this manner is experimentally costly. Therefore, computational methods have been developed to estimate the impact of an interfacial mutation on protein-protein interactions. 
These computational methods come in two main flavours. One involves rigorous free energy calculations, and, while highly accurate, these methods are computationally expensive. The other category includes faster, approximate approaches that predict changes in binding energy using statistical potentials, machine learning, empirical scoring functions etc. Though less precise, these faster methods are practical for large-scale screening and early-stage analysis. In this bonus exercise, we will take a look at two quick ways of estimating the effect of a single mutation in the interface.


### PROT-ON and haddock3-scoring to inspect a single mutation

PROT-ON (Structure-based detection of designer mutations in PROTein-protein interface mutatiONs) is a tool and [online server](http://proton.tools.ibg.edu.tr:8001/about) that scans all possible interfacial mutations and **predicts ΔΔG score** by using EvoEF1 (active in both on the web server and stand-alone versions) or FoldX (active only in the stand-alone version) with the aim of finding the most mutable positions. The original publication describing PROT-ON can be found [here](https://www.frontiersin.org/journals/molecular-biosciences/articles/10.3389/fmolb.2023.1063971/full). 

Here we will use PROT-ON to analyse the interface of our antibody-antigen complex. For that, we will use the provided matched reference structure (`4G6M-matched.pdb`) in which both chains of the antibody have the same chainID (A), which allows us to analyse all interface residues of the antibody at once.

<a class="prompt prompt-info">
Connect to the PROT-ON server page (link above) and fill in the following fields:
</a>

<a class="prompt prompt-info">
Specify your run name* --> 4G6M_matched
</a>

<a class="prompt prompt-info">
Choose / Upload your protein complex* --> Select the provided _4G6M-matched.pdb_ file
</a>

<a class="prompt prompt-info">
Which dimer chains should be analyzed* --> Select chain A for the 1st molecule and B for the 2nd
</a>
<a class="prompt prompt-info">
Pick the monomer for mutational scanning* --> Select the first molecule - the antibody (toggle the switch ON under the chain A)
</a>

<a class="prompt prompt-info">
Click on the Submit button
</a>

Your run should complete in 5-10 minutes. Once finished, you will be presented with a result page summarising the most depleting (ones that decrease the binding affinity) and most enriching (ones that increase the binding affinity) mutations.

<a class="prompt prompt-question">
Which possible mutation would you propose to improve the binding affinity of the antibody?
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See answer</i></b> <i class="material-icons">expand_more</i>
  </summary>
The most enriching mutation is S150W with a -3.69 ΔΔG score.
</details>
<br>

<a class="prompt prompt-question">
Inspect the proposed amino acid in PyMol. Can you rationalise why it might increase the affinity?
</a>

With HADDOCK3, it is possible to take a step further. To perform the mutation, simply rename the desired residue and score such model - HADDOCK will take care of the topology regardless of the side chain differences and energy minimisation of the model. To do so, first either edit _4G6M-matched.pdb_ in your favourite text editor and save this new file as _4G6M_matched_S150W.pdb_, or use the command line: 
<a class="prompt prompt-cmd">
sed 's/SER\ A\ 150/TRP\ A\ 150/g' 4G6M_matched.pdb > 4G6M_matched_S150W.pdb
</a>

Next, score the mutant using the command-line tool `haddock3-score`. 
This tool performs a short workflow composed of the `topoaa` and `emscoring` modules. Use flag `--outputpdb` to save energy-minimized model:
<a class="prompt prompt-cmd">
haddock3-score 4G6M_matched_S150W.pdb \-\-outputpdb
</a>

<a class="prompt prompt-question">
Use _haddock3-score_ to calculate the score of the 4G6M-matched.pdb. Do you see a difference between wild-type and mutant scores? 
Might such single-residue mutation affect the binding affinity? 
</a>

<a class="prompt prompt-info">
Inspect the energy-minimized mutant model (4G6M_matched_S150W_hs.pdb) visually.
Can you rationalise why such a mutation might increase the affinity?
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Zoom in on the mutated residue</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
   <img width="100%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/mutant-stacking.png">
   <center>
   <i>TRP150 is stacking with TYR24 </i>
   </center>
  </figure>
  <br>
</details>
<br>


### Alanine Scanning module 

Another way of exploring interface energetics is by using the `alascan` module of HADDOCK3. `alascan` stands for "Alanine Scanning module". 

This module is capable of mutating interface residues to Alanine and calculating the **Δ HADDOCK score** between the wild-type and mutant, thus providing a measure of the impact of each individual mutation. It is possible to scan all interface residues one by one or limit this scanning to a selected by user set of residues. By default, the mutation to Alanine is performed, as its side chain is just a methyl group, so side chain perturbations are minimal, as well as possible secondary structure changes. It is possible to perform the mutation to any other amino acid type - at your own risk, as such mutations may introduce structural uncertainty. 

**Important**: 1/ `alascan` calculates the difference between wild-type score vs mutant score, i.e. positive `Δscore` indicative of the enriched (stronger) binding and negative `Δscore` is indicative of the depleted (weaker) binding; 2/ Inside `alascan`, a short energy minimization of an input structure is performed, i.e. there's no need to include an additional refinement module prior to `alascan`. 

Here is an example of the workflow to scan interface energetics:
{% highlight toml %}
# ====================================================================
# Scanning interface residues with haddock3
# ====================================================================

# directory in which the scoring will be done
run_dir = "run-energetics-alascan"

# compute mode
mode = "local"
ncores = 50

# Post-processing to generate statistics and plots
postprocess = true
clean = true

molecules =  [
    "pdbs/4G6M_matched.pdb",
    ]

# ====================================================================
# Parameters for each stage are defined below
# ====================================================================
[topoaa]

[alascan]
# mutate each interface residue to Alanine 
scan_residue = 'ALA'
# generate plot of delta score and its components per each mutation
plot = true

# ====================================================================
{% endhighlight %}

A scoring scenario configuration file is provided in the `workflows/` directory as `interaction-energetics.cfg`, and precomputed results are in `runs/run-energetics-alascan`.
The output folder contains, among others, a directory titled `1_alascan` with a file `scan_4G6M_matched_haddock.tsv` that lists each mutation, corresponding score and individual terms:
<pre>
##########################################################
# `alascan` results for 4G6M_matched_haddock.pdb
#
# native score = -145.5891
#
# z_score is calculated with respect to the other residues
##########################################################
chain	res	ori_resname	end_resname	score	vdw	elec	desolv	bsa	delta_score	delta_vdw	delta_elec	delta_desolv	delta_bsa	z_score
A	212	LYS	ALA	-136.33	-66.16	-367.66	3.37	1660.53	-9.26	2.52	-75.12	3.24	37.57	-0.48
A	103	ASP	ALA	-129.64	-59.93	-365.23	3.34	1677.97	-15.95	-3.71	-77.56	3.27	20.13	-1.41
A	54	TRP	ALA	-138.18	-58.34	-435.53	7.27	1690.80	-7.41	-5.30	-7.26	-0.66	7.30	-0.22
A	32	SER	ALA	-143.66	-60.55	-447.37	6.36	1691.72	-1.93	-3.09	4.59	0.24	6.38	0.55
A	58	ASP	ALA	-121.65	-63.49	-306.77	3.20	1639.20	-23.94	-0.15	-136.01	3.41	58.90	-2.52
A	33	GLY	ALA	-148.50	-61.56	-473.22	7.71	1693.18	2.91	-2.08	30.43	-1.10	4.92	1.22
...
</pre>

<a class="prompt prompt-question">
Can you identify the most enriching/depleting mutation of each chain? 
Take a look at _scan_clt_-.tsv_ and open its visualisation _scan_clt_-.html_ in the web browser. 
</a>

You can use an additional script `/scripts/get-alascan-extrema.sh` to check your answer:
<a class="prompt prompt-cmd">
bash scripts/get-alascan-extrema.sh run-energetics-alascan/1_alascan/scan_4G6M_matched_haddock.tsv 
</a>

Mutation of the residue ASP58 turned out to be the most depleting within chain A. 
Let us visualise it in PyMol to analyse its contribution to the binding:
<a class="prompt prompt-pymol">
File menu -> Open -> 4G6M_matched.pdb 
</a>

Display ASP58 as sticks and colour it by atom:
<a class="prompt prompt-pymol">
util.cbc <br>
select asp58, (resi 58 and chain A) <br>
show sticks, asp58 <br>
util.cbao asp58
</a>

Now visualise its neighbouring residues:
<a class="prompt prompt-pymol">
select asp58_neighbour_atoms_4A, (resi 58 and chain A) around 4 and chain B <br>
select asp58_neighbour_residues, byres asp58_neighbour_atoms_4A
show sticks, asp58_neighbour_residues <br>
util.cbao asp58_neighbour_residues <br>
</a>


Let us display contacts using [show contacts plugin](https://pymolwiki.org/index.php/Show_contacts):
<figure style="text-align: center;">
  <img width="100%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/asp58_contacts.png">
  <center>
  <i>ASP58 makes h-bonds with two neighbouring residues</i>
  </center>
</figure>

We can see one hydrogen bond between ASP58 and LYS98, and two hydrogen bonds ASP58 and LYS94. 
Mutating ASP58 to ALA should result in the disappearance of those h-bonds, and the overall depletion of the binding. 
This is reflected by the high negative value (-136.01) of `delta_elec` in either of .tsv files. 

Let us test several mutations to confirm our hypothesis. 
Here is an example of the workflow to perform such mutations and save generated models:

{% highlight ini %}
# ====================================================================
# Mutating selected interface residue with haddock3
# ====================================================================

# directory in which the scoring will be done
run_dir = "run-energetics-mutations"

# compute mode
mode = "local"
ncores = 50

# Post-processing to generate statistics and plots
postprocess = true
clean = true

molecules =  ["pdbs/4G6M_matched.pdb"]

# ====================================================================
# Parameters for each stage are defined below
# ====================================================================
[topoaa]

[alascan]
# mutate residue 58 of chain A to Arginine 
scan_residue = "ARG"
resdic_A = [58]
# save energy-minimised mutant model 
output_mutants= true 

[alascan]
scan_residue = "GLY"
resdic_A = [58]
output_mutants= true 

[alascan]
scan_residue = "TRP"
resdic_A = [58]
output_mutants= true 

{% endhighlight %}

Configuration file for this scenario can be found in `workflows/single-residue-mutations.cfg`, precomputed results are in `run-residue-mutations`. The output folder contains, among others, an energy-minimised mutant model `1_alascan/4G6M_matched_haddock-A_D58R.pdb.gz`, and tables `.tsv` with energetics.
 
<a class="prompt prompt-question">
Take a look at the scores of the mutants. Which mutation depletes binding the most? 
</a>

<a class="prompt prompt-question">
Inspect the mutant vs wild-type complex. Can you see the difference at the interface level? 
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See the overlay of the mutant onto the wild-type structure </i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="100%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/mutant-ref-overlay-alascan.png">
    <center>
    <i>wild-type residue ASP58 is displayed in pink, and mutant residue AGR58 is displayed in orange</i>
    </center>
  </figure>
  <br>
</details>
<br>


<a class="prompt prompt-question">
Compare values obtained with [alascan] to the corresponding values obtained with PROT-ON. Are they different? If yes, can you think of a reason why?
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See answer</i></b> <i class="material-icons">expand_more</i>
  </summary>
The values themselves are expected to differ, because [alascan] calculates ΔHADDOCK score, while PROT-ON predicts ΔΔG. 
Moreover, both tools are making predictions using different methods, so it is normal to have different results. 
However, if both tools consistently identify the same mutations as binding enriching or depleting - this may signal that selected residues indeed play a key role in binding affinity.
</details>
<br>

Now let us consider how sensitive this kind of analysis is to the quality of the docking model.
Instead of using the crystal structure, repeat this analysis using the best model of the top-ranked cluster or the best model with the lowest LRMSD value. 

<a class="prompt prompt-question">
Consider the most binding-enrishing/-depleting mutations predicted based on your favourite docking model. 
How different are those compared to the mutations, predicted based on the crystal structure?
</a>

<hr>
<hr>


## BONUS 2: Does the antibody bind to a known interface of interleukin? ARCTIC-3D analysis

Gevokizumab is a highly specific antibody that targets an allosteric site of Interleukin-1β (IL-1β) in PDB file *4G6M*, thus reducing its binding affinity for its substrate, interleukin-1 receptor type I (IL-1RI). Canakinumab, another antibody binding to IL-1β, has a different mode of action, as it competes directly with the binding site of IL-1RI (in PDB file *4G6J*). For more details please check [this article](https://www.sciencedirect.com/science/article/abs/pii/S0022283612007863?via%3Dihub){:target="_blank"}.

We will now use our new software, [ARCTIC-3D](https://www.nature.com/articles/s42003-023-05718-w){:target="_blank"}, to visualize the binding interfaces formed by IL-1β. First, the program retrieves all the existing binding surfaces formed by IL-1β from the [PDBe website](https://www.ebi.ac.uk/pdbe/){:target="_blank"}. Then, these binding surfaces are compared and clustered together if they span a similar region of the selected protein (IL-1β in our case).

We will run an ARCTIC-3D job targeting the uniprot ID of human Interleukin-1 beta, namely [P01584](https://www.uniprot.org/uniprotkb/P01584/entry){:target="_blank"}.

For this first open the ARCTIC-3D web-server page [here](https://wenmr.science.uu.nl/arctic3d/){:target="_blank"}. 

<a class="prompt prompt-info">
Insert the selected UniProt ID in the **UniprotID** field.
</a>

<a class="prompt prompt-info">
Leave the other parameters as they are and click on **Submit**.
</a>

Wait a few seconds for the job to complete or access a precalculated run [here](https://wenmr.science.uu.nl/arctic3d/example-P01584){:target="_blank"}.

<a class="prompt prompt-question">
How many interface clusters were found for this protein?
</a>

Once you download the output archive, you can find the clustering information presented in the dendrogram:

<figure style="text-align: center;">
<img width="75%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/dendrogram_average_P01584.png">
</figure>

We can see how the two *4G6M* antibody chains are recognized as a unique cluster, clearly separated from the other binding surfaces and, in particular, from those proper to IL-1RI (uniprot ID P14778).

<a class="prompt prompt-info">
Re-run ARCTIC-3D with a clustering threshold equal to 0.95
</a>

This means that the clustering will be looser, therefore lumping more dissimilar surfaces into the same object.

You can inspect a precalculated run [here](https://wenmr.science.uu.nl/arctic3d/example-P01584-095){:target="_blank"}.

<a class="prompt prompt-question">
How do the results change? Are gevokizumab or canakinumab PDB files being clustered with any IL-1RI-related interface?
</a>



<hr>
<hr>

## BONUS 3: How good are AI-based models of antibody for docking?

The release of [AlphaFold2 in late 2020](https://www.nature.com/articles/s41586-021-03819-2) has brought structure prediction methods to a new frontier, providing accurate models for the majority of known proteins. This revolution did not spare antibodies, with [Alphafold2-multimer](https://github.com/sokrypton/ColabFold){:target="_blank"} and other prediction methods (most notably [ABodyBuilder2](https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/abodybuilder2/){:target="_blank"}, from the ImmuneBuilder suite) performing nicely on the variable regions.

For a short introduction to AI and AlphaFold2 refer to this other tutorial [introduction](/education/molmod_online/alphafold/#introduction){:target="_blank"}.

For antibody modelings, CDR loops are clearly the most challenging region to be predicted given their high sequence variability and flexibility. 
Multiple Sequence Alignment (MSA)-derived information is also less useful in this context.

Here we will see whether the antibody models given by Alphafold2-multimer and ABodyBuilder2 can be used for generating reliable models of the antibody-antigen complex by docking, instead of the unbound form used in this tutorial, which, in many cases, will not be available.


### Analysing the AI models

We already ran the prediction with these two tools, and you can find the resulting models in the `pdbs` directory as:

- `4g6k_Abodybuilder2.pdb`
- `4g6k_AF2_multimer.pdb`


As was demonstrated in the tutorial, those files must be preprocessed for their use in HADDOCK. Docking-ready files are also provided in the `pdbs` directory:


- `4G6K_abb_clean.pdb`
- `4G6K_af2_clean.pdb`


Load the experimental unbound structure (`4G6K_clean.pdb`) and the two AI models in PyMOL to see whether they resemble the experimental unbound structure.

<a class="prompt prompt-info">
File menu -> Open -> select 4G6K_clean.pdb
</a>
<a class="prompt prompt-info">
File menu -> Open -> select 4G6K_abb_clean.pdb
</a>
<a class="prompt prompt-info">
File menu -> Open -> select 4G6K_af2_clean.pdb
</a>

Align the models to the experimental unbound structure

<a class="prompt prompt-pymol">
alignto 4G6K_clean
</a>

<a class="prompt prompt-question">
Which model is the closest to the unbound conformation?
</a>

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See the RMSD values</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
  4G6K_abb_clean       RMSD =    0.428 Å
  4G6K_af2_clean       RMSD =    0.765 Å
</pre>
 <br>
</details>
<br>

For docking purposes however, it might be more interesting to know how far are the models from the bound conformation, i.e. the conformation in the antibody-antigen complex.
The closer it is, the easier it should become to model the complex by docking.
To assess this, we can load the structure of the complex in PyMOL and align all other structures/models to it.

<a class="prompt prompt-info">
File menu -> Open -> select 4G6M_matched.pdb
</a>

<a class="prompt prompt-pymol">
color yellow, 4G6M_matched
</a>

Align now the models to the experimental bound structure

<a class="prompt prompt-pymol">
alignto 4G6M_matched and chain A
</a>

<a class="prompt prompt-question">
Which model is the closest to the bound conformation?
</a>

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See the RMSD values</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
  4G6K_abb_clean       RMSD =    0.330 Å
  4G6K_af2_clean       RMSD =    0.675 Å
  4G6K_clean           RMSD =    0.393 Å
</pre>
 <br>
</details>
<br>


<hr>

### Docking performance using AI-based antibody models

We can repeat the docking as described above in our tutorial, but using this time either the ABodyBuilder2 or AlphaFold2 models as input.
For this, modify your haddock3 configuration file, changing the input PDB file of the first molecule (the antibody) using the respective HADDOCK-ready models provided in the `pdbs` directory.
You will also need to change the restraint filename used to keep the two parts of the antibody together (those files are present in the `restraints` directory.

Further, run haddock3 as described above.

Pre-calculated runs are provided in the `runs` directory. Analyse your run (or the pre-calculated ones) as described previously.

<a class="prompt prompt-question">
Which starting structure of the antibody gives the best results in terms of cluster quality and ranking?
</a>

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See the cluster statistics </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1/10_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  1  out of  3
Total number of medium or better clusters:      1  out of  3
Total number of high quality clusters:          0  out of  3

First acceptable cluster - rank:  1  i-RMSD:  1.049  Fnat:  0.879  DockQ:  0.815
First medium cluster     - rank:  1  i-RMSD:  1.049  Fnat:  0.879  DockQ:  0.815
Best cluster             - rank:  1  i-RMSD:  1.049  Fnat:  0.879  DockQ:  0.815

==============================================
== run1-abb/10_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  1  out of  5
Total number of medium or better clusters:      1  out of  5
Total number of high quality clusters:          0  out of  5

First acceptable cluster - rank:  1  i-RMSD:  1.134  Fnat:  0.841  DockQ:  0.796
First medium cluster     - rank:  1  i-RMSD:  1.134  Fnat:  0.841  DockQ:  0.796
Best cluster             - rank:  1  i-RMSD:  1.134  Fnat:  0.841  DockQ:  0.796

==============================================
== run1-af2/10_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  2  out of  3
Total number of medium or better clusters:      0  out of  3
Total number of high quality clusters:          0  out of  3

First acceptable cluster - rank:  1  i-RMSD:  3.974  Fnat:  0.289  DockQ:  0.239
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  3  i-RMSD:  3.305  Fnat:  0.302  DockQ:  0.290
</pre>
 <br>
</details>
<br>

<a class="prompt prompt-question">
Which starting structure of the antibody gives the best overall model (irrespective of the ranking)?
</a>

*__Hint__*: Use the `extract-capri-stats.sh` script to analyse the various runs and find the best (lowest i-RMSD or highest Dock-Q score) as the `emref` stage.

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See single structure statistics </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1/07_caprieval/capri_ss.tsv
==============================================
...
First acceptable model - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
First medium model     - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
Best model             - rank:  11  i-RMSD:  0.841  Fnat:  0.897  DockQ:  0.875

==============================================
== run1-abb/07_caprieval/capri_ss.tsv
==============================================
...
First acceptable model - rank:  1  i-RMSD:  0.990  Fnat:  0.931  DockQ:  0.860
First medium model     - rank:  1  i-RMSD:  0.990  Fnat:  0.931  DockQ:  0.860
Best model             - rank:  1  i-RMSD:  0.990  Fnat:  0.931  DockQ:  0.860

==============================================
== run1-af2/07_caprieval/capri_ss.tsv
==============================================
...
First acceptable model - rank:  1  i-RMSD:  3.246  Fnat:  0.362  DockQ:  0.389
First medium model     - rank:   i-RMSD:   Fnat:   DockQ:
Best model             - rank:  21  i-RMSD:  2.474  Fnat:  0.362  DockQ:  0.468
</pre>
 <br>
</details>
<br>


<hr>

### Conclusions - AI-based docking

All three antibody structures used in input give good to reasonable results.
The unbound and the ABodyBuilder2 antibodies provided better results, with the best cluster showing models within 1 angstrom of interface-RMSD with respect to the unbound structure.
Using the Alphafold2 structure in this case is not the best option, as the input antibody is not perfectly modelled in its H3 loop.


<hr>
<hr>

## BONUS 4: Ensemble docking using a combination of exprimental and AI-predicted antibody structures


Instead of running haddock3 using a specific input structure of the antibody, we can also use an ensemble of all available models.
Such an ensemble can be created from the individual models using `pdb_mkensemble` from PDB-tools:

<a class="prompt prompt-cmd">
pdb_mkensemble 4G6K_clean.pdb 4G6K_abb_clean.pdb 4G6K_af2_clean.pdb > 4G6K-ensemble.pdb
</a>

This ensemble file is provided in the `pdbs` directory.

Now we can make use of the flexibility of haddock3 in defining workflows to add a clustering step after the rigid body docking step in order to make sure that models originating from all models will ideally be selected for the refinement steps (provided they do cluster). This modified workflow looks like:


{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen 
# ====================================================================

# directory in which the scoring will be done
run_dir = "run-ens-CDR-NMR-CSP"

# compute mode
mode = "local"
ncores = 50

# Post-processing to generate statistics and plots
postprocess = true
clean = true

molecules =  [
    "pdbs/4G6K-ensemble.pdb",
    "pdbs/4I1B_clean.pdb"
    ]

# ====================================================================
# Parameters for each stage are defined below, prefer full paths
# ====================================================================
[topoaa]

[rigidbody]
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
# Reduced sampling (150 instead of the default of 1000)
# Increased to 150 so that each conformation is sampled 50 times
sampling = 150

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[clustfcc]
plot_matrix = true

[seletopclusts]
top_models = 10

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[flexref]
tolerance = 5
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[emref]
tolerance = 5
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[clustfcc]
plot_matrix = true

[seletopclusts]
top_models = 4

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[contactmap]

# ====================================================================

{% endhighlight %}


Our workflow consists of the following 14 modules:

0. **`topoaa`**: *Generates the topologies for the CNS engine and builds missing atoms*
1. **`rigidbody`**: *Performs Rigid body energy minimisation* - with increased sampling (150 models - 50 per input model)
2. **`caprieval`**: *Calculates CAPRI metrics*
3. **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
4. **`seletopclusts`**: *Selects the top models of all clusters* - In this case, we select max 10 models per cluster.
5. **`caprieval`**: *Calculates CAPRI metrics* of the selected clusters
6. **`flexref`**: *Performs Semi-flexible refinement of the interface (`it1` in haddock2.4)*
7. **`caprieval`**
8. **`emref`**: *Performs a final refinement by energy minimisation (`itw` EM only in haddock2.4)*
9. **`caprieval`**
10. **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
11. **`seletopclusts`**: *Selects the top models of all clusters*
12. **`caprieval`**
13. **`contactmap`**: *Contacts matrix and a chordchart of intermolecular contacts*

Compared to the original workflow described in this tutorial we have added clustering and cluster selections steps after the rigid body docking.

Run haddock3 with this configuration file as described above.

A pre-calculated run is provided in the `runs` directory as `run1-ens`. 
Analyse your run (or the pre-calculated ones) as described previously.


<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See the cluster statistics </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1-ens//12_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  3  out of  11
Total number of medium or better clusters:      1  out of  11
Total number of high quality clusters:          1  out of  11

First acceptable cluster - rank:  1  i-RMSD:  0.981  Fnat:  0.918  DockQ:  0.850
First medium cluster     - rank:  1  i-RMSD:  0.981  Fnat:  0.918  DockQ:  0.850
Best cluster             - rank:  1  i-RMSD:  0.981  Fnat:  0.918  DockQ:  0.850
</pre>
 <br>
</details>
<br>


<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See single structure statistics </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1-ens//02_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  27  out of  150
Total number of medium or better models:      11  out of  150
Total number of high quality models:          1  out of  150

First acceptable model - rank:  2  i-RMSD:  1.422  Fnat:  0.586  DockQ:  0.631
First medium model     - rank:  2  i-RMSD:  1.422  Fnat:  0.586  DockQ:  0.631
Best model             - rank:  26  i-RMSD:  0.982  Fnat:  0.759  DockQ:  0.774
==============================================
== run1-ens//05_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  16  out of  83
Total number of medium or better models:      10  out of  83
Total number of high quality models:          1  out of  83

First acceptable model - rank:  2  i-RMSD:  1.422  Fnat:  0.586  DockQ:  0.631
First medium model     - rank:  2  i-RMSD:  1.422  Fnat:  0.586  DockQ:  0.631
Best model             - rank:  24  i-RMSD:  0.982  Fnat:  0.759  DockQ:  0.774
==============================================
== run1-ens//07_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  17  out of  83
Total number of medium or better models:      9  out of  83
Total number of high quality models:          4  out of  83

First acceptable model - rank:  1  i-RMSD:  0.836  Fnat:  0.931  DockQ:  0.878
First medium model     - rank:  1  i-RMSD:  0.836  Fnat:  0.931  DockQ:  0.878
Best model             - rank:  7  i-RMSD:  0.829  Fnat:  0.845  DockQ:  0.854
==============================================
== run1-ens//09_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  16  out of  83
Total number of medium or better models:      9  out of  83
Total number of high quality models:          3  out of  83

First acceptable model - rank:  1  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
First medium model     - rank:  1  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
Best model             - rank:  12  i-RMSD:  0.851  Fnat:  0.845  DockQ:  0.851
==============================================
== run1-ens//12_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  10  out of  44
Total number of medium or better models:      4  out of  44
Total number of high quality models:          2  out of  44

First acceptable model - rank:  1  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
First medium model     - rank:  1  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
Best model             - rank:  2  i-RMSD:  0.879  Fnat:  0.948  DockQ:  0.881
</pre>
 <br>
</details>
<br>


We started from three different conformations of the antibody: 1) the unbound crystal structure, 2) the ABodyBuilder2 model and 3) the AlphaFold2 model.

<a class="prompt prompt-question">
Using the information in the _traceback_ directory, try to figure out which of the three starting antibody models makes it into the best cluster at the end of the workflow.
</a>



<hr>
<hr>

## BONUS 5: Antibody-antigen complex structure prediction from sequence using AlphaFold2


With the advent of Artificial Intelligence (AI) and AlphaFold2, we can also try to predict directly the full antibody-antigen complex using AlphaFold2.
For this we are going to use the _AlphaFold2_mmseq2_ Jupyter notebook which can be found with other interesting notebooks in Sergey Ovchinnikov 
[ColabFold GitHub repository](https://github.com/sokrypton/ColabFold){:target="_blank"}, making use of the Google Colab CLOUD resources.

Start the AlphaFold2 notebook on Colab by clicking [here](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb){:target="_blank"}.

**Note**: The bottom part of the notebook contains instructions on how to use it.

<br>

### Setting up the antibody-antigen complex prediction with AlphaFold2

To setup the prediction we need to provide the sequence of the heavy and light chains of the antibody and the sequence of the antigen.
These are respectively

* Antibody heavy chain:
<pre style="background-color:#DAE4E7">
QVQLQESGPGLVKPSQTLSLTCSFSGFSLSTSGMGVGWIRQPSGKGLEWLAHIWWDGDES
YNPSLKSRLTISKDTSKNQVSLKITSVTAADTAVYFCARNRYDPPWFVDWGQGTLVTVSS
</pre>

* Antibody light chain:
<pre style="background-color:#DAE4E7">
DIQMTQSTSSLSASVGDRVTITCRASQDISNYLSWYQQKPGKAVKLLIYYTSKLHSGVPS
RFSGSGSGTDYTLTISSLQQEDFATYFCLQGKMLPWTFGQGTKLEIK
</pre>

* Antigen:
<pre style="background-color:#DAE4E7">
VRSLNCTLRDSQQKSLVMSGPYELKALHLQGQDMEQQVVFSMSFVQGEESNDKIPVALGL
KEKNLYLSCVLKDDKPTLQLESVDPKNYPKKKMEKRFVFNKIEINNKLEFESAQFPNWYI
STSQAENMPVFLGGTKGGQDITDFTMQFVSS
</pre>
<br>

To use AlphaFold2 to predict this antibody-antigen complex follow the following steps:

<a class="prompt prompt-info">
Copy and paste each of the above sequences in the _query_sequence_ field, adding a colon *:* in between the sequences.
</a>

For your convenience the full sequence with colons is provided:

<pre style="background-color:#DAE4E7">
QVQLQESGPGLVKPSQTLSLTCSFSGFSLSTSGMGVGWIRQPSGKGLEWLAHIWWDGDESYNPSLKSRLTISKDTSKNQVSLKITSVTAADTAVYFCARNRYDPPWFVDWGQGTLVTVSS:DIQMTQSTSSLSASVGDRVTITCRASQDISNYLSWYQQKPGKAVKLLIYYTSKLHSGVPSRFSGSGSGTDYTLTISSLQQEDFATYFCLQGKMLPWTFGQGTKLEIK:VRSLNCTLRDSQQKSLVMSGPYELKALHLQGQDMEQQVVFSMSFVQGEESNDKIPVALGLKEKNLYLSCVLKDDKPTLQLESVDPKNYPKKKMEKRFVFNKIEINNKLEFESAQFPNWYISTSQAENMPVFLGGTKGGQDITDFTMQFVSS
</pre>


<a class="prompt prompt-info">
Define the _jobname_, e.g. Ab-Ag
</a>

<a class="prompt prompt-info">
In the _Advanced settings_ block you can check the option to save the results to your Google Drive (if you have an account)
</a>

<a class="prompt prompt-info">
In the top section of the Colab, click: _Runtime > Run All_
</a>

(It may give a warning that this is not authored by Google because it is pulling code from GitHub - you can ignore it). 

This will automatically install, configure and run AlphaFold2 for you - leave this window open. 
After the prediction completed, you will be asked to download a zip archive with the results (if you configured it to use Google Drive, a result archive will be automatically saved to your Google Drive).

<br>
_Time to grab a cup of tea or a coffee!
And while waiting try to answer the following questions:_

<a class="prompt prompt-question">
    How do you interpret AlphaFold2 predictions? What are the predicted LDDT (pLDDT), PAE, iptm?
</a>

_Tip_: Try to find information about the prediction confidence at [https://alphafold.ebi.ac.uk/faq](https://alphafold.ebi.ac.uk/faq){:target="\_blank"}. A nice summary can also be found [here](https://www.rbvi.ucsf.edu/chimerax/data/pae-apr2022/pae.html){:target="\_blank"}.


Pre-calculated AlphFold2 predictions are provided [here](abagtest_2d03e.result.zip){:target="\_blank"}. This archive contains the five predicted models (the naming indicates the rank), figures (png) files (PAE, pLDDT, coverage) and json files containing the corresponding values (the last part of the json files report the ptm and iptm values).


<br>

### Analysis of the generated AF2 models

While the notebook is running, models will appear first under the `Run Prediction` section, colored both by chain and by pLDDT.

The best model will then be displayed under the `Display 3D structure` section. This is an interactive 3D viewer that allows you to rotate the molecule and zoom in or out.

**Note** that you can change the model displayed with the _rank_num_ option. After changing, it execute the cell by clicking on the run cell icon on the left of it.

<a class="prompt prompt-question">
    How similar are the five models generated by AF2?
</a>

Consider the pLDDT of the various models (the higher the pLDDT the more reliable the model).

<a class="prompt prompt-question">
    What is the confidence of those predictions? (check again the FAQ page of the Alphafold database provided above for pLDDT values)
</a>

While the pLDDT score is an overall measure, you can also focus on the interface score reported in the `iptm` score (value between 0 and 1).


<details style="background-color:#DAE4E7">

  <summary style="font-weight: bold">
    <i>See the confidence statistics for the five generated models</i>
  </summary>

   <pre>
    Model1: pLDDT=90.4 pTM=0.654 ipTM=0.525
    Model2: pLDDT=88.0 pTM=0.65  ipTM=0.522
    Model3: pLDDT=88.2 pTM=0.647 ipTM=0.52
    Model4: pLDDT=88.0 pTM=0.644 ipTM=0.516
    Model5: pLDDT=88.1 pTM=0.641 ipTM=0.512
</pre>
<br>
Note that if you performed a fresh run your results might well differ from those shown here.
<br>
</details>
<br>

<a class="prompt prompt-question">
    Based on the iptm scores, would you qualify those models as reliable?
</a>

**Note** that in this case the iptm score reports on all interfaces, i.e. both the interface between the two chains of the antibody, and the antibody-antigen interface

Another useful way of looking at the model accuracy is to check the Predicted Alignment Error plots (PAE) (also referred to as Domain position confidence).
The PAE gives a distance error for every pair of residues: It gives the estimate of the position error at residue x when the predicted and true structures are aligned on residue y.
Values range from 0 to 35 Angstroms.
It is usually shown as a heatmap image with residue numbers running along vertical and horizontal axes and each pixel colored according to the PAE value for the corresponding pair of residues.
If the relative position of two domains is confidently predicted then the PAE values will be low (less than 5A - dark blue) for pairs of residues with one residue in each domain.
When analysing your complex, the diagonal block will indicate the PAE within each molecule/domain, while the off-diagonal blocks report the accuracy of the domain-domain placement.


Our antibody-antigen complex consists of three interfaces:

* The interface between the heavy and light chains of the antibody
* The interface between the heavy chain of the antibody and the antigen
* The interface between the light chain of the antibody and the antigen

<br>
<details style="background-color:#DAE4E7">
  <summary style="font-weight: bold">
    <i>See the PAE plots for the five generated models</i>
  <br>
  </summary>
  <figure align="center">
   <img src="/education/HADDOCK3/HADDOCK3-antibody-antigen/abagtest_2d03e_pae.png">
  </figure>
</details>
<br>

<a class="prompt prompt-question">
    Based on the PAE plots, which interfaces can be considered reliable/unreliable?
</a>


<br>

### Visualization of the generated AF2 models

In order to visualize the models in PyMOL save your predictions to disk or download the precalculated AlphaFold2 models from [here](abagtest_2d03e.result.zip){:target="\_blank"}.

Start PyMOL and load via the File menu all five AF2 models.

<a class="prompt prompt-pymol">File menu -> Open -> select abagtest_2d03e_unrelaxed_rank_001_alphafold2_multimer_v3_model_3_seed_000.pdb</a>

Repeat this for each model (`abagtest_2d03e_unrelaxed_rank_X_alphafold2_multimer_v3_model_X_seed_000.pdb` or whatever the naming of your model is).

Let us superimpose all models on the antibody (the antibody in the provided AF2 models correspond to chains A and B):

<a class="prompt prompt-pymol">
util.cbc<br>
select abagtest_2d03e_unrelaxed_rank_001_alphafold2_multimer_v3_model_3_seed_000 and chain A+B<br>
alignto sele<br>
</a>

This will align all clusters on the antibody, maximizing the differences in the orientation of the antigen.

<a class="prompt prompt-question">
Examine the various models. How does the orientation of the antigen differ between them?
</a>

**Note:** You can turn on and off a model by clicking on its name in the right panel of the PyMOL window.

<details>

  <summary style="font-weight: bold">
    <i>See tips on how to visualize the prediction confidence in PyMOL</i>
  </summary>

  When looking at the structures generated by AlphaFold2 in PyMOL, the pLDDT is encoded as the B-factor. <br>
  To color the model according to the pLDDT type in PyMOL:
  <br>
  <a class="prompt prompt-pymol">
    spectrum b
  </a>

  **Note** that the scale in the B-factor field is the inverse of the color coding in the PAE plots: i.e. red mean reliable (high pLDDT) and blue unreliable (low pLDDT))
</details>
<br>

Since we do have NMR chemical shift perturbation data for the antigen, we can check if the perturbed residues are at the interface in the AF2 models.
Note that there is a shift in the numbering of 2 residues between the AF2 and the HADDOCK models.

<a class="prompt prompt-pymol">
util.cbc<br>
select epitope, (resi 70,71,72,73,81,82,87,88,90,92,94,95,96,113,114,115) and chain C<br>
color orange, epitope<br>
</a>

<a class="prompt prompt-question">
Does any model have the NMR-identified epitope at the interface with the antibody?
</a>


<details style="background-color:#DAE4E7">

  <summary style="font-weight: bold">
    <i>See the AlphaFold2 models with the NMR-mapped epitope </i>
  <br>
  </summary>
  <figure align="center">
   <img width="90%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/ab-ag-af2.png">
  </figure>
  <br>
</details>
<br>

It should be clear from the visualization of the NMR-mapped epitope on the AF2 models that none satisfies the NMR data.
To further make that clear we can compare the models to the crystal structure of the complex (4G6M).

For this download and superimpose the models onto the crystal structure in PyMOL with the following commands:

<a class="prompt prompt-pymol">
fetch 4G6M<br>
remove resn HOH<br>
color yellow, 4G6M<br>
select 4G6M and chain H+L<br>
alignto sele
</a>

<details style="background-color:#DAE4E7">

  <summary style="font-weight: bold">
    <i>See the AlphaFold2 models superimposed onto the crystal structure of the complex (4G6M)</i>
  <br>
  </summary>
  <figure align="center">
   <img width="90%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/ab-ag-af2-4G6M.png">
  </figure>
  <br>
</details>
<br>


More recently, the third version of AlphaFold (AlphaFold3) has been [published](https://www.nature.com/articles/s41586-024-07487-w){:target="\_blank"}.
While the code is not yet released, a dedicated online tool [AlphaFoldServer](https://golgi.sandbox.google.com/){:target="\_blank"} is made available for the academic community to allow us to make upto 20 predictions per day with this new version.
Pre-calculated AlphFold3 predictions are provided [here](af3server_abag_15052024.zip){:target="\_blank"}.

<a class="prompt prompt-question">
Try to reproduce the previous steps and examine the quality of the various generated models. Do AlphaFold3 provide better predictions?
</a>

<details style="background-color:#DAE4E7">

  <summary style="font-weight: bold">
    <i>See the AlphaFold3 models with mapped epitope residues in orange</i>
  <br>
  </summary>
  <figure align="center">
   <img width="90%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/ab-ag-af3-epitope.png">
  </figure>
  <br>
</details>
<br>

<details style="background-color:#DAE4E7">

  <summary style="font-weight: bold">
    <i>See the AlphaFold3 models onto the crystal structure of the complex (4G6M) in red</i>
  <br>
  </summary>
  <figure align="center">
   <img width="90%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/ab-ag-af3-4G6M.png">
  </figure>
  <br>
</details>
<br>

<hr>
<hr>


## BONUS 6: Running a scoring scenario

This section demonstrates the use of HADDOCK3 to score the various models obtained at the previous stages (ensemble docking and AlphaFold predictions) 
and observe if the HADDOCK scoring function is able to detect the quality of the models.

To this end the following workflow is defined:

1. Generate the topologies for the various models.
2. Energy Minimise all complexes.
3. Cluster the models using Fraction of Common Contacts:
  - set the parameter `min_population` to 1 so that all models, including singletons (models that do not cluster with any others), will be forwarded to the next steps.
  - set the parameter `plot_matrix` to true to generate a matrix of the clusters for a visual representation.
4. Comparison of the models with the reference complex `4G6M_matched.pdb` using CAPRI criteria.

For this, two ensembles must be scored and one structure will be used as a reference. You can find them in the `pdbs/` directory:
- `07_emref_and_top5af2_ensemble.pdb`: An ensemble of models obtained from the ensemble run, combined with top5 AlphaFold2 predictions.
- `af3server_15052024_top5ens.pdb`: An ensemble of top5 AlphaFold3 predictions.
- `4G6M_matched.pdb`: The reference structure for quality assessments.


{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen 
# ====================================================================
run_dir = "scoring-haddock3-alphafold2and3-ensemble"

molecules =  [
    "pdbs/haddock3-ens-emref-ensemble.pdb",
    "pdbs/af2-models.pdb",
    "pdbs/af3-models.pdb",
    ]

# ====================================================================
# Parameters for each stage are defined below
# ====================================================================

[topoaa]

[emscoring]

[clustfcc]
# Reduce the min_population to define a cluster to 1 so that models
# that do not cluster with any other will define singlotons
min_population = 1
# Generate a matrix of the clusters
plot_matrix = true

[caprieval]
reference_fname = "4G6M_matched.pdb"

# ====================================================================

{% endhighlight %}


A scoring scenario configuration file is provided in the `workflows/` directory as `scoring-antibody-antigen.cfg, precomputed results in `runs/run-scoring`.

You can again look at the `capri_ss.tsv` file in the `4_caprieval` directory. It contains the energy minimised statistics:

<pre>
              model md5 caprieval_rank   score      irmsd   fnat    lrmsd   ilrmsd  dockq   rmsd    cluster_id  cluster_ranking model-cluster_ranking   air angles  bonds   bsa cdih    coup    dani    desolv  dihe    elec    improper    rdcs    rg  sym total   vdw vean    xpcs
../1_emscoring/emscoring_82.pdb -   1   -157.149    0.910   0.897   2.201   1.456   0.855   1.016  3   1   1   0.000   0.000   0.000   2000.130    0.000  0.000   0.000   7.345   0.000   -599.183  0.000   0.000   0.000   0.000   -643.841        -44.658 0.000   0.000
../1_emscoring/emscoring_2.pdb  -   2   -156.452    0.880   0.948   1.949   1.355   0.881   0.989  3   1   2   0.000   0.000   0.000   1914.860    0.000  0.000   0.000   3.125   0.000   -504.372  0.000   0.000   0.000   0.000   -563.075        -58.703 0.000   0.000
../1_emscoring/emscoring_64.pdb -   3   -138.214    1.052   0.914   3.039   1.955   0.824   1.294  3   1   3   0.000   0.000   0.000   1784.350    0.000  0.000   0.000   -2.359  0.000   -424.542  0.000   0.000   0.000   0.000   -475.489        -50.947 0.000   0.000
../1_emscoring/emscoring_40.pdb -   4   -135.230    1.085   0.897   1.866   1.756   0.836   1.144  3   1   4   0.000   0.000   0.000   1875.210    0.000  0.000   0.000   3.490   0.000   -429.067  0.000   0.000   0.000   0.000   -481.973        -52.906 0.000   0.000
../1_emscoring/emscoring_37.pdb -   5   -134.569   13.624  0.069   22.589  21.764  0.068   13.881  5   2   1   0.000   0.000   0.000   1802.890    0.000  0.000   0.000   6.081   0.000   -426.815  0.000   0.000   0.000   0.000   -482.102        -55.287 0.000   0.000

...
</pre>

<a class="prompt prompt-question">
Did the HADDOCK scoring do a good job at putting the best models on top (consider for example the DockQ score)? 
</a>

The `emscoring` module renames all models, which makes it difficult to know what was the original model. 
You can however trace back a model to its original file by looking into the `traceback/traceback.tsv` file:

<pre>
00_topoaa                                               1_emscoring             1_emscoring_rank
emref_9_from_haddock3-ens-emref-ensemble_83_haddock.psf emscoring_82.pdb        1
emref_10_from_haddock3-ens-emref-ensemble_2_haddock.psf emscoring_2.pdb         2
emref_7_from_haddock3-ens-emref-ensemble_67_haddock.psf emscoring_64.pdb        3
emref_5_from_haddock3-ens-emref-ensemble_45_haddock.psf emscoring_40.pdb        4
...
</pre>

<a class="prompt prompt-question">
Try to locate the AlphaFold2 and AlphaFold3 models (their filenames start with _abag_test_ and _af3server_, respectively)
</a>

A simple way to extra this information is to use `grep`:

<a class="prompt prompt-cmd">
grep abag traceback.tsv
</a>

<details style="background-color:#DAE4E7">
  <summary style="font-weight: bold">
    <i>See the output of grep for the AlphaFold2 models</i>
  <br>
  </summary>
  <pre>
> grep abag traceback.tsv
abagtest_2d03e_unrelaxed_rank_001_alphafold2_multimer_v3_model_3_seed_000_from_af2-models_1_haddock.psf	emscoring_84.pdb	86
abagtest_2d03e_unrelaxed_rank_005_alphafold2_multimer_v3_model_2_seed_000_from_af2-models_5_haddock.psf	emscoring_88.pdb	90
abagtest_2d03e_unrelaxed_rank_004_alphafold2_multimer_v3_model_4_seed_000_from_af2-models_4_haddock.psf	emscoring_87.pdb	91
abagtest_2d03e_unrelaxed_rank_003_alphafold2_multimer_v3_model_1_seed_000_from_af2-models_3_haddock.psf	emscoring_86.pdb	92
abagtest_2d03e_unrelaxed_rank_002_alphafold2_multimer_v3_model_5_seed_000_from_af2-models_2_haddock.psf	emscoring_85.pdb	93
  </pre>
</details>
<br>


<a class="prompt prompt-cmd">
grep af3server traceback.tsv
</a>

<details style="background-color:#DAE4E7">
  <summary style="font-weight: bold">
    <i>See the output of grep for the AlphaFold3 models</i>
  <br>
  </summary>
  <pre>
> grep abag traceback.tsv
af3server_15052024_2_ready_from_af3-models_2_haddock.psf	emscoring_90.pdb	40
af3server_15052024_1_ready_from_af3-models_1_haddock.psf	emscoring_89.pdb	81
af3server_15052024_4_ready_from_af3-models_4_haddock.psf	emscoring_92.pdb	87
af3server_15052024_3_ready_from_af3-models_3_haddock.psf	emscoring_91.pdb	88
af3server_15052024_5_ready_from_af3-models_5_haddock.psf	emscoring_93.pdb	89
  </pre>
</details>
<br>

<a class="prompt prompt-question">
What are their ranks?
</a>

We have already seen in the previous section that none of the AlphaFold models were close to the real complex. 
This is however also the case for some of the HADDOCK models.
Still the AlpaFold models score very badly, toward the end of the ranked list of models.

<a class="prompt prompt-question">
Having found their ranks, can you figure out from the statistics in _capri_ss.tsv_ which component of the HADDOCK score causes in particular this bad scoring?
</a>


<details style="background-color:#DAE4E7">
  <summary style="font-weight: bold">
    <i>See the answer</i>
  <br>
  </summary>
  <p> The bottom eight models (the worst ranking ones) are all AlphaFold3/2 models. Looking at the componenents of the score 
  (some were left out in the table below for simplicity) one can see that it is mainly the van der Waals energy that causes the high scores, 
  which is indicative of clashes in the models.</p>
  <pre>
model               md5 caprieval_rank  score    irmsd   fnat    lrmsd   ilrmsd  dockq   rmsd    bsa        desolv    elec      vdw vean    xpcs
...
../1_emscoring/emscoring_84.pdb -   86  -67.914  11.123  0.000   22.413  18.626  0.048   12.213  3535.520   -67.537  -150.913    29.806 
../1_emscoring/emscoring_92.pdb -   87  -63.263  11.426  0.000   22.104  21.035  0.049   11.048  1383.920    -9.924   -88.656   -35.607
../1_emscoring/emscoring_91.pdb -   88  -50.990  13.665  0.000   23.793  22.150  0.042   13.796  1492.150    -8.962  -167.236    -8.581 
../1_emscoring/emscoring_93.pdb -   89  -46.871   6.644  0.000   10.617  11.333  0.146   6.455   1740.990    -8.906   -35.623   -30.841
../1_emscoring/emscoring_88.pdb -   90   48.283  12.919  0.000   20.484  19.885  0.053   14.706  3914.250   -68.786  -129.461   142.961
../1_emscoring/emscoring_87.pdb -   91  180.468  12.447  0.000   22.153  19.299  0.048   14.160  3639.430   -66.857  -240.130   295.351
../1_emscoring/emscoring_86.pdb -   92  240.307  12.572  0.000   21.662  19.799  0.049   14.187  3535.820   -69.380  -154.703   340.628
../1_emscoring/emscoring_85.pdb -   93  781.210  15.174  0.000   23.497  24.993  0.042   17.151  3278.340   -61.261   -86.026   859.677
  </pre>
</details>
<br>

<a class="prompt prompt-question">
Inspect more closely the reported scores above? Can you discover something peculiar with the buried surface area?
</a>

<a class="prompt prompt-question">
How can you explain that?
</a>

**_Hint 1_**: The HADDOCK score is calculated over all existing interfaces defined by different chainIDs.

**_Hint 2_**: Visualise two of the models with very different BSA values, color-coding the chains.

<hr>
<hr>

## Congratulations! 🎉

You have completed this tutorial. If you have any questions or suggestions, feel free to contact us via email or asking a question through our [support center](https://ask.bioexcel.eu){:target="_blank"}.

And check also our [education](/education){:target="_blank"} web page where you will find more tutorials!

<hr>
<hr>

<!-- Links -->
[air-help]: https://www.bonvinlab.org/software/haddock2.4/airs/ "AIRs help"
[gentbl]: https://wenmr.science.uu.nl/gentbl/ "GenTBL"
[haddock24protein]: /education/HADDOCK24/HADDOCK24-protein-protein-basic/
[haddock-repo]: https://github.com/haddocking/haddock3 "HADDOCK3 GitHub"
[haddock-tools]: https://github.com/haddocking/haddock-tools "HADDOCK tools GitHub"
[installation]: https://www.bonvinlab.org/haddock3/INSTALL.html "Installation"
[link-cns]: https://cns-online.org "CNS online"
[link-forum]: https://ask.bioexcel.eu/c/haddock "HADDOCK Forum"
[link-freesasa]: https://freesasa.github.io "FreeSASA"
[nat-pro]: https://www.nature.com/articles/s41596-024-01011-0.epdf?sharing_token=UHDrW9bNh3BqijxD2u9Xd9RgN0jAjWel9jnR3ZoTv0O8Cyf_B_3QikVaNIBRHxp9xyFsQ7dSV3t-kBtpCaFZWPfnuUnAtvRG_vkef9o4oWuhrOLGbBXJVlaaA9ALOULn6NjxbiqC2VkmpD2ZR_r-o0sgRZoHVz10JqIYOeus_nM%3D "Nature protocol"
[tbl-examples]: https://github.com/haddocking/haddock-tools/tree/master/haddock_tbl_validation "tbl examples"
