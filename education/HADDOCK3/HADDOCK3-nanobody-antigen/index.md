---
layout: page
title: "Nanobody-antigen modelling tutorial using a local version of HADDOCK3"
excerpt: "A tutorial describing the use of HADDOCK3 to model a nanobody-antigen complex"
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
the structure of a nanobody-antigen complex using different possible information scenarios, ranging
from complete knowledge of the epitope to no information at all. 

Nanobodies are monomeric proteins that closely resemble the variable region of the heavy chain of an antibody.
They are derived from camelid heavy-chain antibodies and are composed of a single variable domain (VHH) that
contains the antigen-binding site. Nanobodies are small, stable, and soluble proteins that can be easily
produced in bacteria, yeast, or mammalian cells. They have a high affinity for their target antigens, typically
comparable to that of monoclonal antibodies. Nanobodies are used in a wide range of applications, such as


<figure style="text-align: center;">
  <img src="/education/HADDOCK3/nanobody_figure.png">
</figure>

As in antibodies, the small part of the nanobody region that binds the antigen is called **paratope**, while part of the antigen
that binds to an nanobody is called **epitope**. Different from antibodies, nanobodies have only 
**three complementarity-determining regions (CDRs)** (hypervariable loops) whose sequence and conformation are altered to bind to different antigens. 
Another important feature of these molecules is that the highly conserved amino acids that are not par of the CDRs, namely the **framework regions (FRs)**,
can play a role in the binding to the antigen. These interactions are thought to be non-specific and to occur because the absence of a light chain in the nanobody
makes using the FRs to interact with the antigen more necessary to attain higher affinity.

In this tutorial we will be working with the complex between a nanobody, 
and mouse plexing protein B1 (PDB ID: [8BB7](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k){:target="_blank"}).

<figure style="text-align: center;">
  <img src="/education/HADDOCK24/HADDOCK24-antibody-antigen/CDRs.png">
</figure>

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

We assume that you have a working installation of HADDOCK3 on your system. 
If not, please install it through

```bash
pip install haddock3
```

