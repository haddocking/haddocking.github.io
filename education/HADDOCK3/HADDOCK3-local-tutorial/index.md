---
layout: page
title: "Tutorial describing the use of a local version of HADDOCK3"
excerpt: "A tutorial describing the use a local version HADDOCK3"
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

This tutorial demonstrates how to use a local installation of HADDOCK3 for
predicting the structure of biomolecular complexes. It will cover various steps:
1) the local installation of HADDOCK3 and the third party software required, 2)
the preparation of PDB files for docking, 3) the definition of restraints to
guide the docking, 4) the setup of the docking and 5) finally the analysis of
the results. General information about HADDOCK can be found on our [group
page][link-haddock] and its corresponding [online manual][link-manual]. Also
take note of the [HADDOCK online forum][link-forum] where you can post
HADDOCK-related questions and search the archive for possible answers.

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

## HADDOCK general concepts

HADDOCK (see
[https://www.bonvinlab.org/software/haddock2.2](https://www.bonvinlab.org/software/haddock2.2))
is a collection of python scripts derived from ARIA
([https://aria.pasteur.fr](https://aria.pasteur.fr)) that harness the power of
CNS (Crystallography and NMR System –
[https://cns-online.org](https://cns-online.org)) for structure calculation of
molecular complexes. What distinguishes HADDOCK from other docking software is
its ability, inherited from CNS, to incorporate experimental data as restraints
and use these to guide the docking process alongside traditional energetics and
shape complementarity. Moreover, the intimate coupling with CNS endows HADDOCK
with the ability to actually produce models of sufficient quality to be
archived in the Protein Data Bank.

A central aspect to HADDOCK is the definition of Ambiguous Interaction
Restraints or AIRs. These allow the translation of raw data such as NMR
chemical shift perturbation or mutagenesis experiments into distance restraints
that are incorporated in the energy function used in the calculations. AIRs are
defined through a list of residues that fall under two categories: active and
passive. Generally, active residues are those of central importance for the
interaction, such as residues whose knockouts abolish the interaction or those
where the chemical shift perturbation is higher. Throughout the simulation,
these active residues are restrained to be part of the interface, if possible,
otherwise incurring in a scoring penalty. Passive residues are those that
contribute for the interaction, but are deemed of less importance. If such a
residue does not belong in the interface there is no scoring penalty. Hence, a
careful selection of which residues are active and which are passive is
critical for the success of the docking.

The docking protocol of HADDOCK was designed so that the molecules experience
varying degrees of flexibility and different chemical environments, and it can
be divided in three different stages, each with a defined goal and
characteristics:

### A brief into HADDOCK3

Contrarily to HADDOCK2.X which follows a rigid (yet highly parametrizable)
procedure, in HADDOCK3, users can create their own simulation workflows by
combining a multitude of independent modules that perform specialized tasks.

Read [here about the overview and concept of the HADDOCK3 project][overview].

<hr>
<hr>
### Downloading HADDOCK

In this tutorial we will make use of the new HADDOCK3 version. To obtained
HADDOCK3 navigate to [its official repository][haddock-repo], fill the
registration form, and clone the repository to a folder on your preference:

<a class="prompt prompt-cmd">
  cd software <br>
  git clone https://github.com/haddocking/haddock3 <br>
</a>


### Downloading CNS
The other required piece of software to run HADDOCK is its computational engine,
CNS (Crystallography and NMR System –
[https://cns-online.org](https://cns-online.org) ). CNS is
freely available for non-profit organisations. In order to get access to all
features of HADDOCK you will need to recompile CNS using the additional files
provided in the HADDOCK distribution in the `cns1.3` directory. Compilation of
CNS might be non-trivial. Consult for some guidance the related entry in the
[HADDOCK
forum](https://ask.bioexcel.eu/t/cns-errors-before-after-recompilation/54/23).

*Untar* the archive in the `software` directory.

### Installing HADDOCK3

Now, follow the installation instructions described in the [INSTALL][installation]
document online, or locally under `docs/INSTALL.md` in the `haddock3` cloned
folder.

### Auxiliary software

**[FreeSASA][link-freesasa]**. In order to identify surface-accessible residues
to define restraints for HADDOCK we can make use of [NACCESS][link-naccess]
freely available to non-profit users, or its open-source software alternative
[FreeSASA][link-freesasa]. We will here make use of FreeSASA. Following the
download and installation instructions from the [FreeSASA
website][link-freesasa]. The direct download command is:

<a class="prompt prompt-cmd">
  cd <br>
  mkdir software <br>
  cd software <br>
  wget https://freesasa.github.io/freesasa-2.0.3.tar.gz
</a>

If running into problems you might want to disable `json` and `xml` support.
Here we will assume you save the tar archive under the `software` directory in
your home directory:

<a class="prompt prompt-cmd">
  tar xvfz freesasa-2.0.3.tar.gz <br>
  cd freesasa-2.0.3 <br>
  ./configure \-\-disable-json \-\-disable-xml \-\-prefix ~/software <br>
  make<br>
  make install<br>
</a>

**[PDB-tools][link-pdbtools]**: A useful collection of Python scripts for the
manipulation (renumbering, changing chain and segIDs...) of PDB files is freely
available from our GitHub repository. `pdb-tools` is automatically installed
with HADDOCK3. If you have activated the HADDOCK3 Python enviroment you have
access to the pdb-tools package.

**[PyMol][link-pymol]**: We will make use of PyMol for visualisation. If not
already installed on your system, download and install PyMol.

At this point we will assume that you successfully downloaded all auxiliary
software and installed the executables (or links to them) in `~/software/bin`.

<a class="prompt prompt-info">
In order to run this tutorial smoothly, you should add to your path the various
software directories we just installed. Go into the software directory where
you installed the various software components.
</a>

If running under `bash` shell, type:

<a class="prompt prompt-cmd">
  cd bin; export PATH=${PATH}:\`pwd\` <br>
  cd .. <br>
  cd haddock-tools; export PATH=${PATH}:\`pwd\` <br>
  cd .. <br>
  cd freesasa-2.0.3/src; export PATH=${PATH}:\`pwd\` <br>
  cd ..<br>
</a>

<!--
TODO: is csh needed?
-->

And for `csh`:

<a class="prompt prompt-cmd">
cd bin; set path= ( $path \`pwd\` ) <br>
cd .. <br>
cd haddock-tools; set path= ( $path \`pwd\` ) <br>
cd .. <br>
</a>

<!--
TODO: add installation for haddock-tools
-->

<!--
TODO - explain the job batch system
Or maybe in a later section.
-->


## Preparing PDB files for docking

In this section we describe some basic points in preparing PDB files for
HADDOCK. First of all, each PDB file must end with an `END` statement. We will
illustrate here three aspects:

* Cleaning PDB files prior to docking
* Introducing a mutation in a PDB file
* Dealing with an ensemble of models
* Dealing with multi-chain proteins

We suggest to create separate directories for the different cases and work from
those.

### Cleaning PDB files prior to docking

We will use here as example the E2A structure used as input in our [HADDOCK
webserver basic protein-protein docking
tutorial](/education/HADDOCK24/HADDOCK24-protein-protein-basic/). This protein
is part of a phospho-transfer complex and one of its histidine residue should in
principle be phosphorylated. Start PyMOL and in the command line window of
PyMOL (indicated by PyMOL>) type:

<a class="prompt prompt-pymol">
  fetch 1F3G <br>
</a>

<a class="prompt prompt-pymol">
  show cartoon <br>
  hide lines <br>
  show sticks, resn HIS <br>
</a>

You should see a backbone representation of the protein with only the histidine
side-chains visible. Try to locate the histidines in this structure.

<a class="prompt prompt-question">
  Is there any phosphate group present in this structure?
</a>

Note that you can zoom on the histidines by typing in PyMOL:

<a class="prompt prompt-pymol">
  zoom resn HIS
</a>

Revert to a full view with:

<a class="prompt prompt-pymol">
  zoom vis
</a>

As a preparation step before docking, it is advised to remove any irrelevant
water and other small molecules (e.g. small molecules from the crystallisation
buffer), however do leave relevant co-factors if present. For E2A, the PDB file
only contains water molecules. You can remove those in PyMOL by typing:

<a class="prompt prompt-pymol">
  remove resn HOH
</a>

As final step save the molecule as a new PDB file which we will call:
*e2a_1F3G.pdb*. For this, in the PyMOL command line type:

<a class="prompt prompt-pymol">
  save e2a_1F3G.pdb
</a>

**Note** that you can of course also simply edit the PDB file with your favorite
text editor.

Since the biological function of the E2A-HPR complex is to transfer a phosphate
group from one protein to another, via histidines side-chains, it is relevant to
make sure that a phosphate group be present for docking. As we have seen above
none is currently present in the PDB files. HADDOCK does support a list of
modified amino acids which you can find at the following link:
[https://wenmr.science.uu.nl/haddock2.4/library](https://wenmr.science.uu.nl/haddock2.4/library).

<a class="prompt prompt-question">
  Check the list of supported modified amino acids.
</a>

<a class="prompt prompt-question">
  What is the proper residue name for a phospho-histidine in HADDOCK?
</a>

In order to use a modified amino-acid in HADDOCK, the only thing you will need
to do is to edit the PDB file and change the residue name of the amino-acid you
want to modify. Don't bother deleting irrelevant atoms or adding missing ones,
HADDOCK will take care of that. For E2A, the histidine that is phosphorylated
has residue number 90. In order to change it to a phosphorylated histidine do
the following:

<a class="prompt prompt-info">
  Edit the PDB file (*e2a_1F3G.pdb*) in your favorite editor.
</a>

<a class="prompt prompt-info">
  Change the name of histidine 90 to NEP.
</a>

<a class="prompt prompt-info">
  Save the file (as simple text file) under a new name, e.g. *e2aP_1F3G.pdb*.
</a>

**Note:** The same procedure can be used to introduce a mutation in an input
protein structure.

**Note:** In the `haddock-tools` scripts that you installed, there is a python
script called `pdb_mutate.py` that allows you to introduce such a mutation from
the command line (call the script without arguments to see its usage):

<a class="prompt prompt-cmd">
  pdb_mutate.py e2a_1F3G.pdb A 90 HIS NEP > e2aP_1F3G.pdb
</a>

Prior to using this file in HADDOCK you need to remove any chainID and segID
information. This can easily be done using our `pdb-tools` scripts:

<a class="prompt prompt-cmd">
  pdb_chain e2aP_1F3G.pdb | pdb_seg > e2aP_1F3G-clean.pdb
</a>

In case your PDB file comes from some modelling software, it might be good to
check that it is properly formatted. This can be done with our `pdb-tools`
script:

<a class="prompt prompt-cmd">
  pdb_validate e2aP_1F3G-clean.pdb
</a>

You can also check if your PDB model has gaps in the structure. If gaps are
detected you can either try to model the missing fragments, or define a few
distance restraints to keep the fragments together during docking (see the
section about [Dealing with multi-chain proteins](#dealing-with-multi-chain-proteins).

<a class="prompt prompt-cmd">
  pdb_gap e2aP_1F3G-clean.pdb
</a>

Another possible issue with the starting PDB structures can be double occupancy
of some side-chains. This is quite common in high resolution crystal structures.
For HADDOCK, you will have to remove those double occupancies (or create
multiple models corresponding to various conformations). A simply way to get rid
of double occupancies (only the first occurrence of each side-chain will be kept)
is to use the `pdb-tools` `pdb_selaltloc` command.

<a class="prompt prompt-cmd">
  pdb_selaltloc e2aP_1F3G-clean.pdb > tmp && mv tmp e2aP_1F3G-clean.pdb && rm tmp
</a>

### Dealing with an ensemble of models

HADDOCK can take as input an ensemble of conformations. This has the advantage
that it allows to pre-sample possible conformational changes. We however
recommend to limit the number of conformers used for docking, because the number
of conformer combinations of the input molecules might explode (e.g. 10
conformers each will give 100 starting combinations, and if we generate 1000
rigid body models (see [HADDOCK general concepts](#haddock-general-concepts)
above) each combination will only be sampled 10 times).

While the HADDOCK2.4 webportal will take those as an ensemble PDB file (with
`MODEL` / `ENDMDL` statements), the local version of HADDOCK3 expects those
models to be provided as single structure. To illustrate this we will use the
HPR protein used as input in our [HADDOCK2.4 webserver basic protein-protein
docking tutorial](/education/HADDOCK24/HADDOCK24-protein-protein-basic/). The
input structure for docking corresponds to an NMR ensemble of 30 models.

We will now inspect the HPR structure. For this, start PyMOL and in the command
line window of PyMOL type:

<a class="prompt prompt-pymol">
  fetch 1HDN
</a>

<a class="prompt prompt-pymol">
  show cartoon <br>
  set all_states, on <br>
</a>

You should now be seeing the 30 conformers present in this NMR structure. Save
the molecule as a new PDB file which we will call: *hpr_1HDN.pdb*. For this, in
the PyMOL command line window type:

<a class="prompt prompt-pymol">
  save hpr_1HDN.pdb, state=0
</a>

As in the previous example, make sure to remove all chainID and segidID from the
PDB file:

<a class="prompt prompt-cmd">
  pdb_chain hpr_1HDN.pdb | pdb_seg > hpr_1HDN-clean.pdb
</a>

In the `example/docking-protein-protein/data` subfolder of the `haddock3`
installation folder, you will find the `hpr_ensemble.pdb` file that contains [10
models of the HPR structure][hpr-ensemble].

<hr>
<hr>
### Dealing with multi-chain proteins

It can happen that one of your molecule consists of multiple chains, such as for
example a homo-dimer or an antibody structure.  HADDOCK can in principle handle
those, but it is important that there is not overlap in the residue numbering
between the chains since the molecule will be assigned a single chainID/segID
for docking. As an example we will consider an antibody structure (PDB entry
4G6K).

<a class="prompt prompt-pymol">
fetch 4G6K<br>
</a>

<a class="prompt prompt-pymol">
show cartoon<br>
hide lines<br>
remove resn HOH<br>
</a>

This structure consists of two chains, L and H, with overlapping residue
numbering. Turn on the sequence in PyMol (under the Display menu) and find out
what is the last residue number of the first chain L. We need this information
to know by how much we should shift the numbering of the second chain.

Save the molecule as a PDB file:

<a class="prompt prompt-pymol">save 4G6K.pdb</a>

We will now shift the numbering of chain L to avoid overlap in numbering. This
can easily be done using our `pdb-tools` scripts. The first chain ends with
residue number 212 and the second chain starts at 1. We will shift the numbering
of the second chain by 500 to avoid numbering overlap:

<a class="prompt prompt-cmd">
  pdb_selchain -H 4G6K.pdb | pdb_tidy > 4G6K_H.pdb <br>
  pdb_selchain -L 4G6K.pdb | pdb_shiftres.py -500 | pdb_tidy > 4G6K_L.pdb <br>
  pdb_merge 4G6K_H.pdb 4G6K_L.pdb | pdb_chain.py | pdb_seg.py | pdb_tidy > 4G6K-clean.pdb <br>
</a>

We added a TER statement between the chains and an END statement at the end of
the file.

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

<!---
TODO: confirm the above examples with unambig work
Note that the values differ from HADDOCK2 to the example in HADDOCK3 docking-antibody-antigen/data/unambig.tbl
-->


[haddock-repo]: https://github.com/haddocking/haddock3 "HADDOCK 3 GitHub"
[installation]: https://www.bonvinlab.org/haddock3/INSTALL.html "Installation"
[link-forum]: https://ask.bioexcel.eu/c/haddock "HADDOCK Forum"
[link-freesasa]: https://freesasa.github.io "FreeSASA"
[link-haddock]: https://bonvinlab.org/software/haddock2.2 "HADDOCK 2.2"
[link-naccess]: https://www.bioinf.manchester.ac.uk/naccess/ "NACCESS"
[link-pymol]: https://www.pymol.org/ "PyMOL"
[overview]: https://www.bonvinlab.org/haddock3/intro.html "A brief introduction to HADDOCK3"
[hpr-ensemble]: https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-protein/data/hpr_ensemble.pdb "HPR ensemble"
