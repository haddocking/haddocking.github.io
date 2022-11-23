---
layout: page
title: "Antibody-antigen modelling tutorial using a local version of HADDOCK3"
excerpt: "A tutorial describing the use of HADDOCK3 to model an antibody-antigen complex"
tags: [HADDOCK, installation, preparation, proteins, docking, analysis]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}


<hr>
## Introduction

This tutorial demonstrates the use of the new modular HADDOCK3 version for predicting 
the structure of an antibody-antigen complex using knowledge of the hypervariable loops 
on the antibody and either the entire surface or an epitope identified from NMR chemical 
shift perturbation data for the antigen to guide the docking.

An antibody is a large protein that generally works by attaching itself to an antigen, 
which is a unique site of the pathogen. The binding harnesses the immune system to directly 
attack and destroy the pathogen. Antibodies can be highly specific while showing low immunogenicity, 
which is achieved by their unique structure. **The fragment crystallizable region (Fc region**) 
activates the immune response and is species-specific, i.e. the human Fc region should not 
induce an immune response in humans.  **The fragment antigen-binding region (Fab region**) 
needs to be highly variable to be able to bind to antigens of various nature (high specificity). 
In this tutorial we will concentrate on the terminal **variable domain (Fv**) of the Fab region. 
 

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-antibody-antigen/antibody_described.png">
</figure>

The small part of the Fab region that binds the antigen is called **paratope**. The part of the antigen 
that binds to an antibody is called **epitope**. The paratope consists of six highly flexible loops, 
known as **complementarity-determining regions (CDRs)** or hypervariable loops whose sequence 
and conformation are altered to bind to different antigens. CDRs are shown in red in the figure below: 

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-antibody-antigen/CDRs.png">
</figure>

