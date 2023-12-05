---
layout: page
title: "Low-sampling antibody-antigen modelling tutorial using a local version of HADDOCK3"
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
attack and destroy the pathogen. Antibodies can be highly specific while showing low immunogenicity,
which is achieved by their unique structure. **The fragment crystallizable region (Fc region)**
activates the immune response and is species-specific, i.e. the human Fc region should not
induce an immune response in humans.  **The fragment antigen-binding region (Fab region**)
needs to be highly variable to be able to bind to antigens of various nature (high specificity).
In this tutorial we will concentrate on the terminal **variable domain (Fv)** of the Fab region.

<figure style="text-align: center;">
  <img src="/education/HADDOCK24/HADDOCK24-antibody-antigen/antibody_described.png">
</figure>

The small part of the Fab region that binds the antigen is called **paratope**. The part of the antigen
that binds to an antibody is called **epitope**. The paratope consists of six highly flexible loops,
known as **complementarity-determining regions (CDRs)** or hypervariable loops whose sequence
and conformation are altered to bind to different antigens. CDRs are shown in red in the figure below:

<figure style="text-align: center;">
  <img src="/education/HADDOCK24/HADDOCK24-antibody-antigen/CDRs.png">
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

## Setup/Requirements

In order to follow this tutorial you will need to work on a Linux or MacOSX system. We will also make use of [**PyMOL**][link-pymol] (freely available for most operating systems) in order to visualize the input and output data.

