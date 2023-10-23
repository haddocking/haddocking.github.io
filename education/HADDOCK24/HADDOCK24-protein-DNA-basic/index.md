---
layout: page
title: "Protein-DNA docking Using HADDOCK High-Ambiguity Driven DOCKing"
excerpt: "A basic tutorial on protein-DNA docking in HADDOCK2.4."
tags: [HADDOCK, Pymol, Protein-DNA]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>

## Introduction

Structures of protein-DNA complexes fulfill a key role in our understanding of the complex regulatory mechanisms in the living cell.
With the ever-increasing number of putative DNA-interacting proteins, there is a need for high-throughput structural biology pipelines.

However, not all biomolecular complexes are that straightforward to solve using experimental methods such as X-ray crystallography and Nucleic Magnetic Resonance (NMR) spectroscopy.
Indeed, complexes that engage in transient interactions are, by definition, highly dynamic during interaction, while too big ones remain still a challenge for structural experimental techniques.

Computational methods for the calculation of structural models at atomic resolution have proven to be a valid toolset to help overcome some of these experimental limitations.
Especially docking algorithms are becoming increasingly popular. These algorithms aim to solve the structure of a complex from its native constituents using various computational approaches.
While very performant for protein-protein interactions, many of these algorithms suffer limitations when trying to model protein-DNA complexes such as the location of the interaction interfaces and dealing with conformational change upon complex formation.

This tutorial will introduce HADDOCK (High Ambiguity Driven DOCKing) [1] as a method to overcome some of the limitations associated with protein-DNA docking.

<hr>

## About this tutorial

