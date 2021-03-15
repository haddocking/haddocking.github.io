---
layout: page
title: "LightDock+HADDOCK membrane proteins tutorial"
excerpt: "A tutorial demonstrating the use of LightDock for predicting the structure of membrane receptor–soluble protein complex using the topological information provided by the membrane to guide the modeling process and the refinement of the predicted models using HADDOCK"
tags: [HADDOCK, LightDock, membrane, proteins, soluble, docking, transmembrane, lipid]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>

## 1. Introduction

This tutorial demonstrates the use of [LightDock](https://lightdock.org){:target="_blank"} for predicting the structure of membrane receptor–soluble protein complex using the topological information provided by the membrane to guide the modeling process. The resulting LightDock models are then refined using [HADDOCK2.4 webserver](https://haddock.science.uu.nl/haddock2.4/). We will be following the protocol described in [Roel-Touris *et al*, 2020](https://www.nature.com/articles/s41467-020-20076-5){:target="_blank"}.

Membrane proteins are among the most challenging systems to study with experimental structural biology techniques, thus computational techniques such as docking might offer invaluable insights on the modeling of those systems.

<figure style="text-align:center">
    <img src="/education/HADDOCK24/LightDock-membrane-proteins/3x29_membrane.png">
    <figcaption style="text-align:center"><b>Fig.1</b> 3X29 complex in a lipid bilayer as simulated by <a href="http://memprotmd.bioch.ox.ac.uk/_ref/PDB/3x29" target="_blank">MemProtMD</a>.</figcaption>
</figure>

In this tutorial we will be working with the crystal structure  of _Mus musculus_ [Claudin-19](http://www.ebi.ac.uk/interpro/entry/InterPro/IPR006187/){:target="_blank"} transmembrane protein (PDB code [3X29](https://www.ebi.ac.uk/pdbe/entry/pdb/3x29){:target="_blank"}, chain A) in complex with the unbound C-terminal fragment of the _Clostridium perfringens_ [Enteroxin](http://www.ebi.ac.uk/interpro/entry/InterPro/IPR003897/){:target="_blank"} (PDB code [2QUO](https://www.ebi.ac.uk/pdbe/entry/pdb/2quo){:target="_blank"}, chain A). The PDB code of the complex is [3X29](https://www.ebi.ac.uk/pdbe/entry/pdb/3x29){:target="_blank"} (chains A and B).

3X29 complex is one of the cases covered in the [MemCplxDB](https://github.com/haddocking/MemCplxDB) membrane protein complex benchmark ([Koukos _et al_, 2018](https://www.sciencedirect.com/science/article/pii/S0022283618308222)). Despite not being one of the most challenging cases covered in the benchmark in terms of flexibility, its relatively small size will help us describing the complete modeling protocol in the short time intended for a tutorial.

<hr>

For this tutorial we will make use of the [HADDOCK2.4 webserver](https://haddock.science.uu.nl/haddock2.4){:target="_blank"} and [LightDock software](https://lightdock.org/){:target="_blank"}.

A description of the previous major version of our web server [HADDOCK2.2](https://alcazar.science.uu.nl/services/HADDOCK2.2){:target="_blank"} can be found in the following publications:

* G.C.P van Zundert, J.P.G.L.M. Rodrigues, M. Trellet, C. Schmitz, P.L. Kastritis, E. Karaca, A.S.J. Melquiond, M. van Dijk, S.J. de Vries and  A.M.J.J. Bonvin.
[The HADDOCK2.2 webserver: User-friendly integrative modeling of biomolecular complexes](https://doi.org/doi:10.1016/j.jmb.2015.09.014){:target="_blank"}.
_J. Mol. Biol._, **428**, 720-725 (2015).

* S.J. de Vries, M. van Dijk and A.M.J.J. Bonvin.
[The HADDOCK web server for data-driven biomolecular docking.](https://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html){:target="_blank"}
_Nature Protocols_, **5**, 883-897 (2010).  Download the final author version [here](https://igitur-archive.library.uu.nl/chem/2011-0314-200252/UUindex.html){:target="_blank"}.

The integrative approach followed in this tutorial is described here:

* J. Roel-Touris, B. Jimenez-Garcia and A.M.J.J. Bonvin. [Integrative modeling of membrane-associated protein assemblies](https://www.nature.com/articles/s41467-020-20076-5){:target="_blank"}. _Nat. Commun._, **11**, 6210 (2020).

LightDock docking framework is described in the following publications:

* J. Roel-Touris, A.M.J.J. Bonvin and B. Jimenez-Garcia. [LightDock goes information-driven](https://doi.org/10.1093/bioinformatics/btz642){:target="_blank"}. _Bioinformatics_, **36**:3 950-952 (2020).

* B. Jimenez-Garcia, J. Roel-Touris, M. Romero-Durana, M. Vidal, D. Jimenez-Gonzalez, J. Fernandez-Recio. [LightDock: a new multi-scale approach to protein-protein docking](https://doi.org/10.1093/bioinformatics/btx555){:target="_blank"}. _Bioinformatics_, **34**:1 49-55 (2018).

Throughout the tutorial, colored text will be used to refer to questions or instructions, commands to be executed in the terminal, and/or PyMOL commands.

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

<hr>

## 2. LightDock general concepts

LightDock is a macromolecular docking software written in the Python programming language, designed as a framework for rapid prototyping and test of scientific hypothesis in structural biology. It was designed to be easy extensible by users and scalable for high-throughput computing (HTC). LightDock is capable of modeling backbone flexibility of molecules using anisotropic model networks ([ANM](https://en.wikipedia.org/wiki/Anisotropic_Network_Model)) and the energetic minimization is based on the [Glowworm Swarm Optimization](https://dx.doi.org/10.1007/978-3-319-51595-3) (GSO) algorithm.

LightDock protocol is divided in two main steps: **setup** and **simulation**. On setup step, input PDB structures for receptor and ligand partners are parsed and prepared for the simulation. Moreover, a set of _swarms_ is arranged around the receptor surface. Each of these swarms represents an independent simulation in LightDock where a fixed number of agents, called _glowworms_, encodes for a possible receptor-ligand pose. During the simulation step, each of these glowworms will sample a given region of the energetic landscape depending on its neighboring glowworms. 

<figure style="text-align:center">
    <img src="/education/HADDOCK24/LightDock-membrane-proteins/4g6m_restraints.png">
    <figcaption style="text-align:center"><b>Fig.2</b> A receptor surface showing only two swarms. Each swarm contains a set of glowworms representing a possible receptor-ligand pose.</figcaption>
</figure>

Swarms on the receptor surface can be easily filtered according to regions of interest. Figure 2 shows an example where only two swarms have been calculated to focus on two residues of interest on the receptor partner (depicted in <span style="color:orange">orange</span>). **On this tutorial we will explore this capability in order to filter out incompatible transmembrane binding regions in membrane complex docking**.

For more information about LightDock, please visit the [tutorials section](https://lightdock.org/tutorials/).

<hr>

## 3. Setup/Requirements

In order to run this tutorial you will need to have the following software installed: [LightDock][link-lightdock], [pdb-tools][link-pdbtools] and [PyMOL][link-pymol].

Also, if not provided with special workshop credentials to use the HADDOCK portal, make sure to register in order to be able to submit jobs. Use for this the following registration page: [https://haddock.science.uu.nl/auth/register/haddock](https://haddock.science.uu.nl/auth/register/haddock){:target="_blank"}.


### Installing LightDock

LightDock is distributed as a Python package through the [Python Package Index](https://pypi.org/project/lightdock/) (PyPI) repository.

#### Command line
Installing LightDock is as simple as creating a virtual environment for **Python 3.6+** and running `pip` command (make sure your instances of `virtualenv` and `pip` are for Python 3.6+ versions). We will install the version _0.9.0a2_ of LightDock which is the first released version with support for the membrane protocol and execution in [Jupyter Notebooks](https://jupyter.org/) (see next section):

<a class="prompt prompt-cmd">
virtualenv venv<br>
source venv/bin/activate<br>
pip install numpy && pip install lightdock==0.9.0a2<br>
</a>

If the installation finished without errors, you should be able to execute LightDock in the terminal:

<a class="prompt prompt-cmd">
lightdock3.py -v
</a>

and to see an output similar to this:

<pre style="background-color:#DAE4E7">
lightdock3 0.9.0a2
</pre>

#### Jupyter Notebook and Google Colab

Another option to use LightDock is through [Google Colaboratory](https://colab.research.google.com) ("Colab" for short) which allows you to write and execute Python in the browser using _notebooks_. In case of choosing this option, simply execute in a new notebook in the first cell the following command:

<a class="prompt prompt-info">
!pip install lightdock==0.9.0a2
</a>

### Installing PDB-Tools

PDB-Tools is a set of Python scripts for manipulating PDB files following the philosophy of *one script, one task*. For different manipulating tasks on a PDB file, the procedure would be to *pipe* the different PDB-Tools scripts to accomplish the different tasks. 

PDB-Tools is distributed as a PyPI package. To install it, simply:

<a class="prompt prompt-info">
pip install pdb-tools
</a>

or alternatively in a Google Colab notebook:

<a class="prompt prompt-info">
!pip install pdb-tools
</a>

<hr>

## 4. Data preparation

We will make use of the 3X29 complex simulated in a membrane lipid bilayer from the MemProtMD database ([Newport _et al._, 2018](https://doi.org/10.1093/nar/gky1047)).

First, browse the [3X29 complex page](http://memprotmd.bioch.ox.ac.uk/_ref/PDB/3x29/_sim/3x29_default_dppc/) at MemProtMD. On the `Data Download` section, download the PDB file corresponding to the [Coarse-grained snapshot (MARTINI representation)](http://memprotmd.bioch.ox.ac.uk/data/memprotmd/simulations/3x29_default_dppc/files/structures/cg.pdb). This file in PDB format contains the [MARTINI](http://cgmartini.nl/) coarse-grained (CG) representation of the phospholipid bilayer membrane and the protein complex. We will use the phosphate beads as the boundary for the transmembrane region for filtering the sampling region of interest in LightDock.

<figure style="text-align:center">
    <img src="/education/HADDOCK24/LightDock-membrane-proteins/3x29_cg.png">
    <figcaption style="text-align:center">
        <b>Fig.3</b> MARTINI Coarse-grained representation of the 3X29 complex in a lipid bilayer. Protein is depicted as <span style="color:dodgerblue">blue</span> surface, CG beads for phospholipids in white, except for NC3 beads in <span style="color:darkturquoise">turquoise</span> and PO4 beads in <span style="color:orange">orange</span>.
    </figcaption>
</figure>

We have prepared a Python script to parse, rename and remove non-necessary beads for the membrane protocol in LightDock: <a href="/education/HADDOCK24/LightDock-membrane-proteins/prepare4lightdock.py">prepare4lightdock.py</a>. You will need to execute it in your terminal using the <a href="/education/HADDOCK24/LightDock-membrane-proteins/3x29_default_dppc-coarsegrained.pdb">3x29_default_dppc-coarsegrained.pdb</a> PDB file as input:

<a class="prompt prompt-cmd">
python3 prepare4lightdock.py 3x29_default_dppc-coarsegrained.pdb membrane_cg.pdb
</a>

The output of this script is the <a href="/education/HADDOCK24/LightDock-membrane-proteins/membrane_cg.pdb">membrane_cg.pdb</a> PDB file (Figure 4).

<figure style="text-align:center">
    <img src="/education/HADDOCK24/LightDock-membrane-proteins/3x29_mmb.png">
    <figcaption style="text-align:center">
        <b>Fig.4</b> Lipid bilayer membrane and protein after using the `prepare4lightdock.py` script. Protein is depicted as <span style="color:dodgerblue">blue</span> surface (only CA), membrane beads ready for LightDock in <span style="color:orange">orange</span>.
    </figcaption>
</figure>

The last step will be to open the just generated <a href="/education/HADDOCK24/LightDock-membrane-proteins/membrane_cg.pdb">membrane_cg.pdb</a> file in PyMOL to align the atomistic representation of the <a href="/education/HADDOCK24/LightDock-membrane-proteins/3x29_receptor.pdb">3X29 receptor partner</a> to the membrane CG bilayer:

<a class="prompt prompt-cmd">
pymol 3x29_receptor.pdb membrane_cg.pdb
</a>

Now execute the following commands on PyMOL to align the membrane with the atomistic receptor and saving the resulting PDB structure:

<a class="prompt prompt-pymol">
align 3x29_receptor and name CA, membrane_cg and name CA
</a>
<a class="prompt prompt-pymol">
remove membrane_cg and name CA
</a>
<a class="prompt prompt-pymol">
save 3x29_receptor_membrane.pdb, all
</a>

The last PyMOL command will save the aligned atomistic 3X29 receptor to the CG lipid bilayer: <a href="/education/HADDOCK24/LightDock-membrane-proteins/3x29_receptor_membrane.pdb">3x29_receptor_membrane.pdb</a>.

<hr>

## 5. LightDock simulation

### Simulation set up

The fist step in any LightDock simulation is setup. We will make use of `lightdock3_setup.py` command to initialize our 3X29 membrane simulation and the required input data is:

* <a href="/education/HADDOCK24/LightDock-membrane-proteins/3x29_receptor_membrane.pdb">Receptor structure PDB file</a>
* <a href="/education/HADDOCK24/LightDock-membrane-proteins/3x29_ligand.pdb">Ligand structure PDB file</a>

Use the `lightdock3_setup.py` command to set up the LightDock simulation:

<a class="prompt prompt-cmd">
lightdock3_setup.py 3x29_receptor_membrane.pdb 3x29_ligand.pdb --noxt --noh --membrane
</a>

In short, we are indicating to the setup command to use `3x29_receptor_membrane.pdb` as the receptor partner, `3x29_ligand.pdb` as the ligand, to skip `NOXT` and hydrogen atoms and to detect membrane beads with the `--membrane` flag. The output of the command should look similar to this:

<pre style="background-color:#DAE4E7">
[lightdock3_setup] INFO: Ignoring OXT atoms
[lightdock3_setup] INFO: Ignoring Hydrogen atoms
[lightdock3_setup] INFO: Reading structure from 3x29_receptor_membrane.pdb PDB file...
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue GLN.61
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue GLN.63
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue LYS.65
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue LEU.66
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue ASP.68
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue HIS.76
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue MET.95
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue MET.102
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue LYS.103
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue LYS.115
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue ARG.117
[lightdock3_setup] INFO: 1608 atoms, 601 residues read.
[lightdock3_setup] INFO: Ignoring OXT atoms
[lightdock3_setup] INFO: Ignoring Hydrogen atoms
[lightdock3_setup] INFO: Reading structure from 3x29_ligand.pdb PDB file...
[lightdock3_setup] INFO: 933 atoms, 117 residues read.
[lightdock3_setup] INFO: Calculating reference points for receptor 3x29_receptor_membrane.pdb...
[lightdock3_setup] INFO: Reference points for receptor found, skipping
[lightdock3_setup] INFO: Done.
[lightdock3_setup] INFO: Calculating reference points for ligand 3x29_ligand.pdb...
[lightdock3_setup] INFO: Reference points for ligand found, skipping
[lightdock3_setup] INFO: Done.
[lightdock3_setup] INFO: Saving processed structure to PDB file...
[lightdock3_setup] INFO: Done.
[lightdock3_setup] INFO: Saving processed structure to PDB file...
[lightdock3_setup] INFO: Done.
[lightdock3_setup] INFO: Calculating starting positions...
[lightdock3_setup] INFO: Generated 62 positions files
[lightdock3_setup] INFO: Done.
[lightdock3_setup] INFO: Number of calculated swarms is 62
[lightdock3_setup] INFO: Preparing environment
[lightdock3_setup] INFO: Done.
[lightdock3_setup] INFO: LightDock setup OK
</pre>

In previous versions of LightDock, the number of swarms of the simulated was given by the user (typically around 400), but since version `0.9.0`, the number of swarms of the simulation is automatically calculated depending on the surface area of the receptor structure. However, the number of swarms can be fixed by the user using the `-s` flag for reproducibility of old results purpose. Another difference with previous versions is that the number of glowworms is now default to 200. This value has been extensively tested on our previous work, but it may be defined by the user as well using the `-g` flag.

A complete list of `lightdock3_setup.py` command options might be obtained executing the command without arguments or with the `--help` flag:

<pre style="background-color:#DAE4E7">
usage: lightdock3_setup [-h] [-s SWARMS] [-g GLOWWORMS] [--seed_points STARTING_POINTS_SEED] [--noxt] [--noh] [--verbose_parser] [-anm] [--seed_anm ANM_SEED] [-ar ANM_REC]
                        [-al ANM_LIG] [-r restraints] [-membrane] [-transmembrane] [-sp] [-sd SURFACE_DENSITY] [-sr SWARM_RADIUS]
                        receptor_pdb_file ligand_pdb_file
lightdock3_setup: error: the following arguments are required: receptor_pdb_file, ligand_pdb_file
</pre>

The setup command has generated several files and directories:

<a class="prompt prompt-question">What is the content of the **setup.json** file?</a>

<a class="prompt prompt-question">What does the **init** directory contains?</a>

We may visualize the distribution of swarms over the receptor:

<a class="prompt prompt-cmd">
pymol lightdock_3x29_receptor_membrane.pdb init/swarm_centers.pdb
</a>

<figure style="text-align:center">
    <img src="/education/HADDOCK24/LightDock-membrane-proteins/3x29_membrane_swarms.gif">
    <figcaption style="text-align:center">
        <b>Fig.5</b> Distribution of swarms in the current simulation.
    </figcaption>
</figure>

<a class="prompt prompt-question">Is this a regid-body or a flexible simulation?</a>

### Running the simulation

The simulation is ready to run at this point. The number of swarms after focusing on the cytosolic region of the membrane is of 62.

LightDock optimization strategy (using the GSO algorithm) is agnostic of the scoring function (force-field). There are several scoring functions available at LightDock, from atomistic to coarse-grained. In this tutorial we will make use of `fastdfire`, which is the implementation of [DFIRE](https://doi.org/10.1110/ps.0217002) using the Python C API and the default if no scoring function is specified by the user. Find [here](https://lightdock.org/tutorials/basics#32-available-scoring-functions) a complete list of the current supported scoring functions by LightDock.

Simulation is the most time-consuming part of the protocol. For that reason, we will only simulate one of the 62 total swarms. Pick a swarm number between [0..61] and use that id in the `-l` argument:

<a class="prompt prompt-cmd">
lightdock3.py setup.json 100 -c 1 -s fastdfire -l 60
</a>

In the command above, we specify the JSON file of the simulation (`setup.json`), the number of steps of the simulation (`100`), the number of CPU cores to use (`-c 1`), the scoring function (`-s fastdfire`). If no `-l` argument is provided, the protocol would simulate all the swarms.

For your convenience, you can [download the full run](/education/HADDOCK24/LightDock-membrane-proteins/simulation.tgz) as a compressed file (45MB).

Once the simulation has finished, navigate to the `swarm_60` directory (or the one you have selected) and list the directory.

<a class="prompt prompt-question">How many gso_* files have been generated? Which one corresponds to the last step of the simulation?</a>

### Generating models

Once the simulation has finished successfully, it is time to generate the predicted models. For each swarm, there is a `gso_100.out` file containing the information to generate as many models as `glowworms` were defined in the simulation (200 in this tutorial). The command in charge of generating the models is `lgd_generate_conformations.py`.

Pick a swarm folder and generate the 200 models simulated as in step 100:

<a class="prompt prompt-cmd">
lgd_generate_conformations.py 3x29_receptor_membrane.pdb 3x29_ligand.pdb swarm_60/gso_100.out 200
</a>

You should see an output similar to this:

<pre style="background-color:#DAE4E7">
[generate_conformations] INFO: Reading ../lightdock_3x29_receptor_membrane.pdb receptor PDB file...
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue GLN.61
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue GLN.63
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue LYS.65
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue LEU.66
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue ASP.68
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue HIS.76
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue MET.95
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue MET.102
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue LYS.103
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue LYS.115
[pdb] WARNING: Possible problem: [SideChainError] Incomplete sidechain for residue ARG.117
[generate_conformations] INFO: 1608 atoms, 601 residues read.
[generate_conformations] INFO: Reading ../lightdock_3x29_ligand.pdb ligand PDB file...
[generate_conformations] INFO: 933 atoms, 117 residues read.
[generate_conformations] INFO: Read 200 coordinate lines
[generate_conformations] INFO: Generated 200 conformations
</pre>

### Clustering models

To remove very similar and redundant models in the same swarm, we will cluster the 200 generated models:

<a class="prompt prompt-cmd">
lgd_cluster_bsas.py swarm_60/gso_100.out
</a>

After a verbose output of the command above, a new file `cluster.repr` is generated inside the `swarm_60` folder. This file should look like this:

<pre style="background-color:#DAE4E7">
0:3:26.80832:115:lightdock_115.pdb
1:9:24.45152:42:lightdock_42.pdb
2:62:22.70320:37:lightdock_37.pdb
3:35:20.35832:0:lightdock_0.pdb
4:41:16.69347:38:lightdock_38.pdb
5:3:15.71026:79:lightdock_79.pdb
6:7:13.89057:72:lightdock_72.pdb
7:7:11.84427:164:lightdock_164.pdb
8:1: 8.69611:92:lightdock_92.pdb
9:1: 2.92199:137:lightdock_137.pdb
10:22:-0.00771:95:lightdock_95.pdb
11:2:-24.59441:93:lightdock_93.pdb
12:7:-31.35821:57:lightdock_57.pdb
</pre>

Each line represents a different cluster and lines are sorted from best to worst energy. For each line, there is information about the `cluster id`, the number of structures in the cluster, the best energy of the cluster, the `glowworm id` of the model with best energy and the PDB file name of the structure with best energy.

Open the best predicted model for this swarm in PyMOL and have a look.

<a class="prompt prompt-cmd">
pymol swarm_60/lightdock_115.pdb
</a>

<a class="prompt prompt-question">How does this model look in general? What about the side chains?</a>

<hr>

## 6. HADDOCK Refinement

HADDOCK (see [https://www.bonvinlab.org/software/haddock2.4](https://www.bonvinlab.org/software/haddock2.4)) is a collection of python scripts derived from [ARIA](https://aria.pasteur.fr) that harness the power of CNS (Crystallography and NMR System – [https://cns-online.org](https://cns-online.org)) for structure calculation of molecular complexes. What distinguishes HADDOCK from other docking software is its ability, inherited from CNS, to incorporate experimental data as restraints and use these to guide the docking process alongside traditional energetics and shape complementarity. Moreover, the intimate coupling with CNS endows HADDOCK with the ability to actually produce models of sufficient quality to be archived in the Protein Data Bank. **In this tutorial we will make use of the HADDOCK outstanding capabilities for refining inaccurate protein models.**

The HADDOCK2.4 online server provides a dedicated web interface to run a refinement on a molecular complex and can be accessed [here](https://haddock.science.uu.nl/haddock2.4/refinement).

### Data preparation

The first step to refine out top predicted models by LightDock will be to prepare an ensemble multi-model PDB file containing those top predicted models.

* First, download and decompress the [provided complete run](/education/HADDOCK24/LightDock-membrane-proteins/simulation.tgz).
* There is a file `lgd_clustered_rank.list` with all the clustered structures from the simulation ranked by score and already analyzed in terms of fraction of native contacts (fnc), interface RMSD (i-RMSD) and ligand RMSD (L-RMSD). See below the first ten structures:

<pre style="background-color:#DAE4E7">
# Structure        fnc     i-RMSD  L-RMSD  Score
swarm_22_112.pdb  0.05333  12.807  12.627  28.735
swarm_37_11.pdb   0.26667   4.250   4.146  28.152
swarm_39_11.pdb   0.14667   4.262   3.699  26.893
swarm_60_115.pdb  0.45333   1.868   2.285  26.808
swarm_54_167.pdb  0.0      16.469  15.239  25.651
swarm_37_34.pdb   0.02667  15.721  15.336  25.461
swarm_55_181.pdb  0.0      13.723  12.603  25.272
swarm_60_42.pdb   0.29333   4.312   4.216  24.452
swarm_37_169.pdb  0.0       8.642   7.771  24.426
swarm_37_83.pdb   0.0      16.334  15.516  24.133
</pre>

* Using `pdb-tools`, we will remove `MMB` fake bead residues, copy the chain ID into the segid field and finally creating an ensemble of the top 10 models (we provide the generated [top10_ensemble.pdb](/education/HADDOCK24/LightDock-membrane-proteins/top10_ensemble.pdb) for your convenience):

<a class="prompt prompt-cmd">
cd clustered; pdb_mkensemble swarm_22_112.pdb swarm_37_11.pdb swarm_39_11.pdb swarm_60_115.pdb swarm_54_167.pdb swarm_37_34.pdb swarm_55_181.pdb swarm_60_42.pdb swarm_37_169.pdb swarm_37_83.pdb | pdb_delresname -MMB | pdb_chainxseg > top10_ensemble.pdb
</a>

Please note that the structures are located inside the `clustered` directory.


### Submission

The HADDOCK refinement interface is composed by two separate steps.

* In the first step, provide a name for the project, for example *"3x29-top10-refinement"*. Then, select the file `top10_ensemble.pdb` containing the top 10 predicted models as a PDB multi-model ensemble file and click on *Next*.
* In the second step, a summary of the chains found by the server will be displayed. On the clustering section, leave it as if. Click on *Submit* to submit your refinement job to the server queue.

Depending on the server load, this step may take some time, but you will receive an email once the job has completed.

For your convenience, we provide the refinement job already calculated for you:
[https://wenmr.science.uu.nl/haddock2.4/run/4242424242/51589-3x29-top10-refinement ](https://wenmr.science.uu.nl/haddock2.4/run/4242424242/51589-3x29-top10-refinement)

<hr>

## 7. Analysis

<hr>

## Conclusions

We have demonstrated the use of membrane information on a protein docking simulation and how to further refine predicted models.

<hr>

## Congratulations!

You have completed this tutorial. If you have any questions or suggestions, feel free to contact us via email or asking a question through our [support center](https://ask.bioexcel.eu){:target="_blank"}.

And check also our [education](/education) web page where you will find more tutorials!

[link-pymol]: https://www.pymol.org/ "PyMOL"
[link-lightdock]: https://lightdock.org "LightDock"
[link-pdbtools]: https://github.com/haddocking/pdb-tools/ "PDB-Tools"

