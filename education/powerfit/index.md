---
layout: page
title: "PowerFit Tutorial"
excerpt: "A small tutorial on PowerFit for automatic rigid body fitting"
tags: [PowerFit, Cryo-EM, HADDOCK, Ribosome, Chimera, rigid body fitting]
image:
  feature: pages/banner_education-thin.jpg
---

## Introduction

PowerFit is a software application developed to fit atomic resolution
structures of biomolecules to cryo-EM density maps. It is open-source and
available for download on [Github][link-powerfit].

This tutorial will show you how to utilize PowerFit
by applying it to an E.coli ribosome case. To follow this tutorial,
you need, in addition to PowerFit, the [UCSF Chimera][link-chimera] 
visualization software, a popular tool in the cryo-electron microscopy
community for its volume visualization capabilities. We will further discuss 
the limits of rigid body fitting, and how
HADDOCK can alleviate some of the shortcomings. We provide the data necessary 
to run this tutorial [here][link-data]. If you are following one of our 
workshops, where we use a Virtual Machine, then all the required software and 
data should already be installed.

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
ribosome and KsgA, a methyltransferase. There are crystal structures available
for the E. coli ribosome and KsgA (PDBID 
[4ADV](www.rcsb.org/pdb/explore/explore.do?structureId=4adv)), and a cryo-EM 
density map of around 13Å
resolution ([EMD-2017](www.ebi.ac.uk/pdbe/entry/emdb/EMD-2017)).


## Inspecting the data

Let us first inspect the data we have available, namely the cryo-EM density map 
and the crystal structures we will attempt to fit. We prepared a folder that 
contains the electron density map files in XPLOR format and the crystal 
structures, both randomly oriented and already fit to their position on the 
map. 

<a class="prompt prompt-info">
  Copy the data to the Desktop and then move the newly copied folder.
</a>

<a class="prompt prompt-cmd">
    cp -r /opt/powerfit-tutorial ~/Desktop  
    cd ~/Desktop/powerfit-tutorial
</a>

Using Chimera, we can easily visualize and inspect the density and crystal 
structures, mostly through a few mouse clicks.

<a class="prompt prompt-info">
  Open the density map and the already fitted structures of the ribosome and 
KsgA.
</a>
<a class="prompt prompt-cmd">
    chimera ribosome-KsgA.map ribosome.pdb KsgA.pdb
</a>

In the `Volume Viewer` window, the middle slide bar provides
control on the value at which the isosurface of the density is shown. At high 
values, the envelope will sink while lower values might even display the noise 
in the map.  We will first make the density transparent, to see the fitted 
structure inside:

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
cross-correlation, a common measure of the goodness of fit, between the atomic 
structure and the density map. It performs a systematic 6-dimensional scan of 
the three translational and three rotational degrees of freedom. In short, 
PowerFit will try to fit the structure in many orientations at every position 
on the map and calculate a cross-correlation score for each of them.

<a class="prompt prompt-info">
  Perform the rigid-body fitting of the KsgA structure on the cryo-EM density 
map.
</a>
<a class="prompt prompt-cmd">
  powerfit KsgA.pdb ribosome-KsgA.map 13 -d run-KsgA -a 20 -p 2 -l
</a>

While performing the search, PowerFit will update you on the progress of the 
search. The example case in this tutorial should run in 5 minutes. If the ETA 
on your screen is substantially lower, your computer might be fast enough to 
allow an increase in the rotational sampling interval to 10°.

While the calculation is running, open a second terminal window (or tab) and 
type `powerfit --help` to have a look at the several features and options of 
PowerFit and what each flag of the previous command means.

PowerFit requires three arguments: the crystal structure of the molecule to be 
fitted (`KsgA.pdb`), the electron density map where to fit 
(`ribosome-KsgA.map`), and the resolution, in Ångstrom, of the density map 
(`13`). 

The `-a` (or `--angle`) option specifies the
rotational sampling interval in degrees, i.e. how tightly the three rotational 
degrees of freedom will be sampled. Lower values will cause PowerFit to perform 
a finer search, at the expense of computational time. The default value is 10°, 
but it can be lowered to 5° for more sensitive searches, or raised to 20° if time 
is an issue or if there aren't sufficient computational resources. For the sake 
of time in this tutorial, we set the sampling interval to this latter coarser 
value. The `-d` option specifies where the results will be stored while the 
`-p` option specifies the number of processors that PowerFit can use during the 
search, to leverage available CPU resources.

Finally, the `-l` flag applies a Laplace pre-filter on the density data, which 
increases the cross-correlation sensitivity by enhancing
edges in the density. In this example scenario, all other options are left at 
their default values but feel free to explore them.

## Analyzing the results

After the search, PowerFit creates a `run-KsgA` directory containing the 
following files:

* `fit_N.pdb`: the best *N* fits, judged by the cross-correlation score.
* `solutions.out`: list all non-redundant solutions, ordered by their
correlation score. The first column shows the cross-correlation score; columns 
2 to 4 are the z, y and x coordinate of the center of the structure; columns 5 
to 14 show the rotation matrix values.
* `lcc.mrc`: a cross-correlation map showing, at each grid position, the 
highest cross-correlation score found during the search, thus showing the most 
likely location of the center of mass of the structure.
* `powerfit.log`: a log file of the calculation, including the input parameters 
with date and timing information.

