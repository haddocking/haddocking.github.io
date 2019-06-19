---
layout: page
title: "PowerFit web server Tutorial"
excerpt: "A small tutorial on PowerFit web server for automatic rigid body fitting"
tags: [PowerFit, Cryo-EM, HADDOCK, Ribosome, Chimera, rigid body fitting]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}


## Introduction

PowerFit is a software developed in our lab to fit atomic resolution
structures of biomolecules into cryo-electron microscopy (cryo-EM) density maps.
It is open-source and available for download from our [Github repository][link-powerfit]{:target="_blank"}.
To facilitate its use, we have developed a [web portal][link-powerfit-web]{:target="_blank"} for it.

This tutorial demonstrates the use of the PowerFit web server. The server makes use of either
local resources on our cluster, using the multi-core version of the software, or GPGPU-accelerated grid resources of the
[EGI](http://www.egi.eu){:target="_blank"} to speed up the calculations. It only requires a web browser to work and benefits from the latest
developments in the software based on a stable and tested workflow. Next to providing an automated workflow around
PowerFit, the web server also summarizes and higlights the results in a single page including some additional postprocessing
of the PowerFit output using [UCSF Chimera][link-chimera]{:target="_blank"}.
Chimera is a visualization software and popular tool in the cryo-EM community for its volume visualization capabilities.

The case we will be investigating is a complex between the 30S maturing *E. coli*
ribosome and RsgA, a GTPase. There are models ([2YKR][link-pdb]{:target="_blank"}) and a cryo-EM density map of around 9.8Å resolution
([EMD-1884][link-density]{:target="_blank"}) available for the complex.

A related tutorial, based on a local installation of PowerFit can be found [here][link-powerfit-tuto]{:target="_blank"}. It provides a more
detailed analysis of the results of a run with the methyltransferase KsgA, another 30S ribosome partner, and shows how HADDOCK can be used to obtain higher quality models.


The PowerFit and HADDOCK software are described in:

* G.C.P. van Zundert, M. Trellet, J. Schaarschmidt, Z. Kurkcuoglu, M. David, M. Verlato, A. Rosato and A.M.J.J. Bonvin.
[The DisVis and PowerFit web servers: Explorative and Integrative Modeling of Biomolecular Complexes.](https://doi.org/10.1016/j.jmb.2016.11.032){:target="_blank"}.
_J. Mol. Biol._. *429(3)*, 399-407 (2016).

* G.C.P van Zundert and A.M.J.J. Bonvin.
[Defining the limits and reliability of rigid-body fitting in cryo-EM maps using multi-scale image pyramids](https://doi.org/10.1016/j.jsb.2016.06.011){:target="_blank"}.
  _J. Struct. Biol._ *195*, 252-258 (2016).

* G.C.P. van Zundert and A.M.J.J. Bonvin.
[Fast and sensitive rigid-body fitting into cryo-EM density maps with PowerFit](https://doi.org/doi:10.3934/biophy.2015.2.73){:target="_blank"}.
_AIMS Biophysics_. *2*, 73-87 (2015).

* G.C.P. van Zundert, A.S.J. Melquiond and A.M.J.J. Bonvin.
[Integrative modeling of biomolecular complexes: HADDOCKing with Cryo-EM data.](https://doi.org/10.1016/j.str.2015.03.014){:target="_blank"}.
_Structure._ *23*, 949-960 (2015).


Throughout the tutorial, coloured text will be used to refer to questions,
instructions, and Chimera commands.

<a class="prompt prompt-question">This is a question prompt: try answering
it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a Chimera prompt: write this in the
Chimera command line prompt!</a>


## Setup/Requirements

In order to follow this tutorial you only need a **web browser**, a **text editor**, and [**UCSF Chimera**][link-chimera]{:target="_blank"}
(freely available for most operating systems) on your computer in order to visualise the input and output data.  
Further, the required data to run this tutorial should be downloaded [**here**][link-data]{:target="_blank"}.
Once downloaded, make sure to unpack the archive.


## Inspecting the data

Let us first inspect the data we have available, namely the cryo-EM density map
and the structures we will attempt to fit.

Using Chimera, we can easily visualize and inspect the density and models,
mostly through a few mouse clicks.

For this open the density map `ribosome-RsgA.map` and the PDB file of the ribosome which is already fitted into the map `ribosome.pdb`.

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
  open /path/to/ribosome-RsgA.map
</a>
<a class="prompt prompt-pymol">
  open /path/to/ribosome.pdb
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

Notice that the density becomes transparent providing a better view of the fit
of the ribosome model. On closer inspection, you can also discern a region of
the density that is not accounted for by the ribosome structure alone: This should be the
binding location of RsgA. Although you could try and manually place the crystal
structure in that region, finding the correct orientation is not
straightforward. PowerFit can help you here as it will exhaustively sample all possible translations and rotations in order to find the best fit, based on an objective score.


## Rigid body fitting

PowerFit is a rigid body fitting software that quickly calculates the
cross-correlation, a common measure of the goodness-of-fit, between the atomic
structure and the density map. It performs a systematic 6-dimensional scan of
the three translational and three rotational degrees of freedom. In short,
PowerFit will try to systematically fit the structure in different orientations at every position
in the map and calculate a cross-correlation score for each of them.

In order to perform the search PowerFit requires three different things:
a high-resolution atomic structure of the
biomolecule to be fitted (`RsgA.pdb`), a target cryo-EM density map to fit the
structure in (`ribosome-RsgA.map`), and the resolution, in Ångstrom, of the
density map (`9.8`). This is also the minimal required input for the web server in order to setup a run.

To run PowerFit, go to

<a class="prompt prompt-info" href="http://haddock.science.uu.nl/services/POWERFIT" target="_blank">http://haddock.science.uu.nl/services/POWERFIT</a>

On this page, you will find the most relevant information about the server as well as the links to the local and grid versions of the portal's submission page.

### Step1: Register to the server

[Register][link-powerfit-register]{:target="_blank"} for getting access to the webserver (or use the credentials provided in case of a workshop).

You can click on the "**Register**" menu from any PowerFit page and fill the required information.
Registration is not automatic but is usually processed within 12h, so be patient.

### Step2: Define the input files and parameters and submit

Click on the "**Submit**" menu to access the [input form][link-powerfit-submit]{:target="_blank"}:

<figure align="center">
<img src="/education/Others/powerfit-webserver/powerfit_submission.png">
</figure>

Complete the form by filling the required fields and selecting the respective files
(most browsers should also support dragging the files onto the selection button):

<a class="prompt prompt-info">Cryo-EM map → ribosome-RsgA.map</a>
<a class="prompt prompt-info">Map resolution → 9.8</a>
<a class="prompt prompt-info">Atomic structure → RsgA.pdb</a>
<a class="prompt prompt-info">Rotational angle interval → 10.0</a>

Once the fields have been filled in you can submit your job to our server
by clicking on "**Submit**" at the bottom of the page.

If the input fields have been correctly filled you should be redirected to a status page displaying a pop-up message
indicating that your run has been successfully submitted.
While performing the search, the PowerFit web server will update you on the progress of the
job by reloading the status page every 30 seconds.
The runtime of this example case is below 5 minutes on our local servers. However the load of the server as well as
pre- and post-processing steps might substantially increase the time until the results are available.

While the calculations are running, open a second tab and go to

<a class="prompt prompt-info" href="http://haddock.science.uu.nl/services/POWERFIT" target="_blank">http://haddock.science.uu.nl/services/POWERFIT</a>

Then click on the "**Help/Manual**" menu.

Here, you can have a look at the several features and options of PowerFit and read about the meaning of the various input
parameters (including the ones under "**Advanced options**").

The rotational sampling interval option is given in
degrees and defines how tightly the three rotational degrees of freedom will be
sampled. Lower values will cause PowerFit to perform a finer search, at the
expense of increased computational time. The default value is 10°, but it can be lowered
to 5° for more sensitive searches, or raised to 20° if time is an issue or if
there aren't sufficient computational resources.
The number of processors used for the calculation is fixed on the web server side to 8 processors.
This number can of course be changed when using the local version of PowerFit.


## Analysing the results

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

If you don't' want to wait for your run to complete, you can access the precalculated results of a run submitted
with the same input [here][link-powerfit-tutorial]{:target="_blank"}.

The higher the cross-correlation score the better the fit. But also important is the Fisher z-score (the higher the better),
which, together with its associated number of standard deviations (σ difference), is an excellent indicator of the accuracy of a fit
(see for details [van Zundert and Bonvin, J. Struct. Biol. (2016)](https://doi.org/10.1016/j.jsb.2016.06.011){:target="_blank"}
and PowerFit [help page](link-powerfit-help){:target="_blank"}).
To enhance the interpretation of the results in the `Solutions` table, the entries are colored in a green gradient up to
a sigma difference of 3.


<figure align="center">
  <img width="400" src="/education/Others/powerfit-webserver/sigma-difference.jpg">
  <figcaption>The true-positive rate is given versus the difference in Fisher z-score standard deviations between the
  top 2 solutions. The fitting results were binned in 6 bins, starting from 0 to 3 sigma with a step size of 0.5.</figcaption>
</figure>


You can inspect online the results for the top 10 models (different views are provided). However, it is difficult to
really appreciate the accuracy of PowerFit and the differences between the solutions with only images.
Therefore download the results archive to your computer which is available at the top of your results page.

You will find in it the following files:

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


Let us now inspect the solutions in Chimera.

<a class="prompt prompt-info">
  Open the density map, the *lcc.mrc* cross-correlation map, and the 10
best-ranked solutions in Chimera.
</a>

Use for this either the `Menus` or the `command line interface` as explained [before](#inspecting-the-data), e.g.:

<a class="prompt prompt-pymol">
  open /path/to/ribosome-RsgA.map
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

To view each fitted solution individually, open the `Model Panel` window.

<a class="prompt prompt-pymol">
Favorites → Model Panel
</a>

The window shows each model
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

* `ribosome-RsgA.map`
* `ribosome.pdb`
* `fit_?.pdb`

Replace *?* by the appropriate solution number.


**Note**: Make sure to load the files in the specified order for the subsequent commands
to work on the correct residues!

You now have combined the ribosome structure with the rigid-body fit of RsgA
calculated by PowerFit, yielding an initial model of the complex. Take a closer look at residues `R47` to `H51`
which are contributing to the interface with the ribosome.

In the command line of Chimera, type the
following instructions to center your view on these residues and highlight
their interactions:

<a class="prompt prompt-pymol">
  show #2:47-51 zr<5 & #1 || #2:47-51  
  focus #2:47-51 zr<5 & #1 || #2:47-51
</a>
<a class="prompt prompt-info">
  Take some time to inspect the model, paying particular attention to these five
  residues and their spatial neighbors.
</a>
<a class="prompt prompt-question">
  Are there any clashes between the ribosome and RsgA chains?
</a>

Chimera also includes a tool to locally optimize the fit of a rigid structure
against a given density map, which can be an additional help on top of the
PowerFit calculations. Make the main display window active by clicking on it,

<a class="prompt prompt-info">
Go to Tools → Volume data → Fit in Map
</a>
<a class="prompt prompt-info">
In the newly opened Fit in Map window, select the best-fitted structure of PowerFit (fit_?.pdb) as
Fit model and the original density map (ribosome-RsgA.map) as the map.
</a>
<a class="prompt prompt-info">
Press Fit to start the optimization.
</a>

<a class="prompt prompt-question">
  Does the Chimera local fit optimization tool improve the results of PowerFit?
</a>

The scoring function used by Chimera to estimate the quality of the fit makes
our model worse, increasing the number of clashes between the ribosomal RNA and
RsgA. Click `Undo` in the `Fit in Map` window to undo the optimization.

Next, we will try to optimize the fit using the cross-correlation that Chimera
provides.

<a class="prompt prompt-info">
Click "Options" and check the "Use map simulated from atoms, resolution" box and fill in 9.8 for resolution.
</a>
<a class="prompt prompt-info">
Check the "correlation" radio button and uncheck the "Use only data above contour level from first map".
</a>
<a class="prompt prompt-info">
Press "Fit".
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
This is demonstrated in the [command line version][link-haddock-tuto]{:target="_blank"} of the PowerFit tutorial and described in:

* G.C.P. van Zundert, A.S.J. Melquiond and A.M.J.J. Bonvin.
[Integrative modeling of biomolecular complexes: HADDOCKing with Cryo-EM data.](https://doi.org/10.1016/j.str.2015.03.014){:target="_blank"}
_Structure._ *23*, 949-960 (2015).

Thank you for following this tutorial. If you have any questions or suggestions, feel free to contact us via email, or post your question to
our [PowerFit forum](http://ask.bioexcel.eu/c/powerfit){:target="_blank"} hosted by the [<img width="70" src="/images/Bioexcel_logo.png">](http://bioexcel.eu){:target="_blank"} center of excellence
for computational biomolecular research.


[link-powerfit]: https://github.com/haddocking/powerfit "PowerFit"
[link-powerfit-web]: http://haddock.science.uu.nl/services/POWERFIT/ "PowerFit web server"
[link-powerfit-register]: http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/register "PowerFit registration"
[link-powerfit-submit]: http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/submit "PowerFit submission"
[link-powerfit-help]: http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/help "PowerFit submission"
[link-chimera]: https://www.cgl.ucsf.edu/chimera/ "UCSF Chimera"
[link-data]: http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/powerfit-tutorial.tgz "PowerFit tutorial data"
[link-density]: https://www.ebi.ac.uk/pdbe/entry/emdb/EMD-1884 "Ribosome RsgA density"
[link-pdb]: http://www.rcsb.org/pdb/explore/explore.do?structureId=2YKR "PDBid 2YKR"
[link-haddock-tuto]: http://bonvinlab.org/education/Others/powerfit#HADDOCK-cryoEM "HADDOCK with cryoEM data"
[link-powerfit-tuto]: http://bonvinlab.org/education/Others/powerfit "Powerfit command-line tutorial"
[link-powerfit-tutorial]: http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/example "Powerfit tutorial results page"
