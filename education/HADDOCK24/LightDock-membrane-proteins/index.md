---
layout: page
title: "LightDock+HADDOCK membrane proteins tutorial"
excerpt: "A tutorial demonstrating the use of LightDock for predicting the structure of membrane receptor–soluble protein complex using the topological information provided by the membrane to guide the modelling process and the refinement of the predicted models using HADDOCK"
tags: [HADDOCK, LightDock, membrane, proteins, soluble, docking, transmembrane, lipid]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>

## 1. Introduction

This tutorial demonstrates the use of [LightDock](https://lightdock.org){:target="_blank"} for predicting the structure of membrane receptor–soluble protein complex using the topological information provided by the membrane to guide the modelling process. The resulting LightDock models are then refined using [HADDOCK2.4 webserver](https://haddock.science.uu.nl/haddock2.4/). We will be following the protocol described in [Roel-Touris *et al*, 2020](https://www.nature.com/articles/s41467-020-20076-5){:target="_blank"}.

Membrane proteins are among the most challenging systems to study with experimental structural biology techniques, thus computational techniques such as docking might offer invaluable insights on the modelling of those systems.

<figure align="center">
    <img src="/education/HADDOCK24/LightDock-membrane-proteins/3x29_membrane.png">
    <figcaption style="text-align:center"><b>Fig.1</b> 3X29 complex in a lipid bilayer as simulated by <a href="http://memprotmd.bioch.ox.ac.uk/_ref/PDB/3x29" target="_blank">MemProtMD</a>.</figcaption>
</figure>

In this tutorial we will be working with the crystal structure  of _Mus musculus_ [Claudin-19](http://www.ebi.ac.uk/interpro/entry/InterPro/IPR006187/){:target="_blank"} transmembrane protein (PDB code [3X29](https://www.ebi.ac.uk/pdbe/entry/pdb/3x29){:target="_blank"}, chain A) in complex with the unbound C-terminal fragment of the _Clostridium perfringens_ [Enteroxin](http://www.ebi.ac.uk/interpro/entry/InterPro/IPR003897/){:target="_blank"} (PDB code [2QUO](https://www.ebi.ac.uk/pdbe/entry/pdb/2quo){:target="_blank"}, chain A). The PDB code of the complex is [3X29](https://www.ebi.ac.uk/pdbe/entry/pdb/3x29){:target="_blank"} (chains A and B).

3X29 complex is one of the cases covered in the [MemCplxDB](https://github.com/haddocking/MemCplxDB) membrane protein complex benchmark ([Koukos _et al_, 2018](https://www.sciencedirect.com/science/article/pii/S0022283618308222)). Despite not being one of the most challenging cases covered in the benchmark in terms of flexibility, its relatively small size will help us describing the complete modelling protocol in the short time intended for a tutorial.

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

Throughout the tutorial, coloured text will be used to refer to questions or instructions, commands to be executed in the terminal, and/or PyMOL commands.

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

<hr>

## 2. LightDock general concepts

LightDock is a macromolecular docking software written in the Python programming language, designed as a framework for rapid prototyping and test of scientific hypothesis in structural biology. It was designed to be easy extensible by users and scalable for high-throughput computing (HTC). LightDock is capable of modelling backbone flexibility of molecules using anisotropic model networks ([ANM](https://en.wikipedia.org/wiki/Anisotropic_Network_Model)) and the energetic minimization is based on the [Glowworm Swarm Optimization](https://dx.doi.org/10.1007/978-3-319-51595-3) (GSO) algorithm.

LightDock protocol is divided in two main steps: **setup** and **simulation**. On setup step, input PDB structures for receptor and ligand partners are parsed and prepared for the simulation. Moreoever, a set of _swarms_ is arranged around the receptor surface. Each of these swarms represents an independent simulation in LightDock where a fixed number of agents, called _glowworms_, encodes for a possible receptor-ligand pose. During the simulation step, each of these glowworms will sample a given region of the energetic landscape depending on its neighboring glowworms. 

<figure align="center">
    <img src="/education/HADDOCK24/LightDock-membrane-proteins/4g6m_restraints.png">
    <figcaption style="text-align:center"><b>Fig.2</b> A receptor surface showing only two swarms. Each swarm contains a set of glowworms representing a possible receptor-ligand pose.</figcaption>
</figure>

Swarms on the receptor surface can be easily filtered according to regions of interest. Figure 2 shows an example where only two swarms have been calculated to focus on two residues of interest on the receptor partner (depicted in <span style="color:orange">orange</span>). **On this tutorial we will explore this capability in order to filter out incompatible transmembrane binding regions in membrane complex docking**.

For more information about LightDock, please visit the [tutorials section](https://lightdock.org/tutorials/).

<hr>

## 3. Setup/Requirements

In order to run this tutorial you will need to have the following software installed: [LightDock][link-lightdock] and [PyMOL][link-pymol].

Also, if not provided with special workshop credentials to use the HADDOCK portal, make sure to register in order to be able to submit jobs. Use for this the following registration page: [https://haddock.science.uu.nl/auth/register/haddock](https://haddock.science.uu.nl/auth/register/haddock){:target="_blank"}.


### Installing LightDock

Lightdock is distributed as a Python package through the [Python Package Index](https://pypi.org/project/lightdock/) (PyPI) repository.

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

<hr>

## 4. Data preparation

We will make use of the 3X29 complex simulated in a membrane lipid bilayer from the MemProtMD database ([Newport _et al._, 2018](https://doi.org/10.1093/nar/gky1047)).

First, go to the [3X29 complex page](http://memprotmd.bioch.ox.ac.uk/_ref/PDB/3x29/_sim/3x29_default_dppc/) at MemProtMD. On the `Data Download` section, download the PDB file corresponding to the [Coarse-grained snapshot (MARTINI representation)](http://memprotmd.bioch.ox.ac.uk/data/memprotmd/simulations/3x29_default_dppc/files/structures/cg.pdb). This file in PDB format contains the [MARTINI](http://cgmartini.nl/) coarse-grained (CG) representation of the phospholipid bilayer membrane and the protein complex. We will use the phosphate beads as the boundary for the transmembrane region for filtering the sampling region of interest in LightDock.

<figure align="center">
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

<figure align="center">
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

<hr>

## 6. HADDOCK Refinement

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

