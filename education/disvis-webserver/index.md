---
layout: page
title: "DisVis web server Tutorial"
excerpt: "A small tutorial on DisVis web server for visualisation of distance restraints between macromolecular complexes."
tags: [PowerFit, Cryo-EM, HADDOCK, Ribosome, Chimera, rigid body fitting]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* [Introduction](#introduction)
* [Setup](#setup)
* [Inspecting the data](#inspecting-the-data)
* [Accessible interaction space search](#access-inter-space-search)
* [Analyzing the results](#analysing-the-results)
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

The case we will be investigating is the RNA polymerase II complex of S. cerevisiae (PDBid: [1WCM](https://www.ebi.ac.uk/pdbe/entry/pdb/1wcm))
and more precisely the interaction between its chains A and E. Six BS3 cross-links are available 
([Chen et al., 2010](https://dx.doi.org/10.1038/emboj.2009.401); [Kahraman et al., 2013](https://dx.doi.org/10.1371/journal.pone.0073411))
on top of which we will add two false-positive restraints of 35.7 (FP1) and 42.2Å (FP2). We will try to see if DisVis is 
 able to filter out these false-positive restraints while asserting the true interaction space between the two chains.
 As a last step, we will show how the restraints can be provided to HADDOCK in order to model the 3D interaction between the
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
instructions and/or PyMol commands.

<a class="prompt prompt-question">This is a question prompt: try answering 
it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMol prompt: write this in the 
Chimera command line prompt!</a>


## Setup

In order to run this tutorial, which can be run from any operating system and does not require Linux expertise, you will 
need to install [PyMol][link-pymol] on your computer in order to visualise the input and output data.  
Further, the required data to run this tutorial should be downloaded from this [link][link-data].
Once downloaded, make sure to unpack the archive.


## Inspecting the data

Let us first inspect the data we have available, namely the two individual structures as well as the distance restraints
we will provide as input. 

Using PyMol, we can easily visualize the models and the identified cross-links as distance restraints, mostly with a few 
lines of command within PyMol software.

For this open the PDB files `1wcm_A.pdb` and `1wcm_E.pdb`.

<a class="prompt prompt-info">
  PyMol Menu -> File -> Open... -> Select the file
</a>

Repeat this for each file. PyMol will automatically guess their type.

If you want to use instead the the PyMol command-line and type:

<a class="prompt prompt-pymol">
  open /path/to/1wcm_A.pdb
</a>
<a class="prompt prompt-pymol">
  open /path/to/1wcm_E.pdb
</a> 

The 1st step will be to customize a bit the look of the molecules to easily spot the interesting regions.
We will first draw them using a cartoon representation for the protein backbone and hide the side chains for better clarity.
To do so type:

<a class="prompt prompt-pymol">
  show cartoon
</a>

You can explore quickly the two chains and try to imagine where their interactive regions will be located.

Now, we will visualize the cross-links identified in the two articles mentioned above. The cross-link will be visualized by
 drawing a line for each bond identified between each pair of atoms.
We have to look at the file gathering the distance restraints to extract the information.
Open `restraints.txt` from the tutorial input data with your favorite text editor.

To draw a line between two atoms in PyMol, we will use the distance widget. And first, we will slightly change the way those
distances will be displayed in PyMol:

<a class="prompt prompt-pymol">
  set dash_gap, 0
</a>
<a class="prompt prompt-pymol">
  set dash_radius, 0.4
</a>

An extra slider bar appears in the box called A, for the alpha channel.

<a class="prompt prompt-info">
Set the alpha channel value to around 0.6.
</a>

Notice that the density becomes transparent providing a better view of the fit
of the ribosome model. On closer inspection, you can also discern a region of
the density that is not accounted for by the ribosome structure alone: This should be the
binding location of KsgA. Although you could try and manually place the crystal
structure in that region, finding the correct orientation is not
straightforward. PowerFit can help you here as it will exhaustively sample all possible translations and rotations in order to find the best fit, based on an objective score.


## Rigid body fitting

PowerFit is a rigid body fitting software that quickly calculates the 
cross-correlation, a common measure of the goodness-of-fit, between the atomic 
structure and the density map. It performs a systematic 6-dimensional scan of 
the three translational and three rotational degrees of freedom. In short, 
PowerFit will try to fit the structure in many orientations at every position 
on the map and calculate a cross-correlation score for each of them.

PowerFit requires three input: a high-resolution atomic structure of the
biomolecule to be fitted (`KsgA.pdb`), a target cryo-EM density map to fit the
structure in (`ribosome-KsgA.map`), and the resolution, in ångstrom, of the
density map (`13`). They correspond to the minimum number of input you have 
to provide to the web server in order to setup a run.
To run PowerFit, go to

<a class="prompt prompt-info" href="http://haddock.science.uu.nl/services/POWERFIT">http://haddock.science.uu.nl/services/POWERFIT</a>

Then click on the "**Submit**" menu to access the submit form.

<figure align="center">
  <img src="/education/powerfit-webserver/powerfit_submission.png">
</figure>


* **Step1:** Register for getting access to the webserver (or use the credentials provided in case of a workshop).

Click on the "**Register**" menu and fill the required information. Registration is not automatic, so be patient.


* **Step2:** Define the input files and parameters.

<a class="prompt prompt-info">Cryo-EM map -> ribosome-KsgA.map</a>
<a class="prompt prompt-info">Map resolution -> 13</a>
<a class="prompt prompt-info">Atomic structure -> KsgA.pdb</a>
<a class="prompt prompt-info">Rotational angle interval -> 20.0</a>

Once the fields have been filled in you can submit your job to our server 
by clicking on "**Submit**" at the bottom of the page.

If the input fields have been correctly filled you should be redirected to a status page displaying a pop-up message
indicating that your run has been successfully submitted.
While performing the search, the PowerFit web server will update you on the progress of the 
job by reloading the status page every 30 seconds.
The example case in this tutorial should run in about 5 minutes on our local servers but due to pre- and post-processing
it might take a bit longer for the result page to appear.

While the calculations are running, open a second tab and go to

<a class="prompt prompt-info" href="http://haddock.science.uu.nl/services/POWERFIT">http://haddock.science.uu.nl/services/POWERFIT</a>

Then click on the "**Help/Manual**" menu. 

Here, you can have a look at the several features and options of PowerFit and read about the meaning of the various input parameters (including the ones in "**Advanced parameters**").

The rotational sampling interval option is given in
degrees and defines how tightly the three rotational degrees of freedom will be
sampled. Lower values will cause PowerFit to perform a finer search, at the
expense of increased computational time. The default value is 10°, but it can be lowered
to 5° for more sensitive searches, or raised to 20° if time is an issue or if
there aren't sufficient computational resources. For the sake of time in this
tutorial, we set the sampling interval to this latter coarser value.
The number of processors used for the calculation is fixed on the web server side to 8 processors. 
This number can of course be changed when using the local version of PowerFit.


## Analyzing the results

Once your job has completed, and provided you did not close the status page, you will be automatically redirected to the results
page (you will also receive an email notification). The results page presents a summary split into several sections:

* `Status`: In this section you will find a link from which you can download the output data as well as some information
about how to cite the use of the portal.
* `Solutions`: The best 15 non-redundant solutions found, ordered by their
cross correlation score. The first column shows the rank, column 2 the cross correlation
score, column 3 and 4 the Fisher z-score and the number of standard
deviations. The table is created with values taken from the file `solutions.out`.
* `Fit N`: Summary of the previous table for the 10 best fitted structures according to the cross correlation score. 
A PDB of the solution can be downloaded and 6 images of the PDB within the density map are shown, covering different 
views over the scene.

The higher the cross-correlation score the better the fit. But also important is the Fisher z-score (the higher the better), which, together with its associated number of standard deviations, is an excellent indicator of the accuracy of a fit (see for details [van Zundert and Bonvin, J. Struct. Biol. (2016)](http://dx.doi.org/10.1016/j.jsb.2016.06.011).
 

<figure align="center">
  <img src="/education/powerfit-webserver/powerfit_results_summary.png">
</figure>

<figure align="center">
  <img src="/education/powerfit-webserver/powerfit_results.png">
</figure>
 

You can inspect online the results for the top 10 models (different views are provided). However, it is difficult to really appreciate the accuracy of PowerFit and the differences between the solutions with only images. Therefore download to your computer the results archive available at the top of your results page. You will find in it the following files:

* `fit_N.pdb`: the best *N* fits, judged by the cross-correlation score.
* `solutions.out`: all the non-redundant solutions found, ordered by their
cross-correlation score. The first column shows the rank, column 2 the correlation
score, column 3 and 4 the Fisher z-score and the number of standard
deviations; column 5 to 7 are the x, y and z coordinate of the center of the
chain; column 8 to 17 are the rotation matrix values.
* `lcc.mrc`: a cross-correlation map showing, at each grid position, the 
highest cross-correlation score found during the search, thus showing the most 
likely location of the center of mass of the structure.
* `powerfit.log`: a log file of the calculation, including the input parameters 
with date and timing information.


Let us inspect now the solutions in Chimera.

<a class="prompt prompt-info">
  Open the density map, the *lcc.mrc* cross-correlation map, and the 10 
best-ranked solutions in Chimera.
</a>

Use for this either the `Menus` or the `command line interface` as explained [before](#inspecting-the-data), e.g.:

<a class="prompt prompt-pymol">
  open /path/to/ribosome-KsgA.map
</a>
<a class="prompt prompt-pymol">
  open /path/to/lcc.mrc
</a>
<a class="prompt prompt-pymol">
  open /path/to/ribosome.pdb
</a>
<a class="prompt prompt-pymol">
  open /path/to/fit_*.pdb
</a>


Make the density map transparent again, by adjusting the alpha channel value to
0.6. The values of the `lcc.mrc` slider bar correspond to the cross-correlation
score found. In this way, you can selectively visualize regions of high or low
cross-correlation values: i.e., pushing the slider to the right (higher cutoff)
shows only regions of the grid with high cross-correlation scores. 

As you can see, PowerFit found quite some local optima, one of which stands out
(if the rotational search was tight enough). Further, the 10 best-ranked
solutions are centered on regions corresponding to local cross-correlation maxima.

To view each fitted solution individually, in the main panel, go to `Favorites`
→ `Model Panel` to open the `Model Panel` window. The window shows each model
and its associated color that Chimera has processed. To show or hide a specific
model you can click the box in the `S` column.

<a class="prompt prompt-info">
  Go through the 10 solutions one by one to asses their goodness-of-fit
  with the density.
</a>

<a class="prompt prompt-question">
  Do you agree with what PowerFit proposes as the best solution?
</a>

<a class="prompt prompt-info">
  In a new Chimera session, reopen the density map and the fit that you find 
best.
</a>

Use for this either the `Menus` or the `Command Line`option to load the following files:

* `ribosome-KsgA.map`
* `ribosome.pdb`
* `fit_?.pdb`

Replace *?* by the appropriate solution number.

You now have combined the ribosome structure with the rigid-body fit of KsgA
calculated by PowerFit, yielding an initial model of the complex. Mutagenesis
experiments performed on this complex indicate three charged residues of KsgA -
`R221`, `R222`, and `K223` - that are of special importance for the
interaction. 

In the same session of Chimera where you have your chosen fitted KsgA
structure, go to `Favorites` → `Command Line`. A command line is now present
below the main viewing window.  In the command line of Chimera, type the
following instructions to center your view on these residues and highlight
their interactions:

<a class="prompt prompt-pymol">
  show #2:221-223 zr<5 & #1 || #2:221-223  
  center #2:221-223 zr<5 & #1 || #2:221-223
</a>
<a class="prompt prompt-info">
  Take some time to inspect the model, paying particular attention to these three
  residues and their spatial neighbors.
</a>
<a class="prompt prompt-question">
  Are there any clashes between the ribosome and KsgA chains?
</a>
<a class="prompt prompt-question">
  Is the mutagenesis data explained by the model, i.e. are the three charged 
amino acids involved in strong interactions?
</a>

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
