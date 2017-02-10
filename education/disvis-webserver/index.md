---
layout: page
title: "DisVis web server Tutorial"
excerpt: "A small tutorial on DisVis web server for visualisation of distance restraints between macromolecular complexes."
tags: [DisVis, Interaction, HADDOCK, 26S proteasome, Chimera, Visualisation]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* [Introduction](#introduction)
* [Setup](#setup)
* [Inspecting the data](#inspecting-the-data)
* [Accessible interaction space search](#access-inter-space-search)
* [Analyzing the results](#analysing-the-results)
* [Residues interaction analysis](#residues-interaction-analysis)
* [Final remarks](#final-remarks)



## Introduction

DisVis is a software developed in our lab to visualize and quantify the information content of distance restraints 
between macromolecular complexes. It is open-source and available for download from our [Github repository][link-disvis].
To facilitate its use, we have developed a [web portal][link-disvis-web] for it.


This tutorial demonstrates the use of the DisVis web server. The server makes use of either 
local resources on our cluster, using the multi-core version of the software, or GPGPU-accelerated grid resources of the 
[EGI](http://www.egi.eu) to speed up the calculations. It only requires a web browser to work and benefits from the latest
developments in the software based on a stable and tested workflow. Next to providing an automated workflow around DisVis, 
the web server also performs some postprocessing of the DisVis output using [UCSF Chimera][link-chimera] to provide a
first overview of the interaction space between the two molecules.

The case we will be investigating is the interaction between two proteins of the 26S proteasome of S. pombe, PRE5 
(UniProtKB: [O14250](http://www.uniprot.org/uniprot/O14250)) and PUP2 (UniProtKB: [Q9UT97](http://www.uniprot.org/uniprot/Q9UT97)). 
Seven cross-links (4 ADH & 3 ZL) are available ([Leitner et al., 2014](https://dx.doi:10.1073/pnas.1320298111)) and on top of which 
we will add two false-positive restraints. We will try to see if DisVis is able to filter out these false-positive 
restraints while asserting the true interaction space between the two chains.
We will then use the interaction analysis feature of DisVis that allows for a more complete analysis of the residues 
putatively involved in the interaction between the two molecules. To do so, we will extract all accessible residues of
the two partners, and give the list of residue to DisVis using its interaction analysis feature.
Finally, we will show how the restraints can be provided to HADDOCK in order to model the 3D interaction between the
 2 partners.
  
The DisVis and HADDOCK software are described in:

* G.C.P van Zundert and A.M.J.J. Bonvin. 
[DisVis: Quantifying and visualizing accessible interaction space of distance-restrained biomolecular complexes](http://dx.doi.org/doi:10.1093/bioinformatics/btv333). 
  _Bioinformatics_ *31*, 3222-3224 (2015).

* G.C.P. van Zundert, M. Trellet, J. Schaarschmidt, Z. Kurkcuoglu, M. David, M. Verlato, A. Rosato and A.M.J.J. Bonvin.
[The DisVis and PowerFit web servers: Explorative and Integrative Modeling of Biomolecular Complexes.](http://dx.doi.org/10.1016/j.jmb.2016.11.032).
_J. Mol. Biol._. *429(3)*, 399-407 (2015).

* G.C.P. van Zundert, J.P.G.L.M. Rodrigues, M. Trellet, C. Schmitz, P.L. Kastritis, E. Karaca, A.S.J. Melquiond, M. van Dijk, S.J. de Vries, A.M.J.J. Bonvin.
[The HADDOCK2.2 webserver: User-friendly integrative modeling of biomolecular complexes.](http://dx.doi.org/doi:10.1016/j.jmb.2015.09.014)
_J. Mol. Biol._ *428(4)*, 720-725 (2016).


Throughout the tutorial, colored text will be used to refer to questions or 
instructions and/or Chimera commands.

<a class="prompt prompt-question">This is a question prompt: try answering 
it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a Chimera prompt: write this in the 
Chimera command line prompt!</a>


## Setup

In order to run this tutorial, which can be run from any operating system and does not require Linux expertise, you will 
need to install [UCSF Chimera][link-chimera] on your computer in order to visualise the input and output data.  
Further, the required data to run this tutorial should be downloaded from this [link][link-data].
Once downloaded, make sure to unpack the archive.


## Inspecting the data

Let us first inspect the data we have available, namely the two individual structures as well as the distance restraints
we will provide as input. 

Using Chimera, we can easily visualize the models and the identified cross-links as distance restraints, mostly with a few 
lines of command within Chimera command-line interface.

For this open the PDB files `PRE5.pdb` and `PUP2.pdb`.

<a class="prompt prompt-info">
  UCSG Chimera Menu -> File -> Open... -> Select the file
</a>

Repeat this for each file. Chimera will automatically guess their type.


If you want to use instead the the Chimera command-line:

<a class="prompt prompt-info">
  UCSG Chimera Menu -> Favorites -> Command Line
</a>

and type:

<a class="prompt prompt-pymol">
  open /path/to/PRE5.pdb
</a>
<a class="prompt prompt-pymol">
  open /path/to/PUP2.pdb
</a>


The 1st step will be to slightly adapt the look of the molecules to easily spot the interesting regions.
You can explore quickly the two chains and try to imagine where their interactive regions will be located.

Now, we will visualize the cross-links identified in the two articles mentioned above. The cross-link will be visualized by
 drawing a line for each bond identified between each pair of atoms.
We have to look at the file gathering the distance restraints to extract the information.
Open `restraints.txt` from the tutorial input data with your favorite text editor.

To draw a line between two atoms in Chimera, we will use the ['distance'](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/framecommand.html) widget.
To help you with the atom selection syntax, you can have a look at the ['atom specification'](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/midas/frameatom_spec.html) 
section of Chimera documentation.
Here are the commands you need to execute in order to draw all restraints:

<a class="prompt prompt-pymol">
distance #0:27@CA | #1:18@CA
</a>
<a class="prompt prompt-pymol">
distance #0:122@CA | #1:125@CA
</a>
<a class="prompt prompt-pymol">
distance #0:122@CA | #1:127@CA
</a>
<a class="prompt prompt-pymol">
distance #0:122@CA | #1:128@CA
</a>
<a class="prompt prompt-pymol">
distance #0:164@CA | #1:49@CA
</a>
<a class="prompt prompt-pymol">
distance #0:55@CA | #1:169@CA
</a>
<a class="prompt prompt-pymol">
distance #0:55@CA | #1:179@CA
</a>
<a class="prompt prompt-pymol">
distance #0:54@CA | #1:179@CA
</a>
<a class="prompt prompt-pymol">
distance #0:49@CA | #1:188@CA
</a>

Each restraint present in the `restraints.txt` file should now be displayed in Chimera. For a better view of these restraints,
you can open the `Distances` windows:

<a class="prompt prompt-pymol">
UCSG Chimera Menu -> Tools -> Structure Analysis -> Distances
</a>

And now change the `Line width`, the `Line style` or even the `Color` of the distance representations.

<a class="prompt prompt-question">
Can you already spot the false positive restraints?
</a>

We will try to assess the quality of those restraints with DisVis and try to figure out which restraints might be false positive
thanks to an exhaustive analysis of the interaction space between the two molecules.

## Accessible interaction space search

DisVis performs a full and systematic 6 dimensional search of the three translational and rotational degrees of freedom to 
determine the number of complexes consistent with the restraints. In addition, it outputs the percentage of restraints 
being violated and a density that represents the center-of-mass position of the scanning chain corresponding to the 
highest number of consistent restraints at every position in space.

DisVis requires three input: two high-resolution atomic structures of the biomolecules to be analysed (`PRE5.pdb` and 
`PUP2.pdb`) and a list of distance restraints, under TBL format, with which the two biomolecules should comply with 
(`restraints.txt`). They correspond to the minimum number of input you have to provide to the web server in order to 
setup a run.
To run DisVis, go to

<a class="prompt prompt-info" href="http://haddock.science.uu.nl/services/DISVIS">http://haddock.science.uu.nl/services/DISVIS</a>

Then click on the "**Submit**" menu to access the submit form.

<figure align="center">
  <img src="/education/disvis-webserver/disvis_submission.png">
</figure>


* **Step1:** Register for getting access to the web server (or use the credentials provided in case of a workshop).

Click on the "**Register**" menu and fill the required information. Registration is not automatic, so be patient.


* **Step2:** Define the input files and parameters.

<a class="prompt prompt-info">Fixed chain -> PRE5.pdb</a>
<a class="prompt prompt-info">Scanning chain -> PUP2.pdb</a>
<a class="prompt prompt-info">Restraints file -> restraints.txt</a>

Once the fields have been filled in you can submit your job to our server 
by clicking on "**Submit**" at the bottom of the page.

If the input fields have been correctly filled you should be redirected to a status page displaying a pop-up message
indicating that your run has been successfully submitted.
While performing the search, the DisVis web server will update you on the progress of the 
job by reloading the status page every 30 seconds.
The example case in this tutorial should run in about 5 minutes on our local servers but due to pre- and post-processing
it might take a bit longer for the result page to appear.

While the calculations are running, open a second tab and go to

<a class="prompt prompt-info" href="http://haddock.science.uu.nl/services/DISVIS">http://haddock.science.uu.nl/services/DISVIS</a>

Then click on the "**Help/Manual**" menu. 

Here, you can have a look at the several features and options of DisVis and read about the meaning of the various input 
parameters (including the ones in "**Advanced options**").

The rotational sampling interval option is given in
degrees and defines how tightly the three rotational degrees of freedom will be
sampled. Voxel spacing is the size of the grid's voxels that will be crossed during the 6D search.
Lower values of both parameters will cause DisVis to perform a finer search, at the
expense of increased computational time. The default value is `15°` and `2.0Å` for a quick scanning and `9.72°` and `1.0Å` 
for a complete one. 
For the sake of time in this tutorial, we will keep the sampling interval to the quick scanning value (`15.00°`).
The number of processors used for the calculation is fixed on the web server side to 8 processors. 
This number can of course be changed when using the local version of DisVis.


## Analyzing the results

<h3> Web server output </h3>

Once your job has completed, and provided you did not close the status page, you will be automatically redirected to the results
page (you will also receive an email notification). The results page presents a summary split into several sections:

* `Status`: In this section you will find a link from which you can download the output data as well as some information
about how to cite the use of the portal.
* `Accessible Interaction Space`: Here, images of the fixed chain together with the accessible interaction space, as 
a density map representation, will be displayed. Several point of views over the molecular scene can be chosen by clicking
 on the right or left part of the image frame. Each set of images matches a specific level of restraints N which corresponds
 to the accessible interaction space by complexes consistent with at least N restraints. A slider vbelow the image container
 gives the possibility to change the level and load the corresponding set of images.
* `Accessible Complexes`: Summary of the statistics for complexes consistent with at least N number of restraints. Statistics
 are displayed for the N levels, N being the total number of restraints provided in the restraints file (here `restraints.txt`)
* `z-Score`: For each restraint provided as input, a z-Score, as a indication of how likely the restraint is a false-positive,
is provided. The higher the score, the most likely a restraint might be a false-positive. Putative false-positive restraints
are highlighted if there was no complexes found to be consistent with a certain number of restraints provided. If DisVis
found complexes consistent with all restraints provided, z-Score will be displayed as an indication but cannot be used to
discriminate true- and false-positive restraints and should be then ignored.
* `Violations`: The table in this sections shows how often a specific restraint is violated for complexes consistent with 
a number of restraints. The higher the violation fraction of a specific restraint, the more likely it is to be a false-positive. 
Column 1 shows the number of consistent restraints N, while each following column indicates the violation fractions of 
a specific restraint for complexes consistent with at least N restraints. Each row thus represents the fraction of all 
complexes consistent with at least N restraints that violated a particular restraint. As for z-Scores, if complexes have
been found to be consistent with all restraints provided, this table should be ignored.


<figure align="center">
  <img src="/education/disvis-webserver/disvis_results_summary.png">
</figure>

You can have a complete overview of a typical DisVis web server output in the [Example](http://milou.science.uu.nl/cgi/services/DISVIS/disvis/example)
section of the web server. (You will note that this tutorial is an extension of the `26S proteasome` example). 
 
It is already possible to extract significant results from the results page. 

<a class="prompt prompt-question"> Using the different descriptions of the sections we provided above together with the information
on the results page of your run, what are the two restraints DisVis has detected as false-positive?</a>

<a class="prompt prompt-question"> Does it validate the guess you had when loking at those restraints in Chimera?</a>

As mentioned above, the two last sections feature a table that highlight putative false-positive restraints based on 
their z-Score and their violations frequency for a specific number of restraints. We will naturally look for the 
statistics of the highest number of restraints. DisVis preformat the results in a way that false-positive restraints 
are highlighted and can be spotted in a glance.

In our case, you should observe that the following two restraints are highlighted as putative false-positives:
<details><summary><b>See solution:</b>
</summary>
<center><b>A164(CA)-A49(CA)  &  A49(CA)-A188(CA)</b></center>
</details>


<h3> DisVis output files </h3>

It is difficult to really appreciate the accessible interaction space between the two partners with only images. 
Therefore download to your computer the results archive available at the top of your results page. You will find in it the 
following files:

* `accessible_complexes.out`: a text file containing the number of complexes consistent with a number of restraints.
* `accessible_interaction_space.mrc`: a density file in MRC format. The density represents the center of mass of the 
scanning chain conforming to the maximum found consistent restraints at every position in space
* `disvis.log`: a log file showing all the parameters used, together with date and time indications.
* `violations.out`: a text file showing how often a specific restraint is violated for each number of consistent restraints.
* `z-score.out`: a text file giving the Z-score for each restraint. The higher the score, the more likely the restraint 
is a false-positive.

Let us inspect now the solutions in Chimera.

<a class="prompt prompt-info">
  Open the fixed chain PDB file and the *accessible_interaction_space.mrc* density map in Chimera.
</a>

Use for this either the `Menus` or the `Command-line interface` as explained [before](#inspecting-the-data), e.g.:

<a class="prompt prompt-pymol">
  open /path/to/fixed_chain.pdb
</a>
<a class="prompt prompt-pymol">
  open /path/to/accessible_interaction_space.mrc
</a>

The values of the `accessible_interaction_space.mrc` slider bar correspond to the number of restraints (N).
In this way, you can selectively visualize regions where complexes have been found to be consistent with a certain number of 
restraints. In our case, we are interested in observing the results for the maximum number of restraints where complexes 
were found, here **7**.

<a class="prompt prompt-question">
  Does the accessible interaction space between of the fixed chain seem to match the conformation found in the litterature
   and used as template for the structure observed in the 1st step?
</a>

## Residues interaction analysis

We now have an idea of the interactive region between the two molecules. To go further, and prepare a putative future
docking experiment to obtain models of the interaction, we might want to know what are the most important residues involved
in the interaction.
To do so, we will use the `Interaction Analysis` feature of DisVis by providing a list of residues that DisVis will analysis
 with regards to the complexes found consistent with a number of restraints.
 
Go to:

<a class="prompt prompt-info" href="http://haddock.science.uu.nl/cgi/services/DISVIS/disvis/submit">http://haddock.science.uu.nl/cgi/services/DISVIS/disvis/submit</a>

As for the 1st run of DisVis, we will use the same input files:

<a class="prompt prompt-info">Fixed chain -> PRE5.pdb</a>
<a class="prompt prompt-info">Scanning chain -> PUP2.pdb</a>
<a class="prompt prompt-info">Restraints file -> restraints.txt</a>

But we will also provide a list of residue for the fixed and scanning chains in a file names `selection.txt` and present
in the tutorial data. The residues we have selected are all residues considered as surface accessible for both the fixed
and the scanning chain. We used [NACCESS](http://www.bioinf.manchester.ac.uk/naccess/) to compute the accessibility of each
and defined a threshold of 40% of relative accessibility for either the backbone or the side-chain to filter accessible 
to non-accessible residues.

<a class="prompt prompt-info">Interaction Analysis -> selection.txt</a>

For this specific run, we will use the `Complete scanning` option but we will uncheck the `Occupancy Analysis` option to
keep the computation time in a reasonable window for this tutorial.

Then click on the `Submit` button to start the run. The monitoring of your job will be identical to the one explained in
the [previous section](#access-inter-space-search).

One your job is finished, the results page will display, complementary to the sections we had previously, a new section:
 
* `Interaction analysis`: The tables of these sections shows how many interactions a specific residue makes in the complexes
 consistent with a specific number of restraints. The higher the interaction fraction of a specific residue is, the more 
 likely it is involved in the complex interaction.

Thanks to this new information, we can now identify key residues that play a crucial role in the complexes consistent with
our restraints. It is easy to sort the tables by their average number of interactions and then detect the most important ones.

<a class="prompt prompt-question> How many key residues can you identify from the tables? </a>
<a class="prompt prompt-question> Create a list of these residues for both the fixed and the scanning chain.</a>

<details><summary><b>See solution:</b>
</summary>
Respectively <b>X</b> and <b>Y</b> residues have been identified as important for the interaction in the fixed and
 scanning chains:><br>
 
</details>

In order to check if those residues are indeed important for the interaction, we will highlight them in Chimera, using a
recently published ([article]november 2016) structure of an homologue of the 26S proteasome we are studying where the structure of 
two very similar molecules have been solved by X-ray at high resolution (2.4Å).

We voluntarily placed the two molecules in a particular conformation found in a known structure of the 26S proteasome solved
 by X-ray at a 2.4Å resolution and released in november 2016 (see [associated article](https://dx.doi.org/10.15252/embj.201695222)).

Chimera also includes a tool to locally optimize the fit of a rigid structure 
against a given density map, which can be an additional help on top of the 
PowerFit calculations. Make the main display window active by clicking on it, 

<a class="prompt prompt-info">
Go to Tools → Volume data → Fit in Map
</a>
<a class="prompt prompt-info">
In the newly opened Fit in Map window, select the best-fitted structure of PowerFit (fit_?.pdb) as 
Fit model and the original density map (ribosome-KsgA.map) as the map.
</a>
<a class="prompt prompt-info">
Press Fit to start the optimization. 
</a>

<a class="prompt prompt-question">
  Does the Chimera local fit optimization tool improve the results of PowerFit?
</a>

The scoring function used by Chimera to estimate the quality of the fit makes 
our model worse, increasing the number of clashes between the ribosomal RNA and 
KsgA. Click `Undo` in the `Fit in Map` window to undo the optimization.

Next, we will try to optimize the fit using the cross-correlation that Chimera 
provides. 

<a class="prompt prompt-info">
Click Options and check the Use map simulated from atoms, resolution box and fill in 13 for resolution. 
</a>
<a class="prompt prompt-info">
Check the correlation radio button and uncheck the Use only data above contour level from first map. 
</a>
<a class="prompt prompt-info">
Press Fit. 
</a>

<a class="prompt prompt-question">
  Does this second strategy improve the quality of the fit? If not, undo it 
again.
</a>


## Final remarks

We have demonstrated in this tutorial how to make use of the PowerFit web server to fit
atomic structures in cryo-EM map. 
The obvious limitation of rigid-body fitting is that it cannot account for any
conformational changes that the structures might undergo. Further, the low
resolution of this particular density map does not allow to identify
side-chain atoms. The quality of the fitted models by PowerFit is, therefore,
limited. In particular, such models will typically result in a significant clashes at the interface between molecules.
Such clashes can be removed by making use of the HADDOCK-EM flexible refinement capabilities.
This is demonstrated in the [command line version][link-haddock-tuto] of the PowerFit tutorial and described in:

* G.C.P. van Zundert, A.S.J. Melquiond and A.M.J.J. Bonvin.
[Integrative modeling of biomolecular complexes: HADDOCKing with Cryo-EM data.](http://dx.doi.org/10.1016/j.str.2015.03.014)
_Structure._ *23*, 949-960 (2015).


Thank you for following this tutorial. If you have any questions or 
suggestions, feel free to contact us via email.

[link-disvis]: https://github.com/haddocking/disvis "DisVis"
[link-disvis-web]: http://haddock.science.uu.nl/services/DISVIS/ "DisVis web server"
[link-disvis-submit]: http://milou.science.uu.nl/cgi/services/DISVIS/disvis/submit "DisVis submission"
[link-chimera]: https://www.cgl.ucsf.edu/chimera/ "UCSF Chimera"
[link-data]: http://milou.science.uu.nl/cgi/services/DISVIS/disvis/disvis-tutorial.tgz "DisVis tutorial data"
[link-pdb]: https://www.ebi.ac.uk/pdbe/entry/pdb/1wcm "PDBid 1WCM"
[link-pymol]: https://sourceforge.net/projects/pymol/ "PyMol open source"
