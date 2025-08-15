---
layout: page
title: "HADDOCK3 tutorials"
tags: [HADDOCK, HADDOCK3, docking, antibodies, workflows]
image:
  feature: pages/banner_education-thin.jpg
---
In this page you can find links to tutorials on the usage of the new modular HADDOCK3 version. HADDOCK3 has been and is developed under
the umbrella of the [BioExcel Center of Excellence for Computational Biomolecular Research](https://www.bioexcel.eu){:target="_blank"} and in collaboration with the [Netherlands e-Science Center](https://www.esciencecenter.nl/){:target="_blank"}. 

_Note that HADDOCK3 is still in heavy development and as such the software is evolving quickly._

<hr>

# Getting started

* **Online lectures**:
  These two recordings of HADDOCK lectures explain basis of HADDOCK, ambiguous interaction restraints and introduce HADDOCK3 (*by Prof. Bonvin (June 7th, 2021) at the [BioExcel](https://www.bioexcel.eu){:target="_blank"} summerschool*):

  <ul>
  <details>
  <summary>Click here to view recorded lecture Part I (46 min.)
  </summary>
    <iframe width="560" height="315" src="https://www.youtube.com/embed/N2Sr4qtRKhs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> 
  </details>
  <br>
  </ul>
  <ul>
  <details>
  <summary>Click here to view recorded lecture Part II (43 min.)
  </summary>
     <iframe width="560" height="315" src="https://www.youtube.com/embed/qpx6bQZhWrU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
  </details>
  <br>
  </ul>

* [**Basic docking run with HADDOCK3**](/education/HADDOCK3/HADDOCK3-antibody-antigen):
  This tutorial describes a full step-by-step process from preparing the files for the docking, to the interpretation of the results. The tutorial is available as a video [**here**](https://youtu.be/0pLOPev3ni0?feature=shared){:target="_blank"}. It is a good idea to go through it to get a basic introduction to HADDOCK3. *Note that this is the basic antibody-antigen tutorial; if you've already followed it elsewhere, there's no need to repeat it.*

<hr>

# System-specific basic tutorials

* [**Antibody-antigen docking**](/education/HADDOCK3/HADDOCK3-antibody-antigen):
  This tutorial demonstrates the use of HADDOCK3 for predicting the structure of an antibody-antigen complex using information
  about the hypervariable loops of the antibody and a loose definition of the epitope determined through NMR experiments.
  As HADDOCK3 only exists as a command line version, this tutorial does require some basic Linux expertise.

* [**Nanobody-antigen docking**](/education/HADDOCK3/HADDOCK3-nanobody-antigen):
  This tutorial is similar to the antibody-antigen docking tutorial, but it uses a nanobody instead of an antibody. In the tutorial we explain how to generate an ensemble of nanobody conformations in their unbound form and then how to dock it to the antigen using HADDOCK3.

* [**Protein-Glycan modelling and docking**](/education/HADDOCK3/HADDOCK3-protein-glycan):
  This tutorial shows how to use HADDOCK3 to dock a glycan to a protein, provided that some information exists about the protein binding site.
  As HADDOCK3 only exists as a command line version, this tutorial does require some basic Linux expertise.

* [**Protein-DNA docking tutorial**](/education/HADDOCK3/HADDOCK3-protein-DNA-basic):
  This tutorial demonstrates the use of Haddock3 for predicting the structure of a protein-DNA complex in which two protein units bind 
  to the double-stranded DNA in a symmetrical manner (reference structure [3CRO](https://www.rcsb.org/structure/3CRO)).
  In addition to provided ambiguous restraints used to drive the docking, symmetry restraints are also defined to enforce symmetrical binding to the protein.
  As HADDOCK3 only exists as a command line version, this tutorial does require some basic Linux expertise.

* [**Protein-peptide docking tutorial**](/education/HADDOCK3/HADDOCK3-protein-peptide):
  This tutorial guides you through protein–peptide docking in HADDOCK3, from preparing input structures and defining restraints to running the protocol and analyzing results. The peptide is docked as a pre-generated ensemble prepared in advance.

<hr>

# Advanced tutorials

*coming soon*

<hr>

# Documentations

* [**HADDOCK3 user manual**](https://www.bonvinlab.org/haddock3-user-manual/)
  User manual for HADDOCK3, with a comprehensive description of the software and its features, including a [Best Practices](https://www.bonvinlab.org/haddock3-user-manual/bpg.html){:target="_blank"} section and descriptions of several [HADDOCK docking scenarios](https://www.bonvinlab.org/haddock3-user-manual/docking_scenarios.html){:target="_blank"}.

* [**HADDOCK restraints generation**](https://www.bonvinlab.org/haddock-restraints/home.html){:target="_blank"}:
  A guide for the `haddock-restraints` tool allowing to generate various types of distance restraints for use in HADDOCK, also available via [a graphical user interface](http://wenmr.science.uu.nl/haddock-restraints){:target="_blank"}.

* [**HADDOCK3 software documentation**](https://www.bonvinlab.org/haddock3)
  Documentation for HADDOCK3 including [installation instructions](https://www.bonvinlab.org/haddock3/INSTALL.html){:target="_blank"}.