or refer to the [HADDOCK3 installation instructions](https://github.com/haddocking/haddock3/blob/main/docs/INSTALL.md){:target="_blank"} for more details.

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


<hr>
<hr>

## Preparing PDB files for docking

In this section we will prepare the PDB files of the nanobody and antigen for docking.
Crystal structures of both the antibody and the antigen in their free forms are available from the
[PDBe database](https://www.pdbe.org){:target="_blank"}.

_**Note**_ that `pdb-tools` is also available as a [web service](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.


_**Note**_: Before starting to work on the tutorial, make sure to activate haddock3 if installed using `conda`

<a class="prompt prompt-cmd">
conda activate haddock3
</a>


<hr>

### Preparing the nanobody structural ensemble

When having to deal with a nanobody, it is quite unlikely that its structure in the "unbound" form (i.e., without the antigen attached) has already been deposited on the PDB, but it's always good to check.

Our sequence of interest is the following:

<pre style="background-color:#DAE4E7">
>1-2C7
QVQLQESGGGLVQPGGSLRLSCAASGDTLDLYAIGWFRQTPGEEREGVSCISPSGSRTN
YADSVKGRFTISRDNAKNTVYLQMNGLRPEDTAVYFCAGSRPSAHYCSHYPTEYDDWGQ
GTQVTV
</pre>

Let's search the PDB database for similar sequences using the [PDB advanced search](https://www.rcsb.org/search/advanced){:target="_blank"}.

<a class="prompt prompt-info">Paste the nanobody sequence into the Sequence Similarity box.</a>

<a class="prompt prompt-info">Select Polymer Entities rather than Structures in the **Return** menu at the bottom of the search and submit the query.</a>

<a class="prompt prompt-question">Besides the target complex, what is the closest structure to our nanobody sequence? How close are the two sequences in terms of sequence identity?</a>

Taking the nanobody structure from the target PDB (7X2M) would not be very realistic, as the nanobody is already bound to the antigen. In a real-case scenario you would be forced to model the nanobody structure from scratch.

A possible way to do this is to use AlphaFold2. You can run your AlphaFold modelling from [Colabfold]()

We provide you with AlphaFold2 models coming from the nanobody run in presence (multimer) and absence (monomer) of the antigen. The models are available in the `pdbs` directory of the archive you downloaded. Additionally, we provide you with some models coming from an antibody-specific predictor, [ImmuneBuilder](https://immunebuilder.org/){:target="_blank"}.

Let's have a look at them in PyMOL.

<a class="prompt prompt-pymol">
File menu -> Open -> select 7X2M_multimer_rank_001.pdb
File menu -> Open -> select 7X2M_monomer_rank_001.pdb
File menu -> Open -> select 7X2M_IB_rank_001.pdb
</a>

<a class="prompt prompt-info">Remember that the ranking used by AlphaFold2 changes between the monomer and multimer version!</a>

Check out [this description]() for more information about it.

SOMETHING ABOUT THE KINKED CONFORMATION OF THE NANOBODY

<a class="prompt prompt-question">Are the two nanobody models different? If yes, where do you see the major differences?</a>

The CDR3 loop is the main contributor to the binding, and it is the longest and most variable loop in the nanobody. Predicting its conformation is extremely challenging, and it is not uncommon to see different conformations in the models.

Let's visualize AlphaFold2's confidence in the prediction and in particular the values of the predicted Local Distance Difference Test (pLDDT) score. The pLDDT score is a per-residue confidence score that ranges from 0 to 100, with higher values indicating higher confidence. In AlphaFold2 and similar predictors the confidence score is typically encoded in the B-factor column of the PDB file.

<a class="prompt prompt-pymol">
select cd3, 7X2M_monomer_rank_001.pdb and resi 99:115
spectrum b, selection=cd3
</a>

<a class="prompt prompt-question">What are the residues with the highest/lowest confidence in this region? Are the residues with the lowest confidence those that change the most between the three structural models?</a>

<figure align="center">
  <img width="90%" src="/education/HADDOCK3/HADDOCK3-nanobody-antigen/af2_monomer_h3_plddt.png">
</figure>
<center>
  <i>Top ranked AlphaFold2-monomer nanobody prediction. The CDR3 is coloured according to the pLDDT values. The lowest ones (around 60) are shown in blue, while the highest ones (>90) are the anchor residues, shown in red.</i>
</center>

<a class="prompt prompt-info">Inspect the pLDDT of the H1 and H2 loops and check that they are confidently predicted.</a>

In this situation we are quite happy about the overall fold of the nanobody and we can say that the kinked region of the CDR3 loop is well predicted. We cannot say much about the three residues at the start of the loop, as their confidence is not great. In this case we will therefore mix the three nanobody models to create a structural ensemble, with the aim of capturing the right H3 conformation in at least one of the models. This has been shown multiple times to be a good strategy to improve the docking results.

First, let's extract the nanobody from the multimer model.

<a class="prompt prompt-cmd">
pdb_selchain -A 7X2M_multimer_rank_001.pdb > 7X2M_multimer_rank_001_A.pdb
</a>

Now we have to renumber the ImmuneBuilder models, as its numbering is not coherent with the other two models.

<a class="prompt prompt-cmd">
pdb_reres -1 7X2M_IB_rank_001.pdb | pdb_chain -A | pdb_tidy > 7X2M_IB_A.pdb
</a>

We're now ready to create the ensemble.

<a class="prompt prompt-cmd">
pdb_mkensemble 7X2M_multimer_rank_001_A.pdb 7X2M_monomer_rank_001.pdb 7X2M_IB_A.pdb | pdb_tidy > 7X2M_nb_ensemble.pdb
</a>

_**Note**_ that the corresponding files can be found in the `pdbs` directory of the archive you downloaded.

<hr>

### Preparing the antigen structure

Is it necessary to build the antigen structure from scratch using AlphaFold? Again, let's check the PDB database. The fact that we are dealing with a fragment of an extremely well-studied protein (the Sars-CoV-2 spike protein) makes it very likely that we will find the structure of the antigen in the PDB.

The sequence of the antigen is the following:

<pre style="background-color:#DAE4E7">
>P0DTC2
TNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCF
TNVYADSFVIRGDEVRQIAPGQTGNIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYL
YRLFRKSNLKPFERDISTEIYQAGSTPCNGVKGFNCYFPLQSYGFQPTYGVGYQPYRVVV
LSFELLHAPATVCGPK
</pre>

<a class="prompt prompt-info">Repeat the Sequence Similarity search described [here](Preparing-the-nanobody-structural-ensemble).</a>

<a class="prompt prompt-question">Are there any structures showing 100% sequence identity?</a>

Using PDB-tools we will download an unbound structure of the antigen from the PDB database (the PDB ID is [7EKG](https://www.ebi.ac.uk/pdbe/entry/pdb/7ekg){:target="_blank"}).

We will select the chain corresponding to our antigen, remove the hetero atoms from the structure, and renumber the residues and then... we will have our antigen!

<a class="prompt prompt-cmd">
pdb_fetch 7EKG | pdb_selchain -B | pdb_delhetatm | pdb_keepcoord | pdb_reres -1 | pdb_chain -B | pdb_chainxseg | pdb_tidy -strict > 7EKG_clean.pdb
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
HADDOCK illustrating four scenarios:

* **paratope on the nanobody, epitope region on the antigen**
* **HV loops on the nanobody, epitope region on the antigen**
* **HV loops on the nanobody, vaguely defined epitope region on the antigen**
* **HV loops on the nanobody, mutagenesis-based restraints on the antigen**

Information about various types of distance restraints in HADDOCK can also be
found in our [online manual][air-help]{:target="_blank"} pages.

<hr>

### Identifying the paratope of the antibody

<pre style="background-color:#DAE4E7">
26,27,28,30,31,54,56,57,100,101,102,104,105,109,111,112,114
</pre>

The numbering corresponds to the numbering of the `7X2M_nb_ensemble.pdb` PDB file.

Let us visualize those onto the 3D structure.
For this start PyMOL and load one of the elements of the `7X2M_nb_ensemble.pdb` ensemble (e.g., the monomer model).

<a class="prompt prompt-pymol">
File menu -> Open -> select 7X2M_monomer_rank_001.pdb
</a>

We will now highlight the predicted paratope. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all
</a>
<a class="prompt prompt-pymol">
select paratope, (resi 26+27+28+30+31+54+56+57+100+101+102+104+105+109+111+112+114)<br>
</a>
<a class="prompt prompt-pymol">
color red, paratope
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
    <b><i>See surface view of the paratope</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="50%" src="./nanobody-paratope.png">
  </figure>
  <br>
</details>

<hr>


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
