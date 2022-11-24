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
and note the location of the extracted PDB files in your system. You should find the following directories and files:

TO BE UPDATED...

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
registration form, and then follow the [installation instructions](https://www.bonvinlab.org/haddock3/INSTALL.html){:target="_blank"}.


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
pdb_fetch 4G6K | pdb_tidy -strict  | pdb_selchain -H | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_tidy -strict > 4G6K_H.pdb<br>
</a>
<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy -strict  | pdb_selchain -L | pdb_delhetatm | pdb_fixinsert | pdb_shiftres -1000 | pdb_keepcoord | pdb_tidy -strict > 4G6K_L.pdb<br>
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

Using PDB-tools we will download the structure from the PDB database (the PDB ID is [4I1B](https://www.ebi.ac.uk/pdbe/entry/pdb/4i1b){:target="_blank"}), remove the hetero atoms and then process it to assign it chainID B.

<a class="prompt prompt-cmd">
pdb_fetch 4I1B | pdb_tidy -strict  | pdb_delhetatm  | pdb_keepcoord | pdb_chain -B | pdb_chainxseg | pdb_tidy -strict >4I1B_clean.pdb
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
8. **`caprieval`**: *Calculates CAPRI metrics (i-RMDS, l-RMSD, Fnat, DockQ) with respect to the top scoring model or reference structure if provided*

The input PDB files are the same for all three scenarios. The differences are in the ambiguous interaction restraint files used and the sampling at the rigid body stage in the case of scenario1.


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
haddock3 docking-Ab-Ag-CDR-surface-node.cfg
{% endhighlight %}
<br>
</details>

<br>
#### 2. HPC/batch mode

In this mode HADDOCK3 will typically be started on your local server (e.g. the login node) and will dispatch jobs to the batch system of your cluster. 
Two batch systems are currently supported: `slurm` and `torque` (defined by the `batch_type` parameter). In the configuration file you will 
have to define the `queue` name and the maximum number of conccurent jobs sent to the queue (`queue_limit`). Since HADDOCK3 single model 
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
cd $HOME/HADDOCK3-antibody-antigen

# execute
haddock3 docking-Ab-Ag-CDR-NMR-epitope-act-mpi.cfg
{% endhighlight %}
<br>
</details>

<hr>
### Scenario 1: Paratope - antigen surface


Now that we have all data ready, and know about execution modes of HADDOCK3 it is time to setup the docking for the first scenario in which we will use the paratope on the antibody to guide the docking, targeting the entire surface of the antibody. The restraint file to use for this is `ambig-paratope-surface.tbl`. We will also define the restraints to keep the two antibody chains together using for this the `antibody-unambig.tbl` restraint file. Further, as we have no information on the antigen side, it is important to increase the sampling in the ridig body sampling stage to 10000. And we will also turn off the default random removal of restraints to keep all the information on the paratote (`randremoval = false`). The configuration file for this scenario (assuming a local running mode, eventually submitted to the batch system requesting a full node) is:

{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the entire surface of the antigen
# ====================================================================

# directory name of the run
run_dir = "scenario1-CDR-surface"

# compute mode
mode = "local"
#  1 nodes x 96 threads
ncores = 96

# molecules to be docked
molecules =  [
    "4G6K_clean.pdb",
    "4I1B_clean.pdb"
    ]

# ====================================================================
# Parameters for the various stages
# ====================================================================
[topoaa]

[rigidbody]
# CDR to surface ambig restraints
ambig_fname = "ambig-CDR-surface.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "unambig.tbl"
# Turn off ramdom removal of restraints
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
reference_fname = "4G6M_matched.pdb"

[flexref]
# Acceptable percentage of model failures
tolerance = 5
# CDR to surface ambig restraints
ambig_fname = "ambig-CDR-surface.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "unambig.tbl"
# Turn off ramdom removal of restraints
randremoval = false

[emref]
# CDR to surface ambig restraints
ambig_fname = "ambig-CDR-surface.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "unambig.tbl"
# Turn off ramdom removal of restraints
randremoval = false

[clustfcc]

[seletopclusts]
top_cluster = 500

[caprieval]
reference_fname = "4G6M_matched.pdb"

# ====================================================================
{% endhighlight %}

This configuration file can be found [here](./haddock3/docking-Ab-Ag-CDR-surface-node.cfg) and is also provided 
in the `haddock3` directory of the downloaded data set for this tutorial as `docking-Ab-Ag-CDR-surface-node.cfg`. 
An MPI version is also available as `docking-Ab-Ag-CDR-surface-mpi.cfg`.


<a class="prompt prompt-question">
Compared to the workflow described above (Setting up the docking with HADDOCK3), 
this example has one additional step. Can you identify which one?
</a>

If you have everything ready, you can launch haddock3 either from the command line, or, better, 
submitting it to the batch system requesting in this local run mode a full node (see local execution mode above).

_**Note**_ that this scenario is computationally more expensive because of the increased sampling. 
On our own cluster, running in MPI mode with 250 cores on AMD EPYC 7451 processors the run completed in 1h23min. 
The same run on a single node using all 96 threads took on the same architecture 4 hours and 8 minutes.


<hr>
### Scenario 2a: Paratope - NMR-epitope as passive


In scenario 2a we are settinp up the docking in which the paratope on the antibody is used to guide the docking, targeting the NMR-identied epitope (+surface neighbors) defined as passive residues. The restraint file to use for this is `ambig-CDR-NMR-epitope-pass.tbl`. As for scenario1, we will also define the restraints to keep the two antibody chains together using for this the `antibody-unambig.tbl` restraint file. In this case since we have information for both interfaces default sampling parameters are sufficient. And we will also turn off the default random removal of restraints to keep all the information on the paratote (`randremoval = false`). The configuration file for this scenario (assuming a local running mode, eventually submitted to the batch system requesting a full node) is:

{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen (as passive)
# ====================================================================

# directory name of the run
run_dir = "run1-mpi-CDR-NMR-epitope-pass"

# MPI compute mode
mode = "local"
#  1 nodes x 96 threads
ncores = 96

# molecules to be docked
molecules =  [
    "4G6K_clean.pdb",
    "4I1B_clean.pdb"
    ]

# ====================================================================
# Parameters for each stage are defined below, prefer full paths
# ====================================================================
[topoaa]

[rigidbody]
# CDR to surface ambig restraints
ambig_fname = "ambig-CDR-NMR-epitope-pass.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "unambig.tbl"
# Turn off ramdom removal of restraints
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
reference_fname = "4G6M_matched.pdb"

[flexref]
# Acceptable percentage of model failures
tolerance = 5
# CDR to surface ambig restraints
ambig_fname = "ambig-CDR-NMR-epitope-pass.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "unambig.tbl"
# Turn off ramdom removal of restraints
randremoval = false

[emref]
# CDR to surface ambig restraints
ambig_fname = "ambig-CDR-NMR-epitope-pass.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "unambig.tbl"
# Turn off ramdom removal of restraints
randremoval = false

[clustfcc]

[seletopclusts]
top_cluster = 500

[caprieval]
reference_fname = "4G6M_matched.pdb"

# ====================================================================
{% endhighlight %}

This configuration file can be found [here](./haddock3/docking-Ab-Ag-CDR-NMR-epitope-pass-node.cfg) and is also provided in the `haddock3` directory of the downloaded data set for this tutorial as `docking-Ab-Ag-CDR-NMR-epitope-pass-node.cfg`. An MPI version is also available as `docking-Ab-Ag-CDR-NMR-epitope-pass-mpi.cfg`.


If you have everything ready, you can launch haddock3 either from the command line, or, better, submitting it to the batch system requesting in this local run mode a full node (see local execution mode above).

_**Note**_ that this scenario is less expensive since we keep the default sampling parameters. On our own cluster, running in MPI mode with 250 cores on AMD EPYC 7451 processors the run completed in about 7 minutes. The same run on a single node using all 96 threads took on the same architecture about 21 minutes. In HPC/batch mode, using 100 queue slots and 10 models per job, the same run completed in about 45 minutes.


<hr>
### Scenario 2b: Paratope - NMR-epitope as active


Scenario 2b is rather similar to scenario 2a with the difference that the NMR-identified epitope is treated as active, meaning restraints will be defined from it to "force" it to be at the interface.
And since there might be more false positive data in the identified interfaces, we will leave the random removal of restraints on. The restraint file to use for this is `ambig-CDR-NMR-epitope-act.tbl`. As for scenario1, we will also define the restraints to keep the two antibody chains together using for this the `antibody-unambig.tbl` restraint file. In this case since we have information for both interfaces default sampling parameters are sufficient. The configuration file for this scenario (assuming a local running mode, eventually submitted to the batch system requesting a full node) is:

{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen (as active)
# and keeping the random removal of restraints
# ====================================================================

# directory name of the run
run_dir = "run1-node-CDR-NMR-epitope-act"

# compute mode
mode = "local"
#  1 nodes x 96 cores
ncores = 96

# molecules to be docked
molecules =  [
    "4G6K_clean.pdb",
    "4I1B_clean.pdb"
    ]

# ====================================================================
# Parameters for each stage are defined below, prefer full paths
# ====================================================================
[topoaa]

[rigidbody]
# CDR to surface ambig restraints
ambig_fname = "ambig-CDR-NMR-epitope-act.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "unambig.tbl"

[clustfcc]
threshold = 10

[seletopclusts]
## select all the clusters
top_cluster = 500
## select the best 10 models of each cluster
top_models = 10

[caprieval]
# this is only for this tutorial to check the performance at the rigidbody stage
reference_fname = "4G6M_matched.pdb"

[flexref]
# Acceptable percentage of model failures
tolerance = 5
# CDR to surface ambig restraints
ambig_fname = "ambig-CDR-NMR-epitope-act.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "unambig.tbl"

[emref]
# CDR to surface ambig restraints
ambig_fname = "ambig-CDR-NMR-epitope-act.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "unambig.tbl"

[clustfcc]

[seletopclusts]
top_cluster = 500

[caprieval]
reference_fname = "4G6M_matched.pdb"

# ====================================================================

{% endhighlight %}

This configuration file can be found [here](./haddock3/docking-Ab-Ag-CDR-NMR-epitope-act-node.cfg) and is also provided in the `haddock3` directory of the downloaded data set for this tutorial as `docking-Ab-Ag-CDR-NMR-epitope-act-node.cfg`. An MPI version is also available as `docking-Ab-Ag-CDR-NMR-epitope-act-mpi.cfg`.


If you have everything ready, you can launch haddock3 either from the command line, or, better, submitting it to the batch system requesting in this local run mode a full node (see local execution mode above).

_**Note**_ The running time for this scenario is similar to that of scenario 2a (see above).


<hr>
<hr>
## Analysis of docking results


### Structure of the run directory

Once your run has completed inspect the content of the resulting directory. You will find the various steps (modules) of the defined workflow numbered sequentially, e.g.:

{% highlight shelll %}
> ls scenario2a-CDR-NMR-epitope-pass/
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

For example, the `X_seletopclusts` directory contains the selected models from each cluster. Information about the origin of these files can be found in that directory in the `seletopclusts.txt` file.

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
* **dockq**: *the DockQ score, which is a combination of irmsd, lrmsd and fnat and provides a continuous scale betweeen 1 (equal to reference) and 0*

The iRMSD, lRMSD and Fnat metrics are the ones used in the blind protein-protein prediction experiment [CAPRI](https://capri.ebi.ac.uk/) (Critical PRediction of Interactions).

In CAPRI the quality of a model is defined as (for protein-protein complexes):

* **acceptable model**: i-RMSD < 4Å or l-RMSD<10Å and Fnat > 0.1 
* **medium quality model**: i-RMSD < 2Å or l-RMSD<5Å and Fnat > 0.3
* **high quality model**: i-RMSD < 1Å or l-RMSD<1Å and Fnat > 0.5

<a class="prompt prompt-question">
What is based on this CAPRI criterion the quality of the best model listed above (emref_19.pdb)?
</a>

In case the `caprieval` module is called after a clustering step an additional file will be present in the directory: `capri_clt.tsv`.
This file contains the cluster ranking and score statistics, averaged over the minimumber number of models defined for clustering 
(4 by default), with their corresponding standard deviations. E.g.:

<pre style="background-color:#DAE4E7">
cluster_rank    cluster_id      n       under_eval      score   score_std       irmsd   irmsd_std       fnat    fnat_std        lrmsd   lrmsd_std       dockq   dockq_std             caprieval_rank
1       6       10      -       -137.815        5.725   1.192   0.126   0.797   0.051   2.581   0.713   0.774   0.044   1
2       2       16      -       -109.687        4.310   14.951  0.044   0.069   0.000   22.895  0.030   0.067   0.000   2
3       8       4       -       -105.095        13.247  14.909  0.119   0.069   0.000   23.066  0.336   0.066   0.001   3
4       5       10      -       -100.189        4.222   5.148   0.024   0.130   0.015   10.476  0.586   0.202   0.014   4
...
</pre>

In this file you find the cluster rank, the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (n) in the cluster and the corresponding statistics (averages + standard deviations). The corresponding cluster PDB files will be found in the precessind `X_seletopclusts` directory.


<hr>
### Analysis scenario 1: Paratope - antigen surface


<hr>
### Analysis scenario 2a: Paratope - NMR-epitope as passive


Let us now analyse the docking results for this scenario. Use for that either your own run or a pre-calculated run provided in the `runs` directory (note that to save space on partial data have been kept in this pre-calculated runs, but all relevant information is available).

First of all let us check the final cluster statistics. 

<a class="prompt prompt-info">Inspect the _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
<summary>
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

<a class="prompt prompt-question">How many clusters or acceptable or better quality have been generate according to CAPRI criteria?</a>

<a class="prompt prompt-question">What is the rank of the best cluster generated?</a>

<a class="prompt prompt-question">What is the rank of the first acceptable of better cluster generated?</a>



In this run we also had a `caprieval` after the clustering of the rigid body models (step 4 of our workflow). 

<a class="prompt prompt-info">Inspect the corresponding _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
<summary>
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
<summary>
<i>Answer:</i>
 </summary>
<p> After rigid body docking the first acceptable cluster is at rank 2. After refinement it scores at the top with score significantly better than the second-ranked cluster.
</p>
</details>
<br>

<a class="prompt prompt-question">Did the rank improve after refinement?</a>


We are providing in the `scripts` a simple script that extract some cluster statistics for acceptable or better clusters from the `caprieval` steps.
To use is simply call the script with as argument the run directory you want to analyse, e.g.:

<a class="prompt prompt-cmd">
   ./scripts/extract-capri-stats-clt.sh ./runs/scenario2a-CDR-NMR-epitope-pass
</a>


<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script:</i>
 </summary>
<pre>
==============================================
== scenario2a-CDR-NMR-epitope-pass//4_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  1  out of  9
Total number of medium or better clusters:      1  out of  9
Total number of high quality clusters:          0  out of  9

First acceptable cluster - rank:  2  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
First medium cluster     - rank:  2  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
Best cluster             - rank:  2  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
==============================================
== scenario2a-CDR-NMR-epitope-pass//9_caprieval/capri_clt.tsv
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
   ./scripts/extract-capri-stats.sh ./runs/scenario2a-CDR-NMR-epitope-pass
</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script:</i>
 </summary>
<pre>
==============================================
== scenario2a-CDR-NMR-epitope-pass//4_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  10  out of  90
Total number of medium or better models:      10  out of  90
Total number of high quality models:          2  out of  90

First acceptable model - rank:  11  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
First medium model     - rank:  11  i-RMSD:  1.247  Fnat:  0.690  DockQ:  0.741
Best model             - rank:  18  i-RMSD:  0.980  Fnat:  0.586  DockQ:  0.739
==============================================
== scenario2a-CDR-NMR-epitope-pass//9_caprieval/capri_ss.tsv
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
<summary>
<i>Answer:</i>
 </summary>
<p> In terms of iRMSD values we only observe very small differences with a slight increase. 
The fraction of native contacts and the DockQ scores are however improving much more after flexible refinement.
All this will of course depend on how different are the bound and unbound conformations and the amount of data 
used to drive the docking process. In general, from our experience, the more and better data at hand, 
the larger the conformational changes that can be induced.
</p>
</details>
<br>

<a class="prompt prompt-question">Is the best model always rank as first?</a>

<details style="background-color:#DAE4E7">
<summary>
<i>Answer:</i>
 </summary>
<p> This is clearly not the case. The scoring function is not perfect, but does a reasonable job in ranking models of acceptable or better quality on top in this case.</p>
</details>
<br>


<hr>
### Analysis scenario 2b: Paratope - NMR-epitope as active


Let us now analyse the docking results for this scenario. Use for that either your own run or a pre-calculated run provided in the `runs` directory (note that to save space on partial data have been kept in this pre-calculated runs, but all relevant information is available).

First of all let us check the final cluster statistics. 

<a class="prompt prompt-info">Inspect the _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
<summary>
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

<a class="prompt prompt-question">How many clusters or acceptable or better quality have been generate according to CAPRI criteria?</a>

<a class="prompt prompt-question">What is the rank of the best cluster generated?</a>

<a class="prompt prompt-question">What is the rank of the first acceptable of better cluster generated?</a>


In this run we also had a `caprieval` after the clustering of the rigid body models (step 4 of our workflow). 

<a class="prompt prompt-info">Inspect the corresponding _capri_clt.tsv_ file</a>

<details style="background-color:#DAE4E7">
<summary>
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
<summary>
<i>Answer:</i>
 </summary>
<p> After rigid body docking the first acceptable cluster is at rank 1 and the same is true after refinement, but the iRMSD values have improved.</p>
</details>
<br>


Use the `extract-capri-stats-clt.sh` script to extract some simple cluster statistics for this run.

<a class="prompt prompt-cmd">
   ./scripts/extract-capri-stats-clt.sh ./runs/scenario2b-CDR-NMR-epitope-pass
</a>


<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script:</i>
 </summary>
<pre>
==============================================
== scenario2b-CDR-NMR-epitope-act//4_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  4  out of  14
Total number of medium or better clusters:      1  out of  14
Total number of high quality clusters:          0  out of  14

First acceptable cluster - rank:  1  i-RMSD:  2.514  Fnat:  0.332  DockQ:  0.437
First medium cluster     - rank:  3  i-RMSD:  1.083  Fnat:  0.733  DockQ:  0.766
Best cluster             - rank:  3  i-RMSD:  1.083  Fnat:  0.733  DockQ:  0.766
==============================================
== scenario2b-CDR-NMR-epitope-act//9_caprieval/capri_clt.tsv
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
   ./scripts/extract-capri-stats.sh ./runs/scenario2b-CDR-NMR-epitope-pass
</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script:</i>
 </summary>
<pre>
==============================================
== scenario2b-CDR-NMR-epitope-act//4_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  36  out of  140
Total number of medium or better models:      10  out of  140
Total number of high quality models:          1  out of  140

First acceptable model - rank:  2  i-RMSD:  2.533  Fnat:  0.328  DockQ:  0.434
First medium model     - rank:  13  i-RMSD:  1.152  Fnat:  0.810  DockQ:  0.794
Best model             - rank:  15  i-RMSD:  0.982  Fnat:  0.776  DockQ:  0.803
==============================================
== scenario2b-CDR-NMR-epitope-act//9_caprieval/capri_ss.tsv
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
<summary>
<i>Answer:</i>
 </summary>
<p> In this case we observe a small improvement in terms of iRMSD values and quite some large improvement in 
the fraction of native contacts and the DockQ scores. Also the single model rankings have improved, but the top ranked model is not the best one.
</p>
</details>
<br>

<a class="prompt prompt-question">Is the best model always rank as first?</a>

<details style="background-color:#DAE4E7">
<summary>
<i>Answer:</i>
 </summary>
<p> This is clearly not the case. The scoring function is not perfect, but does a reasonable job in ranking models of acceptable or better quality on top in this case.</p>
</details>
<br>


<hr>
### Comparing the performance of the three scenarios



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