<a class="prompt prompt-info">
  Open the density map, the *lcc.mrc* cross-correlation map, and the ten 
best-ranked solutions in Chimera.
</a>
<a class="prompt prompt-cmd">
  chimera ribosome-KsgA.map run-KsgA/lcc.mrc run-KsgA/fit_*.pdb
</a>

Make the density map transparent again, by adjusting the alpha channel value to 
0.6. The values of the `lcc.mrc` slider bar
correspond to the cross-correlation score found. In this way, you can
selectively visualize regions of high or low cross-correlation values: i.e., 
pushing the slider to the right (higher cutoff) shows only regions of the grid 
with high cross-correlation scores. 

As you can see, PowerFit found quite some local optima, one of which stands 
out. Further, the ten best-ranked solutions are centered on regions of very 
high local cross-correlation.

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

The structure of the ribosome is available on the RCSB PDB. For simplicity, we 
provide it in the tutorial material: `ribosome.pdb`. In the same session of 
Chimera where you have your chosen fitted KsgA structure, go to `Favorites` → 
`Command Line`. A command line is now present below the main viewing window. 
Use it to load the ribosome structure:

<a class="prompt prompt-pymol">
    open ribosome.pdb
</a>

You now have combined the ribosome structure with the rigid-body fit of KsgA 
calculated by PowerFit, yielding an initial model of the complex. Mutagenesis 
experiments performed on this complex indicate three charged residues of KsgA - 
`R221`, `R222`, and `K223` - that are of special importance for the 
interaction. 

<a class="prompt prompt-info">
Take some time to inspect the model, paying particular attention to these  
three residues and their spatial neighbors.
</a>

In the command line of Chimera, type the following instructions to center your 
view on these residues and highlight their interactions:

<a class="prompt prompt-pymol">
  show #2:221-223 zr<5 & #1 || #2:221-223  
  center #2:221-223 zr<5 & #1 || #2:221-223
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
Map` window, select the best-fitted structure of PowerFit (`fit_1.pdb`) as 
`Fit` model and the original electron density map (`emd-2017.map`) as the map. 
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
resolution of this particular electron density map does not allow the 
identification of side-chain atoms. The quality of the fitted models of 
PowerFit is, therefore, limited.

Given the availability of both the cryo-EM density map and of the mutagenesis 
experiments, we can integrate both in HADDOCK and benefit of its semi-flexible 
refinement protocols to improve the stereochemistry of our model. To use 
cryo-EM data, HADDOCK requires the map and also the approximate positions of 
each chain, as given by their centers of mass. This information is provided 
directly by PowerFit, in the `solutions.out` file, columns 2 to 4 (z,y,x 
coordinates):

<a class="prompt prompt-cmd">
  head -n 10 run-KsgA/solutions.out
</a>

Unfortunately, running HADDOCK is out of the scope of this tutorial and 
requires a significant amount of time. Therefore, we provide the best-ranked 
HADDOCK model, generated by using combining the cryo-EM map, the PowerFit 
centroid positions, and the mutagenesis data, in the tutorial data folder.

<a class="prompt prompt-info">
  Open the density map in Chimera and load the best-ranked HADDOCK model.
</a>

<a class="prompt prompt-cmd">
  chimera ribosome-KsgA.map HADDOCK-ribosome.pdb HADDOCK-KsgA.pdb
</a>

<a class="prompt prompt-question">
Does HADDOCK improve the quality of the model, i.e., reduces the number of 
clashes?
</a>

<a class="prompt prompt-question">
  Are the three residues identified by mutagenesis involved in any 
energetically favourable interaction?
</a>

Finally, to make the impact of HADDOCK more quantitative, we will make a
distance histogram of the contacts between the ribosome and KsgA. First,
combine the ribosome together your preferred PowerFit fit.

<a class="prompt prompt-cmd">
  cat ribosome.pdb run-KsgA/fit_?.pdb > ribosome-KsgA.pdb
</a>

To calculate all the contacts distances, we make use of a standard tool that is
shipped with HADDOCK. 

<a class="prompt prompt-cmd">
  contact-chainID ribosome-KsgA.pdb > ribosome-KsgA.contacts
</a>

Now we can generate the histogram, and visualize it with xmgrace

<a class="prompt prompt-cmd">
  make-contact-histogram.csh ribosome-KsgA.contacts
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
high-resolution structures to an electron density map and how to interpret the 
results. Further, we also showed how integrative modeling using HADDOCK can 
improve the stereochemistry of the models, in particular if done in combination 
with additional experimental data, such as mutagenesis.

Thank you for following this tutorial. If you have any questions or 
suggestions, feel free to contact us via email or by submitting an issue in the 
appropriate Github repository.

[link-powerfit]: https://github.com/haddocking/powerfit "PowerFit"
[link-chimera]: https://www.cgl.ucsf.edu/chimera/ "UCSF Chimera"
[link-data]: https://github.com/haddocking/powerfit-tutorial "PowerFit tutorial data"
