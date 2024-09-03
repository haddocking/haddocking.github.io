---
layout: page
title: ""
excerpt: ""
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, manual, usage]
image:
  feature: pages/banner_software.jpg
---

* table of contents
{:toc}

<hr>

# How to install haddock3

To install haddock3, you will need to sucessfully manage to get your hands on the following four steps:

* [Download haddock3 source code](#download-haddock3)
* [Install CNS](#install-cns)
* [Setup a virual environment](#virtual-environments)
* [Finalise installation](#finalise-installation)

A complete guide is also available on our [haddock3 GitHub repository](https://github.com/haddocking/haddock3/blob/main/docs/INSTALL.md).


## Download haddock3

Haddock3 is an open source software and therefore its source code can be downloaded at any time.
We are hosting the code on a dedicated [GitHub repository](https://github.com/haddocking/haddock3/), allowing for better version control, code development and maintainability.

For usage tracking purposes (to avoid counting robots downloading the tool), we advise users to download it from our [lab page](https://www.bonvinlab.org/software/haddock3/#haddock3-distribution-download), as it allows us for easier reporting to authoritise supporting the development of this project with grants.


## Install CNS

HADDOCK is using [Crystallography & NMR System (CNS)](http://cns-online.org/v1.3/) as core computing engine.
CNS is a FORTRAN66 code that must be compiled on your machine, for your own hardware.
Please see the up-to-date installation procedure of CNS [here](https://github.com/haddocking/haddock3/blob/main/docs/CNS.md), where you will find specific guide and troubleshooting sections.

## Virtual environments

Haddock3 makes use of system variables as well as external libraries.
To ensure a reproducible and stable functional version of haddock3, we strongly advise to intall it using a virual environment.
When used from within a virtual environment, common installation tools such as `pip` will install Python packages into a virtual environment without needing to be told to do so explicitly.

Two major environment managing system are effective and capable of installing haddock3, namely 
[venv](https://docs.python.org/3/library/venv.html)
and [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
Below you will find the instruction on how to install them and setup a proper haddock3 environment.


### venv

As the `venv` library is part of the python3 standard library, hence there is no need to installing it, considering python3 is installed on your machine.
By using `venv`, you will be able to set the python3 version you want (>=3.9 for haddock3).

For more details and troubleshooting with the `venv` library, have a look at [its documentation](https://docs.python.org/3/library/venv.html)

### Anaconda / miniconda

For more details and troubleshooting with the `conda` library, have a look at [its documentation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)


## Finalise installation

A complete guide on how to [install haddock3 is available here](https://github.com/haddocking/haddock3/blob/main/docs/INSTALL.md).