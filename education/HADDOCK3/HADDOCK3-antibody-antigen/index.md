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


<hr>
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


<hr>
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


<hr>
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


<hr>
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


<hr>
### Preparing the antigen structure

Using PDB-tools we will download the structure from the PDB database (the PDB ID is [4I1B](https://www.ebi.ac.uk/pdbe/entry/pdb/4i1b){:target="_blank"}), remove the hetero atoms and then process it to assign it chainID B. In this case we also select for `ATOM` lines to remove the `ANISOU` statements from the PDB file.

<a class="prompt prompt-cmd">
pdb_fetch 4I1B | pdb_tidy -strict  | pdb_delhetatm  | grep ATOM | pdb_chain -B | pdb_chainxseg | pdb_tidy -strict >4I1B_clean.pdb
</a>


<hr>
<hr>
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
HADDOCK illustrating two scenarios:

* **HV loops on the antibody, full surface on the antigen**
* **HV loops on the antibody, NMR interface mapping on the antigen**

Information about various types of distance restraints in HADDOCK can also be
found in our [online manual][air-help] pages.

<hr>
### Identifying the paratope of the antibody

Nowadays there are several computational tools that can identify the paratope (the residues of the hypervariable loops involved in binding) from the provided antibody sequence. In this tutorial we are providing you the corresponding list of residue obtained using [ProABC-2](https://wenmr.science.uu.nl/proabc2/){:target="_blank"}. ProABC-2 uses a convolutional neural network to identify not only residues which are located in the paratope region but also the nature of interactions they are most likely involved in (hydrophobic or hydrophilic). The work is described in [Ambrosetti, *et al* Bioinformatics, 2020](https://academic.oup.com/bioinformatics/article/36/20/5107/5873593){:target="_blank"}.

The corresponding paratope residues (those with either an overall probability >= 0.4 or a probabily for hydrophobic or hydrophylic > 0.3) are:

<pre style="background-color:#DAE4E7">
    31,32,33,34,35,52,54,55,56,100,101,102,103,104,105,106,1031,1032,1049,1050,1053,1091,1092,1093,1094,1096
</pre>

The numbering corresponds to the numbering of the `4G6K_clean.pdb` PDB file.

Let's visualize those onto the 3D structure.
For this start PyMOL and load `4G6K_clean.pdb`

<a class="prompt prompt-pymol">File menu -> Open -> select 4G6K_clean.pdb</a>

or from the command line:

<a class="prompt prompt-cmd">
    pymol 4G6K_clean.pdb
</a>

We will now highlight the predicted paratope. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all<br>
select paratope, (resi 31+32+33+34+35+52+54+55+56+100+101+102+103+104+105+106+1031+1032+1049+1050+1053+1091+1092+1093+1094+1096)<br>
color red, paratope<br>
</a>

<a class="prompt prompt-question">Can you identify the H3 loop? H stands for heavy chain (the first domain in our case with lower residue numbering). H3 is typically the longest loop.</a>

Let's now switch to a surface representation to inspect the predicted binding site.

<a class="prompt prompt-pymol">
show surface<br>
</a>

Inspect the surface.

<a class="prompt prompt-question">Do the identified residues form a well defined patch on the surface?</a>


<details style="background-color:#DAE4E7">
<summary style="bold">
<b><i>See surface view of the paratope:</i></b>
 </summary>
 <figure align="center">
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
  echo \" \" \> antigen-surface.pass<br>
  awk \'{if (NF==13 && ($7>40 || $9>40)) printf \"\%d \",$3; if (NF==14 && ($8>40 || $10>40)) printf \"\%d \",$4}\' 4I1B_clean.rsa \>\> antigen-surface.pass<br>
</a>

We can visualize the selected surface residues of Interleukin-1β.  
For this start PyMOL and from the PyMOL File menu open the PDB file of the antigen.

<a class="prompt prompt-pymol">File menu -> Open -> select 4I1B_clean.pdb</a>

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select surface40, (resi 3+4+5+6+13+14+15+20+21+22+23+24+25+30+32+33+34+35+37+38+48+49+50+51+52+53+54+55+61+63+64+65+66+73+74+75+76+77+80+84+86+87+88+89+90+91+93+94+96+97+105+106+107+108+109+118+119+126+127+128+129+130+135+136+137+138+139+140+141+142+147+148+150+151+152+153)<br>
color green, surface40<br>
</a>



<hr>
### Antigen scenario 2: NMR-mapped epitope information


The article describing the crystal structure of the antibody-antigen complex we are modelling also reports 
on experimental NMR chemical shift titration experiments to map the binding site of the antibody (gevokizumab) 
on Interleukin-1β. The residues affected by binding are listed in Table 5 of 
[Blech et al. JMB 2013](https://dx.doi.org/10.1016/j.jmb.2012.09.021){:target="_blank"}:

<figure align="center">
   <img width="50%" src="/education/HADDOCK24/HADDOCK24-antibody-antigen-basic/Table5-Blech.png">
</figure>
 
The list of binding site (epitope) residues identified by NMR is:

<pre style="background-color:#DAE4E7">
    72,73,74,75,81,83,84,89,90,92,94,96,97,98,115,116,117
</pre>

We will now visualize the epitope on Interleukin-1β.  For this start PyMOL and from the PyMOL File menu open the provided PDB file of the antigen.

<a class="prompt prompt-pymol">File menu -> Open -> select 4I1B_clean.pdb</a>

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select epitope, (resi 72+73+74+75+81+83+84+89+90+92+94+96+97+98+115+116+117)<br>
color red, epitope<br>
</a>

Inspect the surface.

<a class="prompt prompt-question">Do the identified residues form a well defined patch on the surface?</a>

The answer to that question should be yes, but we can see some residues not colored that might also be involved in the binding 
(there are some white spots around/in the red surface. 

<details style="background-color:#DAE4E7">
<summary style="bold">
<b><i>See surface view of the epitope identified by NMR</i></b>
 </summary>
 <figure align="center">
  <img width="50%" src="./antigen-epitope.png">
 </figure>
 <br>
</details>
<br>

In HADDOCK we are dealing with potentially uncomplete binding sites by defining surface neighbours as `passive` residues. 
These are added to the definition of the interface but will not lead to any energetic penalty if they are not part of the 
binding site in the final models, while the residues defined as `active` (typically the identified or predicted binding 
site residues) will. When using the HADDOCK server, `passive` residues will be automatically defined. Here since we are 
using a local version, we need to define those manually. 

This can easily be done using a script from our [haddock-tools][haddock-tools] repository, which is also provided for convenience
in the `scripts` directly of the archive you downloaded for this tutorial:

<a class="prompt prompt-cmd">
  python ./scripts/passive_from_active.py 4I1B_clean.pdb  72,73,74,75,81,83,84,89,90,92,94,96,97,98,115,116,117
</a>

The NMR-identified residues and their surface neighbours generated with the above command can be used to define ambiguous interactions restraints, either using the NMR identified residues as active in HADDOCK, or combining those with the surface neighbors and use this combination as passive only.
The corresponding files can be found in the `restraints/antigen-NMR-epitope.act-pass` and `restraints/antigen-NMR-epitope.pass`files. 
Note in the second file the empty first line. The file consists of two lines, with the first one defining the `active` residues and 
the second line the `passive` ones. We will use later these files to generate the ambiguous distance restraints for HADDOCK. 

In general it is better to be too generous rather than too strict in the
definition of passive residues.

And important aspect is to filter both the active (the residues identified from
your mapping experiment) and passive residues by their solvent accessibility.
Our webserver uses a default relative accessibility of 15% as cutoff. This is
not a hard limit. You might consider including even more buried residues if some
important chemical group seems solvent accessible from a visual inspection.


<hr>
### Defining ambiguous restraints for scenario 1


Once you have defined your active and passive residues for both molecules, you
can proceed with the generation of the ambgiuous interaction restraints (AIR) file for HADDOCK. 
For this you can either make use of our online [GenTBL][gentbl] webserver, entering the
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
  ./scripts/active-passive-to-ambig.py ./restraints/antibody-paratope.act-pass ./restraints/antigen-surface.pass > ambig-paratope-surface.tbl
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
`haddock_tbl_validation` that contains a script called `validate_tbl.py` (also provided here in the `scripts` directory. 
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
done using a script from `[haddock-tools][haddock-tools]` repository, which is also provided for convenience
in the `scripts` directly of the archive you downloaded for this tutorial.


<a class="prompt prompt-cmd">
  ./scripts/restrain_bodies.py  4G6K_clean.pdb >antibody-unambig.tbl
</a>

The result file contains two CA-CA distance restraints with the exact distance
measured between the picked CA atoms:

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
we have much more flexibility in doing this.





<hr>
<hr>
## Conclusions

We have demonstrated the antibody-antigen docking guided with and without the knowledge about epitope. Always check and compare multiple clusters, don't blindly trust the cluster with the best HADDOCK score!


<hr>
<hr>
## Congratulations!

You have completed this tutorial. If you have any questions or suggestions, feel free to contact us via email or asking a question through our [support center](https://ask.bioexcel.eu){:target="_blank"}.

And check also our [education](/education) web page where you will find more tutorials!




[air-help]: https://www.bonvinlab.org/software/haddock2.4/generate_air_help/ "AIRs help"
[gentbl]: https://wenmr.science.uu.nl/gentbl/ "GenTBL"
[haddock24protein]: /education/HADDOCK24/HADDOCK24-protein-protein-basic/
[haddock-repo]: https://github.com/haddocking/haddock3 "HADDOCK3 GitHub"
[haddock-tools]: https://github.com/haddocking/haddock-tools "HADDOCK tools GitHub"
[installation]: https://www.bonvinlab.org/haddock3/INSTALL.html "Installation"
[link-forum]: https://ask.bioexcel.eu/c/haddock "HADDOCK Forum"
[link-freesasa]: https://freesasa.github.io "FreeSASA"
[link-pdbtools]:http://www.bonvinlab.org/pdb-tools/ "PDB-Tools"
[link-pymol]: https://www.pymol.org/ "PyMOL"
[nat-pro]: https://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html "Nature protocol"
[tbl-examples]: https://github.com/haddocking/haddock-tools/tree/master/haddock_tbl_validation "tbl examples"
