---
layout: page
title: "Modelling a homo-oligomeric complex from MS cross-links"
excerpt: "A small tutorial making use of our DisVis and HADDOCK web servers to define the oligomeric state of a homomeric complex from MS cross-linking data."
tags: [DisVis, Interaction, HADDOCK, 26S proteasome, Chimera, Visualisation]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}


<hr>
## Introduction

In this tutorial, your task is to determine the oligomeric state of a homomeric symmetrical complex and model its 3D structure, based on cross-linking data obtained by mass spectrometry.
Note that for the purpose of this tutorial we are using simulated data that would correspond to rather short cross-linkers that are not amino-acid specific.
We are also assuming that all detected cross-links are highly reliable, i.e. there are no false positives in our data. 
(This differs thus from our [DisVis Webserver Tutorial](/education/disvis-webserver) in which you first have to identify false positives). 

You will first use our DisVis web server to analyse the data and visualise the accessible interaction space defined by the cross-links.
Based on those results you should then make a choice about the putative oligomeric state of the complex (e.g. homodimer, homotrimer, homotetramer,...) 
and then try to model its 3D structure using our HADDOCK web portal. This means defining the cross-links as distance restraints to guide the docking 
and imposing symmetry restraints to generate the proper homomeric complex. Those two aspects are described in two related online tutorials:

* [**HADDOCK MS cross-links tutorial**](/education/HADDOCK-Xlinks):
  A tutorial demonstrating the use of cross-linking data from mass spectrometry to guide the docking in HADDOCK.

* [**HADDOCK ab-initio, multi-body symmetrical docking tutorial**](/education/HADDOCK-CASP-CAPRI-T70):
  A tutorial demonstrating multi-body docking with HADDOCK using its ab-initio mode with symmetry restraints.

  
DisVis and HADDOCK are described in:

