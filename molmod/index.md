---
layout: page
title: "Molecular Modelling"
excerpt: "Introductory M.Sc course to molecular modelling and simulation"
tags: [sample post, images, test]
image:
  feature: pages/banner_education-thin.jpg
---

#### About
The Molecular Modelling course, created and maintained by the [Computational Structural
Biology group](http://bonvinlab.org) of [Utrecht University](http://www.uu.nl), is aimed at those
interested in learning homology modelling, molecular simulation, and docking of biological molecules.
The course material assumes you have a solid understanding of molecular biology, namely of protein 
sequence and structure, as well as familiarity with basic chemistry concepts. Experience with a 
UNIX-like command-line environment is not required, but helps to tie the software to the modelling 
concepts more easily.  
  
The course is divided in three modules, each covering a particular modelling method. While the goal 
is to combine the three methods to answer a biological problem, each module is independent and can be
followed on its own. For the two first modules, homology modelling and molecular dynamics, you need 
to acquire specific software packages (that might require licensing) that are nonetheless free for 
academical use. Utrecht University students will be provided with a pre-configured Virtual Image
compatible with [Virtualbox](http://www.virtualbox.org) (also free to install).  
  
Each module has its own separate set of web pages, but they all share the same conventions. Throughout
the material, you will find colored text that might refer to questions or instructions, Linux and/or
Pymol commands, and attention prompts (to avoid distractions!). You should try your best and answer 
the questions and you should *not* blindly copy-paste the commands!  

<a class="prompt prompt-attention">You should pay special attention to this!</a>
<a class="prompt prompt-question">Can you see this question? You should answer it!</a>
<a class="prompt prompt-info">You should follow the instructions written here.</a>
<a class="prompt prompt-pymol">Pymol commands will be displayed here.</a>
<a class="prompt prompt-cmd">These will be used for Linux commands you should insert in the terminal.</a>

#### Layout & Biological Significance
The aim of this course is to computationally probe the binding of an N-terminal peptide sequence of 
the p53 regulator protein, also known as the cell's *guardian angel* due to its tumor suppressor 
function, and the E3 ubiquitin-protein ligase MDM2, which contributes to the inactivation of p53 by two
main pathways: ubiquitination and consequent protesomal degradation; and binding, therefore blocking,
the p53 trans-activation domain. Not surprisingly, many cancer types take advantage of this interplay
and overexpress MDM2, making the p53/MDM2 interaction a prime target for drug development for cancer
therapeutics. For a more in-depth review of the p53/MDM2 interaction, [see this review](http://www.ncbi.nlm.nih.gov/pubmed/14707283).  

While many researchers focus on the human p53/MDM2 interaction, we think that our mice friends also
deserve their share of cutting-edge research, if only for their long-standing contribution to human
disease! As such, you will be asked to study the structure of the mouse (Mus musculus) p53/MDM2 complex.
Since neither partner has an experimentally determined crystal structure available, this scientific 
problem suits computational structural biology approaches perfectly. You will build structural models
for the N-terminal MDM2 domain via homology modelling; for the N-terminal trans-activation peptide
of p53, given its small size, you will use molecular dynamics simulations to probe its conformational
landscape. Finally, using these models, you will predict the structure of the complex through docking
simulations. Maybe, at the end of the course, you will be able to suggest a possible interface and 
produce a starting model to design and develop drugs that will help save millions of mice. Further,
you might be lucky and find features that will be transferrable to our own p53/MDM2 system and also
contribute to our own cure for cancer!

#### Get started!
To get started, click on the titles of the modules. Obviously, you need some sort of models to do the
docking simulations, so we suggest you leave that to the end. If you have limited time, then start 
with the Molecular Dynamics simulations, as these will need to run for a few days. While you wait, 
have fun modelling MDM2.

- Molecular Dynamics  
&nbsp;Exploration of the conformational landscape of an N-terminal mouse p53 peptide sequence using 
[GROMACS](http://www.gromacs.org). 

- [Homology Modelling]({{site.url}}/molmod/modelling1.html)  
&nbsp;Structure prediction of the mouse MDM2 protein using [HMMER](http://hmmer.janelia.org) & 
[MODELLER](https://salilab.org/modeller).  

- Protein-Peptide Docking  
&nbsp;Data-driven structure prediction of the mouse MDM2/p53 complex using [HADDOCK](http://haddocking.org).


### Good luck!
