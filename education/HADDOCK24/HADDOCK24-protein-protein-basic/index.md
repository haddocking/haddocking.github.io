---
layout: page
title: "HADDOCK2.4 basic protein-protein docking tutorial"
excerpt: "A small tutorial on predicting a protein-protein complex using interface residues identified from NMR chemical shift perturbation experiments"
tags: [HADDOCK, NMR, docking, dimer, chemical shifts]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

This tutorial was last updated on 12-03-2026

<hr>
## Introduction

This tutorial will demonstrate the use of HADDOCK for predicting the structure of a protein-protein complex from NMR chemical shift perturbation (CSP) data. Namely, we will dock two E. coli proteins involved in glucose transport: the glucose-specific enzyme IIA (E2A) and the histidine-containing phosphocarrier protein (HPr). 

[about glucose transport]

The structures in the free form have been determined using X-ray crystallography (E2A) (PDB ID [1F3G](https://www.ebi.ac.uk/pdbe/entry/pdb/1f3g){:target="_blank"}) and NMR spectroscopy (HPr) (PDB ID [1HDN](https://www.ebi.ac.uk/pdbe/entry/pdb/1hdn){:target="_blank"}). The structure of the native complex has also been determined with NMR (PDB ID [1GGR](https://www.ebi.ac.uk/pdbe/entry/pdb/1ggr){:target="_blank"}). These NMR experiments have also provided us with an array of data on the interaction itself (chemical shift perturbations, intermolecular NOEs, residual dipolar couplings, and simulated diffusion anisotropy data), which will be useful for the docking. For this tutorial, we will only make use of inteface residues identified from NMR chemical shift perturbation data as described in [Wang *et al*, EMBO J (2000)](https://doi.org/10.1093/emboj/19.21.5635){:target="_blank"}.

For this tutorial we will make use of the [HADDOCK2.4 webserver](https://wenmr.science.uu.nl/haddock2.4){:target="_blank"}.

{% include paper_citation.html key="haddock24" %}


Throughout the tutorial, coloured text will be used to refer to questions or instructions, and/or PyMOL commands.

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>

<hr>
## Setup

In order to run this tutorial you will need to have the following software installed: [PyMOL][link-pymol].

Also, if not provided with special workshop credentials to use the HADDOCK portal, make sure to register in order to be able to submit jobs. Use for this the following registration page: [https://wenmr.science.uu.nl/auth/register/haddock](https://wenmr.science.uu.nl/auth/register/haddock){:target="_blank"}.

<hr>
## HADDOCK general concepts

HADDOCK (see [https://www.bonvinlab.org/software/haddock2.4/](https://www.bonvinlab.org/software/haddock2.4/){:target="_blank"}) is a collection of python scripts derived from ARIA ([https://aria.pasteur.fr](https://aria.pasteur.fr){:target="_blank"}) that harness the power of CNS (Crystallography and NMR System – [https://cns-online.org](https://cns-online.org){:target="_blank"}) for structure calculation of molecular complexes. What distinguishes HADDOCK from other docking software is its ability, inherited from CNS, to incorporate experimental data as restraints and use these to guide the docking process alongside traditional energetics and shape complementarity. Moreover, the intimate coupling with CNS endows HADDOCK with the ability to actually produce models of sufficient quality to be archived in the Protein Data Bank.

A central aspect to HADDOCK is the definition of Ambiguous Interaction Restraints or AIRs. These allow the translation of raw data such as NMR chemical shift perturbation or mutagenesis experiments into distance restraints that are incorporated in the energy function used in the calculations. AIRs are defined through a list of residues that fall under two categories: active and passive. Generally, active residues are those of central importance for the interaction, such as residues whose knockouts abolish the interaction or those where the chemical shift perturbation is higher. Throughout the simulation, these active residues are restrained to be part of the interface, if possible, otherwise incurring in a scoring penalty. Passive residues are those that contribute for the interaction, but are deemed of less importance. If such a residue does not belong in the interface there is no scoring penalty. Hence, a careful selection of which residues are active and which are passive is critical for the success of the docking.
The docking protocol of HADDOCK was designed so that the molecules experience varying degrees of flexibility and different chemical environments, and it can be divided in three different stages, each with a defined goal and characteristics:


**1. Randomization of orientations and rigid-body minimization (it0)**
In this initial stage, the interacting partners are treated as rigid bodies, meaning that all geometrical parameters such as bonds lengths, bond angles, and dihedral angles are frozen. The partners are separated in space and rotated randomly about their centres of mass. This is followed by a rigid body energy minimization step, where the partners are allowed to rotate and translate to optimize the interaction. The role of AIRs in this stage is of particular importance. Since they are included in the energy function being minimized, the resulting complexes will be biased towards them. For example, defining a very strict set of AIRs leads to a very narrow sampling of the conformational space, meaning that the generated poses will be very similar. Conversely, very sparse restraints (e.g. the entire surface of a partner) will result in very different solutions, displaying greater variability in the region of binding.

<details >
<summary style="bold">
<b><i>See animation of rigid-body minimization (it0):</i></b>
</summary>
<figure align="center">
  <img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/haddock_mini.gif">
</figure>
</details>
<br>

**2. Semi-flexible simulated annealing in torsion angle space (it1)**
The second stage of the docking protocol introduces flexibility to the interacting partners through a three-step molecular dynamics-based refinement in order to optimize interface packing. It is worth noting that flexibility in torsion angle space means that bond lengths and angles are still frozen. The interacting partners are first kept rigid and only their orientations are optimized. Flexibility is then introduced in the interface, which is automatically defined based on an analysis of intermolecular contacts within a 5Å cut-off. This allows different binding poses coming from it0 to have different flexible regions defined. Residues belonging to this interface region are then allowed to move their side chains in a second refinement step. Finally, both backbone and side chains of the flexible interface are granted freedom. The AIRs again play an important role at this stage since they might drive conformational changes.

  <details >
  <summary style="bold">
  <b><i>See animation of semi-flexible simulated annealing (it1):</i></b>
  </summary>
  <figure align="center">
    <img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/haddock_sa.gif">
  </figure>
  </details>
  <br>

 **3. Refinement in Cartesian space with explicit solvent (water)**
 **Note:** This stage was part of the standard HADDOCK protocol up to (and including) v2.2. As of v2.4 it is no longer performed by default but the user still has the option of enabling it. In its place, a short energy minimisation is performed instead. The final stage of the docking protocol immerses the complex in a solvent shell so as to improve the energetics of the interaction. HADDOCK currently supports water (TIP3P model) and DMSO environments. The latter can be used as a membrane mimic. In this short explicit solvent refinement the models are subjected to a short molecular dynamics simulation at 300K, with position restraints on the non-interface heavy atoms. These restraints are later relaxed to allow all side chains to be optimized.

 <details >
 <summary style="bold">
 <b><i>See animation of refinement in explicit solvent (water):</i></b>
 </summary>
 <figure align="center">
   <img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/haddock_water.gif">
 </figure>
 </details>
 <br>



The performance of this protocol of course depends on the number of models generated at each step. Few models are less probable to capture the correct binding pose, while an exaggerated number will become computationally unreasonable. The standard HADDOCK protocol generates 1000 models in the rigid body minimization stage, and then refines the best 200 – regarding the energy function - in both it1 and water. Note, however, that while 1000 models are generated by default in it0, they are the result of five minimization trials and for each of these the 180º symmetrical solution is also sampled. Effectively, the 1000 models written to disk are thus the results of the sampling of 10.000 docking solutions.
The final models are automatically clustered based on a specific similarity measure - either the *positional interface ligand RMSD* (iL-RMSD) that captures conformational changes about the interface by fitting on the interface of the receptor (the first molecule) and calculating the RMSDs on the interface of the smaller partner, or the *fraction of common contacts* (current default) that measures the similarity of the intermolecular contacts. For RMSD clustering, the interface used in the calculation is automatically defined based on an analysis of all contacts made in all models.

<hr>
## Inspecting and preparing E2A for docking

We will now inspect the E2A structure. For this start PyMOL and in the command line window of PyMOL (indicated by PyMOL>) type:
<a class="prompt prompt-pymol">
fetch 1F3G<br>
show cartoon<br>
hide lines<br>
</a>

You should see a cartoon representation of the protein. 
It is known from the literature that a phosphate group interacts with the side chain of a histidine residue. 
Let us first check whether histidine residues are present in this structure.
<a class="prompt prompt-pymol">
show sticks, resn HIS<br>
</a>

The histidine side chains are now displayed in stick representation.  
You can zoom in on the histidines using:
<a class="prompt prompt-pymol">zoom resn HIS</a>

To return to the full view of the structure, type:
<a class="prompt prompt-pymol">zoom vis</a>

This structure has two histidines present. How about phosphate group? 
<a class="prompt prompt-question">Is there a phosphate group present in this structure?</a>

*Hint* : you can select phosphate atoms with the following command and check how many atoms are in this selection: 
<a class="prompt prompt-pymol">select elem P</a>

As a preparation step before docking, it is advised to remove any irrelevant water and other small molecules (e.g. small molecules from the crystallisation buffer), however do leave relevant co-factors if present. For E2A, the PDB file only contains water molecules. You can remove those in PyMOL by typing:
<a class="prompt prompt-pymol">remove resn HOH</a>

Now let's vizualize the residues affected by binding as identified by NMR. From [Wang *et al*, EMBO J (2000)](https://doi.org/10.1093/emboj/19.21.5635){:target="_blank"} the following residues of E2A were identified has having significant chemical shift perturbations:

<a class="prompt prompt-info">38,40,45,46,69,71,78,80,94,96,141</a>

We will now switch to a surface representation of the molecule and highlight the NMR-defined interface. In PyMOL type the following commands:
<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select e2a_active, (1F3G and resi 38,40,45,46,69,71,78,80,94,96,141)<br>
color red, e2a_active<br>
</a>

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/e2a-surface-airs.png">
</figure>

Inspect the surface.

<a class="prompt prompt-question">Do the identified residues form a well defined patch on the surface?</a>
<a class="prompt prompt-question">Do they form a contiguous surface?</a>

The answer to the last question should be no: we can observe residue in the center of the patch that do not seem significantly affected while still being in the middle of the defined interface. This is the reason why in HADDOCK we also define "*passive*" residues that correspond to surface neighbors of active residues. These can be selected manually, or more conveniently you can let the HADDOCK server do it for you (see [Setting up the docking run](#setting-up-the-docking-run) below).

As final step save the molecule as a new PDB file which we will call: *e2a_1F3G.pdb*<br>
For this in the PyMOL menu on top select:
<a class="prompt prompt-info">File -> Export molecule...</a>
<a class="prompt prompt-info">Click on the save button</a>
<a class="prompt prompt-info">Select as ouptut format PDB (*.pdb *.pdb.gz)</a>
<a class="prompt prompt-info">Name your file *e2a_1F3G.pdb* and note its location</a>

Another way to saves the structure as a PDB file is via the command:
<a class="prompt prompt-pymol">save e2a_1F3G.pdb, 1F3G</a>

The file will be written to the current working directory: if PyMOL was launched from a terminal, it will be saved in the directory from which PyMOL was started; if PyMOL was opened manually (e.g., via the graphical interface), it is typically saved in your home directory.

After saving the molecule delete it from the PyMOL window or close PyMOL. You can remove the molecule by:
<a class="prompt prompt-pymol">
delete 1F3G
</a>

<hr>
## Inspecting and preparing HPR for docking

We will now inspect the HPR structure. For this start PyMOL and in the command line window of PyMOL type:
<a class="prompt prompt-pymol">
fetch 1HDN<br>
show cartoon<br>
hide lines<br>
</a>

<a class="prompt prompt-question">Are there any histidines present in this structure?</a>
<a class="prompt prompt-question">Is there a phosphate group present in this structure?</a>

Since this is an NMR structure it does not contain any water molecules and we don't need to remove them.

Let's vizualize the residues affected by binding as identified by NMR. From [Wang *et al*, EMBO J (2000)](https://doi.org/10.1093/emboj/19.21.5635){:target="_blank"} the following residues were identified has having significant chemical shift perturbations:

<a class="prompt prompt-info">15,16,17,20,48,49,51,52,54,56</a>

We will now switch to a surface representation of the molecule and highlight the NMR-defined interface. In PyMOL type the following commands:
<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select hpr_active, (1HDN and resi 15,16,17,20,48,49,51,52,54,56)<br>
color red, hpr_active<br>
</a>

Again, inspect the surface.

<a class="prompt prompt-question">Do the identified residues form a well defined patch on the surface?</a>
<a class="prompt prompt-question">Do they form a contiguous surface?</a>

You may have noticed that the set of PyMOL commands above took slightly longer to execute compared to similar commend for E2A.
This is because 1HDN is an NMR structure. Unlike X-ray structures, NMR entries often contain an ensemble of models - in this case, 30 conformers.

You can display all 30 models in quick succession and in a loop using:
<a class="prompt prompt-pymol"> mplay </a>
To stop the playback:
<a class="prompt prompt-pymol"> mstop </a>


HADDOCK is able to handle such ensembles by using each conformer in turn as a starting point for docking. 
We generally recommend limiting the number of conformers used. 
Otherwise, the number of possible combinations between the input molecules can quickly explode (i.e. become very large).
For example, if both partners contain 10 conformers, this results in 100 possible starting combinations. If 1000 rigid-body models are generated (see [HADDOCK general concepts](#haddock-general-concepts) above), each combination would then be sampled only 10 times!

In case if limiting number of input conformers is an unreasonable choice, it is possible to increase the number of models generated in the rigid-body docking stage (it0).
However, this requires elevated access privileges on the HADDOCK 2.4 server. 

Now let's display all models of this NMR ensemble simultaneously in ribbon representation. 
This representation is handy for visualizing backbone conformation:
<a class="prompt prompt-pymol">
hide all<br>
show ribbon<br>
set all_states, on<br>
</a>

You should now be seing the 30 conformers present in this NMR structure. 
It may appear that conformation is fairly conserved between the models, so let us look at the side chains of the active residues:
<a class="prompt prompt-pymol">
show lines, hpr_active<br>
</a>

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/hpr-ensemble.png">
</figure>

You should now be able to observe the range of conformational space sampled by these surface side chains. 
Some residues clearly adopt a wide variety of conformations, and one of these might lead to much better docking results.
This illustrates the potential benefit of using an ensemble of conformations as starting points rather than a single structure, especially when there is no clear indication of which 1 out of the 30 models would be best for the docking.

As final step, save the molecule as a new PDB file which we will call: *hpr-ensemble.pdb*
For this in the PyMOL menu select:
<a class="prompt prompt-info">File -> Export molecule...</a>
<a class="prompt prompt-info">Select as State 0 (all states)</a>
<a class="prompt prompt-info">Click on Save...</a>
<a class="prompt prompt-info">Select as ouptut format PDB (*.pdb *.pdb.gz)</a>
<a class="prompt prompt-info">Name your file *hpr-ensemble.pdb* and note its location</a>

**Note:** that it is important to change "State" from the default "-1" to "0". Otherwise a single conformation will be saved instead of the multiple ones.

<hr>
## Adding a phosphate group

Since the biological function of this complex is to transfer a phosphate group from one protein to another via histidine side chains, it is important that the phosphate group be present during docking.
Yet both the structures we prepared and saved do not currently contain any phosphate group.

As a reminder (see [Introduction](#introduction) above), in bacteria the phosphate group is transferred between histidine residues of the interacting proteins.
From the literature it is known that in E2A histidine 90 is involved in this transfer.
We can include phosphate group into the docking by modifying this canonical histidine into a phosphorylated histidine, i.e. histidine with covalently attached phosphate group.

HADDOCK supports a number of modified amino acids, which can be found at:  
[https://wenmr.science.uu.nl/haddock2.4/library](https://wenmr.science.uu.nl/haddock2.4/library){:target="_blank"}.

<a class="prompt prompt-question">Check the list of supported modified amino acids. What is the proper residue name for a phosphorylated histidine in HADDOCK?</a>

To use a modified amino acid in HADDOCK, it is sufficient to edit the PDB file and change the residue name of the corresponding residue. There is no need to add or delete atoms - HADDOCK will take care of this automatically.

To introduce this modification:
<a class="prompt prompt-info">Open the PDB file *e2a_1F3G.pdb* in your favorite text editor</a>
<a class="prompt prompt-info">Find histidine with residue sequence number equal to 90</a> 
Remember that residue sequence number is the second integer value in the line starting with "ATOM". Check [this link](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html){:target="_blank"} for more info.
<a class="prompt prompt-info">Change this residue name to NEP</a>
<a class="prompt prompt-info">Save the file under a new name, e.g. *e2aP_1F3G.pdb*</a>

**Note:** The same procedure can also be used to introduce mutations in an input protein structure.

<hr>
## Setting up the docking run

#### Registration / Login

In order to use HADDOCK web server, you need to navigate to [wenmr portal](https://wenmr.science.uu.nl/auth/){:target="_blank"} and login. 
After successful validation of credentials, scroll down to "Services", locate **HADDOCK v2.4** and click on "Go to service". Or use this link: [https://wenmr.science.uu.nl/haddock2.4/](https://wenmr.science.uu.nl/haddock2.4/){:target="_blank"}.

#### HADDOCK submission: Input data

Locate "[Submit a new job](https://wenmr.science.uu.nl/haddock2.4/submit/1){:target="_blank"}" button. Note that you are now in "Input data" tab.

In this stage of the submission process we will upload the structures we previously prepared with PyMOL.

* **Step1:** In the field "Job name", define a name for your docking run, e.g. *E2A-HPR*.

* **Step2:** In the field "Number of molecules", select the number of molecules to dock, in this case 2.

* **Step3:** In the section "Molecule 1 - input", upload the PDB file for E2A.   

<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *e2aP_1F3G.pdb* (the file you edited to modify the histidine)
</a>

Leave all other options to their default values. 
**_Note_** that you can fold and unfold the "Molecule 1 - input" section by clicking on the ▼ icon. This works for any section and subsection of HADDOCK server.

* **Step4:** In the subsection "Molecule 2 - input", upload the PDB file for HPR. 

<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *hpr-ensemble.pdb* (the ensemble of NMR conformations you saved)
</a>

**_Note_** that HADDOCK server will automatically adjust several docking parameters based on the field "What kind of molecule are you docking?". 

* **Step 5:** Click on the "Next" button at the bottom left of the interface. 

This will upload the structures to the HADDOCK webserver where they will be processed and validated (checked for formatting errors). The server makes use of [Molprobity](http://molprobity.biochem.duke.edu/){:target="_blank"} to check side chain conformations, eventually swap them (e.g. for asparagines) and define the protonation state of histidine residues.


#### HADDOCK submission: Input parameters

If processing and validation of the input files run without errors, you will be brought to the "Input parameters" tab. In case any issues had occurred - you will remain in the "Input data" tab and the error message will be shown either on top of the page or in the subsection for one of the molecules. 

##### Definition of restraints

In this tab, we will define distance restraints by specify active residues for each molecule.

* **Step 6:** In the section "Molecule 1 - parameters", in the subsection "Active/Passive residues - Selection #1", in the field "Active residues (directly involved in the interaction)", specify the active residues for E2A.

**_Note_** that "residue sequence number" and "residue ID" are equivalent terms. 

<a class="prompt prompt-info">
Active residues (directly involved in the interaction) -> 38,40,45,46,69,71,78,80,94,96,141
</a>
<a class="prompt prompt-info">Automatically define passive residues around the active residues -> check (checked by default)
</a>

* **Step 7:** In the section "Molecule 2 - parameters", in the subsection "Active/Passive residues - Selection #2", in the field "Active residues (directly involved in the interaction)", specify the active residues for the HPR.

<a class="prompt prompt-info">
Active residues (directly involved in the interaction) -> 15,16,17,20,48,49,51,52,54,56
</a>
<a class="prompt prompt-info">Automatically define passive residues around the active residues -> check (checked by default)
</a>

##### Checking the histidines protonation state

The HADDOCK server assigns the protonation states of histidines automatically using [MolProbity](http://molprobity.biochem.duke.edu/){:target="_blank"}.
However, we know that the histidine of HPR that is expected to interact with the phosphate group should be positively charged.
From the literature, this residue in HPR is most likely histidine 15. Let's make sure this histidine is positively charged. 

* **Step 8:** In the section "Molecule 2 - parameters", unfold the subsection "Histidine protonation state" and check the defined protonation state of HIS 15.

<a class="prompt prompt-info">
Change the state of HIS 15 to "HIS+" 
</a>


* **Step 9:** Click on the "Next" button at the bottom left of the interface.


#### HADDOCK submission: Docking parameters

This interface allows us to modify many parameters that control the behaviour of HADDOCK but in our case the default values are all appropriate. The best way to learn more about these parameters is by completing the other HADDOCK 2.4 tutorials. 

<a class="prompt prompt-info"> Scroll to the bottom of the page. </a>

Here you should see buttons "Download parameter file" and "Download input files". The "parameter file" is a json that contains all the settings of the run. We strongly recommend to download and keep this file - this will allow you to run reproducible experiments. With this file, you can use [HADDOCK File Upload Interface](https://wenmr.science.uu.nl/haddock2.4/submit_file){:target="_blank"} to repeat the run with exact same parameters. This file can also be edited to change a one or a few parameters - it's quicker than repeating all submission steps. An excerpt of this file is shown here:
<pre>
{
    "amb_cool1": 10.0,
    "amb_cool2": 50.0,
    "amb_cool3": 50.0,
    "amb_firstit": 0,
    "amb_hot": 10.0,
    "amb_lastit": 2,
    "anastruc_1": 200,
...
</pre>

The "input files" is a tar archive that contains all files HADDOCK will use during the run. For example, in this archive you will se 30 separate PDB file titled _protein2_1.pdb_, _protein2_2.pdb_ ... _protein2_30.pdb_ - these are individual conformations extracted from _hpr_ensemble.pdb_ we uploaded earlier. Another example is _ambig.tbl_ - ths file will contain an actual list of distance restraints created based on the active residues we selected earlier. Lastly, *job_params.json* is the "parameter file" discussed above.

* **Step 10:** Click on the "Submit" button at the bottom left of the interface.

##### Your job has been successfully processed!

Upon submission you will be presented with a web page with a message "Your job has been successfully processed!". This page allows you to track the execution of the run and also download "parameter file".

At first your job will have status "Processed", then "Queued", and eventually it will change to "Running" and you will see progress bar moving along each stage. 

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/running.png">
</figure>

This run will take between 30 minutes to several hours - depending on the load of the server. You will be notified by email once your job has been completed.

You do not have to keep this page open, all resent jobs can be accessed via the "[Workspace](https://wenmr.science.uu.nl/haddock2.4/workspace){:target="_blank"}" button in the navigation bar.

<hr>
## Analysing the results

Once your run has completed you will be presented with a result page showing the cluster statistics and some graphical representation of the data (and if registered, you will also be notified by email). Such an example output page can be found [here](https://wenmr.science.uu.nl/haddock2.4/run/4242424242/195967-E2A-HPR){:target="_blank"} in case you don't want to wait for the results of your docking run.

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/HADDOCK-result-page.png">
</figure>

<a class="prompt prompt-question">Inspect the result page</a>
<a class="prompt prompt-question">How many clusters are generated?</a>

**Note:** The bottom of the page gives you some graphical representations of the results, showing the distribution of the solutions for various measures (HADDOCK score, van der Waals energy, ...) as a function of the Fraction of Common Contact with- and RMSD from the best generated model (the best scoring model). The graphs are interactive and you can turn on and off specific clusters, but also zoom in on specific areas of the plot.

The bottom graphs show you the distribution of scores (Evdw, Eelec and Edesol) for the various clusters.


<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/HADDOCK-result-graph.png">
</figure>

The ranking of the clusters is based on the average score of the top 4 members of each cluster. The score is calculated as:
<pre>
      HADDOCKscore = 1.0 * Evdw + 0.2 * Eelec + 1.0 * Edesol + 0.1 * Eair
</pre>
where Evdw is the intermolecular van der Waals energy, Eelec the intermolecular electrostatic energy, Edesol represents an empirical desolvation energy term adapted from Fernandez-Recio *et al.* J. Mol. Biol. 2004, and Eair the AIR energy. The cluster numbering reflects the size of the cluster, with cluster 1 being the most populated cluster. The various components of the HADDOCK score are also reported for each cluster on the results web page.

<a class="prompt prompt-question">Consider the cluster scores and their standard deviations.</a>
<a class="prompt prompt-question">Is the top ranked cluster significantly better than the second one? (This is also reflected in the z-score).</a>

In case the scores of various clusters are within standard devatiation from each other, all should be considered as a valid solution for the docking. Ideally, some additional independent experimental information should be available to decide on the best solution. In this case we do have such a piece of information: the phosphate transfer mechanism (see [Biological insights](#biological-insights) below).


**Note:** The type of calculations performed by HADDOCK does have some chaotic nature, meaning that you will only get exactly the same results if you are running on the same hardware, operating system and using the same executable. The HADDOCK server makes use of [EGI](https://www.egi.eu)/[EOSC](https://www.eosc-hub.eu){:target="_blank"} high throughput computing (HTC) resources to distribute the jobs over a wide grid of computers worldwide. As such, your results might look slightly different from what is presented in the [example output page](https://wenmr.science.uu.nl/haddock2.4/run/4242424242/E2A-HPR){:target="_blank"}. That run was run on our local cluster. Small differences in scores are to be expected, but the overall picture should be consistent.



<hr>
## Visualisation

The new HADDOCK2.4 server integrates the NGL viewer which allows you to quickly visualize a specific structure. For that click on the "eye" icon next to a structure.

In order to compare the various clusters we will however download the models and inspect them using PyMol.
<a class="prompt prompt-info">Download and save to disk the first model of each cluster (use the PDB format)</a>

Then start PyMOL and load each cluster representative:
<a class="prompt prompt-pymol">File menu -> Open -> select cluster1_1.pdb</a>

Repeat this for each cluster. Once all files have been loaded:
<a class="prompt prompt-pymol">
show cartoon<br>
util.cbc<br>
hide lines<br>
</a>

Let's then superimpose all models on chain A of the first cluster:
<a class="prompt prompt-pymol">
select cluster1_1 and chain A<br>
alignto sele<br>
</a>

This will align all clusters on chain A (E2A), maximizing the differences in the orientation of chain B (HPR).

<a class="prompt prompt-question">
Examine the various clusters. How does the orientation of HPR differ between them?
</a>

**Note:** You can turn on and off a cluster by clicking on its name in the right panel of the PyMOL window.

Let's now check if the active residues which we defined are actually part of the interface. In the PyMOL command window type:
<a class="prompt prompt-pymol">
select e2a_active, (resi 38,40,45,46,69,71,78,80,94,96,141) and chain A<br>
select hpr_active, (resi 15,16,17,20,48,49,51,52,54,56) and chain B<br>
color red, e2a_active<br>
color orange, hpr_active<br>
</a>

<a class="prompt prompt-question">
Are the active residues in the interface?
</a>

<hr>
## Biological insights

The E2A-HPR complex is involved in phosphate-transfer, in which a phosphate group attached to histidine 90 of E2A (which we named NEP) is transferred to a histidine of HPR. As such, the docking models should make sense according to this information, meaning that two histidines should be in close proximity at the interface. Using PyMOL, check the various cluster representatives (we are assuming here you have performed all PyMOL commands of the previous section):
<a class="prompt prompt-pymol">
select histidines, resn HIS+NEP<br>
show spheres, histidines<br>
util.cnc<br>
</a>

<a class="prompt prompt-question">First of all, has the phosphate group been properly generated?</a>

**Note:** You can zoom on the phosphorylated histidine using the following PyMOL command:

<a class="prompt prompt-pymol">
zoom resn NEP<br>
</a>

<figure align="center">
<img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/phosphorylated-histidine.png">
</figure>

Zoom back to all visible molecules with:
<a class="prompt prompt-pymol">
zoom vis<br>
</a>

Now inspect each cluster in turn and check if histidine 90 of E2A is in close proximity to another histidine of HPR.
To facilitate this analysis, view each cluster in turn (use the right panel to activate/desactivate the various clusters by clicking on their name).

<a class="prompt prompt-question">Based on this analysis, which cluster does satisfy best the biolocal information?</a>

<a class="prompt prompt-question">Is this cluster also the best ranked one?</a>

<hr>
## Comparison with the reference structure

As explained in the introduction, the structure of the native complex has been determined by NMR (PDB ID [1GGR](https://www.ebi.ac.uk/pdbe/entry/pdb/1ggr){:target="_blank"}) using a combination of intermolecular NOEs and dipolar coupling restraints. We will now compare the docking models with this structure.

If you still have all cluster representative open in PyMOL you can proceed with the sub-sequent analysis, otherwise load again each cluster representative as described above. Then, fetch the reference complex by typing in PyMOL:
<a class="prompt prompt-pymol">
fetch 1GGR<br>
show cartoon<br>
color yellow, 1GGR and chain A<br>
color orange, 1GGR and chain B<br>
</a>

The number of chain B in this structure is however different from the HPR numbering in the structure we used: It starts at 301 while in our models chain B starts at 1. We can change the residue numbering easily in PyMol with the following command:
<a class="prompt prompt-pymol">
alter (chain B and 1GGR), resv -=300<br>
</a>

Then superimpose all cluster representatives on the reference structure, using the entire chain A (E2A):
<a class="prompt prompt-pymol">
select 1GGR and chain A<br>
alignto sele<br>
</a>

<a class="prompt prompt-question">
Does any of the cluster representatives ressemble the reference NMR structure?
</a>
<a class="prompt prompt-question">
In case you found a reasonable prediction, what is its cluster rank?
</a>

In the blind protein-protein prediction experiment [CAPRI](https://capri.ebi.ac.uk/){:target="_blank"} (Critical PRediction of Interactions), a measure of the quality of a model is the so-called ligand-RMSD (l-RMSD). It is calculated by fitting on the receptor chain (E2A or chain A in our case) and calculating the RMSD on the backbone of the ligand (HPR or chain B in our case). This can be done in PyMOL with the following command:
<a class="prompt prompt-pymol">
rms_cur cluster1_1 and chain B, 1GGR<br>
</a>

**Note:** If "rms_cur" fails on your machine, use this command instead:
<a class="prompt prompt-pymol">
align cluster1_1, 1GGR, cycles=0<br>
</a>

This will align the two structures based on the all-atom RMSD, different from the ligand-RMSD (l-RMSD) that you can calculate with rms_cur and the above commands.

In CAPRI, the l-RMSD value defines the quality of a model:
* acceptable model: l-RMSD<10Å
* medium quality model: l-RMSD<5Å
* high quality model: l-RMSD<1Å

<a class="prompt prompt-question">
What is based on this CAPRI criterion the quality of the best model?
</a>

<hr>
## Congratulations! 🎉

You have completed this tutorial. If you have any questions or suggestions, feel free to contact us via email or asking a question through our [support center](https://ask.bioexcel.eu){:target="_blank"}.

<hr>
## Additional docking runs

If you are curious and want learn more about HADDOCK and the impact of the input data on the docking results, consider performing and analysing, as described above, the following runs:

* Same run as above, but without defining the phosphorylated histidine;
* Same run as above, but using only the first model of the HPR ensemble - you can either open ensemble in PyMOL and save the 1st state only, or manually copy "MODEL 1" from file using text editor, or use [PDBTOOLS](https://wenmr.science.uu.nl/pdbtools/submit){:target="_blank"}.

Don't hesitate to browse [education](/education) page, you will find more tutorials these!

[link-pymol]: https://www.pymol.org/ "PyMOL"