* G.C.P. van Zundert, M. Trellet, J. Schaarschmidt, Z. Kurkcuoglu, M. David, M. Verlato, A. Rosato and A.M.J.J. Bonvin.
[The DisVis and PowerFit web servers: Explorative and Integrative Modeling of Biomolecular Complexes.](http://dx.doi.org/10.1016/j.jmb.2016.11.032){:target="_blank"}.
_J. Mol. Biol._. *429(3)*, 399-407 (2016).

* G.C.P van Zundert and A.M.J.J. Bonvin. 
[DisVis: Quantifying and visualizing accessible interaction space of distance-restrained biomolecular complexes](http://dx.doi.org/doi:10.1093/bioinformatics/btv333){:target="_blank"}. 
  _Bioinformatics_ *31*, 3222-3224 (2015).

* G.C.P. van Zundert, J.P.G.L.M. Rodrigues, M. Trellet, C. Schmitz, P.L. Kastritis, E. Karaca, A.S.J. Melquiond, M. van Dijk, S.J. de Vries, A.M.J.J. Bonvin.
[The HADDOCK2.2 webserver: User-friendly integrative modeling of biomolecular complexes.](http://dx.doi.org/doi:10.1016/j.jmb.2015.09.014){:target="_blank"}
_J. Mol. Biol._ *428(4)*, 720-725 (2016).

* S.J. de Vries, M. van Dijk and A.M.J.J. Bonvin.
[The HADDOCK web server for data-driven biomolecular docking.](http://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html)
_Nature Protocols_, *5*, 883-897 (2010).

Further, multi-body docking and the use of symmetry restraints is described in the following paper:

* E. Karaca, A.S.J. Melquiond, S.J. de Vries, P.L. Kastritis and A.M.J.J. Bonvin.
[Building macromolecular assemblies by information-driven docking: Introducing the HADDOCK multi-body docking server.](http://dx.doi.org/doi:10.1074/mcp.M000051-MCP201)
_Mol. Cell. Proteomics_, *9*, 1784-1794 (2010). Download the final author version <a href="http://igitur-archive.library.uu.nl/chem/2011-0314-200254/UUindex.html">here</a>.


Throughout the tutorial, coloured text will be used to refer to questions, 
instructions, and PyMol commands.

<a class="prompt prompt-question">This is a question prompt: Answer it! (This will be part of the report you should submit)</a>
<a class="prompt prompt-info">This is an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMol prompt: write this in the PyMol command line prompt!</a>

<hr>
## Setup/Requirements

In order to follow this tutorial you only need a **web browser**, a **text editor** and [**PyMOL**][link-pymol]{:target="_blank"}
(freely available for most operating systems) on your computer in order to visualize the input and output data.  

Further, the required data to run this tutorial should be downloaded from [**here**](/education/XL-MS-oligomer/XL-MS-oligomer.zip).
Once downloaded, make sure to unzip the archive.

<hr>
## Inspecting the data

Let us first inspect the available data, namely the structure of the monomeric protein and the cross-links.

The downloaded data contain 5 PDB files, which are identical copies of the same monomeric protein, but with different chainIDs (A,B,C,D,E). 
Note that this does not imply the solution is a pentamer per se...

The detected cross-links are between the following residues:
<pre style="background-color:#DAE4E7">
# cross-links
Residue  40 <-> 252 
Residue  90 <-> 176 
Residue 135 <-> 158 
Residue 161 <-> 132
</pre>

In principle, since we are dealing with a homomeric complex, we don't know if those cross-links are intra- or intermolecular.
Based on the cross-linking reaction we assume here a maximum distance between CA carbons of 10Å. Let us first inspect the structure and 
check if those cross-links could be explained by intramolecular links. 

Using PyMOL, we will visualize the information from MS.
For this open first the PDB file `monomer-A.pdb`.

<a class="prompt prompt-info">
  PyMOL Menu → File → Open... → Select the file
</a>

If you want to use the PyMOL command-line instead, type the following command:

<a class="prompt prompt-pymol">
  load monomer-A.pdb
</a>

Highlight the residues involved in cross-links:

<a class="prompt prompt-pymol">
  as cartoon<br>
  select name CA and resid 40+90+135+161+252+176+158+132<br>
  show sphere, sele<br>
</a>

The CA atoms of those residues are now shown as spheres.
Let's now measure the intramolecular distances corresponding to the detected cross-links:

<a class="prompt prompt-pymol">
  distance name CA and resid 40, name CA and resid 252<br>
  distance name CA and resid 90, name CA and resid 176<br>
  distance name CA and resid 135, name CA and resid 158<br>
  distance name CA and resid 161, name CA and resid 132<br>
</a>

This creates four objects called dist01...dist04. You toggle them on and off in the right panel by clicking on them. Check the reported distance for each .

<a class="prompt prompt-question">
<b>Q1:</b> Can any of the cross-links be explained by an intramolecular contact?
Or differently said, is any of those distances shorter than 10Å?
</a>

In case you do identify a crosslink that could be explained by an intramolecular contact (within the same monomer), exclude it from all steps in the remaining part of this tutorial.

<hr>
## Visualizing the accessible interaction space with DisVis

DisVis is a software we developed that allows you to visualize and quantify the information content of distance restraints between macromolecular complexes.
It performs a full and systematic 6 dimensional search of the three translational and rotational degrees of freedom of the two components of a complex to 
determine the number of solutions consistent with the restraints. 

It outputs information about the inconsistent/violated restraints and a density map that represents the center-of-mass position of the scanning chain consistent with a given 
number of restraints at every position in space.

DisVis requires three input files: two high-resolution atomic structures of the biomolecules to be analysed (`monomer-A.pdb` and 
`monomer-B.pdb` in this particular case) and a text file containing the list of distance restraints between the two molecules.


The cross-links should be defined according to the following format:

`<chainid 1> <resid 1> <atomname 1> <chainid 2> <resid 2> <atomname 2> <mindist> <maxdist>`


In this particular case, for the DisVis analysis, we have to duplicate the cross-links given 
above since we are dealing with a symmetrical homomeric system. This is required since in principle we don't know from which monomer they originate. 


The data you downloaded already contain a text file with the cross-links defined in the proper DisVis format: `cross-links.txt`

<pre style="background-color:#DAE4E7">
# cross-links
A  40 CA B 252 CA 3.0 10.0
A  90 CA B 176 CA 3.0 10.0
A 135 CA B 158 CA 3.0 10.0
A 161 CA B 132 CA 3.0 10.0
#
# symmetrical cross-links
A 252 CA B  40 CA 3.0 10.0
A 176 CA B  90 CA 3.0 10.0
A 158 CA B 135 CA 3.0 10.0
A 132 CA B 161 CA 3.0 10.0
</pre>
<br>


<a class="prompt prompt-question">
<b>Q2:</b> Can you rationalize why we are using a lower limit of 3Å between two CA atoms?
</a>


We have all input data required to run DisVis. To launch the run go to:

<a class="prompt prompt-info" href="http://haddock.science.uu.nl/services/DISVIS" target="_blank">http://haddock.science.uu.nl/services/DISVIS</a>

On this page, you will find the most relevant information about the server. 

* **Step1:** Register to the server

[Register][link-disvis-register]{:target="_blank"} for getting access to the web server (or use the credentials provided to you).

You can click on the "**Register**" menu from any DisVis page and fill the required information.
Registration is not automatic but is usually processed within 12h, so be patient.


* **Step2:** Define the input files and parameters and submit

Click on the "**Submit**" menu to access the [input form][link-disvis-submit]{:target="_blank"}.

<figure align="center">
<img src="/education/disvis-webserver/disvis_submission.png">
</figure>

<a class="prompt prompt-info">Fixed chain → monomer-A.pdb</a>
<a class="prompt prompt-info">Scanning chain → monomer-B.pdb</a>
<a class="prompt prompt-info">Restraints file → cross-links.txt</a>

Once the fields have been filled in, you can submit your job to our server 
by clicking on "**Submit**" at the bottom of the page.

If the input fields have been correctly filled you should be redirected to a status page displaying a message
indicating that your run has been successfully submitted.
While performing the search, the DisVis web server will update you on the progress of the 
job by reloading the status page every 30 seconds.
The runtime of this example case is below  5 minutes on our local CPU and grid GPU servers. However the load of the server as well as 
pre- and post-processing steps might substantially increase the time until the results are available.

The default on the server is to perform a `quick scanning` (meaning `15.00°` rotational sampling and `2.0Å` grid) in order to get results in a reasonable time.
You can however choose to perform a `complete scanning`, which should give more reliable results (`9.72°` rotational sampling and `1.0Å` grid). 


<hr>
## Analysing the DisVis results

**Web server output**

Once your job has completed, and provided you did not close the status page, you will be automatically redirected to the results
page (you will also receive an email notification). 

If you don't' want to wait for your run to complete, you can access the precalculated results of a run submitted 
with the same input and complete scanning [here](http://milou.science.uu.nl/cgi/enmr/services/DISVIS/disvis/tutorial/3){:target="_blank"}.

The results page presents a summary split into several sections:

* `Status`: In this section you will find a link from which you can download the output data as well as some information
about how to cite the use of the portal.
* `Accessible Interaction Space`: Here, images of the fixed chain together with the accessible interaction space, in 
a density map representation, are displayed. Different views of the molecular scene can be chosen by clicking
 on the right or left part of the image frame. Each set of images matches a specific level of N restraints which corresponds
 to the accessible interaction space by complexes consistent with at least N restraints. A slider below the image container
 allows you to change the the number of restraints N and load the corresponding set of images.
* `Accessible Complexes`: Summary of the statistics for number of complexes consistent with at least N number of restraints. 
 The statistics are displayed for the N levels, N being the total number of restraints provided in the restraints file (here `restraints.txt`)
* `z-Score`: For each restraint provided as input, a z-Score is provided, giving an indication of how likely it is that the restraint is a false positive. 
The higher the score, the more likely it is that a restraint might be a false positive. Putative false positive restraints
are only highlighted if no single solution was found to be consistent with the total number of restraints provided. If DisVis
finds complexes consistent with all restraints, the z-Scores are still displayed, but should be ignored.
* `Violations`: The table in this sections shows how often a specific restraint is violated for all models consistent with 
a given number of restraints. The higher the violation fraction of a specific restraint, the more likely it is to be a false positive. 
Column 1 shows the number of consistent restraints N, while each following column indicates the violation fractions of 
a specific restraint for complexes consistent with at least N restraints. Each row thus represents the fraction of all 
complexes consistent with at least N restraints that violated a particular restraint. As for the z-Scores, if solutions have been found 
that are consistent with all restraints provided, this table should be ignored.
 

Take your time to analyse the output of DisVis and try to answer the following questions.


<a class="prompt prompt-question"> <b>Q3:</b> Looking at the results section _Accessible Complexes_, what is the maximum number of restraints for which DisVis can find consistent solutions?</a>

Looking at the `z-Score` section, the DisVis output does highlight some restraints as likely false positives. 
Remember however that we have full trust in our cross-links. 
So we don't expect any false positives. Look now at the pictures visualising the accessible space in the `Accessible Interaction Space` section.
Change the value of the slider `Current Level (N)`. Changing its value changes the displayed accessible space, showing the space consistent with N cross-links.

<a class="prompt prompt-question"> <b>Q4:</b> Do you observe a continuous density?</a>

<a class="prompt prompt-question"> <b>Q5:</b> If not, knowing all cross-links are correct ones, what does it tell you about the binding site and the oligomeric state of the complex?</a>

Now set the `Current Level (N)` to its maximum value and look at the view from the top of the structure (i.e. looking down the helices) (you can toggle between different views by clicking on the arrows on the side of the picture):

<a class="prompt prompt-question"><b>Q6:</b> Considering the shape of the molecule and the accessible interaction space, what would be your guess of the oligomeric state of this complex?</a>


The next step in this tutorial will be to model the complex based on the cross-links and the oligomeric state you think if the correct one from the DisVis analysis.


## Modelling the symmetrical homomeric complex using HADDOCK

Our information-driven docking approach [HADDOCK](http://www.bonvinlab.org/software/haddock2.2) has been a 
consistent top predictor and scorer since the start of its participation in the [CAPRI](http://www.ebi.ac.uk/msd-srv/capri) 
community-wide blind docking experiment. This sustained performance is due, in part, to its ability to integrate experimental data and/or 
bioinformatics information into the modelling process, and also to the overall robustness of the scoring function used to assess and rank the predictions. 

Here we will use HADDOCK in order to model the symmetrical oligomeric state of this complex. In order to drive the docking process we will make use of the following information:

1. Knowledge of the stochiometry of the complex (from your above analysis of DisVis results), i.e. how many monomers should we dock?
1. Distance restraints based on MS cross-links
2. [Center-of-mass restraints](http://www.bonvinlab.org/software/haddock2.2/run/#disre) to bring the subunits together and ensure compact solutions
3. [Symmetry restraints](http://www.bonvinlab.org/software/haddock2.2/run/#sym) to define the symmetry of the assembly.

For this you will make use of the [multi-body docking interface][link-haddock-multi]{:target="_blank"} of our 
[HADDOCK web portal][link-haddock-web]{:target="_blank"}. This does require guru level access (provided with course credentials if given to you, 
otherwise [register][link-haddock-register]{:target="_blank"} to the server and request this access level)


Before setting up the docking we need first to generate the distance restraint file for the cross-links in a format suitable for HADDOCK. 
HADDOCK uses [CNS][link-cns] as computational engine. A description of the format for the various restraint types supported by HADDOCK can
be found in our [Nature Protocol](http://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html) paper, Box 4.

Distance restraints are defined as follows:

<pre>
assi (selection1) (selection2) distance, lower-bound correction, upper-bound correction
</pre>

The lower limit for the distance is calculated as: distance minus lower-bound correction
and the upper limit as: distance plus upper-bound correction

The syntax for the selections can combine information about:

* chainID - `segid` keyword 
* residue number - `resid` keyword
* atom name - `name` keyword.

Other keywords can be used in various combinations of OR and AND statements. Please refer for that to the [online CNS manual][link-cns]{:target="_blank"}.

E. g. a distance restraint between the CB carbons of residues 10 and 200 in chains A and B with an 
allowed distance range between 10 and 20Å would be defined as follows:

<pre>
assi (segid A and resid 10 and name CB) (segid B and resid 200 and name CB) 20.0 10.0 0.0
</pre>

<a class="prompt prompt-question">
<b>Q7:</b> Can you think of a different way of defining the distance and lower and upper corrections while maintaining the same 
allowed range?
</a>

A HADDOCK-compatible distance restraint file based on the cross-links defined above for DisVis is already provided in the data you downloaded: `crosslinks-restraints.tbl`.
It contains the following distance restraints (8 in total):

<pre>
assi (segid A and resid  40   and name  CA ) (not segid A and resid  252  and name  CA )  10.0 7.0 0.0
assi (segid A and resid  90   and name  CA ) (not segid A and resid  176  and name  CA )  10.0 7.0 0.0
assi (segid A and resid  135  and name  CA ) (not segid A and resid  158  and name  CA )  10.0 7.0 0.0
assi (segid A and resid  161  and name  CA ) (not segid A and resid  132  and name  CA )  10.0 7.0 0.0
assi (segid A and resid  252  and name  CA ) (not segid A and resid   40  and name  CA )  10.0 7.0 0.0
assi (segid A and resid  176  and name  CA ) (not segid A and resid   90  and name  CA )  10.0 7.0 0.0
assi (segid A and resid  158  and name  CA ) (not segid A and resid  135  and name  CA )  10.0 7.0 0.0
assi (segid A and resid  132  and name  CA ) (not segid A and resid  161  and name  CA )  10.0 7.0 0.0
</pre>

Since we might be docking various numbers of monomers - and we thus don't know to which monomer a cross-link should be defined, 
the above syntax will define distance restraints between the CA atoms of chain A and the corresponding CA atoms of all other chains (the `"not segid A"` part of the second selection).


Let's now setup the docking run! 

Connect to the [multi-body docking interface][link-haddock-multi]{:target="_blank"} of HADDOCK.

__Note:__ _The blue bars on the server can be folded/unfolded by clicking on the arrow on the right._

* **Step1:** Define a name for your docking run, e.g. *XL-MS-XXmer*.

* **Step2:** Input the first protein PDB file. For this unfold the **First Molecule menu**.

<a class="prompt prompt-info">
First molecule: where is the structure provided? -> "I am submitting it"
</a>
<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *monomer-A.pdb*
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> A
</a>

* **Step3:** Input the second protein PDB files. For this unfold the **Second Molecule menu**.

<a class="prompt prompt-info">
Second molecule: where is the structure provided? -> "I am submitting it"
</a>
<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *monomer-B.pdb*
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> B
</a>

* **Step3X:** Repeat Step3 as many times as required based on the stoichiometry you choose from the DisVis results (from 2 to 5 molecules). For this unfold the **Third Molecule menu** and additional ones as needed.

<a class="prompt prompt-info">
XX molecule: where is the structure provided? -> "I am submitting it"
</a>
<a class="prompt prompt-info">
Which chain to be used? -> All (for this particular case)
</a>
<a class="prompt prompt-info">
PDB structure to submit -> Browse and select *monomer-X.pdb*  (where X is C,D or E)
</a>
<a class="prompt prompt-info">
Segment ID to use during docking -> X (where X is C,D or E)
</a>

* **Step4:** Input the cross-links distance restraints and turn on center-of-mass restraints. 
For this unfold the **Distance Restraint menu**.

<a class="prompt prompt-info">
Input under the unambiguous distance restraints the cross-links distance restraints file _crosslinks-restraints.tbl_
</a>
<a class="prompt prompt-info">
Center of mass restraints -> Check the box
</a>

* **Step 5:** Define noncrystallographic symmetry restraint to enforce the various chains will have exactly the same conformation. For this unfold the **Noncrystallographic symmetry restraints menu**:

<a class="prompt prompt-info">
Use this type of restraints	 -> Check the box
</a>
Unfold the **segment pair menu** and define for N molecules N-1 segment pairs, e.g. for a trimer this would be: A-B and B-C.
The protein sequence starts at residue 32 and ends at residue 254. Use those numbers to define the various segments.

* **Step 6:** Define the symmetry restraints to enforce the symmetry that corresponds to the oligomeric state you choose. For this unfold the **symmetry restraints menu**:

<a class="prompt prompt-info">
Use this type of restraints	 -> Check the box
</a>
<a class="prompt prompt-info">
For the symmetry that matches your choosen oligomeric state (C2, C3, C4 or C5), unfold the first CX symmetry segment menu and enter the first and last residue numbers and specify the chainID for each monomer.
</a>

* **Step 7:** Upweight the cross-link restraints in the scoring function since we do trust them. For this unfold the **Scoring parameters menu** and change the weights of the various Eair terms to 1.0:

<a class="prompt prompt-info">
Eair 1	 -> 1.0<br>
Eair 2	 -> 1.0<br>
Eair 3	 -> 1.0<br>
</a>

* **Step 8:** You are ready to submit! Enter your username and password (or the course credentials provided to you). Remember that for this interface you do need guru access.


<hr>
## Analysing the docking results

Once you docking run has completed you will be presented with a result page (and in case you registered for the server an email will be sent to you). 
HADDOCK returns statistics for the top10 clusters, which are averages over the top4 members of each cluster. 
The ranking of the clusters is based on the HADDOCK score. Consult the online [HADDOCK manual](http://www.bonvinlab.org/software/haddock2.2/run/#scoring) 
pages for an explanation of the scoring scheme and the default weights used at various stages. 
Remember that we have increased the weight of the distance restraints for our runs since we wanted to put more weight on the cross-links which we considered highly reliable.

Answer the following questions:

<a class="prompt prompt-question"><b>Q8:</b>  How many clusters have been generated?</a>

<a class="prompt prompt-question"><b>Q9:</b>  Considering the HADDOCK scores and their standard deviation, is the top-ranked cluster significantly better than the second one?</a>

<a class="prompt prompt-question"><b>Q10:</b>  Which cluster has the smallest restraints violation energy (meaning it satisfies best the cross-link restraints) ?</a>

Now download the top model of each cluster and inspect them in PyMol:

<a class="prompt prompt-info">
  PyMOL Menu → File → Open... → Select the file
</a>

If you want to use the PyMOL command-line instead, type the following command:

<a class="prompt prompt-pymol">
  load cluster1_1.pdb<br>
  as cartoon<br>
  util.cbc<br>
</a>

This will display the docking model in cartoon mode, with each chain colored differently.

<a class="prompt prompt-question"><b>Q11:</b>  Do the models show the symmetry that you defined?</a>

<a class="prompt prompt-question"><b>Q12:</b>  If two clusters have rather similar scores (possibly overlapping within their standard deviations), compare them in PyMol. What are the differences?</a>

Now select what you consider is your best model and check if it satisfies the defined cross-links. For this we need to check all possible combinations between the chains.
For example for the first cross-link between residues 40 and 252 we should calculate all possible distances between residue 40 of chainA and residue 252 of all other chains in the model:

<a class="prompt prompt-pymol">
  distance name CA and resid 40 and chain A, name CA and resid 252 and chain B<br>
  distance name CA and resid 40 and chain A, name CA and resid 252 and chain C<br>
  ...<br>
</a>

<a class="prompt prompt-question"><b>Q13:</b>  For each of our experimental cross-links (the 8 restraints we defined), 
find the shortest distance from the various chain combinations. Does the model satisfy the cross-links?</a>

If the restraint energy is still very high and your best docking model does not satisfy the restraints very well, you could conclude that your choice of oligomeric state was not optimal. 
In that case you could consider performing another docking run with a different number of monomers and another symmetry.

In case you did perform multiple docking runs with different numbers of monomers and symmetries, it could happen that two runs generate solutions that satisfy the cross-links equally.
In that case compare their HADDOCK scores. Remember that the HADDOCK score is calculated based on intermolecular interactions. 
So when comparing the scores of runs from different numbers of monomers, take the number of interfaces in your complex into account when comparing two runs to make your choice 
(for example by dividing the HADDOCK score of each run by the number of interfaces).

Another way of thinking about your choice is to apply Occam's razor (see [Wikipedia](https://en.wikipedia.org/wiki/Occam%27s_razor) page):

_"Occam's razor (also Ockham's razor; Latin: lex parsimoniae "law of parsimony") is a problem-solving principle that, when presented with competing hypothetical answers to a problem, one should select the one that makes the fewest assumptions."_

<a class="prompt prompt-question"><b>Q14:</b>  FINALLY, based on all above analysis, what is your conclusion concerning the oligomeric state and symmetry of this complex?

 
<hr>
## Your report

Congratulations! You should have completed this assignment. For your report we expect the following:

1. An answer to all 14 questions asked in this tutorial (with a short motivation for each)
2. The PDB file of what you consider to be the best model for this homomeric complex
3. The web link to the result page of the docking run from which you selected your best model

Make sure to write your name and student number at the top of your report.




[link-cns]: http://cns-online.org "CNS online"
[link-disvis]: https://github.com/haddocking/disvis "DisVis GitHub repository"
[link-disvis-web]: http://haddock.science.uu.nl/services/DISVIS/ "DisVis web server"
[link-disvis-submit]: http://milou.science.uu.nl/cgi/services/DISVIS/disvis/submit "DisVis submission"
[link-disvis-register]: http://milou.science.uu.nl/cgi/services/DISVIS/disvis/register "DisVis registration"
[link-disvis-tutorial]: http://milou.science.uu.nl/cgi/services/DISVIS/disvis/tutorial "DisVis Tutorial"
[link-data]: http://milou.science.uu.nl/cgi/services/HADDOCK2.2/disvis/disvis-tutorial.tgz "DisVis tutorial data"
[link-chimera]: https://www.cgl.ucsf.edu/chimera/ "UCSF Chimera"
[link-chimera-distance]: https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/framecommand.html "UCSF Chimera distance command"
[link-chimera-atomspec]: https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/framecommand.html "UCSF Chimera atom specification"
[link-pymol]: http://www.pymol.org/ "PyMOL"
[naccess]: http://www.bioinf.manchester.ac.uk/naccess/ "NACCESS"
[link-haddock]: http://bonvinlab.org/software/haddock2.2 "HADDOCK 2.2"
[link-haddock-web]: http://haddock.science.uu.nl/services/HADDOCK2.2 "HADDOCK 2.2 webserver"
[link-haddock-multi]: http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-multi.html "HADDOCK 2.2 multibody docking interface"
[link-haddock-register]: http://haddock.science.uu.nl/services/HADDOCK2.2/signup.html "HADDOCK 2.2 registration"
[link-haddock-tutorial]: http://bonvinlab.org/education/HADDOCK-protein-protein-basic "HADDOCK 2.2 webserver tutorial"
