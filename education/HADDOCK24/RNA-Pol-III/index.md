---
layout: page
title: "Integrative modelling of the apo RNA-Polymerase-III complex from MS cross-linking and cryo-EM data"
excerpt: "A tutorial demonstrating the use of MS crosslinks and low resolution cryo-EM data to build a complex molecular machine."
tags: [MS, Cross-links, cryo-EM, Interaction, HADDOCK, DISVIS, PowerFit, RNA Polymerase, Pymol, Chimera, Visualisation]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}



<hr>
## Introduction

This tutorial will demonstrate the use of our DISVIS, POWERFIT and HADDOCK web servers for predicting the structure of a large biomolecular assembly from MS cross-linking data and low resolution cryo-EM data.
The case we will be investigating is the apo form of the Saccharomyces Cerevisiae RNA Polymerase-III (Pol III). Pol III is a 17-subunit enzyme that transcribes tRNA genes. Its architecture can be subdivided into a core, stalk, heterodimer, and heterotrimer of C82, C34, and C31 subunits.
<ul>
<figure align="center">
  <img src="/education/HADDOCK24/RNA-Pol-III/Pol-III-architecture.png">
</figure>
<b>Figure 1:</b> Pol III subunits are shown as rectangular bars except for C160 and C128, which are shown as ovals for the sake of clarity. Inter-links are shown as lines connecting the protein bars, while intra-links are shown as curves. Inter-links to C31 are colored yellow, to C34 - gold, to C37 – violet, to C53 - cyan. The remaining inter-links are colored gray. Domains of C82 and C34 discussed in this work are explicitely represented. Regions missing in crystal structures or homology models are colored in black. The figure was created with xiNET. Figure reproduced from <a href="https://www.nature.com/articles/nmeth.3838" target="_blank">Ferber et al, 2016</a>.
<br>
<br>
</ul>

During this tutorial, we pretend that the structure of the Pol 3 core (14 subunits) is known and thus we will focus on modeling the positioning of the C82/C34/C31 heterotrimer subunits relatively to the others (which we will treat as the core of Pol III). The structure of Pol III core is quite well characterized, with multiple cryo-EM structures of Pol III published.

