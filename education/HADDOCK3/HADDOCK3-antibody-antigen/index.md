---
layout: page
title: "Antibody-antigen modelling tutorial using a local version of HADDOCK3"
excerpt: "A tutorial describing the use of HADDOCK3 to model an antibody-antigen complex"
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

This tutorial demonstrates the use of the new modular HADDOCK3 version for predicting
the structure of an antibody-antigen complex using knowledge of the hypervariable loops
on the antibody and either the entire surface or an epitope identified from NMR chemical
shift perturbation data for the antigen to guide the docking.

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

In this tutorial we will be working with  Interleukin-1β (IL-1β)
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

In order to follow this tutorial you will need to work on a Linux or MacOSX
system. We will also make use of [**PyMOL**][link-pymol] (freely available for
most operating systems) in order to visualize the input and output data. We will
provide you links to download the various required software and data.

Further we are providing pre-processed PDB files for docking and analysis (but the
preprocessing of those files will also be explained in this tutorial). The files have been processed
to facilitate their use in HADDOCK and for allowing comparison with the known reference
structure of the complex. For this _download and unzip the following_
[zip archive](https://surfdrive.surf.nl/files/index.php/s/HvXxgxCTY1DiPsV){:target="_blank"}
_and note the location of the extracted PDB files in your system_. In it you should find the following directories:

* `haddock3`: Contains HADDOCK3 configuration and job files for the various scenarios in this tutorial
* `pdbs`: Contains the pre-processed PDB files
* `plots`: Contains pre-generated html plots for the various scenarios in this tutorial
* `restraints`: Contains the interface information and the correspond restraint files for HADDOCK
* `runs`: Contains pre-calculated (partial) run results for the various scenarios in this tutorial
* `scripts`: Contains a variety of scripts used in this tutorial

### Setup for the EU-ASEAN HPC school on Fugaku

The software and data required for this tutorial have been pre-installed on Fugaku.
In order to run the tutorial, first copy the required data into your home directory on fugagku:

<a class="prompt prompt-cmd">
tar xfz /vol0601/share/ra020021/LifeScience/20221208_Bonvin/HADDOCK3-antibody-antigen.tgz
</a>

This will create the `HADDOCK3-antibody-antigen` directory with all necessary data and script and job examples ready for submission to the batch system.

HADDOCK3 has been pre-installed, both on the login node and on the compute nodes.
To active HADDOCK3 on the login node type:

<a class="prompt prompt-cmd">
source /vol0601/share/ra020021/LifeScience/20221208_Bonvin/miniconda3/etc/profile.d/conda.sh<br>
conda activate haddock3
</a>

You will now have all the require software in place to run the various steps of this tutorial.

In case you would start an interactive session on a node, e.g. with the following command:

<a class="prompt prompt-cmd">
pjsub \-\-interact \-\-sparam wait-time=60 \-L  \"elapse=02:00:00\" \-x \"PJM_LLIO_GFSCACHE=/vol0003:/vol0006\"
</a>

use then the following command to active the HADDOCK3 environment for the arm8 architecture of the compute nodes:

<a class="prompt prompt-cmd">
source /vol0601/share/ra020021/LifeScience/20221208_Bonvin/miniconda3-arm8/etc/profile.d/conda.sh<br>
conda activate haddock3
</a>

This is the command you will also find in the example job script for batch submission.

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
<img width="75%" src="./HADDOCK2-stages.png">
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
<img width="75%" src="./HADDOCK3-workflow-scheme.png">
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


### Installing HADDOCK3

In this tutorial we will make use of the HADDOCK3 version. In case HADDOCK3
is not pre-installed in your system you will have to install it.

To obtain HADDOCK3 navigate to [its repository][haddock-repo], fill the
registration form, and then follow the [installation instructions](https://www.bonvinlab.org/haddock3/INSTALL.html){:target="_blank"}.


### Auxiliary software

**[FreeSASA][link-freesasa]**: FreeSASA will be used to identify surface-accessible residues
(pre-calculated data are provided).
The software can be easily installed into your HADDOCK3 python installation with:

<a class="prompt prompt-cmd">
  pip install freesasa
</a>

**[PDB-tools][link-pdbtools]**: A useful collection of Python scripts for the
manipulation (renumbering, changing chain and segIDs...) of PDB files is freely
available from our GitHub repository. `pdb-tools` is automatically installed
with HADDOCK3. If you have activated the HADDOCK3 Python environment you have
access to the pdb-tools package.

**[PyMol][link-pymol]**: We will make use of PyMol for visualization. If not
already installed on your system, download and install PyMol.


<hr>
<hr>

## Preparing PDB files for docking

In this section we will prepare the PDB files of the antibody and antigen for docking.
Crystal structures of both the antibody and the antigen in their free forms are available from the
[PDBe database](https://www.pdbe.org){:target="_blank"}. In the case of the antibody which consists
of two chains (L+H) we will have to prepare it for use in HADDOCK such as it can be treated as
a single chain with non-overlapping residue numbering. For this we will be making use of `pdb-tools` from the command line.

_**Note**_ that `pdb-tools` is also available as a [web service](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.


_**Note**_: Before starting to work on the tutorial, make sure to activate haddock3, e.g. if installed using `conda`

<a class="prompt prompt-cmd">
conda activate haddock3
</a>


<hr>
### Preparing the antibody structure

Using PDB-tools we will download the structure from the PDB database (the PDB ID is [4G6K](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k){:target="_blank"}) and then process it to have a unique chain ID (A) and non-overlapping residue numbering by shifting the residue numbering of the second chain.

This can be done from the command line with:

<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy -strict | pdb_selchain -H | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_tidy -strict > 4G6K_H.pdb
</a>
<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy -strict | pdb_selchain -L | pdb_delhetatm | pdb_fixinsert | pdb_shiftres -1000 | pdb_keepcoord | pdb_tidy -strict > 4G6K_L.pdb
</a>
<a class="prompt prompt-cmd">
pdb_merge 4G6K_H.pdb 4G6K_L.pdb |pdb_chain -A |pdb_chainxseg | pdb_tidy -strict > 4G6K_clean.pdb
</a>

The first command fetches the PDB ID, select the heavy chain (H) and removes water and heteroatoms (in this case no co-factor is present that should be kept).
An important part for antibodies is the `pdb_fixinsert` command that fixes the residue numbering of the HV loops: Antibodies often follow the [Chothia numbering scheme](https://pubmed.ncbi.nlm.nih.gov/9367782/?otool=inluulib){:target="_blank"} and insertions created by this numbering scheme (e.g. 82A,82B,82C) cannot be processed by HADDOCK directly. As such renumbering is necessary before starting the docking.

The second command does the same for the light chain (L) with an additional step of shifting the residue numbering by 1000 (using `pdb_shiftres`) to avoid overlap in the numbering of the two chains.

The third and last command merges the two processed chains and assign them unique chain- and segIDs, resulting in the HADDOCK-ready `4G6K_clean.pdb` file.

_**Note**_ that the corresponding files can be found in the `pdbs` directory of the archive you downloaded.

<hr>

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
assi (selection1) (selection2) distance, lower-bound correction, upper-bound correction
</pre>

The lower limit for the distance is calculated as: distance minus lower-bound
correction and the upper limit as: distance plus upper-bound correction.  The
syntax for the selections can combine information about chainID - `segid`
keyword -, residue number - `resid` keyword -, atom name - `name` keyword.
Other keywords can be used in various combinations of OR and AND statements.
Please refer for that to the [online CNS manual](https://cns-online.org/v1.3/){:target="_blank"}.

We will shortly explain in this section how to generate both ambiguous
interaction restraints (AIRs) and specific distance restraints for use in
HADDOCK illustrating two scenarios:

* **HV loops on the antibody, full surface on the antigen**
* **HV loops on the antibody, NMR interface mapping on the antigen**

Information about various types of distance restraints in HADDOCK can also be
found in our [online manual][air-help]{:target="_blank"} pages.

<hr>

### Identifying the paratope of the antibody

Nowadays there are several computational tools that can identify the paratope (the residues of the hypervariable loops involved in binding) from the provided antibody sequence. In this tutorial we are providing you the corresponding list of residue obtained using [ProABC-2](https://wenmr.science.uu.nl/proabc2/){:target="_blank"}. ProABC-2 uses a convolutional neural network to identify not only residues which are located in the paratope region but also the nature of interactions they are most likely involved in (hydrophobic or hydrophilic). The work is described in [Ambrosetti, *et al* Bioinformatics, 2020](https://academic.oup.com/bioinformatics/article/36/20/5107/5873593){:target="_blank"}.

The corresponding paratope residues (those with either an overall probability >= 0.4 or a probability for hydrophobic or hydrophilic > 0.3) are:

<pre style="background-color:#DAE4E7">
31,32,33,34,35,52,54,55,56,100,101,102,103,104,105,106,1031,1032,1049,1050,1053,1091,1092,1093,1094,1096
</pre>

The numbering corresponds to the numbering of the `4G6K_clean.pdb` PDB file.

Let us visualize those onto the 3D structure.
For this start PyMOL and load `4G6K_clean.pdb`

<a class="prompt prompt-pymol">
File menu -> Open -> select 4G6K_clean.pdb
</a>

or from the command line:

<a class="prompt prompt-cmd">
pymol 4G6K_clean.pdb
</a>

We will now highlight the predicted paratope. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all
</a>
<a class="prompt prompt-pymol">
select paratope, (resi 31+32+33+34+35+52+54+55+56+100+101+102+103+104+105+106+1031+1032+1049+1050+1053+1091+1092+1093+1094+1096)<br>
</a>
<a class="prompt prompt-pymol">
color red, paratope
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
Do the identified residues form a well defined patch on the surface?
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See surface view of the paratope:</i></b>
  </summary>
  <figure style="text-align: center;">
    <img width="50%" src="./antibody-paratope.png">
  </figure>
  <br>
</details>

<hr>

### Antigen scenario 1: no information

In this scenario, we will target the entire surface of the antigen by selecting the solvent accessible residues.
For this we will use `freesasa` to calculate the solvent accessible surface area (SASA) for the different
residues:

<a class="prompt prompt-cmd">
freesasa 4I1B_clean.pdb \-\-format=rsa >4I1B_clean.rsa
</a>

<pre style="background-color:#DAE4E7">
REM  FreeSASA 2.0.3
REM  Absolute and relative SASAs for 4I1B_clean.pdb
REM  Atomic radii and reference values for relative SASA: ProtOr
REM  Chains: A
REM  Algorithm: Lee & Richards
REM  Probe-radius: 1.40
REM  Slices: 20
REM RES _ NUM      All-atoms   Total-Side   Main-Chain    Non-polar    All polar
REM                ABS   REL    ABS   REL    ABS   REL    ABS   REL    ABS   REL
RES VAL A   3    84.83  55.8  13.08  11.8  71.76 172.9  30.45  26.5  54.38 147.5
RES ARG A   4   200.36  84.1 192.85  98.3   7.51  17.9  71.92  98.3 128.44  77.8
RES SER A   5    48.69  41.1  25.55  34.1  23.14  53.3  22.44  47.8  26.25  36.8
RES LEU A   6    71.91  40.0  70.87  50.7   1.04   2.6  71.91  50.5   0.00   0.0
RES ASN A   7    31.01  21.4  25.87  25.0   5.14  12.4   0.00   0.0  31.01  30.0
...
</pre>

The following command will return all residues with a relative SASA for either
the backbone or the side-chain > 40% (we use 40% to limit the number of surface residues selected as their
number does increase the computational requirements)

<a class="prompt prompt-cmd">
awk \'{if (NF==13 && ($7>40 || $9>40)) printf \"\%d \",$3; if (NF==14 && ($8>40 || $10>40)) print $0}\' 4I1B_clean.rsa
</a>

The resulting list of residues can be found in the `restraints/antigen-surface.act-pass` file. Note in this file the empty first line. The file consists
of two lines, with the first one defining the `active` residues and the second line the `passive` ones, in this case the solvent accessible residues.
We will use later this file to generate the ambiguous distance restraints for HADDOCK.

If you want to generate the same file, first create an empty line and then use the `awk` command, piping the results to an output file, e.g.:

<a class="prompt prompt-cmd">
echo \" \" \> antigen-surface.pass
</a>
<a class="prompt prompt-cmd">
awk \'{if (NF==13 && ($7>40 || $9>40)) printf \"\%d \",$3; if (NF==14 && ($8>40 || $10>40)) printf \"\%d \",$4}\' 4I1B_clean.rsa \>\> antigen-surface.pass<br>
</a>

We can visualize the selected surface residues of Interleukin-1β.
For this start PyMOL and from the PyMOL File menu open the PDB file of the antigen.

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
select surface40, (resi 3+4+5+6+13+14+15+20+21+22+23+24+25+30+32+33+34+35+37+38+48+49+50+51+52+53+54+55+61+63+64+65+66+73+74+75+76+77+80+84+86+87+88+89+90+91+93+94+96+97+105+106+107+108+109+118+119+126+127+128+129+130+135+136+137+138+139+140+141+142+147+148+150+151+152+153)
</a>
<a class="prompt prompt-pymol">
color green, surface40
</a>

<hr>

### Antigen scenario 2: NMR-mapped epitope information


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

We will now visualize the epitope on Interleukin-1β.  For this start PyMOL and from the PyMOL File menu open the provided PDB file of the antigen.

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
    <b><i>See surface view of the epitope identified by NMR</i></b>
  </summary>
  <figure style="text-align: center;">
    <img width="50%" src="./antigen-epitope.png">
  </figure>
  <br>
</details>

<br>

In HADDOCK we are dealing with potentially incomplete binding sites by defining surface neighbors as `passive` residues.
These are added to the definition of the interface but will not lead to any energetic penalty if they are not part of the
binding site in the final models, while the residues defined as `active` (typically the identified or predicted binding
site residues) will. When using the HADDOCK server, `passive` residues will be automatically defined. Here since we are
using a local version, we need to define those manually.

This can easily be done using a script from our [haddock-tools][haddock-tools] repository, which is also provided for convenience
in the `scripts` directly of the archive you downloaded for this tutorial:

<a class="prompt prompt-cmd">
python ./scripts/passive_from_active.py 4I1B_clean.pdb  72,73,74,75,81,83,84,89,90,92,94,96,97,98,115,116,117
</a>

The NMR-identified residues and their surface neighbors generated with the above command can be used to define ambiguous interactions restraints, either using the NMR identified residues as active in HADDOCK, or combining those with the surface neighbors and use this combination as passive only.
The corresponding files can be found in the `restraints/antigen-NMR-epitope.act-pass` and `restraints/antigen-NMR-epitope.pass`files.
Note in the second file the empty first line. The file consists of two lines, with the first one defining the `active` residues and
the second line the `passive` ones. We will use later these files to generate the ambiguous distance restraints for HADDOCK.

In general it is better to be too generous rather than too strict in the
definition of passive residues.

An important aspect is to filter both the active (the residues identified from
your mapping experiment) and passive residues by their solvent accessibility.
Our web service uses a default relative accessibility of 15% as cutoff. This is
not a hard limit. You might consider including even more buried residues if some
important chemical group seems solvent accessible from a visual inspection.

<hr>

### Defining ambiguous restraints for scenario 1


Once you have defined your active and passive residues for both molecules, you
can proceed with the generation of the ambiguous interaction restraints (AIR) file for HADDOCK.
For this you can either make use of our online [GenTBL][gentbl] web service, entering the
list of active and passive residues for each molecule, and saving the resulting
restraint list to a text file, or use the relevant `haddock-tools` script.

To use our `haddock-tools` `active-passive-to-ambig.py` script you need to
create for each molecule a file containing two lines:

* The first line corresponds to the list of active residues (numbers separated by spaces)
* The second line corresponds to the list of passive residues.

For scenario 1 this would be:

* For the antibody (the file called `antibody-paratope.act-pass` from the `restraints` directory):
<pre style="background-color:#DAE4E7">
31 32 33 34 35 52 54 55 56 100 101 102 103 104 105 106 1031 1032 1049 1050 1053 1091 1092 1093 1094 1096
</pre>

* and for the antigen (the file called `antigen-surface.pass` from the `restraints` directory):
<pre style="background-color:#DAE4E7">
3 4 5 6 13 14 15 20 21 22 23 24 25 30 32 33 34 35 37 38 48 49 50 51 52 53 54 55 61 63 64 65 66 73 74 75 76 77 80 84 86 87 88 89 90 91 93 94 96 97 105 106 107 108 109 118 119 126 127 128 129 130 135 136 137 138 139 140 141 142 147 148 150 151 152 153
</pre>

Using those two files, we can generate the CNS-formatted AIR restraint files
with the following command:

<a class="prompt prompt-cmd">
python ./scripts/active-passive-to-ambig.py ./restraints/antibody-paratope.act-pass ./restraints/antigen-surface.pass > ambig-paratope-surface.tbl
</a>

This generates a file called `ambig-paratope-surface.tbl` that contains the AIR
restraints. The default distance range for those is between 0 and 2Å, which
might seem short but makes senses because of the 1/r^6 summation in the AIR
energy function that makes the effective distance be significantly shorter than
the shortest distance entering the sum.

The effective distance is calculated as the SUM over all pairwise atom-atom
distance combinations between an active residue and all the active+passive on
the other molecule: SUM[1/r^6]^(-1/6).

If you modify manually this file, it is possible to quickly check if the format is valid.
To do so, you can find in our [haddock-tools][haddock-tools] repository a folder named
`haddock_tbl_validation` that contains a script called `validate_tbl.py` (also provided here in the `scripts` directory).
To use it, type:

<a class="prompt prompt-cmd">
python ./scripts/validate_tbl.py \-\-silent ambig-paratope-surface.tbl
</a>

No output means that your TBL file is valid.

<hr>

### Defining ambiguous restraints for scenario 2a

In this scenario the NMR epitope combined with the surface neighbors are used as passive residues in HADDOCK.

The creation of the AIR tbl file for scenario 2a is similar to scenario 1, but instead using the `antigen-NMR-epitope.pass` file for the antigen:

<a class="prompt prompt-cmd">
./scripts/active-passive-to-ambig.py ./restraints/antibody-paratope.act-pass ./restraints/antigen-NMR-epitope.pass > ambig-paratope-NMR-epitope-pass.tbl
</a>

<hr>

### Defining ambiguous restraints for scenario 2b

In this scenario the NMR epitope is defined as active (meaning ambiguous distance restraints will be defined from the NMR epitope residues) and the surface neighbors are used as passive residues in HADDOCK.

The creation of the AIR tbl file for scenario 2b is similar to scenario 1, but instead using the `antigen-NMR-epitope.act-pass` file for the antigen:

<a class="prompt prompt-cmd">
./scripts/active-passive-to-ambig.py ./restraints/antibody-paratope.act-pass ./restraints/antigen-NMR-epitope.act-pass > ambig-paratope-NMR-epitope.tbl
</a>

<hr>

### Additional restraints for multi-chain proteins

As an antibody consists of two separate chains, it is important to define a few distance restraints
to keep them together during the high temperature flexible refinement stage of HADDOCK. This can easily be
done using a script from [haddock-tools][haddock-tools] repository, which is also provided for convenience
in the `scripts` directly of the archive you downloaded for this tutorial.

<a class="prompt prompt-cmd">
python ./scripts/restrain_bodies.py  4G6K_clean.pdb >antibody-unambig.tbl
</a>

The result file contains two CA-CA distance restraints with the exact distance measured between the picked CA atoms:

<pre style="background-color:#DAE4E7">
  assign (segid A and resi 220 and name CA) (segid A and resi 1018 and name CA) 47.578 0.0 0.0
  assign (segid A and resi 193 and name CA) (segid A and resi 1014 and name CA) 33.405 0.0 0.0
</pre>

This file is also provided in the `restraints` directory of the archive you downloaded.

<hr>
<hr>

## Setting up the docking with HADDOCK3

Now that we have all required files at hand (PBD and restraints files) it is time to setup our docking protocol.
For this we need to create a HADDOCK3 configuration file that will define the docking workflow. In contrast to HADDOCK2.X,
we have much more flexibility in doing this. We will illustrate this flexibility by introducing a clustering step
after the initial rigid-body docking stage, select up to 10 models per cluster and refine all of those.

HADDOCK3 also provides an analysis module (`caprieval`) that allows
to compare models to either the best scoring model (if no reference is given) or a reference structure, which in our case
we have at hand. This will directly allow us to assess the performance of the protocol for the following three scenarios:

1. Scenario 1: Docking using the paratope information only and the surface of the antigen
2. Scenario 2a: Docking using the paratope and the NMR-identified epitope as passive
3. Scenario 2b: Docking using the paratope and the NMR-identified epitope as active

The basic workflow for all three scenarios will consists of the following modules, with some differences in the restraints used and some parameter settings (see below):

1. **`topoaa`**: *Generates the topologies for the CNS engine and build missing atoms*
2. **`rigidbody`**: *Rigid body energy minimisation (`it0` in haddock2.x)*
3. **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
4. **`seletopclusts`**: *Selection of the top10 models of all clusters*
5. **`flexref`**: *Semi-flexible refinement of the interface (`it1` in haddock2.4)*
6. **`emref`**: *Final refinement by energy minimisation (`itw` EM only in haddock2.4)*
7. **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
8. **`caprieval`**: *Calculates CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ) with respect to the top scoring model or reference structure if provided*

The input PDB files are the same for all three scenarios. The differences are in the ambiguous interaction restraint files used and the sampling at the rigid body stage in the case of scenario1.

**_Note_ that for the** [EU ASEAN HPC school](https://www.hpcschool.net){:target="_blank"} **, we will only run scenario2a with a reduced sampling for the rigid body module of 240 models to limit to the computing time and get results within a reasonable time. The Fugaku example scripts for this are provided in the `haddock3` directory (`scenario2a-NMR-epitope-pass-node.cfg` and `scenario2a-NMR-epitope-pass-node-fugaku.job`). Copy those into the main tutorial directory before submitting the job file to the batch system with the `pjsub` command.**

<hr>

### HADDOCK3 execution modes

HADDOCK3 currently supports three difference execution modes that are defined in the first section of the configuration file of a run.

#### 1. local mode

In this mode HADDOCK3 will run on the current system, using the defined number of cores (`ncores`) in the config file
to a maximum of the total number of available cores on the system minus one. An example of the relevant parameters to be defined in the first section of the config file is:

{% highlight toml %}
# compute mode
mode = "local"
#  1 nodes x 96 ncores
ncores = 96
{% endhighlight %}

In this mode HADDOCK3 can be started from the command line with as argument the configuration file of the defined workflow.

<a class="prompt prompt-cmd">
haddock3 \<my-workflow-configuration-file\>
</a>

Alternatively redirect the output to a log file and send haddock3 to the background

<a class="prompt prompt-cmd">
haddock3 \<my-workflow-configuration-file\> \> haddock3.log &
</a>

_**Note**_: This is also the execution mode that should be used for example when submitting the HADDOCK3 job to a node of a cluster, requesting X number of cores.

<details>
  <summary style="bold">
    <i>View an example script for submitting via the slurm batch system:</i>
  </summary>

  {% highlight shell %}
  #!/bin/bash
  #SBATCH --nodes=1
  #SBATCH --tasks-per-node=96
  #SBATCH -J haddock3
  #SBATCH --partition=medium

  # load haddock3 module
  module load haddock3
  # or activate the haddock3 conda environment
  ##source $HOME/miniconda3/etc/profile.d/conda.sh
  ##conda activate haddock3

  # go to the run directory
  cd $HOME/HADDOCK3-antibody-antigen

  # execute
  haddock3 scenario1-surface-node.cfg
  {% endhighlight %}
  <br>
</details>

<details>
  <summary style="bold">
    <i>EU-ASEAN HPC school example script for submitting to the Fugaku batch system:</i>
  </summary>
  {% highlight shell %}
  #!/bin/bash
  #PJM -L  "node=1"                            # Assign 1 node
  #PJM -L  "elapse=02:00:00"                   # Elapsed time limit 2 hour
  #PJM -x PJM_LLIO_GFSCACHE=/vol0003:/vol0006  # volume names that job uses
  #PJM -s                                      # Statistical information output

  # active the haddock3 conda environment
  source /vol0601/share/ra020021/LifeScience/20221208_Bonvin/miniconda3-arm8/etc/profile.d/conda.sh
  conda activate haddock3

  # go to the tutorial directory in your home directory
  # edit if needed to specify the correct location
  cd $HOME/HADDOCK3-antibody-antigen

  # execute haddock3
  haddock3 scenario2a-NMR-epitope-pass-node.cfg
  {% endhighlight %}
  <br>
</details>

<br>

#### 2. HPC/batch mode

In this mode HADDOCK3 will typically be started on your local server (e.g. the login node) and will dispatch jobs to the batch system of your cluster.
Two batch systems are currently supported: `slurm` and `torque` (defined by the `batch_type` parameter). In the configuration file you will
have to define the `queue` name and the maximum number of concurrent jobs sent to the queue (`queue_limit`). Since HADDOCK3 single model
calculations are quite fast, it is recommended to calculate multiple models within one job submitted to the batch system.
The number of model per job is defined by the `concat` parameter in the configuration file.
You want to avoid sending thousands of very short jobs to the batch system if you want to remain friend with your system administrators...

An example of the relevant parameters to be defined in the first section of the config file is:

{% highlight toml %}
# compute mode
mode = "hpc"
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

#### 3. MPI mode

HADDOCK3 supports a parallel MPI implementation (functional but still very experimental at this stage). For this to work, the `mpi4py` library
must have been installed at installation time. Refer to the [MPI-related instructions](https://www.bonvinlab.org/haddock3/tutorials/mpi.html).
The execution mode should be set to `mpi` and the total number of cores should match the requested resources when submitting to the batch system.

An example of the relevant parameters to be defined in the first section of the config file is:

{% highlight toml %}
# compute mode
mode = "mpi"
#  5 nodes x 50 tasks = ncores = 250
ncores = 250
{% endhighlight %}

In this execution mode the HADDOCK3 job should be submitted to the batch system requesting the corresponding number of nodes and cores per node.

<details>
  <summary style="bold">
    <i>View an example script for submitting an MPI HADDOCK3 job the slurm batch system:</i>
  </summary>
  {% highlight shell %}
  #!/bin/bash
  #SBATCH --nodes=5
  #SBATCH --tasks-per-node=50
  #SBATCH -J haddock3mpi

  # load haddock3 module
  module load haddock3
  # or make sure haddock3 is activated
  ##source $HOME/miniconda3/etc/profile.d/conda.sh
  ##conda activate haddock3

  # go to the run directory
  # edit if needed to specify the correct location
  cd $HOME/HADDOCK3-antibody-antigen

  # execute
  haddock3 scenario2a-NMR-epitope-pass-mpi.cfg
  {% endhighlight %}
  <br>
</details>

<hr>

### Scenario 1: Paratope - antigen surface

Now that we have all data ready, and know about execution modes of HADDOCK3 it is time to setup the docking for the first scenario in which we will use the paratope on the antibody to guide the docking, targeting the entire surface of the antibody. The restraint file to use for this is `ambig-paratope-surface.tbl`. We will also define the restraints to keep the two antibody chains together using for this the `antibody-unambig.tbl` restraint file. Further, as we have no information on the antigen side, it is important to increase the sampling in the rigid body sampling stage to 10000. And we will also turn off the default random removal of restraints to keep all the information on the paratope (`randremoval = false`). The configuration file for this scenario (assuming a local running mode, eventually submitted to the batch system requesting a full node) is:

{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the entire surface of the antigen
# ====================================================================

# directory name of the run
run_dir = "scenario1-surface"

# compute mode
mode = "local"
#  1 nodes x 96 threads
ncores = 96

# Self contained rundir (to avoid problems with long filename paths)
self_contained = true

# Cleaning to compress files and save space
clean = true

# molecules to be docked
molecules =  [
    "pdbs/4G6K_clean.pdb",
    "pdbs/4I1B_clean.pdb"
    ]

# ====================================================================
# Parameters for the various stages
# ====================================================================
[topoaa]

[rigidbody]
# CDR to surface ambig restraints
ambig_fname = "restraints/ambig-paratope-surface.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
# Turn off random removal of restraints
randremoval = false
# Number of models to generate
sampling = 10000

[clustfcc]
threshold = 10

[seletopclusts]
## select all the clusters
top_cluster = 500
## select the best 10 models of each cluster
top_models = 10

[caprieval]
# this is only for this tutorial to check the performance at the rigidbody stage
reference_fname = "pdbs/4G6M_matched.pdb"

[flexref]
# Acceptable percentage of model failures
tolerance = 5
# CDR to surface ambig restraints
ambig_fname = "restraints/ambig-paratope-surface.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
# Turn off random removal of restraints
randremoval = false

[emref]
# CDR to surface ambig restraints
ambig_fname = "restraints/ambig-paratope-surface.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
# Turn off random removal of restraints
randremoval = false

[clustfcc]

[seletopclusts]
top_cluster = 500

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

# ====================================================================
{% endhighlight %}

This configuration file is provided in the `haddock3` directory of the downloaded data set for this tutorial as `scenario1-surface-node.cfg`.
An MPI version (this is still very much experimental and might not work on all systems) is also available as `scenario1-surface-mpi.cfg`.

<a class="prompt prompt-question">
Compared to the workflow described above (Setting up the docking with HADDOCK3), this example has one additional step. Can you identify which one?
</a>

If you have everything ready, you can launch haddock3 either from the command line, or, better,
submitting it to the batch system requesting in this local run mode a full node (see local execution mode above).

_**Note**_ that this scenario is computationally more expensive because of the increased sampling.
On our own cluster, running in MPI mode with 250 cores on AMD EPYC 7451 processors the run completed in 1h23min.
The same run on a single node using all 96 threads took on the same architecture 4 hours and 8 minutes.

On the Fugaku supercomputer used for the EU ASEAN HPC school, running on a single node 48 [armv8 A64FX](https://github.com/fujitsu/A64FX){:target="_blank" processors}, this run completed in about 23 hours.

<hr>

### Scenario 2a: Paratope - NMR-epitope as passive

In scenario 2a we are setting up the docking in which the paratope on the antibody is used to guide the docking, targeting the NMR-identified epitope (+surface neighbors) defined as passive residues. The restraint file to use for this is `ambig-paratope-NMR-epitope-pass.tbl`. As for scenario1, we will also define the restraints to keep the two antibody chains together using for this the `antibody-unambig.tbl` restraint file. In this case since we have information for both interfaces default sampling parameters are sufficient. And we will also turn off the default random removal of restraints to keep all the information on the paratope (`randremoval = false`). The configuration file for this scenario (assuming a local running mode, eventually submitted to the batch system requesting a full node) is:

{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen (as passive)
# ====================================================================

# directory name of the run
run_dir = "scenario2a-NMR-epitope-pass"

# MPI compute mode
mode = "local"
#  1 nodes x 96 threads
ncores = 96

# Self contained rundir (to avoid problems with long filename paths)
self_contained = true

# Cleaning to compress files and save space
clean = true

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
# CDR to surface ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope-pass.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
# Turn off random removal of restraints
randremoval = false

[clustfcc]
threshold = 10

[seletopclusts]
## select all the clusters
top_cluster = 500
## select the best 10 models of each cluster
top_models = 10

[caprieval]
# this is only for this tutorial to check the performance at the rigidbody stage
reference_fname = "pdbs/4G6M_matched.pdb"

[flexref]
# Acceptable percentage of model failures
tolerance = 5
# CDR to surface ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope-pass.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
# Turn off random removal of restraints
randremoval = false

[emref]
# CDR to surface ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope-pass.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
# Turn off random removal of restraints
randremoval = false

[clustfcc]

[seletopclusts]
top_cluster = 500

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

# ====================================================================
{% endhighlight %}

This configuration is provided in the `haddock3` directory of the downloaded data set for this tutorial as `scenario2a-NMR-epitope-pass-node.cfg`. An MPI version  (this is still very much experimental and might not work on all systems) is also available as `scenario2a-NMR-epitope-pass-mpi.cfg`.

If you have everything ready, you can launch haddock3 either from the command line, or, better, submitting it to the batch system requesting in this local run mode a full node (see local execution mode above).

_**Note**_ that this scenario is less expensive since we keep the default sampling parameters. On our own cluster, running in MPI mode with 250 cores on AMD EPYC 7451 processors the run completed in about 7 minutes. The same run on a single node using all 96 threads took on the same architecture about 21 minutes. In HPC/batch mode, using 100 queue slots and 10 models per job, the same run completed in about 45 minutes.

On the Fugaku supercomputer used for the EU ASEAN HPC school, running on a single node (48 [armv8 A64FX](https://github.com/fujitsu/A64FX){:target="_blank"} processors), this run completed in about 1 hour and 15 minutes. Limiting the sampling to 240 rigid body models (recommended for the EU ASEAN HPC school) shorten the execution time to 37 minutes.

<hr>

### Scenario 2b: Paratope - NMR-epitope as active

Scenario 2b is rather similar to scenario 2a with the difference that the NMR-identified epitope is treated as active, meaning restraints will be defined from it to "force" it to be at the interface.
And since there might be more false positive data in the identified interfaces, we will leave the random removal of restraints on. The restraint file to use for this is `ambig-paratope-NMR-epitope-act.tbl`. As for scenario1, we will also define the restraints to keep the two antibody chains together using for this the `antibody-unambig.tbl` restraint file. In this case since we have information for both interfaces default sampling parameters are sufficient. The configuration file for this scenario (assuming a local running mode, eventually submitted to the batch system requesting a full node) is:

{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen (as active)
# and keeping the random removal of restraints
# ====================================================================

# directory name of the run
run_dir = "scenario2b-NMR-epitope-act"

# compute mode
mode = "local"
#  1 nodes x 96 cores
ncores = 96

# Self contained rundir (to avoid problems with long filename paths)
self_contained = true

# Cleaning to compress files and save space
clean = true

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
# CDR to surface ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope-act.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[clustfcc]
threshold = 10

[seletopclusts]
## select all the clusters
top_cluster = 500
## select the best 10 models of each cluster
top_models = 10

[caprieval]
# this is only for this tutorial to check the performance at the rigidbody stage
reference_fname = "pdbs/4G6M_matched.pdb"

[flexref]
# Acceptable percentage of model failures
tolerance = 5
# CDR to surface ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope-act.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[emref]
# CDR to surface ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope-act.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[clustfcc]

[seletopclusts]
top_cluster = 500

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

# ====================================================================

{% endhighlight %}

This configuration file is provided in the `haddock3` directory of the downloaded data set for this tutorial as `scenario2b-NMR-epitope-act-node.cfg`. An MPI version is also available as `scenario2b-NMR-epitope-act-mpi.cfg`.

If you have everything ready, you can launch haddock3 either from the command line, or, better, submitting it to the batch system requesting in this local run mode a full node (see local execution mode above).

_**Note**_ The running time for this scenario is similar to that of scenario 2a (see above).

<hr>
<hr>

## Analysis of docking results

### Structure of the run directory

Once your run has completed inspect the content of the resulting directory. You will find the various steps (modules) of the defined workflow numbered sequentially, e.g.:

{% highlight shell %}
> ls scenario2a-NMR-epitope-pass/
    0_topoaa/
    1_rigidbody/
    2_clustfcc/
    3_seletopclusts/
    4_caprieval/
    5_flexref/
    6_emref/
    7_clustfcc/
    8_seletopclusts/
    9_caprieval/
    data/
    log
{% endhighlight %}

There is one additional `data` directory containing the input data (PDB and restraint files) for the various modules and the `log` file of the run.
You can find information about the duration of the run at the bottom of that file. Each sampling/refinement/selection module will contain PBD files.

For example, the `X_seletopclusts` directory contains the selected models from each cluster. The clusters in that directory are numbered based
on their rank, i.e. `cluster_1` refers to the top-ranked cluster. Information about the origin of these files can be found in that directory in the `seletopclusts.txt` file.

The simplest way to extract ranking information and the corresponding HADDOCK scores is to look at the `X_caprieval` directories (which is why it is a good idea to have it as the final module, and possibly as intermediate steps). This directory will always contain a `capri_ss.tsv` file, which contains the model names, rankings and statistics (score, iRMSD, Fnat, lRMSD, ilRMSD and dockq score). E.g.:

<pre style="background-color:#DAE4E7">
model   md5     caprieval_rank  score   irmsd   fnat    lrmsd   ilrmsd  dockq   cluster-id      cluster-ranking model-cluster-ranking
../6_emref/emref_19.pdb -       1       -147.606        1.252   0.793   2.355   1.680   0.770   6       1       1
../6_emref/emref_18.pdb -       2       -135.651        1.048   0.879   2.246   1.408   0.829   6       1       2
../6_emref/emref_15.pdb -       3       -134.860        1.100   0.776   1.937   1.236   0.792   6       1       3
../6_emref/emref_11.pdb -       4       -133.143        1.367   0.741   3.787   1.952   0.707   6       1       4
....
</pre>

If clustering was performed prior to calling the `caprieval` module the `capri_ss.tsv` will also contain information about to which cluster the model belongs to and its ranking within the cluster as shown above.

The relevant statistics are:

* **score**: *the HADDOCK score (arbitrary units)*
* **irmsd**: *the interface RMSD, calculated over the interfaces the molecules*
* **fnat**: *the fraction of native contacts*
* **lrmsd**: *the ligand RMSD, calculated on the ligand after fitting on the receptor (1st component)*
* **ilrmsd**: *the interface-ligand RMSD, calculated over the interface of the ligand after fitting on the interface of the receptor (more relevant for small ligands for example)*
* **dockq**: *the DockQ score, which is a combination of irmsd, lrmsd and fnat and provides a continuous scale between 1 (equal to reference) and 0*

The iRMSD, lRMSD and Fnat metrics are the ones used in the blind protein-protein prediction experiment [CAPRI](https://capri.ebi.ac.uk/) (Critical PRediction of Interactions).

In CAPRI the quality of a model is defined as (for protein-protein complexes):

* **acceptable model**: i-RMSD < 4Å or l-RMSD<10Å and Fnat > 0.1
* **medium quality model**: i-RMSD < 2Å or l-RMSD<5Å and Fnat > 0.3
* **high quality model**: i-RMSD < 1Å or l-RMSD<1Å and Fnat > 0.5

<a class="prompt prompt-question">
What is based on this CAPRI criterion the quality of the best model listed above (emref_19.pdb)?
</a>

In case the `caprieval` module is called after a clustering step an additional file will be present in the directory: `capri_clt.tsv`.
This file contains the cluster ranking and score statistics, averaged over the minimum number of models defined for clustering
(4 by default), with their corresponding standard deviations. E.g.:

<pre style="background-color:#DAE4E7">
cluster_rank    cluster_id      n       under_eval      score   score_std       irmsd   irmsd_std       fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std             caprieval_rank
1       6       10      -       -137.815        5.725   1.192   0.126   0.797   0.051   2.581   0.713   0.774   0.044   1
2       2       16      -       -109.687        4.310   14.951  0.044   0.069   0.000   22.895  0.030   0.067   0.000   2
3       8       4       -       -105.095        13.247  14.909  0.119   0.069   0.000   23.066  0.336   0.066   0.001   3
4       5       10      -       -100.189        4.222   5.148   0.024   0.130   0.015   10.476  0.586   0.202   0.014   4
...
</pre>

In this file you find the cluster rank, the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (n) in the cluster and the corresponding statistics (averages + standard deviations). The corresponding cluster PDB files will be found in the processing `X_seletopclusts` directory.

<hr>

### Analysis scenario 1: Paratope - antigen surface

Let us now analyze the docking results for this scenario. Use for that either your own run or a pre-calculated run provided in the `runs` directory (note that to save space only partial data have been kept in this pre-calculated runs, but all relevant information for this tutorial is available).

First of all let us check the final cluster statistics.

<a class="prompt prompt-info">Inspect the _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the pre-calculated 9_caprieval/capri_clt.tsv file:</i>
  </summary>
    <pre>
      cluster_rank	cluster_id	n	under_eval	score	score_std	irmsd	irmsd_std	fnat	fnat_std	lrmsd	lrmsd_std	dockq	dockq_std	caprieval_rank
      1	19	16	-	-140.175	9.738	1.466	0.177	0.797	0.048	2.535	0.562	0.743	0.046	1
      2	60	10	-	-122.575	3.526	9.009	0.146	0.021	0.007	18.958	0.615	0.072	0.003	2
      3	92	10	-	-119.626	1.463	13.086	0.115	0.000	0.000	21.740	0.128	0.049	0.001	3
      4	59	10	-	-118.236	0.413	5.376	0.080	0.077	0.008	13.677	0.254	0.143	0.005	4
      5	72	10	-	-113.917	1.937	12.261	0.092	0.000	0.000	20.726	0.154	0.053	0.001	5
      6	90	10	-	-113.181	1.395	10.618	0.136	0.000	0.000	20.154	0.494	0.057	0.002	6
      7	7	20	-	-111.937	3.665	12.260	0.028	0.000	0.000	20.665	0.349	0.053	0.001	7
      8	85	10	-	-110.695	8.444	14.879	0.073	0.065	0.007	23.062	0.130	0.065	0.003	8
      9	11	19	-	-109.705	5.332	11.054	0.029	0.000	0.000	19.394	0.067	0.059	0.001	9
      10	17	16	-	-108.098	3.981	13.670	0.009	0.013	0.007	24.332	0.170	0.044	0.003	10
      11	98	10	-	-106.659	2.970	12.158	0.055	0.000	0.000	20.612	0.198	0.053	0.001	11
      12	86	10	-	-106.316	2.878	14.273	0.192	0.013	0.007	24.535	0.105	0.044	0.002	12
      13	4	23	-	-105.156	2.533	13.963	0.199	0.000	0.000	22.478	0.129	0.045	0.001	13
      14	14	18	-	-105.128	7.401	13.479	0.063	0.000	0.000	20.564	0.114	0.053	0.000	14
      15	22	14	-	-104.649	8.107	13.085	0.040	0.000	0.000	21.382	0.197	0.050	0.001	15
      16	20	16	-	-102.610	4.765	15.685	0.116	0.000	0.000	24.036	0.111	0.040	0.000	16
      17	9	20	-	-101.800	8.272	11.436	0.199	0.107	0.008	21.328	0.195	0.087	0.002	17
      18	2	27	-	-100.607	1.540	14.735	0.097	0.000	0.000	22.948	0.109	0.043	0.001	18
      19	89	10	-	-100.587	2.000	12.719	0.049	0.000	0.000	20.333	0.085	0.054	0.000	19
      20	29	12	-	-99.050	3.078	13.695	0.152	0.017	0.000	23.648	0.062	0.048	0.000	20
      21	73	10	-	-97.672	5.060	14.054	0.055	0.000	0.000	21.648	0.082	0.048	0.000	21
      22	96	10	-	-97.667	6.281	14.300	0.063	0.000	0.000	23.246	0.012	0.043	0.000	22
      23	100	10	-	-95.925	1.389	13.889	0.119	0.000	0.000	22.660	0.201	0.045	0.001	23
      24	65	10	-	-95.760	3.302	14.337	0.059	0.056	0.014	22.013	0.039	0.066	0.005	24
      25	71	10	-	-95.267	6.264	11.962	0.133	0.099	0.007	21.587	0.376	0.083	0.004	25
      26	31	12	-	-94.951	3.221	10.734	0.058	0.069	0.021	19.494	0.178	0.082	0.007	26
      27	121	4	-	-94.188	8.529	3.106	0.078	0.388	0.009	5.858	0.363	0.419	0.013	27
      28	75	10	-	-93.970	4.822	5.280	0.109	0.142	0.007	10.643	0.363	0.202	0.005	28
      29	18	16	-	-93.331	3.086	12.409	0.141	0.000	0.000	20.079	0.382	0.055	0.002	29
      30	119	4	-	-92.330	10.292	9.446	0.043	0.017	0.000	14.287	0.257	0.101	0.002	30
      31	101	10	-	-92.261	5.345	9.800	0.077	0.000	0.000	15.515	0.160	0.085	0.001	31
      32	10	20	-	-90.694	3.864	10.219	0.103	0.000	0.000	16.036	0.345	0.080	0.002	32
      33	6	21	-	-90.148	4.092	13.212	0.053	0.017	0.000	20.609	0.060	0.058	0.000	33
      34	16	16	-	-89.323	9.887	9.428	0.056	0.009	0.009	14.054	0.217	0.100	0.002	34
      35	5	22	-	-89.263	2.347	14.311	0.060	0.009	0.009	23.183	0.022	0.046	0.003	35
      36	123	4	-	-88.747	8.292	15.746	0.121	0.000	0.000	24.015	0.166	0.040	0.000	36
      37	78	10	-	-88.528	9.521	12.364	0.077	0.000	0.000	18.814	0.182	0.061	0.001	37
      38	83	10	-	-88.197	9.904	13.447	0.235	0.026	0.009	23.009	0.369	0.053	0.003	38
      39	81	10	-	-87.569	8.685	12.703	0.020	0.000	0.000	18.492	0.031	0.063	0.000	39
      40	118	5	-	-87.252	9.487	13.121	0.035	0.000	0.000	21.167	0.297	0.051	0.001	40
      41	24	13	-	-86.540	5.970	12.645	0.770	0.000	0.000	19.893	0.726	0.056	0.003	41
      42	84	10	-	-85.979	2.744	14.188	0.117	0.000	0.000	21.476	0.344	0.049	0.001	42
      43	25	13	-	-84.501	2.962	14.382	0.042	0.000	0.000	22.722	0.032	0.044	0.001	43
      44	1	28	-	-84.340	1.370	9.001	0.914	0.035	0.027	16.367	2.880	0.095	0.031	44
      45	63	10	-	-83.736	4.316	14.591	0.081	0.000	0.000	22.469	0.069	0.045	0.000	45
      46	97	10	-	-83.686	6.602	14.149	0.139	0.000	0.000	23.074	0.142	0.044	0.000	46
      47	30	12	-	-83.529	3.990	11.787	0.053	0.000	0.000	20.554	0.054	0.054	0.000	47
      48	54	10	-	-83.403	3.788	12.974	0.064	0.056	0.007	20.854	0.115	0.071	0.003	48
      49	46	10	-	-83.310	6.606	14.430	0.284	0.017	0.000	22.882	0.282	0.050	0.001	49
      50	69	10	-	-82.880	6.995	11.784	0.417	0.000	0.000	20.187	1.031	0.056	0.005	50
      51	57	10	-	-82.760	6.197	11.157	0.133	0.034	0.000	18.869	0.335	0.073	0.002	51
      52	94	10	-	-82.423	6.914	14.130	0.062	0.000	0.000	23.093	0.164	0.043	0.001	52
      53	103	9	-	-82.022	4.969	15.203	0.054	0.000	0.000	23.535	0.043	0.042	0.000	53
      54	26	12	-	-81.742	1.991	13.384	0.210	0.034	0.012	22.859	0.310	0.056	0.004	54
      55	91	10	-	-81.267	6.629	15.566	0.053	0.000	0.000	24.457	0.130	0.039	0.000	55
      56	108	8	-	-80.439	11.603	14.473	0.068	0.030	0.007	22.816	0.125	0.054	0.002	56
      57	28	12	-	-78.247	6.927	10.478	0.098	0.017	0.000	18.264	0.340	0.072	0.002	57
      58	62	10	-	-78.246	8.408	13.032	0.020	0.000	0.000	21.309	0.145	0.050	0.000	58
      59	45	10	-	-78.206	2.484	9.505	0.130	0.004	0.007	15.186	0.247	0.089	0.003	59
      60	115	6	-	-77.856	2.216	16.460	0.133	0.000	0.000	26.020	0.470	0.035	0.001	60
      61	8	20	-	-77.752	2.826	14.214	0.046	0.021	0.007	21.569	0.064	0.056	0.003	61
      62	99	10	-	-77.750	5.035	7.694	0.215	0.199	0.008	15.181	0.319	0.158	0.002	62
      63	48	10	-	-77.607	4.468	11.108	0.016	0.000	0.000	19.215	0.140	0.060	0.001	63
      64	3	24	-	-77.365	2.597	10.515	0.044	0.000	0.000	16.626	0.271	0.076	0.002	64
      65	107	8	-	-76.752	3.445	14.437	0.052	0.043	0.009	24.505	0.095	0.054	0.003	65
      66	113	7	-	-75.718	1.472	12.647	0.177	0.060	0.009	22.175	0.221	0.067	0.004	66
      67	105	8	-	-75.593	2.622	14.201	0.135	0.000	0.000	22.814	0.272	0.044	0.001	67
      68	21	14	-	-74.437	5.957	16.514	0.018	0.000	0.000	25.976	0.182	0.035	0.001	68
      69	109	8	-	-73.513	6.194	12.527	0.081	0.009	0.009	20.987	0.068	0.054	0.003	69
      70	74	10	-	-73.003	3.465	13.165	0.056	0.000	0.000	21.360	0.143	0.050	0.000	70
      71	77	10	-	-71.648	0.561	11.918	0.040	0.017	0.000	21.634	0.101	0.056	0.000	71
      72	49	10	-	-71.560	6.030	5.008	0.184	0.116	0.008	9.167	0.487	0.221	0.009	72
      73	104	8	-	-70.911	3.763	13.889	0.034	0.038	0.008	23.657	0.008	0.054	0.003	73
      74	51	10	-	-70.780	9.246	7.842	0.150	0.000	0.000	13.598	0.444	0.106	0.005	74
      75	35	10	-	-70.430	5.164	13.602	0.091	0.000	0.000	20.613	0.219	0.052	0.001	75
      76	110	8	-	-69.449	1.311	13.525	0.037	0.000	0.000	19.242	0.068	0.058	0.000	76
      77	70	10	-	-69.388	0.920	8.359	0.127	0.142	0.022	15.357	0.326	0.136	0.009	77
      78	52	10	-	-69.055	0.977	14.489	0.073	0.004	0.007	22.368	0.133	0.047	0.002	78
      79	106	8	-	-68.877	5.518	4.163	0.205	0.181	0.035	6.794	0.699	0.303	0.023	79
      80	38	10	-	-68.753	7.732	13.343	0.176	0.039	0.015	20.894	0.209	0.065	0.005	80
      81	66	10	-	-68.504	5.913	12.877	0.117	0.000	0.000	21.724	0.222	0.049	0.001	81
      82	15	17	-	-67.855	2.892	9.655	0.050	0.000	0.000	15.217	0.397	0.087	0.003	82
      83	33	10	-	-65.493	3.248	12.339	0.072	0.000	0.000	17.830	0.140	0.067	0.001	83
      84	102	10	-	-64.829	2.213	15.441	0.142	0.000	0.000	24.099	0.156	0.040	0.000	84
      85	122	4	-	-64.279	12.986	14.400	0.042	0.000	0.000	22.780	0.098	0.044	0.001	85
      86	82	10	-	-63.998	1.773	14.535	0.074	0.000	0.000	21.529	0.089	0.049	0.001	86
      87	111	7	-	-63.794	4.372	14.484	0.158	0.022	0.019	22.200	0.055	0.053	0.006	87
      88	56	10	-	-63.762	5.564	12.294	0.066	0.026	0.009	20.656	0.107	0.062	0.003	88
      89	80	10	-	-63.705	3.580	13.595	0.085	0.000	0.000	20.534	0.291	0.053	0.001	89
      90	114	6	-	-63.682	7.451	14.480	0.041	0.000	0.000	22.810	0.229	0.044	0.001	90
      91	61	10	-	-61.901	11.071	14.219	0.079	0.069	0.012	22.790	0.118	0.067	0.004	91
      92	12	19	-	-60.382	5.857	12.874	0.131	0.017	0.000	22.338	0.496	0.053	0.002	92
      93	34	10	-	-60.036	2.926	14.457	0.121	0.000	0.000	22.658	0.144	0.044	0.001	93
      94	23	13	-	-58.403	7.442	13.243	0.509	0.038	0.008	23.414	0.125	0.056	0.002	94
      95	37	10	-	-58.175	2.996	13.611	0.134	0.000	0.000	21.855	0.055	0.048	0.000	95
      96	47	10	-	-57.985	4.230	13.635	0.062	0.000	0.000	23.044	0.295	0.044	0.001	96
      97	112	7	-	-57.472	3.095	11.023	0.184	0.000	0.000	17.724	0.207	0.069	0.001	97
      98	67	10	-	-56.292	5.752	16.468	0.071	0.000	0.000	25.003	0.219	0.037	0.001	98
      99	53	10	-	-55.050	3.361	14.717	0.145	0.039	0.015	24.422	0.141	0.053	0.005	99
      100	50	10	-	-54.225	0.809	13.769	0.083	0.000	0.000	22.152	0.195	0.047	0.001	100
      101	87	10	-	-54.190	6.893	10.524	0.082	0.090	0.014	17.480	0.182	0.100	0.006	101
      102	93	10	-	-53.904	2.314	14.830	0.068	0.000	0.000	23.240	0.076	0.043	0.000	102
      103	55	10	-	-53.568	6.669	14.739	0.033	0.026	0.009	23.112	0.085	0.052	0.003	103
      104	32	11	-	-50.548	4.058	11.331	0.797	0.035	0.017	19.898	1.058	0.069	0.011	104
      105	79	10	-	-50.529	2.976	16.573	0.038	0.000	0.000	25.040	0.080	0.037	0.000	105
      106	88	10	-	-49.778	5.255	15.849	0.067	0.000	0.000	24.756	0.036	0.038	0.000	106
      107	44	10	-	-49.354	7.328	14.194	0.019	0.000	0.000	23.287	0.161	0.043	0.000	107
      108	120	4	-	-46.538	8.766	12.821	0.050	0.000	0.000	21.468	0.207	0.050	0.001	108
      109	27	12	-	-45.525	6.848	11.290	0.827	0.000	0.000	18.572	1.342	0.064	0.008	109
      110	116	5	-	-45.517	3.319	10.343	0.057	0.000	0.000	17.257	0.423	0.072	0.003	110
      111	40	10	-	-45.441	2.625	12.288	0.063	0.000	0.000	21.187	0.251	0.051	0.001	111
      112	68	10	-	-44.240	1.811	8.542	0.046	0.039	0.015	14.546	0.123	0.108	0.006	112
      113	43	10	-	-43.729	6.095	15.171	0.108	0.000	0.000	22.761	0.057	0.044	0.000	113
      114	13	18	-	-43.691	4.318	13.278	0.104	0.021	0.007	22.962	0.450	0.052	0.002	114
      115	117	5	-	-43.457	9.729	10.550	0.154	0.017	0.000	18.293	0.341	0.072	0.002	115
      116	41	10	-	-42.476	7.209	9.068	0.283	0.000	0.000	16.314	0.438	0.080	0.004	116
      117	64	10	-	-42.104	9.222	13.102	0.107	0.000	0.000	21.255	0.443	0.051	0.002	117
      118	95	10	-	-40.686	4.305	15.197	0.063	0.000	0.000	23.698	0.129	0.041	0.000	118
      119	58	10	-	-39.840	1.959	13.880	0.071	0.000	0.000	22.557	0.166	0.045	0.001	119
      120	39	10	-	-37.130	1.900	11.006	0.186	0.000	0.000	17.019	0.332	0.073	0.002	120
      121	36	10	-	-24.435	0.997	11.997	0.038	0.000	0.000	19.463	0.188	0.058	0.001	121
      122	76	10	-	-16.375	3.018	13.416	0.025	0.000	0.000	22.706	0.087	0.045	0.000	122
      123	42	10	-	-10.570	1.469	10.092	0.124	0.000	0.000	17.541	0.465	0.071	0.003	123
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

In this run we also had a `caprieval` after the clustering of the rigid body models (step 4 of our workflow).

<a class="prompt prompt-info">Inspect the corresponding _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the pre-calculated 4_caprieval/capri_clt.tsv file:</i>
  </summary>
    <pre>
      cluster_rank	cluster_id	n	under_eval	score	score_std	irmsd	irmsd_std	fnat	fnat_std	lrmsd	lrmsd_std	dockq	dockq_std	caprieval_rank
      1	40	10	-	-12.925	0.755	13.403	0.034	0.000	0.000	21.424	0.117	0.050	0.001	1
      2	20	10	-	-10.730	0.386	16.017	0.000	0.000	0.000	24.133	0.000	0.040	0.000	2
      3	11	10	-	-10.139	0.556	15.857	0.000	0.000	0.000	24.143	0.000	0.040	0.000	3
      5	128	10	-	-9.461	0.656	15.461	0.121	0.000	0.000	23.886	0.095	0.041	0.000	4
      4	69	10	-	-8.921	0.171	14.254	0.000	0.000	0.000	22.411	0.000	0.046	0.000	5
      12	88	10	-	-7.933	0.902	15.057	0.055	0.000	0.000	23.167	0.032	0.043	0.000	6
      7	92	10	-	-7.888	0.173	14.981	0.000	0.000	0.000	23.642	0.000	0.041	0.000	7
      6	62	10	-	-7.845	0.175	9.909	0.113	0.000	0.000	15.543	0.256	0.084	0.002	8
      8	82	10	-	-6.984	0.120	13.301	0.000	0.000	0.000	21.881	0.000	0.048	0.000	9
      9	61	10	-	-6.787	0.106	14.379	0.000	0.000	0.000	23.134	0.000	0.043	0.000	10
      11	59	10	-	-6.598	0.366	12.685	0.000	0.000	0.000	20.851	0.000	0.052	0.000	11
      10	64	10	-	-6.453	0.194	7.774	0.000	0.138	0.000	15.156	0.000	0.138	0.000	12
      14	39	10	-	-6.240	0.648	14.552	0.000	0.000	0.000	23.101	0.000	0.043	0.000	13
      13	14	10	-	-6.215	0.594	13.551	0.000	0.017	0.000	23.531	0.000	0.048	0.000	14
      16	136	10	-	-6.106	0.573	14.398	0.000	0.000	0.000	23.115	0.000	0.043	0.000	15
      15	35	10	-	-5.681	0.456	14.596	0.115	0.000	0.000	23.388	0.123	0.043	0.000	16
      18	55	10	-	-5.629	0.550	15.360	0.000	0.000	0.000	23.619	0.000	0.041	0.000	17
      17	100	10	-	-5.540	0.578	14.454	0.000	0.017	0.000	23.209	0.000	0.049	0.000	18
      20	45	10	-	-5.447	0.583	15.923	0.062	0.000	0.000	24.503	0.056	0.039	0.000	19
      19	54	10	-	-5.436	0.434	12.638	0.183	0.000	0.000	20.234	0.601	0.054	0.003	20
      29	134	10	-	-5.106	0.565	13.872	0.000	0.000	0.000	20.718	0.000	0.052	0.000	21
      21	1	10	-	-4.840	0.717	10.316	0.088	0.000	0.000	16.192	0.239	0.079	0.002	22
      22	18	10	-	-4.566	0.461	13.640	0.000	0.000	0.000	20.630	0.000	0.052	0.000	23
      23	12	10	-	-4.500	0.590	10.910	0.000	0.000	0.000	19.503	0.000	0.059	0.000	24
      27	29	10	-	-4.395	0.251	14.738	0.000	0.000	0.000	22.854	0.000	0.044	0.000	25
      24	31	10	-	-4.395	0.217	12.983	0.000	0.000	0.000	20.366	0.000	0.054	0.000	26
      25	28	10	-	-4.341	0.269	10.532	0.221	0.009	0.009	17.600	0.723	0.072	0.002	27
      26	48	10	-	-4.117	0.271	11.428	0.484	0.043	0.009	21.233	0.821	0.067	0.006	28
      28	57	10	-	-3.713	0.258	13.370	0.239	0.000	0.000	21.771	0.059	0.048	0.000	29
      39	115	10	-	-3.238	1.994	14.816	0.034	0.000	0.000	23.075	0.087	0.043	0.000	30
      30	7	10	-	-3.228	0.078	16.858	0.000	0.000	0.000	26.285	0.000	0.034	0.000	31
      31	21	10	-	-3.181	0.364	14.904	0.000	0.000	0.000	23.018	0.000	0.043	0.000	32
      32	56	10	-	-2.818	0.240	16.116	0.012	0.000	0.000	24.674	0.045	0.038	0.000	33
      33	72	10	-	-2.463	0.570	12.839	0.168	0.056	0.007	22.343	0.365	0.065	0.004	34
      34	89	10	-	-2.437	0.467	10.431	0.000	0.069	0.000	17.182	0.000	0.095	0.000	35
      35	98	10	-	-2.172	0.296	14.829	0.324	0.017	0.000	24.804	0.318	0.044	0.001	36
      53	68	10	-	-2.057	0.703	9.577	0.000	0.017	0.000	19.779	0.000	0.066	0.000	37
      42	86	10	-	-1.894	0.720	15.423	0.000	0.000	0.000	23.556	0.000	0.042	0.000	38
      36	4	10	-	-1.743	0.243	13.133	0.000	0.017	0.000	20.519	0.000	0.059	0.000	39
      47	81	10	-	-1.730	0.538	14.595	0.000	0.017	0.000	22.873	0.000	0.050	0.000	40
      37	16	10	-	-1.636	0.362	14.586	0.000	0.017	0.000	21.890	0.000	0.053	0.000	41
      40	122	10	-	-1.568	0.414	11.650	0.000	0.086	0.000	20.836	0.000	0.082	0.000	42
      46	95	10	-	-1.410	0.312	10.477	0.166	0.017	0.000	18.950	0.159	0.069	0.001	43
      38	19	10	-	-1.395	0.125	13.132	0.000	0.000	0.000	21.510	0.000	0.049	0.000	44
      41	90	10	-	-1.246	0.097	2.535	0.000	0.345	0.000	5.317	0.000	0.441	0.000	45
      43	33	10	-	-1.219	0.200	14.753	0.000	0.069	0.000	22.926	0.000	0.067	0.000	46
      44	83	10	-	-1.211	0.430	14.651	0.000	0.000	0.000	22.855	0.000	0.044	0.000	47
      45	93	10	-	-1.129	0.330	12.217	0.000	0.000	0.000	19.162	0.000	0.060	0.000	48
      48	38	10	-	-0.659	0.390	10.615	0.000	0.000	0.000	16.944	0.000	0.074	0.000	49
      49	138	10	-	-0.508	0.323	14.657	0.000	0.000	0.000	22.827	0.000	0.044	0.000	50
      50	116	10	-	-0.508	0.826	12.890	0.000	0.000	0.000	21.465	0.000	0.050	0.000	51
      51	71	10	-	0.238	0.234	14.396	0.000	0.000	0.000	21.398	0.000	0.049	0.000	52
      52	30	10	-	0.386	0.830	11.978	0.000	0.000	0.000	20.524	0.000	0.054	0.000	53
      55	132	10	-	0.476	0.336	14.904	0.000	0.000	0.000	21.778	0.000	0.047	0.000	54
      54	85	10	-	0.675	0.419	1.483	0.348	0.616	0.157	2.500	0.599	0.684	0.099	55
      57	80	10	-	0.855	1.116	13.629	0.000	0.034	0.000	23.309	0.000	0.055	0.000	56
      91	109	10	-	0.931	0.501	12.545	0.000	0.000	0.000	18.859	0.000	0.061	0.000	57
      56	73	10	-	0.935	0.129	13.865	0.000	0.017	0.000	23.819	0.000	0.047	0.000	58
      59	74	10	-	1.034	0.221	11.393	0.000	0.000	0.000	17.851	0.000	0.067	0.000	59
      58	121	10	-	1.042	0.797	13.598	0.000	0.000	0.000	19.177	0.000	0.059	0.000	60
      61	26	10	-	1.404	0.362	10.784	0.000	0.034	0.000	18.978	0.000	0.074	0.000	61
      74	99	10	-	1.505	0.137	5.592	0.000	0.069	0.000	14.052	0.000	0.135	0.000	62
      60	25	10	-	1.536	0.490	12.884	0.000	0.000	0.000	18.468	0.000	0.063	0.000	63
      63	63	10	-	1.569	0.908	12.982	0.469	0.000	0.000	22.020	1.741	0.048	0.006	64
      62	2	10	-	1.837	0.762	11.164	0.000	0.052	0.000	19.040	0.000	0.079	0.000	65
      64	41	10	-	2.013	0.260	14.068	0.000	0.000	0.000	22.077	0.000	0.047	0.000	66
      65	5	10	-	2.156	0.427	10.791	0.000	0.000	0.000	17.019	0.000	0.073	0.000	67
      90	75	10	-	2.251	0.585	5.066	0.000	0.069	0.000	9.975	0.000	0.190	0.000	68
      67	50	10	-	2.401	0.335	14.563	0.000	0.052	0.000	24.552	0.000	0.056	0.000	69
      66	110	10	-	2.432	0.585	11.423	0.000	0.000	0.000	19.224	0.000	0.060	0.000	70
      68	103	10	-	2.514	0.496	12.761	0.000	0.000	0.000	18.893	0.000	0.061	0.000	71
      71	101	10	-	2.560	0.273	12.562	0.000	0.000	0.000	20.703	0.000	0.053	0.000	72
      72	124	10	-	2.738	1.042	5.087	0.000	0.155	0.000	10.120	0.000	0.216	0.000	73
      69	36	10	-	2.790	0.207	16.902	0.145	0.000	0.000	24.913	0.185	0.037	0.000	74
      78	60	10	-	2.914	0.449	11.694	0.000	0.000	0.000	19.183	0.000	0.060	0.000	75
      70	49	10	-	2.944	0.075	11.857	0.000	0.034	0.000	21.364	0.000	0.062	0.000	76
      88	107	10	-	3.058	2.268	14.619	0.158	0.000	0.000	23.064	0.574	0.043	0.002	77
      75	111	10	-	3.351	0.712	12.503	0.000	0.017	0.000	23.218	0.000	0.050	0.000	78
      73	9	10	-	3.357	0.253	9.774	0.000	0.000	0.000	15.433	0.000	0.085	0.000	79
      76	47	10	-	3.671	0.217	13.872	0.065	0.004	0.007	24.566	0.146	0.041	0.002	80
      79	78	10	-	3.678	1.717	12.076	0.000	0.052	0.000	21.755	0.000	0.066	0.000	81
      81	51	10	-	3.745	0.410	4.153	0.000	0.103	0.000	6.798	0.000	0.276	0.000	82
      77	79	10	-	3.945	0.270	13.402	0.000	0.000	0.000	22.188	0.000	0.047	0.000	83
      80	17	10	-	3.955	0.883	13.463	0.000	0.000	0.000	22.895	0.000	0.044	0.000	84
      89	130	10	-	4.205	0.668	13.286	0.000	0.000	0.000	21.366	0.000	0.050	0.000	85
      82	67	10	-	4.267	0.278	10.556	0.000	0.017	0.000	18.409	0.000	0.071	0.000	86
      85	32	10	-	4.356	0.841	13.516	0.086	0.000	0.000	21.320	0.051	0.050	0.000	87
      84	114	10	-	4.651	0.413	14.224	0.000	0.000	0.000	21.578	0.000	0.048	0.000	88
      83	10	10	-	4.687	0.269	13.434	0.000	0.000	0.000	20.399	0.000	0.053	0.000	89
      86	8	10	-	4.688	0.510	17.516	0.000	0.000	0.000	26.049	0.000	0.035	0.000	90
      87	58	10	-	5.001	0.603	8.479	0.001	0.121	0.000	15.383	0.000	0.128	0.000	91
      101	141	10	-	5.056	0.911	14.978	0.000	0.017	0.000	22.349	0.000	0.051	0.000	92
      95	133	10	-	5.170	0.585	12.375	0.000	0.017	0.000	20.811	0.000	0.058	0.000	93
      92	87	10	-	5.251	0.124	13.506	0.000	0.000	0.000	22.629	0.000	0.045	0.000	94
      93	120	10	-	5.497	0.599	12.373	0.000	0.000	0.000	19.683	0.000	0.057	0.000	95
      94	27	10	-	5.790	0.199	8.495	0.000	0.034	0.000	14.481	0.000	0.107	0.000	96
      103	96	10	-	5.906	0.479	14.566	0.000	0.000	0.000	22.629	0.000	0.045	0.000	97
      99	129	10	-	5.907	0.331	14.134	0.000	0.069	0.000	22.657	0.000	0.068	0.000	98
      97	105	10	-	5.929	0.690	14.969	0.056	0.000	0.000	22.642	0.080	0.044	0.001	99
      100	117	10	-	5.971	0.490	13.408	0.000	0.000	0.000	21.813	0.000	0.048	0.000	100
      96	24	10	-	6.025	0.353	14.550	0.000	0.034	0.000	22.100	0.000	0.058	0.000	101
      104	106	10	-	6.113	2.639	7.362	0.131	0.004	0.007	12.702	0.106	0.117	0.004	102
      98	94	10	-	6.160	0.357	16.706	0.008	0.000	0.000	25.092	0.092	0.037	0.000	103
      111	126	10	-	6.505	0.283	14.166	0.000	0.000	0.000	22.492	0.001	0.045	0.000	104
      110	140	10	-	6.538	0.922	7.750	0.000	0.000	0.000	13.963	0.000	0.102	0.000	105
      109	22	10	-	6.688	1.190	9.694	0.048	0.000	0.000	14.315	0.159	0.094	0.001	106
      112	142	10	-	6.785	0.528	12.685	0.088	0.000	0.000	20.691	0.226	0.052	0.001	107
      102	15	10	-	6.826	0.296	13.543	0.000	0.000	0.000	23.882	0.000	0.042	0.000	108
      108	42	10	-	6.962	0.523	11.212	0.000	0.017	0.000	18.910	0.000	0.068	0.000	109
      107	65	10	-	7.032	0.585	14.104	0.000	0.034	0.000	23.768	0.000	0.053	0.000	110
      106	53	10	-	7.052	0.245	12.974	0.000	0.017	0.000	22.407	0.000	0.052	0.000	111
      105	70	10	-	7.068	0.472	9.062	0.000	0.000	0.000	15.333	0.000	0.087	0.000	112
      117	137	10	-	7.907	1.092	11.372	0.107	0.000	0.000	20.206	0.162	0.056	0.001	113
      115	118	10	-	8.217	0.396	14.705	0.000	0.034	0.000	24.680	0.000	0.050	0.000	114
      120	135	10	-	8.244	0.387	14.723	0.074	0.000	0.000	22.755	0.017	0.044	0.000	115
      113	6	10	-	8.290	0.561	15.939	0.155	0.000	0.000	24.010	0.156	0.040	0.000	116
      114	23	10	-	8.534	0.494	14.667	0.000	0.034	0.000	23.361	0.000	0.054	0.000	117
      118	46	10	-	8.584	0.297	14.607	0.000	0.000	0.000	22.439	0.000	0.045	0.000	118
      116	52	10	-	8.626	0.073	13.076	0.000	0.034	0.000	21.077	0.000	0.062	0.000	119
      119	76	10	-	8.738	0.196	13.133	0.422	0.000	0.000	22.329	0.173	0.046	0.001	120
      121	13	10	-	9.000	0.489	13.992	0.000	0.000	0.000	22.481	0.000	0.045	0.000	121
      126	123	10	-	9.154	0.738	14.591	0.000	0.000	0.000	23.260	0.000	0.043	0.000	122
      130	139	10	-	9.191	1.322	13.053	0.330	0.000	0.000	22.965	0.886	0.045	0.003	123
      123	104	10	-	9.273	0.812	13.775	0.000	0.000	0.000	23.083	0.000	0.044	0.000	124
      125	125	10	-	9.418	0.650	13.752	0.250	0.026	0.009	23.171	0.422	0.052	0.004	125
      122	77	10	-	9.516	0.492	10.661	0.296	0.000	0.000	17.319	0.103	0.071	0.001	126
      124	3	10	-	9.758	0.374	14.428	0.000	0.034	0.000	21.942	0.000	0.059	0.000	127
      127	102	10	-	9.882	0.749	11.377	0.000	0.000	0.000	19.716	0.000	0.058	0.000	128
      132	108	10	-	9.926	0.765	8.739	0.000	0.017	0.000	14.595	0.000	0.100	0.000	129
      129	37	10	-	9.943	0.507	9.814	0.000	0.017	0.000	15.996	0.000	0.087	0.000	130
      131	131	10	-	10.020	0.283	15.446	0.000	0.000	0.000	22.899	0.000	0.043	0.000	131
      128	91	10	-	10.130	0.391	15.032	0.220	0.000	0.000	23.201	0.100	0.043	0.000	132
      133	43	10	-	10.640	1.661	10.602	0.000	0.000	0.000	18.071	0.001	0.067	0.000	133
      134	113	10	-	10.860	0.393	9.007	0.000	0.000	0.000	16.713	0.000	0.077	0.000	134
      136	97	10	-	11.372	1.198	11.161	0.121	0.000	0.000	17.073	0.094	0.072	0.000	135
      135	44	10	-	11.648	0.086	11.900	0.000	0.017	0.000	18.763	0.000	0.068	0.000	136
      139	127	10	-	12.333	0.212	13.926	0.168	0.000	0.000	20.746	0.188	0.052	0.001	137
      137	34	10	-	12.422	0.795	13.616	0.543	0.000	0.000	21.178	0.451	0.050	0.002	138
      140	119	10	-	12.685	0.612	10.014	0.281	0.000	0.000	19.676	0.908	0.060	0.005	139
      138	112	10	-	12.813	0.159	13.916	0.000	0.000	0.000	22.043	0.000	0.047	0.000	140
      141	84	10	-	13.223	0.097	12.241	0.000	0.000	0.000	19.872	0.000	0.056	0.000	141
      142	66	10	-	15.759	0.476	12.552	0.000	0.000	0.000	17.958	0.000	0.066	0.000	142
    </pre>
  </details>
<br>

<a class="prompt prompt-question">How many clusters are generated?</a>

<a class="prompt prompt-question">Is this the same number that after refinement (see above)?</a>

<a class="prompt prompt-question">If not what could be the reason?</a>

<a class="prompt prompt-question">Consider now the rank of the first acceptable cluster based on iRMSD values. How does this compare with the refined clusters (see above)?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer:</i>
  </summary>
    <p>
      After rigid body docking the first acceptable cluster is at rank 41. After refinement it scores at the top with score significantly better than the second-ranked cluster!
    </p>
  </details>

<br>

We are providing in the `scripts` directory a simple script that extract some cluster statistics for acceptable or better clusters from the `caprieval` steps.
To use is simply call the script with as argument the run directory you want to analyze, e.g.:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats-clt.sh ./runs/scenario2a-NMR-epitope-pass
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the output of the script:</i>
  </summary>
  <pre>
    ==============================================
    == run2-mpi-surface/4_caprieval/capri_clt.tsv
    ==============================================
    Total number of acceptable or better clusters:  2  out of  142
    Total number of medium or better clusters:      1  out of  142
    Total number of high quality clusters:          0  out of  142

    First acceptable cluster - rank:  41  i-RMSD:  2.535  Fnat:  0.345  DockQ:  0.441
    First medium cluster     - rank:  54  i-RMSD:  1.483  Fnat:  0.616  DockQ:  0.684
    Best cluster             - rank:  54  i-RMSD:  1.483  Fnat:  0.616  DockQ:  0.684
    ==============================================
    == run2-mpi-surface/9_caprieval/capri_clt.tsv
    ==============================================
    Total number of acceptable or better clusters:  2  out of  123
    Total number of medium or better clusters:      1  out of  123
    Total number of high quality clusters:          0  out of  123

    First acceptable cluster - rank:  1  i-RMSD:  1.466  Fnat:  0.797  DockQ:  0.743
    First medium cluster     - rank:  1  i-RMSD:  1.466  Fnat:  0.797  DockQ:  0.743
  </pre>
</details>

<br>

Similarly some simple statistics can be extracted from the single model `caprieval` `capri_ss.tsv` files with the `extract-capri-stats.sh` script:


<a class="prompt prompt-cmd">
./scripts/extract-capri-stats.sh ./runs/scenario2a-NMR-epitope-pass
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the output of the script:</i>
  </summary>
  <pre>
    ==============================================
    == run2-mpi-surface/4_caprieval/capri_ss.tsv
    ==============================================
    Total number of acceptable or better models:  20  out of  1420
    Total number of medium or better models:      9  out of  1420
    Total number of high quality models:          0  out of  1420

    First acceptable model - rank:  372  i-RMSD:  2.535  Fnat:  0.345  DockQ:  0.441
    First medium model     - rank:  511  i-RMSD:  1.282  Fnat:  0.707  DockQ:  0.741
    Best model             - rank:  574  i-RMSD:  1.049  Fnat:  0.569  DockQ:  0.721
    ==============================================
    == run2-mpi-surface/9_caprieval/capri_ss.tsv
    ==============================================
    Total number of acceptable or better models:  22  out of  1379
    Total number of medium or better models:      11  out of  1379
    Total number of high quality models:          0  out of  1379

    First acceptable model - rank:  1  i-RMSD:  1.165  Fnat:  0.879  DockQ:  0.822
    First medium model     - rank:  1  i-RMSD:  1.165  Fnat:  0.879  DockQ:  0.822
    Best model             - rank:  11  i-RMSD:  1.038  Fnat:  0.862  DockQ:  0.835
  </pre>
</details>

<br>

_**Note**_ that this kind of analysis only makes sense when we know the reference complex and for benchmarking / performance analysis purposes.

<a class="prompt prompt-info">Look at the single structure statistics provided by the script</a>

<a class="prompt prompt-question">How does the quality of the model changes after flexible refinement? Consider here the various metrics.</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer:</i>
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
    <i>Answer:</i>
  </summary>
  <p>
    This is clearly not the case. The scoring function is not perfect, but does a reasonable job in ranking models of acceptable or better quality on top in this case.
  </p>
</details>

<br>

#### Analysis scenario 1: visualizing the scores and their components

We have precalculated a number of interactive plots to visualize the scores and their components versus ranks and model quality.

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>

Models statistics:

* [iRMSD versus HADDOCK score](plots/scenario1-surface/irmsd_score.html){:target="_blank"}
* [DockQ versus HADDOCK score](plots/scenario1-surface/dockq_score.html){:target="_blank"}
* [DockQ versus van der Waals energy](plots/scenario1-surface/dockq_vdw.html){:target="_blank"}
* [DockQ versus electrostatic energy](plots/scenario1-surface/dockq_elec.html){:target="_blank"}
* [DockQ versus ambiguous restraints energy](plots/scenario1-surface/dockq_air.html){:target="_blank"}
* [DockQ versus desolvation energy](plots/scenario1-surface/dockq_desolv.html){:target="_blank"}

Cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank):

* [HADDOCK scores](plots/scenario1-surface/score_clt.html){:target="_blank"}
* [van der Waals energies](plots/scenario1-surface/vdw_clt.html){:target="_blank"}
* [electrostatic energies](plots/scenario1-surface/elec_clt.html){:target="_blank"}
* [ambiguous restraints energies](plots/scenario1-surface/air_clt.html){:target="_blank"}
* [desolvation energies](plots/scenario1-surface/desolv_clt.html){:target="_blank"}


<a class="prompt prompt-question">For this antibody-antigen case, which of the score component is correlating best with the quality of the models?.</a>

<hr>

### Analysis scenario 2a: Paratope - NMR-epitope as passive

Let us now analyze the docking results for this scenario. Use for that either your own run or a pre-calculated run provided in the `runs` directory (note that to save space only partial data have been kept in this pre-calculated runs, but all relevant information for this tutorial is available).

First of all let us check the final cluster statistics.

<a class="prompt prompt-info">Inspect the _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the pre-calculated 9_caprieval/capri_clt.tsv file:</i>
  </summary>
  <pre>
    cluster_rank    cluster_id      n       under_eval      score   score_std       irmsd   irmsd_std       fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std             caprieval_rank
    1       6       10      -       -137.815        5.725   1.192   0.126   0.797   0.051   2.581   0.713   0.774   0.044   1
    2       2       16      -       -109.687        4.310   14.951  0.044   0.069   0.000   22.895  0.030   0.067   0.000   2
    3       8       4       -       -105.095        13.247  14.909  0.119   0.069   0.000   23.066  0.336   0.066   0.001   3
    4       5       10      -       -100.189        4.222   5.148   0.024   0.130   0.015   10.476  0.586   0.202   0.014   4
    5       1       21      -       -88.813 8.067   8.637   0.162   0.125   0.014   15.842  0.277   0.126   0.004   5
    6       4       10      -       -84.534 6.278   4.258   0.119   0.233   0.076   8.326   0.256   0.284   0.027   6
    7       7       9       -       -67.116 5.464   6.978   0.279   0.138   0.012   13.652  0.502   0.154   0.010   7
    8       3       10      -       -52.597 8.348   4.736   0.334   0.125   0.014   9.410   0.615   0.223   0.017   8
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

In this run we also had a `caprieval` after the clustering of the rigid body models (step 4 of our workflow).

<a class="prompt prompt-info">Inspect the corresponding _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the pre-calculated 4_caprieval/capri_clt.tsv file:</i>
  </summary>
  <pre>
    cluster_rank    cluster_id      n       under_eval      score   score_std       irmsd   irmsd_std       fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std             caprieval_rank
    1       1       10      -       -6.886  0.250   14.798  0.000   0.069   0.000   23.003  0.000   0.066   0.000   1
    2       4       10      -       -4.685  0.268   1.247   0.000   0.690   0.000   2.093   0.000   0.741   0.000   2
    3       5       10      -       -3.176  0.361   12.988  0.000   0.069   0.000   21.338  0.000   0.073   0.000   3
    4       6       10      -       -2.576  0.140   5.104   0.000   0.138   0.000   10.149  0.000   0.210   0.000   4
    5       3       10      -       -2.535  0.183   8.639   0.000   0.121   0.000   15.932  0.000   0.124   0.000   5
    6       2       10      -       0.258   0.306   10.007  0.027   0.048   0.008   17.988  0.047   0.084   0.003   6
    7       8       10      -       3.854   0.077   4.032   0.000   0.121   0.000   8.122   0.000   0.255   0.000   7
    8       9       10      -       4.665   0.189   7.100   0.000   0.121   0.000   13.749  0.000   0.147   0.000   8
    9       7       10      -       10.165  0.434   4.776   0.000   0.086   0.000   9.249   0.000   0.211   0.000   9
  </pre>
</details>

<br>

<a class="prompt prompt-question">How many clusters are generated?</a>

<a class="prompt prompt-question">Is this the same number that after refinement (see above)?</a>

<a class="prompt prompt-question">If not what could be the reason?</a>

<a class="prompt prompt-question">Consider now the rank of the first acceptable cluster based on iRMSD values. How does this compare with the refined clusters (see above)?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer:</i>
  </summary>
  <p>
    After rigid body docking the first acceptable cluster is at rank 2. After refinement it scores at the top with score significantly better than the second-ranked cluster.
  </p>
</details>

<br>

<a class="prompt prompt-question">Did the rank improve after refinement?</a>

We are providing in the `scripts` a simple script that extract some cluster statistics for acceptable or better clusters from the `caprieval` steps.
To use is simply call the script with as argument the run directory you want to analyze, e.g.:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats-clt.sh ./runs/scenario2a-NMR-epitope-pass
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the output of the script:</i>
  </summary>
  <pre>
    ==============================================
    == scenario2a-NMR-epitope-pass//4_caprieval/capri_clt.tsv
    ==============================================
    Total number of acceptable or better clusters:  1  out of  9
    Total number of medium or better clusters:      1  out of  9
    Total number of high quality clusters:          0  out of  9

    First acceptable cluster - rank:  2  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
    First medium cluster     - rank:  2  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
    Best cluster             - rank:  2  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
    ==============================================
    == scenario2a-NMR-epitope-pass//9_caprieval/capri_clt.tsv
    ==============================================
    Total number of acceptable or better clusters:  1  out of  8
    Total number of medium or better clusters:      1  out of  8
    Total number of high quality clusters:          0  out of  8

    First acceptable cluster - rank:  1  i-RMSD:  1.192  Fnat:  0.797  DockQ:  0.774
    First medium cluster     - rank:  1  i-RMSD:  1.192  Fnat:  0.797  DockQ:  0.774
    Best cluster             - rank:  1  i-RMSD:  1.192  Fnat:  0.797  DockQ:  0.774
  </pre>
</details>

<br>

Similarly some simple statistics can be extracted from the single model `caprieval` `capri_ss.tsv` files with the `extract-capri-stats.sh` script:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats.sh ./runs/scenario2a-NMR-epitope-pass
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the output of the script:</i>
  </summary>
  <pre>
    ==============================================
    == scenario2a-NMR-epitope-pass//4_caprieval/capri_ss.tsv
    ==============================================
    Total number of acceptable or better models:  10  out of  90
    Total number of medium or better models:      10  out of  90
    Total number of high quality models:          2  out of  90

    First acceptable model - rank:  11  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
    First medium model     - rank:  11  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
    Best model             - rank:  18  i-RMSD:  0.980  Fnat:  0.586  DockQ:  0.739
    ==============================================
    == scenario2a-NMR-epitope-pass//9_caprieval/capri_ss.tsv
    ==============================================
    Total number of acceptable or better models:  10  out of  90
    Total number of medium or better models:      10  out of  90
    Total number of high quality models:          0  out of  90

    First acceptable model - rank:  1  i-RMSD:  1.252  Fnat:  0.793  DockQ:  0.770
    First medium model     - rank:  1  i-RMSD:  1.252  Fnat:  0.793  DockQ:  0.770
    Best model             - rank:  2  i-RMSD:  1.048  Fnat:  0.879  DockQ:  0.829
  </pre>
</details>
<br>

_**Note**_ that this kind of analysis only makes sense when we know the reference complex and for benchmarking / performance analysis purposes.

<a class="prompt prompt-info">Look at the single structure statistics provided by the script</a>

<a class="prompt prompt-question">How does the quality of the model changes after flexible refinement? Consider here the various metrics.</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer:</i>
  </summary>
  <p>
    In terms of iRMSD values we only observe very small differences with a slight increase.
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
    <i>Answer:</i>
  </summary>
  <p>
    This is clearly not the case. The scoring function is not perfect, but does a reasonable job in ranking models of acceptable or better quality on top in this case.
  </p>
</details>

<br>

#### Analysis scenario 2a: visualizing the scores and their components

We have precalculated a number of interactive plots to visualize the scores and their components versus ranks and model quality.

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>

Models statistics:

* [iRMSD versus HADDOCK score](plots/scenario2a-NMR-epitope-pass/irmsd_score.html){:target="_blank"}
* [DockQ versus HADDOCK score](plots/scenario2a-NMR-epitope-pass/dockq_score.html){:target="_blank"}
* [DockQ versus van der Waals energy](plots/scenario2a-NMR-epitope-pass/dockq_vdw.html){:target="_blank"}
* [DockQ versus electrostatic energy](plots/scenario2a-NMR-epitope-pass/dockq_elec.html){:target="_blank"}
* [DockQ versus ambiguous restraints energy](plots/scenario2a-NMR-epitope-pass/dockq_air.html){:target="_blank"}
* [DockQ versus desolvation energy](plots/scenario2a-NMR-epitope-pass/dockq_desolv.html){:target="_blank"}

Cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank):

* [HADDOCK scores](plots/scenario2a-NMR-epitope-pass/score_clt.html){:target="_blank"}
* [van der Waals energies](plots/scenario2a-NMR-epitope-pass/vdw_clt.html){:target="_blank"}
* [electrostatic energies](plots/scenario2a-NMR-epitope-pass/elec_clt.html){:target="_blank"}
* [ambiguous restraints energies](plots/scenario2a-NMR-epitope-pass/air_clt.html){:target="_blank"}
* [desolvation energies](plots/scenario2a-NMR-epitope-pass/desolv_clt.html){:target="_blank"}

<a class="prompt prompt-question">For this antibody-antigen case, which of the score component is correlating best with the quality of the models?.</a>

<hr>

### Analysis scenario 2b: Paratope - NMR-epitope as active

Let us now analyze the docking results for this scenario. Use for that either your own run or a pre-calculated run provided in the `runs` directory (note that to save space only partial data have been kept in this pre-calculated runs, but all relevant information for this tutorial is available).

First of all let us check the final cluster statistics.

<a class="prompt prompt-info">Inspect the _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
    <summary style="bold">
      <i>View the pre-calculated 9_caprieval/capri_clt.tsv file:</i>
    </summary>
    <pre>
      cluster_rank    cluster_id      n       under_eval      score   score_std       irmsd   irmsd_std       fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std             caprieval_rank
      1       1       17      -       -148.986        7.256   1.774   0.659   0.690   0.136   4.096   1.402   0.652   0.138   1
      2       5       10      -       -131.282        3.481   14.993  0.055   0.069   0.000   23.430  0.078   0.065   0.000   2
      3       6       10      -       -109.953        10.789  4.999   0.104   0.130   0.009   10.137  0.730   0.209   0.013   3
      4       9       9       -       -108.985        6.842   5.048   0.702   0.310   0.068   9.739   1.195   0.277   0.045   4
      5       3       11      -       -102.771        11.794  14.779  0.157   0.095   0.009   23.291  0.274   0.074   0.004   5
      6       8       9       -       -100.618        16.534  4.691   0.704   0.250   0.058   8.812   1.324   0.279   0.051   6
      7       4       10      -       -94.901 3.834   9.640   0.464   0.077   0.015   18.645  0.917   0.091   0.010   7
      8       11      8       -       -86.147 6.887   3.785   0.420   0.383   0.058   7.878   1.242   0.355   0.048   8
      9       12      7       -       -85.281 13.431  14.745  0.102   0.077   0.019   23.084  0.106   0.069   0.006   9
      10      10      8       -       -85.188 8.390   3.042   0.195   0.483   0.056   6.999   0.304   0.425   0.025   10
      11      2       15      -       -81.657 7.278   13.872  0.749   0.086   0.012   22.271  0.727   0.075   0.004   11
      12      7       10      -       -81.123 2.345   7.474   0.122   0.172   0.000   15.516  0.447   0.147   0.004   12
      13      13      4       -       -68.804 9.982   14.468  0.091   0.090   0.014   22.792  0.056   0.075   0.005   13
    </pre>
  </details>

  <br>

  <a class="prompt prompt-question">How many clusters are generated?</a>

  <a class="prompt prompt-question">Can you think of a reason why this scenario leads to more clusters? (think of the differences in the setup of the two scenarios)</a>

  <a class="prompt prompt-question">Look at the score of the first few clusters: Are they significantly different if you consider their average scores and standard deviations?</a>

  <a class="prompt prompt-question">How many clusters of acceptable or better quality have been generate according to CAPRI criteria?</a>

  <a class="prompt prompt-question">What is the rank of the best cluster generated?</a>

  <a class="prompt prompt-question">What is the rank of the first acceptable of better cluster generated?</a>

  In this run we also had a `caprieval` after the clustering of the rigid body models (step 4 of our workflow).

  <a class="prompt prompt-info">Inspect the corresponding _capri_clt.tsv_ file</a>

  <details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the pre-calculated 4_caprieval/capri_clt.tsv file:</i>
  </summary>
  <pre>
    cluster_rank    cluster_id      n       under_eval      score   score_std       irmsd   irmsd_std       fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std             caprieval_rank
    1       7       10      -       -13.629 0.864   2.514   0.090   0.332   0.007   5.341   0.156   0.437   0.010   1
    2       5       10      -       -13.011 1.684   7.800   0.011   0.138   0.000   15.447  0.052   0.135   0.000   2
    3       1       10      -       -11.014 0.302   1.083   0.063   0.733   0.062   2.661   0.486   0.766   0.032   3
    4       3       10      -       -10.651 0.900   5.020   0.032   0.168   0.007   9.968   0.075   0.224   0.004   4
    5       4       10      -       -9.350  1.336   14.819  0.022   0.069   0.000   23.182  0.033   0.066   0.000   5
    6       2       10      -       -8.480  0.941   9.877   0.785   0.043   0.045   18.943  1.710   0.079   0.026   6
    7       14      10      -       -6.270  0.901   12.963  0.009   0.069   0.000   21.422  0.039   0.073   0.000   7
    8       6       10      -       -3.691  0.591   14.746  0.008   0.069   0.000   23.205  0.031   0.066   0.000   8
    10      9       10      -       -2.325  2.898   3.434   0.489   0.267   0.029   7.040   1.183   0.344   0.048   9
    9       8       10      -       -1.813  0.530   3.220   0.088   0.336   0.026   7.050   0.360   0.369   0.005   10
    12      12      10      -       -0.867  1.673   5.290   0.416   0.181   0.015   10.690  1.286   0.216   0.023   11
    11      11      10      -       0.309   1.236   14.796  0.397   0.052   0.012   23.420  0.358   0.059   0.005   12
    13      13      10      -       3.010   1.008   4.422   0.490   0.185   0.033   7.855   0.843   0.278   0.035   13
    14      10      10      -       5.161   0.834   14.703  0.060   0.052   0.000   23.147  0.239   0.060   0.001   14
  </pre>
</details>

<br>

<a class="prompt prompt-question">How many clusters are generated?</a>

<a class="prompt prompt-question">Is this the same number that after refinement (see above)?</a>

<a class="prompt prompt-question">If not what could be the reason?</a>

<a class="prompt prompt-question">Consider again the rank of the first acceptable cluster based on iRMSD values. How does this compare with the refined clusters (see above)?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer:</i>
  </summary>
  <p>
    After rigid body docking the first acceptable cluster is at rank 1 and the same is true after refinement, but the iRMSD values have improved.
  </p>
</details>

<br>

Use the `extract-capri-stats-clt.sh` script to extract some simple cluster statistics for this run.

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats-clt.sh ./runs/scenario2b-NMR-epitope-pass
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the output of the script:</i>
  </summary>
  <pre>
    ==============================================
    == scenario2b-NMR-epitope-act//4_caprieval/capri_clt.tsv
    ==============================================
    Total number of acceptable or better clusters:  4  out of  14
    Total number of medium or better clusters:      1  out of  14
    Total number of high quality clusters:          0  out of  14

    First acceptable cluster - rank:  1  i-RMSD:  2.514  Fnat:  0.332  DockQ:  0.437
    First medium cluster     - rank:  3  i-RMSD:  1.083  Fnat:  0.733  DockQ:  0.766
    Best cluster             - rank:  3  i-RMSD:  1.083  Fnat:  0.733  DockQ:  0.766
    ==============================================
    == scenario2b-NMR-epitope-act//9_caprieval/capri_clt.tsv
    ==============================================
    Total number of acceptable or better clusters:  3  out of  13
    Total number of medium or better clusters:      1  out of  13
    Total number of high quality clusters:          0  out of  13

    First acceptable cluster - rank:  1  i-RMSD:  1.774  Fnat:  0.690  DockQ:  0.652
    First medium cluster     - rank:  1  i-RMSD:  1.774  Fnat:  0.690  DockQ:  0.652
    Best cluster             - rank:  1  i-RMSD:  1.774  Fnat:  0.690  DockQ:  0.652
  </pre>
</details>

<br>

Similarly some simple statistics can be extracted from the single model `caprieval` `capri_ss.tsv` files with the `extract-capri-stats.sh` script:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats.sh ./runs/scenario2b-NMR-epitope-pass
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View the output of the script:</i>
  </summary>
  <pre>
    ==============================================
    == scenario2b-NMR-epitope-act//4_caprieval/capri_ss.tsv
    ==============================================
    Total number of acceptable or better models:  36  out of  140
    Total number of medium or better models:      10  out of  140
    Total number of high quality models:          1  out of  140

    First acceptable model - rank:  2  i-RMSD:  2.533  Fnat:  0.328  DockQ:  0.434
    First medium model     - rank:  13  i-RMSD:  1.152  Fnat:  0.810  DockQ:  0.794
    Best model             - rank:  15  i-RMSD:  0.982  Fnat:  0.776  DockQ:  0.803
    ==============================================
    == scenario2b-NMR-epitope-act//9_caprieval/capri_ss.tsv
    ==============================================
    Total number of acceptable or better models:  31  out of  128
    Total number of medium or better models:      10  out of  128
    Total number of high quality models:          6  out of  128

    First acceptable model - rank:  1  i-RMSD:  2.554  Fnat:  0.552  DockQ:  0.506
    First medium model     - rank:  2  i-RMSD:  1.051  Fnat:  0.897  DockQ:  0.834
    Best model             - rank:  10  i-RMSD:  0.894  Fnat:  0.845  DockQ:  0.854
  </pre>
</details>

<br>

_**Note**_ that this kind of analysis only makes sense when we know the reference complex and for benchmarking / performance analysis purposes.

<a class="prompt prompt-info">Look at the single structure statistics provided by the script</a>

<a class="prompt prompt-question">How does the quality of the model changes after flexible refinement? Consider here the various metrics.</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer:</i>
  </summary>
  <p>
    In this case we observe a small improvement in terms of iRMSD values and quite some large improvement in
    the fraction of native contacts and the DockQ scores. Also the single model rankings have improved, but the top ranked model is not the best one.
  </p>
</details>

<br>

<a class="prompt prompt-question">Is the best model always rank as first?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer:</i>
  </summary>
  <p>
  This is clearly not the case. The scoring function is not perfect, but does a reasonable job in ranking models of acceptable or better quality on top in this case.
  </p>
</details>

<br>

#### Analysis scenario 2b: visualizing the scores and their components

We have precalculated a number of interactive plots to visualize the scores and their components versus ranks and model quality.

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>

Models statistics:

* [iRMSD versus HADDOCK score](plots/scenario2b-NMR-epitope-act/irmsd_score.html){:target="_blank"}
* [DockQ versus HADDOCK score](plots/scenario2b-NMR-epitope-act/dockq_score.html){:target="_blank"}
* [DockQ versus van der Waals energy](plots/scenario2b-NMR-epitope-act/dockq_vdw.html){:target="_blank"}
* [DockQ versus electrostatic energy](plots/scenario2b-NMR-epitope-act/dockq_elec.html){:target="_blank"}
* [DockQ versus ambiguous restraints energy](plots/scenario2b-NMR-epitope-act/dockq_air.html){:target="_blank"}
* [DockQ versus desolvation energy](plots/scenario2b-NMR-epitope-act/dockq_desolv.html){:target="_blank"}

Cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank):

* [HADDOCK scores](plots/scenario2b-NMR-epitope-act/score_clt.html){:target="_blank"}
* [van der Waals energies](plots/scenario2b-NMR-epitope-act/vdw_clt.html){:target="_blank"}
* [electrostatic energies](plots/scenario2b-NMR-epitope-act/elec_clt.html){:target="_blank"}
* [ambiguous restraints energies](plots/scenario2b-NMR-epitope-act/air_clt.html){:target="_blank"}
* [desolvation energies](plots/scenario2b-NMR-epitope-act/desolv_clt.html){:target="_blank"}

<a class="prompt prompt-question">For this antibody-antigen case, which of the score component is correlating best with the quality of the models?.</a>

<hr>

### Comparing the performance of the three scenarios

Clearly all three scenarios give good results with an acceptable cluster in all three cases ranked at the top:

{% highlight shell %}
=============================================================
== scenario1-surface//9_caprieval/capri_clt.tsv
=============================================================
Total number of acceptable or better clusters:  2  out of  123
Total number of medium or better clusters:      1  out of  123
Total number of high quality clusters:          0  out of  123

First acceptable cluster - rank:  1  i-RMSD:  1.466  Fnat:  0.797  DockQ:  0.743
First medium cluster     - rank:  1  i-RMSD:  1.466  Fnat:  0.797  DockQ:  0.743
Best cluster             - rank:  1  i-RMSD:  1.466  Fnat:  0.797  DockQ:  0.743

=============================================================
== scenario2a-NMR-epitope-pass//9_caprieval/capri_clt.tsv
=============================================================
Total number of acceptable or better clusters:  1  out of  8
Total number of medium or better clusters:      1  out of  8
Total number of high quality clusters:          0  out of  8

First acceptable cluster - rank:  1  i-RMSD:  1.192  Fnat:  0.797  DockQ:  0.774
First medium cluster     - rank:  1  i-RMSD:  1.192  Fnat:  0.797  DockQ:  0.774
Best cluster             - rank:  1  i-RMSD:  1.192  Fnat:  0.797  DockQ:  0.774

=============================================================
== scenario2b-NMR-epitope-act//9_caprieval/capri_clt.tsv
=============================================================
Total number of acceptable or better clusters:  3  out of  13
Total number of medium or better clusters:      1  out of  13
Total number of high quality clusters:          0  out of  13

First acceptable cluster - rank:  1  i-RMSD:  1.774  Fnat:  0.690  DockQ:  0.652
First medium cluster     - rank:  1  i-RMSD:  1.774  Fnat:  0.690  DockQ:  0.652
Best cluster             - rank:  1  i-RMSD:  1.774  Fnat:  0.690  DockQ:  0.652

{% endhighlight %}

The best models are obtained when combining the information about the paratope with the NMR epitope defined as passive for HADDOCK,
which is also the scenario described in our Structure 2020 article:

* F. Ambrosetti, B. Jiménez-García, J. Roel-Touris and A.M.J.J. Bonvin. [Modeling Antibody-Antigen Complexes by Information-Driven Docking](https://doi.org/10.1016/j.str.2019.10.011). _Structure_, *28*, 119-129 (2020). Preprint freely available from [here](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3362436).

What is striking here is that the surface-based protocol (scenario1) is givin now thanks to the clustering step after the rigid-body
docking step an excellent solution ranking on top, while these would not make through the refinement stage in the static HADDOCK2.4
protocol (or only very few that would not cluster at the end). Check for comparison our the
[related HADDOCK2.4 tutorial](http://localhost:4000/education/HADDOCK24/HADDOCK24-antibody-antigen/#scenario-2-a-loose-definition-of-the-epitope-is-known-1){:target="_blank"}
where you can find l-RMSD values for the surface scenario. Of course, due to the increased sampling it is also more costly.

<hr>
<hr>

## Visualization of the models

To visualize the models from top cluster of your favorite run,  start PyMOL and load the cluster representatives you want to view, e.g. this could be the top model from cluster1 of scenario2a.
These can be found in the `runs/scenario2a-NMR-epitope-pass/8_seletopclusts/` directory

<a class="prompt prompt-pymol">File menu -> Open -> select cluster_1_model_1.pdb</a>

If you want to get an impression of how well defined a cluster is, repeat this for the best N models you want to view (`cluster_1_model_X.pdb`).
Also load the reference structure from the `pdbs` directory, `4G6M-matched.pdb`.

PyMol can also be started from the command line with as argument all the PDB files you want to visualize, e.g.:

<a class="prompt prompt-cmd">
pymol runs/scenario2a-NMR-epitope-pass/8_seletopclusts/cluster_1_model_[1-4].pdb pdbs/4G6M-matched.pdb
</a>

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
select paratope, (resi 31+32+33+34+35+52+54+55+56+100+101+102+103+104+105+106+1031+1032+1049+1050+1053+1091+1092+1093+1094+1096 and chain A)
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
 <b><i>See the overlay of the best model onto the reference structure</i></b>
 </summary>
 <p> Top4 models of the top cluster of scenario2a superimposed onto the reference crystal structure (in yellow)</p>
 <figure style="text-align: center">
   <img width="75%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/results-best-model.png">
 </figure>
 <br>
</details>

<hr>
<hr>

## Conclusions

We have demonstrated three different scenarios for antibody-antigen modelling, all making use of the paratope information on the
antibody side and either no information (surface) or a NMR-mapped epitope for the other two scenarios. Compared to the static
HADDOCK2.X workflow, the modularity and flexibility of HADDOCK3 allowed to implement a clustering step after rigid-body sampling
and select all resulting clusters for refinement. This strategy led to excellent results in this case while no single acceptable
cluster was obtained with HADDOCK2.4. While HADDOCK3 is still very much work in progress, those results indicate already that we
should be able to improve the performance of antibody-antigen modelling compared to the results we presented in our
[Structure 2020](https://doi.org/10.1016/j.str.2019.10.011){:target="_blank"} article and in the [related HADDOCK2.4 tutorial](/education/HADDOCK24/HADDOCK24-antibody-antigen){:target="_blank"}.

<hr>
<hr>

## Congratulations! 🎉

You have completed this tutorial. If you have any questions or suggestions, feel free to contact us via email or asking a question through our [support center](https://ask.bioexcel.eu){:target="_blank"}.

And check also our [education](/education) web page where you will find more tutorials!

<hr>
<hr>

## A look into the future Virtual Research Environment for HADDOCK3

In the context of a project with the [Netherlands e-Science Center](https://www.esciencecenter.nl){:target="_blank"} we are working on
building a Virtual Research Environment (VRE) for HADDOCK3 that will allow you to build and edit custom workflows,
execute those on a variety of infrastructures (grid, cloud, local, HPC) and provide an interactive analysis
platform for analyzing your HADDOCK3 results. This is _work in progress_ but you can already take a glimpse of the
first component, the workflow builder, [here](https://wonderful-noether-53a9e8.netlify.app){:target="_blank"}.

All the HADDOCK3 VRE software development is open and can be followed from our [GitHub i-VRESSE](https://github.com/i-VRESSE){:target="_blank"} repository.

So stay tuned!

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
