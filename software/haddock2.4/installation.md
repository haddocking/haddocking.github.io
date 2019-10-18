---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK2.4</font> manual

## <font color="RED">I</font>nstallation

* * *

HADDOCK consists of a collection of [python](http://www.python.org) and [CNS](http://cns-online.org) scripts and other additional scripts and programs (csh, awk or gawk, perl, c++). We have been running HADDOCK without problems on linux and MacOSX systems. HADDOCK has also been installed on IBM and SGI systems, requiring modifications in some scripts to properly define the path of awk or gawk. Installation on other architectures should work but has not been tested.  

**Important:** Python version 2.7 or higher (not tested on 3>) and CNS needs to be recompiled with the files provided in the haddock2.4/cns1.3 directory in order to use the new HADDOCK2.4 features (like radius of gyration and pseudo-contact shifts restraints.  

Note that HADDOCK is NOT supported on Windows systems.  

The HADDOCK distribution comes as a gzipped tar file _haddock2.4.tgz_. To install HADDOCK uncompress this file and untar it with:

<pre style="background-color:#DAE4E7">    tar xvfz haddock2.4.tgz
</pre>

This will create a directory called haddock2.4 containing various subdirectories:

*   **Haddock**: contains all the python scripts  

*   **cgi**: cgi scripts (these are installed on our web server). You can install them locally on your server and modify the html files to access them.  

*   **cns1.1**: contains a number of CNS routines (including the VEAN statement) with a few small modifications use with HADDOCK. We recommend to recompile CNS with these routines.  

*   **cns1.2**: contains a number of CNS routines (including the VEAN statement) with a few small modifications use with HADDOCK. We recommend to recompile CNS with these routines.  

*   **doc**: contains a README file pointing to the [online HADDOCK manual](/software/haddock2.4/manual)  

*   **examples**: contains examples for running HADDOCK  

*   **examples-run-data**: contains a script with which pre-calculates example runs can be downlaoded  

*   **protocols**: contains the CNS scripts  

*   **tests**: a short version of the examples to test modifications to the sofware  

*   **tools**: contains various awk, csh and perl scripts for preparation of [PDB files](/software/haddock2.4/pdb) and [analysis](/software/haddock2.4/analysis)  

    **NOTE:** check that the correct location of awk, gawk and perl are defined for your system in the various awk and perl scripts.

*   **toppar**: contains CNS topology and parameter files.  

*   **RDCtools**: contains scripts (python and gawk) to generate RDC restraints (SANI) or intervector projection angle restraints (VEAN) including examples. See [RDC restraints](/software/haddock2.4/RDC_help) for information.  

*   **DANItools**: contains scripts (csh and gawk) to generate diffusion anisotropy restraints (DANI) , calculate tensor parameters and analyze PDB files. See [DANI restraints](/software/haddock2.4/DANI_help) for information.  

In the main haddock directory you will find setup files named **_haddock_configure.csh_** and **_haddock_configure.sh_** which you should edit to define a number of environment variables. Two examples are provided (for setup under MacOSX and linux)  

<pre style="background-color:#DAE4E7">#!/bin/tcsh
#
# HADDOCK configuration file
#
#
setenv HADDOCK /home/abonvin/haddock2.4
setenv HADDOCKTOOLS $HADDOCK/tools
setenv PYTHONPATH $HADDOCK
alias  haddock2.4 `which python` $HADDOCK/Haddock/RunHaddock.py
#
# Define location of third party software
#
setenv NACCESS /software/bin/naccess
setenv PALES   /software/bin/pales
setenv PROFIT  /software/bin/profit
setenv TENSOR2 /software/bin/tensor2
</pre>

**_Note_** that this is a csh/tcsh script. An example of a bash script is also provided.  

Also control the various scripts in the **tools** directory for a proper definition of the location of gawk (or awk if gawk is not installed) and perl and compile the various C++ programs in the **tools** directory by typing in the main haddock directory:

<pre style="background-color:#DAE4E7">   make clean; make
</pre>

If needed, edit the Makefile files in **tools** to define the c++ compiler and compiler flags.  

To initialize and run HADDOCK then simply source the **_haddock_configure.csh_** file with e.g. under csh/tcsh:

<pre style="background-color:#DAE4E7">   source haddock_configure.csh
</pre>

Before running HADDOCK2.4 you need of course to install python version 2.7 or higher and CNS.  

The additional required software and licenses required to run HADDOCK (e.g. CNS) should be obtained directly from the distribution sites. (see the [software links](/software/haddock2.4/software)).  

* * *

_<u>Special topics:</u>_  

If you are going to run HADDOCK without using a queuing system, e.g. simply _csh_, it is recommended to use full pathnames for the job files. This can be defined in the python file **UseLongFilename.py** located in the **Haddock/Main** directory.  

In our environment, we are making use of various queuing systems (PBS, torque) with wrapper scripts that require the jobs to be submitted from the local directory. Because of that our default setup does not use long filenames, i.e. _useLongJobFileNames_ is set to 0.

* * *
