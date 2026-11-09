---
layout: page
title: "PowerFit Tutorial"
excerpt: "A small tutorial on PowerFit for automatic rigid body fitting"
tags: [PowerFit, Cryo-EM, Ribosome, ChimeraX, rigid body fitting]
image:
  feature: pages/banner_education-thin.jpg
---

This tutorial consists of the following sections:

* table of contents
{:toc}

This tutorial was last updated on 08-11-2026 and is up-to-date 
with release v6.1.0. <br>

## Introduction

PowerFit is a software application developed to fit atomic resolution
structures of biomolecules to cryo-electron microscopy (cryo-EM) density maps.
It is open-source and available for download on [Github][link-powerfit]. In addition 
you can find a manual on usage of PowerFit [here][link-manual]. 

This tutorial will show you how to utilize PowerFit by applying it to an E.coli
ribosome case. To follow this tutorial, you need, in addition to PowerFit, the
[UCSF ChimeraX][link-chimerax] visualization software, a popular tool in the
cryo-electron microscopy community for its volume visualization capabilities.
We will further discuss the limits of rigid body fitting and compare the
models with experimental structures of the complex. We provide the data
necessary to run this tutorial [here][link-data]. If you do not want to install
PowerFit, the same case can be run with our [PowerFit web server][link-powerfit-web-tuto].

PowerFit is described in

