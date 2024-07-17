---
layout: page
title: "Protein-glycan modelling tutorial using a local version of HADDOCK3"
excerpt: "A tutorial describing the use of HADDOCK3 to model a protein-glycan interaction"
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
the structure of a protein-glycan complex using information about the binding site.

A glycan is a molecule composed of different monosaccharide units, linked to each other
by glycosidic bonds. Glycans are involved in a wide range of biological processes, such as
cell-cell recognition, cell adhesion, and immune response. The glycan structure is highly
diverse and complex, and the prediction of glycan-protein interactions is a challenging
task. In this tutorial, we will use HADDOCK3 to predict the structure of a protein-glycan
complex using information about the binding site on the protein.

In this tutorial we will be working with the catalytic domain of the *Humicola Grisea* Cel12A enzyme
(PDB code [1OLR](https://www.ebi.ac.uk/pdbe/entry/pdb/1olr){:target="_blank"}) and a linear, homo-polymer,
4 beta glucopyranose, as glycan
(PDB code of the complex [1UU6](https://www.ebi.ac.uk/pdbe/entry/pdb/1uu6){:target="_blank"}).

<figure style="text-align: center;">
  <img src="/education/HADDOCK3/HADDOCK3-protein-glycan/1UU6.png">
</figure>

Throughout the tutorial, colored text will be used to refer to questions or
instructions, and/or PyMOL commands.

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

<hr>
<hr>

## Requirements

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

<hr>

## Preparing PDB files for docking

In this section we will prepare the PDB files of the protein and glycan for docking.
A crystal structure of the protein in the unbound form is available, but you are welcome to
use either the bound form or the Alphafold structure if you prefer.

_**Note**_: Before starting to work on the tutorial, make sure to activate haddock3 (follow the workshop-specific instructions above), or, e.g. if installed using `conda`

<a class="prompt prompt-cmd">
conda activate haddock3
</a>

<hr>

### Preparing the protein structure

Using PDB-tools we will download the structure from the PDB database (the PDB ID is [4G6K](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k){:target="_blank"}) and then process it to have a unique chain ID (A) and non-overlapping residue numbering by shifting the residue numbering of the second chain.

This can be done from the command line with:

<a class="prompt prompt-cmd">
pdb_fetch 1OLR | pdb_tidy -strict pdb_delhetatm | pdb_keepcoord | pdb_tidy -strict > 1OLR_ready.pdb
</a>

The command fetches the PDB ID and removes water and heteroatoms (in this case no co-factor is present that should be kept).

_**Note**_ that the corresponding files can be found in the `pdbs` directory of the archive you downloaded.

<hr>

### Preparing the glycan structure

We will model the glycan using the Glycam web server. The glycan is a linear polymer of 4 beta-D-glucopyranose units.
Beta-D-glucopyranose is a common monosaccharide found basically all the living organisms. In this case the four monosaccharides are linked by beta-1,4-glycosidic bonds, where the C1 of one monosaccharide is linked to the C4 of the next one.

<a class="prompt prompt-info">Open the [GLYCAM webserver](https://glycam.org/cb/) to start modelling the glycan!</a>

Unfortunately, the glycan structure we just obtained cannot be directly used in HADDOCK as it's not properly formatted.
We will need to manually edit it to remove the several TER statements GLYCAM placed between the monosaccharides, and to add the [HADDOCK residue name](https://rascar.science.uu.nl/haddock2.4/library) proper to beta-D-glucopyranose.

<a class="prompt prompt-question">What is the HADDOCK three letter code corresponding to beta-D-glucopyranose?</a>

<a class="prompt prompt-info">Open the GLYCAM file and remove all the TER statements</a>

<a class="prompt prompt-info">Substitute every residue name like 0GB and 4GB with BGC</a>

The pre-processed glycan structure can be found in the `pdbs` directory of the archive you downloaded.

Now we would like to know how close the modelled glycan is to the reference structure. For this we will use Pymol to superimpose the two structures and calculate the RMSD.

<a class="prompt prompt-pymol">
File menu -> Open -> select 1UU6_l_u.pdb
</a>

<a class="prompt prompt-pymol">
fetch 1UU6
</a>

<a class="prompt prompt-pymol">
align 1UU6_l_u, 1UU6
</a>

<a class="prompt prompt-question">What is the RMSD between the two glycan structures? In which of the four monosaccharide units the model is better? In which ones is it worse?</a>

## Defining restraints for docking

In this section we will define the restraints that will guide the docking of the protein and glycan structures.

A description of the format for the various restraint types supported by
HADDOCK can be found in our [Nature Protocol][nat-pro]{:target="_blank"} paper, Box 4.
Information about various types of distance restraints in HADDOCK can also be
found in our [online manual][air-help]{:target="_blank"} pages.

* **Binding site on the protein, no knowledge about the glycan**

Here we mimic a scenario where we have information about the glycan binding site on the protein, but no knowledge about which monosaccharide units are relevant for the binding. In this case (see Fig. 1), all the four beta-D-glucopyranose units are at the interface, but this is not true in general, especially when longer glycans are considered.

Let's visualize the interface on our unbound structure.

<a class="prompt prompt-pymol">
File menu -> Open -> select 1OLR_clean.pdb
</a>

The corresponding residues correspond to the protein binding site, as calculated from the crystal structure of the complex:

<pre style="background-color:#DAE4E7">
22,24,59,64,97,103,105,115,120,122,124,131,132,133,134,155,158,205,207
</pre>

<a class="prompt prompt-pymol">
color white, all
</a>
<a class="prompt prompt-pymol">
select binding_site, (resi 22+24+59+64+97+103+105+115+120+122+124+131+132+133+134+155+158+205+207)<br>
</a>
<a class="prompt prompt-pymol">
color red, binding_site
</a>

In order to visualize the binding site of a small molecule we have to add the side chains to our representation.

<a class="prompt prompt-pymol">
show sticks, binding_site
</a>

<hr>

### Defining ambiguous restraints for the protein-glycan docking



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
