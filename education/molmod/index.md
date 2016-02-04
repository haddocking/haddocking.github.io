---
layout: page
title: "Structural Bioinformatics & Modelling"
excerpt: "Introductory M.Sc course to structural bioinformatics and modelling"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modelling, docking, p53, MDM2]
image:
  feature: pages/banner_education-thin.jpg
---

## About this course
The Structural Bioinformatics & Modelling course, created and maintained by the [Computational Structural Biology group](http://bonvinlab.org) of [Utrecht University](http://www.uu.nl), is aimed at those interested in learning homology modelling, molecular simulation, and docking of biological molecules. The course material requires a solid understanding of molecular biology, namely of protein sequence and structure, as well as familiarity with basic chemistry concepts. Experience with a UNIX-like command-line environment is not required but helps tying the commands to the modelling concepts and the biology.

The course is divided into three modules, each covering a particular modelling method. While the goal is to combine the three methods to answer a biological problem, each module can be followed independently. The two first modules, molecular dynamics and homology modelling, require installation of specific software packages: [GROMACS](http://www.gromacs.org), [MODELLER](https://salilab.org/modeller), and [HMMER](http://hmmer.janelia.org). Further, the homology modelling part relies heavily on MODELLER, which is free for academical use but nonetheless requires registration. The third module, data-driven docking, uses the [HADDOCK web server](http://haddocking.org), which, like MODELLER, requires registration but is free for academical users. The course material is available for free on [GitHub](http://github.com/haddocking/molmod) and makes use of virtualization software ([Virtualbox](http://virtualbox.org)).

Each module has its separate set of web pages, but they all share the same conventions. Throughout the material, colored text will be used to refer to questions or instructions, Linux and/or Pymol commands, and attention prompts (to avoid distractions!). Students following these tutorials should try their best and answer these questions, _instead of_ blindly copy-pasting commands!

<a class="prompt prompt-attention">This is an attention prompt: pay special attention to this!</a>
<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it properly!</a>
<a class="prompt prompt-pymol">This is a Pymol prompt: commands are for Pymol only!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

## Layout & Biological Significance
The E3 ubiquitin-protein ligase MDM2 regulates p53, also known as the _cell's guardian angel_, via two main mechanisms: ubiquitination-dependent proteasomal degradation and direct inhibition through binding to a region of the trans-activation domain of p53. Not surprisingly, many cancer types take advantage of this interplay and overexpress MDM2, making the p53/MDM2 interaction a prime target for drug development for cancer therapeutics. While many researchers focus on the human p53/MDM2 interaction, we believe mice (Mus musculus) also deserve their share of cutting-edge research, if only for their long-standing contribution to human disease! Therefore, the aim of this course is to probe the binding of a peptide sequence of the mouse p53 tumor suppressor protein to mouse MDM2. Since neither partner has an experimentally determined crystal structure available, this scientific problem is perfectly suited for a course on computational structural biology.

To this end, the course will describe how to build structural models for the mouse MDM2 protein via homology modelling and for the p53 trans-activation peptide via molecular dynamics simulations. Afterwards, the resulting models will seed docking simulations to predict the structure of the p53/MDM2 complex. The final goal is to suggest a possible interface and produce a starting model to design and develop drugs that will help save millions of mice! Maybe, with the right amount of luck, these results will be transferable to the human p53/MDM2 complex and will also contribute to our well-being.

## Get started!
To get started, click on the icons of the modules. Since the docking simulations require structures, we suggest that for last. If time is an issue, start with the molecular dynamics simulations and, while these run, have fun modelling MDM2.

<table class="three-col-table">
  <tr>
    <td>
      <a href="/education/molmod/modelling"
         alt="Structure prediction of the mouse MDM2 protein using HMMER & MODELLER"
         title="Structure prediction of the mouse MDM2 protein using HMMER & MODELLER">
         <img src="/images/molmod/hm_protein.jpg" class="col-table">
      </a>
    </td>
    <td>
      <a href="/education/molmod/simulation"
         alt="Molecular dynamics simulation of a mouse p53 peptide fragment using GROMACS."
         title="Molecular dynamics simulation of a mouse p53 peptide fragment using GROMACS.">
         <img src="/images/molmod/md_ensemble.jpg" class="col-table">
      </a>
    </td>
    <td>
      <a href="/education/molmod/docking"
         alt="Data-driven structure prediction of the mouse MDM2/p53 complex using HADDOCK."
         title="Data-driven structure prediction of the mouse MDM2/p53 complex using HADDOCK.">
         <img src="/images/molmod/protein_cmplx.jpg" class="col-table">
      </a>
    </td>
  </tr>
</table>
