---
layout: page
title: "HADDOCK basic protein-protein docking tutorial"
excerpt: "A small tutorial on predicting a protein-protein complex using interface residues identified from NMR chemical shift perturbation experiments"
tags: [HADDOCK, NMR, docking, dimer, chemical shifts]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* [Introduction](#introduction)
* [Setup](#setup)
* [HADDOCK general concepts](#haddock-general-concepts)
* [Inspecting and preparing E2A for docking](#inspecting-and-preparing-e2a-for-docking)
* [Inspecting and preparing HPR for docking](#inspecting-and-preparing-hpr-for-docking)
* [Adding a phosphate group](#adding-a-phosphate-group)
* [Setting up the docking run](#setting-up-the-docking-run)
* [Analysing the results](#analysing-the-results)
* [Biological insights](#biological-insights)
* [Comparison with the reference structure](#comparison-with-the-reference-structure)
* [Additional docking runs](#additional-docking-runs)

<hr>
## Introduction

This tutorial will demonstrate the use of HADDOCK for predicting the structure of a protein-protein complex from NMR chemical shift perturbation (CSP) data. Namely, we will dock two E. coli proteins involved in glucose transport: the glucose-specific enzyme IIA (E2A) and the histidine-containing phosphocarrier protein (HPr). The structures in the free form have been determined using X-ray crystallography (E2A) (PDB ID [1F3G](http://www.ebi.ac.uk/pdbe/entry/search/index?text:1F3G)) and NMR spectroscopy (HPr) (PDB ID [1HDN](http://www.ebi.ac.uk/pdbe/entry/search/index?text:1HDN)). The structure of the native complex has also been determined with NMR (PDB ID [1GGR](http://www.ebi.ac.uk/pdbe/entry/search/index?text:1GGR)). These NMR experiments have also provided us with an array of data on the interaction itself (chemical shift perturbations, intermolecular NOEs, residual dipolar couplings, and simulated diffusion anisotropy data), which will be useful for the docking. For this tutorial, we will only make use of inteface residues identified from NMR chemical shift perturbation data as described in [Wang *et al*, EMBO J (2000)](http://onlinelibrary.wiley.com/doi/10.1093/emboj/19.21.5635/abstract).

For this tutorial we will make use of the H[ADDOCK2.2 webserver](http://haddock.science.uu.nl/services/HADDOCK2.2).
A description of our web server can be found in the following publications:

* G.C.P van Zundert, J.P.G.L.M. Rodrigues, M. Trellet, C. Schmitz, P.L. Kastritis, E. Karaca, A.S.J. Melquiond, M. van Dijk, S.J. de Vries and  A.M.J.J. Bonvin.
[The HADDOCK2.2 webserver: User-friendly integrative modeling of biomolecular complexes](http://dx.doi.org/doi:10.1016/j.jmb.2015.09.014).
_J. Mol. Biol._, *428*, 720-725 (2015).

* S.J. de Vries, M. van Dijk and A.M.J.J. Bonvin.
[The HADDOCK web server for data-driven biomolecular docking.](http://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html)
_Nature Protocols_, *5*, 883-897 (2010).  Download the final author version <a href="http://igitur-archive.library.uu.nl/chem/2011-0314-200252/UUindex.html">here</a>.

Throughout the tutorial, coloured text will be used to refer to questions or 
instructions, and/or PyMOL commands.

<a class="prompt prompt-question">This is a question prompt: try answering 
it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the 
PyMOL command line prompt!</a>


<hr>
## Setup

In order to run this tutorial you will need to have the following software installed: [PyMOL][link-pymol].

Also, if not provided with special workshop credentials to use the HADDOCK portal, make sure to register in order to be able to submit jobs. Use for this the following registration page: [http://haddock.science.uu.nl/services/HADDOCK2.2/signup.html](http://haddock.science.uu.nl/services/HADDOCK2.2/signup.html).

<hr>
## HADDOCK general concepts

HADDOCK (see [http://www.bonvinlab.org/software/haddock2.2/haddock.html](http://www.bonvinlab.org/software/haddock2.2/haddock.html)) is a collection of python scripts derived from ARIA ([http://aria.pasteur.fr](http://aria.pasteur.fr)) that harness the power of CNS (Crystallography and NMR System – [http://cns-online.org](http://cns-online.org)) for structure calculation of molecular complexes. What distinguishes HADDOCK from other docking software is its ability, inherited from CNS, to incorporate experimental data as restraints and use these to guide the docking process alongside traditional energetics and shape complementarity. Moreover, the intimate coupling with CNS endows HADDOCK with the ability to actually produce models of sufficient quality to be archived in the Protein Data Bank. 

A central aspect to HADDOCK is the definition of Ambiguous Interaction Restraints or AIRs. These allow the translation of raw data such as NMR chemical shift perturbation or mutagenesis experiments into distance restraints that are incorporated in the energy function used in the calculations. AIRs are defined through a list of residues that fall under two categories: active and passive. Generally, active residues are those of central importance for the interaction, such as residues whose knockouts abolish the interaction or those where the chemical shift perturbation is higher. Throughout the simulation, these active residues are restrained to be part of the interface, if possible, otherwise incurring in a scoring penalty. Passive residues are those that contribute for the interaction, but are deemed of less importance. If such a residue does not belong in the interface there is no scoring penalty. Hence, a careful selection of which residues are active and which are passive is critical for the success of the docking. 

The docking protocol of HADDOCK was designed so that the molecules experience varying degrees of flexibility and different chemical environments, and it can be divided in three different stages, each with a defined goal and characteristics:

* **1. Randomization of orientations and rigid-body minimization (it0)** <BR>
In this initial stage, the interacting partners are treated as rigid bodies, meaning that all geometrical parameters such as bonds lengths, bond angles, and dihedral angles are frozen. The partners are separated in space and rotated randomly about their centres of mass. This is followed by a rigid body energy minimization step, where the partners are allowed to rotate and translate to optimize the interaction.
The role of AIRs in this stage is of particular importance. Since they are included in the energy function being minimized, the resulting complexes will be biased towards them. For example, defining a very strict set of AIRs leads to a very narrow sampling of the conformational space, meaning that the generated poses will be very similar. Conversely, very sparse restraints (e.g. the entire surface of a partner) will result in very different solutions, displaying greater variability in the region of binding.

* **2. Semi-flexible simulated annealing in torsion angle space (it1)** <BR>
The second stage of the docking protocol introduces flexibility to the interacting partners through a three-step molecular dynamics-based refinement in order to optimize interface packing. It is worth noting that flexibility in torsion angle space means that bond lengths and angles are still frozen. The interacting partners are first kept rigid and only their orientations are optimized. Flexibility is then introduced in the interface, which is automatically defined based on an analysis of intermolecular contacts within a 5Å cut-off. This allows different binding poses coming from it0 to have different flexible regions defined. Residues belonging to this interface region are then allowed to move their side-chains in a second refinement step. Finally, both backbone and side-chains of the flexible interface are granted freedom.
The AIRs again play an important role at this stage since they might drive conformational changes.

* **3. Refinement in Cartesian space with explicit solvent (water)** <BR>
The final stage of the docking protocol immerses the complex in a solvent shell so as to improve the energetics of the interaction. HADDOCK currently supports water (TIP3P model) and DMSO environments. The latter can be used as a membrane mimic. In this short explicit solvent refinement the models are subjected to a short molecular dynamics simulation at 300K, with position restraints on the non-interface heavy atoms. These restraints are later relaxed to allow all side chains to be optimized.

The performance of this protocol of course depends on the number of models generated at each step. Few models are less probable to capture the correct binding pose, while an exaggerated number will become computationally unreasonable. The standard HADDOCK protocol generates 1000 models in the rigid body minimization stage, and then refines the best 200 – regarding the energy function - in both it1 and water. Note, however, that while 1000 models are generated by default in it0, they are the result of five minimization trials and for each of these the 180º symmetrical solution is also sampled. Effectively, the 1000 models written to disk are thus the results of the sampling of 10.000 docking solutions.

The final models are automatically clustered based on a specific similarity measure – positional interface ligand RMSD (iL-RMSD) – that captures conformational changes about the interface by fitting on the interface of the receptor (the first molecule) and calculating the RMSDs on the interface of the smaller partner. The interface used in this calculation is automatically defined based on an analysis of all contacts made in all models. 


<hr>
## Inspecting and preparing E2A for docking

We will now inspect the E2A structure. For this start PyMOL and in the command line window of PyMOL (indicated by PyMOL>) type:

<a class="prompt prompt-pymol">
fetch 1F3G<br>
show cartoon<br>
hide lines<br>
show sticks, resn HIS<br>
</a>

You should see a backbone representation of the protein with only the histidine side-chains visible.
Try to locate the histidines in this structure.

<a class="prompt prompt-question">Is there any phosphate group present in this structure?</a>

Note that you can zoom on the histidines by typing in PyMOL:

<a class="prompt prompt-pymol">zoom resn HIS</a>

Revert to a full view with:

<a class="prompt prompt-pymol">zoom vis</a>

As a preparation step before docking, it is advised to remove any irrelevant water and other small molecules (e.g. small molecules from the crystallisation buffer), however do leave relevant co-factors if present. For E2A, the PDB file only contains water molecules. You can remove those in PyMOL by typing:

<a class="prompt prompt-pymol">remove resn HOH</a>

Now let's vizualize the residues affected by binding as identified by NMR. From [Wang *et al*, EMBO J (2000)](http://onlinelibrary.wiley.com/doi/10.1093/emboj/19.21.5635/abstract) the following residues of E2A were identified has having significant chemical shift perturbations:

<a class="prompt prompt-info">38,40,45,46,69,71,78,80,94,96,141</a>

We will now switch to a surface representation of the molecule and highlight the NMR-defined interface. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select e2a_active, (resi 38,40,45,46,69,71,78,80,94,96,141)<br>
color red, e2a_active<br>
</a>

<figure align="center">
<img src="/education/HADDOCK-protein-protein-basic/e2a-surface-airs.png">
</figure>

Inspect the surface.

<a class="prompt prompt-question">Do the identified residues form a well defined patch on the surface?</a>
<a class="prompt prompt-question">Do they form a contiguous surface?</a>

The answer to the last question should be no: We can observe residue in the center of the patch that do not seem significantly affected while still being in the middle of the defined interface. This is the reason why in HADDOCK we also define "*passive*" residues that correspond to surface neighbors of active residues. These can be selected manually, or more conveniently you can let the HADDOCK server do it for you (see [Setting up the docking run](#setting-up-the-docking-run) below).

As final step save the molecule as a new PDB file which we will call: *e2a_1F3G.pdb*<br>
For this in the PyMOL menu on top select:

<a class="prompt prompt-info">File -> Save molecule...</a>
<a class="prompt prompt-info">Select 1F3G and click on the save button</a>
<a class="prompt prompt-info">Name your file *e2a_1F3G.pdb* and note its location</a>


<hr>
## Inspecting and preparing HPR for docking

We will now inspect the HPR structure. For this start PyMOL and in the command line window of PyMOL type:

<a class="prompt prompt-pymol">
fetch 1HDN<br>
show cartoon<br>
hide lines<br>
</a>

Since this is an NMR structure it does not contain any water molecules and we don't need to remove them.

Let's vizualize the residues affected by binding as identified by NMR. From [Wang *et al*, EMBO J (2000)](http://onlinelibrary.wiley.com/doi/10.1093/emboj/19.21.5635/abstract) the following residues were identified has having significant chemical shift perturbations:

<a class="prompt prompt-info">15,16,17,20,48,49,51,52,54,56</a>

We will now switch to a surface representation of the molecule and highlight the NMR-defined interface. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select hpr_active, (resi 15,16,17,20,48,49,51,52,54,56)<br>
color red, hpr_active<br>
</a>

Again, inspect the surface.

<a class="prompt prompt-question">Do the identified residues form a well defined patch on the surface?</a>
<a class="prompt prompt-question">Do they form a contiguous surface?</a>

Now since this is an NMR structure, it actually consists of an ensemble of models. HADDOCK can handle such ensemble, using each conformer in turn as starting point for the docking. We however recommend to limit the number of conformers used for docking, since the number of conformer combinations of the input molecules might explode (e.g. 10 conformers each will give 100 starting combinations and if we generate 1000 ridig body models (see [HADDOCK general concepts](#haddock-general-concepts) above) each combination will only be sampled 10 times). 

Now let's vizualise this NMR ensemble. In PyMOL type:

<a class="prompt prompt-pymol">
hide all<br>
show ribbon<br>
set all_states, on<br>
</a>

You should now be seing the 20 conformers present in this NMR structure. To illustrate the potential benefit of using an ensemble of conformations as starting point for docking let's look at the side-chains of the active residues:

<a class="prompt prompt-pymol">
show lines, hpr_active<br>
</a>

<figure align="center">
<img src="/education/HADDOCK-protein-protein-basic/hpr-ensemble.png">
</figure>

You should be able to see the amount of conformational space sampled by those surface side-chains. You can clearly see that some residues do sample a large variety of conformations, one of which might lead to much better docking results. 

**Note:** Pre-sampling of possible conformational changes can thus be beneficial for the docking, but again do limit the number of conformers used for the docking (or increase the number of sampled models, which is possible in the [expert interface](http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-expert.html) of the HADDOCK portal - the default access level is however only easy - for a higher level access do request it via email).

As final step, save the molecule as a new PDB file which we will call: *hpr-ensemble.pdb*
For this in the PyMOL menu select:

<a class="prompt prompt-info">File -> Save molecule...</a>
<a class="prompt prompt-info">Select 1HDN and click on the save button</a>
<a class="prompt prompt-info">Name your file *hpr-ensemble.pdb* and note its location</a>


<hr>
## Adding a phosphate group

Since the biological function of this complex is to transfer a phosphate group from one protein to another, via histidines side-chains, it is relevant to make sure that a phosphate group be present for docking. As we have seen above none is currently present in the PDB files. HADDOCK does support a list of modified amino acids which you can find at the following link: [http://haddock.science.uu.nl/services/HADDOCK2.2/library.html](http://haddock.science.uu.nl/services/HADDOCK2.2/library.html). 

<a class="prompt prompt-question">Check the list of supported modified amino acids.</a>
<a class="prompt prompt-question">What is the proper residue name for a phospho-histidine in HADDOCK?</a>

In order to use a modified amino-acid in HADDOCK, the only thing you will need to do is to edit the PDB file and change the residue name of the amino-acid you want to modify. Don't bother deleting irrelevant atoms or adding missing ones, HADDOCK will take care of that. For E2A, the histidine that is phosphorylated has residue number 90. In order to change it to a phosphorylated histidine do the following:

<a class="prompt prompt-info">Edit the PDB file (*e2a_1F3G.pdb*) in your favorite editor</a>
<a class="prompt prompt-info">Change the name of histidine 90 to NEP </a>
<a class="prompt prompt-info">Save the file (as simple text file) under a new name, e.g. *e2aP_1F3G.pdb*</a>

**Note:** The same procedure can be used to introduce a mutation in an input protein structure.



<hr>
## Setting up the docking run

We will now launch the docking run. For this we will make us of the [easy interface](http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-easy.html) of the HADDOCK web server:

<a class="prompt prompt-info">
http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-easy.html
</a>

**Note:** The blue bars on the server can be folded/unfolded by clicking on the arrow on the right


* **Step1:** Define a name for your docking run, e.g. *E2A-HPR*.

* **Step2:** Input the first protein PDB file. For this unfold the **First Molecule menu**.

<a class="prompt prompt-info">
First molecule: where is the structure provided? -> "I am submitting it"
</a>
<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *e2aP_1F3G.pdb* (the file you edited to modify the histidine)
</a>
<a class="prompt prompt-info">
Active residues (directly involved in the interaction) -> 38,40,45,46,69,71,78,80,94,96,141
</a>
<a class="prompt prompt-info">Define passive residues automatically around the active residues -> check box
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> A
</a>

* **Step3:** Input the proteins PDB files. For this unfold the **Second Molecule menu**.

<a class="prompt prompt-info">
First molecule: where is the structure provided? -> "I am submitting it"
</a>
<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *hpr-ensemble.pdb* (the file you saved)
</a>
<a class="prompt prompt-info">
Active residues (directly involved in the interaction) -> 15,16,17,20,48,49,51,52,54,56
</a>
<a class="prompt prompt-info">Define passive residues automatically around the active residues -> check box
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> B
</a>

* **Step 4:** You are ready to submit! 

<a class="prompt prompt-info">
Enter your username and password (or the course credentials provided to you).
</a>



<hr>
## Analysing the results

Once your run has completed you will be presented with a result page showing the cluster statistics and some graphical representation of the data (and if registered, you will also be notified by email). Such an example output page can be found [here](http://haddock.science.uu.nl/services/HADDOCK2.2/Files/E2A-HPr-demo/index.html) in case you don't want to wait for the results of your docking run.

<a class="prompt prompt-question">Inspect the result page</a>
<a class="prompt prompt-question">How many clusters are generated?</a>

**Note:** The bottom of the page gives you some graphical representations of the results, showing the distribution of the solutions for various measures (HADDOCK score, van der Waals energy, ...) as a function of the RMSD from the best generated model (the best scoring model).


The ranking of the clusters is based on the average score of the top 4 members of each cluster. The score is calculated as:
<pre>
      HADDOCKscore = 1.0 * Evdw + 0.2 * Eelec + 1.0 * Edesol + 1.0 * Eair
</pre>
where Evdw is the intermolecular van der Waals energy, Eelec the intermolecular electrostatic energy, Edesol represents an empirical desolvation energy term adapted from Fernandez-Recio *et al.* J. Mol. Biol. 2004, and Eair the AIR energy. The cluster numbering reflects the size of the cluster, with cluster 1 being the most populated cluster. The various components of the HADDOCK score are also reported for each cluster on the results web page.

<a class="prompt prompt-question">Consider the cluster scores and their standard deviations.</a>
<a class="prompt prompt-question">Is the top ranked cluster significantly better than the second one? (This is also reflected in the z-score).</a>

In case the scores of various clusters are within standard devatiation from each other, all should be considered as a valid solution for the docking. Ideally, some additional independent experimental information should be available to decide on the best solution. In this case we do have such a piece of information: the phosphate transfer mechanism (see [Biological insights](#biological-insights) below).

Let's now visualise the various solutions.

<a class="prompt prompt-info">Download and save to disk the first model of each cluster</a>

Then start PyMOL and load each cluster representative:

<a class="prompt prompt-pymol">File menu -> Open -> select cluster1_1.pdb</a>

Repeat this for each cluster. Once all files have been loaded, type in the PyMOL command window:

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

This will align all clusters on chain A (E2A), maximizing the differences in the orientation of chain B (HPR).

<a class="prompt prompt-question">
Examine the various clusters. How does the orientation of HPR differ between them?
</a>

**Note:** You can turn on and off a cluster by clicking on its name in the left panel of the PyMOL window.

Let's now check if the active residues which we defined are actually part of the interface. In the PyMOL command window type:

<a class="prompt prompt-pymol">
select e2a_active, (resi 38,40,45,46,69,71,78,80,94,96,141) and chain A<br>
select hpr_active, (resi 15,16,17,20,48,49,51,52,54,56) and chain B<br>
color red, e2a_active<br>
color orange, hrp_active<br>
</a>

<a class="prompt prompt-question">
Are the active residues in the interface?
</a>


<hr>
## Biological insight

The E2A-HPR complex is involved in phosphate-transfer, in which a phosphate group attached to histidine 90 of E2A (which we named NEP) is transferred to a histidine of HPR. As such, the docking models should make sense according to this information, meaning that two histidines should be in close proximity at the interface. Using PyMOL, check the various cluster representatives (we are assuming here you have performed all PyMOL commands of the previous section):

<a class="prompt prompt-pymol">
select histidines, resn HIS+NEP
show spheres, histidines
</a>

<a class="prompt prompt-question">First of all, has the phosphate group been poperly generated?</a>

**Note:** You can zoom on the phosphorylated histidine using the following PyMOL command:

<a class="prompt prompt-pymol">
zoom resn NEP
</a>

Zoom back to all visible molecules with 

<a class="prompt prompt-pymol">
zoom vis
</a>


Now inspect each cluster in turn and check if histidine 90 of E2A is in close proximity to another histidine of HPR.
To facilitate this analysis, view each cluster in turn (use the left panel to activate/desactivate the various clusters by clicking on their name).

<a class="prompt prompt-question">Based on this analysis, which cluster does satisfy best the biolocal information?</a>

<a class="prompt prompt-question">Is this cluster also the best ranked one?</a>


<hr>
## Comparison with the reference structure

As explained in the introduction, the structure of the native complex has been determined by NMR (PDB ID [1GGR](http://www.ebi.ac.uk/pdbe/entry/search/index?text:1GGR)) using a combination of intermolecular NOEs and dipolar coupling restraints. We will now compare the docking models with this structure.

If you still have all cluster representative open in PyMOL you can proceed with the sub-sequent analysis, otherwise load again each cluster representative as described above. Then, fetch the reference complex by typing in PyMOL:

<a class="prompt prompt-pymol">
fetch 1GGR<br>
show cartoon<br>
color yellow, 1GGR and chain A<br>
color orange, 1GGR and chain B<br>
</a>

Then superimpose all cluster representatives on the reference structure, using chain A (E2A):

<a class="prompt prompt-pymol">
select cluster1_11GGR and chain A<br>
align cluster1_1, sele
</a>

<a class="prompt prompt-info">
Repeat the align command for each cluster representative.
</a>

<a class="prompt prompt-question">
Does any of the cluster representatives ressemble the reference NMR structure?
</a>
<a class="prompt prompt-question">
In case you found a reasonable prediction, what is its cluster rank?
</a>

In the blind protein-protein prediction experiment [CAPRI](http://capri.ebi.ac.uk/) (Critical PRediction of Interactions), a measure of the quality of a model is the so-called ligand-RMSD (l-RMSD). It is calculated by fitting on the receptor chain (E2A or chain A in our case) and calculating the RMSD on the backbone of the ligand (HPR or chain B in our case). This can be done in PyMOL with the following command:

<a class="prompt prompt-pymol">
rmsd cluster1_1 and chain B, 1GGR<br>
</a>

In CAPRI, the l-RMSD value defines the quality of a model:

* acceptable model: l-RMSD<10Å
* medium quality model: l-RMSD<5Å
* high quality model: l-RMSD<1Å

<a class="prompt prompt-question">
What is based on this CAPRI criterion the quality of the best model?
</a>


<hr>
## Congratulations!

You have completed this tutorial. If you have any questions or 
suggestions, feel free to contact us via email or asking a question through our [support center](http://ask.bioexcel.eu).



<hr>
## Additional docking runs

If you are curious and want learn more about HADDOCK and the impact of the input data on the docking results, consider performing and analysing, as described above, the following runs:

* Same run as above, but without defining the phosphorylated histidine
* Same run as above, but using only the first model of the HPR ensemble (edit the file to extract it)

And check also our [education](/education) web page where you will find more tutorials!


[link-pymol]: http://www.pymol.org/ "PyMOL"

