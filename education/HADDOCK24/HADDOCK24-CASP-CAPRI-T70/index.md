---
layout: page
title: "HADDOCK 2.4 CASP-CAPRI T70 ab-initio docking tutorial"
excerpt: "A small tutorial on predicting a CASP-CAPRI target using the ab-initio mode of HADDOCK"
tags: [HADDOCK, CASP, CAPRI, docking, symmetry, dimer, tetramer]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}



## Introduction

Our information-driven docking approach [HADDOCK](https://www.bonvinlab.org/software/haddock2.2) is a consistent top predictor and scorer since the start of its participation in the [CAPRI](https://www.ebi.ac.uk/msd-srv/capri) community-wide experiment. This sustained performance is due, in part, to its ability to integrate experimental data and/or bioinformatics information into the modelling process, and also to the overall robustness of the scoring function used to assess and rank the predictions.

This tutorial will demonstrate the use of HADDOCK for predicting target70 of the CASP-CAPRI experiment. This target was given to the CAPRI community as a tetramer, but there has been discussions whether the biological unit is a dimer or a tetramer. We will use this target to illustrate the ab-initio docking mode of HADDOCK, using a combination of [center-of-mass restraints](https://www.bonvinlab.org/software/haddock2.2/run/#disre) to bring the subunits together and [symmetry restraints](https://www.bonvinlab.org/software/haddock2.2/run/#sym) to define the symmetry of the assembly.

For this tutorial we will make use of the [HADDOCK2.4 webserver](https://wenmr.science.uu.nl/haddock2.4).


A description of the previous major version of our web server [HADDOCK2.2](https://alcazar.science.uu.nl/services/HADDOCK2.2/) can be found in the following publications:

* G.C.P van Zundert, J.P.G.L.M. Rodrigues, M. Trellet, C. Schmitz, P.L. Kastritis, E. Karaca, A.S.J. Melquiond, M. van Dijk, S.J. de Vries and  A.M.J.J. Bonvin.
[The HADDOCK2.2 webserver: User-friendly integrative modeling of biomolecular complexes](https://doi.org/doi:10.1016/j.jmb.2015.09.014).
_J. Mol. Biol._, *428*, 720-725 (2015).

* S.J. de Vries, M. van Dijk and A.M.J.J. Bonvin.
[The HADDOCK web server for data-driven biomolecular docking.](https://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html)
_Nature Protocols_, *5*, 883-897 (2010).  Download the final author version <a href="https://igitur-archive.library.uu.nl/chem/2011-0314-200252/UUindex.html">here</a>.

Further, multi-body docking and the use of symmetry restraints is described in the following paper:

* E. Karaca, A.S.J. Melquiond, S.J. de Vries, P.L. Kastritis and A.M.J.J. Bonvin.
[Building macromolecular assemblies by information-driven docking: Introducing the HADDOCK multi-body docking server.](https://doi.org/doi:10.1074/mcp.M000051-MCP201)
_Mol. Cell. Proteomics_, *9*, 1784-1794 (2010).


Throughout the tutorial, coloured text will be used to refer to questions or
instructions, Linux and/or Pymol commands.

<a class="prompt prompt-question">This is a question prompt: try answering
it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a Pymol prompt: write this in the
Pymol command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the
terminal!</a>

The case we will be investigating is target70 from the CASP-CAPRI experiment, which corresponds to PDB entry [4PWU](https://www.ebi.ac.uk/pdbe/entry/search/index?text:4PWU).


<hr>
## Setup

In order to run this tutorial you will need to have the following software installed:
 ([Pymol][link-pymol] and [ProFit][link-profit]),
and download the data to run this tutorial from our GitHub
data repository [here][link-data] or clone it from the command line

<a class="prompt prompt-cmd">
    git clone https://github.com/haddocking/CASP-CAPRI-T70-tutorial
</a>

Alternatively, if you don't have git installed, simply go the above web address and download the zip archive.
You will also need to compile a few provided programs for post-analysis.
For this go into the ana_scripts directory of the cloned directory and type make
(we are here assuming a tcsh or csh shell):

<a class="prompt prompt-cmd">
cd CASP-CAPRI-T70-tutorial/ana_scripts<BR>
make<BR>
source set-target.csh<BR>
cd ..</a>

And for ```bash```:

<a class="prompt prompt-cmd">
cd CASP-CAPRI-T70-tutorial/ana_scripts<BR>
make<BR>
source set-target.sh<BR>
cd ..</a>


If you don't want to wait with the docking runs to complete in order to proceed with the analysis (see below), you can already download pre-calculated runs using the script provided into the runs directory:

<a class="prompt prompt-cmd">cd runs<BR>./download-run-data-h24.csh<BR>cd ..</a>

This will download two reduced docking runs, one for the dimeric and one for the tetrameric forms of T70 (about 38MB of data).

Or:
<a class="prompt prompt-cmd">cd runs<BR>./download-run-data-full-h24.csh<BR>cd ..</a>

This will download two full docking runs, one for the dimeric and one for the tetrameric forms of T70  (about 800MB of data).


<hr>
## Inspecting the content of the tutorial

Let us first inspect the various files provided with this tutorial.
You will see three directories and one file:

* **HADDOCK-runfiles**: this directory contains the reference HADDOCK parameter files for dimer and tetramer docking. These can be used to reproduce the docking using the file [upload interface](https://wenmr.science.uu.nl/haddock2.4/submit_file) of the HADDOCK server.

* **ana_scripts**: this directory contains various analysis scripts to analyse the results of the docking, including the calculation of the CAPRI i-RMSD and Fnat statistics

* **protein1.pdb**: this is the model we built for this target based on the sequence information that was provided to the CAPRI predictors.

* **runs**: this directory contains a script that allows you to download pre-calculated full docking runs.


<hr>
## Ab-initio, multi-body docking with symmetry restraints


#### Registration / Login

In order to start the submission, either click on "*here*" next to the submission section, or click [here](https://bianca.science.uu.nl/auth/register/). To start the submission process, we are prompted for our login credentials. After successful validation of our credentials we can proceed to the structure upload.

**Note:** The blue bars on the server can be folded/unfolded by clicking on the arrow on the left

#### Submission and validation of structures

We will launch two docking runs, one for the dimeric and one for the tetrameric form of this target.
For this we will make us of the [HADDOCK 2.4 interface](https://wenmr.science.uu.nl/haddock2.4/submit/1) of the HADDOCK web server, where you will need to register as a user and request Expert or Guru level access [here](https://bianca.science.uu.nl/auth/register/).

We will first set up a symmetrical tetramer docking run:

* **Step1:** Define a name for your docking run, e.g. *T70-tetramer*.

* **Step2:** Select the number of molecules you will be using, in this case 4.

* **Step3:** Input the proteins PDB files.

<a class="prompt prompt-info">
First molecule: where is the structure provided? -> "I am submitting it"
</a>
<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select protein1.pdb
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> A
</a>
<a class="prompt prompt-info">
The N-terminus of your protein is positively charged -> Switch off
</a>
<a class="prompt prompt-info">
The C-terminus of your protein is negatively charged -> Switch off
</a>

(Our model might not be the real fragment used for crystallisation - better to have uncharged termini)

* **Steps 4X:** Repeat step 2 to define the other three molecules, using the same input protein file and assigning segment IDs as B,C and D.

* **Step 5:** Click on the "Next" button at the bottom left of the interface. This will upload the structures to the HADDOCK webserver where they will be processed and validated (checked for formatting errors). The server makes use of [Molprobity](http://molprobity.biochem.duke.edu/) to check side-chain conformations, eventually swap them (e.g. for asparagines) and define the protonation state of histidine residues.

#### Definition of restraints




If everything went well, the interface window should have updated itself and it should now show the list of residues for molecules 1 and 2. Since we do not define these residues, click on the "Next" button at the bottom left of the interface.

* **Step 6:** Turn on center-of-mass restraints. For this unfold the **Distance restraints menu** in the **Docking parameters window**

<a class="prompt prompt-info">
Center of mass restraints -> Switch on

* **Step 7:** Since we are doing ab-initio docking we do need to increase the sampling. For this unfold the **Sampling parameters menu**:

<a class="prompt prompt-info">
Number of structures for rigid body docking -> 10000
</a>
<a class="prompt prompt-info">
Number of structures for semi-flexible refinement -> 400
</a>
<a class="prompt prompt-info">
Number of structures for the final refinement -> 400
</a>


**Note:** If you use course credentials, these numbers will be reduced to 500/50/50 to save computing time and get back results faster. You can also manually decrease those numbers and download instead a full pre-calculated run for analysis (see setup above).


* **Step 8:** Define noncrystallographic symmetry restraint to enforce the various chains will have exactly the same conformation. For this unfold the **Noncrystallographic symmetry restraints menu**:

<a class="prompt prompt-info">
Use this type of restraints	 -> Switch on
</a>

Set the number of segment pairs to three: A-B, B-C and C-D.
The protein sequence starts at residue 6 and ends at residue 78. Use those numbers to define the various segments.

<a class="prompt prompt-question">We have four molecules, so do three pairs of NCS restraints make sense to ensure all four molecules remain similar?</a>

* **Step 9:** Define the symmetry restraints to enforce the symmetry of our tetramer. For this unfold the **Symmetry restraints menu**:

<a class="prompt prompt-question">We are dealing with a symmetrical tetramer. Two kind of symmetries are possible: C4 or D2. What are the differences between those two symmetries?</a>

Since we don't know a priori which symmetry the system has, we can define 6 pairs of C2 restraints which are consistent with both C4 and D2. For this we will need to define the following symmetry pairs: A-B, A-C, A-D, B-C, B-D, C-D. In this way the system will be free to adopt one of those two symmetries.

<a class="prompt prompt-info">
Use this type of restraints	 -> switch on
</a>

Use the **C2 symmetry segment pair** menu to define those six pairs of symmetry restraints. Use for defining the segments again residues 6 and 78 as start and end points.

#### Job submission

* **Step 10:** You are ready to submit!  Click on the "Submit" button at the bottom left of the interface.


<hr>
## First visual analysis of the results

Once your run has completed you will be presented with a result page showing the cluster statistics and some graphical representation of the data. Such an example output page can be found [here](https://wenmr.science.uu.nl/haddock2.4/run/4242424242/T70-dimer) for dimer and [here](https://wenmr.science.uu.nl/haddock2.4/run/4242424242/T70-tetramer) for tetramer. You can also quickly visualize a specific structure by clicking on the “eye” icon next to a structure.


The run with reduced number of models (course setting) should be returning only one cluster. Load a representative model and compare it to the crystal structure:

<a class="prompt prompt-linux">
pymol cluster1_1.pdb $WDIR/30_70.2.pdb
</a>

This will load cluster1_1 and the reference crystal structure (the second interface evaluated by CAPRI) into pymol (make sure to have run the setup described above). In case WDIR is not defined or you are not running under a linux-like environment you can find the reference structure into the *ana_scripts* directory.

In pymol you can type the following to superimpose the models and change the style:

<a class="prompt prompt-pymol">
align cluster1_1, 30_70.2<br>
zoom vis<br>
show cartoon<br>
util.cbc
</a>

<a class="prompt prompt-question">
Does the model (or any of the cluster representatives in case of a full run) resemble the reference crystal structure?
</a>
<a class="prompt prompt-question">
In case you found a reasonable prediction, check what was its rank in the server?
</a>


<hr>
## More quantitative analysis of the results

Let's have a more detailed look at the quality and ranking of the generated models. For this we will calculate CAPRI statistics, namely the interface RMSD (i-RMSD) and fraction of native contacts (Fnat) compared to the reference crystal structure. CAPRI has defined the following criteria to assess the quality of a model:

* **Unacceptable**:    i-RMSD >4Å or Fnat < 0.1
* **Acceptable**:      4Å <=i-RMSD < 2Å and Fnat > 0.1
* **Medium**:          2Å <=i-RMSD < 1Å and Fnat > 0.3
* **High**:            i-RMSD < 1Å and Fnat > 0.5

In order to perform the more quantitative analysis, download the full run from the results page (provide in a link in the first line of the result page) and unpack it. Alternatively, download the pre-calculated data from the following links:

* T70 tetramer docking - reduced settings: [link](https://surfdrive.surf.nl/files/index.php/s/jUjk3gbLRkylPo4/download)
* T70 tetramer docking - full sampling: [link](https://surfdrive.surf.nl/files/index.php/s/NQe3VPuPF05iFVY/download)
* T70 dimer docking - reduced settings: [link](https://surfdrive.surf.nl/files/index.php/s/tnT2sZKcpDNmZeP/download)
* T70 dimer docking - full sampling: [link](https://surfdrive.surf.nl/files/index.php/s/t7wIYpuddJqhlFn/download)

Then start the quantitative analysis in the directory where you saved and unpacked the run with the following command:

<a class="prompt prompt-linux">
$WDIR/run_all.csh *my-run-directory*
</a>

**Note**: If you use the pre-calculated runs, this analysis has already been performed and you can skip the above step.


Be patient since this might take some time depending on whether you are analysing a full or reduced run. The script will calculate CAPRI statistics for all generated models (rigid-body (it0) - semi-flexible refinement (it1) - final refinement (water)). Those can be found in the unpacked run directory under `structures/it0`, `structures/it1` and `structures/it1/water` directories, respectively.

Once the analysis script has completed you can get a first glimpse of the number of acceptable models or better using the following command:

<a class="prompt prompt-linux">
$WDIR/check_runs_i-rmsd.csh *my-run-directory*
</a>

Here is an example of what this script will return for a full tetramer docking run:


<pre>
T70-tetramer
  #it0: structures with i-RMSD<4A:       211
  #it0: structures within best400 with i-RMSD<4A:       41
  #it0: structures within best400 with i-RMSD<2A:       41
  #it0: structures within best400 with i-RMSD<1A:        0
  #it1: structures with i-RMSD<4A:        54
  #it1: structures with i-RMSD<2A:        54
  #it1: structures with i-RMSD<1A:         0
  #water: structures with i-RMSD<4A:        54
  #water: structures with i-RMSD<2A:        54
  #water: structures with i-RMSD<1A:         0
</pre>

**Note**: To get the proper stats in case of a reduced sampling run, use instead `check_runs_i-rmsd-reduced.csh`.

<a class="prompt prompt-question">
Are there any acceptable models after the final refinement?
</a>

<a class="prompt prompt-question">
Which fraction of the acceptable models at it0 is selected for further refinement?
</a>

<a class="prompt prompt-question">
Considering that we are generating 10000 models for a full run at it0, how successful was our scoring function in selecting acceptable models for further flexible refinement?
</a>

You can also check the cluster-based statistics with the following command:

<a class="prompt prompt-linux">
$WDIR/check_clusterranks.csh *my-run-directory*
</a>

Here is an example of what this script will return for a full tetramer docking run:

<pre>
######################################################

  HADDOCK scoring water
______________________________________________________
=========== T70-tetramer =============
Rank of clusters with i-RMSD<4A:
   1 clust5    1.33 +/-  0.03  Fnat=  0.57 +/-  0.02
   4 clust12   1.31 +/-  0.06  Fnat=  0.61 +/-  0.05
######################################################

  HADDOCK scoring it1
______________________________________________________
=========== T70-tetramer =============
Rank of clusters with i-RMSD<4A:
  14 clust11   1.33 +/-  0.03  Fnat=  0.58 +/-  0.01
</pre>

<a class="prompt prompt-question">
The above results show three clusters with medium quality (around 1.3Å i-RMSD). What could be the reason that these do not fall within one single cluster? Remember here that we are docking four molecules with different chainIDs.
</a>

<a class="prompt prompt-question">
Check also the ranking of the clusters. Did the HADDOCK score do a good job are ranking at the top acceptable clusters?
</a>

In case there is no single acceptable cluster, but the `check_runs_i-rmasd.csh` script did report some acceptable models at the final refinement, do check the ranking of those single structure. For this go into the *my-docking-run*`/structures/it1/water` directory and inspect the `i-RMSD.dat` file. This file contains the i-RMSD values sorted according to the HADDOCK score.

<a class="prompt prompt-linux">
cd *my-docking-run*/structures/it1/water<br>
less i-RMSD.dat
</a>

<a class="prompt prompt-question">
Did HADDOCK rank any acceptable model at the top? If not, try to find out what is the rank of the first acceptable model.
</a>

You can also inspect the fraction of native contacts of the models by looking at the `file.nam_fnat` file.

Let's inspect the best generated model in terms of i-RMSDs. This is the top model listed in `i-RMSD-sorted.dat`. Upload it in pymol (or your favourite graphical program) and compare it to the crystal structure:

<a class="prompt prompt-linux">
pymol *my-best-model* $WDIR/30_70.2.pdb
</a>

And in pymol:

<a class="prompt prompt-pymol">
align *my-best-model*, 30_70.2<br>
zoom vis<br>
show cartoon<br>
util.cbc
</a>

The above align command might not show a convincing superimposition because different chains might be forming the correct interface. If this is the case, pymol provide another command to perform a better structural alignment:

<a class="prompt prompt-pymol">
cealign *my-best-model*, 30_70.2<br>
</a>


<hr>
## Comparing dimer and tetramer docking

You can follow the same steps described above to perform instead of a tetramer docking a dimer docking. Simply follow the provided instructions, but inputting to the HADDOCK server only two molecules.

Repeat the analysis of the results and compare the success with tetramer docking.

<a class="prompt prompt-question">
Is dimer docking as successful as tetramer docking?
</a>



<hr>
## Congratulations!

You have completed this tutorial. If you have any questions or
suggestions, feel free to contact us via email or by submitting an issue in the
appropriate [Github repository](https://github.com/haddocking/CASP-CAPRI-T70-tutorial) or asking a question through our [support center](https://ask.bioexcel.eu).

[link-profit]: http://www.bioinf.org.uk/software/profit "ProFit"
[link-pymol]: https://www.pymol.org/ "Pymol"
[link-data]: https://github.com/haddocking/CASP-CAPRI-T70-tutorial "CASP-CAPRI tutorial data"