We will be making use of i) our [DISVIS server](https://bianca.science.uu.nl/disvis/){:target="_blank"} to analyse the cross-links and detect possible false positives and ii) of the new [HADDOCK2.4 webserver](https://bianca.science.uu.nl/haddock2.4){:target="_blank"} to setup docking runs, using the new coarse-graining option to speed up the calculations (especially needed due to the large size of the system). 
As an alternative strategy, we will use our [PowerFIt server][link-powerfit-web] to fit the largest components of the complex into the 9Å cryo-EM map and then use those as starting point for the modelling of the remaining components.

A description of our the previous version of our web server [HADDOCK2.2](https://haddock.science.uu.nl/services/HADDOCK2.2/){:target="_blank"} can be found in the following publications:

* G.C.P van Zundert, J.P.G.L.M. Rodrigues, M. Trellet, C. Schmitz, P.L. Kastritis, E. Karaca, A.S.J. Melquiond, M. van Dijk, S.J. de Vries and  A.M.J.J. Bonvin.
[The HADDOCK2.2 webserver: User-friendly integrative modeling of biomolecular complexes](https://doi.org/doi:10.1016/j.jmb.2015.09.014){:target="_blank"}.
_J. Mol. Biol._, *428*, 720-725 (2015).

* S.J. de Vries, M. van Dijk and A.M.J.J. Bonvin.
[The HADDOCK web server for data-driven biomolecular docking.](http://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html){:target="_blank"}
_Nature Protocols_, *5*, 883-897 (2010).

Throughout the tutorial, colored text will be used to refer to questions or
instructions, and/or PyMOL commands.

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>


<hr>
## Setup/Requirements


In order to follow this tutorial you will need a **web browser**, a **text editor**, [**PyMOL**][link-pymol]{:target="_blank"} and [**Chimera**][link-chimera]{:target="_blank"}
(both freely available for most operating systems) to visualize the input and output data. 
We used our [**pdb-tools**](https://github.com/haddocking/pdb-tools){:target="_blank"} to pre-process PDB files for HADDOCK, 
renumbering the core domains to avoid overlap in their residue numbering.
Ready to dock models are provided as part of the material for this tutorial. 
The required data to run this tutorial should be downloaded from [**here**](/education/HADDOCK24/RNA-Pol-III/RNA-Pol-III.zip){:target="_blank"}.
Once downloaded, make sure to unpack/unzip the archive (for Windows system you can install the [7-zip](https://www.7-zip.org){:target="_blank"} software if needed to unpack tar archives).

Also, if not provided with special workshop credentials to use the HADDOCK portal, make sure to register in order to be able to submit jobs. Use for this the following registration page: [https://bianca.science.uu.nl/auth/register/haddock](https://bianca.science.uu.nl/auth/register/haddock){:target="_blank"}.

<hr><hr>
## HADDOCK general concepts

HADDOCK (see [http://www.bonvinlab.org/software/haddock2.2](http://www.bonvinlab.org/software/haddock2.2){:target="_blank"}) is a collection of python scripts derived from ARIA ([http://aria.pasteur.fr](http://aria.pasteur.fr){:target="_blank"}) that harness the
power of CNS (Crystallography and NMR System, [http://cns-online.org](http://cns-online.org){:target="_blank"}) for structure
calculation of molecular complexes. What distinguishes HADDOCK from other docking software is its ability, inherited
from CNS, to incorporate experimental data as restraints and use these to guide the docking process alongside
traditional energetics and shape complementarity. Moreover, the intimate coupling with CNS endows HADDOCK with the
ability to actually produce models of sufficient quality to be archived in the Protein Data Bank.

A central aspect to HADDOCK is the definition of Ambiguous Interaction Restraints or AIRs. These allow the translation
of raw data such as NMR chemical shift perturbation or mutagenesis experiments into distance restraints that are
incorporated in the energy function used in the calculations. AIRs are defined through a list of residues that fall
under two categories: active and passive. Generally, active residues are those of central importance for the
interaction, such as residues whose knockouts abolish the interaction or those where the chemical shift perturbation is
higher. Throughout the simulation, these active residues are restrained to be part of the interface, if possible,
otherwise incurring in a scoring penalty. Passive residues are those that contribute for the interaction, but are
deemed of less importance. If such a residue does not belong in the interface there is no scoring penalty. Hence, a
careful selection of which residues are active and which are passive is critical for the success of the docking.

The docking protocol of HADDOCK was designed so that the molecules experience varying degrees of flexibility and
different chemical environments, and it can be divided in three different stages, each with a defined goal and
characteristics:

* **1. Randomization of orientations and rigid-body minimization (it0)** <BR>
In this initial stage, the interacting partners are treated as rigid bodies, meaning that all geometrical parameters
such as bonds lengths, bond angles, and dihedral angles are frozen. The partners are separated in space and rotated
randomly about their centers of mass. This is followed by a rigid body energy minimization step, where the partners are
allowed to rotate and translate to optimize the interaction.
The role of AIRs in this stage is of particular importance. Since they are included in the energy function being
minimized, the resulting complexes will be biased towards them. For example, defining a very strict set of AIRs leads
to a very narrow sampling of the conformational space, meaning that the generated poses will be very similar.
Conversely, very sparse restraints (e.g. the entire surface of a partner) will result in very different solutions,
displaying greater variability in the region of binding.

* **2. Semi-flexible simulated annealing in torsion angle space (it1)** <BR>
The second stage of the docking protocol introduces flexibility to the interacting partners through a three-step
molecular dynamics-based refinement in order to optimize interface packing. It is worth noting that flexibility in
torsion angle space means that bond lengths and angles are still frozen. The interacting partners are first kept rigid
and only their orientations are optimized. Flexibility is then introduced in the interface, which is automatically
defined based on an analysis of intermolecular contacts within a 5A cut-off. This allows different binding poses coming
from it0 to have different flexible regions defined. Residues belonging to this interface region are then allowed to
move their side-chains in a second refinement step. Finally, both backbone and side-chains of the flexible interface
are granted freedom.
The AIRs again play an important role at this stage since they might drive conformational changes.

* **3. Refinement in Cartesian space with explicit solvent (water)** <BR>
The final stage of the docking protocol allows to immerse the complex in a solvent shell to improve the energetics of the
interaction. HADDOCK currently supports water (TIP3P model) and DMSO environments. The latter can be used as a membrane
mimic. In this short explicit solvent refinement the models are subjected to a short molecular dynamics simulation at
300K, with position restraints on the non-interface heavy atoms. These restraints are later relaxed to allow all side
chains to be optimized. In the 2.4 version of HADDOCK, the explicit solvent refinement is replaced by default by a simple 
energy minimisation as benchmarking has shown it does not add much to the quality of the models. This allows to save time.

The performance of this protocol depends on the number of models generated at each step. Few models are less
probable to capture the correct binding pose, while an exaggerated number will become computationally unreasonable. The
standard HADDOCK protocol generates 1000 models in the rigid body minimization stage, and then refines the best 200 
(ranked based on the HADDOCK score) in both it1 and water. Note, however, that while 1000 models are generated by default
in it0, they are the result of five minimization trials and for each of these the 180 degrees symmetrical solution is also
sampled. Effectively, the 1000 models written to disk are thus the results of the sampling of 10.000 docking solutions.

The final models are automatically clustered based on a specific similarity measure - either the *positional interface
ligand RMSD* (iL-RMSD) that captures conformational changes about the interface by fitting on the interface of the
receptor (the first molecule) and calculating the RMSDs on the interface of the smaller partner, or the *fraction of
common contacts* (current default) that measures the similarity of the intermolecular contacts. For RMSD clustering,
the interface used in the calculation is automatically defined based on an analysis of all contacts made in all models.

The new 2.4 version of HADDOCK also allows to coarse grain the system, which effectively reduces the number of 
particles and speeds up the computations. We are using for this the [MARTINI2.2 force field](https://doi.org/10.1021/ct300646g){:target="_blank"}, 
which is based on a four-to-one mapping of atoms on coarse-grained beads.

<hr><hr>
## The information at hand

Let us first inspect the available data, namely the various structures (or homology models) as well as
the information from MS we have at hand to guide the docking. After unpacking the archive provided for this tutorial (see [Setup](#setuprequirements) above),
you should see a directory called `RNA-Pol-III` with the following subdirectories in it:

  * __cryo-EM__: This directory contains a 9Å cryo-EM map of the RNA Pol III.
  
  * __disvis__: This directory contains text files called `xlinks-all-X-Y.disvis` describing the cross-links between the various domains (X and Y).
These files are in the format required to run DISVIS. The directory also containts the results of DISVIS analysis of the various domain pairs as directories named `disvis-results-X-Y`

  * __docking__: This directory contains json files containing all the parameters and input data for HADDOCK. Those are reference files of the docking setup and allow to repeat the modelling using the `Submit File` option of the HADDOCK2.4 web server:
    * `run-PolIII-C82-C34-C31model-xlinks.json`: Docking following the 1st scenario described in this tutorial
    * `run-PolIII-C82-C34-C31dummyLYS-xlinks.json`: Docking following the 1st scenario, but using dummy lysines for the C31 domain
    * `run-PolIII-core-C82-EMfit-C34-C31-xlinks.json`: Docking following the 2nd scenario described in this tutorial
    * `run-PolIII-core-C82-EMfit-C34-C31dummyLYS-xlinks.json`: Docking following the 2nd scenario described in this tutorial, but using dummy lysines for the C31 domain
    * `run-PolIII-core-C82-refine.json`: Refinement of the core and C82 models fitted into the cryo-EM map with PowerFit
    
  * __input-pdbs__: This directory contains the HADDOCK-ready input PDB files for the various domains
    * `A_5fja-core.pdb`: The core region of Pol III with non-overlapping residue numbering (named as chain A)
    * `B_C82-2XUBA.pdb`: The C82 structure, homology modelled on PDB entry 2XUB excluding the disordered long loops (named as chain B)
    * `C_C34_wHTH1-2DK8A.pdb`: The first helix-turn-helix domain of C34, homology modelled on PDB entry 2DK8-chainA (named as chain C)
    * `D_C34_wHTH2-2DK8A.pdb`: The second helix-turn-helix domain of C34, homology modelled on PDB entry 2DK8-chainA (named as chain D)
    * `E_C34_wHTH3-1KDDA.pdb`: The third helix-turn-helix domain of C34, homology modelled on PDB entry 1KDD-chainA (named as chain E)
    * `F_C31_iTasser.pdb`: A de novo model from I-TASSER, conformation very uncertain (named as chain F)    
    * `F_C31_LYS91.pdb`: Lysine 91 from C31 (named as chain F) - for use instead of the iTasser model
    * `F_C31_LYS111.pdb`: Lysine 111 from C31 (named as chain G) - for use instead of the iTasser model

  * __restraints__:
    * `xlink-all-inter.tbl`: This file contains all cross-links between the various domains (using the full C31 model)
    * `xlink-all-inter-disvis-filtered.tbl`: This file contains the disvis-filtered cross-links between the various domains (using the full C31 model)
    * `xlinks-all-inter-disvis-filtered-C31dummyLYS.tbl`: This file contains the disvis-filtered cross-links between the various domains (using the C31 single Lysines as dummies)
    * `C34-connectivity.tbl`: Connectivity restraints between the two C34 domains
    * `C31-Lys91-Lys111.tbl`: Connectivity restraints between the two lysines of C31 for docking using those as dummies
    * `C31-C34-connectivities.tbl`: The combination of the two previous files

From MS, we have experimentally determined cross-links between the various domains. We have only kept  here  the inter-domain cross-links relevant for  this tutorial.
The cross-links are taken from ([Ferber et al. 2016](https://www.nature.com/articles/nmeth.3838){:target="_blank"}. These are the files present in the `disvis` directory. As an example here
are the cross-links identified between the Pol III core (chain A here) and C31 (chain F):

<pre style="background-color:#DAE4E7">
A  143 CB F 179 CB 0.0 30.0
A 1458 CB F 111 CB 0.0 30.0
A 1458 CB F  91 CB 0.0 30.0
A  166 CB F 196 CB 0.0 30.0
A  189 CB F 199 CB 0.0 30.0
A 3402 CB F  91 CB 0.0 30.0
A 3514 CB F 111 CB 0.0 30.0
A 4206 CB F  91 CB 0.0 30.0
A 4359 CB F  91 CB 0.0 30.0
A 4361 CB F  91 CB 0.0 30.0
</pre>

This is the format used by DisVis to represent the cross-links. Each cross-link definition consists of eight fields:

* chainID of the 1st molecule
* residue number
* atom name
* chainID of the 2nd molecule
* residue number
* atom name
* lower distance limit
* upper distance limit


<hr><hr>
## Using DISVIS to visualize the interaction space and filter false positive restraints


### Introduction to DISVIS

DisVis is a software developed in our lab to visualise and quantify the information content of distance restraints
between macromolecular complexes. It is open-source and available for download from our [Github repository][link-disvis]{:target="_blank"}.
To facilitate its use, we have developed a [web portal][link-disvis-web]{:target="_blank"} for it.

DisVis performs a full and systematic 6 dimensional search of the three translational and rotational degrees of freedom to
determine the number of complexes consistent with the restraints. It outputs information about the inconsistent/violated
restraints and a density map that represents the center-of-mass position of the scanning chain consistent with a given
number of restraints at every position in space.

DisVis requires three input files: atomic structures of the biomolecules to be analysed and a text file containing the list of distance restraints between the two molecules .
This is also the minimal required input for the web server to setup a run.  

DisVis and  its webserver are described in:

* G.C.P. van Zundert, M. Trellet, J. Schaarschmidt, Z. Kurkcuoglu, M. David, M. Verlato, A. Rosato and A.M.J.J. Bonvin.
[The DisVis and PowerFit web servers: Explorative and Integrative Modeling of Biomolecular Complexes.](https://doi.org/10.1016/j.jmb.2016.11.032){:target="_blank"}.
_J. Mol. Biol._. *429(3)*, 399-407 (2016).

* G.C.P van Zundert and A.M.J.J. Bonvin.
[DisVis: Quantifying and visualizing accessible interaction space of distance-restrained biomolecular complexes](https://doi.org/doi:10.1093/bioinformatics/btv333){:target="_blank"}.
  _Bioinformatics_ *31*, 3222-3224 (2015).

<hr>
### Analysing the Pol III domain-domain interactions with DISVIS

Before modelling Pol III, we will first run DisVis using the cross-links for the various pairs of domains to both 
assess the information content of the cross-links and detect possible false positives. For the latter, please note that DisVis does not account for
conformational changes. As such, a cross-link flagged as possible false positive might also simply reflect a conformational change occuring upon binding.

We have cross-links available for 8 pairs of domains (see the `disvis` directory from the downloaded data). As an illustration of running DisVis, we will here
setup the analysis for the Pol III core (chain A) - C31 (chain F) pair.

To run DisVis, go to

<a class="prompt prompt-info" href="https://bianca.science.uu.nl/disvis" target="_blank">https://bianca.science.uu.nl/disvis</a>

On this page, you will find the most relevant information about the server, as well as the links to the local and grid versions of the portal's submission page.

#### Step1: Register to the server (if needed) or login

[Register][link-disvis-register]{:target="_blank"} for getting access to the web server (or use the credentials provided in case of a workshop).

You can click on the "**Register**" menu from any DisVis page and fill the required information.
Registration is not automatic but is usually processed within 12h, so be patient.

If you already have credential, simply login in the upper right corner of the [disvis input form][link-disvis-submit]{:target="_blank"}


#### Step2: Define the input files and parameters and submit

Click on the "**Submit**" menu to access the [input form][link-disvis-submit]{:target="_blank"}.

<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/disvis-submission.png">
</figure>

From the `input-pdbs` directory select:
<a class="prompt prompt-info">Fixed chain → A_5fja-core.pdb</a>
<a class="prompt prompt-info">Scanning chain → F_C31_model.pdb</a>
From the `disvis` directory select:
<a class="prompt prompt-info">Restraints file → xlinks-all-A-F.disvis</a>

Once the fields have been filled in, you can submit your job to our server
by clicking on "**Submit**" at the bottom of the page.

If the input fields have been correctly filled you should be redirected to a status page displaying a message
indicating that your run has been successfully submitted.
While performing the search, the DisVis web server will update you on the progress of the
job by reloading the status page every 30 seconds.
The runtime of this example case is less than 5 minutes on our local CPU and grid GPU servers. 
However the load of the server as well as pre- and post-processing steps might substantially increase the waiting time.

If you want to learn more about the meaning of the various parameters, you can go to:

<a class="prompt prompt-info" href="https://bianca.science.uu.nl/disvis" target="_blank">https://bianca.science.uu.nl/disvis</a>

Then click on the "**Help/Manual**" menu.

The rotational sampling interval option is in
degrees and defines how tightly the three rotational degrees of freedom will be
sampled. Voxel spacing is the size of the grid's voxels that will be cross-correlated during the 3D translational search.
Lower values of both parameters will cause DisVis to perform a finer search, at the
expense of increased computational time. The default values are `15°` and `2.0Å` for a quick scanning and `9.72°` and `1.0Å`
for a more thorough scanning.
For the sake of time, in this tutorial we will keep the sampling interval as the quick scanning settings (`15.00°` and `2.0Å`).
The number of processors used for the calculation is fixed to 8 processors on the web server side.
This number can of course be changed when using the local version of DisVis.

<hr>
#### Analysing the results

Once your job has completed, and provided that you did not close the status page, you will be automatically redirected to the results
page (you will also receive an email notification).

If you don't want to wait for your run to complete, you can access the pre-calculated results [here](https://bianca.science.uu.nl/disvis/tutorial/3){:target="_blank"}.

The results page presents a summary split into several sections:

* `Status`: In this section you will find a link from which you can download the output data as well as some information
about how to cite the use of the portal.
* `Accessible Interaction Space`: Here, images of the fixed chain together with the accessible interaction space (in
a density map representation) are displayed. Different views of the molecular scene can be chosen by clicking
 on the right or left part of the image frame. Each view shows the accessible space consistent with the selected number of restraints (using the slider below the picture).
* `Accessible Complexes`: Summary of the statistics for the number of complexes consistent with at least N number of restraints.
 The statistics are displayed for the N levels, N being the total number of restraints provided in the restraints file (here `restraints.txt`)
* `z-Score`: For each restraint provided as input, a z-Score is calculated, indicating the likelihood that a restraint is a false positive.
The higher the score, the more likely it is that a restraint is a false positive. Putative false positive restraints
are only highlighted if no single solution was found to be consistent with the total number of restraints provided. If DisVis
finds complexes consistent with all restraints, the z-Scores are still displayed, but in this case they should be ignored.
* `Violations`: The table in this sections shows how often a specific restraint is violated for all models consistent with
a given number of restraints. The higher the violation fraction of a specific restraint, the more likely it is to be a false positive.
Column 1 shows the number of restraints N considered, while each following column indicates the violation fractions of
a specific restraint for complexes consistent with at least N restraints. Each row thus represents the fraction of all
complexes consistent with at least N restraints that violated a particular restraint. As for the z-Scores, if solutions are found 
that are consistent with all restraints provided, this table should be ignored.

<a class="prompt prompt-question"> Using the different descriptions of the sections we provided above together with the results of your run, 
which ones are the likely false positive restraints according to DisVis?</a>

As mentioned above, the two last sections feature a table that highlights putative false positive restraints based on
their z-Score and their violation frequency for a specific number of restraints. We will naturally look for the
crosslinks with the highest number of violations. The DisVis web server preformats the results in a way that false positive restraints
are highlighted and can be spotted at a glance.

In our case, you should observe that DisVis found solutions consistent with up to 8 restraints indicating that there might be two false positive restraints.
Taking a closer look at the violations table might already be enough to determine which residues are most likely true false positives.
In this example, two restraints are violated in all complexes that are consistent with 8 restraints. These are thus the most likely candidates:

<details style="background-color:#DAE4E7"><summary><b>See solution:</b>
</summary>
<center><b>A166(CB)-F196(CB)</b></center>
<center><b>A189(CB)-F199(CB)</b></center>
</details>
<br>
<br>
When DisVis fails to identify complexes consistent with all provided restraints during quick scanning, it is advisable to rerun with the complete scanning parameters before removing all restraints (or removing only the most violated ones and rerunning with complete scanning). It is possible that a more thourough sampling of the interaction space will yield complexes consistent with all restraints or at least reduce the list of putative false positive restraints.  

<hr>
#### DisVis output files

It is difficult to appreciate the accessible interaction space between the two partners with static images only.
Therefore you should download the results archive to your computer (which is available at the top of your results page).
You will find in the archive the following files:

* `accessible_complexes.out`: A text file containing the number of complexes consistent with a number of restraints.
* `accessible_interaction_space.mrc`: A density file in MRC format. The density represents the space where the center of mass of the
scanning chain can be placed while satisfying the consistent restraints.
* `violations.out`: A text file showing how often a specific restraint is violated for each number of consistent restraints.
* `z-score.out`: A text file giving the z-score for each restraint. The higher the score, the more likely the restraint
is a false positive.
* `run_parameters.json`: A text file containing the parameters of your run.

_Note_: Results for the different pair combinations are available from the tutorial data directory in the `disvis` directory as `disvis-results-X-Y`.

Let us now inspect the solutions and visualise the interaction space in Chimera:

<a class="prompt prompt-info">
  Open the *fixed_chain.pdb* file and the *accessible_interaction_space.mrc* density map in Chimera.
</a>

<a class="prompt prompt-info">
  UCSF Chimera Menu → File → Open... → Select the file
</a>

Or from the Linux command line:

<a class="prompt prompt-linux">
chimera fixed_chain.pdb accessible_interaction_space.mrc
</a>

The values of the `accessible_interaction_space.mrc` slider bar correspond to the number of satisfied restraints (N).
In this way, you can selectively visualise regions where complexes have been found to be consistent with a given number of
restraints. Try to change the level in the "**Volume Viewer**" to see how the addition of restraints reduces
the accessible interaction space. 

_Note_: The interaction space displayed corresponds to the region of space where the center of mass 
        of the scanning molecule can be placed while satisfying a given number of restraints


<hr>
### Converting DISVIS restraints into HADDOCK restraints

In principle you should repeat the DisVis analysis for all pairs to detect possible false positives. 
We are however providing the files that have already been filtered for possible false positive cross-links.
Try to figure out how many cross-links were removed by comparing the following two files in the `disvis` directory:

 * `xlinks-all-inter.txt`
 * `xlinks-all-inter-disvis-filtered.txt`

This can be easily done at the Linux level with:

<a class="prompt prompt-linux">
diff xlinks-all-inter.disvis xlinks-all-inter-disvis-filtered.disvis
</a>

<a class="prompt prompt-question">
  How many restraints have been removed as false positive for the entire system? And between which domains?
</a>

<details style="background-color:#DAE4E7"><summary><b>See solution:</b>
</summary>
Next to the two cross-links between domains A and F that we already identified from our DisVis analysis, one additional one was removed:
B322(CB)-F179(CB)
</details>
<br>

Before setting up the docking, we need to generate the distance restraint file for the cross-links in a format suitable for HADDOCK.
HADDOCK uses [CNS][link-cns] as its computational engine. A description of the format for the various restraint types supported by HADDOCK can
be found in our [Nature Protocols](http://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html){:target="_blank"} paper, Box 4.

Distance restraints are defined as:

<pre>
assi (selection1) (selection2) distance, lower-bound correction, upper-bound correction
</pre>

The lower limit for the distance is calculated as: distance minus lower-bound correction
and the upper limit as: distance plus upper-bound correction

The syntax for the selections can combine information about chainID - `segid` keyword -, residue number - `resid`
keyword -, atom name - `name` keyword.
Other keywords can be used in various combinations of OR and AND statements. Please refer for that to the [online CNS manual][link-cns].

As an example, a distance restraint between the CB carbons of residues 10 and 200 in chains A and B with an
allowed distance range between 10 and 20Å can be defined as:

<pre>
assi (segid A and resid 10 and name CB) (segid B and resid 200 and name CB) 20.0 10.0 0.0
</pre>

<a class="prompt prompt-question">
Can you think of a different way of defining the target distance and its lower and upper corrections while maintaining the same
allowed range?
</a>


Under Linux (or OSX), this file can be generated automatically from the `xlinks-all-inter-disvis-filtered.disvis`
file provided with the data for this tutorial by giving the following command (one line) in a terminal window:

<a class="prompt prompt-linux">
cat xlinks-all-inter-disvis-filtered.disvis| awk '{if (NF == 8) {print "assi (segid ",$1," and resid ",$2," and name ",$3,") (segid ",$4," and resid ",$5," and name ",$6,") ",$8,$8,$7}}' > xlinks-all-inter-disvis-filtered.tbl
</a>

The correspondong pre-generated CNS/HADDOCK formatted restraints files are provided in the `restraints` directory as:

  * `xlinks-all-inter.tbl`
  * `xlinks-all-inter-disvis-filtered.tbl`
  * `xlinks-all-inter-disvis-filtered-C31dummyLYS.tbl` (for use with the dummy Lysines of C31)
  
Inspect the `xlinks-all-inter-disvis-filtered.tbl` file (open it as a text file)

<a class="prompt prompt-question">
We used CB atoms to define the restraints in the disvis restraint file. Can you find those is this file?
Are there other atoms defined? What could those be? (Hint... MARTINI)
</a>

<details style="background-color:#DAE4E7"><summary><b>See solution:</b>
</summary>
Additional atoms are included in the distance restraints definitions: SC* . These correspond to the side-chain atom names in the MARTINI representation.
</details>
<br>

In the restraints directory provided, there are additional restraint file provided, e.g.: `C34-connectivity.tbl`.
Inspect its content.

<a class="prompt prompt-question">
What are those restraints for?
</a>

<details style="background-color:#DAE4E7"><summary><b>See solution:</b>
</summary>
C34 consists of three helix-turn-helix domains which have been modelled separately. They are connected by flexible linkers for which no structure is available.
The defined restraints impose upper limits to the distance between the C- and N-terminal domains of the the domains. The upper limit was estimated as the number of missing segments/residues * 4.5Å (a typical distance observed in diffraction data for amyloid fibrils, representing a CA-CA distance in an extended conformation).
</details>
<br>

_Note_: You should notice that the restraints are duplicated (actually 4 times). This is a way to tell HADDOCK to give more weight to those restraints.



<hr><hr>
## Strategy 1): Modelling the complex by docking with cross-links only

We only have cross-links for two of the three C34 domains. We will therefore not include C34_wHTH3 into the modelling.
Further, we have the choice to trust or not the C31 iTasser model. Docking with unreliable models might do more harm than good.
But excluding completely C31 would mean loosing information coming from the cross-links between C31 and the other domains.

An alternative solution would be to include only separate Lysine residues to which cross-links are defined. In this case, there
are two lysines with multiple cross-links each: Lys91 and Lys111. Instead of using the full C31 model we can include those two lysines,
each being defined as a separate molecule (see [alternative runs](#alternative-runs) below).

Here will set up a five-body docking using the PolIII-core, C82, C34_wHTH1, C34_wHTH2 and the iTasser C31 structures/models:

* 1st molecule - chainA: PolIII-core
* 2nd molecule - chainB: C82 homology model
* 3rd molecule - chainC: C34 wHTH1 domain homology model
* 4th molecule - chainD: C34 wHTH2 domain homology model
* 5th molecule - chainF: C31 iTasser model

_Note_: ChainE is reserved for the 3rd C34 wHTH domain (not used here since no cross-links defining its position).


<hr>
### Setting up the docking with cross-links using the full C31

#### Registration / Login

To start the submission, click [here](https://bianca.science.uu.nl/haddock2.4/submit/1){:target="_blank"}. You will be prompted for our login credentials. 
After successful validation of your credentials you can proceed to the structure upload.
If running this tutorial in the context of a course/workshop, you will be provided with course credentials.

**Note:** The blue bars on the server can be folded/unfolded by clicking on the arrow on the left.

#### Submission and validation of structures

We will make us of the [HADDOCK2.4 interface](https://bianca.science.uu.nl/haddock2.4/submit/1){:target="_blank"} of the HADDOCK web server.

* **Step 1:** Define a name for your docking run, e.g. *PolIII-C82-C34-C31model-xlinks*.

* **Step 2:** Define the number of components, i.e. *5*.

* **Step 3:** Input the first protein PDB file. For this unfold the **Molecule 1 input menu**.

<a class="prompt prompt-info">
First molecule: where is the structure provided? -> "I am submitting it"
</a>
<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *A_PolIII-5fja-core.pdb*
</a>
<a class="prompt prompt-info">
Do you want to coarse-grain your molecule? -> turn on
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> A
</a>

* **Step 4:** Input the second protein PDB files.

<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *B_C82-2XUBA.pdb*
</a>
Since we do not allow to mix all-atom and coarse grained models, the option to coarse grain this molecule is already turned on.
<a class="prompt prompt-info">
Segment ID to use during docking -> B
</a>

* **Step 5:** Input the third protein PDB files.

<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *C_C34_wHTH1-2DK8A.pdb*
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> C
</a>

* **Step 6:** Input the fourth protein PDB files.

<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *D_C34_wHTH2-2DK8A.pdb*
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> D
</a>

* **Step 7:** Input the fifth protein PDB files.

<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *F_C31_iTasser.pdb*
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> F
</a>

===> _Make sure to change the Segmend ID to F otherwise the restraints for C31 won't be used!_ <===


* **Step 8:** Click on the "Next" button at the bottom left of the interface. This will upload the structures to the HADDOCK webserver where they will be processed and validated (checked for formatting errors). The server makes use of [Molprobity](http://molprobity.biochem.duke.edu/){:target="_blank"} to check side-chain conformations, eventually swap them (e.g. for asparagines) and define the protonation state of histidine residues.


#### Definition of restraints

If everything went well, the interface window should have updated itself and it should show the list of residues for molecules 1 and 2.

* **Step 9:** Instead of specifying active and passive residues, we will supply restraint files to HADDOCK. 
No further action is required in this page, so click on the "Next" button at the bottom of the **Input parameters** window, 
which proceeds to the  **Distance Restraint** menu  of the **Docking Parameters** window.

* **Step 10:** Upload the cross-link restraints file to the ambiguous restraints category

<a class="prompt prompt-info">
Instead of specifying active and passive residues, you can supply a HADDOCK restraints TBL file (ambiguous restraints) -> Browse and select *xlinks-all-inter-disvis-filtered.tbl*
</a>

**Note:** Although the name points to ambiguous restraints, any type of distance restraints can be uploaded here. The only thing to remember
          is that by default 50% of the ambiguous restraints will be randomly discarded for each docking model generated. This option can be
          turned off -something we will do below since we have a limited amount of cross-links and already checked them with DisVis.

* **Step 11:** Upload the C34 connectivity restraints file to the unambiguous restraints category

<a class="prompt prompt-info">
You can supply a HADDOCK restraints TBL file with restraints that will always be enforced (unambiguous restraints) -> Browse and select *C34-connectivities.tbl*
</a>

* **Step 12:** Turn off random removal of restraints

<a class="prompt prompt-info">
Randomly exclude a fraction of the ambiguous restraints (AIRs) -> Turn off
</a>

#### Other docking settings and job submission

In  the same page as where restraints are provided you can modify a large number of docking settings.

* **Step 13:** Unfold the **sampling parameters** menu.

Here you can change the number of models that will be calculated, the default being 1000/200/200 for the three stages of HADDOCK (see [HADDOCK General Concepts](#haddock-general-concepts). When docking multiple subunits it is recommended to increase the sampling, e.g. to 10000/400/400 (at the cost of longer computations). For this tutorial we might use 2000/400/400 (but if you are using course accounts, this will be automatically downsampled to 250/50/50). 


When docking only with  interface information (i.e. no specific distances), we are systematically sampling the 180 degrees rotated solutions for each interface, minimizing the rotated solution and keeping the best of the two in terms of HADDOCK score. Since here we are using rather specific distance restraints, we can turn off this option to save time.

<a class="prompt prompt-info">
Sample 180 degrees rotated solutions during rigid body EM -> turn off
</a>


We are now ready to submit the docking run.

The interface also allows us to download the input structures of the docking run (in the form of a tgz archive) and a haddockparameter file which contains all the settings and input structures for our run (in json format). We strongly recommend to download this file as it will allow you to repeat the run after uploading  it into the [file upload inteface](https://bianca.science.uu.nl/haddock2.4/submit_file){:target="_blank"} of the HADDOCK webserver. This file, which provides a reference input of your run, can also be edited to change a few parameters for example. An excerpt of this file is shown here:

<pre>
{
    "runname": "RNA-Pol-III-xlinks",
    "amb_cool1": 10.0,
    "amb_cool2": 50.0,
    "amb_cool3": 50.0,
    "amb_firstit": 0,
    "amb_hot": 10.0,
    "amb_lastit": 2,
    "anastruc_1": 200,
...
</pre>

This file contains all parameters and input data of your run, including the uploaded PDB files and the restraints.

<a class="prompt prompt-question">
Can you locate the distance restraints in this file?
</a>

* **Step 14:** Click on the "Submit" button at the bottom left of the interface.

Upon submission you will be presented with a web page which also contains a link to the previously mentioned haddockparameter file as well as some information about the status of the run.

<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/submission.png">
</figure>

Currently, your run should be queued but eventually its status will change to "Running" with the page showing the progress of the calculations.
The page will automatically refresh and the results will appear upon completion (which can take between 1/2 hour to
several hours depending on the size of your system and the load of the server). Since we are dealing here with a large complex, 
the docking will take quite some time (probably 1/2 day). So be patient. You will be notified by email once your job has successfully completed.



<hr>
### First analysis of the results

Once your run has completed you will be presented with a result page showing the cluster statistics and some graphical
representation of the data. If you are using course credentials the number of models generated will have been decreased 
to allow the runs to complete within a reasonable amount of time. Because of that, the results might not be very good.

We have already performed a full docking runs (with 2000/400/400 models generated for the
rigid-body docking, semi-flexible and water refinement stages). 
The full run can be accessed [here](https://bianca.science.uu.nl/haddock2.4/run/4242424242/PolIII-C82-C34-C31model-xlinks){:target="_blank"}.


<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/HADDOCK-result-page.png">
<p> Example result page</p>
</figure>

<a class="prompt prompt-question">Inspect the result page.</a>
<a class="prompt prompt-question">How many clusters are generated?</a>


__Note:__ The bottom of the page gives you some graphical representations of the results, showing the distribution of
the solutions for various measures (HADDOCK score, van der Waals energy, ...) as a function of the RMSD from the best
generated model (the best scoring model). The plots are interactive and you can zoom into selected areas, move the graph, select specific points, all of it by clicking on the icons on the top of each graph. You can also turn on and off specific clusters.

<details style="background-color:#DAE4E7"><summary><b>See graphical analysis view:</b>
</summary>
<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/graphical-analysis.png">
<p> <i>Graphical view of the docking results</i></p>
</figure>
</details>
<br>

<details style="background-color:#DAE4E7"><summary><b>See cluster analysis view:</b>
</summary>
<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/cluster-analysis.png">
<p> <i>HADDOCK score components distributions per cluster</i></p>
</figure>
</details>
<br>

You can also quickly visualize a specific structure by clicking on the "eye" icon next to a structure.
While in the “eye” mode, you can use the middle mouse to zoom in/out.

<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/online-visualisation.png">
</figure>


The ranking of the clusters is based on the average score of the top 4 members of each cluster. The score is calculated
as:
<pre>
      HADDOCKscore = 1.0 * Evdw + 0.2 * Eelec + 1.0 * Edesol + 0.1 * Eair
</pre>
where Evdw is the intermolecular van der Waals energy, Eelec the intermolecular electrostatic energy, Edesol represents
an empirical desolvation energy term adapted from Fernandez-Recio *et al.* J. Mol. Biol. 2004, and Eair the AIR energy.

The cluster numbering reflects the size of the cluster, with cluster 1 being the most populated cluster. 
The various components of the HADDOCK score are also reported for each cluster on the results web page.

<a class="prompt prompt-question">Consider the cluster scores and their standard deviations.</a>
<a class="prompt prompt-question">Is the top ranked significantly better than the second one?</a>
<a class="prompt prompt-question">Which energy terms are playing a dominant role in the ranking of top clusters?</a>
<a class="prompt prompt-question">Which cluster satisfies the experimental restraints best?</a>

In case the scores of various clusters are within the standard deviation from each other, all should be considered as a
valid solution for the docking. Ideally, some additional independent experimental information should be available to
decide on the best solution.


<hr>
### Visualisation of docked models

Let's now visualize the various clusters. The result page allows to download individual models, but it also has an option to download 
all clusters at once. Look for the following sentence, just above the cluster statistics:

<pre>
You can also download all cluster files (best X of the top 10 cluster(s)).
</pre>

<a class="prompt prompt-info">Download the archive by clicking on the link and unpack it</a>

Start PyMOL and load each cluster representative (`clusterX_1.pdb`):

<a class="prompt prompt-pymol">File menu -> Open -> select cluster12_1.pdb</a>

Repeat this for each cluster. 

__Note:__ If using the command line, all clusters can be loaded easily in one command:

<a class="prompt prompt-cmd">pymol cluster*_1.pdb</a>


Once all files have been loaded, type in the PyMOL command window:

<a class="prompt prompt-pymol">
show cartoon<br>
util.cbc<br>
hide lines<br>
</a>

Let's then superimpose all models on chain A of the first cluster:

<a class="prompt prompt-pymol">
select cluster1_1 and chain A<br>
align cluster2_1, sele
</a>

<a class="prompt prompt-info">
Repeat the align command for each cluster representative.
</a>

Alternatively, you can superimpose all models on the selection, by:
<a class="prompt prompt-info">
Find the sele entry in the menu listing all molecules on the right side of the PyMol window.
</a>
<a class="prompt prompt-info">
Click on the A button next to it -> align -> all to this (*/CA).
</a>


This will align all clusters on chain A (PolIII-core), maximizing the differences in the orientation of the other chains.


<a class="prompt prompt-question">
Examine the various clusters. Compare the orientation of each domain (C82,C34_wHTH1, C34_wHTH2 and C31). 
How does their orientation differ between the various clusters?
</a>

__Note:__ You can turn on and off a cluster by clicking on its name in the right panel of the PyMOL window.

__Reminder:__ ChainA corresponds to PolIII-core, B to C82, C to C34_wHTH1, D to C34_wHTH2, F to C31.

<details style="background-color:#DAE4E7"><summary><b>See PyMol view:</b>
</summary>
<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/clusters-pymol.png">
<p> <i>PyMol view of the various clusters, superimposed on PolIII core</i></p>
</figure>
</details>
<br>
<br>

<a class="prompt prompt-question">
Which domain is the best defined over the various clusters?
</a>

<a class="prompt prompt-question">
Which domain is the worst defined over the various clusters?
</a>


### Satisfaction of cross-link restraints

Let's now check if the solutions actually fit the cross-links we defined.
Start a new PyMOL session and load as described above the model you want to analyze, e.g. the best model of the top
ranking cluster, `cluster12_1.pdb`.

#### Analysing the cross-links defining the position of the C82 domain

In the PyMOL command window type:

<a class="prompt prompt-pymol">
show cartoon<br>
util.cbc<br>
hide lines<br>
distance C82-d01-30A, chain B and resid  50 and name CB, chain F and resid   91 and name CB<br>
distance C82-d02-30A, chain B and resid 472 and name CB, chain A and resid 5394 and name CB<br>
distance C82-d03-30A, chain B and resid 520 and name CB, chain A and resid 5394 and name CB<br>
distance C82-d04-30A, chain B and resid 520 and name CB, chain D and resid  135 and name CB<br>
distance C82-d05-30A, chain B and resid 520 and name CB, chain D and resid  138 and name CB<br>
distance C82-d06-30A, chain B and resid 520 and name CB, chain D and resid  141 and name CB<br>
distance C82-d07-30A, chain B and resid 604 and name CB, chain F and resid   66 and name CB<br>
distance C82-d08-30A, chain B and resid 605 and name CB, chain F and resid   91 and name CB<br>
distance C82-d09-30A, chain B and resid 612 and name CB, chain F and resid   57 and name CB<br>
distance C82-d10-30A, chain B and resid 612 and name CB, chain F and resid  111 and name CB<br>
</a>

This will draw lines between the connected atoms and display the corresponding Euclidian distance.
Objects are created in the left panel with their name corresponding to the cross-link and its associated maximum distance.

<a class="prompt prompt-info">
Inspect the various cross-link distances.
</a>

<a class="prompt prompt-question">
Is the model satisfying the cross-link restraints?
</a>

<a class="prompt prompt-question">
If not, which ones are not satistified?
</a>

__Note__ that the reported distances are Euclidian distances. In reality, the cross-linker will have to follow the
surface of the molecule which might results in a longer effective distance. A proper comparison would require
calculating the surface distance instead. Such an analysis can be done with the [XWalk][link-xwalk] or [jwalk](http://jwalk.ismb.lon.ac.uk/jwalk/){:target="_blank"} software.

#### Analysing the cross-links defining the position of the C34_wHTH1 domain

You can first hide the distances shown for C82 by unselecting them in the menu on the right side of the window.
Alternatively delete them in PyMol by typing:

<a class="prompt prompt-pymol">delete C82*</a>

In the PyMOL command window type:

<a class="prompt prompt-pymol">
distance C34-1-d1-30A, chain C and resid 65 and name CB, chain A and resid 5394 and name CB<br>
distance C34-1-d2-30A, chain C and resid 62 and name CB, chain D and resid   82 and name CB<br>
distance C34-1-d3-30A, chain C and resid 62 and name CB, chain D and resid   83 and name CB<br>
distance C34-1-d4-30A, chain C and resid 62 and name CB, chain D and resid  123 and name CB<br>
distance C34-1-d5-30A, chain C and resid 65 and name CB, chain D and resid   82 and name CB<br>
distance C34-1-d6-30A, chain C and resid 65 and name CB, chain D and resid  123 and name CB<br>
distance C34-1-d7-30A, chain C and resid 65 and name CB, chain D and resid  126 and name CB<br>
distance C34-1-d8-30A, chain C and resid 65 and name CB, chain D and resid  135 and name CB<br>
</a>

<a class="prompt prompt-info">
Inspect the various cross-link distances.
</a>

<a class="prompt prompt-question">
Is the model satisfying the cross-link restraints?
</a>

<a class="prompt prompt-question">
If not, which ones are not satistified?
</a>

#### Analysing the cross-links defining the position of the C34_wHTH2 domain

You can first hide the distances shown for C34_wHTH1 by unselecting them in the menu on the right side of the window.
Alternatively delete them in PyMol by typing:

<a class="prompt prompt-pymol">delete C34-1*</a>

In the PyMOL command window type:

<a class="prompt prompt-pymol">
distance C34-2-d01-30A, chain D and resid  82 and name CB, chain C and resid   62 and name CB<br>
distance C34-2-d02-30A, chain D and resid  82 and name CB, chain C and resid   62 and name CB<br>
distance C34-2-d03-30A, chain D and resid  82 and name CB, chain C and resid   65 and name CB<br>
distance C34-2-d04-30A, chain D and resid 123 and name CB, chain A and resid 5394 and name CB<br>
distance C34-2-d05-30A, chain D and resid 123 and name CB, chain C and resid   62 and name CB<br>
distance C34-2-d06-30A, chain D and resid 123 and name CB, chain C and resid   65 and name CB<br>
distance C34-2-d07-30A, chain D and resid 126 and name CB, chain C and resid   65 and name CB<br>
distance C34-2-d08-30A, chain D and resid 126 and name CB, chain F and resid  196 and name CB<br>
distance C34-2-d09-30A, chain D and resid 135 and name CB, chain C and resid   65 and name CB<br>
distance C34-2-d10-30A, chain D and resid 135 and name CB, chain D and resid  520 and name CB<br>
distance C34-2-d11-30A, chain D and resid 138 and name CB, chain D and resid  520 and name CB<br>
distance C34-2-d12-30A, chain D and resid 141 and name CB, chain D and resid  520 and name CB<br>
</a>

<a class="prompt prompt-info">
Inspect the various cross-link distances.
</a>

<a class="prompt prompt-question">
Is the model satisfying the cross-link restraints?
</a>

<a class="prompt prompt-question">
If not, which ones are not satistified?
</a>


#### Analysing the cross-links defining the position of the C31 domain

You can first hide the distances shown for C34_wHTH2 by unselecting them in the menu on the right side of the window.
Alternatively delete them in PyMol by typing:

<a class="prompt prompt-pymol">delete C34-2*</a>

In the PyMOL command window type:

<a class="prompt prompt-pymol">
distance C31-d01-30A, chain F and resid  57 and name CB, chain B and resid  612 and name CB<br>
distance C31-d02-30A, chain F and resid  66 and name CB, chain B and resid  604 and name CB<br>
distance C31-d03-30A, chain F and resid  91 and name CB, chain A and resid 1458 and name CB<br>
distance C31-d04-30A, chain F and resid  91 and name CB, chain A and resid 3402 and name CB<br>
distance C31-d06-30A, chain F and resid  91 and name CB, chain A and resid 4206 and name CB<br>
distance C31-d07-30A, chain F and resid  91 and name CB, chain A and resid 4359 and name CB<br>
distance C31-d08-30A, chain F and resid  91 and name CB, chain A and resid 4361 and name CB<br>
distance C31-d09-30A, chain F and resid  91 and name CB, chain B and resid   50 and name CB<br>
distance C31-d10-30A, chain F and resid  91 and name CB, chain B and resid  605 and name CB<br>
distance C31-d11-30A, chain F and resid 111 and name CB, chain B and resid  612 and name CB<br>
distance C31-d12-30A, chain F and resid 111 and name CB, chain A and resid 3514 and name CB<br>
distance C31-d13-30A, chain F and resid 111 and name CB, chain A and resid 1458 and name CB<br>
distance C31-d14-30A, chain F and resid 179 and name CB, chain A and resid  143 and name CB<br>
distance C31-d15-30A, chain F and resid 196 and name CB, chain D and resid  126 and name CB<br>
</a>

<a class="prompt prompt-info">
Inspect the various cross-link distances.
</a>

<a class="prompt prompt-question">
Is the model satisfying the cross-link restraints?
</a>

<a class="prompt prompt-question">
If not, which ones are not satistified?
</a>


<hr><hr>
## Fitting the docking models into low resolution cryo-EM maps

We will now fit the models we obained into the unpublished 9Å resolution cryo-EM map for the RNA Polymerase III apo state.
For this we will use the [UCSF Chimera][link-chimera]{:target="_blank"} software.

For this open the PDB file of the cluster you want to fit and the EM map `PolIII_9A.mrc` (available in the `cryo-EM` directory).

<a class="prompt prompt-info">
  UCSF Chimera Menu → File → Open... → Select the file
</a>

Repeat this for each file. Chimera will automatically guess their type.


If you want to use the Chimera command-line instead, you need to first display it:

<a class="prompt prompt-info">
  UCSF Chimera Menu → Favorites → Command Line
</a>

and type:

<a class="prompt prompt-pymol">
  open /path/to/clusterX_1.pdb
</a>
<a class="prompt prompt-pymol">
  open /path/to/PolIII_9A.mrc
</a>


In the `Volume Viewer` window, the middle slide bar provides control on the
value at which the isosurface of the density is shown. At high values, the
envelope will shrink while lower values might even display the noise in the map.
In the same window, you can click on `Center` to center the view on all visible molecules and the density.

We will first make the density transparent, in order to be able to see the fitted structure inside:

<a class="prompt prompt-info">
  Within the Volume Viewer window click on the gray box next to Color
</a>

This opens the`Color Editor` window.

<a class="prompt prompt-info">
Check the Opacity box.
</a>

An extra slider bar appears in the box called A, for the alpha channel.

<a class="prompt prompt-info">
Set the alpha channel value to around 0.6.
</a>

In order to distinguish the various chains we can color the structure by chain. For this:
<a class="prompt prompt-info">
Chimera menu -> Tools -> Depiction -> Rainbow
Select the option to color by chain and click the Apply button
</a>


In order to perform the fit, we will use the Command Line more:

<a class="prompt prompt-info">
UCSF Chimera Menu → Favorites → Command Line
</a>

Also open the Model Panel to know the ID of the various files within Chimera:

<a class="prompt prompt-info">
UCSF Chimera Menu → Favorites → Model Panel
</a>

Note the number of the cluster model you upload and of the cryo-EM map (e.g. if you loaded first the PDB file, it must have model #0 and the map is #1).
Then, in the Command Line interface type:

<a class="prompt prompt-pymol">
molmap #0 9 modelId 3    
</a>

This generate a 9Å map from the PDB model we uploaded with ID #3.
The next command then performs the fit of this map onto the experimental cryo-EM map:

<a class="prompt prompt-pymol">
fitmap #1 #3 search 100<br>
close #3
</a>

When the fit completes, a window will appear showing the fit results in terms of correlation coefficients.
Note the value for the cluster you selected.

You also try to improve further the fit:
<a class="prompt prompt-info">
UCSF Chimera Menu → Tools → Volume Data -> Fit in Map
</a>

<a class="prompt prompt-info">
Click the Options button
</a>
<a class="prompt prompt-info">
Select the Use map simulated from atoms and set the Resolution to 9
</a>
<a class="prompt prompt-info">
Click on Update and note the correlation value
</a>
<a class="prompt prompt-info">
Click on Fit and check if the correlation does improve
</a>


You can repeat this procedure for the various clusters and try to find out which solution best fits the map.
In case you upload multiple models simultaneously, make sure to use the correct model number in the above commands (check the Model Panel window for this).



<hr><hr>
## Strategy 2): Modelling the complex by docking with cross-links only, using as starting conformations the models fitted into the cryo-EM map

In this alternative strategy we will start by fitting the largest components (core and C82) into the 9Å cryo-EM map using our PowerFit web server.
This fitted models will then be used as input for the docking with cross-links, keeping those fixed at their original position.


<hr>
### Introduction to PowerFit

PowerFit is a software developed in our lab to fit atomic resolution
structures of biomolecules into cryo-electron microscopy (cryo-EM) density maps.
PowerFit performs a rigid body fitting, calculating the
cross-correlation, a common measure of the goodness-of-fit, between the atomic
structure and the density map. It performs a systematic 6-dimensional scan of
the three translational and three rotational degrees of freedom. In short,
PowerFit will try to systematically fit the structure in different orientations at every position
in the map and calculate a cross-correlation score for each of them.

It is open-source and available for download from our [Github repository][link-powerfit]{:target="_blank"}.
To facilitate its use, we have developed a [web portal][link-powerfit-web]{:target="_blank"} for it.

The server makes use of either local resources on our cluster, using the multi-core version of the software, or GPGPU-accelerated grid resources of the
[EGI](http://www.egi.eu){:target="_blank"} to speed up the calculations. It only requires a web browser to work and benefits from the latest
developments in the software, based on a stable and tested workflow. Next to providing an automated workflow around
PowerFit, the web server also summarizes and higlights the results in a single page including some additional postprocessing
of the PowerFit output using [UCSF Chimera][link-chimera]{:target="_blank"}.

For more details about PowerFit and its usage we refer to a related [online tutorial](/education/Others/powerfit-webserver){:target="_blank"}.

<hr>
### Fitting PolIII-core and C82 into the 9Å cryo-EM map

To run PowerFit, go to

<a class="prompt prompt-info" href="http://haddock.science.uu.nl/services/POWERFIT" target="_blank">http://haddock.science.uu.nl/services/POWERFIT</a>

On this page, you will find the most relevant information about the server as well as the links to the local and grid versions of the portal's submission page.

Click on the "**Submit**" menu to access the [input form][link-powerfit-submit]{:target="_blank"}:

Complete the form by filling the required fields and selecting the respective files
(most browsers should also support dragging the files onto the selection button):

<a class="prompt prompt-info">Cryo-EM map → PolIII_9A.mrc</a>
<a class="prompt prompt-info">Map resolution → 9.0</a>
<a class="prompt prompt-info">Atomic structure → A_PolIII-5fja-core.pdb</a>
<a class="prompt prompt-info">Rotational angle interval → 10.0</a>

Once the fields have been filled in you can submit your job to our server
by clicking on "**Submit**" at the bottom of the page.

If the input fields have been correctly filled you should be redirected to a status page displaying a pop-up message
indicating that your run has been successfully submitted.
While performing the search, the PowerFit web server will update you on the progress of the
job by reloading the status page every 30 seconds.


For convenience, we have already provided pre-calculated results in the `cryo-EM/powerfit-PolIII-core` directory in the data downloaded for this tutorial.
The `fit_1.pdb` file corresponds to the top solution predicted by PowerFit. You can inspect it and see how well it fits into the cryo-EM map 
using `Chimera` with its `Volume -> Fit in Map` tool (see instructions above).


Repeat the above procedure, but this time for the C82 domain. 
Pre-calculated results are available in the `cryo-EM/powerfit-PolIII-C82` directory and also online:

* Pol III core domain [powerfit results](https://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/example/4){:target="_blank"}
* Pol III C82 domain [powerfit results](https://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/example/5){:target="_blank"}


<hr>
### Refining the fit in Chimera

Let's see how well did PowerFit perform in fitting and try to further optimize the fit using Chimera.

<a class="prompt prompt-info">
  UCSF Chimera Menu → File → Open... → Select the cryo-EM/powerfit-PolIII-core/fit_1.pdb
</a>
<a class="prompt prompt-info">
  UCSF Chimera Menu → File → Open... → Select the cryo-EM/powerfit-PolIII-C82/fit_1.pdb
</a>
<a class="prompt prompt-info">
  UCSF Chimera Menu → File → Open... → Select the cryo-EM/PolIII_9A.mrc
</a>

In the `Volume Viewer` window, the middle slide bar provides control on the
value at which the isosurface of the density is shown. At high values, the
envelope will shrink while lower values might even display the noise in the map.
In the same window, you can click on `Center` to center the view on all visible molecules and the density.

First make the density transparent, in order to be able to see the fitted structure inside:

<a class="prompt prompt-info">
  Within the Volume Viewer window click on the gray box next to Color
</a>
<a class="prompt prompt-info">
Set the alpha channel value to around 0.6.
</a>

In order to distinguish the various chains color the structure by chain:

<a class="prompt prompt-info">
Chimera menu -> Tools -> Depiction -> Rainbow
Select the option to color by chain and click the Apply button
</a>

Now let's check the quality of the fit:

<a class="prompt prompt-info">
UCSF Chimera Menu → Tools → Volume Data -> Fit in Map
</a>
<a class="prompt prompt-info">
Click the Options button
</a>
<a class="prompt prompt-info">
Select the Use map simulated from atoms and set the Resolution to 9
</a>
<a class="prompt prompt-info">
Click on Update and note the correlation value
</a>
<a class="prompt prompt-info">
Click on Fit and check if the correlation does improve
</a>

If the correlation has improved after fitting, do save the fitted molecules:

<a class="prompt prompt-info">
File -> Save PDB -> Select fit_1.pdb (#0) and give a filename (e.g.: PolIII-core-fitted.pdb)
</a>
<a class="prompt prompt-info">
File -> Save PDB -> Select fit_1.pdb (#1) and give a filename (e.g.: PolIII-C82-fitted.pdb)
</a>

The two molecules were fitted separately into the map, which can cause clashes at the interface.
Inspect the interface (first turn off the map by clicking on the "eye" in the Volume Viewer window).

<a class="prompt prompt-question">
Can you identify possible problematic areas of the interface?
</a>

<details style="background-color:#DAE4E7"><summary><b>See solution:</b>
</summary>
<p>There are clearly several regions where the two molecules are clashing. Before using those, a refinement of the interface is thus required. This can be done using HADDOCK</p>
<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/core-C82-clashes.png">
</figure>
</details>
<br>
<br>


<hr>
### Refining the interface of the cryo-EM fitted models with HADDOCK

To refine the fitted models, we can use HADDOCK, keeping the molecules in their original orientation, skipping the initial rigid body docking stage and semi-flexible refimenent and only performing the final refinement (or morphing from CG to AA if coarse graining is used). Since we are dealing with severe clashes, a coarse graining approach would be better since the individual all atom representation are effectively docked onto the coarse-grained model and refined.

We will make use of the [HADDOCK2.4 interface](https://bianca.science.uu.nl/haddock2.4/submit/1){:target="_blank"} of the HADDOCK web server.

* **Step 1:** Define a name for your refinement run, e.g. *PolIII-core-C82-refine*.

* **Step 2:** Define the number of components, i.e. *2*.

* **Step 3:** Input the first protein PDB file.

<a class="prompt prompt-info">
First molecule: where is the structure provided? -> "I am submitting it"
</a>
<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *PolIII-core-fitted.pdb* (the model we saved from Chimera)
</a>
<a class="prompt prompt-info">
Do you want to coarse-grain your molecule? -> turn on
</a>
<a class="prompt prompt-info">
Fix molecule at its original position during it0? -> turn on
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> A
</a>


* **Step 4:** Input the second protein PDB file.

<a class="prompt prompt-info">
First molecule: where is the structure provided? -> "I am submitting it"
</a>
<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *PolIII-C82-fitted.pdb* (the model we saved from Chimera)
</a>
<a class="prompt prompt-info">
Do you want to coarse-grain your molecule? -> turn on
</a>
<a class="prompt prompt-info">
Fix molecule at its original position during it0? -> turn on
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> B
</a>


* **Step 5:** Click on the "Next" button at the bottom left of the interface. This will upload the structures to the HADDOCK webserver where they will be processed and validated (checked for formatting errors). The server makes use of [Molprobity](http://molprobity.biochem.duke.edu/){:target="_blank"} to check side-chain conformations, eventually swap them (e.g. for asparagines) and define the protonation state of histidine residues.

If everything went well, the interface window should have updated itself and it should now show the list of residues for molecules 1 and 2.

* **Step 6:** No need for changes at this stage. Simply click on `Next`.

* **Step 7:** We don't need to provide restraints, but will turn on center-of-mass restraints.

<a class="prompt prompt-info">
Define center of mass restraints to enforce contact between the molecules -> Turn on
</a>


In the same page where the restraints are provided you can modify a large number of docking settings.

* **Step 8:** Unfold the **sampling parameters** menu.

For refinement purposes a limited number of models is sufficient:

<a class="prompt prompt-info">
Decrease thee number of models to 20 for all stages (rigid body, semi-flexible refinement and water refinement)
</a>
<a class="prompt prompt-info">
Number of trials for rigid body minimisation -> 1
</a>
<a class="prompt prompt-info">
Sample 180 degrees rotated solutions during rigid body EM -> off
</a>


* **Step 9:** Unfold the **advanced sampling parameters** menu.

We will here turn off the first rigid body docking and semi-flexible refinement stages:
<a class="prompt prompt-info">
Randomize starting orientations -> off
</a>
<a class="prompt prompt-info">
Perform initial rigid body minimisation -> off
</a>
<a class="prompt prompt-info">
Allow translation in rigid body minimisation -> off
</a>
<a class="prompt prompt-info">
Number of MD steps for rigid body high temperature TAD -> 0
</a>
<a class="prompt prompt-info">
Number of MD steps during first rigid body cooling stage -> 0
</a>
<a class="prompt prompt-info">
Number of MD steps during second cooling stage with flexible side-chains at interface -> 0
</a>
<a class="prompt prompt-info">
Number of MD steps during third cooling stage with fully flexible interface -> 0
</a>

We are now ready to submit the docking run.

If you don't want to wait for your results, a pre-calculated refinement run is available [here](https://bianca.science.uu.nl/haddock2.4/run/4242424242/PolIII-core-C82-refine){:target="_blank"}.

<a class="prompt prompt-question">
Inspect the results page: Are the intermolecular energies favorable?
</a>

<a class="prompt prompt-question">
Download the top model and inspect it in PyMol. Are the clashing segments identified above still problematic?
</a>

__Note__: A refined model is available in the `cryo-EM` directory with as filename: `PolIII-core-C82-powerfit-chimera-fitted-refined.pdb`


<a class="prompt prompt-question">
Using Chimera, fit the refined model into the 9Å cryo-EM map (as described previously) and check the correlation coefficient.
How does it compare with the Chimera-fitted, unrefined model?
</a>


<hr>
### Setting up the full docking run with C34 and C31 and the cryo-EM fitted, refined core and C82 domains

We will now repeat the steps from the the first [HADDOCK run submission](#strategy-1-modelling-the-complex-by-docking-with-cross-links-only), 
with as difference that we will use the PowerFit/Chimera, HADDOCK-refined structures of PolIII core and C82. Those will be kept fixed in their original positions
for the initial rigid-body docking stage.

Connect to the [HADDOCK2.4 interface](https://bianca.science.uu.nl/haddock2.4/submit/1){:target="_blank"} of the HADDOCK web server.

* **Step 1:** Define a name for your docking run, e.g. *PolIII-core-C82-EMfit-C34-C31-xlinks*.

* **Step 2:** Define the number of components, i.e. *5*.

* **Step 3:** Input the first PDB file.

<a class="prompt prompt-info">
Which chain to be used? -> A
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select from the cryo-EM directory *PolIII-core-C82-powerfit-chimera-fitted-refined.pdb*
</a>
<a class="prompt prompt-info">
Do you want to coarse-grain your molecule? -> turn on
</a>
<a class="prompt prompt-info">
Fix molecule at its original position during it0? -> turn on
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> A
</a>


* **Step 4:** Input the second protein PDB files.

<a class="prompt prompt-info">
Which chain to be used? -> B
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select from the cryo-EM directory *PolIII-core-C82-powerfit-chimera-fitted-refined.pdb*
</a>
<a class="prompt prompt-info">
Do you want to coarse-grain your molecule? -> turn on
</a>
<a class="prompt prompt-info">
Fix molecule at its original position during it0? -> turn on
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> B
</a>


* **Step 5:** Input the third protein PDB files.

<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *C_C34_wHTH1-2DK8A.pdb*
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> C
</a>

* **Step 6:** Input the fourth protein PDB files.

<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *D_C34_wHTH2-2DK8A.pdb*
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> D
</a>

* **Step 7:** Input the fifth protein PDB files.

<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *F_C31_iTasser.pdb*
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> F
</a>

===> _Make sure to change the Segmend ID to F otherwise the restraints for C31 won't be used!_ <===


* **Step 8:** Click on the "Next" button at the bottom left of the interface. 

If everything went well, the interface window should have updated itself and it should now show the list of residues for molecules 1 and 2.

* **Step 9:** No further action is required in this page, so click on the "Next" button at the bottom of the **Input parameters** window, 
which proceeds to the  **Distance Restraint menu**  menu of the **Docking Parameters** window.

* **Step 10:** Upload the cross-link restraints file to the ambiguous restraints category

<a class="prompt prompt-info">
Instead of specifying active and passive residues, you can supply a HADDOCK restraints TBL file (ambiguous restraints) -> Browse and select *xlinks-all-inter-disvis-filtered.tbl*
</a>

* **Step 11:** Upload the C34 connectivity restraints file to the unambiguous restraints category

<a class="prompt prompt-info">
You can supply a HADDOCK restraints TBL file with restraints that will always be enforced (unambiguous restraints) -> Browse and select *C34-connectivities.tbl*
</a>

* **Step 12:** Turn off random removal of restraints

<a class="prompt prompt-info">
Randomly exclude a fraction of the ambiguous restraints (AIRs) -> Turn off
</a>

* **Step 13:** Unfold the **clustering parameters** menu.

Since the largest interface between PolIII core and C82 is fixed, we can increase the clustering cutoff to 0.75 
to better discriminate between various orientations of the smaller C34 and C31 domains.

<a class="prompt prompt-info">
RMSD Cutoff for clustering (recommended: 7.5A for RMSD, 0.60 for FCC) -> 0.75
</a>

* **Step 14:** Unfold the **sampling parameters** menu.

Here you can change the number of models that will be calculated, the default being 1000/200/200 for the three stages of HADDOCK (see [HADDOCK General Concepts](#haddock-general-concepts). When docking multiple subunits, it is recommended to increase the sampling, e.g. to 10000/400/400 (at the cost of longer computations). For this tutorial, we might use 2000/400/400 (but if you are using course accounts, this will be automatically downsampled to 250/50/50). 


When docking only with  interface information (i.e. no specific distances), we systematically sample the 180 degrees rotated solutions for each interface, mimimizing the rotated solution and keeping the best of the two in terms of HADDOCK score. Since here we are using specific distance restraints, we can turn off this option to save time.

<a class="prompt prompt-info">
Sample 180 degrees rotated solutions during rigid body EM -> turn off
</a>


We are now ready to submit the docking run!

<hr>
### Analysis of the docking results

Once your run has completed you will be presented with the result page. You can also access a pre-calculated run following the docking scenario just described from the following [link](https://bianca.science.uu.nl/haddock2.4/run/4242424242/PolIII-core-C82-EMfit-C34-C31-xlinks){:target="_blank"}.

<a class="prompt prompt-info">
Inspect the results page
</a>

<a class="prompt prompt-question">How many clusters are generated?</a>
<a class="prompt prompt-question">How different are the clustering results compared to the cross-links only setup described in the first part of this tutorial?</a>

<a class="prompt prompt-question">Compare the score and the various energy terms of the best cluster and the best cluster obtained using Strategy 1) using only cross-links. Which strategy leads to better scores/energies?</a>

<a class="prompt prompt-info">
Download the clustered models, and visualize them in PyMol as described above, loading the top model of each cluster in PyMol.
</a>

<a class="prompt prompt-question">Which domain is the least well defined?</a>

<details style="background-color:#DAE4E7"><summary><b>See solution:</b>
</summary>
<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/PolIII-cryoEM-C34-C31.png">
</figure>
<p>C34 wHTH1 (in pink) is clearly the less defined domain</p>
</details>
<br>
<br>


<a class="prompt prompt-info">
Now repeat the cross-links analysis in PyMol as described previsously.
</a>

<a class="prompt prompt-question">Which cross-links are the most violated?</a>


<a class="prompt prompt-info">
Finally, perform the fitting into the 9Å cryo-EM map as described above.
</a>


<a class="prompt prompt-question">Which one of the two strategies described in this tutorial leads to the best correlaction coefficient with the 9Å map</a>


<details style="background-color:#DAE4E7"><summary><b>See solution:</b>
</summary>
<figure align="center">
<img src="/education/HADDOCK24/RNA-Pol-III/strategy2-EMfit.png">
</figure>
<p>Strategy 2, consisting of first fitting the largest domains into the map and using those as starting point for the docking leads to a better fit in the EM map (correlation 0.937). Comparing the two sets of solutions, one can clearly see that C82 fits much better into the density. The C34 domains are found in regions of the map where unaccounted density appear when playing with the level at which the map is represented. As for C31 (see right panel in the figure below) it is positioned in a region of low density, probably indicating disorder.</p>
</details>
<br>
<br>


<hr><hr>
## Conclusions

We have demonstrated the use of cross-linking data from mass spectrometry for guiding the docking process in HADDOCK.
The results show that it is not straightforward to satisfy all cross-links, even when false positives are first identified with DisVis.
In the original work of [Ferber et al. 2016](https://www.nature.com/articles/nmeth.3838){:target="_blank"} from which the cross-links were taken, many 
cross-links remained violated. See for example Suppl. Table 5 in  the corresponding [supplementary material](https://media.nature.com/original/nature-assets/nmeth/journal/v13/n6/extref/nmeth.3838-S1.pdf){:target="_blank"}. It is also possible that the cross-linking experiments might have captured transient or non-native interactions.

Our modelling here was based on homology models, which brings another level of complexity. Clearly some domains show much
more variability in their positions (e.g. C34_wHTH1), which might explain why they are not seen in the cryo-EM density.

And finally, using the cryo-EM data to pre-orient molecules prior to docking seems to be a better strategy in this particular case.

<hr><hr>
## Alternative runs

1) Instead of using the full C31 model, you could repeat the docking using the dummy Lysines residues for C31 and compare the results.
Compare in particular the position of the various domains and the retraint energy indicating how well the cross-links are satistified.
In that case you should setup a six-body docking run using:

* 1st molecule - chainA: PolIII-core
* 2nd molecule - chainB: C82 homology model
* 3rd molecule - chainC: C34 wHTH1 domain homology model
* 4th molecule - chainD: C34 wHTH2 domain homology model
* 5th molecule - chainF: C31 lysine91
* 6th molecule - chainG: C31 lysine111

and as restraint files: `xlinks-all-inter-disvis-filtered-C31dummyLYS.tbl` for the cross-links and `C31-C34-connectivities.tbl` as connectivity restraints.

The results of such a run using exclusively cross-links (strategy 1) can be accessed 
[here](https://bianca.science.uu.nl/haddock2.4/run/4242424242/RNA-Pol-III-xlinks-C31dummies){:target="_blank"}.

The results of such a run using the cryo-EM fitted core and C82 domains with cross-links (strategy 2) can be accessed 
[here](https://bianca.science.uu.nl/haddock2.4/run/4242424242/PolIII-core-C82-EMfit-C34-C31dummies){:target="_blank"}.

2) Try to identify from the run described in this tutorial the heavily violated cross-links and remove them from the restraints list. 
Repeat the docking and check if this affects the position of the various domains.


<hr><hr>
## Congratulations!

Thank you for following this tutorial. If you have any questions or suggestions, feel free to contact us via email, or post your question to
our [HADDOCK forum](http://ask.bioexcel.eu/c/haddock){:target="_blank"} hosted by the
[<img width="70" src="/images/Bioexcel_logo.png">](http://bioexcel.eu){:target="_blank"} Center of Excellence for Computational Biomolecular Research.

[link-cns]: http://cns-online.org "CNS online"
[link-chimera]: https://www.cgl.ucsf.edu/chimera/ "UCSF Chimera"
[link-disvis]: https://github.com/haddocking/disvis "DisVis GitHub repository"
[link-disvis-web]: hhttps://bianca.science.uu.nl/disvis "DisVis web server"
[link-disvis-submit]: https://bianca.science.uu.nl/disvis/submit "DisVis submission"
[link-disvis-register]: https://bianca.science.uu.nl/auth/register "DisVis registration"
[link-pymol]: http://www.pymol.org/ "PyMOL"
[link-haddock]: http://bonvinlab.org/software/haddock2.2 "HADDOCK 2.2"
[link-haddock-web]: https://wenmr.science.uu.nl/haddock2.4/ "HADDOCK 2.4 webserver"
[link-haddock-easy]: http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-easy.html "HADDOCK2.2 webserver easy interface"
[link-haddock-expert]: http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-expert.html "HADDOCK2.2 webserver expert interface"
[link-haddock-register]: https://bianca.science.uu.nl/auth/register/"HADDOCK web server registration"
[link-molprobity]: http://molprobity.biochem.duke.edu "MolProbity"
[link-powerfit]: https://github.com/haddocking/powerfit "PowerFit"
[link-powerfit-web]: http://haddock.science.uu.nl/services/POWERFIT/ "PowerFit web server"
[link-powerfit-register]: https://bianca.science.uu.nl/auth/register  "PowerFit registration"
[link-powerfit-submit]: http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/submit "PowerFit submission"
[link-powerfit-help]: http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/help "PowerFit submission"
[link-xwalk]: http://www.xwalk.org
