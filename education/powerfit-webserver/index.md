---
layout: page
title: "PowerFit Tutorial"
excerpt: "A small tutorial on PowerFit webserver for automatic rigid body fitting"
tags: [PowerFit, Cryo-EM, HADDOCK, Ribosome, Chimera, rigid body fitting]
image:
  feature: pages/banner_education-thin.jpg
---

## Introduction

PowerFit is a software application developed to fit atomic resolution
structures of biomolecules to cryo-electron microscopy (cryo-EM) density maps.
It is open-source and available for download on [Github][link-powerfit].


This tutorial will show you how to utilize the PowerFit web server developped
in our lab and that uses either a multi-core version of the software through 
a local cluster hosted in Utrecht or some GPGPU resources available worldwide. 
This web server only requires a web browser to work and benefits from the last
development made in the software within a stable and tested workflow.
Beyond the automated workflow making use of PowerFit, the web server also performs
some postprocessing steps of PowerFit output using [UCSF Chimera][link-chimera].
Chimera is a visualization software and a popular tool in the cryo-electron 
microscopy community for its volume visualization capabilities. You will need to
install Chimera to visualise the data that will be used as input for PowerFit.
 
The version of the web server will use during this tutorial is the multi-core
version making use of a cluster resources available in Utrecht: 
[PowerFit web server][link-powerfit-web]

We will apply Powerfit to an E.coli ribosome case and we will further discuss 
the limits of rigid body fitting, and how HADDOCK can alleviate some of the 
shortcomings. We provide the data necessary to run this tutorial [here][link-data]. 
If you are following one of our workshops, where we use a Virtual Machine, 
then all the required software and data should already be installed.

The PowerFit and HADDOCK software are described in

