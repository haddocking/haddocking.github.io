---
layout: page
title: "Basic protein-DNA docking using local version of Haddock3"
excerpt: "A basic tutorial on protein-DNA docking in Haddock3."
tags: [HADDOCK, Haddock3, Pymol, Protein-DNA]
image:
 feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>

## Introduction
This tutorial demonstrates a simplified Haddock3 workflow dedicated to predicting the 3D structure of protein-DNA (double-stranded DNA) complexes using pre-defined restraints, derived from the literature, and symmetry restraints. Here, we introduce the basic concepts of HADDOCK, suitable for tackling various typical protein-DNA docking challenges: 
basic preparation of the input pdb files; 
creation of the suitable Haddock3 workflow; 
basic analysis of the docking results. 
Please note that we do not cover the processing of literature data into docking restraints; for more information, please refer to the advanced tutorial. 

Computation within this tutorial should take 1.5 hours on 8 CPUs. The tutorial data, as well as precomputed results available [here](https://surfdrive.surf.nl/ADD_NEW_DATA todo ).  

This tutorail is an adaptation of the basic protein-DNA docking [tutorial](#todo link) using HADDOCK2.4 webserver. 

This tutorial is an adaptation of Haddock2.4 

#### Tutorial test case
In this tutorial, we will work with the phage 434 Cro/OR1 complex (PDB: [3CRO](https://www.rcsb.org/structure/3CRO)), formed by bacteriophage 434 Cro repressor proteins and the OR1 operator.

Cro is part of the bacteriophage 434 genetic switch, playing a key role in controlling the switch between the lysogenic and lytic cycles of the bacteriophage. It is a *repressor* protein that works in opposition to the phage's repressor cI protein to control the genetic switch. Both repressors compete to gain control over an operator region containing three operators that determine the state of the lytic/lysogenic genetic switch. If Cro prevails, the late genes of the phage will be expressed, resulting in lysis. Conversely, if the cI repressor prevails, the transcription of Cro genes is blocked, and cI repressor synthesis is maintained, resulting in a state of lysogeny.

#### Solved structure of the Cro-OR1 complex
The structure of the phage 434 Cro/OR1 complex was solved by X-RAY crystallography at 2.5Å. We will use this experimentally solved structure as a reference within the tutorial. Cro is a symmetrical dimer, each subunit contains a helix-turn-helix (HTH), with helices α2 and α3 being separated by a short turn. This is a DNA binding motif that is known to bind major grooves. Helix α3 is the recognition helix that fits into the major groove of the operator DNA and is oriented with its axes parallel to the major groove. The side chains of each helix are thus positioned to interact with the edges of base pairs on the floor of the groove. Non-specific interactions also help to anchor Cro to the DNA. These include H-bonds between main chain NH groups and phosphate oxygens of the DNA in the region of the operator. Cro distorts the normal B-form DNA conformation: the OR1 DNA is bent (curved) by Cro, and the middle region of the operator is overwound, as reflected in the reduced distance between phosphate backbones in the minor groove.

<figure align="center">
<img src="/CRO-OR1.png">
</figure>

Throughout the tutorial, coloured text will be used to refer to questions, instructions, PyMOL and terminal prompts:

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This is an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!<a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

It is always possible that you have questions or run into problems for which you cannot find the answer. Here are some additional links that can help you to find the answers and solutions:

* Haddock3 Documentation: [https://www.bonvinlab.org/haddock3/](https://www.bonvinlab.org/haddock3/)
* Bioexcel User Forum: [https://ask.bioexcel.eu/c/haddock/6](https://ask.bioexcel.eu/c/haddock/6)
* Haddock3 Github (issues & discussions): [https://github.com/haddocking/haddock3/](https://github.com/haddocking/haddock3/)
* HADDOCK Help Center: [https://wenmr.science.uu.nl/haddock2.4/help](https://wenmr.science.uu.nl/haddock2.4/help)

<hr>

## Software and data setup
For a complete setup of the local Haddock3 version refer to [Haddock3 Documentation](https://www.bonvinlab.org/haddock3/). Please, familiarise yourself with the sections '**A brief introduction to HADDOCK3**' and '**Installation**'.

In this tutorial we will use the PyMOL molecular visualisation system. If not already installed, download and install PyMOL from [here](https://pymol.org/). You can use your favourite visualisation software instead, but be aware that instructions here are provided only for PyMOL.

Please, download and decompress the tutorial data archive. Move the archive to your working directory of choice and extract it. You can download and unzip this archive directly from the Linux command line:

<a class="prompt prompt-cmd">
wget https://surfdrive.surf.nl/files/index.php/ADD_NEW_LINK -O haddock3-protein-dna-basic.zip<br> todo
unzip haddock3-protein-dna-basic.zip
</a>

Decompressing the file will create the `haddock3-protein-dna-basic` directory with the following subdirectories and items: # todo formatting 
* `workflow`:
 - `protein-dna-basic.cfg`, a Haddock configuration file.
* `pdbs`: <more here, todo>
 - `1ZUG.pdb`, a single structure coming from the NMR ensemble (`1ZUG_ensemble.pdb`) with the terminal disordered residues removed;
 - `OR1_unbound.pdb`, a structure of the OR1 operator in B-DNA conformation;
 - `1ZUG_ensemble.pdb`, an NMR ensemble (10 structures) of the 343 Cro repressor structures;
 - `3CRO_complex.pdb`, an X-RAY structure of the sought-for complex, to be used to evaluate the docking poses.
* `restraints`:
 - `ambig_prot_dna.tbl`, a file containing the ambiguous restraints for this docking scenario.
* `run`, a folder with Haddock3 output, produced by the `protein-dna-basic.cfg` workflow. We will navigate relevant parts of this folder throughout the tutorial.

<hr>

## Understanding the Ambiguous Interaction Restraints

The Ambiguous Interaction Restraints (AIRs) are crucial to successful docking as AIRs should guide docking partners towards the correct conformation. AIRs consist of the residues located in the interface of a complex.

#### Visualisation of the interface
Let's visualise residues in the interface of the 3CRO using PyMOL.
Open `pdbs/3CRO_complex.pdb` in PyMOL and type:
<a class="prompt prompt-pymol">
color lightorange, all
</a>
<a class="prompt prompt-pymol">
select interface, (chain A and resi 28+29+30+31+32+34+35, chain C and resi 28+29+30+31+32+34+35, chain B and resi 4+5+6+7+13+14+15+16+17+18+22+23+24+25+31+32+33+34+35+36)
</a>
<a class="prompt prompt-pymol">
color red, interface
</a>

<details style="background-color:#DAE4E7">
 <summary>
   Now the residues of the interface are displayed in red.<i class="material-icons">expand_more</i>
 </summary>
 <figure style="text-align: center;">
   <img width="50%" src="/CRO-OR1-interface.png">
 </figure>
 <br>
</details>

Let's highlight the same residues on the unbound NRM structure of the protein.
Open PyMOL and type:
<a class="prompt prompt-pymol">
fetch 1ZUG
</a>
<a class="prompt prompt-pymol">
color lightorange, all
</a>
select region, (resi 28+29+30+31+32+34+35)
</a>
<a class="prompt prompt-pymol">
color red, region
</a>
<a class="prompt prompt-pymol">
set all_states, on
</a>

<a class="prompt prompt-question">
How much does the conformation of the interacting region change in the provided ensemble? Is this the most flexible region of the protein?
</a>
<details style="background-color:#DAE4E7">
 <summary style="bold">
   <i>Answer</i> <i class="material-icons">expand_more</i>
 </summary>
 <p>
   The conformation of the interacting region does not change in the ensemble, this region is not the most flexible. The most flexible region is the tail of the protein, and it appears to not interact with the DNA.
 </p>
</details>

Let's switch to the surface representation of a single model:
<a class="prompt prompt-pymol">
set all_states, off
</a>
<a class="prompt prompt-pymol">
show surface
</a>

<details style="background-color:#DAE4E7">
 <summary>
   Surface representation of a single model with interface residues highlighted in red.<i class="material-icons">expand_more</i>
 </summary>
 <figure style="text-align: center;">
   <img width="50%" src="education/HADDOCK3/HADDOCK3-protein-DNA-basic/CRO-interface.png">
 </figure>
 <br>
</details>

<a class="prompt prompt-question">
Can you tell why the residue 33 is excluded from the interface amino acids?
</a>
<details style="background-color:#DAE4E7">
 <summary style="bold">
   <i>Answer</i> <i class="material-icons">expand_more</i>
 </summary>
 <p>
   The residue 33 is not solvent accessible, thus it does not belong to the interface. You can visualise it by colouring residue 33 in blue, and switching between to the cartoon and surface representations (`sele resi 33`, `color blue, sele`, `show cartoon`, `show surface`)
 </p>
</details>

<a class="prompt prompt-info">
Repeat the same analysis with the DNA molecule OR1_unbound.pdb using the residues (13+14+15+16+17+18+22+23+24+25) or (4+5+6+7+31+32+33+34+35+36) as an interface.
</a>

_**Note**_ that in the real docking case the bound structure of a complex is unavailable. In this case, the interface residues could be located using experimental data, knowledge from the literature, using computational predictions, etc.

#### What’s inside of the restraints file?

The ambiguous interaction restraints are defined in the `ambig_prot_dna.tbl` file. This file was created using both experimental knowledge and information from literature. A detailed explanation of how to generate these restraints can be found in the advanced version of the tutorial, [here](link/to/there) todo
Let’s have a look at it's first lines:
```bash
assign ( resid 35 and segid C)
(
( resid 32 and segid B and (name H3 or name O4 or name C4 or name C5 or name C6 or name C7))
or
( resid 33 and segid B and (name H3 or name O4 or name C4 or name C5 or name C6 or name C7))
) 2.000 2.000 0.000
```
The first line means that the residue 35 from the chain C (protein) should interact either with the residue 32, or with the residue 33 of the chain B (DNA). Additionally, the substring `(name H3 or name O4 or name C4 or name C5 or name C6 or name C7)` precise the atoms with which the interaction should occur.

In other words, if at least one pair or residues (residue 35 from chain C; residue 32 from chain B) or (residue 35 from chain C; residue 33 from chain B) are located within 2Å from one another - then this particular restraint is satisfied.

<a class="prompt prompt-question">
Check out the list of atoms defined in `ambig_prot_DNA.tbl`. Which part of the DNA is targeted by defining a given set of atoms? What is the effect of such restraints onto the docking process? 
</a>

You may notice that not all residues of the protein’s interface are used for the AIRs. This is done to save computational time.

HADDOCK is not limited to ambiguous restraints, other types, like unambiguous and symmetry restraints can play an important role as well. As mentioned before, Cro is known to function as a symmetrical dimer. This means we should **enforce a pairwise symmetry (C2)** between the two protein monomers. This part will be explained in the “Haddock3 workflow” section of the tutorial.

## Preparation of pdb files for the docking (optional)

Haddock3 requires an input structure for each docking partner. The quality of these input structures are highly influential to the quality of the docking models. Conformational deficiencies such as clashes, chain breaks and missing atoms may cause problems during the docking, so it is important to verify each input file.
Another important factor is the difference between unbound and bound conformations. The more different these conformations are, the more difficult it is to generate correct docking models.

In this section we will go over the preparation of the protein structures. The preparation of the DNA structure is out of the score of this tutorial and detailed [todo](here).
Note that the ready-to-dock structures are available in `pdbs` directory, namely `1ZUG_dimer1.pdb`, `1ZUG_dimer2.pdb` and `OR1_unbound.pdb`.

#### Protein structures

An unbound structure of the protein is available on [https://www.rcsb.org/structure/1ZUG](PDB). We already examined this structure using PyMOL. Our observation revealed that this protein has a disordered tail, and that this disordered tail does not interact with the DNA. Since the core conformation remains unchanged, we can simply take the first conformation from the ensemble, remove the disordered tail from it and use it as an input structure for the docking. 

This can be done using `pdb-tools`, a collection of simple scripts handy to manipulate pdb files. `pdb-tools` is installed automatically with Haddock3. Alternatively, a web-server is available as a [https://rascar.science.uu.nl/pdbtools/](web-server).

To obtain a single trimmed structure using command-line version of `pdb-tools` (_**remember to activate a virtual environment for Haddock3 first!**_):
<a class="prompt prompt-cmd">
pdb_fetch 1ZUG | pdb_selmodel -1 | pdb_delhetatm | pdb_selres -1:66 | pdb_tidy -strict > 1ZUG_dimer1.pdb
</a>

This sequence of commands: 1/ Downloads given structure in PDB format from the RCSB website; 2/ Extracts the first model from the file; 3/ Removes all HETATM records in the PDB file; 4/ Selects residues by their index (in a range); 5/ Adds TER statement at the end of the chain.

The complex of interest contains 2 copies of the protein. As each molecule given to HADDOCK in a docking scenario must have a **unique chain ID and segment ID**, we have to change chain ID from A to C and save this as a new structure (segment ID remains empty for both cases, which is acceptable):
<a class="prompt prompt-cmd">
pdb_rplchain -A:C 1ZUG_dimer1.pdb > 1ZUG_dimer2.pdb
</a>

_**Note**_ that it is possible to perform the docking with an ensemble of trimmed conformations. Such ensemble can be obtained using the next command: `pdb_fetch 1ZUG | pdb_delhetatm | pdb_selres -1:66 | pdb_tidy -strict > 1zug_ens.pdb`

## Docking with Haddock3

In this section, we will discuss the specifics of protein-DNA docking in the frame of Haddock3. We will then create an appropriate Haddock3 workflow and, finally, perform an analysis of the docking results using the experimentally solved structure as a reference.

#### Specifics of the protein-DNA docking

Docking a double-stranded DNA requires adjusting several default parameters to better mimic the conditions under which DNA interactions occur. The following parameters should be modified:
Add an automatic restraint to maintain the input conformation of the DNA during refinement: `dnarest_on = true`;
Perform explicit solvent molecular dynamics refinement instead of energy minimization refinement by using the `[mdref]` module instead of `[emref]`;
Set the dielectric constant to 78 for both sampling and flexible refinement (but not for MD refinement): `epsilon = 78`;
Fix the relative dielectric constant in the Coulomb potential (rather than using a distance-dependent mode) for both sampling and flexible refinement: `dielec = cdie`;
Set the weight of the desolvation energy term to 0: `w_desolv = 0`;
Lower the scaling factor for flexible refinement to 4 (from 8) to allow less movement during the refinement: `tadfactor = 4`;
Lower the initial temperature for the final round of flexible refinement to 300 (from 1000) to allow less movement during the final refinement stage: `temp_cool3_init = 300`.

_**Note**_ that Haddock3 distinguishes DNA nucleotides from RNA nucleotides based on the residue naming in the PDB file. DNA nucleotides are named with two letters starting with 'D' (e.g., 'DA' for adenine in DNA), while RNA nucleotides use single-letter names (e.g., 'A' for adenine in RNA).

#### Haddock3 workflow

Now that we have all the necessary files ready for docking, along with several insights into the specifics of protein-DNA docking, it’s time to create the docking workflow. In this scenario, we will adhere to the following straightforward workflow: rigid-body docking, semi-flexible refinement, and explicit solvent molecular dynamics (MD) refinement followed by clustering.

Out workflow consists of the following modules:
topoaa: _Generates the topologies for the CNS engine and builds missing atoms_
rigidbody: _Performs sampling by rigid-body energy minimization (equivalent to it0 in Haddock2.x)_
caprieval: _Calculates CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ) with respect to the best-scored model or a provided reference structure_
seletop: _Selects X best-scored models from the previous module_
flexref: _Performs semi-flexible refinement of the interface (equivalent to it1 in Haddock2.x)_ 
caprieval
mdref: _Performs final refinement via explicit solvent MD (equivalent to itw in Haddock2.X)_
caprieval 
rmsdmatrix: _Calculates of the root mean squared deviation (RMSD) matrix between all models from the previous module_
clustrmsd: _Takes the RMSD matrix calculated in the [rmsdmatrix] module and performs a hierarchical clustering procedure on it_
caprieval
seletopclusts: _Selects X best-scored models of Y clusters_

As mentioned before, we should enforce C2 symmetry between the proteins throughout the entire docking process. This can be achieved by adding the following parameters to the `[rigidbody]` , `[flexref]` , and `[mdref]` modules::

```
# Turn on symmetry restraints 
sym_on = true
# Define first symmetry partner 
c2sym_seg1_1 = 'A'
# Define second symmetry partner 
c2sym_seg2_1 = 'C'
# Specify the range of residues that should be taken from the first partner
c2sym_sta1_1 = 4
c2sym_end1_1 = 64
# Specify the range of residues that should be taken from the second partner
c2sym_sta2_1 = 4
c2sym_end2_1 = 64
```

**Note** that in this definition we omitted the first 3 residues of each protein.

Take a look at the tolm configuration file `workflow/protein-dna-basic.cfg`. 
<a class="prompt prompt-info"> Take your time to read the comments and relate parameters of this file to the information given above :</a>

{% highlight toml %}
# ====================================================================
# Protein-DNA basic docking example with:
# 1. Pre-generated ambiguous restraints between protein dimer and DNA partners
# 2. Pairwise (C2) symmetry between the two protein monomers
# ====================================================================

# directory in which the docking will be performed
run_dir = "run1"

# compute mode
mode = "local"
ncores=8

# input pdbs of the docking partners 
molecules =  [
    "pdbs/1ZUG_dimer1.pdb",
    "pdbs/OR1_unbound.pdb"
    "pdbs/1ZUG_dimer2.pdb"
    ]

# ====================================================================
# Workflow is defined as a pipeline of modules with specified parameters per module 
# ====================================================================

[topoaa]

[rigidbody]
# Cro to OR1 ambiguous restraints

ambig_fname = "/restraints/ambig_prot_DNA.tbl"
# C2 symmetry
sym_on = true
c2sym_seg1_1 = 'A'
c2sym_seg2_1 = 'C'
c2sym_sta1_1 = 4
c2sym_sta2_1 = 4
c2sym_end1_1 = 64
c2sym_end2_1 = 64

# constant for the electrostatic energy term
epsilon = 78

# fix constant in Coulomb potential
dielec = 'cdie'

# weight of the desolvation energy term 
w_desolv = 0

[caprieval]
reference_fname = "/pdbs/3CRO_complex.pdb"

[seletop]

[flexref]
# to maintain conformation of the DNA with automatic restraints
dnarest_on = true

# Cro to OR1 ambiguous restraints
ambig_fname = "/trinity/login/arha/tuto/protein-DNA_basic/restraints/ambig_prot_DNA.tbl"

# C2 symmetry
sym_on = true
c2sym_seg1_1 = 'A'
c2sym_seg2_1 = 'C'
c2sym_sta1_1 = 4
c2sym_sta2_1 = 4
c2sym_end1_1 = 64
c2sym_end2_1 = 64

# constant for the electrostatic energy term
epsilon = 78

# fix constant in Coulomb potential
dielec = 'cdie'

# weight of the desolvation energy term 
w_desolv = 0

# allow less movement during the refinement 
tadfactor = 4
temp_cool3_init = 300

[caprieval]
reference_fname = "/pdbs/3CRO_complex.pdb"

[mdref]
# to maintain conformation of the DNA with automatic restraints
dnarest_on = true

# Cro to OR1 ambiguous restraints
ambig_fname = "/trinity/login/arha/tuto/protein-DNA_basic/restraints/ambig_prot_DNA.tbl"

# C2 symmetry
sym_on = true
c2sym_seg1_1 = 'A'
c2sym_seg2_1 = 'C'
c2sym_sta1_1 = 4
c2sym_sta2_1 = 4
c2sym_end1_1 = 64
c2sym_end2_1 = 64

# constant for the electrostatic energy term (default value)
epsilon = 1
w_desolv = 0
# reduce number of MD steps 
watersteps = 750

[caprieval]
reference_fname = "pdbs/3CRO_complex.pdb"

[rmsdmatrix]
# use all residues of each docking partner to calculate RMSD matrix
resdic_A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66]
resdic_B = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
resdic_C = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66]

[clustrmsd]
# generate an interactive plot of the clustering results
plot_matrix = true

[seletopclusts]
[caprieval]
reference_fname = "/pdbs/3CRO_complex.pdb

# ====================================================================

{% endhighlight %}

_**Note**_ that in this example we use relative paths to define input files and output folder. However it is preferable to use the full paths instead. 

This workflow begins by creating topologies for the docking partners. Rigid body sampling is performed with ambiguous and symmetry restraints, generating 1000 models, from which the top 200 are selected. These models then undergo flexible refinement followed by MD refinement in explicit solvent, still maintaining the same ambiguous and symmetry restraints. Finally, docking models are clustered via RMSD, with all residues used to calculate RMSD values. The top 5 models from each cluster are selected. The `caprieval` module is added after each step to simplify model analysis and track the rank of models throughout the docking process.

#### Running Haddock3 locally

In the first section of the configuration file you can see:

{% highlight toml %}
# compute mode
mode = "local"
ncores=8
{% endhighlight %}

The parameter `mode` defines how this workflow will be executed. In this case, it will run locally, on your machine, using 8 CPUs (feel free to change this value). You can find out about other modes [link?](here). #todo

To start the docking you need to **activate your haddock3 environment**, then navigate to the folder with the configuration file `workflow/protein-dna-basic.cfg`, and type:
 type one of the following:
<a class="prompt prompt-cmd">
haddock3 protein-dna-basic.cfg > log-protein-dna-basic.out &
</a>
<a class="prompt prompt-cmd">
haddock3 protein-dna-basic.cfg 
</a>

The first version of this command will run the docking in the background and will save output in the files `log-protein-dna-basic.out`. The second version will run directly in the terminal window and will print output on the screen.
# todo 
This workflow took 1.5 hours to complete using 8 CPUs (. You can run it and wait for the results, or you can access pre-computed results of this protocol immediately by navigating to the `run` directory.

## Analysis of the docking results

Inspect the content of the resulting directory. You will find the various steps of our workflow (modules) numbered sequentially starting at 0:

{% highlight shell %}
> ls run1/
     00_topoaa/
     01_rigidbody/
     02_caprieval/
     03_seletop/
     04_flexref/
     05_caprieval/
     06_mdref/
     07_caprieval/
     08_rmsdmatrix/
     09_clustrmsd/
     10_seletopclusts/
     11_caprieval/
     analysis/
     data/
     log
     traceback/
{% endhighlight %}

There are also:
* `log` file, here you can verify execution of each module, and, more importantly, in case the docking run fails, identify the reason for it by reading carefully the error message. At the very bottom of the file you can see the execution time of this docking run;
* `analysis` directory contains information relevant to the result of each `caprieval` step, including various plots to visualise statistics of the results. Here you can find a general report (`report.html`) of the run. This file can be opened in the web browser;
* `data` directory contains input pdbs (not the actual docking models!) and restraints files used within each  module;
* `traceback` directory contains the `traceback.tsv` file, which displays the name and rank of each docking model throughout the entire workflow. 

Each sampling/refinement/selection module’s directory contains compressed pdb files of the docking models. For example, `10_seletopclusts` contains 10 top-ranked docking models from each of the 14 clusters. The clusters themselves are numbered based on the average rank of the models within, thus `cluster_1` contains top-ranked models of the run. Information about the origin of each model can be found in `10_seletopclusts/seletopclusts.txt`. 

<a class="prompt prompt-info"> Open `analysis/report.html` in a web browser. Inspect displayed on the top of the page table with cluster statistics.
</a>

<a class="prompt prompt-question">
Look at the score of the first few clusters: Are they significantly different if you consider their average scores and standard deviations?
</a>
<details style="background-color:#DAE4E7">
 <summary style="bold">
   <i>Answer</i> <i class="material-icons">expand_more</i>
 </summary>
 <p>
   According to the two-sample t-test, 3 first clusters are significantly different from each other at the 0.05 significance level. #todo
 </p>
</details>

For this docking case we had access to the experimentally solved structure of the complex, and we provided this structure to the caprieval modules. This means that the interface RMSD, ligand RMSD, Fraction of Common Contacts (FCC) and DockQ statistics report on the quality of the docked model compared to the reference structure. Remember here that higher DockQ and FCC values and lower RMSD values correspond to better models. 

<a class="prompt prompt-question">
Look at the DockQ of the clusters: Does the top-ranked cluster has the highest average DockQ?
</a>
<details style="background-color:#DAE4E7">
 <summary style="bold">
   <i>Answer</i> <i class="material-icons">expand_more</i>
 </summary>
 <p>
No, Cluster2 nad Cluster5 have the highest average DockQ value (0.26). Cluster 1 has average DockQ of 0.2. #todo
 </p>
</details>

#### Visualisation of the HADDOCK scores and their components

Under the cluster statistic table, you can see a variety of plost displaying the HADDOCK score and its components against various metrics (i-RMSD, l-RMSD, FCC, Dock-Q) with a color-coded representation of the clusters. Last rows display plots the cluster statistics - distributions of values per cluster ordered according to their HADDOCK rank. 

These plots are interactive. A menu on the top right, just above the right corner of the last plot in the the first row (you have to position your mouth there for this menu to appear) allows you to zoom in and out in the plots and hide/show clusters on the plots.

<a class="prompt prompt-info"> Inspect plots displayed on the top of the page table with cluster statistics. Which of the score components correlates best with the quality of the models?
</a>

Depending on the docking models, there could be a set of unclustered models. Typically it will be shown in `report.html`. You can see origins of these models in `traceback/traceback.tsv`. 

#### Visualisation of the docking models

It’s time to visualise some of the docking models. Let’s visualise cluster_1_model_1.pdb, the best-ranked model, cluster_X_model_Y, the model with the lowest i-RMSD (according to the plot x vs y) and reference structure. Please open all these files in PyMOL. `Cluster_1_model_1.pdb` and `cluster_1_model_1.pdb` can be found in `path, reference structure `3CRO_complex.pdb` in `pdbs`. Then type in the PyMOL command line: 

<a class="prompt prompt-pymol">
show cartoon 
</a>
<a class="prompt prompt-pymol">
 color paleyellow, 3CRO_complex
</a>
<a class="prompt prompt-pymol">
alignto 3CRO_complex
</a>

<a class="prompt prompt-question">
How close there models are to the reference? Did HADDOCK do a good job at ranking docking models?
</a>
<details style="background-color:#DAE4E7">
 <summary style="bold">
   <i>Answer</i> <i class="material-icons">expand_more</i>
 </summary>
 <p>
Models are asseptably close to the reference. While the best model is not top-ranked, HADDOCK produces reasonable ranking. 
 </p>
</details>

It could be helpful to examine several top-ranked models of each cluster. This can give you an idea about the diversity of the models within a cluster, as well as the diversity of models coming from the different clusters. 

<a class="prompt prompt-info"> Compare top-ranked models of the same cluster. Is this cluster well-defined?
</a>

## Congratulations!

You have made it to the end of this basic protein-DNA docking tutorial. We hope it has been illustrative and may help you get started with your own docking projects. Check out [advanced version of this tutorial](#todo) to get more insights on protein-DNA docking! 

Happy docking!


#todo
1. check all todos in text
2. make zip with data + run 
3. Paste correst cfg 
4. Add images to analysis 
5. Add working links (+ link to report.html)
6. Add correct numbers to analysis 