### PyMOL on the DEVANA cluster
It is possible to run PyMOL directly on DEVANA by connecting to the [DEVANA Desktop application](https://ood.devana.nscc.sk/pun/sys/dashboard/batch_connect/sessions). There, you can start a Desktop session by specifying the **testing** partition and 1 as the number of cores.

Once logged in, you can start a terminal in the DEVANA Desktop emulator. From there, you can start PyMOL by typing:
<a class="prompt prompt-cmd">
module load PyMOL
</a>
and then
<a class="prompt prompt-cmd">
pymol
</a>

Further we are providing pre-processed PDB files for docking and analysis (but the preprocessing of those files will also be explained in this tutorial). The files have been processed
to facilitate their use in HADDOCK and for allowing comparison with the known reference structure of the complex.

For this, navigate through the terminal to the tutorial directory:

<details>
  <summary style="bold">
  Cagliari<i class="material-icons">expand_more</i>
 </summary>
  
  <a class="prompt prompt-cmd">
  cd /home/utente/BioExcel_SS_2023/HADDOCK
  </a>
  <br>
</details>

### Bratislava

  Please connect to the DEVANA supercomputer using your credentials, either using SSH or accessing [this page](https://ood.devana.nscc.sk/pun/sys/shell/ssh/login01)

  From your home directory, navigate to the tutorial directory:
  <a class="prompt prompt-cmd">
  cd HADDOCK
  </a>
  

In it you should find the following directories and files:

* `pdbs`: Contains the pre-processed PDB files
* `restraints`: Contains the interface information and the corresponding restraint files for HADDOCK
* `runs`: Contains pre-calculated run results for the various protocols in this tutorial
* `scripts`: Contains a variety of scripts used in this tutorial
* `docking-antibody-antigen-CDR-NMR-CSP*.cfg`: the different HADDOCK3 configuration files that can be used in the tutorial

<hr>

If you are working from your own computer please download [this zip archive](https://surfdrive.surf.nl/files/index.php/s/2NbStaQ4ub5Vgv1). Remember that on your local machine you'll have to install CNS and HADDOCK3.

## HADDOCK general concepts

HADDOCK (see [https://www.bonvinlab.org/software/haddock2.4](https://www.bonvinlab.org/software/haddock2.4){:target="_blank"})
is a collection of python scripts derived from ARIA ([https://aria.pasteur.fr](https://aria.pasteur.fr){:target="_blank"})
that harness the power of CNS (Crystallography and NMR System – [https://cns-online.org](https://cns-online.org){:target="_blank"})
for structure calculation of molecular complexes. What distinguishes HADDOCK from other docking software is its ability,
inherited from CNS, to incorporate experimental data as restraints and use these to guide the docking process alongside
traditional energetics and shape complementarity. Moreover, the intimate coupling with CNS endows HADDOCK with the
ability to actually produce models of sufficient quality to be archived in the Protein Data Bank.

A central aspect to HADDOCK is the definition of Ambiguous Interaction Restraints or AIRs. These allow the
translation of raw data such as NMR chemical shift perturbation or mutagenesis experiments into distance
restraints that are incorporated in the energy function used in the calculations. AIRs are defined through
a list of residues that fall under two categories: active and passive. Generally, active residues are those
of central importance for the interaction, such as residues whose knockouts abolish the interaction or those
where the chemical shift perturbation is higher. Throughout the simulation, these active residues are
restrained to be part of the interface, if possible, otherwise incurring in a scoring penalty. Passive residues
are those that contribute for the interaction, but are deemed of less importance. If such a residue does
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
<img width="75%" src="../HADDOCK3-antibody-antigen/HADDOCK2-stages.png">
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
<img width="75%" src="../HADDOCK3-antibody-antigen/HADDOCK3-workflow-scheme.png">
</figure>

To keep HADDOCK3 modules organized, we catalogued them into several
categories. But, there are no constraints on piping modules of different
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
    * `caprieval`: *Calculates CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ) with respect to the top scoring model or reference structure if provided.*
    * `clustfcc`: *Clusters models based on the fraction of common contacts (FCC)*
    * `clustrmsd`: *Clusters models based on pairwise RMSD matrix calculated with the `rmsdmatrix` module.*
    * `rmsdmatrix`: *Calculates the pairwise RMSD matrix between all the models generated in the previous step.*
    * `seletop`: *Selects the top N models from the previous step.*
    * `seletopclusts`: *Selects top N clusters from the previous step.*

The HADDOCK3 workflows are defined in simple configuration text files, similar to the TOML format but with extra features.
Contrarily to HADDOCK2.X which follows a rigid (yet highly parameterisable)
procedure, in HADDOCK3, you can create your own simulation workflows by
combining a multitude of independent modules that perform specialized tasks.


<hr>
<hr>

## Software requirements


### Installing CNS
The other required piece of software to run HADDOCK is its computational engine,
CNS (Crystallography and NMR System –
[https://cns-online.org](https://cns-online.org){:target="_blank"}). CNS is
freely available for non-profit organizations. In order to get access to all
features of HADDOCK you will need to compile CNS using the additional files
provided in the HADDOCK distribution in the `varia/cns1.3` directory. Compilation of
CNS might be non-trivial. Some guidance on installing CNS is provided in the online
HADDOCK3 documentation page [here](https://www.bonvinlab.org/haddock3/CNS.html){:target="_blank"}.

In this tutorial CNS has already been installed, so you don't have to worry.


### Installing HADDOCK3

In this tutorial we will make use of the HADDOCK3 version. HADDOCK3 is already pre-installed in your system.

To make sure the HADDOCK3 is properly installed
<details>
  <summary style="bold">
  Cagliari<i class="material-icons">expand_more</i>
 </summary>

  activate its conda environment:

  <a class="prompt prompt-cmd">
  conda activate haddock3
  </a>
</details>
 
### Bratislava

  load the Python 3.9.6 module:

  <a class="prompt prompt-cmd">
  module load Python/3.9.6-GCCcore-11.2.0
  </a>

  and then source the HADDOCK3 environment:
  <a class="prompt prompt-cmd">
  source /home/projects/training-05/.haddock3-env/bin/activate
  </a>

and then type

<a class="prompt prompt-cmd">
haddock3 -h
</a>

in the terminal. You should see a small help message explaining how to use the software.

In case you want to obtain HADDOCK3 for another platform, navigate to [its repository][haddock-repo], fill the
registration form, and then follow the [installation instructions](https://www.bonvinlab.org/haddock3/INSTALL.html){:target="_blank"}.


### Auxiliary software

**[PDB-tools][link-pdbtools]**: A useful collection of Python scripts for the
manipulation (renumbering, changing chain and segIDs...) of PDB files is freely
available from our GitHub repository. `pdb-tools` is automatically installed
with HADDOCK3. If you have activated the HADDOCK3 Python environment you have
access to the pdb-tools package.

**[PyMol][link-pymol]**: We will make use of PyMol for visualization. If not already installed on your system, download and install PyMol.

<hr>
<hr>

## Preparing PDB files for docking

In this section we will prepare the PDB files of the antibody and antigen for docking.
Crystal structures of both the antibody and the antigen in their free forms are available from the
[PDBe database](https://www.pdbe.org){:target="_blank"}. In the case of the antibody which consists
of two chains (L+H) we will have to prepare it for use in HADDOCK such as it can be treated as
a single chain with non-overlapping residue numbering. For this we will be making use of `pdb-tools` from the command line.

_**Note**_ that `pdb-tools` is also available as a [web service](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.


<hr>

### Preparing the antibody structure

Using PDB-tools we will download the unbound structure of the antibody from the PDB database (the PDB ID is [4G6K](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k){:target="_blank"}) and then process it to have a unique chain ID (A) and non-overlapping residue numbering by renumbering the merged pdb (starting from 1).

This can be done from the command line with:

<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy -strict | pdb_selchain -H | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_selres -1:120 | pdb_tidy -strict > 4G6K_H.pdb
</a>
<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy -strict | pdb_selchain -L | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_selres -1:107 | pdb_tidy -strict > 4G6K_L.pdb
</a>
<a class="prompt prompt-cmd">
pdb_merge 4G6K_H.pdb 4G6K_L.pdb | pdb_reres -1 | pdb_chain -A | pdb_chainxseg | pdb_reres -1 | pdb_tidy -strict > 4G6K_clean.pdb
</a>

The first command fetches the PDB ID, selects the heavy chain (H) and removes water and heteroatoms (in this case no co-factor is present that should be kept).
An important part for antibodies is the `pdb_fixinsert` command that fixes the residue numbering of the HV loops: Antibodies often follow the [Chothia numbering scheme](https://pubmed.ncbi.nlm.nih.gov/9367782/?otool=inluulib){:target="_blank"} and insertions created by this numbering scheme (e.g. 82A, 82B, 82C) cannot be processed by HADDOCK directly. As such renumbering is necessary before starting the docking. Then, the command `pdb_selres` selects only the residues from 1 to 120, so as to consider only the variable domain (FV) of the antibody. This allows to save a substantial amount of computational resources.

The second command does the same for the light chain (L) with the difference that the light chain is slightly shorter and we can focus on the first 107 residues.

The third and last command merges the two processed chains and assign them unique chain and segIDs, resulting in the HADDOCK-ready `4G6K_clean.pdb` file. You can view its sequence running:

<a class="prompt prompt-cmd">
pdb_tofasta 4G6K_clean.pdb
</a>

_**Note**_ that the corresponding files can be found in the `pdbs` directory of the archive you downloaded.

<hr>

### Machine-learning-based modelling of antibodies

The release of Alphafold2 in late 2020 has brought structure prediction methods to a new frontier, providing accurate models for the majority of known proteins. This revolution did not spare antibodies, with [Alphafold2-multimer](https://github.com/sokrypton/ColabFold) and other prediction methods (most notably [ABodyBuilder2](https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/abodybuilder2/), from the ImmuneBuilder suite) performing nicely on the variable regions.

For a short introduction to AI and AlphaFold refer to this other tutorial [introduction](/education/molmod_online/alphafold/#introduction){:target="_blank"}.

CDR loops are clearly the most challenging region to be predicted given their high sequence variability and flexibility. Multiple Sequence Alignment (MSA)-derived information is also less useful in this context.

Here we will see whether the antibody models given by Alphafold2-multimer and ABodyBuilder2 can be used to target the antigen in place of the standard unbound form, which is not usually available.

We already ran the prediction with these two tools, and you can find them in the `pdbs` directory (with names `4g6k_Abodybuilder2.pdb` and `4g6k_AF2_multimer.pdb`).

Let's preprocess these models!

<a class="prompt prompt-cmd">
pdb_tidy -strict pdbs/4g6k_Abodybuilder2.pdb | pdb_selchain -H | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_tidy -strict > 4G6K_abb_H.pdb
</a>
<a class="prompt prompt-cmd">
pdb_tidy -strict pdbs/4g6k_Abodybuilder2.pdb | pdb_selchain -L | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_tidy -strict > 4G6K_abb_L.pdb
</a>
<a class="prompt prompt-cmd">
 pdb_merge 4G6K_abb_H.pdb 4G6K_abb_L.pdb | pdb_chain -A | pdb_chainxseg | pdb_reres -1 | pdb_tidy -strict > 4G6K_abb_clean.pdb
</a>

Now the Alphafold2-multimer top ranked structure. By default it is written to disk with chains A and B.

<a class="prompt prompt-cmd">
pdb_tidy -strict pdbs/4g6k_AF2_multimer.pdb | pdb_selchain -A | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_tidy -strict > 4g6k_af2_A.pdb
</a>
<a class="prompt prompt-cmd">
pdb_tidy -strict pdbs/4g6k_AF2_multimer.pdb | pdb_selchain -B | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_tidy -strict > 4g6k_af2_B.pdb
</a>
<a class="prompt prompt-cmd">
pdb_merge 4g6k_af2_A.pdb 4g6k_af2_B.pdb | pdb_chain -A | pdb_chainxseg | pdb_reres -1 | pdb_tidy -strict > 4G6K_af2_clean.pdb
</a>

Let's load the three cleaned antibody structures in Pymol to see whether they resemble the experimental unbound structure.

<a class="prompt prompt-pymol">
File menu -> Open -> select 4G6K_clean.pdb
</a>
<a class="prompt prompt-pymol">
File menu -> Open -> select 4G6K_abb_clean.pdb
</a>
<a class="prompt prompt-pymol">
File menu -> Open -> select 4G6K_af2_clean.pdb
</a>

We now use the backbone RMSD to align the machine learning models to the experimental structure.
<a class="prompt prompt-pymol">
alignto 4G6K_clean
</a>

<a class="prompt prompt-question">
Which structure (between _4G6K_abb_clean.pdb_ and _4G6K_af2_clean.pdb_) is closer to the unbound conformation?
</a>

Both ABodyBuilder2 and Alphafold2 can give an _ensemble_ of models in output. All the structures in these ensembles may be used as input antibody molecules in HADDOCK.

<a class="prompt prompt-info">The remaining of the tutorial will consider only the experimental unbound structure, but you can use your preprocessed predicted structures simply by substituting _4G6K_clean.pdb_ with either _4G6K_abb_clean.pdb_ or _4G6K_af2_clean.pdb_.</a>

### Preparing the antigen structure

Using PDB-tools we will download the structure from the PDB database (the PDB ID is [4I1B](https://www.ebi.ac.uk/pdbe/entry/pdb/4i1b){:target="_blank"}), remove the hetero atoms and then process it to assign it chainID B.

<a class="prompt prompt-cmd">
pdb_fetch 4I1B | pdb_tidy -strict | pdb_delhetatm  | pdb_keepcoord | pdb_chain -B | pdb_chainxseg | pdb_tidy -strict > 4I1B_clean.pdb
</a>

<hr>
<hr>

## Defining restraints for docking

Before setting up the docking we need first to generate distance restraint files
in a format suitable for HADDOCK.  HADDOCK uses [CNS][link-cns]{:target="_blank"} as computational
engine. A description of the format for the various restraint types supported by
HADDOCK can be found in our [Nature Protocol][nat-pro]{:target="_blank"} paper, Box 4.

Distance restraints are defined as:

<pre style="background-color:#DAE4E7">
assign (selection1) (selection2) distance, lower-bound correction, upper-bound correction
</pre>

The lower limit for the distance is calculated as: distance minus lower-bound
correction and the upper limit as: distance plus upper-bound correction.  The
syntax for the selections can combine information about chainID - `segid`
keyword -, residue number - `resid` keyword -, atom name - `name` keyword.
Other keywords can be used in various combinations of OR and AND statements.
Please refer for that to the [online CNS manual](http://cns-online.org/v1.3/){:target="_blank"}.

We will shortly explain in this section how to generate both ambiguous
interaction restraints (AIRs) and specific distance restraints for use in
HADDOCK illustrating a scenario in which no _a priori_ knowledge is available
about the antibody binding site, but in which the antigen epitope has been pinpointed
by an NMR chemical shift perturbation experiment.

Information about various types of distance restraints in HADDOCK can also be
found in our [online manual][air-help]{:target="_blank"} pages.

<hr>

### Identifying the paratope of the antibody

Nowadays there are several computational tools that can identify the paratope (the residues of the hypervariable loops involved in binding) from the provided antibody sequence. In this tutorial we are providing you the corresponding list of residue obtained using [ProABC-2](https://wenmr.science.uu.nl/proabc2/){:target="_blank"}. ProABC-2 uses a convolutional neural network to identify not only residues which are located in the paratope region but also the nature of interactions they are most likely involved in (hydrophobic or hydrophilic). The work is described in [Ambrosetti, *et al* Bioinformatics, 2020](https://academic.oup.com/bioinformatics/article/36/20/5107/5873593){:target="_blank"}.

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

We will now highlight the predicted paratope. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all
</a>
<a class="prompt prompt-pymol">
select paratope, (resi 31+32+33+34+35+52+54+55+56+100+101+102+103+104+105+106+151+152+169+170+173+211+212+213+214+216)<br>
</a>
<a class="prompt prompt-pymol">
color red, paratope
</a>

<a class="prompt prompt-question">
Can you identify the H3 loop? H stands for heavy chain (the first domain in our case with lower residue numbering). H3 is typically the longest loop.
</a>

Let us now switch to a surface representation to inspect the predicted binding site.

<a class="prompt prompt-pymol">
color white, all
</a>
<a class="prompt prompt-pymol">
show surface<br>
</a>
<a class="prompt prompt-pymol">
color red, paratope
</a>

Inspect the surface.

<a class="prompt prompt-question">
Do the identified residues form a well defined patch on the surface?
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See surface view of the paratope</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="50%" src="../HADDOCK3-antibody-antigen/antibody-paratope.png">
  </figure>
  <br>
</details>

<hr>

### Antigen: NMR-mapped epitope information

The article describing the crystal structure of the antibody-antigen complex we are modelling also reports
on experimental NMR chemical shift titration experiments to map the binding site of the antibody (gevokizumab)
on Interleukin-1β. The residues affected by binding are listed in Table 5 of
[Blech et al. JMB 2013](https://dx.doi.org/10.1016/j.jmb.2012.09.021){:target="_blank"}:

<figure style="text-align: center;">
  <img width="50%" src="/education/HADDOCK24/HADDOCK24-antibody-antigen-basic/Table5-Blech.png">
</figure>

The list of binding site (epitope) residues identified by NMR is:

<pre style="background-color:#DAE4E7">
72,73,74,75,81,83,84,89,90,92,94,96,97,98,115,116,117
</pre>

We will now visualize the epitope on Interleukin-1β. For this start PyMOL and from the PyMOL File menu open the provided PDB file of the antigen.

<a class="prompt prompt-pymol">
File menu -> Open -> select 4I1B_clean.pdb
</a>

<a class="prompt prompt-pymol">
color white, all
</a>
<a class="prompt prompt-pymol">
show surface
</a>
<a class="prompt prompt-pymol">
select epitope, (resi 72+73+74+75+81+83+84+89+90+92+94+96+97+98+115+116+117)
</a>
<a class="prompt prompt-pymol">
color red, epitope
</a>

Inspect the surface.

<a class="prompt prompt-question">
Do the identified residues form a well defined patch on the surface?
</a>

The answer to that question should be yes, but we can see some residues not colored that might also be involved in the binding - there are some white spots around/in the red surface.

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See surface view of the epitope identified by NMR</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="50%" src="../HADDOCK3-antibody-antigen/antigen-epitope.png">
  </figure>
  <br>
</details>

<br>

In HADDOCK we are dealing with potentially incomplete binding sites by defining surface neighbors as `passive` residues.
These are added to the definition of the interface but will not lead to any energetic penalty if they are not part of the
binding site in the final models, while the residues defined as `active` (typically the identified or predicted binding
site residues) will. When using the HADDOCK server, `passive` residues will be automatically defined. Here since we are
using a local version, we need to define those manually.

This can easily be done in the following way:

<a class="prompt prompt-cmd">
haddock3-restraints passive_from_active 4I1B_clean.pdb 72,73,74,75,81,83,84,89,90,92,94,96,97,98,115,116,117
</a>

The NMR-identified residues and their surface neighbors generated with the above command can be used to define ambiguous interactions restraints, either using the NMR identified residues as active in HADDOCK, or combining those with the surface neighbors and use this combination as passive only. We will focus only on this second case here: the corresponding residues can be found in the `restraints/antigen-NMR-epitope.act-pass` file.
The file consists of two lines, with the first one defining the `active` residues and
the second line the `passive` ones. We will use later these files to generate the ambiguous distance restraints for HADDOCK.

In general it is better to be too generous rather than too strict in the definition of passive residues.

An important aspect is to filter both the active (the residues identified from
your mapping experiment) and passive residues by their solvent accessibility.
Our web service uses a default relative accessibility of 15% as cutoff. This is
not a hard limit. You might consider including even more buried residues if some
important chemical group seems solvent accessible from a visual inspection.

<hr>


### Defining ambiguous restraints

Once you have defined your active and passive residues for both molecules, you
can proceed with the generation of the ambiguous interaction restraints (AIR) file for HADDOCK.
For this you can either make use of our online [GenTBL][gentbl] web service, entering the
list of active and passive residues for each molecule, and saving the resulting
restraint list to a text file, or use the relevant `haddock3-restraints` command.

To use our `haddock3-restraints active_passive_to_ambig` script you need to
create for each molecule a file containing two lines:

* The first line corresponds to the list of active residues (numbers separated by spaces)
* The second line corresponds to the list of passive residues.

In this scenario the NMR epitope is defined as active (meaning ambiguous distance restraints will be defined from the NMR epitope residues) and the surface neighbors are used as passive residues in HADDOCK.

* For the antibody we will use the file `antibody-paratope.act-pass` from the `restraints` directory:
<pre style="background-color:#DAE4E7">
1 32 33 34 35 52 54 55 56 100 101 102 103 104 105 106 151 152 169 170 173 211 212 213 214 216

</pre>

* and for the antigen (the file called `antigen-NMR-epitope.act-pass` from the `restraints` directory):
<pre style="background-color:#DAE4E7">
72 73 74 75 81 83 84 89 90 92 94 96 97 98 115 116 117
3 24 46 47 48 50 66 76 77 79 80 82 86 87 88 91 93 95 118 119 120
</pre>

Using those two files, we can generate the CNS-formatted AIR restraint files with the following command:

<a class="prompt prompt-cmd">
haddock3-restraints active_passive_to_ambig ./restraints/antibody-paratope.act-pass ./restraints/antigen-NMR-epitope.act-pass > ambig-paratope-NMR-epitope.tbl
</a>

This generates a file called `ambig-paratope-NMR-epitope.tbl` that contains the AIR
restraints. The default distance range for those is between 0 and 2Å, which
might seem short but makes senses because of the 1/r^6 summation in the AIR
energy function that makes the effective distance be significantly shorter than
the shortest distance entering the sum.

The effective distance is calculated as the SUM over all pairwise atom-atom
distance combinations between an active residue and all the active+passive on
the other molecule: SUM[1/r^6]^(-1/6).

If you modify manually this file, it is possible to quickly check if the format is valid.

<a class="prompt prompt-cmd">
haddock3-restraints validate_tbl ambig-paratope-NMR-epitope.tbl --silent
</a>

No output means that your TBL file is valid.

<hr>

### Additional restraints for multi-chain proteins

As an antibody consists of two separate chains, it is important to define a few distance restraints
to keep them together during the high temperature flexible refinement stage of HADDOCK. This can easily be
done using the `haddock3-restraints restrain_bodies` subcommand.

<a class="prompt prompt-cmd">
haddock3-restraints restrain_bodies 4G6K_clean.pdb > antibody-unambig.tbl
</a>

The result file contains two CA-CA distance restraints with the exact distance measured between the picked CA atoms:

<pre style="background-color:#DAE4E7">
  assign (segid A and resi 110 and name CA) (segid A and resi 132 and name CA) 47.578 0.0 0.0
  assign (segid A and resi 97 and name CA) (segid A and resi 204 and name CA) 33.405 0.0 0.0
</pre>

This file is also provided in the `restraints` directory of the archive you downloaded.

If you are considering Alphafold2 or ABodyBuilder2 antibodies you have to create the appropriate distance restraints:

<a class="prompt prompt-cmd">
haddock3-restraints restrain_bodies 4G6K_af2_clean.pdb > af2-antibody-unambig.tbl
</a>

<a class="prompt prompt-cmd">
haddock3-restraints restrain_bodies 4G6K_abb_clean.pdb > abb-antibody-unambig.tbl
</a>

<hr>
<hr>

## Setting up the docking with HADDOCK3

Now that we have all required files at hand (PDB and restraints files) it is time to setup our docking protocol. The idea is to execute a fast HADDOCK3 docking workflow reducing the non-negligible computational cost of HADDOCK by decreasing the sampling, without impacting too much the accuracy of the resulting models.
For this we need to create a HADDOCK3 configuration file that will define the docking workflow. In contrast to HADDOCK2.X,
we have much more flexibility in doing this. As an example, we could use this flexibility by introducing a clustering step
after the initial rigid-body docking stage, select up to 4 models per cluster and refine all of those.

HADDOCK3 also provides an analysis module (`caprieval`) that allows
to compare models to either the best scoring model (if no reference is given) or a reference structure, which in our case
we have at hand. This will directly allow us to assess the performance of the protocol.

The basic workflow will consists of the following modules:

1. **`topoaa`**: *Generates the topologies for the CNS engine and build missing atoms*
2. **`rigidbody`**: *Rigid body energy minimisation (`it0` in haddock2.x)*
3. **`caprieval`**: *Calculates CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ) with respect to the top scoring model or reference structure if provided*
4. **`seletop`** : *Selection of the top X models from the previous module*
5. **`flexref`**: *Semi-flexible refinement of the interface (`it1` in haddock2.4)*
6. **`caprieval`**
7. **`emref`**: *Final refinement by energy minimisation (`itw` EM only in haddock2.4)*
8. **`caprieval`**
9. **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
10. **`seletopclusts`**: *Selection of the top10 models of all clusters*
11. **`caprieval`**
<hr>

### HADDOCK3 execution modes

HADDOCK3 currently supports three difference execution modes that are defined in the first section of the configuration file of a run:

- **local mode** : in this mode HADDOCK3 will run on the current system, using the defined number of cores (`ncores`) in the config file to a maximum of the total number of available cores on the system minus one;
- **HPC/batch mode**: in this mode HADDOCK3 will typically be started on your local server (e.g. the login node) and will dispatch jobs to the batch system of your cluster;
- **MPI mode**: HADDOCK3 supports a parallel MPI implementation (functional but still very experimental at this stage).

## Cagliari
  
In this tutorial we are using local resources (our laptops), and therefore we will stick to the **local** mode. For the tutorial we limit the number of cores to 12, that is, the maximum number ofavailable cores on your computer.

Make sure your `haddock3` conda environment is active:

<a class="prompt prompt-cmd">
conda activate haddock3
</a>


## Bratislava
  
  In this tutorial we are using local resources of remote nodes on DEVANA, and therefore we will stick to the **local** mode. For the tutorial we limit the number of cores to 12, so as to avoid overloading the nodes.

<hr>

### Docking Scenario: Paratope - NMR-epitope

Now that we have all data ready it is time to setup the docking. Here we are using the NMR-identified epitope, which is treated as active, meaning restraints will be defined from it to "force" it to be at the interface.

The restraint file to use for this is `ambig-paratope-NMR-epitope.tbl`. We will also define the restraints to keep the two antibody chains together using for this the `antibody-unambig.tbl` restraint file.

<a class="prompt prompt-info">If you are using the Alphafold2 antibody you should use the *af2-antibody-unambig.tbl* file.</a>

<a class="prompt prompt-info">If you are using the ABodyBuilder2 antibody you should use the *abb-antibody-unambig.tbl* file.</a>

In this case since we have information for both interfaces we use a low-sampling configuration file, which takes only a small amount of computational resources to run. The configuration file for this scenario (assuming a local running mode, eventually submitted to the batch system requesting a full node) is:

{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen (as active)
# and keeping the random removal of restraints
# ====================================================================

# directory name of the run
run_dir = "run1-CDR-NMR-CSP"

# compute mode
mode = "local"
#  12 local cores
ncores = 12

# Self contained rundir (to avoid problems with long filename paths)
self_contained = true

# Post-processing to generate statistics and plots
postprocess = true

# molecules to be docked
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
sampling = 96

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[seletop]
select = 48

[flexref]
tolerance = 5
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[emref]
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[clustfcc]

[seletopclusts]

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

# ====================================================================

{% endhighlight %}

The idea of this configuration file is to generate 96 models with the standard rigid-body energy minimization (*rigidbody* module). Only the 48 best scoring models are selected (*seletop* module) for flexible refinement (*flexref* module). Refined modes are then subject to a short energy minimisation in the OPLS force field (*emref*). FCC clustering (*clustfcc*) is applied at the end of the workflow to group together models sharing a consistent fraction of the interface contacts. The top 4 models of each cluster are saved to disk (*seletopclusts*). Multiple *caprieval* modules are executed at different stages of the workflow to check how the quality (and rankings) of the models change throughout the protocol.


<details>
  <summary style="bold">
  Cagliari<i class="material-icons">expand_more</i>
 </summary>
  
  This configuration file is provided in the `/home/utente/BioExcel_SS_2023/HADDOCK` directory on your laptop as `docking-antibody-antigen-CDR-NMR-CSP.cfg` (`docking-antibody-antigen-CDR-NMR-CSP-af2.cfg` and `docking-antibody-antigen-CDR-NMR-CSP-abb.cfg` for Alphafold2 and ABodyBuilder2 antibodies, respectively).

  If you want to use your own pdb and restraint files please change the paths in the configuration files (for example from `pdbs/4G6K_clean.pdb` to `4G6K_abb_clean.pdb`).

  If you have everything ready, you can launch haddock3 from the command line.

  <a class="prompt prompt-cmd">
  haddock3 docking-antibody-antigen-CDR-NMR-CSP.cfg
  </a>  
</details>


## Bratislava
  
  This configuration file is provided in the `HADDOCK` directory within your home folder on DEVANA as `docking-antibody-antigen-CDR-NMR-CSP.cfg` (`docking-antibody-antigen-CDR-NMR-CSP-af2.cfg` and `docking-antibody-antigen-CDR-NMR-CSP-abb.cfg` for Alphafold2 and ABodyBuilder2 antibodies, respectively).

  If you want to use your own pdb and restraint files please change the paths in the configuration files (for example from `pdbs/4G6K_clean.pdb` to `4G6K_abb_clean.pdb`).

  If you have everything ready, we can submit our haddock3 run to the cluster.

  <a class="prompt prompt-cmd">
  sbatch run-haddock3.job
  </a>

<hr>

## Analysis of docking results

In case something went wrong with the docking (or simply if you don't want to wait for the results) you can find the following precalculated runs in the `runs` directory:
- `run1-CDR-NMR-CSP`: run started using the unbound antibody
- `run1-CDR-NMR-CSP-af2`: run started using the Alphafold-multimer antibody
- `run1-CDR-NMR-CSP-abb`: run started using the Immunebuilder antibody

### Structure of the run directory

Once your run has completed inspect the content of the resulting directory. You will find the various steps (modules) of the defined workflow numbered sequentially, e.g.:

{% highlight shell %}
> ls run1-CDR-NMR-CSP/
    0_topoaa/
    1_rigidbody/
    2_caprieval/
    3_seletop/
    4_flexref/
    5_caprieval/
    6_emref/
    7_caprieval
    8_clustfcc/
    9_seletopclusts/
    10_caprieval/
    analysis/
    data/
    log
{% endhighlight %}

There is in addition the log file (text file) and two additional directories:

- the `data` directory containing the input data (PDB and restraint files) for the various modules
- the `analysis` directory containing various plots to visualise the results for each `caprieval` step

You can find information about the duration of the run at the bottom of the log file. Each sampling/refinement/selection module will contain PDB files.

For example, the `09_seletopclusts` directory contains the selected models from each cluster. The clusters in that directory are numbered based
on their rank, i.e. `cluster_1` refers to the top-ranked cluster. Information about the origin of these files can be found in that directory in the `seletopclusts.txt` file.

The simplest way to extract ranking information and the corresponding HADDOCK scores is to look at the `10_caprieval` directories (which is why it is a good idea to have it as the final module, and possibly as intermediate steps). This directory will always contain a `capri_ss.tsv` file, which contains the model names, rankings and statistics (score, iRMSD, Fnat, lRMSD, ilRMSD and dockq score). E.g.:

<pre style="background-color:#DAE4E7">
model                    md5     caprieval_rank     score    irmsd    fnat   lrmsd  ilrmsd   dockq      air       bsa  desolv      elec     total       vdw
../06_emref/emref_2.pdb  -       1               -164.078    2.111   0.621   5.456   4.368   0.555   96.928  2077.920   6.253  -584.597  -550.774   -63.105
../06_emref/emref_8.pdb  -       2               -144.476    1.472   0.759   2.659   2.691   0.726   43.505  2018.670   5.884  -549.010  -550.413   -44.908
../06_emref/emref_4.pdb  -       3               -138.888    1.087   0.724   2.888   1.830   0.759  116.384  1817.670   2.875  -558.618  -483.913   -41.678
../06_emref/emref_3.pdb  -       4               -138.860    0.983   0.931   1.826   1.554   0.862  100.098  1822.150   1.606  -503.198  -452.935   -49.836
../06_emref/emref_1.pdb  -       5               -138.754    1.146   0.828   1.738   1.846   0.806   36.138  1924.090   5.316  -528.536  -534.375   -41.976
../06_emref/emref_5.pdb  -       6               -138.362    0.921   0.914   1.817   1.482   0.866   73.832  1897.950   4.279  -484.430  -463.736   -53.138
../06_emref/emref_6.pdb  -       7               -138.054    1.153   0.862   2.220   1.880   0.809   63.112  1958.060   5.507  -529.438  -510.311   -43.985
../06_emref/emref_9.pdb  -       8               -134.536    1.313   0.810   2.508   2.239   0.765   63.951  1862.230   7.050  -522.799  -502.269   -43.421
../06_emref/emref_11.pdb -       9               -131.577    0.965   0.862   1.337   1.428   0.848   58.716  1905.400   9.684  -519.910  -504.344   -43.151
....
</pre>

If clustering was performed prior to calling the `caprieval` module the `capri_ss.tsv` file will also contain information about to which cluster the model belongs to and its ranking within the cluster.

The relevant statistics are:

* **score**: *the HADDOCK score (arbitrary units)*
* **irmsd**: *the interface RMSD, calculated over the interfaces the molecules*
* **fnat**: *the fraction of native contacts*
* **lrmsd**: *the ligand RMSD, calculated on the ligand after fitting on the receptor (1st component)*
* **ilrmsd**: *the interface-ligand RMSD, calculated over the interface of the ligand after fitting on the interface of the receptor (more relevant for small ligands for example)*
* **dockq**: *the DockQ score, which is a combination of irmsd, lrmsd and fnat and provides a continuous scale between 1 (exactly equal to reference) and 0*

The iRMSD, lRMSD and Fnat metrics are the ones used in the blind protein-protein prediction experiment [CAPRI](https://capri.ebi.ac.uk/) (Critical PRediction of Interactions).

In CAPRI the quality of a model is defined as (for protein-protein complexes):

* **acceptable model**: i-RMSD < 4Å or l-RMSD<10Å and Fnat > 0.1 (0.23 < DOCKQ < 0.49)
* **medium quality model**: i-RMSD < 2Å or l-RMSD<5Å and Fnat > 0.3 (0.49 < DOCKQ < 0.8)
* **high quality model**: i-RMSD < 1Å or l-RMSD<1Å and Fnat > 0.5 (DOCKQ > 0.8)

<a class="prompt prompt-question">
What is based on this CAPRI criterion the quality of the best model listed above (emref_6.pdb)?
</a>

In case the `caprieval` module is called after a clustering step an additional file will be present in the directory: `capri_clt.tsv`.
This file contains the cluster ranking and score statistics, averaged over the minimum number of models defined for clustering
(4 by default), with their corresponding standard deviations. E.g.:

<pre style="background-color:#DAE4E7">
cluster_rank	cluster_id	n	under_eval	score	score_std	irmsd	irmsd_std	fnat	fnat_std	lrmsd	lrmsd_std	dockq	dockq_std	air	air_std	bsa	bsa_std	desolv	desolv_std	elec	elec_std	total	total_std	vdw	vdw_std	caprieval_rank
1	2	10	-	-139.014	7.386	1.426	0.182	0.746	0.081	3.235	0.650	0.715	0.056	131.826	51.848	2002.760	76.340	8.397	4.920	-584.336	90.832	-496.236	89.379	-43.727	11.464	1
2	3	10	-	-120.115	6.139	14.964	0.018	0.069	0.000	23.390	0.342	0.065	0.001	189.120	18.758	1998.883	56.075	4.601	5.111	-426.788	71.303	-295.939	64.795	-58.270	8.018	2
3	1	19	-	-86.814	2.027	8.747	0.451	0.112	0.019	16.725	0.548	0.115	0.010	203.898	11.457	1554.495	32.501	7.527	1.994	-355.098	23.298	-194.910	27.573	-43.710	4.911	3
...
</pre>


In this file you find the cluster rank, the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (n) in the cluster and the corresponding statistics (averages + standard deviations). The corresponding cluster PDB files will be found in the processing `09_seletopclusts` directory.

<hr>

### Analysis

Let us now analyse the docking results. Use for that either your own run or a pre-calculated run provided in the `runs` directory.
Go into the _analysis/10_caprieval_analysis_  directory of the respective run directory and

<a class="prompt prompt-info">Inspect the final cluster statistics in _capri_clt.tsv_ file </a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the pre-calculated 10_caprieval/capri_clt.tsv file</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
cluster_rank	cluster_id	n	under_eval	    score	score_std	 irmsd irmsd_std	  fnat	fnat_std	lrmsd	lrmsd_std	  dockq	dockq_std	     air	air_std	      bsa	 bsa_std	desolv	desolv_std	     elec	elec_std	   total total_std	    vdw	vdw_std	caprieval_rank
1             1          17          -   -146.575    10.361  1.413     0.442   0.759     0.112    3.207   1.357   0.726     0.110   89.229   27.411  1934.102  116.109   4.155       1.970   -548.856   29.400  -509.509    42.520  -49.882   8.168   1
2             2          15          -   -108.943     2.131  4.978     0.092   0.134     0.014   11.239   0.427   0.194     0.009  158.010   45.857  1670.585   42.916   8.673       2.771   -344.907   20.265  -251.333    32.787  -64.436   2.947   2
3             3          5           -   -96.132     13.387  9.913     0.553   0.077     0.019   19.462   0.471   0.087     0.009  155.613   56.813  1460.395   15.293   1.130       1.740   -348.077   48.270  -235.672    68.325  -43.208   9.309   3
4             4          4           -   -87.709     10.400 14.477     0.276   0.073     0.026   23.422   0.445   0.067     0.010   99.097   12.356  1602.033  180.993   6.684       2.524   -311.045   11.794  -254.042    22.508  -42.094   8.503   4
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


We are providing in the `scripts` a simple script that extract some cluster statistics for acceptable or better clusters from the `caprieval` steps.
To use is simply call the script with as argument the run directory you want to analyze, e.g.:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats-clt.sh runs/run1-CDR-NMR-CSP
</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== runs/run1-CDR-NMR-CSP/10_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  1  out of  4
Total number of medium or better clusters:      1  out of  4
Total number of high quality clusters:          0  out of  4
 
First acceptable cluster - rank:  1  i-RMSD:  1.413  Fnat:  0.759  DockQ:  0.726
First medium cluster     - rank:  1  i-RMSD:  1.413  Fnat:  0.759  DockQ:  0.726
Best cluster             - rank:  1  i-RMSD:  1.413  Fnat:  0.759  DockQ:  0.726
</pre>
</details>

<br>

We can now do the same for runs that used Alphafold2 and ABodyBuilder2 antibodies in input:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats-clt.sh runs/run1-CDR-NMR-CSP-af2
</a>

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats-clt.sh runs/run1-CDR-NMR-CSP-abb
</a>

<a class="prompt prompt-question">According to this cluster analysis, which run produced the most accurate models?</a>

Similarly some simple statistics can be extracted from the single model `caprieval` `capri_ss.tsv` files with the `extract-capri-stats.sh` script:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats.sh ./runs/run1-CDR-NMR-CSP
</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== ./runs/run1-CDR-NMR-CSP/02_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  25  out of  96
Total number of medium or better models:      15  out of  96
Total number of high quality models:          0  out of  96
 
First acceptable model - rank:  1  i-RMSD:  2.504  Fnat:  0.328  DockQ:  0.405
First medium model     - rank:  5  i-RMSD:  1.169  Fnat:  0.828  DockQ:  0.788
Best model             - rank:  13  i-RMSD:  1.013  Fnat:  0.672  DockQ:  0.735
==============================================
== ./runs/run1-CDR-NMR-CSP/05_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  18  out of  48
Total number of medium or better models:      15  out of  48
Total number of high quality models:          4  out of  48
 
First acceptable model - rank:  1  i-RMSD:  1.107  Fnat:  0.810  DockQ:  0.805
First medium model     - rank:  1  i-RMSD:  1.107  Fnat:  0.810  DockQ:  0.805
Best model             - rank:  10  i-RMSD:  0.857  Fnat:  0.810  DockQ:  0.848
==============================================
== ./runs/run1-CDR-NMR-CSP/07_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  18  out of  48
Total number of medium or better models:      15  out of  48
Total number of high quality models:          5  out of  48
 
First acceptable model - rank:  1  i-RMSD:  2.111  Fnat:  0.621  DockQ:  0.555
First medium model     - rank:  2  i-RMSD:  1.472  Fnat:  0.759  DockQ:  0.726
Best model             - rank:  6  i-RMSD:  0.921  Fnat:  0.914  DockQ:  0.866
==============================================
== ./runs/run1-CDR-NMR-CSP/10_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  17  out of  41
Total number of medium or better models:      15  out of  41
Total number of high quality models:          5  out of  41
 
First acceptable model - rank:  1  i-RMSD:  2.111  Fnat:  0.621  DockQ:  0.555
First medium model     - rank:  2  i-RMSD:  1.472  Fnat:  0.759  DockQ:  0.726
Best model             - rank:  6  i-RMSD:  0.921  Fnat:  0.914  DockQ:  0.866
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
    In terms of iRMSD values we only observe very small differences in the best model. The fraction of native contacts and the DockQ scores are however improving much more after flexible refinement. All this will of course depend on how different are the bound and unbound conformations and the amount of data used to drive the docking process. In general, from our experience, the more and better data at hand, the larger the conformational changes that can be induced.
  </p>
</details>
<br>

<a class="prompt prompt-question">Is the best model always ranked as first?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
    This is clearly not the case. The scoring function is not perfect, but does a reasonable job in ranking models of acceptable or better quality on top in this case.
  </p>
</details>

<br>

#### Visualizing the scores and their components

By setting `postprocess=true` in the config files, interactive plots have been automatically generated in the _analysis_ directory of the run.
These are useful to visualise the scores and their components versus ranks and model quality.

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>

Models statistics:

* [iRMSD versus HADDOCK score](plots/run1-CDR-NMR-CSP/irmsd_score.html){:target="_blank"}
* [DockQ versus HADDOCK score](plots/run1-CDR-NMR-CSP/dockq_score.html){:target="_blank"}
* [DockQ versus van der Waals energy](plots/run1-CDR-NMR-CSP/dockq_vdw.html){:target="_blank"}
* [DockQ versus electrostatic energy](plots/run1-CDR-NMR-CSP/dockq_elec.html){:target="_blank"}
* [DockQ versus ambiguous restraints energy](plots/run1-CDR-NMR-CSP/dockq_air.html){:target="_blank"}
* [DockQ versus desolvation energy](plots/run1-CDR-NMR-CSP/dockq_desolv.html){:target="_blank"}

Cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank):

* [HADDOCK scores](plots/run1-CDR-NMR-CSP/score_clt.html){:target="_blank"}
* [van der Waals energies](plots/run1-CDR-NMR-CSP/vdw_clt.html){:target="_blank"}
* [electrostatic energies](plots/run1-CDR-NMR-CSP/elec_clt.html){:target="_blank"}
* [ambiguous restraints energies](plots/run1-CDR-NMR-CSP/air_clt.html){:target="_blank"}
* [desolvation energies](plots/run1-CDR-NMR-CSP/desolv_clt.html){:target="_blank"}

<a class="prompt prompt-question">For this antibody-antigen case, which of the score component is correlating best with the quality of the models?.</a>

You can also access the full analysis report on your web browser:

<a class="prompt prompt-cmd">
firefox HADDOCK/runs/run1-CDR-NMR-CSP/analysis/10_caprieval_analysis/report.html
</a>

<hr>

### Comparing the performance of the three antibodies

All three antibody structures used in input give good results. The unbound and the ABodyBuilder2 antibodies provided better results, with the best cluster showing models within 1 angstrom of interface-RMSD with respect to the unbound structure. Using the Alphafold2 structure in this case is not the best option, as the input antibody is not perfectly modelled in its H3 loop.

The good information about the paratope with the NMR epitope is critical for the good docking performance, which is also the scenario described in our Structure 2020 article:

* F. Ambrosetti, B. Jiménez-García, J. Roel-Touris and A.M.J.J. Bonvin. [Modeling Antibody-Antigen Complexes by Information-Driven Docking](https://doi.org/10.1016/j.str.2019.10.011). _Structure_, *28*, 119-129 (2020). Preprint freely available from [here](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3362436).

<hr>
<hr>

## Visualization of the models

To visualize the models from top cluster of your favorite run,  start PyMOL and load the cluster representatives you want to view, e.g. this could be the top model from cluster1 for run `run1-CDR-NMR-CSP`.
These can be found in the `runs/run1-CDR-NMR-CSP/09_seletopclusts/` directory

<a class="prompt prompt-pymol">File menu -> Open -> select cluster_1_model_1.pdb</a>

If you want to get an impression of how well defined a cluster is, repeat this for the best N models you want to view (`cluster_1_model_X.pdb`).
Also load the reference structure from the `pdbs` directory, `4G6M-matched.pdb`.

Once all files have been loaded, type in the PyMOL command window:

<a class="prompt prompt-pymol">
show cartoon
</a>
<a class="prompt prompt-pymol">
util.cbc
</a>
<a class="prompt prompt-pymol">
color yellow, 4G6M_matched
</a>

Let us then superimpose all models on the reference structure:

<a class="prompt prompt-pymol">
alignto 4G6M_matched
</a>

<a class="prompt prompt-question">
How close are the top4 models to the reference? Did HADDOCK do a good job at ranking the best in the top?
</a>

Let’s now check if the active residues which we have defined (the paratope and epitope) are actually part of the interface. In the PyMOL command window type:

<a class="prompt prompt-pymol">
select paratope, (resi 31+32+33+34+35+52+54+55+56+100+101+102+103+104+105+106+151+152+169+170+173+211+212+213+214+216 and chain A)
</a>
<a class="prompt prompt-pymol">
color red, paratope
</a>
<a class="prompt prompt-pymol">
select epitope, (resi 72+73+74+75+81+83+84+89+90+92+94+96+97+98+115+116+117 and chain B)
</a>
<a class="prompt prompt-pymol">
color orange, epitope
</a>

<a class="prompt prompt-question">
Are the residues of the paratope and NMR epitope at the interface?
</a>

**Note:** You can turn on and off a model by clicking on its name in the right panel of the PyMOL window.

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <b><i>See the overlay of the best model onto the reference structure</i></b> <i class="material-icons">expand_more</i>
 </summary>
 <p> Top4 models of the top cluster superimposed onto the reference crystal structure (in yellow)</p>
 <figure style="text-align: center">
   <img width="75%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen-bioexcel2023/results-best-model.png">
 </figure>
 <br>
</details>

<hr>
<hr>

## BONUS: Does the antibody bind to a known interface of interleukin? ARCTIC-3D analysis

Gevokizumab is a highly specific antibody that targets an allosteric site of Interleukin-1β (IL-1β) in PDB file *4G6M*, thus reducing its binding affinity for its substrate, interleukin-1 receptor type I (IL-1RI). Canakinumab, another antibody binding to IL-1β, has a different mode of action, as it competes directly with IL-1RI's binding site (in PDB file *4G6J*). For more details please check [this article](https://www.sciencedirect.com/science/article/abs/pii/S0022283612007863?via%3Dihub).

We will now use our new software, [ARCTIC-3D](https://www.biorxiv.org/content/10.1101/2023.07.10.548477v1), to visualize the binding interfaces formed by IL-1β. First, the program retrieves all the existing binding surfaces formed by IL-1β from the [PDBe website](https://www.ebi.ac.uk/pdbe/). Then, these binding surfaces are compared and clustered together if they span a similar region of the selected protein (IL-1β in our case).

We can now open the ARCTIC-3D web-server page [here](https://wenmr.science.uu.nl/arctic3d/). We will run an ARCTIC-3D job targeting the uniprot ID proper to human Interleukin-1 beta, namely [P01584](https://www.uniprot.org/uniprotkb/P01584/entry).

<a class="prompt prompt-info">
Insert the selected uniprot ID in the **UniprotID** field.
</a>

<a class="prompt prompt-info">
Leave the other parameters as they are and click on **Submit**.
</a>

Wait a few seconds for the job to complete or access a precalculated run [here](https://wenmr.science.uu.nl/arctic3d/example-P01584).

<a class="prompt prompt-question">
How many interface clusters were found for this protein?
</a>

Once you download the output archive, you can find the clustering information presented in the dendrogram:

<figure style="text-align: center;">
<img width="75%" src="dendrogram_average_P01584.png">
</figure>

We can see how the two *4G6M* antibody chains are recognized as a unique cluster, clearly separated from the other binding surfaces and, in particular, from those proper to IL-1RI (uniprot ID P14778).

<a class="prompt prompt-info">
Rerun ARCTIC-3D with a clustering threshold equal to 0.95
</a>

This means that the clustering will be looser, therefore lumping more dissimilar surfaces into the same object.

You can inspect a precalculated run [here](https://wenmr.science.uu.nl/arctic3d/example-P01584-095).

<a class="prompt prompt-question">
How do the results change? Are gevokizumab or canakinumab PDB files being clustered with any IL-1RI-related interface?
</a>

<hr>
<hr>

## BONUS: Alphafold2 for antibody-antigen complex structure prediction

With the advent of Artificial Intelligence (AI) and AlphaFold we can also try to predict with AlphaFold this antibody-antigen complex.

To predict our complex, we are going to use the _AlphaFold2_mmseq2_ Jupyter notebook which can be found with other interesting notebooks in Sergey Ovchinnikov's [ColabFold GitHub repository](https://github.com/sokrypton/ColabFold){:target="_blank"}, making use of the Google Colab CLOUD resources.

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

To use AlphaFold2 to predict e.g. the pentamer follow the following steps:

<a class="prompt prompt-info">
Copy and paste each of the above sequence in the _query_sequence_ field, adding a colon *:* in between the sequences.
</a>

<a class="prompt prompt-info">
Define the _jobname_, e.g. Ab_Ag
</a>

<a class="prompt prompt-info">
In the _Advanced settings_ block you can check the option to save the results to your Google Drive (if you have an account)
</a>

<a class="prompt prompt-info">
In the top section of the Colab, click: _Runtime > Run All_
</a>

(It may give a warning that this is not authored by Google, because it is pulling code from GitHub). This will automatically install, configure and run AlphaFold for you - leave this window open. After the prediction complete you will be asked to download a zip-archive with the results (if you configured it to use Google Drive, a result archive will be automatically saved to your Google Drive).

<br>
_Time to grap a cup of tea or a coffee!
And while waiting try to answer the following questions:_

<a class="prompt prompt-question">
    How do you interpret AlphaFold's predictions? What are the predicted LDDT (pLDDT), PAE, iptm?
</a>

_Tip_: Try to find information about the prediction confidence at [https://alphafold.ebi.ac.uk/faq](https://alphafold.ebi.ac.uk/faq){:target="\_blank"}. A nice summary can also be found [here](https://www.rbvi.ucsf.edu/chimerax/data/pae-apr2022/pae.html){:target="\_blank"}.


Pre-calculated AlphFold2 predictions are provided [here](abagtest_2d03e.result.zip){:target="\_blank"}. This archive contains the five predicted models (the naming indicates the rank), figures (png) files (PAE, pLDDT, coverage) and json files containing the corresponding values (the last part of the json files report the ptm and iptm values).

<br>

### Analysis of the generated AF2 models

While the notebook is running models will appear first under the `Run Prediction` section, colored both by chain and by pLDDT.

The best model will then be displayed under the `Display 3D structure` section. This is an interactive 3D viewer that allows you to rotate the molecule and zoom in or out.

**Note** that you can change the model displayed with the _rank_num_ option. After changing it execute the cell by clicking on the run cell icon on the left of it.

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

</details>
<br>

<a class="prompt prompt-question">
    Based on the iptm scores, would you qualify those models as reliable?
</a>

**Note** that in this case the iptm score reports on all interfaces, i.e. both the interface between the two chains of the antibody, and the antibody-antigen interface

Another useful way of looking at the model accuracy is to check the Predicted Alignment Error plots (PAE) (also referred to as Domain position confidence).
The PAE gives a distance error for every pair of residues: It gives AlphaFold's estimate of position error at residue x when the predicted and true structures are aligned on residue y.
Values range from 0 to 35 Angstroms. It is usually shown as a heatmap image with residue numbers running along vertical and horizontal axes and each pixel colored according to the PAE value for the corresponding pair of residues. If the relative position of two domains is confidently predicted then the PAE values will be low (less than 5A - dark blue) for pairs of residues with one residue in each domain. When analysing your complex, the diagonal block will indicate the PAE within each molecule/domain, while the off-diagonal blocks report on the accuracy of the domain-domain placement.


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
   <img src="/education/HADDOCK3/HADDOCK3-antibody-antigen-bioexcel2023/abagtest_2d03e_pae.png">
  </figure>
</details>
<br>

<a class="prompt prompt-question">
    Based on the PAE plots, which interfaces can be considered reliable/unreliable?
</a>


<br>

### Visualization of the generated AF2 models

Let's now visualize the models in PyMOL. For this save your predictions to disk or download the precalculated AlphaFold2 model from [here](abagtest_2d03e.result.zip){:target="\_blank"}.

Start PyMOL and load via the File menu all five AF2 models.

<a class="prompt prompt-pymol">File menu -> Open -> select abagtest_2d03e_unrelaxed_rank_001_alphafold2_multimer_v3_model_3_seed_000.pdb</a>

Repeat this for each model (`abagtest_2d03e_unrelaxed_rank_X_alphafold2_multimer_v3_model_X_seed_000.pdb` or whatever the naming of your model is).

Let's superimpose all models on the antibody (the antibody in the provided AF2 models correspond to chains A and B):

<a class="prompt prompt-pymol">
util.cbc<br>
select Ab_Ag_unrelaxed_rank_1_model_2 and chain A+B<br>
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

  When looking at the structures generated by AlphaFold in PyMOL, the pLDDT is encoded as the B-factor. <br>
  To color the model according to the pLDDT type in PyMOL:
  <br>
  <a class="prompt prompt-pymol">
    spectrum b
  </a>

  **Note** that the scale in the B-factor field is the inverse of the color coding in the PAE plots: i.e. red mean reliable (high pLDDT) and blue unreliable (low pLDDT))
</details>
<br>

Since we do have NMR chemical shift perturbation data for the antigen, let's check if the perturbed residues are at the interface in the AF2 models.
Note that there is a shift in numbering of 2 residues between the AF2 and the HADDOCK models.

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
    <i>See the AlphaFold models with the NMR-mapped epitope </i>
  <br>
  </summary>
  <figure align="center">
   <img width="90%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen-bioexcel2023/ab-ag-af2.png">
  </figure>
  <br>
</details>
<br>

It should be clear from the visualization of the NMR-mapped epitope on the AF2 models that none does satisfy the NMR data.
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
    <i>See the AlphaFold models superimposed onto the crystal structure of the complex (4G6M)</i>
  <br>
  </summary>
  <figure align="center">
   <img width="90%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen-bioexcel2023/ab-ag-af2-4G6M.png">
  </figure>
  <br>
</details>
<br>

<hr>

## Conclusions

We have demonstrated the usage of HADDOCK3 in an antibody-antigen docking scenario making use of the paratope information on the antibody side (i.e. no prior experimental information) and a NMR-mapped epitope for the antigen. Compared to the static
HADDOCK2.X workflow, the modularity and flexibility of HADDOCK3 allows to customise the docking protocols and to run a deeper analysis of the results.
While HADDOCK3 is still very much work in progress, its intrinsic flexibility can be used to improve the performance of antibody-antigen modelling compared to the results we presented in our
[Structure 2020](https://doi.org/10.1016/j.str.2019.10.011){:target="_blank"} article and in the [related HADDOCK2.4 tutorial](/education/HADDOCK24/HADDOCK24-antibody-antigen){:target="_blank"}.

<hr>
<hr>

## Congratulations! 🎉

You have completed this tutorial. If you have any questions or suggestions, feel free to contact us via email or asking a question through our [support center](https://ask.bioexcel.eu){:target="_blank"}.

And check also our [education](/education) web page where you will find more tutorials!

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
[link-pdbtools]:http://www.bonvinlab.org/pdb-tools/ "PDB-Tools"
[link-pymol]: https://www.pymol.org/ "PyMOL"
[nat-pro]: https://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html "Nature protocol"
[tbl-examples]: https://github.com/haddocking/haddock-tools/tree/master/haddock_tbl_validation "tbl examples"
