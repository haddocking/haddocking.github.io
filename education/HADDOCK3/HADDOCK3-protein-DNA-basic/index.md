---
layout: page
title: "Basic protein-DNA docking using local version of HADDOCK3"
excerpt: "A basic tutorial on protein-DNA docking in HADDOCK3."
tags: [HADDOCK, Pymol, Protein-DNA]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>

## Introduction
This tutorial demonstrates a simplified Haddock3 workflow dedicated to predicting the 3D structure of protein-DNA complexes using data from the literature and symmetry restraints. Here, we introduce the basic concepts of HADDOCK, suitable for tackling various typical protein-DNA docking challenges. We do not cover the processing of literature data into docking restraints; for more information, please refer to the advanced tutorial.

Computation within this tutorial should take X hours on 8 CPUs. The tutorial data, as well as precomputed resuts awaliable [here](https://surfdrive.surf.nl/ADD_NEW_DATA todo ). 

### Tutorial test case 
In this tutorial, we will work with the phage 434 Cro/OR1 complex (PDB: [3CRO](https://www.rcsb.org/structure/3CRO)), formed by bacteriophage 434 Cro repressor proteins and the OR1 operator.

Cro is part of the bacteriophage 434 genetic switch, playing a key role in controlling the switch between the lysogenic and lytic cycles of the bacteriophage. It is a *repressor* protein that works in opposition to the phage's repressor cI protein to control the genetic switch. Both repressors compete to gain control over an operator region containing three operators that determine the state of the lytic/lysogenic genetic switch. If Cro prevails, the late genes of the phage will be expressed, resulting in lysis. Conversely, if the cI repressor prevails, the transcription of Cro genes is blocked, and cI repressor synthesis is maintained, resulting in a state of lysogeny.

#### Solved structure of the Cro-OR1 complex
The structure of the phage 434 Cro/OR1 complex was solved by X-RAY crystallography at 2.5Å. We will use this experimentally solved structure as a reference within the tutorial. Cro is a symmetrical dimer, each subunit contains a helix-turn-helix (HTH), with helices α2 and α3 being separated by a short turn. This is a DNA binding motif that is known to bind major grooves. Helix α3 is the recognition helix that fits into the major groove of the operator DNA and is oriented with its axes parallel to the major groove. The side chains of each helix are thus positioned to interact with the edges of base pairs on the floor of the groove. Non-specific interactions also help to anchor Cro to the DNA. These include H-bonds between main chain NH groups and phosphate oxygens of the DNA in the region of the operator. Cro distorts the normal B-form DNA conformation: the OR1 DNA is bent (curved) by Cro, and the middle region of the operator is overwound, as reflected in the reduced distance between phosphate backbones in the minor groove.

<figure align="center">
<img src="/education/HADDOCK3/HADDOCK3-protein-DNA-basic/CRO-OR1.png">
</figure>

Throughout the tutorial, colored text will be used to refer to questions, instructions, PyMOL and terminal prompts:

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!<a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

It is always possible that you have questions or run into problems for which you cannot find the answer in the regular documentation. Here are some additional links that you can find answers to your questions:

* Haddock3 Documentation: [https://www.bonvinlab.org/haddock3/](https://www.bonvinlab.org/haddock3/)
* Bioexcel User Forum: [https://ask.bioexcel.eu/c/haddock/6](https://ask.bioexcel.eu/c/haddock/6)
* Haddock3 Github (issues & disuccions): [https://github.com/haddocking/haddock3/](https://github.com/haddocking/haddock3/)
* HADDOCK Help Center: [https://wenmr.science.uu.nl/haddock2.4/help](https://wenmr.science.uu.nl/haddock2.4/help) 

<hr>

## Software and data setup
For a compete set up of local Haddock3 version refer to [Haddock3 Documentation](https://www.bonvinlab.org/haddock3/). Please, familirize yourself with the sections 'A brief introduction to HADDOCK3' and 'Installation'. 

In this tutorial we will use PyMOL molecular visualisation system. If not already installed, download and install PyMOL from [here](https://pymol.org/). You can use your favorite visulation software instead, but be aware that instructions here are provided only for PyMOL.

Please, download and decompress the tutorial data archive. Move the archive to your working directory of choice and extract it. You can download and unzip this archive directly from the Linux command line:

<a class="prompt prompt-cmd">
wget https://surfdrive.surf.nl/files/index.php/ADD_NEW_LINK -O haddock3-protein-dna-basic.zip<br> todo
unzip haddock3-protein-dna-basic.zip
</a>

Decompressing the file will create the `haddock3-protein-dna-basic` directory with the following subdirectories and items:
* `pdbs`: <more here, todo>
  - `1ZUG.pdb`, a single structure coming from the NMR ensemble (`1ZUG_ensemble.pdb`) with the terminal disordered residues removed;
  - `OR1_unbound.pdb`, a structure of the OR1 operator in B-DNA conformation;
  - `1ZUG_ensemble.pdb`, an NMR ensemble (10 structures) of the 343 Cro repressor structures;
  - `3CRO_complex.pdb`, an X-RAY structure of the sought-for complex, to be used to evaluate the docking poses.
* `restraints`:
  - `ambig_pm.tbl`, a file containing the ambiguous restrains for this docking senario. This file was created using both experimental knowledge and information from literature. A detailed explanation of how to generate these restraints can be found [here](link/to/there) todo
* `workflow`:
  - `protein-dna-basic.cfg`, a Hadddokc3 workflow file.
* `run`, a folder with Haddock3 output, produced by the `protein-dna-basic.cfg` workflow. We will navigate relevant parts of this folder throughtout the tutorial. 

<hr>

## Understanding the Ambiguous Irteraction Restraints 

The Ambiguous Irteraction Restraints (AIRs) are crusial to sucessful docking as AIRs should guide docking partners towards each other in the correct conformation. AIRs consist of the residues located in the interface of a complex. 

#### Visualisation 
Let's visualise residues in the interface of the 3CRO complex using PyMOL. 
Open `pdbs/3CRO_complex.pdb` in PyMOL and type:
<a class="prompt prompt-pymol">
color white, all
</a>
<a class="prompt prompt-pymol">
select interface, (chain A and resi 28+29+30+31+32+34+35, chain C and resi 28+29+30+31+32+34+35, chain B and resi 4+5+6+7+13+14+15+16+17+18+22+23+24+25+32+33+34+35+36)
</a>
<a class="prompt prompt-pymol">
color red, interface
</a>
Now the residues of the interface are displayed in red. 

Let's highlight the same residues on the unbound NRM structure of the protein. 
Open PyMOL and type:
<a class="prompt prompt-pymol">
fetch 1ZUG
</a>
<a class="prompt prompt-pymol">
color white, all
</a>
select region, (resi 28+29+30+31+32+34+35)
</a>
<a class="prompt prompt-pymol">
color red, region
</a>

<a class="prompt prompt-question">
How much does the conformation of the interacting region change in the provided ensemble? Is this the most flexible region of the protein?
</a>
<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
    The conformation of the interacting region does not change in the ensamle, this region is not the most flexible. The most flexible region is the tail of the protein, it appears to not interact with the DNA.
  </p>
</details>

Let's swithch to the surface representation:
<a class="prompt prompt-pymol">
show surface
</a>

<a class="prompt prompt-question">
Can you tell why the residue 33 is excluded from the interface amino acids?
</a>
<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
    The residue 33 is not solvent accessible, thus it does not belong to the interface.
  </p>
</details>

<a class="prompt prompt-info">
Repeat the same analysis with the DNA molecule OR1_unbound.pdb using the residues (13+14+15+16+17+18+22+23+24+25) or (4+5+6+7+32+33+34+35+36) as an interface.
</a>

_**Note**_ that in the real docking case bound strcuture of a complex is unawaliable. The interface residues could be  located using experimental data, knowledge from the literature etc.

#### Restraints file 

The ambiguous interaction restraints are defined in the `ambig_prot_DNA.tbl` file. Let’s have a look at it's first lines:
```bash
assign ( resid 35 and segid C)
(
( resid 32 and segid B and (name H3 or name O4 or name C4 or name C5 or name C6 or name C7))
or
( resid 33 and segid B and (name H3 or name O4 or name C4 or name C5 or name C6 or name C7))
) 2.000 2.000 0.000
```
The first line meaning that the residue 35 from the cahin C (protein) should interact either with the residue 32, or with the residue 33 of the cahin B (DNA). Additionally, the subline `(name H3 or name O4 or name C4 or name C5 or name C6 or name C7)` presices the atoms with which the initeraction should occur. 

If at least one pair (residue 35 from chain C; residue 32 from chain B) or (residue 35 from chain C; residue 33 from chain B) are located within 2Å from one another - then this particuar restraint is satisfied.

<a class="prompt prompt-question">
Check out the list of atoms defined in `ambig_prot_DNA.tbl`. What is their effect on the restraint? <- #todo Which part of the DNA is targeted by defining given set of atoms?
</a>

## Preparing PDB files for docking (optional)

Haddock3 requires an input structure for each docking partner. The quality of these input structures are highly influential to the quality of the docking models. Conformational deficiencies such as clashes, chain breaks and missing atoms may cause problems during the docking, so it is important to verifiy each input file. 
Another important factor is the difference between unbound and bound conformations. The more different these conformations are the more difficult it is to generate correct docking models. 

In this section we will go over the preparation of the protein strcutures. The preparation of the DNA strcuture is out of the score of this tutorial and detailed [todo](here).
Note that the ready-to-dock structures are avaliable in `pdbs`, namely `1ZUG_dimer1.pdb`, `1ZUG_dimer2.pdb` and `OR1_unbound.pdb`.

#### Protein structures

An unbound structutre of the protein is avaliable on [https://www.rcsb.org/structure/1ZUG](PDB). We already examined this structutre using PyMOL. Our observation revealed that this protein has a disordered tail, and that this disordered tail does not interact with the DNA. Since the core conformation remains unchanged, we can simply take the first conformation from the ensemble and remove the disordered tail from it.

This can be done using `pdb-tools`, a collection of simple scripts hadny to manipulate pdb files. `pdb-tools` is installed automatically with Haddock3. Alternatively, a web-server is avaliable as a [https://rascar.science.uu.nl/pdbtools/](web-server).

To obtain a singe trimmed structure using command-line version of `pdb-tools` (_**remember to activate a virtual environment for Haddock3 first!**_):
<a class="prompt prompt-cmd">
pdb_fetch 1ZUG | pdb_selmodel -1 | pdb_delhetatm | pdb_selres -1:66 | pdb_tidy -strict > 1ZUG_dimer1.pdb
</a>

This sequence of commands: 1/ Downloads given structure in PDB format from the RCSB website; 2/ Extracts the first model from the file; 3/ Removes all HETATM records in the PDB file; 4/ Selects residues by their index (in a range); 5/ Adds TER statement at the end of the cahin.

The complex of interest contains 2 copies of the protein. As each molecule given to HADDOCK in a docking scenario must have a unique chain ID and segment ID, we have to change chain ID from A to C and save this as a new strcuture:
<a class="prompt prompt-cmd">
pdb_rplchain -A:C 1ZUG_dimer1.pdb > 1ZUG_dimer2.pdb
</a>

_**Note**_ that it is possible to perform the docking with an enamble of trimmed conformations. Such ensembe can be obtained using the next command: `pdb_fetch 1ZUG | pdb_delhetatm | pdb_selres -1:66 | pdb_tidy -strict > 1zug_ens.pdb`

## Docking with Haddock3 

#### Specificity of the protien-DNA docking 
 
+ epsilon 
+ w_desolv 
+ dnarest_on
+ dielec
+ tadfactor = 4
+ temp_cool3_init = 300

#### Haddock3 workflow 
module-by-module + brief explain what each module doing. 
+ symmetry 
#### Running Haddock3

Here show just local mode.

## Analysis of the docking results 

+ navigation around I guess... 
+ explain capri_ss and capri_csv

+ compare with reference 
+ ? Visualizing the scores and their components 
#### Visualisation of the docking models

## Congratulations!

You have made it to the end of this basic protein-DNA docking tutorial. We hope it has been illustrative and may help you get started with your own docking projects.

Happy docking!

