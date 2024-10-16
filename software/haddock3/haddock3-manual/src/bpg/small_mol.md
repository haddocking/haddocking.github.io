## Small-molecules / Ligands

<p align="right">
  <img src="/software/bpg/bound_smallmol.png" />
</p>
<p style='text-align: right; font-family: "PT Sans"; font-weight: 600;'> <font  size="6" color="RED" >Best practice guide</font></p>


It's possible to dock small ligands using HADDOCK but for that topology and parameter files for the ligand should be provided in CNS format. Several sources exist to find such files:

*   the **PRODGR** server maintained by Daan van Aalten at Dundee University: [https://prodrg2.dyndns.org](https://prodrg2.dyndns.org)  
    This server allows you to draw your molecule or paste coordinates and will return topologies and parameter files in various format, including CNS. You should turn on the electrostatic to obtain partial charges.

*   the **Automated Topology Builder (ATB)** and Repository developed in Prof. Alan Mark's group at the University of Queensland in Brisbane: [https://compbio.biosci.uq.edu.au/atb](https://compbio.biosci.uq.edu.au/atb)  
   

More detailed description is written in the [frequently asked questions page](/software/haddock2.4/faq/#small-ligand-docking-with-haddock). To get increase the chance of getting the right ligand conformation, one can perform ensemble docking. In this scenario multiple conformations can be generated as described [here](/software/bpg/structures/#modeling-of-small-molecules).

Following sections summarize all documentation about small molecule docking with HADDOCK.


<hr>

### [Tutorials](/education/)

* [**HADDOCK2.4 ligand binding site tutorial**](/education/HADDOCK24/HADDOCK24-binding-sites):
  A tutorial demonstrating the use of HADDOCK in ab-initio mode to screen for potential ligand binding sites.
  The information from the ab-initio run is then used to setup a binding pocket-targeted protein-ligand docking run.
  We use as example the multidrug exporter AcrB. 

* [**Metadynamics**](/education/biomolecular-simulations-2020/Metadynamics_tutorial):
  This tutorial highlights the benefits of enhanced sampling using metadynamics to improve the predictive power of molecular docking for protein-small molecule targets, in the case of binding sites undergoing conformational changes. For this, we will first generate an ensemble of conformers for the target protein using [GROMACS](http://www.gromacs.org/) and [PLUMED](http://www.plumed.org/), before proceeding with the docking using [HADDOCK](http://www.bonvinlab.org/software/haddock2.4/).

* [**HADDOCK covalent binding**](/education/biomolecular-simulations-2018/HADDOCK_tutorial):
  This tutorial demonstrates how to use HADDOCK for the prediction of the three dimensional structure of a covalently bound ligand onto a receptor.


<hr>

### [Publications](/publications/)


* A. Basciu, P.I. Koukos, G. Malloci, **A.M.J.J. Bonvin** and A.V. Vargiu. [Coupling enhanced sampling of the apo‐receptor with template‐based ligand conformers selection: performance in pose prediction in the D3R Grand Challenge 4](https://doi.org/10.1007/s10822-019-00244-6). _J. Comp. Aid. Mol. Des._ *34*, 149-162 (2020). A preprint can be downloaded from [here](https://arxiv.org/abs/2005.04142).  

* A. Basciu, P.I. Koukos, G. Malloci, **A.M.J.J. Bonvin** and A.V. Vargiu. [Coupling enhanced sampling of the apo‐receptor with template‐based ligand conformers selection: performance in pose prediction in the D3R Grand Challenge 4](https://doi.org/10.1007/s10822-019-00244-6). _J. Comp. Aid. Mol. Des._ *34*, 149-162 (2020). A preprint can be downloaded from [here](https://arxiv.org/abs/2005.04142).  

* P.I. Koukos, L.C. Xue and **A.M.J.J. Bonvin**. [Protein-ligand pose and affinity prediction. Lessons from D3R Grand Challenge 3](https://doi.org/10.1007/s10822-018-0148-4).  _J. Comp. Aid. Mol. Des._ *33*, 83-91 (2019).
* A. Vangone, J. Schaarschmidt, P. Koukos, C. Geng, N. Citro, M.E. Trellet, L.C. Xue and **A.M.J.J. Bonvin**. [Large-scale prediction of binding affinity in protein-small ligand complexes: the PRODIGY-LIG web server](https://doi.org/10.1093/bioinformatics/bty816). _Bioinformatics_, *35*, 1585–1587 (2019).  

* Z. Kurkcuoglu, P.I. Koukos, N. Citro, M.E. Trellet, J.P.G.L.M. Rodrigues, I.S. Moreira, J. Roel-Touris, A.S.J. Melquiond, C. Geng, J. Schaarschmidt, L.C. Xue, A. Vangone and **A.M.J.J. Bonvin**. [Performance of HADDOCK and a simple contact-based protein-ligand binding affinity predictor in the D3R Grand Challenge 2](https://doi.org/10.1007/s10822-017-0049-y). _J. Comp. Aid. Mol. Des._ *32*, 175-185 (2018).

<hr>

### [Optimal settings for docking of small molecules](https://wenmr.science.uu.nl/haddock2.4/settings#ligands)

<style>
table, th, td {
    padding: 5px;}
</style>


|<font size="4" color="#203A98">Parameter</font>|<font size="4" color="#203A98">run.cns name</font>| <font size="4" color="#203A98">default value</font>|<font size="4" color="#203A98">optimal value</font> |
|-|:-:|:-:|:-:| 
|**Clustering method** | <code> clust_meth</code>| FCC | **RMSD** |   
|**Cutoff for clustering** | <code> clust_cutoff </code>| 0.6 | **2.5** |  
|**Dieletric constant for it0** | <code> dielec_0</code> | rdie | **cdie** |  
|**Dieletric constant for it1** | <code> dielec_1</code> | rdie | **cdie**  |
|**Epsilon constant for the electrostatic energy term in it1** | <code> epsilon_1</code> |  1.0 | **10.0** |  
|**Number of MD steps for rigid body high temperature TAD** | <code> initiosteps</code> | 500 | **0**  | 
|**Number of MD steps during first rigid body cooling stage** | <code> cool1_steps</code>| 500 | **0**  | 
|**Initial temperature for second TAD cooling step with flexible side-chain at the interface**  | <code> tadinit2_t </code>| 1000 | **500** |
|**Initial temperature for third TAD cooling step with fully flexible interface** | <code> tadinit3_t </code> | 1000 | **300** |
|**Evdw 1** | <code> w_vdw_0 </code>| 0.01 | **1.0**  | 
|**Eelec 3**| <code> w_elec_2 </code> | 0.2 | **0.1**  | 


More about optimal settings for different docking scenarios can be found [here](https://wenmr.science.uu.nl/haddock2.4/settings#optimal).

<hr>

### [FAQ](/software/haddock2.4/faq/)

A special section about docking of small molecules with HADDOCK is dedicated in the [frequently asked questions page](/software/haddock2.4/faq/#small-ligand-docking-with-haddock).

Any more questions about small molecule docking with HADDOCK? Have a look at our **[HADDOCK bioexcel forum](https://ask.bioexcel.eu/search?q=ligand%20%23haddock)**  hosted by [<img width="70" src="/images/Bioexcel_logo.png">](https://bioexcel.eu). There is a very high chance that your problem has already been addressed. 
