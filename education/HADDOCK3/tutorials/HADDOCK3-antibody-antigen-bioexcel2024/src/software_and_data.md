## Software and data setup

In order to follow this tutorial you will need to work on a Linux or MacOSX system.
We will also make use of [**PyMOL**](https://www.pymol.org/) (freely available for most operating systems) in order to visualize the input and output data.
We will provide you links to download the various required software and data.

Further, we are providing pre-processed PDB files for docking and analysis (but the preprocessing of those files will also be explained in this tutorial).
The files have been processed to facilitate their use in HADDOCK and to allow comparison with the known reference structure of the complex.

If you are running this tutorial on your own resources _download and unzip the following_ [zip archive](https://surfdrive.surf.nl/files/index.php/s/ts2kMjBFxjaNeId) _and note the location of the extracted PDB files in your system_.
If running as part of the EU-ASEAN HPC school see the instructions below.

_Note_ that you can also download and unzip this archive directly from the Linux command line:

<a class="prompt prompt-cmd">
wget https://surfdrive.surf.nl/files/index.php/s/ts2kMjBFxjaNeId/download -O HADDOCK3-antibody-antigen.zip<br>
unzip HADDOCK3-antibody-antigen-BioExcel.zip
</a>


Unziping the file will create the `HADDOCK3-antibody-antigen-BioExcelSS2024` directory which should contain the following directories and files:

* `pdbs`: a directory containing the pre-processed PDB files
* `restraints`: a directory containing the interface information and the corresponding restraint files for HADDOCK3
* `runs`: a directory containing pre-calculated results
* `scripts`: a directory containing various scripts used in this tutorial
* `workflows`: a directory containing configuration file examples for HADDOCK3
