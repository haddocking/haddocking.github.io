---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
title: "How to analyse docking results from HADDOCK or refine models?"
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---
[_Back to main best practice page_](/software/bpg)
<p align="right">
  <img src="/software/bpg/analysis_1.png" />
</p>
<p style='text-align: right; font-family: "PT Sans"; font-weight: 600;'> <font  size="6" color="RED" >Best practice guide</font></p>


## Protein-protein docking


There are various way how can your docking run be compared to a reference structure:
 
* **local HADDOCK scripts**  
 	If you run HADDOCK locally, you can use the scripts that were installed in the *tools* directory during HADDOCK installation. Such analysis is described in the [local HADDOCK tutorial](/education/HADDOCK24/HADDOCK24-local-tutorial/) and in the [HADDOCK2.4 manual](/software/haddock2.4/analysis/#manual-post-docking-analysis)
  	These scripts can be also found here [Github](https://github.com/haddocking/haddock/tree/haddock2.4/tools).  

* ***ana_scripts***   
	 After using the HADDOCK webserver, one can analyse their results locally with our analysis scripts in the *ana_scripts* directory. This analysis is described in the HADDOCK [ab-intio tutorial](/education/HADDOCK24/HADDOCK24-CASP-CAPRI-T70/). However they need to be modified for each individual use.
 	These scripts can be also found here [Github](https://github.com/haddocking/CASP-CAPRI-T70-tutorial/tree/master/ana_scripts).  

* ***DockQ***  
	[DockQ](https://doi.org/10.1371/journal.pone.0161879) estimates protein-protein model quality in a quantitative way using all parameters as the [CAPRI classification](https://doi.org/10.1002/prot.21804) e.g. fraction of native contacts (fcc), interface root-mean-square-deviation (i-RMSD), ligand RMSD (l-RMSD)
   	DockQ can be found on Github in both [python](https://github.com/bjornwallner/DockQ) or [fortran](https://github.com/nemo8130/DockQ-fortran-code).



## Manual


Analysis of docking results are described in the [HADDOCK2.4 manual](/software/haddock2.4/analysis/) and more about parameters in the *run.cns* file is written [here](/software/haddock2.4/run/#analysis-and-clustering).


## Clustering and scoring

A short section about key analysis parameters is written [here](https://wenmr.science.uu.nl/haddock2.4/settings).



<HR>

## [Advanced model refinement](/software/haddock2.4/tips/advanced_refinement/)

The HADDOCK2.4 server provides a dedicated web interface to run a [refinement on a molecular complex](https://bianca.science.uu.nl/haddock2.4/refinement/1) (still experimental). As input, only a PDB file for each partner of the complex is needed. In case one wants to tune the default parameters, it is possible to run the refinement also locally or using the regular [submission interface](https://wenmr.science.uu.nl/haddock2.4/submit/1). Then following settings need to be adjusted: 

### Settings to run water refinement locally

<style>
table, th, td {
    padding: 5px;}
</style>

|<font size="4" color="#203A98">Parameter</font>|<font size="4" color="#203A98">run.cns name</font>| <font size="4" color="#203A98">default value</font>|<font size="4" color="#203A98">optimal value</font> |
|-|:-:|:-:|:-:| 
|**Center of mass restraints** | <code> cmrest</code>|false|**true**|  
|**Surface contact restraints** | <code>surfrest</code>|false|**true**|  
|**Number of structures for rigid body docking (it0)**|<code>structures_0</code>|1000|**same as itw structures**|
|**Number of structures for semi-flexible refinement (it1)**| <code>structures_1</code>|200| **same as itw structures**|
|**Sample 180 degrees rotated solutions during rigid body EM** |<code>rotate180_0</code>|true| **false**|
|**Refine with short molecular dynamics in explicit solvent?** |<code>solvshell</code>|false| **true**|
|**Perform cross-docking** | <code>crossdock</code>| true| **false**|
|**Multiply the number of calculated structures by all combination** | <code>ensemble_multiply<sup>*</sup></code>| false| **true**|
|**Randomize starting orientations** | <code>randorien</code>| true| **false**|
|**Perform initial rigid body minimisation** | <code>rigidmini</code>| true| **false**|
|**Allow translation in rigid body minimisation** | <code>rigidtrans</code>| true| **false**|
|**Number of MD steps for rigid body high temperature TAD**| <code>initiosteps</code> | 500| **0**|
|**Number of MD steps during first rigid body cooling stage**| <code>cool1_steps</code> | 500| **0**|
|**Number of MD steps during second cooling stage with flexible side-chains at interface**|<code>cool2_steps</code> | 500 |**0**|
|**Number of MD steps during third cooling stage with fully flexible interface**| <code>cool3_steps</code> |500 | **0**|

<sup>\*</sup> - only in *json* files, needs to be modified by hand in *run.cns*

 <HR>

Any more questions about analysis of the HADDOCK run? Have a look at our **[HADDOCK bioexcel forum](https://ask.bioexcel.eu/search?q=ana%20%23haddock)**  hosted by [<img width="70" src="/images/Bioexcel_logo.png">](https://bioexcel.eu). There is a very high chance that your problem has already been addressed. 