* G.C.P. van Zundert and A.M.J.J. Bonvin.
[Fast and sensitive rigid-body fitting into cryo-EM density maps with PowerFit](https://doi.org/doi:10.3934/biophy.2015.2.73).
_AIMS Biophysics_. *2*, 73-87 (2015).

* G.C.P. van Zundert and A.M.J.J. Bonvin.
[Defining the limits and reliability of rigid-body fitting in cryo-EM maps using multi-scale image pyramids](https://doi.org/10.1016/j.jsb.2016.06.011).
_J. Struct. Biol._ *195*, 252-258 (2016).

Throughout the tutorial, colored text will be used to refer to questions or 
instructions, Linux and/or ChimeraX commands.

<a class="prompt prompt-question">This is a question prompt: try answering 
it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a ChimeraX prompt: write this in the 
ChimeraX command line!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the 
terminal!</a>

The case we will be investigating is a complex between the 30S E. coli
ribosomal subunit and RsgA, a GTPase involved in ribosome biogenesis. There
are models ([2YKR][link-pdb]) and a cryo-EM density map of around 9.8Å
resolution ([EMD-1884][link-density]) available for the complex.



## Setup

### Installing PowerFit

PowerFit is a Python package that requires Python 3.11 or greater. It runs on
Linux, macOS and Windows. We recommend installing it in its own virtual
environment.

<a class="prompt prompt-info">
  Create and activate a virtual environment, and install PowerFit in it.
</a>
<a class="prompt prompt-cmd">
    python3 \-m venv powerfit-env <br>
    source powerfit-env/bin/activate <br>
    pip install powerfit-em
</a>

If you use a csh or tcsh shell, activate the environment with `source
powerfit-env/bin/activate.csh` instead. On macOS, also install pyFFTW, which
makes the search faster and is needed for the map used in this tutorial (see
[this issue][link-issue-fft]):

<a class="prompt prompt-cmd">
    pip install pyfftw
</a>

Check that the installation worked:

<a class="prompt prompt-cmd">
    powerfit \-\-version
</a>

This installs the CPU version of PowerFit, which is all you need for this
tutorial. To run PowerFit on a GPU, follow the [installation
instructions][link-install] for your operating system.

You will also need [UCSF ChimeraX][link-chimerax] to visualize the data and
the results, and a web browser to view the PowerFit report.

**Note:** In this tutorial we start ChimeraX from the command line with the
files to load (e.g. `chimerax ribosome-RsgA.map ribosome.pdb`). If the
`chimerax` command is not available in your terminal, start the ChimeraX
application instead and load the same files with the `File > Open...` menu.

### Getting the data

We prepared a folder that contains the cryo-EM density map file in CCP4 format
(`ribosome-RsgA.map`), the model of the ribosome (`ribosome.pdb`), which has
already been fitted in the density, and the model of RsgA (`RsgA.pdb`), taken
from the 2YKR entry, centred at the origin and randomly rotated so that it
does not start from its position in the map. It also contains the
experimental structure `7NAR.pdb`, used at the end of the tutorial, in case it
cannot be downloaded from the PDB.

<a class="prompt prompt-info">
  Download the data and unpack the archive.
</a>
<a class="prompt prompt-cmd">
    curl \-L \-O https://www.bonvinlab.org/education/Others/powerfit/powerfit-tutorial.zip <br>
    unzip powerfit-tutorial.zip <br>
    cd powerfit-tutorial
</a>



## Inspecting the data

Let us first inspect the data we have available, namely the cryo-EM density map
and the structures we will attempt to fit. 

Using ChimeraX, we can easily visualize and inspect the density and models,
mostly through a few mouse clicks.

<a class="prompt prompt-info">
  Open the density map together with the ribosome and RsgA.
</a>
<a class="prompt prompt-cmd">
    chimerax ribosome-RsgA.map ribosome.pdb RsgA.pdb
</a>

In the `Volume Viewer` window, the middle slide bar provides control on the
value at which the isosurface of the density is shown. At high values, the
envelope will shrink while lower values might even display the noise in the map.
We will first make the density transparent, to see the fitted structure inside:

<a class="prompt prompt-pymol">
  transparency #1 60
</a>

Notice that the density becomes transparent providing a better view of the fit
of the ribosome model. On closer inspection, you can also discern a region of
the density that is not accounted for by the ribosome structure alone; this is
the binding location of RsgA. If you cannot find it, try to lower the value of
the isosurface using the slider in the `Volume Viewer` window. RsgA itself is
located at the origin of the coordinate system, outside of the density.
Although you could try and manually place it in the empty region of the
density, finding the correct orientation is not straightforward. PowerFit can
help here as it attempts to find the best fit automatically and exhaustively,
based on an objective score.


## Rigid body fitting

PowerFit is a rigid body fitting software that quickly calculates the 
cross-correlation, a common measure of the goodness-of-fit, between the atomic 
structure and the density map. It performs a systematic 6-dimensional scan of 
the three translational and three rotational degrees of freedom. In short, 
PowerFit will try to fit the structure in many orientations at every position 
on the map and calculate a cross-correlation score for each of them.

<a class="prompt prompt-info">
  Perform the rigid-body fitting of the RsgA structure on the cryo-EM density
  map.
</a>
<a class="prompt prompt-cmd">
  powerfit ribosome-RsgA.map 9.8 RsgA.pdb \-d run-RsgA \-p 4 \-\-report \-\-delimiter , \-\-progressbar
</a>

While performing the search, PowerFit will update you on the progress of the 
search. The example case in this tutorial should run in a few minutes.

**Note:** The command above uses 4 processors (`-p 4`). If your computer has
more CPU cores, you can increase this value to speed up the search (e.g.
`-p 8`). You can check the number of cores with `nproc` on Linux or
`sysctl -n hw.ncpu` on macOS.

**Note:** If the search is much slower than expected, check whether the
`OMP_NUM_THREADS` environment variable is set (`echo $OMP_NUM_THREADS`). Each
PowerFit process then uses that many threads for its FFTs, and with several
processors (`-p`) the computer gets overloaded. Set it to 1 before running
PowerFit with `export OMP_NUM_THREADS=1` (bash/zsh) or
`setenv OMP_NUM_THREADS 1` (csh/tcsh).

While the calculation is running, open a second terminal window (or tab) and 
type `powerfit --help` to have a look at the several features and options of 
PowerFit and what each flag of the previous command means.

PowerFit requires three arguments: a target cryo-EM density map to fit the
structure in (`ribosome-RsgA.map`), the resolution, in ångstrom, of the
density map (`9.8`), and a high-resolution atomic structure of the
biomolecule to be fitted (`RsgA.pdb`).

The `-a` (or `--angle`) option, not used here, specifies the rotational
sampling interval in degrees, i.e. how tightly the three rotational degrees of
freedom will be sampled. Lower values will cause PowerFit to perform a finer
search, at the expense of computational time. The default value of 10° is used
in this tutorial; it can be lowered to 5° for more sensitive searches, or
raised to 20° if time is an issue or if there aren't sufficient computational
resources. The `-d` option specifies where the results will be stored while
the `-p` option specifies the number of processors that PowerFit can use
during the search, to leverage available CPU resources. The `--report` option
creates an HTML report with an interactive 3D view of the best fits; it
requires `--delimiter ,`, which writes the `solutions.out` file in
comma-separated format.

In this example scenario, all other options are left at their default values,
which are also the defaults of the PowerFit web server, but feel free to
explore [them][link-manual].


## Analyzing the results

After the search, PowerFit creates a `run-RsgA` directory containing the 
following files:

* `fit_N.pdb`: the best *N* fits, judged by the cross-correlation score.
* `solutions.out`: all the non-redundant solutions found, ordered by their
correlation score. The first column shows the rank, column 2 the correlation
score, column 3 and 4 the Fisher z-score and the relative z-score (the number
of standard deviations); column 5 to 7 are the x, y and z coordinate of the
center of the chain; column 8 to 16 are the rotation matrix values.
* `lcc.mrc`: a cross-correlation map showing, at each grid position, the 
highest cross-correlation score found during the search, thus showing the most 
likely location of the center of mass of the structure.
* `powerfit.log`: a log file of the calculation, including the input parameters 
with date and timing information.
* `report.html` and `state.mvsj`: an HTML report and its
[MolViewSpec][link-molviewspec] state file, with an interactive 3D view of the
best fits. A copy of the density map is placed next to them for the viewer.

### Viewing the report

The report loads its data from the files in the `run-RsgA` directory, so it
must be opened through a web server rather than by double-clicking
`report.html`. Python comes with a simple one.

<a class="prompt prompt-info">
  Start a local web server in the results directory.
</a>
<a class="prompt prompt-cmd">
  python3 \-m http.server \-d run-RsgA
</a>
<a class="prompt prompt-info">
  Open http://localhost:8000/report.html in your web browser.
</a>

At the top of the report, a Mol* viewer shows the density map with the best
non-redundant solutions. While clicking through the models, the viewer reports
the rank, cross-correlation score, Fisher z-score and sigma difference of each
fit. Below the viewer, a table lists these values for all solutions. A
difference in Fisher z-score of more than ~2.5 standard deviations between the
two top solutions indicates a reliable fit; this is explained in more detail in
the [PowerFit web server tutorial][link-powerfit-web-tuto], whose result page
is the same report.

<a class="prompt prompt-question">
  Based on the sigma differences, does PowerFit find one solution that clearly
  stands out?
</a>

When you are done, stop the web server by pressing `Ctrl-C` in the terminal.

### Inspecting the fits in ChimeraX

For a closer look at the fits, we will now use ChimeraX.

<a class="prompt prompt-info">
  Open the density map, the <i>lcc.mrc</i> cross-correlation map, and the 10 
best-ranked solutions in ChimeraX.
</a>
<a class="prompt prompt-cmd">
  chimerax ribosome-RsgA.map run-RsgA/lcc.mrc ribosome.pdb run-RsgA/fit_*.pdb
</a>

Make the density map transparent again to 60.
The values of the `lcc.mrc` slider bar correspond to the cross-correlation
score found. In this way, you can selectively visualize regions of high or low
cross-correlation values: i.e., pushing the slider to the right (higher cutoff)
shows only regions of the grid with high cross-correlation scores. 

As you can see, PowerFit found quite some local optima, one of which stands out.
Further, the 10 best-ranked solutions are centered on regions corresponding to
local cross-correlation maxima.

To view each fitted solution individually, in the main panel, go to `Tools`
→ `Models` to open the `Model Panel` window. The window shows each model
and its associated color that ChimeraX has processed. To show or hide a specific
model you can click the box in the column with an eye.

<a class="prompt prompt-info">
  Go through the 10 solutions one by one to appreciate their goodness-of-fit
  with the density.
</a>
<a class="prompt prompt-question">
  Do you agree with what PowerFit proposes as the best solution?
</a>

<a class="prompt prompt-info">
  In a new ChimeraX session, reopen the density map and the fit that you find 
best. Replace <i>?</i> by the appropriate solution number.
</a>
<a class="prompt prompt-cmd">
  chimerax ribosome-RsgA.map ribosome.pdb run-RsgA/fit_?.pdb
</a>

You now have combined the ribosome structure with the rigid-body fit of RsgA
calculated by PowerFit, yielding an initial model of the complex. Take a closer
look at residues `R47` to `H51` of RsgA, which contribute to the interface with
the ribosome.

In the same session of ChimeraX where you have your chosen fitted RsgA
structure, type in the command line of ChimeraX the
following instructions to center your view on these residues and highlight
their interactions:

<a class="prompt prompt-pymol">
  hide #2 atoms <br>
  show #2 cartoons <br>
  sel #3:47-51 <br>
  view sel <br>
  contacts sel distanceOnly 5.0 makePseudobonds true reveal true <br>
</a>
<a class="prompt prompt-info">
  Take some time to inspect the model, paying particular attention to these five
  residues and their spatial neighbors.
</a>

### Clash analysis

Since PowerFit treats the structures as rigid bodies and only considers their
fit into the density, the fitted model can contain clashes with the ribosome.
ChimeraX can find all atom pairs between RsgA and the ribosome that overlap
too much:

<a class="prompt prompt-pymol">
  ~contacts <br>
  clashes #3 restrict cross reveal true
</a>

The number of clashes is reported in the bottom bar of the ChimeraX window and
in the `Log`; the clashes are shown as pseudobonds between the atoms.

<a class="prompt prompt-question">
  How many clashes are there between the ribosome and RsgA? Which parts of
  RsgA are involved?
</a>

ChimeraX also includes a tool to locally optimize the fit of a rigid structure 
against a given density map, which can be an additional help on top of the 
PowerFit calculations. To judge whether the optimization improves the fit, we
first calculate the correlation between the density map and a map simulated
from the PowerFit model at 9.8 Å, without moving the model:

<a class="prompt prompt-pymol">
  fitmap #3 inMap #1 resolution 9.8 metric correlation shift false rotate false
</a>

Note the `correlation` and `correlation about mean` values reported in the
`Log`. ChimeraX also adds the simulated map as a
new model, which you can hide in the `Models` panel.

<a class="prompt prompt-info">
  Make the main display window active by clicking on it. <br>
  Go to <i>Tools</i> → <i>Volume Data</i> → <i>Fit in Map</i>. <br>
  In the <i>Fit in Map</i> window, select the best-fitted structure of PowerFit (<i>fit_?.pdb</i>) as <i>Fit</i> model and the original density map (<i>ribosome-RsgA.map</i>) as the map. <br>
  Press <i>Fit</i> to start the optimization.
</a>

<a class="prompt prompt-question">
  Does the ChimeraX local fit optimization tool improve the results of
  PowerFit? Calculate the correlation again with the same <i>fitmap</i> command
  and compare it with the value before the fit. Repeat the clash analysis to
  check.
</a>

<a class="prompt prompt-info">
  If the optimization does not improve the fit, click <i>Undo</i> in the <i>Fit in Map</i> window.
</a>

Next, we will try to optimize the fit using the cross-correlation that ChimeraX 
provides.

<a class="prompt prompt-info">
  Click <i>Options</i>. <br>
  Check the <i>Use map simulated from atoms, resolution</i> box and fill in <i>9.8</i> for the resolution. <br>
  Check the <i>correlation</i> radio button. <br>
  Uncheck the <i>Use only data above contour level from first map</i> box. <br>
  Press <i>Fit</i>.
</a>

<a class="prompt prompt-question">
  Does this second strategy improve the quality of the fit? Compare again the
  correlation and the clashes with the values before the fit. If it does not
  improve, undo it again.
</a>


## Comparison with experimental structures

Since the publication of the 9.8Å map, higher resolution cryo-EM structures of
RsgA bound to the 30S subunit have been determined, for example
[7NAR][link-7nar] (3.0Å), [5NO2][link-5no2] (5.2Å) and [5UZ4][link-5uz4]
(5.8Å). We can use them to check how close our models are to the experimental
structure. To compare the position of RsgA, we first superimpose the 16S
ribosomal RNA of the experimental structure on the one of our ribosome model.
We then calculate the root mean square deviation (RMSD) of the C-alpha atoms
of RsgA, without any further fitting.

<a class="prompt prompt-info">
  Open the ribosome and your preferred PowerFit fit in a new ChimeraX session.
</a>
<a class="prompt prompt-cmd">
  chimerax ribosome.pdb run-RsgA/fit_?.pdb
</a>
<a class="prompt prompt-info">
  Download the 7NAR structure from the PDB and superimpose its 16S rRNA (chain
  A) on the one of the ribosome model.
</a>
<a class="prompt prompt-pymol">
  open 7nar <br>
  matchmaker #3/A to #1/A cutoffDistance none <br>
  hide atoms <br>
  show cartoons
</a>

**Note:** If the download from the PDB fails (e.g. network problems), use the
copy of the structure provided in the tutorial data instead: replace
`open 7nar` by `open 7NAR.pdb`.

RsgA is chain W in 7NAR. Our RsgA model has a few gaps, so we select in 7NAR
only the residues that are also present in the model:

<a class="prompt prompt-pymol">
  rmsd #2@CA to #3/W:35-85,93-110,116-237,251-337@CA
</a>
<a class="prompt prompt-question">
  How close is the PowerFit fit to the experimental structure?
</a>
<a class="prompt prompt-info">
  Open the other top-ranked PowerFit solutions, show them as ribbons only
  (<i>hide atoms</i>, <i>show cartoons</i>) and calculate their RMSD in the
  same way, adapting the model number.
</a>
<a class="prompt prompt-question">
  Does the best-scoring PowerFit solution also have the lowest RMSD?
</a>

The experimental structure also tells us how many clashes to expect between
RsgA and the ribosome in a well-refined model:

<a class="prompt prompt-pymol">
  clashes #3/W restrict cross interModel false
</a>
<a class="prompt prompt-question">
  How does this number compare with the one you found for the PowerFit fit?
</a>

Finally, we can score the experimental position of RsgA in our density map.
Save RsgA from 7NAR in the coordinate frame of the ribosome model:

<a class="prompt prompt-pymol">
  select #3/W <br>
  save RsgA-7NAR.pdb models #3 selectedOnly true relModel #1
</a>

The `powerfit-score` command, installed together with PowerFit, calculates the
cross-correlation, Fisher z-score and relative z-score of a structure at its
current position in the map, without any rotational or translational search.

<a class="prompt prompt-cmd">
  powerfit-score ribosome-RsgA.map 9.8 RsgA-7NAR.pdb <br>
  powerfit-score ribosome-RsgA.map 9.8 run-RsgA/fit_?.pdb
</a>

The scores are printed in the same comma-separated format as `solutions.out`.
Note that the score of a PowerFit fit can differ from the one reported in
`solutions.out`, as `powerfit-score` rebuilds the density from the atomic
coordinates instead of rotating precomputed grids (see `powerfit-score --help`).
Also note that RsgA in 7NAR contains more residues than our model.

<a class="prompt prompt-question">
  How does the fit of the experimental structure in the density compare with
  the PowerFit solution?
</a>

The experimental structures differ between them by a few ångstrom, as they
capture different states of the 30S subunit; you can repeat the comparison
with 5NO2 or 5UZ4 (RsgA is chain Z in both) to see how much.


## BONUS: how robust is the fit to the starting orientation?

PowerFit samples a fixed set of rotations, here every 10°. The orientation of
the input structure therefore determines how close the sampled rotations come
to the correct one. To test how much this matters, create rotated copies of
RsgA in ChimeraX and fit each of them. RsgA is centred at the origin, so we
rotate it around the origin:

<a class="prompt prompt-pymol">
  open RsgA.pdb <br>
  turn x 45 models #1 center 0,0,0 coordinateSystem #1 <br>
  save RsgA-x45.pdb models #1 <br>
  close <br>
  open RsgA.pdb <br>
  turn y 90 models #1 center 0,0,0 coordinateSystem #1 <br>
  save RsgA-y90.pdb models #1 <br>
  close <br>
  open RsgA.pdb <br>
  turn z 135 models #1 center 0,0,0 coordinateSystem #1 <br>
  save RsgA-z135.pdb models #1
</a>
<a class="prompt prompt-cmd">
  powerfit ribosome-RsgA.map 9.8 RsgA-x45.pdb \-d run-x45 \-p 2 \-\-report \-\-delimiter , <br>
  powerfit ribosome-RsgA.map 9.8 RsgA-y90.pdb \-d run-y90 \-p 2 \-\-report \-\-delimiter , <br>
  powerfit ribosome-RsgA.map 9.8 RsgA-z135.pdb \-d run-z135 \-p 2 \-\-report \-\-delimiter ,
</a>

For each run, look at the two top solutions in `solutions.out`, and calculate
the RMSD of `fit_1.pdb` to 7NAR as described above.

<a class="prompt prompt-question">
  Is the position of the best solution robust to the starting orientation?
  And its score and the sigma difference to the second solution?
</a>
<a class="prompt prompt-question">
  What happens if you use a finer rotational sampling (<i>-a 5</i>) for one of the
  orientations?
</a>

<details style="background-color:#f2f2f2; padding:10px 15px; border-radius:4px;">
  <summary style="font-weight:bold; cursor:pointer;">
    <i>See our results</i>
  </summary>

<table>
  <tr><th>Input orientation</th><th>Sampling</th><th>cc rank 1</th><th>Sigma difference rank 1-2</th><th>CA-RMSD fit_1 to 7NAR</th></tr>
  <tr><td><i>RsgA.pdb</i></td><td>10°</td><td>0.401</td><td>4.3</td><td>4.6 Å</td></tr>
  <tr><td><i>RsgA-x45.pdb</i></td><td>10°</td><td>0.417</td><td>6.4</td><td>3.8 Å</td></tr>
  <tr><td><i>RsgA-y90.pdb</i></td><td>10°</td><td>0.398</td><td>2.1</td><td>4.6 Å</td></tr>
  <tr><td><i>RsgA-z135.pdb</i></td><td>10°</td><td>0.451</td><td>4.9</td><td>3.8 Å</td></tr>
  <tr><td><i>RsgA.pdb</i></td><td>5°</td><td>0.441</td><td>5.0</td><td>3.8 Å</td></tr>
  <tr><td>another random orientation</td><td>10°</td><td>0.361</td><td>0.2</td><td>4.9 Å</td></tr>
  <tr><td>another random orientation</td><td>5°</td><td>0.431</td><td>2.5</td><td>4.0 Å</td></tr>
</table>

<p>
  In all cases, the best solution is found at the same position, with
  orientations within 3.5 Å RMSD of each other and 4-5 Å from the experimental
  structure. The cross-correlation and the sigma difference to the second
  solution, however, depend on how close the sampled rotations come to the
  correct orientation: for some orientations, the sigma difference drops below
  the ~2.5 threshold, even though the solution is correct. A finer rotational
  sampling gives a higher score and makes the result less dependent on the
  starting orientation, at the cost of an about seven times longer run. When
  the sigma difference is close to the threshold, it is therefore worth
  repeating the search with a different starting orientation or a finer
  rotational sampling.
</p>
</details>


## Conclusions

In this tutorial, we showed you how to use PowerFit to fit high-resolution
structures to a cryo-EM density map, how to interpret the results, and how to
compare the models with experimental structures. The obvious limitation of
rigid-body fitting is that it cannot account for any conformational changes
the structures might undergo, resulting in clashes at the interface between
the molecules. Further, the low resolution of this particular density map does
not allow the identification of side-chain atoms. Such models can be refined
with flexible refinement protocols, for example with HADDOCK using the cryo-EM
data as restraints:

* G.C.P. van Zundert, A.S.J. Melquiond and A.M.J.J. Bonvin.
[Integrative modeling of biomolecular complexes: HADDOCKing with Cryo-EM data.](https://doi.org/10.1016/j.str.2015.03.014)
_Structure._ *23*, 949-960 (2015).

Thank you for following this tutorial. If you have any questions or 
suggestions, feel free to contact us via email or by submitting an issue in the 
appropriate Github repository.

[link-powerfit]: https://github.com/haddocking/powerfit "PowerFit"
[link-chimerax]: https://www.cgl.ucsf.edu/chimerax/ "UCSF ChimeraX"
[link-data]: /education/Others/powerfit/powerfit-tutorial.zip "PowerFit tutorial data"
[link-density]: https://www.ebi.ac.uk/pdbe/entry/emdb/EMD-1884 "Ribosome RsgA density"
[link-pdb]: https://www.rcsb.org/structure/2YKR "PDBid 2YKR"
[link-manual]: https://bonvinlab.org/powerfit/manual.html "PowerFit manual"
[link-install]: https://bonvinlab.org/powerfit/installation.html "PowerFit installation"
[link-issue-fft]: https://github.com/haddocking/powerfit/issues/160 "PowerFit issue 160"
[link-molviewspec]: https://molstar.org/mol-view-spec/ "MolViewSpec"
[link-powerfit-web-tuto]: /education/Others/powerfit-webserver "PowerFit web server tutorial"
[link-7nar]: https://www.rcsb.org/structure/7NAR "PDBid 7NAR"
[link-5no2]: https://www.rcsb.org/structure/5NO2 "PDBid 5NO2"
[link-5uz4]: https://www.rcsb.org/structure/5UZ4 "PDBid 5UZ4"
