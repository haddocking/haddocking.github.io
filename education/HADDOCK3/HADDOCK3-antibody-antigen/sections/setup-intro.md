## Software and data setup

In order to follow this tutorial you will need to work on a Linux or MacOSX
system. We will also make use of [**PyMOL**](https://www.pymol.org/){:target="_blank"} (freely available for
most operating systems) in order to visualize the input and output data. We will
provide you links to download the various required software and data.

Further, we are providing pre-processed PDB files for docking and analysis (but the
preprocessing of those files will also be explained in this tutorial). The files have been processed
to facilitate their use in HADDOCK and to allow comparison with the known reference
structure of the complex. 

If you are running this tutorial on your own resources _download and unzip the following_
[zip archive](https://surfdrive.surf.nl/public.php/dav/files/R7VHGQM9nx8QuQn){:target="_blank"}
_and note the location of the extracted PDB files in your system_. 

_If running as part of the ASM HPC/AI school or a BioExcel workshop or summerschool see the instructions in the respective next sections._

_Note_ that you can also download and unzip this archive directly from the Linux command line:

<a class="prompt prompt-cmd">
wget https://surfdrive.surf.nl/public.php/dav/files/R7VHGQM9nx8QuQn -O HADDOCK3-antibody-antigen.zip<br>
unzip HADDOCK3-antibody-antigen.zip
</a>


Unziping the file will create the `HADDOCK3-antibody-antigen` directory which should contain the following directories and files:

* `pdbs`: a directory containing the pre-processed PDB files
* `restraints`: a directory containing the interface information and the corresponding restraint files for HADDOCK3
* `runs`: a directory containing pre-calculated results
* `scripts`: a directory containing various scripts used in this tutorial
* `workflows`: a directory containing configuration file examples for HADDOCK3

In case of a workshop of course, HADDOCK3 will usually have been installed on the system you will be using.

In case HADDOCK3 is not pre-installed in your system, you will have to install it.
To obtain HADDOCK3, fill the [registration form](https://docs.google.com/forms/d/e/1FAIpQLScDcd0rWtuzJ_4nftkDAHoLVwr1IAVwNJGhbaZdTYZ4vWu25w/viewform?){:target="_blank"}, and then follow the [installation instructions](https://www.bonvinlab.org/haddock3-user-manual/install.html){:target="_blank"}.

In this tutorial we will use the PyMOL molecular visualisation system. If not already installed, download and install PyMOL from [here](https://pymol.org/){:target="_blank"}. You can use your favourite visualisation software instead, but be aware that instructions in this tutorial are provided only for PyMOL.

This tutorial was last tested using HADDOCK3 version 2024.10.0b7. The provided pre-calculated runs were obtained on a Macbook Pro M2 processors with as OS Sequoia 15.3.1.
