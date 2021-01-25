---
layout: page
title: "Structural Bioinformatics & Modelling"
excerpt: "Introductory M.Sc course to structural bioinformatics and modelling"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modelling, docking, p53, MDM2]
image:
  feature: pages/banner_education-thin.jpg
---

* table of contents
{:toc}


## About this course
The Structural Bioinformatics & Modelling course, created and maintained by the
[Computational Structural Biology group](https://bonvinlab.org){:target="_blank"} of
[Utrecht University](https://www.uu.nl){:target="_blank"}, is aimed
at those interested in learning homology modelling, molecular simulation, and docking of biological
molecules. The course material requires a solid understanding of molecular biology, namely of
protein sequence and structure, as well as familiarity with basic chemistry concepts. Experience
with a UNIX-like command-line environment is not required but helps tying the commands to the
modelling concepts and the biology.

The course is divided into three modules, each covering a particular modelling method. While the
goal is to combine the three methods to answer a biological problem, each module can be followed
independently. Due to the unfortunate COVID-19 reasons, this course has been updated to a fully online version, which can be easily followed remotely.


### Part 1: [Homology modelling](/education/molmod_online/modelling)
This first module is about performing homology modelling of a protein, consisting of Template Search, Template selection, Model building and Model estimation. 

### Part 2: [Molecular dynamic simulations of a peptide](/education/molmod_online/simulation)
This module introduces Molecular Dynamics (MD) simulations of proteins. The simulation protocol can be used as a starting point for the investigation of protein dynamics, provided your system does not contain non-standard groups. By the end of this tutorial, you should know the steps involved in setting up, running, and analyzing a simulation, including critically assessing the choices made at the different steps.

### Part 3: [Protein-peptide docking](/education/molmod_online/docking)
The third module introduces protein-peptide docking using the HADDOCK web server. It also introduces the CPORT web server for interface prediction, based on evolutionary conservation and other biophysical properties. 
By the end of this tutorial, you should know how to setup a HADDOCK run and interpret its results in terms of biological insights.


### Conventions
Each module has its separate set of web pages, but they all share the same conventions. Throughout
the material, colored text will be used to refer to questions or instructions, Linux and/or Pymol
commands, and attention prompts (to avoid distractions!). Students following these tutorials should
try their best and answer these questions, _instead of_ blindly copy-pasting commands!

<a class="prompt prompt-attention">This is an attention prompt: pay special attention to this!</a>
<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it properly!</a>
<a class="prompt prompt-pymol">This is a Pymol prompt: commands are for Pymol only!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>


<hr>
## Requirements

For the homology modelling module we will be using SWISS-MODEL [https://swissmodel.expasy.org](https://swissmodel.expasy.org){:target="_blank"} online modelling tool to perform all stages of homology modelling: Template Search, Template selection, Model building and Model estimation.

The molecular dynamics module requires installation of specific software packages: [GROMACS](https://www.gromacs.org){:target="_blank"}. 
GROMACS is installed on the virtual machines, which students can access via [NMRbox](https://nmrbox.org){:target="_blank"}) (see below). 
Early registration before the course start is necessary [https://nmrbox.org/signup](https://nmrbox.org/signup){:target="_blank"}.

Another software we will be using throughout the course is molecular visualization software [Pymol](https://pymol.org/2/){:target="_blank"}. Pymol can be downloaded for free or used via NMRbox. 

The third module, data-driven docking, uses the [HADDOCK2.4 web server](https://wenmr.science.uu.nl/haddock2.4/){:target="_blank"}, which requires registration but is
free for academic users. All the required [scripts and data](https://github.com/haddocking/molmod-data){:target="_blank"} are available for free
on GitHub. 

Modules 1 (homology modelling) and 3 (docking) can in principle be run from any computer, provided you have web access, and have also installed Pymol.
Module 2 (MD simulations) does require access to terminal and will use Linux commands.
In principle the entire tutorial can also be run from within a [NMRbox](https://nmrbox.org){:target="_blank"} virtual machine (see below).


<hr>
## Use of virtual machines (VMs)

In this course we will be using [**NMR**box](https://nmrbox.org){:target="_blank"}. NMRbox offers cloud-based virtual machines for executing various biomolecular software that can complement NMR (Nuclear Magnetic Resonance). NMRbox users can choose from 226 software packages that focus on research topics as metabolomics, molecular dynamics, structure, intrinsically disordered proteins or binding. One can search through all available packages on [https://nmrbox.org/software](https://nmrbox.org/software){:target="_blank"}.

### Register 
To use virtual machines through NMRbox, one needs to register, preferably with their institutional account [here](https://nmrbox.org/signup){:target="_blank"}. Since the registration has to be manually validated and it can take up to two business days, we strongly encourage students to do so before the course starts. After a successful validation you will receive an e-mail with your NMRbox username and password that you will be using while accessing your virtual machine.

### Accessing NMRbox
To run the virtual machine on a local computer, one needs to install [VNCviewer](https://www.realvnc.com/en/connect/download/vnc/){:target="_blank"}. With the RealVNC client connects your computer to the NMRbox servers with a virtual desktop - graphical interface. More information about the VNC viewer is in the [FAQ of NMRbox](https://nmrbox.org/faqs/vnc-client){:target="_blank"}.
To choose a virtual machine, first log into the user dashboard [https://nmrbox.org/user-dashboard](https://nmrbox.org/user-dashboard){:target="_blank"}. Download the zip file with bookmarks for the production NMRbox virtual machines. Click *File -> Import* connections and select the downloaded zip file. After importing, you will see the current release virtual machines. You can use any available virtual machine. The user-dashboard provides information on machine capabilities and recent compute load, thus it is clever to choose a less occupied one. Double click on one of the VMs. An *“Authentication”* panel appears. Enter your NMRbox username and password. Click on the *“Remember password”* box to have RealVNC save your information. By default, your desktop remains running when you disconnect from it.  If you login to your VM repeatedly you will see a screen symbol next to the VM you connected to recently. For more details follow the quick start guide for using NMRbox with VNC viewer [here](https://api.nmrbox.org/files/quick-start-osx.pdf){:target="_blank"}.


If everything runs correctly you should have a window with your virtual desktop open. In the virtual desktop you have an access to the internet with Chromium as browser or use various programs, including Pymol. Thus, you could run all three stages of this course here or transfer data between your local machine and the virtual machine. File transfer to and from the VM is quite straightforward and it is described here: [https://nmrbox.org/faqs/file-transfer](https://nmrbox.org/faqs/file-transfer){:target="_blank"}.

In this course we will be working with the command line. For those of you who are not familiar with it, a lot of useful tutorials and documentation can be found [here](https://nmrbox.org/faqs/terminal-help). To find the terminal, look for a black icon with a `$_` symbol on it. Once you are familiar with the command line, we can start the Molecular Dynamics tutorial. 

Further NMRbox documentation can be found [here](https://nmrbox.org/pages/documentation){:target="_blank"}.

Once you are done using your VM for the day just log out of it using the top menu button as shown in this [9s video](https://www.youtube.com/watch?v=fHRCij5WJmM&feature=youtu.be){:target="_blank"}.


<hr>
## Tutorial layout & Biological Significance
The E3 ubiquitin-protein ligase MDM2 regulates p53, also known as the _cell's guardian angel_, via
two main mechanisms: ubiquitination-dependent proteasomal degradation and direct inhibition through
binding to a region of the trans-activation domain of p53. Not surprisingly, many cancer types take
advantage of this interplay and overexpress MDM2, making the p53/MDM2 interaction a prime target
for drug development for cancer therapeutics. While many researchers focus on the human p53/MDM2
interaction, we believe mice (Mus musculus) also deserve their share of cutting-edge research, if
only for their long-standing contribution to human disease! Therefore, the aim of this course is to
probe the binding of a peptide sequence of the mouse p53 tumour suppressor protein to mouse MDM2.
Since neither partner has an experimentally determined crystal structure available, this scientific
problem is perfectly suited for a course on computational structural biology.

To this end, the course will describe how to build structural models for the mouse MDM2 protein via
homology modelling and for the p53 trans-activation peptide via molecular dynamics simulations.
Afterwards, the resulting models will seed docking simulations to predict the structure of the
p53/MDM2 complex. The final goal is to suggest a possible interface and produce a starting model to
design and develop drugs that will help save millions of mice! Maybe, with the right amount of
luck, these results will be transferable to the human p53/MDM2 complex and will also contribute to
our well-being.


<hr>
## Get started!
**To get started, click on the icons of the modules**. Since the docking simulations require
structures, we suggest that for last. If time is an issue, start with the molecular dynamics
simulations and, while these run, have fun modelling MDM2.

<table class="three-col-table">
  <tr>
    <td><center><i><b>Homology modelling</b></i></center></td>
    <td><center><i><b>Molecular dynamics</b></i></center></td>
    <td><center><i><b>Docking</b></i></center></td>
  </tr>
  <tr>
    <td>
      <a href="/education/molmod_online/modelling"
         alt="Structure prediction of the mouse MDM2 protein using SSWISS-MODEL"
         title="Structure prediction of the mouse MDM2 protein using SWISS-MODEL">
         <img src="/images/molmod/hm_protein.jpg" class="col-table">
      </a>
    </td>
    <td>
      <a href="/education/molmod_online/simulation"
         alt="Molecular dynamics simulation of a mouse p53 peptide fragment using GROMACS."
         title="Molecular dynamics simulation of a mouse p53 peptide fragment using GROMACS.">
         <img src="/images/molmod/md_ensemble.jpg" class="col-table">
      </a>
    </td>
    <td>
      <a href="/education/molmod_online/docking"
         alt="Data-driven structure prediction of the mouse MDM2/p53 protein-peptide complex using HADDOCK."
         title="Data-driven structure prediction of the mouse MDM2/p53 protein-peptide complex using HADDOCK.">
         <img src="/images/molmod/protein_cmplx.jpg" class="col-table">
      </a>
    </td>
  </tr>
</table>