* G.C.P. van Zundert and A.M.J.J. Bonvin.
[Fast and sensitive rigid-body fitting into cryo-EM density maps with PowerFit](http://dx.doi.org/doi:10.3934/biophy.2015.2.73).
_AIMS Biophysics_. *2*, 73-87 (2015).

* G.C.P. van Zundert, A.S.J. Melquiond and A.M.J.J. Bonvin.
[Integrative modeling of biomolecular complexes: HADDOCKing with Cryo-EM data.](http://dx.doi.org/10.1016/j.str.2015.03.014)
_Structure._ *23*, 949-960 (2015).

Throughout the tutorial, colored text will be used to refer to questions or 
instructions, Linux and/or Chimera commands.

<a class="prompt prompt-question">This is a question prompt: try answering 
it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a Chimera prompt: write this in the 
Chimera command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the 
terminal!</a>

The case we will be investigating is a complex between the 30S maturing E. coli
ribosome and KsgA, a methyltransferase. There are models available for the E.
coli ribosome and KsgA, and a cryo-EM density map of around 13Å resolution
([EMD-2017][link-density]).



## Setup

If you are using one of our pre-packed VM images, the data should be directly
available in the image. We prepared a folder that contains the cryo-EM density
map file in CCP4 format and the starting models of the ribosome and KsgA. The
ribosome has already been properly fitted in the density.

<a class="prompt prompt-info">
  Copy the data to the Desktop and then move the newly copied folder.
</a>
<a class="prompt prompt-cmd">
    cp -r /opt/powerfit-tutorial ~/Desktop  
    cd ~/Desktop/powerfit-tutorial
</a>

*In case you might run this tutorial on your own*, make sure to install [UCSF Chimera][link-chimera]
 and to download the data to run this tutorial from our GitHub data repository [here][link-data] 
or clone it from the command line

<a class="prompt prompt-cmd">
    git clone https://github.com/haddocking/powerfit-tutorial
</a>



## Inspecting the data

Let us first inspect the data we have available, namely the cryo-EM density map
and the structures we will attempt to fit. 

Using Chimera, we can easily visualize and inspect the density and models,
mostly through a few mouse clicks.

<a class="prompt prompt-info">
  Open the density map together with the ribosome and KsgA.
</a>
<a class="prompt prompt-cmd">
    chimera ribosome-KsgA.map ribosome.pdb KsgA.pdb
</a>

In the `Volume Viewer` window, the middle slide bar provides control on the
value at which the isosurface of the density is shown. At high values, the
envelope will sink while lower values might even display the noise in the map.
We will first make the density transparent, to see the fitted structure inside:

* Within the `Volume Viewer` click on the gray box next to `Color`, which opens
  the `Color Editor` window.
* In there, check the `Opacity` box. An extra slider bar appears in the box
  called `A`, for the alpha channel.
* Set the alpha channel value to around 0.6.

Notice that the density becomes transparent providing a better view of the fit
of the ribosome model. On closer inspection, you can also discern a region of
the density that is not accounted by the ribosome structure alone; this is the
binding location of KsgA. Although you could try and manually place the crystal
structure in that region, finding the correct orientation is not
straightforward. PowerFit can help here as it attempts to find the best fit
automatically and exhaustively, based on an objective score.


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
The submission of a PowerFit run takes place here

<a class="prompt prompt-info">http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/submit</a>

<figure align="center">
  <img src="/education/powerfit-webserver/powerfit_submission.png">
</figure>

* **Step1:** Add the input files and parameters.

<a class="prompt prompt-info">Cryo-EM map -> `ribosome-KsgA.map`</a>
<a class="prompt prompt-info">Map resolution -> `13`</a>
<a class="prompt prompt-info">Atomic structure -> `KsgA.pdb`</a>
<a class="prompt prompt-info">Rotational angle interval -> `20.0`</a>
<a class="prompt prompt-info">Submit the job to our server by clicking on "Submit" at the bottom of the page</a>

If the input fields have been correctly filled you should be redirected to a status page displaying a pop-up message
indicating that your run has been successfully submitted to the server.
While performing the search, PowerFit web server will update you on the progress of the 
job by reloading the status page every 30 seconds.
The example case in this tutorial should run in about 5 minutes on our local servers but due to pre- and post-processing
it might take a bit longer to come back to you.

While the calculation is running, open a second tab and go to

<a class="prompt prompt-info">http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/help</a>

Here, you can have a look at the several features and options of PowerFit and what each input parameter (including the
ones in "Advanced parameters") of the submission page means.

The rotational sampling interval option is given in
degrees and defines how tightly the three rotational degrees of freedom will be
sampled. Lower values will cause PowerFit to perform a finer search, at the
expense of computational time. The default value is 10°, but it can be lowered
to 5° for more sensitive searches, or raised to 20° if time is an issue or if
there aren't sufficient computational resources. For the sake of time in this
tutorial, we set the sampling interval to this latter coarser value.
The number of processors used for the calculation is fixed on the web server side to 8 processors. This number can of
course be reduced for a local use of PowerFit.


## Analyzing the results

When a job is finished, and if you did not close the status page, you will be automatically redirected to a results
page.
A summary of the results is displayed and the page is split into several sections:

* `Status`: A link with the ensemble of PowerFit output is available for download there as well as some information
to aknowledge the software.
* `Solutions`: The 15 non-redundant solutions found, ordered by their
cross correlation score. The first column shows the rank, column 2 the correlation
score, column 3 and 4 the Fisher z-score and the number of standard
deviations. The table is created with values taken from the file `solutions.out`.
* `Fit N`: Summary of the previous table for the 10 best fitted structures according to the cross correlation score. 
A PDB of the solution can be downloaded and 6 images of the PDB within the density map are shown, covering different 
views over the scene.

<figure align="center">
  <img src="/education/powerfit-webserver/powerfit_results.png" width="800">
</figure>
 
You can have a first overview online of what the results look like and what are the highest score output by PowerFit.
However, it is difficult to really appreciate the accuracy of PowerFit and the differences between the solutions with
only images.
Download on your computer the results archive available at the top of your results page.
In the archive you can download at the top of the results page, you will find the following files:

* `fit_N.pdb`: the best *N* fits, judged by the cross-correlation score.
* `solutions.out`: all the non-redundant solutions found, ordered by their
correlation score. The first column shows the rank, column 2 the correlation
score, column 3 and 4 the Fisher z-score and the number of standard
deviations; column 5 to 7 are the x, y and z coordinate of the center of the
chain; column 8 to 17 are the rotation matrix values.
* `lcc.mrc`: a cross-correlation map showing, at each grid position, the 
highest cross-correlation score found during the search, thus showing the most 
likely location of the center of mass of the structure.
* `powerfit.log`: a log file of the calculation, including the input parameters 
with date and timing information.


<a class="prompt prompt-info">
  Open the density map, the *lcc.mrc* cross-correlation map, and the 10 
best-ranked solutions in Chimera.
</a>
<a class="prompt prompt-cmd">
  chimera ribosome-KsgA.map run-KsgA/lcc.mrc ribosome.pdb run-KsgA/fit_*.pdb
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
  Go through the 10 solutions one by one to appreciate their goodness-of-fit
  with the density.
</a>
<a class="prompt prompt-question">
  Do you agree with what PowerFit proposes as the best solution?
</a>
<a class="prompt prompt-info">
  In a new Chimera session, reopen the density map and the fit that you find 
best. Replace *?* by the appropriate solution number.
</a>
<a class="prompt prompt-cmd">
  chimera ribosome-KsgA.map ribosome.pdb run-KsgA/fit_?.pdb
</a>

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
then go to `Tools` → `Volume data` → `Fit in Map`. In the newly opened `Fit in 
Map` window, select the best-fitted structure of PowerFit (`fit_?.pdb`) as 
`Fit` model and the original density map (`ribosome-KsgA.map`) as the map. 
Press `Fit` to start the optimization. 

<a class="prompt prompt-question">
  Does the Chimera local fit optimization tool improve the results of PowerFit?
</a>

The scoring function used by Chimera to estimate the quality of the fit makes 
our model worse, increasing the number of clashes between the ribosomal RNA and 
KsgA. Click `Undo` in the `Fit in Map` window to undo the optimization.

Next, we will try to optimize the fit using the cross-correlation that Chimera 
provides. Click `Options` and check the `Use map simulated from atoms, 
resolution` box and fill in `13` for resolution. Check the `correlation` radio 
button and uncheck the `Use only data above contour level from first map`. 
Press `Fit`. 

<a class="prompt prompt-question">
  Does this second strategy improve the quality of the fit? If not, undo it 
again.
</a>


## Integrative modeling with HADDOCK

The obvious limitation of rigid-body fitting is that it cannot account for any
conformational changes the structures might undergo. Further, the low
resolution of this particular density map does not allow the identification of
side-chain atoms. The quality of the fitted models by PowerFit is, therefore,
limited.

Given the availability of both the cryo-EM density map and of the mutagenesis 
experiments, we can integrate both in HADDOCK and benefit of its semi-flexible 
refinement protocols to improve the stereochemistry of our model. To use 
cryo-EM data, HADDOCK requires the map and also the approximate positions of 
each chain, as given by their centers of mass. This information is provided 
directly by PowerFit, in the `solutions.out` file, columns 5 to 7 (x, y, z
coordinates):

<a class="prompt prompt-cmd">
  head -n 10 run-KsgA/solutions.out
</a>

Unfortunately, running HADDOCK is out of the scope of this tutorial as it
requires a significant amount of time. Therefore, we provide the best-ranked 
HADDOCK model, generated by combining the cryo-EM map, the PowerFit centroid
positions, and the mutagenesis data, in the tutorial data folder.

<a class="prompt prompt-info">
  Open the density map in Chimera and load the best-ranked HADDOCK model.
</a>
<a class="prompt prompt-cmd">
  chimera ribosome-KsgA.map HADDOCK-ribosome.pdb HADDOCK-KsgA.pdb
</a>
<a class="prompt prompt-question">
Does HADDOCK improve the quality of the model, i.e. are the number of clashes
reduced?
</a>
<a class="prompt prompt-question">
  Are the three residues identified by mutagenesis involved in any 
energetically favourable interaction?
</a>

Finally, to make the impact of HADDOCK more quantitative, we will make a
distance histogram of the contacts between the ribosome and KsgA. First,
combine the ribosome together with your preferred fitted model.

<a class="prompt prompt-cmd">
  cat ribosome.pdb run-KsgA/fit_?.pdb > ribosome-KsgA.pdb
</a>

To calculate all the contacts within a 5.0Å cutoff distances, we make use of a
standard tool (`contact-chainID`) that is shipped with HADDOCK. 

<a class="prompt prompt-cmd">
  ./contact-chainID ribosome-KsgA.pdb 5.0 > ribosome-KsgA.contacts
</a>

Now we can generate the histogram, and visualize it with xmgrace

<a class="prompt prompt-cmd">
  ./make-contact-histogram.csh ribosome-KsgA.contacts  
  xmgrace ribosome-KsgA-contacts-histogram.xmgr
</a>
<a class="prompt prompt-question">
  Are there any clashes to be found in the model? An interaction is typically
  considered clashing if the distance is smaller than 2.8Å.
</a>

For the HADDOCK model we already combined the ribosome and KsgA
(`HADDOCK-ribosome-KsgA.pdb`).

<a class="prompt prompt-info">
    Make a distance histogram for the HADDOCK generated model.
</a>
<a class="prompt prompt-question">
    Are there any clashes found for the HADDOCK model?
</a>

The combination of cryo-EM and mutagenesis data, a physics-based force field,
and a semi-flexible refinement protocol improves the quality of the resulting
models. In this tutorial, we showed you how to use PowerFit to fit
high-resolution structures to a cryo-EM density map and how to interpret the
results. Further, we also showed how integrative modeling using HADDOCK can
improve the stereochemistry of the models, in particular if done in combination
with additional experimental data, such as mutagenesis.

Thank you for following this tutorial. If you have any questions or 
suggestions, feel free to contact us via email or by submitting an issue in the 
appropriate Github repository.

[link-powerfit]: https://github.com/haddocking/powerfit "PowerFit"
[link-powerfit-web]: http://milou.science.uu.nl/services/POWERFIT/ "PowerFit web server"
[link-powerfit-submit]: http://milou.science.uu.nl/cgi/services/POWERFIT/powerfit/submit "PowerFit submission"
[link-chimera]: https://www.cgl.ucsf.edu/chimera/ "UCSF Chimera"
[link-data]: https://github.com/haddocking/powerfit-tutorial "PowerFit tutorial data"
[link-density]: https://www.ebi.ac.uk/pdbe/entry/emdb/EMD-2017 "Ribosome KsgA density"
