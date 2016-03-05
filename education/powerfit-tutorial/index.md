---
layout: page
title: "PowerFit Tutorial"
excerpt: "A small tutorial into PowerFit for automatic rigid body fitting"
tags: [PowerFit, Cryo-EM, HADDOCK, Ribosome, Chimera, rigid body fitting]
image:
  feature: pages/banner_education-thin.jpg
---

## Introduction

This tutorial will show you how to utilize the [PowerFit][link-powerfit]
software by applying it on an E.coli ribosome case. To follow this tutorials,
you need, in addition to PowerFit, also the [UCSF Chimera][link-chimera]
visualization software. Chimera is widely used in the cryo-electron microscopy
community for its volume visualiziation capabilities, in addition to several
other tools. We will further discuss the limits of rigid body fitting, and how
HADDOCK can alleviate some of the shortcomings. This tutorial is typically
followed during a workshop, where a Virtual Machine (VM) is provided with all
required software and data. If the VM is not available to you, the data can be
found [here][link-data].

The case we will be investigating is a complex between the 30S maturing E. coli
ribosome and KsgA, a methyltransferase. There are crystal structures available
for the E. coli ribosome and KsgA, and a cryo-EM density map of around 13Å
resolution.


## Inspecting the data

We will first inspect the data that are available to us. Copy the data to the
Desktop by opening a terminal, and change the directory to that location.

    cp -r /opt/powerfit-tutorial ~/Desktop
    cd ~/Desktop/powerfit-tutorial

Next, open the density map together with the already fitted ribosome, and the
crystal structure of KsgA.

    chimera ribosome-KsgA.map ribosome.pdb KsgA.pdb

By using the mouse you can inspect the density and the crystal structures.  Go
to the `Volume Viewer` window. The mean slide bar in the window provides
control on the value where the isosurface of the density will be visualized. By
setting it to high values, the envelope will slink, while setting it to lower
values will even visualize the noise in the map.  We will first make the
density transparent so we can properly see the fitted structure inside:

* Within the `Volume Viewer` click on the grey box next to `Color`, which opens
  the `Color Editor` window.
* In there, check the `Opacity` box. An extra slider bar appears in the box
  called `A`.
* Set the alpha channel value to around 0.6.

You will notice that the density is becoming transparent giving a better view
on the fit of the ribosome model.

On closer inspection you will also notice that there is a part of the density
that is not accounted for; this is the binding location of Ksg. However,
finding the correct orientation of KsgA is not straightforward. PowerFit can
help us here, as it tries to find the best fit based on an objective score.


## Rigid body fitting

PowerFit is a rigid body fitting software that quickly calculates the
cross-correlation, a common measure for the goodness of fit, between the atomic
structure and the density map. It performs a systematic 6-dimensional scan of
the three translational and three rotational degrees of freedom. This means
that PowerFit will try to fit the structure in many orientations at every
position in the map and calculate the cross-correlation.

To see all the options of PowerFit and their descriptions, run the following
command in a terminal

    powerfit --help

To perform the rigid body fitting, run PowerFit with the following command

    powerfit KsgA.pdb ribosome-KsgA.map 13 -d run-KsgA -a 20 -p 2 -l

This command tries to fit the KsgA structure in the ribosome with KsgA density
map, having a resolution of 13Å. The `-a` or `--angle` options specifies the
rotational sampling interval, i.e. how tightly the three rotational degrees of
freedom will be sampled. It should preferably be set to around 10 degree
(default) or even lower (down to 5 degree), but if time or computational
resources are a factor you can set it to 20 degree, which corresponds to 648
different orientations.  The `-d` options allows you to specify where the
results will be stored. The `-p` option specifies the number of processors that
PowerFit can use during the search, to leverage available CPU resources.
Finally, the `-l` flag applies the Laplace pre-filter on the density data.
Suffice to say it increases the cross-correlation sensitivity by enhancing
edges in the density. The other options are left to their default values.

While performing the search, PowerFit will update you on the progress of the
search. The tutorial is aimed at a search time of around 5 minutes. If the ETA
is substantally lower, you can increase the rotational sampling interval to 10
degree.


## Analyzing the results

After the search, PowerFit has created the run-KsgA directory that contains the
following files:

