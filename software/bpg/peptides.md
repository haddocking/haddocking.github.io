---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
title: "Peptide docking"
image:
  feature: pages/banner_software.jpg
---
[_Back to main best practice page_](/software/bpg)
<p align="right">
  <img src="/software/bpg/bound_peptide.png" />
</p>

<p style='text-align: right; font-family: "PT Sans"; font-weight: 600;'> <font  size="6" color="RED" >Best practice guide</font></p>

HADDOCK supports docking of peptides as well. Since the secondary structure of short peptides is not always well defined, is is safer to dock an ensemble of multiple conformations. Different ways of generating of these conformations are described [here](/software/bpg/structures/#modelling-of-peptides-and-mutations-in-proteins). More documentation about peptide docking with HADDOCK is in following sections:

* table of contents
{:toc}

<HR>

## [Tutorials](/education/)

* [**HADDOCKing of the p53 N-terminal peptide to MDM2**](/education/molmod/docking/):
  This tutorial introduces protein-peptide docking using the HADDOCK web server. It also introduces the CPORT web server for interface prediction, based on evolutionary conservation and other biophysical properties.  


<HR>

## [Publications](/publications/)

* C. Geng, S. Narasimhan, J. P.G.L.M. Rodrigues and **A.M.J.J. Bonvin**.
[Information-driven, ensemble flexible peptide docking using HADDOCK](https://doi.org/10.1007/978-1-4939-6798-8_8).
_Methods in Molecular Biology: Modeling Peptide-Protein Interactions._ Eds Ora Schueler-Furman and Nir London. Humana Press Inc. *1561*, 109-138 (2017).


* A.D. Spiliotopoulos, P.L. Kastritis, A.S.J. Melquiond, **A.M.J.J. Bonvin**, G. Musco, W. Rocchia and A. Spitaleri.
[dMM-PBSA: a new HADDOCK scoring function for protein-peptide docking](https://journal.frontiersin.org/article/10.3389/fmolb.2016.00046/full).
_Frontiers in Molecular Biosciences_, *3*:46 doi:10.3389/fmolb.2016.00046 (2016).


* E. Deplazes, J. Davies, **A.M.J.J. Bonvin**, G.F. King and A.E. Mark.
[On the Combination of Ambiguous and Unambiguous Data in the Restraint-driven Docking of Flexible Peptides with HADDOCK: The Binding of the Spider Toxin PcTx1 to the Acid Sensing Ion channel (ASIC)1a](https://doi.org/doi:10.1021/acs.jcim.5b00529).
_J. Chem. Inf. and Model._ *56*, 127-138 (2016).

* J.P.G.L.M. Rodrigues, A.S.J. Melquiond and  **A.M.J.J. Bonvin**.
[Molecular Dynamics Characterization of the Conformational Landscape of Small Peptides: A series of hands-on collaborative practical sessions for undergraduate students](https://doi.org/doi:10.1002/bmb.20941).
_Biochemistry and Molecular Biology Education_, *44*, 160-167 (2016).


* M. Trellet, A.S.J. Melquiond and **A.M.J.J. Bonvin**.
[Information-driven modelling of protein-peptide complexes.](https://link.springer.com/protocol/10.1007/978-1-4939-2285-7_10)
_Methods in Molecular Biology._ Ed. Peng Zhou. Humana Press Inc. 221-239 (2015)

* M. Trellet, A.S.J. Melquiond and **A.M.J.J. Bonvin**.
[A Unified Conformational Selection and Induced Fit Approach to Protein-Peptide Docking](https://dx.plos.org/10.1371/journal.pone.0058769)
_PLoS ONE_, *8(3)* e58769 (2013). --> [**ERRATUM**](https://milou.science.uu.nl/Files/ERRATUM_unified_conformational_selection.pdf)



<HR>

## [Optimal settings for docking of peptides](https://wenmr.science.uu.nl/haddock2.4/settings#peptides)

<style>
table, th, td {
    padding: 5px;

}
</style>


|<font size="4" color="#203A98">Parameter</font>|<font size="4" color="#203A98">run.cns name</font>| <font size="4" color="#203A98">default value</font>|<font size="4" color="#203A98">optimal value</font> |
|-|:-:|:-:|:-:| 
|**Clustering method** | <code>clust_meth</code>| FCC | **RMSD** |   
|**Cutoff for clustering** | <code> clust_cutoff </code>| 0.6 | **5** |  
|**Number of MD steps for rigid body high temperature TAD**| <code>initiosteps</code> | 500| **2000**|
|**Number of MD steps during first rigid body cooling stage**| <code>cool1_steps</code> | 500| **2000**|
|**Number of MD steps during second cooling stage with flexible side-chains at interface**|<code>cool2_steps</code> | 500 |**4000**|
|**Number of MD steps during third cooling stage with fully flexible interface**| <code>cool3_steps</code> |500 | **4000**|

More about optimal settings for different docking scenarios can be found [here](https://wenmr.science.uu.nl/haddock2.4/settings#optimal).

<HR>

## [FAQ](/software/haddock2.4/faq/)

Any more questions about peptide docking with HADDOCK? Have a look at our **[HADDOCK bioexcel forum](https://ask.bioexcel.eu/search?q=peptide%20%23haddock)**  hosted by [<img width="70" src="/images/Bioexcel_logo.png">](https://bioexcel.eu). There is a very high chance that your problem has already been addressed. 