In this tutorial we will be working with  Interleukin-1β (IL-1β) 
(PDB code [4I1B](https://www.ebi.ac.uk/pdbe/entry/pdb/4i1b){:target="_blank"})) as an antigen 
and its highly specific monoclonal antibody gevokizumab 
(PDB code [4G6K](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k){:target="_blank"}) 
(PDB code of the complex [4G6M](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6m){:target="_blank"}).  



Throughout the tutorial, colored text will be used to refer to questions or
instructions, and/or PyMOL commands.

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>


<br>
<hr>

## Setup/Requirements

In order to follow this tutorial you will need to work on a Linux or MacOSX
system. We will also make use of [**PyMOL**][link-pymol] (freely available for
most operating systems) in order to visualize the input and output data. We will
provide you links to download the various required software and data.  

Further we are providing pre-processed PDB files for docking and analysis (but the 
preprocessing of those files will also be explained below. The files have been processed 
to facilitate their use in HADDOCK and for allowing comparison with the known reference 
structure of the complex. For this download and unzip the following [zip archive](input-data.zip) 
and note the location of the extracted PDB files in your system. You should find the following files:

* `4G6K_fv.pdb`: The PDB file of the unbound(free) form of the antibody with the two chains defined as a single chain and with residues renumbered to avoid overlap in numbering between the chains. The structure was further truncated to only keep the two domains involved in binding (to save computational time).
* `4I1B-matched.pdb`: The PDB file of the unbound(free) form of the antigen, renumbered to match the numbering of the reference complex.
* `4G6M-matched.pdb`: The PDB file of the reference antibody-antigen complex, matching the chainIDs and residue numbering of the free forms.


<br>
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


<br>
<hr>
## A brief introduction to HADDOCK3


HADDOCK3 is the next generation integrative modelling software in the
long-lasting HADDOCK project. It represents a complete rethinking and rewriting
of the HADDOCK2.X series, implementing a new way to interact with HADDOCK and
offering new features to users who can now define custom workflows. 

In the previous HADDOCK2.x versions, users had access to a highly
parameterisable yet rigid simulation pipeline composed of three steps:
`ridig-body docking (it0)`, `semi-flexible refinemnt (it1)`, and `final refinement (itw)`. 

<figure align="center">
<img width="75%" src="./HADDOCK2-stages.png">
</figure>

In HADDOCK3, users have the freedom to configure docking workflows into
functional pipelines by combining the different HADDOCK3's modules, thus
adapting the workflows to their projects. HADDOCK3 has therefore developed to
truthfully work like a puzzle of many pieces (simulation modules) that users can
combine freely. To this end, the “old” HADDOCK machinery has been modularised,
and several new modules added, including third-party software additions. As a
result, the modularisation achieved in HADDOCK3 allows users to duplicate steps
within one workflow (e.g., to repeat twice the `it1` stage of the HADDOCK2.x
rigid workflow).

Note that, for simplification purposes, at this time, not all functionalities of
HADDOCK2.x have been ported to HADDOCK3, which does not (yet) support NMR RDC,
PCS and diffusion anisotropy restraints, cryo-EM restraints and coarse-graining.
Any type of information that can be converted into ambiguous interaction
restraints can, however, be used in HADDOCK3, which also supports the
*ab initio* docking modes of HADDOCK.

<figure align="center">
<img width="75%" src="./HADDOCK3-workflow-scheme.png">
</figure>

To keep HADDOCK3's modules organised, we catalogued them into several
categories. But, there are no constraints on piping modules of different
categories.

The main module's categories are "topology", "sampling", "refinement",
"scoring", and "analysis". There is no limit to how many modules can belong to a
category. Modules are added as developed, and new categories will be created
if/when needed. You can access the HADDOCK3 documentation page for the list of
all categories and modules. Below is a summary of the available modules:

* **Topology modules**
    * `topoaa`: *generates the all-atom topologies for the CNS engine.*
* **Sampling modules**
    * `rigidbody`: *Rigid body energy minimisation with CNS (`it0` in haddock2.x).*
    * `lightdock`: *Third-party glow-worm swam optimisationdocking software.*
* **Model refinement modules**
    * `flexref`: *Semi-flexible refinement using a simulated annealing protocol through molecular dynamics simulations in torsion angle space (`it1` in haddock2.x).*
    * `emref`: *Refinement by energy minimisation (`itw` EM only in haddock2.4).*
    * `mdref`: *Refinement by a short molecular dynamics simulation in explicit solvent (`itw` in haddock2.X).*
* **Scoring modules**
    * `emscoring`: *scoring of a complex performing a short EM (builds the topology and all missing atoms).*
    * `mdscoring`: *scoring of a complex performing a short MD in explicit solvent + EM (builds the topology and all missing atoms).*
* **Analysis modules**
    * `caprieval`: *Calculates CAPRI metrics (i-RMDS, l-RMSD, Fnat, DockQ) with respect to the top scoring model or reference structure if provided.*
    * `clustfcc`: *Clusters models based on the fraction of common contacts (FCC)*
    * `clustrmsd`: *Clusters models based on pairwise RMSD matrix calculated with the `rmsdmatrix` module.*
    * `rmsdmatrix`: *Calculates the pairwise RMSD matrix between all the models generated in the previous step.*
    * `seletop`: *Selects the top N models from the previous step.*
    * `seletopclusts`: *Selects top N clusters from the previous step.*

The HADDOCK3 workflows are defined in simple configuration text files, similar to the TOML format but with extra features. 
Contrarily to HADDOCK2.X which follows a rigid (yet highly parametrizable)
procedure, in HADDOCK3, you can create your own simulation workflows by
combining a multitude of independent modules that perform specialized tasks.


<br>
<hr>
## Software requirements


### Installing CNS
The other required piece of software to run HADDOCK is its computational engine,
CNS (Crystallography and NMR System –
[https://cns-online.org](https://cns-online.org){:target="_blank"} ). CNS is
freely available for non-profit organisations. In order to get access to all
features of HADDOCK you will need to recompile CNS using the additional files
provided in the HADDOCK distribution in the `varia/cns1.3` directory. Compilation of
CNS might be non-trivial. Some guidance on installing cns can is provided in the online 
HADDOCK3 documentation page [here](https://www.bonvinlab.org/haddock3/CNS.html){:target="_blank"}.


<br>
### Installing HADDOCK3

In this tutorial we will make use of the new HADDOCK3 version. In case HADDOCK3
is not pre-installed in your system you will have to install it.

To obtaine HADDOCK3 navigate to [its official repository][haddock-repo], fill the
registration form, and then follow the [installation instructions](https://www.bonvinlab.org/haddock3/INSTALL.html).


<br>
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
with HADDOCK3. If you have activated the HADDOCK3 Python enviroment you have
access to the pdb-tools package.

**[PyMol][link-pymol]**: We will make use of PyMol for visualisation. If not
already installed on your system, download and install PyMol.


<br>
<hr>
## Preparing PDB files for docking

In this section we will prepare the PDB files of the antibody and antigen for docking.
Crystal structures of both the antibody and the antigen in their free forms are available from the 
[PDB database](https://www.pdbe.org){:target="_blank"}. In the case of the antibody which consists 
of two chains (L+H) we will have to prepare it for use in HADDOCK such as it can be treated as 
a single chain with non-overlapping residue numbering. For this we will be making use of `pdb-tools` from the command line.

_**Note**_ that `pdb-tools` is also available as a [webserver](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.


_**Note**_: Before starting to work on the tutorial, make sure to activate haddock3, e.g. if installed using `conda`

<a class="prompt prompt-cmd">
conda activate haddock3
</a>


<br>
### Preparing the antibody structure

Using PDB-tools we will download the structure from the PDB database (the PDB ID is [4G6K](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k){:target="_blank"}) and then process it to have a unique chain ID (A) and non-overlapping residue numbering by shifting the residue numbering of the second chain.

This can be done from the command line with:

<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy -strict  | pdb_selchain -H | pdb_delhetatm | pdb_fixinsert | grep ATOM | pdb_tidy -strict > 4G6K_H.pdb<br>
</a>
<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy -strict  | pdb_selchain -L | pdb_delhetatm | pdb_fixinsert | pdb_shiftres -1000 | grep ATOM | pdb_tidy -strict > 4G6K_L.pdb<br>
</a>
<a class="prompt prompt-cmd">
pdb_merge 4G6K_H.pdb 4G6K_L.pdb |pdb_chain -A |pdb_chainxseg | pdb_tidy -strict > 4G6K_clean.pdb<br>
</a>

The first command fetches the PDB ID, select the heavy chain (H) and removes water and heteroatoms (in this case no co-factor is present that should be kept).
An important part for antibodies is the `pdb_fixinsert` command that fixes the residue numbering of the HV loops: Antibodies often follow the [Chothia numbering scheme](https://pubmed.ncbi.nlm.nih.gov/9367782/?otool=inluulib){:target="_blank"} and insertions created by this numbering scheme (e.g. 82A,82B,82C) cannot be processed by HADDOCK directly. As such renumbering is necessary before starting the docking. 

The second command does the same for the light chain (L) with an additional step of shifting the residue numbering by 1000 (using `pdb_shiftres`) to avoid overlap in the numbering of the two chains.

The third and last command merges the two processed chains and assign them unique chain- and segIDs, resulting in the HADDOCK-ready `4G6K_clean.pdb` file.

_**Note**_ that the corresponding files can be found in the `pdbs` directory of the archive you downloaded.


<br>
### Preparing the antigen structure



<br>
### Dealing with multi-chain proteins

**Note** that this structure consists of two separate chains. It will therefore
be important to define a few distance restraints to keep them together during
the high temperature flexible refinement stage of HADDOCK. This can easily be
done using another script from `haddock-tools`:

<a class="prompt prompt-cmd">
  restrain_bodies.py  4G6K-clean.pdb >antibody-unambig.tbl
</a>

The result file contains two CA-CA distance restraints with the exact distance
measured between the picked CA atoms:

<pre style="background-color:#DAE4E7">
  assign (segid  and resi 189 and name CA) (segid  and resi 693 and name CA) 21.023 0.0 0.0
  assign (segid  and resi 116 and name CA) (segid  and resi 702 and name CA) 44.487 0.0 0.0
</pre>

**Note** that in this example, we are missing segment identifiers since they
were not present in the PDBs. And if they are present, make sure those match
what you are going to define as segIDs in HADDOCK. So in this case we need to
add `A` for the first molecule and `B` for the second:

<pre style="background-color:#DAE4E7">
  assign (segid A and resi 189 and name CA) (segid B and resi 693 and name CA) 21.023 0.0 0.0
  assign (segid A and resi 116 and name CA) (segid B and resi 702 and name CA) 44.487 0.0 0.0
</pre>

This is the file you should save as `unambig.tbl` and pass to HADDOCK.


<br>
## Defining restraints for docking

Before setting up the docking we need first to generate distance restraint files
in a format suitable for HADDOCK.  HADDOCK uses [CNS][link-cns] as computational
engine. A description of the format for the various restraint types supported by
HADDOCK can be found in our [Nature Protocol][nat_prot] paper, Box 4.

Distance restraints are defined as:

<pre style="background-color:#DAE4E7">
  assi (selection1) (selection2) distance, lower-bound correction, upper-bound correction
</pre>

The lower limit for the distance is calculated as: distance minus lower-bound
correction and the upper limit as: distance plus upper-bound correction.  The
syntax for the selections can combine information about chainID - `segid`
keyword -, residue number - `resid` keyword -, atom name - `name` keyword.
Other keywords can be used in various combinations of OR and AND statements.
Please refer for that to the [online CNS manual](https://cns-online.org/v1.3/).

We will shortly explain in this section how to generate both ambiguous
interaction restraints (AIRs) and specific distance restraints for use in
HADDOCK illustrating three scenarios:

* **Interface mapping on both side** (e.g. from NMR chemical shift perturbation data)
* **Specific distance restraints** (e.g. cross-links detected by MS)
* **Interface mapping on one side, full surface on the other**

Information about various types of distance restraints in HADDOCK can also be
found in our [online manual][air-help] pages.

### Defining AIRs from interface mapping

We will use as example here the NMR chemical shift perturbations from the
E2A-HPR complex used in our [HADDOCK 2.4 webserver basic protein-protein docking
tutorial][haddock24protein]. The following residues of E2A were identified by
[Wang *et al*, EMBO J (2000)][wang2000] as having significant chemical shift
perturbations:

<a class="prompt prompt-info">38,40,45,46,69,71,78,80,94,96,141</a>

Let's visualize them in PyMOL using the clean PDB file we created in the
[Cleaning PDB files prior to docking](#cleaning-pdb-files-prior-to-docking)
section of this tutorial:

<a class="prompt prompt-cmd">
  pymol e2a_1F3G-clean.pdb
</a>

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select e2a_active, (resi 38,40,45,46,69,71,78,80,94,96,141)<br>
color red, e2a_active<br>
</a>

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/e2a-surface-airs.png">
</figure>

Inspect the surface.


<a class="prompt prompt-question">
    Do the identified residues form a well defined patch on the surface?
</a>

<a class="prompt prompt-question">
    Do they form a contiguous surface?
</a>

The answer to the last question should be **no**: We can observe residue in the
center of the patch that do not seem significantly affected while still being in
the middle of the defined interface. This is the reason why in HADDOCK we also
define "*passive*" residues that correspond to surface neighbors of active
residues. These should be selected manually, filtering for solvent accessible
residues (the HADDOCK server will do it for you).

<!-- TODO: describe behaviour in HADDOCK3 -->
<!-- TODO: add the list of residues -->

In the same PyMol session as before you can visualize them with:

<a class="prompt prompt-pymol">
select e2a_passive, (resi 35,37,39,42,43,44,47,48,64,66,68,72,73,74,82,83,84,86,97,99,100,105,109,110,112,131,132,133,143,144)<br>
color green, e2a_passive<br>
</a>

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-local-tutorial/e2a-active-passive.png">
</figure>

In general it is better to be too generous rather than too strict in the
definition of passive residues.

And important aspect is to filter both the active (the residues identified from
your mapping experiment) and passive residues by their solvent accessibility.
Our webserver uses a default relative accessibility of 15% as cutoff. This is
not a hard limit. You might consider including even more buried residues if some
important chemical group seems solvent accessible from a visual inspection.

We can use `freesasa` to calculate the solvent accessibility for the different
residues:

<a class="prompt prompt-cmd">
  freesasa e2a_1F3G.pdb \-\-format=rsa >e2a_1F3G.rsa
</a>

The results is file similar to the output of `naccess` containing the per
residue solvent accessibility, both absolute and relative values, and also
distinguishing between backbone and side-chains:

<pre style="background-color:#DAE4E7">
REM  FreeSASA 2.0.3
REM  Absolute and relative SASAs for e2a_1F3G.pdb
REM  Atomic radii and reference values for relative SASA: ProtOr
REM  Chains: A
REM  Algorithm: Lee & Richards
REM  Probe-radius: 1.40
REM  Slices: 20
REM RES _ NUM      All-atoms   Total-Side   Main-Chain    Non-polar    All polar
REM                ABS   REL    ABS   REL    ABS   REL    ABS   REL    ABS   REL
RES THR A  19   125.49  89.3  59.11  59.9  66.38 158.2  33.47  45.0  92.02 139.1
RES ILE A  20    29.18  16.6  23.16  17.3   6.02  14.5  29.18  21.0   0.00   0.0
RES GLU A  21    63.92  36.7  50.29  38.0  13.63  32.5  13.71  26.5  50.21  41.0
RES ILE A  22     0.00   0.0   0.00   0.0   0.00   0.0   0.00   0.0   0.00   0.0
RES ILE A  23    25.26  14.4  25.26  18.8   0.00   0.0  25.26  18.2   0.00   0.0
...
</pre>

The following command will return all residues with a relative SASA for either
the backbone or the side-chain > 15%:

<a class="prompt prompt-cmd">
  awk \'{if (NF==13 && $5>40) print $0; if (NF==14 && $6>40) print $0}\' e2a_1F3G.rsa
</a>

Once you have defined your active and passive residues for both molecules, you
can proceed with the generation of the AIR restraint file for HADDOCK.  For this
you can either make use of our online [GenTBL][gentbl] webserver, entering the
list of active and passive residues for each molecule, and saving the resulting
restraint list to a text file, or use the relevant `haddock-tools` script.

To use our `haddock-tools` `active-passive-to-ambig.py` script you need to
create for each molecule a file containing two lines:

* The first line corresponds to the list of active residues (numbers separated by spaces)
* The second line corresponds to the list of passive residues.

For our E2A-HPR example this would be:

* For E2A (a file called [e2a-act-pass.list](/education/HADDOCK24/HADDOCK24-local-tutorial/e2a-act-pass.list)):
<pre style="background-color:#DAE4E7">
38 40 45 46 69 71 78 80 94 96 141
35 37 39 42 43 44 47 48 64 66 68 72 73 74 82 83 84 86 97 99 100 105 109 110 112 131 132 133 143 144
</pre>

* and for HPR (a file called [hpr-act-pass.list](/education/HADDOCK24/HADDOCK24-local-tutorial/hpr-act-pass.list)):
<pre style="background-color:#DAE4E7">
15 16 17 20 48 49 51 52 54 56
9 10 11 12 21 24 25 34 37 38 40 41 43 45 46 47 53 55 57 58 59 60 84 85
</pre>

Using those two files, we can generate the CNS-formatted AIR restraint files
with the following command:

<a class="prompt prompt-cmd">
  active-passive-to-ambig.py e2a-act-pass.list hpr-act-pass.list > e2a-hpr-ambig.tbl
</a>

This generates a file called `e2a-hpr-ambig.tbl` that contains the AIR
restraints. The default distance range for those is between 0 and 2Å, which
might seem short but makes senses because of the 1/r^6 summation in the AIR
energy function that makes the effective distance be significantly shorter than
the shortest distance entering the sum.

The effective distance is calculated as the SUM over all pairwise atom-atom
distance combinations between an active residue and all the active+passive on
the other molecule: SUM[1/r^6]^(-1/6).

If you modify this file, it is possible to quickly check if the format is valid.
To do so, you can find in the `haddock-tools` repository a folder named
`haddock_tbl_validation` that contains a script called `validate_tbl.py`. To use
it, run:

<a class="prompt prompt-cmd">
  python ~/software/haddock-tools/haddock_tbl_validation/validate_tbl.py --silent e2a-hpr-ambig.tbl
</a>

No output means that your TBL file is valid. You can also find TBL file examples
for different types of restraints in the `haddock-tools/haddock_tbl_validation/`
directory, [or here online][tbl-examples].

### Defining specific distance restraints

You can define in HADDOCK unambiguous distance restraints between specific pairs
of atoms to define restraints coming for example from MS cross-linking
experiments or DEER experiments. As an illustration we will use cross-links from
our [HADDOCK cross-links tutorial](/education/HADDOCK24/HADDOCK24-Xlinks)
obtained for the complex between PRE5 (UniProtKB:
[O14250](https://www.uniprot.org/uniprot/O14250)) and PUP2
(UniProtKB: [Q9UT97](https://www.uniprot.org/uniprot/Q9UT97)).
From MS, we have seven experimentally determined cross-links (4 ADH & 3 ZL)
([Leitner et al.,
2014](https://doi.org/10.1073/pnas.1320298111)), which we will
define as CA-CA distance restraints
([restraints.txt](/education/HADDOCK24/HADDOCK24-local-tutorial/restraints.txt)):

<pre style="background-color:#DAE4E7">
# ADH crosslinks
A  27 CA B  18 CA 0 23
A 122 CA B 125 CA 0 23
A 122 CA B 128 CA 0 23
A 122 CA B 127 CA 0 23

# ZL crosslinks
A 55 CA B 169 CA 0 26
A 55 CA B 179 CA 0 26
A 54 CA B 179 CA 0 26
</pre>

This is the format used by our [DisVis portal](https://wenmr.science.uu.nl/disvis)
to represent the cross-links. Each cross-link definition consists of eight
fields:

1. chainID of the 1st molecule
1. residue number
1. atom name
1. chainID of the 2nd molecule
1. residue number
1. atom name
1. lower distance limit
1. upper distance limit

The corresponding CNS-formatted HADDOCK restraint file for those would be
([unambig-xlinks.tbl](/education/HADDOCK24/HADDOCK24-local-tutorial/unambig-xlinks.tbl)):

<pre style="background-color:#DAE4E7">
assign (segid A and resid 27  and name CA) (segid B and resid 18  and name CA)  23 23 0
assign (segid A and resid 122 and name CA) (segid B and resid 125 and name CA)  23 23 0
assign (segid A and resid 122 and name CA) (segid B and resid 128 and name CA)  23 23 0
assign (segid A and resid 122 and name CA) (segid B and resid 127 and name CA)  23 23 0
assign (segid A and resid 55  and name CA) (segid B and resid 169 and name CA)  26 26 0
assign (segid A and resid 55  and name CA) (segid B and resid 179 and name CA)  26 26 0
assign (segid A and resid 54  and name CA) (segid B and resid 179 and name CA)  26 26 0
</pre>

As a reminder, distance restraints are defined as:

<pre style="background-color:#DAE4E7">
    assign (selection1) (selection2) distance, lower-bound correction, upper-bound correction
</pre>

Where the lower limit for the distance is calculated as the distance minus
lower-bound correction and the upper limit as the distance plus upper-bound
correction.

**Note:** Under Linux (or OSX), this file could be generated automatically from
a text file containing the DisVis restraints with the following command (one
line) in a terminal window:

<a class="prompt prompt-linux">
  cat restraints.txt | awk \'{if (NF == 8) {print \"assi (segid \",$1,\" and resid \",$2,\" and name \",$3,\") (segid \",$4,\" and resid \",$5,\" and name \",$6,\") \",$8,$8,$7}}\' > pre5-pup2-Xlinks.tbl
</a>

[tbl-examples]: https://github.com/haddocking/haddock-tools/tree/master/haddock_tbl_validation "tbl examples"
[gentbl]: https://wenmr.science.uu.nl/gentbl/ "GenTBL"
[haddock24protein]: /education/HADDOCK24/HADDOCK24-protein-protein-basic/
[haddock-repo]: https://github.com/haddocking/haddock3 "HADDOCK 3 GitHub"
[installation]: https://www.bonvinlab.org/haddock3/INSTALL.html "Installation"
[link-forum]: https://ask.bioexcel.eu/c/haddock "HADDOCK Forum"
[link-freesasa]: https://freesasa.github.io "FreeSASA"
[link-pdbtools]:http://www.bonvinlab.org/pdb-tools/ "PDB-Tools"
[link-pymol]: https://www.pymol.org/ "PyMOL"
[nat-pro]: https://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html "Nature protocol"
[air-help]: https://www.bonvinlab.org/software/haddock2.2/generate_air_help/ "AIRs help"