* *fit_N.pdb*: the top *N* best fits.
* *solutions.out*: all non-redundant solutions found, ordered by their
correlation score. The first column shows the correlation score; column 2 to 4
are the z, y and x coordinate of the center of the chain; column 5 to 14 are
the rotation matrix values.
* *lcc.mrc*: a cross-correlation map, showing at each grid position the highest
correlation score found during the search. This provides a clear indication of
where the center of mass of the chain is likely to be found.
* *powerfit.log*: a log file, including the input parameters with date and
timing information.

To analyze the results, open the density map, together with the
cross-correlation map `lcc.mrc`, and the top 10 solutions

    chimera ribosome-KsgA.map run-KsgA/lcc.mrc run-KsgA/fit_*.pdb

Make the density map transparent again. The value of the `lcc.mrc` slide bar
corresponds to the cross-correlation score found, and by adjusting it you can
visualize regions of high cross-correlation values. The further the bar is set
to the right, the higher the cross-correlation values are. As you can see,
there are quite some local optima found by PowerFit, but one position sticks
out. The top 10 fits are also shown, notice how their center is positioned on
the local correlation optima. Inspect the fits, and check if you agree with the
fit that PowerFit proposes as the best solution. Close Chimera, and reopen it
with the density map, and the fit that you liked best, like this (change `?` to
the number you want)

    chimera ribosome-KsgA.map ribosome.pdb run-KsgA/fit_?.pdb

Next, open the ribosome structure within Chimera. Go to `Favorites` → `Command
Line`. A command line is now popping up under the main viewing window. In it type

    open ribosome.pdb

Together with the rigid body fit of KsgA, we have now an initial model of the
complex. Additional mutagenesis experiments have been performed for this
complex that indicated that 3 charged residues of KsgA are involved in the
interaction with the ribosome, namely R221, R222 and K223. To visualize those
residues and their interacting neighbours, input the following commands in the
command line

    show #2:221-223 zr<5 & #1 || #2:221-223
    center #2:221-223 zr<5 & #1 || #2:221-223

Check whether there are any clashes between the ribosome and KsgA chains, and
also whether the three important amino acids are making proper interactions.

UCSF Chimera also allows to locally optimize the fit of a rigid chain against
the density.  Make the main display window active by clicking on it, then go to
`Tools` → `Volume data` → `Fit in Map`. A new `Fit in Map` window will be
opened. Select as `Fit` model `fit_1.pdb` in map `emd-2017.map`. Press `Fit` to
start the optimization. However, the scoring function that is used by Chimera
here makes the fit actually worse, and KsgA is now classing with the ribosomal
RNA. Click `Undo` in the `Fit in Map` window to undo the optimization.

Next, we will try to optimize the fit using the cross-correlation that UCSF
Chimera provides. Click `Options` and check the `Use map simulated from atoms,
resolution` box and fill in `13` for resolution. Check the `correlation`
radiobox and uncheck the `Use only data above contour level from first map`.
Press `Fit` and investigate whether this improves the situation.


## Integrative modeling with HADDOCK

The obvious limitation of rigid body fitting is of course that conformational
changes are not acounted for. Since the resolution of the density map is too
low to properly see the arrangement of the side-chains, we need another modeling
tool. Because of the ambiguous cryo-EM data and the complementing mutagenesis
information available, our docking software HADDOCK is a worthwhile choice.
HADDOCK requires in addition to the cryo-EM data also the approximate position
of the center of mass of a chain, in this case of the KsgA. This information
can easily be extracted from the PowerFit run.

Print the first 10 lines of the `solutions.out` in the terminal

    head -n 10 run-KsgA/solutions.out

As stated above, column 2 to 4 correspond to the z, y, and x coordinate center
of mass of KsgA in the density map. We have added the best scoring HADDOCK
model that is formed when combining all the data available, as setting up a
HADDOCK run falls outside the scope of this tutorial. Open the density map and
HADDOCK models

    chimera ribosome-KsgA.map HADDOCK-ribosome.pdb HADDOCK-KsgA.pdb

Visualize the important residues again. Check if they are any clashes and
whether energetically favorable interactions are formed.

This ends the tutorial, where we have set up a PowerFit run, visualized and
analyzed the results. We also explained how the data can be further used to
perform more complicated modeling through HADDOCK to adjust for the ambiguity
of the data and the flexiblity of the side-chains.


[link-powerfit]: https://github.com/haddocking/powerfit "PowerFit"
[link-chimera]: https://www.cgl.ucsf.edu/chimera/ "UCSF Chimera"
[link-data]: https://github.com/haddocking/powerfit-tutorial "PowerFit tutorial data"
