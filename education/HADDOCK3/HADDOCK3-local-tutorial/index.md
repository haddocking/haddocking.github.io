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
TODO: add installation for profit?
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

You can visit this example in the `examples/docking-antibody-antigen` folder.

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
[gentbl]: https://alcazar.science.uu.nl/services/GenTBL/ "GenTBL"
[haddock24protein]: /education/HADDOCK24/HADDOCK24-protein-protein-basic/
[wang2000]: https://onlinelibrary.wiley.com/doi/10.1093/emboj/19.21.5635/abstract "Wang 2000"
[haddock-repo]: https://github.com/haddocking/haddock3 "HADDOCK 3 GitHub"
[installation]: https://www.bonvinlab.org/haddock3/INSTALL.html "Installation"
[link-forum]: https://ask.bioexcel.eu/c/haddock "HADDOCK Forum"
[link-freesasa]: https://freesasa.github.io "FreeSASA"
[link-haddock]: https://bonvinlab.org/software/haddock2.2 "HADDOCK 2.2"
[link-naccess]: https://www.bioinf.manchester.ac.uk/naccess/ "NACCESS"
[link-pymol]: https://www.pymol.org/ "PyMOL"
[overview]: https://www.bonvinlab.org/haddock3/intro.html "A brief introduction to HADDOCK3"
[hpr-ensemble]: https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-protein/data/hpr_ensemble.pdb "HPR ensemble"
[nat-pro]: https://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html "Nature protocol"
[air-help]: https://www.bonvinlab.org/software/haddock2.2/generate_air_help/ "AIRs help"