In this tutorial, we aim to introduce you to basic concepts of protein-DNA docking using HADDOCK2.4 webserver.
For a complete protein-DNA docking using HADDOCK 2.4, including the generation of Ambiguous Interaction Restraints (AIRs) and starting structures, visit [the advanced tutorial on protein-DNA docking](https://www.bonvinlab.org/education/HADDOCK24/HADDOCK24-protein-DNA-advanced/).

### What is new in this tutorial?

You will perform a docking of a protein-DNA system composed of 3 biomolecules (2 proteins and 1 DNA).
All of these molecules are in their unbound conformation.

* Introduction on the use of symmetry restraints. 
* Special considerations for the use of flexibility in protein-DNA systems.

### Using this tutorial

You should be able to go through this tutorial in about 1 hours.
Basic knowledge on the principles and use of Linux command lines and HADDOCK is useful but not required.
We will be using the HADDOCK 2.4 webserver [https://wenmr.science.uu.nl/haddock2.4/](https://wenmr.science.uu.nl/haddock2.4/) to perform the docking.

### Tutorial data set

In this tutorial you will perform a protein-DNA docking using the bacteriophage 434 Cro repressor protein and the OR1 operator as an example case.
All the tutorial data are made available as a tar.gz archive and can be downloaded at the following [address](https://surfdrive.surf.nl/files/index.php/s/FFHdJqlUYwnihzR/download).

### Extract the archive

You need to decompress the tutorial data archive.
Move the archive to your working directory of choice and extract it.
You can either extract the archive by just selecting “extract” option.

Extract the archive in the current working directory:

<a class="prompt prompt-cmd">
tar -xvf protein-DNA_basic.tgz
</a>

Extraction of the archive will present you with a new directory called `protein-DNA_basic` that contains a number of files and directories:
* the prepared structure of the 343 Cro repressor structure (`1ZUG_ensemble.pdb`)
* the structure of the OR1 operator in B-DNA conformation (`OR1_unbound.pdb`)
* the ambiguous restrains (`ambig_pm.tbl`) extracted from the reference complex
* the X-ray structure of the complex `3CRO_complex.pdb` used as reference to compare with the docking results
* the `Pre-computed-example` directory holds a sample of the results obtained by doing this tutorial.
* the `Analysis` directory holds various scripts and tools used in the **bonus** section at the end of this tutorial.

To obtain more detailed information about how to obtain these files, please refer to the [advanced tutorial on protein-DNA docking](https://www.bonvinlab.org/education/HADDOCK24/HADDOCK24-protein-DNA-advanced/).

### Where can I find more information?

An elaborate discussion of all the concepts of protein-DNA docking and the various options of the HADDOCK docking software is beyond the scope of this tutorial.
Where needed, some concepts will be explained throughout the tutorial to maintain the readability and flow of this document.
The tutorial ends with a reference block that provides links to in depth literature or Internet documentation about various topics. 

### What if I do not find an answer to my questions?

It is always possible that you have questions or run into problems for which you cannot find the answer in the regular documentation. Here are some additional links that you can find answers to your questions:

* Bioexcel user forum: [https://ask.bioexcel.eu/c/haddock/6](https://ask.bioexcel.eu/c/haddock/6) 
* HADDOCK Help Center: [https://wenmr.science.uu.nl/haddock2.4/help](https://wenmr.science.uu.nl/haddock2.4/help) 
* HADDOCK software and online manual: [https://www.bonvinlab.org/software/haddock2.4/manual/](https://www.bonvinlab.org/software/haddock2.4/manual/)

### Tutorial icon conventions

Throughout the tutorial we will use the following special fonts and icons to perform certain tasks or draw your attention:

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

<hr>

## Introduction to the tutorial test case

To illustrate our protein-DNA docking protocol we will use as an example the complex between the bacteriophage 434 Cro repressor proteins and the OR1 operator.

### Cro is part of the bacteriophage 434 genetic switch

Cro is a *repressor* protein of the temperate bacteriophage 434.
It works in opposition to the phage's *repressor* protein to control the genetic switch.
The competition between both determines whether the phage embarks on a lytic or lysogenic lifecycle after infection.
The *repressors* compete to gain control over an operator region containing three operators that determine the state of the lytic/lysogenic genetic switch.
If Cro wins the late genes of the phage will be expressed and the result is lysis.
If the phage *repressor* wins the transcription of Cro, genes is further blocked and *repressor* synthesis is maintained, resulting in a state of lysogeny.

### Structure of the Cro-OR1 complex

The structure of bacteriophage 434 Cro in complex with the OR1 operator was solved by X-ray crystallography ([4], **Figure 1**).
We will use this structure as reference (or target) during the remaining of the tutorial.
Cro functions as a symmetrical dimer.
Each subunit contains a helix-turn-helix (HTH) DNA binding motif.
This is a typical DNA major groove-binding motif.
Helices α2 and α3 are separated by a short turn. Helix α3 is the recognition helix that fits into the major groove of the operator DNA and is oriented with its axes parallel to the major groove.
The side chains of each helix are thus positioned to interact with the edges of base pairs on the floor of the groove.
Non-specific interactions also help anchor Cro to operator DNA.
These include H-bonds between main chain NH groups and phosphate oxygen's of the DNA in the region of the operator.
Cro distorts the normal B-form DNA conformation: the OR1 DNA is bent (curved) by Cro, and the middle region of the operator is overwound, as reflected in the reduced distance between phosphate backbones in the minor groove. 

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-DNA-basic/CRO-OR1.png">
<p> <b>Figure 1:</b> Cartoon representation of the X-ray structure (PDB id 3CRO) of the bacteriophage 434 Cro-OR1 complex.</p>
</figure>

<hr>

## Preparing the HADDOCK2.4 web server run

The introduction of the HADDOCK web server in 2008 and the eNMR Grid-enabled web server shortly after, changed a lot in the docking community.
HADDOCK 2.4 is now available for commercial use through [https://wenmr.science.uu.nl/haddock2.4/](https://wenmr.science.uu.nl/haddock2.4/) after registration.
As the years progressed, new machine learning based modelling tools started to emerge, such as AlphaFold.
Although machine learning based methods eased modelling of a variety of protein-protein complexes, it cannot be used for protein-DNA or protein-RNA modelling.
Therefore, HADDOCK remain a convenient tool to be used for protein-DNA docking.
The combination of automated setup procedures, vigorous checks of the input, best practice defaults, easy access to many of the powerful HADDOCK features and access to ample computer resources has made docking available to a wide audience. 

Protein-DNA complexes are one of the more challenging systems to dock but also here the HADDOCK web server assists the user with a number of automated routines to setup the system correctly.
This tutorial will introduce you to these features. 

### Using this part

With the protein and DNA starting structures available and the Ambiguous Interaction Restraints setup, you can start setting up your docking using the HADDOCK web server.

This part will introduce you to the use of the HADDOCK web server for the docking of protein-DNA systems.
Although basic two-body protein-DNA docking can be performed using the HADDOCK Easy interface privileges, the use of custom Ambiguous Interaction Restraints requires the `Expert` privileges and the use of additional restraint types such as symmetry restraints, tweaking of the sampling parameters and multi-body docking requires the `Guru` privileges.
Hence, for this tutorial you will require Guru access privileges.
After registering to HADDOCK from [here](https://wenmr.science.uu.nl/auth/register/haddock), you can request access elevation from [here](https://wenmr.science.uu.nl/usr/).

<hr>

## Protein-DNA docking using the HADDOCK web server

Apart from the default setup procedures and server input checks, the use of DNA requires two additional steps that are automatically performed by the server:

* The server will define the proper nucleic acid topology, parameter and linkage files for the partners indicated to be DNA. A ribose or deoxyribose patch will be applied depending on the choice of “Nucleic acid (DNA and/or RNA)” as input structure. 
* An additional set of restraints will be generated to help maintain the helical structure of the DNA. These include sugar-pucker restraints, nucleotide base planarity restraints, sugar-phosphate backbone dihedral restraints and Watson-Crick hydrogen bond restraints between nucleotides that have been detected to be within pairing distance of one another. 

In addition to these automatic setup procedures, there are a number of settings specific to protein-DNA docking that are worth considering:

* Flexibility: DNA often changes conformation globally in the vicinity of the interface of the protein. To allow such changes to occur, you need to define nearly the full DNA sequence as semi-flexible to allow the DNA to change conformation globally. Full flexibility is not recommended.
* Dielectric constant (epsilon): Is set to 78 on default for both *it0* and *it1*.
* Advanced sampling parameters: the heating and cooling regime in the simulated annealing stages is optimized for protein systems but might be a bit too coarse for DNA systems. Reducing temperature, and the number and size of time steps will help in maintaining the helical structure of the DNA.

<hr>

## Preparing the Cro-OR1 docking run

Setup the Cro-OR1 multi-body docking run using HADDOCK 2.4 webserver.
Input files can be found in `protein-DNA_basic` directory.

### Input data

<a class="prompt prompt-info">
Name --> Give your run a name.
</a>
<a class="prompt prompt-info">
Molecules --> 3
</a>

**Molecule 1 - input:**

<a class="prompt prompt-info">
Which chain of the structure must be used? --> All<br>
PDB structure to submit --> 1ZUG_ensemble.pdb<br>
What kind of molecule are you docking? --> Protein or Protein-Ligand<br>
Segment ID to use during the docking --> A
</a>

**Molecule 2 - input:**

<a class="prompt prompt-info">
Which chain of the structure must be used? --> All<br>
PDB structure to submit --> 1ZUG_ensemble.pdb<br>
What kind of molecule are you docking? --> Protein or Protein-Ligand<br>
Segment ID to use during the docking --> C
</a>

**Molecule 3 - input:**

<a class="prompt prompt-info">
Which chain of the structure must be used? --> All<br>
PDB structure to submit --> OR1_unbound.pdb<br>
What kind of molecule are you docking? --> Nucleic acid (DNA and/or RNA)<br>
Segment ID to use during the docking --> B
</a>

Click `Next` at the bottom of the page to proceed to “Input parameters” section.
This will upload the structures to the HADDOCK webserver where they will be processed and validated (checked for formatting errors).
The server makes use of *Molprobity* to check side-chain conformations, eventually swap them (e.g. for asparagines) and define the protonation state of histidine residues.

### Input parameters

**Molecule 3 (OR1) - parameters:**

<a class="prompt prompt-info">
From the “Semi-flexible segments” definition of molecule 3:<br>
How are the flexible segments defined? --> Manual<br>
Semi-flexible segments --> 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39
</a>

Click `Next` at the bottom of the page to proceed to “Docking parameters” section.

### Docking parameters

**Distance restraints:**

<a class="prompt prompt-info">
Upload the `ambig_pm.tbl` AIR file at “Instead of specifying active and passive residues, you can supply a HADDOCK restraints TBL file (ambiguous restraints)”
</a>

**Energy and interaction parameters:**

<a class="prompt prompt-info">
Epsilon constant for the electrostatic energy term in it0 --> 78 (78 by default)<br>
Epsilon constant for the electrostatic energy term in it1 --> 78 (78 by default)
</a>

**Clustering parameters:**

<a class="prompt prompt-info">
Clustering method --> RMSD (FCC by default)<br>
RMSD cutoff for clustering --> 20<br>
Minimum cluster size --> 4
</a>

By default, the recommended cut-off value is 7.5 Å.
However, because of the limited number of docking trials you performed with respect to the sampling requirements (due to flexibility and AIR restraints) the cut-off of 7.5 Å will not result in any clusters and hence no proper finalization of the docking run and it therefore increased to 20 Å.
Under “normal” conditions (i.e. not this tutorial), the 7.5 Å cut-off is good value to use.

**Symmetry restraints:**

<a class="prompt prompt-info">
Use symmetry restraints --> Check<br>
Number of C2 symmetry segment pairs --> 1<br>
C2 Segment pair (Segment 1) --> first residue 4, last residue 64, Segment ID: A<br>
C2 Segment pair (Segment 2) --> first residue 4, last residue 64, Segment ID: C
</a>

**Advanced sampling parameters:**

<a class="prompt prompt-info">
Initial temperature for third TAD cooling step with fully flexible interface: 300<br>
Factor for time step in TAD: 4<br>
Number of steps for 300K phase: 750
</a>

Click `Submit` at the bottom of the page to launch the docking.

<a class="prompt prompt-question">
Why is the full DNA structure defined as semi-flexible except for the terminal nucleotide pairs?
</a>

<hr>

## Analysis of docking run

In case you are running short in time, a permanent link to the docking results of this tutorial is made available at [the following link](https://wenmr.science.uu.nl/haddock2.4/run/4242424242/267340-Protein-DNA-Basic).

### Analysis on the HADDOCK result page

After you run has finished (approximately 1 hours, depending on the load of the server), you will be presented with the results page in which you can observe different data for each cluster (**Figure 2**).

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-DNA-basic/cluster_first.png">
<p> <b>Figure 2</b>: HADDOCK2.4 results page of protein-DNA docking of the first cluster, composed of 124 models.</p>
</figure>

**Note:** At the bottom of the page are present graphical representations of the results, showing the distribution of the solutions for various measures (HADDOCK score, van der Waals energy, …) as a function of the Fraction of Common Contact and RMSD from the best generated model (the best scoring model), as presented in **Figure 3**.
The graphs are interactive, you can turn on/off specific clusters, and zoom in on specific areas of the plot.

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-DNA-basic/graph_first.png">
<p> <b>Figure 3</b>: HADDOCK2.4 graphical representation of the results.</p>
</figure>

Finally, the bottom graphs show you the distribution of scores (van der Waals, Electrostatics and AIRs energy terms) for the various clusters.

### Analysis on your own computer

After you analysed the graphs that are presented within the HADDOCK2.4 result page, you can download the complete run output files from the top of the page by clicking the hyperlink after "The complete run can be downloaded as a gzipped tar file".

Open a new PyMol session and type the following commands in the prompt to superimpose the docking complex Y from cluster X to the reference structure.

<a class="prompt prompt-pymol">
load clustX_complex_Y.pdb<br>
load 3CRO_complex.pdb<br>
align clustX_complex_Y, 3CRO_complex
</a>

#### Bonus analysis

For the ones who already want to better digg into the results generated, several tools and scripts are provided in the `3CRO` directory.

First, go to the `3CRO` directory:

<a class="prompt prompt-cmd">
cd 3CRO<br>
ls
</a>

Extract the haddock2.4 docking results archive in the current working directory:

<a class="prompt prompt-cmd">
tar -xvf haddock-run-name.tgz
</a>

Make sure you have enabled the right shell environment:

<a class="prompt prompt-cmd">
source setup.sh (.csh)
</a>

Navigate one directory below the analysis directory root (below `3CRO`):

<a class="prompt prompt-cmd">
cd ..
</a>

Execute the command:

<a class="prompt prompt-cmd">
analysis -r 3CRO/haddock-run-name/ -an complex
</a>

Wait till the process is finished (this analysis procedure will take few minutes).

The analysis program will generate a new directory in `3CRO/haddock-run-name/` called `Analysis_3CRO_protein-DNA_basic`.
The `analysis.stat` file contains a summary of various statistics of the best ranking solutions after rigid body docking (it0), semi-flexible refinement (it1 and water) and for every cluster.
Detailed statistics are provided for the 10 best solutions according to the HADDOCK score and according to i-RMSD to the reference in every stage.
The same detailed statistics are listed for the 10 best solutions of every cluster according to the HADDOCK score (or less than 10 if the cluster is not so large).
For all these cases the interface fitted structures are available in the directory and can be visualized with a molecular viewer.

<hr>

## Congratulations!

You have made it to the end of this basic protein-DNA docking tutorial.
We hope it has been illustrative and may help you get started with your own docking projects.

Happy docking!

<hr>

## References

1) Dominguez, C. et al. (2003). **HADDOCK: a protein-protein docking approach based on biochemical or biophysical information**. *JACS*  125, 1731-1737<br>
2) van Dijk, M. et al. (2006). **Information-driven protein-DNA docking using HADDOCK: it is a matter of flexibility**.  *N.A.R.*  25, 3317-3325<br>
3) van Dijk and Bonvin (2010) **Pushing the limits of what is achievable in protein-DNA docking: benchmarking HADDOCK's performance**. *N.A.R.* 38, 5634-5647<br>
4) Mondragón and Harrison (1991). **The phage 434 Cro/OR1 complex at 2.5 A resolution**. *J Mol Biol* 219, 321-334

More information about the HADDOCK web server:
* de Vries et al. (2010). **The HADDOCK web server for data-driven biomolecular docking**. Nat Protoc 5, 883-897


