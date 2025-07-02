---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

This page provide you links to software, web services and datasets of the computational structural biology group.

* table of contents
{:toc}

<HR>
### WEB PORTAL
  All software offered as web service can be access from our web portal at:
   
   * [**wenmr.science.uu.nl**](https://wenmr.science.uu.nl){:target="_blank"}

<HR>
### HADDOCK
  Software package for integrative modelling of biomolecular complexes
  
  * [**HADDOCK best practice guide**](/software/bpg) - A must read when starting to use our software!
  
  * [**HADDOCK2.5 software**](/software/haddock2.5/) - Official 2.5 production version

  * [**HADDOCK2.4 web server**](https://wenmr.science.uu.nl/haddock2.4/){:target="_blank"} - production version (running the 2.5 version of HADDOCK in background)
  
  * [**HADDOCK3 software**](/software/haddock3) - A [BioExcel](https://www.bioexcel.eu){:target="_blank"} redesign of HADDOCK in a modular code. Still in beta release.

  * [**HADDOCK Restraints Generator**](https://wenmr.science.uu.nl/new/haddock-restraints){:target="_blank"} - A graphical user interface of the [`haddock-restraints`](https://github.com/haddocking/haddock-restraints){:target="_blank"} utility to generate restraints to be used in HADDOCK.

<HR>
### [HADDOCKING GitHub repository](https://github.com/haddocking)
  The GitHub repository for HADDOCK and its associated tools

  * [**Arctic-3D**](https://github.com/haddocking/arctic3d){:target="_blank"}:
    ARCTIC-3D is a software for data-mining and clustering of protein interface information. 
    It allows you to retrieve all the existing interface information for your desired protein from 
    the [PDBE graph database](https://www.ebi.ac.uk/pdbe/pdbe-kb/){:target="_blank"}, grouping similar interfaces in interacting surfaces.<br>
    Also available as **[web service](https://wenmr.science.uu.nl/arctic3d){:target="_blank"}**

  * [**Binding_affinity: PRODIGY**](https://github.com/haddocking/binding_affinity){:target="_blank"}:
    A collection of Python scripts to predict the binding affinity in protein-protein complexes.<br>
    Also available as **[web service](https://wenmr.science.uu.nl/prodigy){:target="_blank"}**

  * [**DisVis**](https://github.com/haddocking/disvis){:target="_blank"}:
    A Python package and command-line tool to quantify and visualize the accessible interaction space of distance-restrained biomolecular complexes.<br>
    Also available as **[web service](https://wenmr.science.uu.nl/disvis){:target="_blank"}**

  * [**Fraction of common contact clustering**](https://github.com/haddocking/fcc){:target="_blank"}:
    Clustering of biomolecular complexes based on the fraction of common contacts

  * [**HADDOCK-tools**](https://github.com/haddocking/haddock-tools){:target="_blank"}:
    A collection of useful scripts related to HADDOCK

  * [**PDB-tools**](https://github.com/haddocking/pdb-tools){:target="_blank"}:
    A collection of Python scripts for the manipulation (renumbering, changing chain and segIDs...) of PDB files.
    For documentation refer to [https://www.bonvinlab.org/pdb-tools/](https://www.bonvinlab.org/pdb-tools/){:target="_blank"}.<br>
    Also available as **[web service](https://wenmr.science.uu.nl/pdbtools){:target="_blank"}**

  * [**PowerFit**](https://github.com/haddocking/powerfit){:target="_blank"}:
    PowerFit is a Python package and simple command-line program to automatically fit high-resolution atomic structures in cryo-EM densities.<br>
    Also available as **[web service](https://alcazar.science.uu.nl/services/POWERFIT){:target="_blank"}**

  * [**Samplex**](https://github.com/haddocking/samplex){:target="_blank"}:
    Samplex is an automatic and unbiased method to distinguish perturbed and unperturbed regions in a protein existing 
    in two distinct states (folded/partially unfolded, bound/unbound). Samplex takes as input a set of data and the corresponding 
    3D structure and returns the confidence for each residue to be in a perturbed or unperturbed state.

  * [**WHISCY**](https://github.com/haddocking/whiscy){:target="_blank"}:
    WHISCY is a program to predict protein-protein interfaces. It is primarily based on conservation, 
    but it also takes into account structural information.<br>
    Also available as **[web service](https://wenmr.science.uu.nl/whiscy){:target="_blank"}**

<HR>
### 3D-DART DNA modelling
  3D-DART provides a convenient means of generating custom structural models of DNA. Our server is no longer in operation because of security issues, but you can run it yourself from a docker container. Visit for this our GitHub repo below.

  * [**3D-DART**](https://github.com/haddocking/3D-DART-server/){:target="_blank"}

<HR>
### Deep learning protein interactions

  * [**DeepRank**](https://github.com/DeepRank/deeprank){:target="_blank"}
  DeepRank is a general, configurable deep learning framework for data mining protein-protein interactions (PPIs) using 3D convolutional neural networks (CNNs).
  
  * [**DeepRank-GNN**](https://github.com/DeepRank/Deeprank-GNN){:target="_blank"}
  DeepRank-GNN is a general, configurable deep learning framework for data mining protein-protein interactions (PPIs) using graph convolutional neural networks (CNNs).
  
  * [**DeepRank-GNN-esm**](https://github.com/haddocking/DeepRank-GNN-esm){:target="_blank"}
  DeepRank-GNN-esm is a general, configurable deep learning framework for data mining protein-protein interactions (PPIs) using graph convolutional neural networks (CNNs) and including language model features.

<HR>
### Benchmarks and datasets

* Docking benchmark of membrane protein complexes ([GitHub](https://github.com/haddocking/MemCplxDB){:target="_blank"}) and associated decoy dataset [ https://doi.org/10.15785/SBGRID/618]( https://doi.org/10.15785/SBGRID/618){:target="_blank"}

* Cleaned Docking Benchmark 5 dataset, HADDOCK-ready, with unbound and bound structures matched: [https://github.com/haddocking/BM5-clean](https://github.com/haddocking/BM5-clean){:target="_blank"}

* HADDOCK docking decoys for the new entries (55) of the protein-protein Docking Benchmark5: [https://data.sbgrid.org/dataset/131/](https://data.sbgrid.org/dataset/131/){:target="_blank"}

* Docking models for Docking Benchmark 4, 5 and CAPRI score_set: [https://doi.org/10.15785/SBGRID/684](https://doi.org/10.15785/SBGRID/684){:target="_blank"}

* HADDOCK refined models for the biological/crystallographic interfaces collected in the DC and MANY datasets: [https://doi.org/10.15785/SBGRID/566](https://doi.org/10.15785/SBGRID/566){:target="_blank"}

* HADDOCK models of mutant protein complexes: [https://doi.org/10.15785/SBGRID/651](https://doi.org/10.15785/SBGRID/651){:target="_blank"}

* [Protein-DNA docking benchmark](https://github.com/haddocking/Prot-DNABenchmark){:target="_blank"}

* [Protein-small molecule benchmark](https://github.com/haddocking/shape-restrained-haddocking){:target="_blank"} containing all data related to our shape-restrained protein-ligand docking protocol (based on the DUDe small molecule benchmark. See the related tutorial [here](https://www.bonvinlab.org/education/HADDOCK24/shape-small-molecule/){:target="_blank"}

* [Protein-cyclic peptide docking benchmark](https://github.com/haddocking/cyclic-peptides){:target="_blank"} and associated models dataset [https://data.sbgrid.org/dataset/912](https://data.sbgrid.org/dataset/912){:target="_blank"}.

* All-atom and Coarse-grained HADDOCK docking models for Protein-DNA complexes: [https://zenodo.org/record/3941636](https://zenodo.org/record/3941636){:target="_blank"}

* [Dataset of modelled protein-cyclic peptide complexes](https://data.sbgrid.org/dataset/912/){:target="_blank"} obtained with HADDOCK corresponding to the optimal protocol described in  [Charitou et al. JCTC 2022](https://doi.org/10.1021/acs.jctc.2c00075){:target="_blank"}
