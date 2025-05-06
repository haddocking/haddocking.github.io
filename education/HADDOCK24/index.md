---
layout: page
title: "HADDOCK Tutorials for version 2.4"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modelling, docking, p53, MDM2]
image:
  feature: pages/banner_education-thin.jpg
---
In this page you can find links to tutorials on the usage of our software and webportal [HADDOCK 2.4](https://wenmr.science.uu.nl/haddock2.4/){:target="_blank"}.

* [**HADDOCK2.4 local installation tutorial**](/education/HADDOCK24/HADDOCK24-local-tutorial):
  A tutorial demonstrating the installation and use of a local installation of HADDOCK2.4. It demonstrates various docking scenarios.
  You will need for this a valid license of HADDOCK2.4.

* [**HADDOCK restraints generation**](https://www.bonvinlab.org/haddock-restraints/home.html){:target="_blank"}:
  A guide for the `haddock-restraints` tool allowing to generate various types of distance restraints for use in HADDOCK.

* [**HADDOCK2.4 basic protein-protein docking tutorial**](/education/HADDOCK24/HADDOCK24-protein-protein-basic):
  A tutorial demonstrating the use of the HADDOCK web server to model a protein-protein complex using interface information derived from NMR chemical shift perturbation data.
  This tutorial does not require any Linux expertise and only makes use of our web server and [PyMol](https://www.pymol.org){:target="_blank"} for visualisation/analysis.

* [**HADDOCK2.4 basic antibody-antigen docking tutorial**](/education/HADDOCK24/HADDOCK24-antibody-antigen-basic):
  This tutorial demonstrates the use of HADDOCK2.4 for predicting the structure of an antibody-antigen complex using information 
  about the hypervariable loops of the antibody and NMR data identifying the epitope.
  This tutorial does not require any Linux expertise and only makes use of our web servers and [PyMol](https://www.pymol.org){:target="_blank"} for visualisation/analysis.
  The complex is also modelled using AlphaFold2 and the results compared to those obtained with HADDOCK.

* [**HADDOCK2.4 basic Protein-DNA tutorial**](/education/HADDOCK24/HADDOCK24-protein-DNA-basic):
  This tutorial demonstrates the use of HADDOCK2.4 for predicting the structure of a protein-DNA complex in which two protein units bind to the DNA in a symmetrical manner (3CRO). Next to ambiguous restraints to drive the docking symmetry restraints are defined to enforce symmetrical protein binding.
    This tutorial does not require any Linux expertise and only makes use of our web servers and [PyMol](https://www.pymol.org){:target="_blank"} for visualisation/analysis.

* [**HADDOCK2.4 MS cross-links tutorial**](/education/HADDOCK24/HADDOCK24-Xlinks):
  A tutorial demonstrating the use of cross-linking data from mass spectrometry to guide the docking in HADDOCK.
  This tutorial builds on our [DisVis tutorial](/education/Others/disvis-webserver/) and illustrates various scenarios of using
  cross-linking data in HADDOCK.
  This tutorial does not require any Linux expertise and only makes use of our web server and [PyMol](https://www.pymol.org){:target="_blank"} for visualisation/analysis.

* [**HADDOCK2.4 CA-CA restraints guided docking tutorial**](/education/HADDOCK24/HADDOCK24-CACA-guided):
  A tutorial demonstrating a template-based approach to model protein-protein complexes. It combines the PS-HomPPI web server to find suitable templates and generate CA-CA distance restraints and HADDOCK for the CA-CA guided modelling.
  This tutorial does not require any Linux expertise and only makes use of the PS-HomPPI and HADDOCK web servers and [PyMol](https://www.pymol.org){:target="_blank"} for visualisation/analysis.

* [**HADDOCK2.4 antibody-antigen docking tutorial**](/education/HADDOCK24/HADDOCK24-antibody-antigen):
  This tutorial demonstrates the use of HADDOCK2.4 for predicting the structure of an antibody-antigen complex using information 
  about the hypervariable loops of the antibody and either the entire surface of the antigen or a loose definition of the epitope.
  This tutorial does not require any Linux expertise and only makes use of our web servers and [PyMol](https://www.pymol.org){:target="_blank"} for visualisation/analysis.

* [**HADDOCK2.4 ab-initio, multi-body symmetrical docking tutorial**](/education/HADDOCK24/HADDOCK24-CASP-CAPRI-T70):
  A tutorial demonstrating multi-body docking with HADDOCK using its ab-initio mode with symmetry restraints.
  It is based on a former CASP-CAPRI target (T70).

* [**HADDOCK2.4 shape-restrained protein-small molecule tutorial**](/education/HADDOCK24/shape-small-molecule):
  This tutorial demonstrate the modelling of protein-ligand complexes making use the shape-based modelling capabilities of HADDOCK.
  It is an advanced tutorial requiring a Linux shell, which, next to using the HADDOCK2.4 webserver, also uses open-source chemoinformatics
  toolkits such as [RDKit](https://www.rdkit.org/){:target="_blank"}.
  
* [**HADDOCK2.4 ligand binding site tutorial**](/education/HADDOCK24/HADDOCK24-binding-sites):
  A tutorial demonstrating the use of HADDOCK in ab-initio mode to screen for potential ligand binding sites.
  The information from the ab-initio run is then used to setup a binding pocket-targeted protein-ligand docking run.
  We use as example the multidrug exporter AcrB.

* [**DISVIS/HADDOCK2.4 oligomer puzzle**](/education/HADDOCK24/XL-MS-oligomer):
  In this tutorial you will have to solve an oligomer puzzle, namely predicting the correct oligomeric state
  of a symmetrical homomer complex based on a few (artificial) cross-links.
  The tutorial does not require any Linux expertise and only makes use of the DISVIS and HADDOCK web servers and [PyMol](https://www.pymol.org){:target="_blank"} for visualisation/analysis.
  It now also includes a part describing the modelling of these homomeric complexes using AlphaFold2.

* [**LightDock+HADDOCK membrane proteins tutorial**](/education/HADDOCK24/LightDock-membrane-proteins):
  This tutorial demonstrates the use of LightDock for predicting the structure of membrane receptor–soluble protein complex using the topological information 
  provided by the membrane to guide the modelling process. The resulting LightDock models are then refined using HADDOCK.
