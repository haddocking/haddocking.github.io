---
layout: full-page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 
comments: false
image:
  feature: pages/banner_research-mini.jpg
---

## COVID-19 related research projects from the CSB group

The novel coronavirus (SARS-CoV-2) that has emerged from Wuhan, China in
December 2019 has spread to almost all countries in the World causing a
dramatic number of deaths. The current absence of  antiviral treatment
against the SARS-CoV-2 urges the scientific community to accelerate the
drug discovery research process.

One way to identify potential treatments and to be able to administer it
swiftly is to focus on drug repurposing studies, i.e. to investigate the
SARS-CoV-2 antiviral potential of drugs that have already been approved
for human use.

### Screening of approved drugs against the SARS-CoV-2 protease

Proteins that are crucial for the survival and replication of the virus
are the most attractive targets for such studies. Here we have focused on
the SARS-CoV-2 main protease (3CLpro) that plays an essential role in the
virus replication process by screening ~2000 approved drugs (and 6 experimental ones - these
 can be identified by searching the tables using the term 'Investigational') against this particular
protein. We used for that [HADDOCK2.4](/software){:target="_blank"}, following a pharmacophore-based and a shape-based strategy adapted from
our successful participation to the [D3R Grand Challanges](https://drugdesigndata.org{:target="_blank"})
and described in the following paper:

* P.I. Koukos, L.C. Xue and  A.M.J.J. Bonvin. [Protein-ligand pose and affinity prediction. Lessons from D3R Grand Challenge 3](https://doi.org/10.1007/s10822-018-0148-4){:target="_blank"}.  _J. Comp. Aid. Mol. Des._ *33*, 83-91 (2019).

More details of the protocol are provided below.

The results of our effort can be seen in the tables and graphs below.
The top part presents the results based on top cluster rankings, while the bottom part is based on single structure rankings.
The scores (in arbitrary units) correspond to the HADDOCK score calculated as:

    HADDOCKscore =  1.0 Evdw + 0.1 Eelec + 1.0 Edesol
    
where:
 
* _Evdw_ is the van der Waals intermolecular energy
* _Eelec_ is the electrostatic intermolecular energy
* _Edesol_ is an empirical desolvation energy term.


The plots show one data point per compound. In total there are 1974 compounds, grouped into one of four categories 'Protease Inhibitors', 'Antivirals', 'Antiinfectives' and 'Other'. The first is made up compounds that are known to inhibit proteases, the second antiviral medications, the third general antiinfectives and the last everything else. The 'NA' group corresponds to compounds that have no specific associations - these tend to be things like dietary supplements, aminoacid residues, etc... These are not shown in the plots but are listed in the tables. 

The compounds were obtained from [Drugbank](https://www.drugbank.ca){:target="_blank"} and pre-processed using the [OpenEye](https://www.eyesopen.com/omega){:target="_blank"} Omega software (Hawkins _et al_. J. Chem. Inf. Model. *50* 572-584 (2010)). For the protease we used PDB entry [6Y2F](https://www.rcsb.org/structure/6y2f) ([Zhang et al. _Science_, 2020](https://doi.org/10.1126/science.abb3405)).

#### Relevance

In total, 7 molecules of the HADDOCK Top 100 drugs (one ranked #2) are under clinical trials in Europe as reported in the European Union Drug Regulating Authorities Clinical Trials Database (EudraCT) [https://www.clinicaltrialsregister.eu/ctr-search/search?query=covid-19](https://www.clinicaltrialsregister.eu/ctr-search/search?query=covid-19){:target="_blank"}:

* 1 kinase targeting antitumor drug: Imatinib
* 2 antiviral drugs: Lopinavir, Remdesivir
* 3 antiinfective drugs: Azithromycin, ceftriaxone, erythromycin
* 1 angiotensin II receptor antagonist: Telmisartan


#### Acknowledgments
Our group efforts have been led in major part by Dr. Panagiotis Koukos and Dr. Manon Réau. Dr. Ed Moret from the Department of Pharmaceutical Sciences at Utrecht University has provided valuable expertise on the compounds and their relevance.

<hr>

The plots are zoomable and clickable and groups can be hidden by clicking on them in the legend.
Hovering over points in the plot will reveal the name of the compounds.


The tables are sorted based on the HADDOCK score. They are also dynamic, sortable and searchable.



<iframe seamless frameborder="0" width="1200" height="2400" src="./covid_mpro_tanimoto.html"></iframe>

<hr>

#### Protocol
##### Virtual library
We considered approved drugs from the DrugBank dataset with molecular weight < 750 g/mol and > 5 heavy atoms. Some of these drugs act as prodrugs, i.e. they are inactive compounds that are metabolized into their active form after administration. When the data was available we collected the active form of the documented prodrugs, referred here as « Active Metabolites », from the PubChem database. We ended up with 1977 drugs and 50 active metabolites and we generated up to 500 conformers per compound using OpenEye.

##### Template compounds 
The rational behind HADDOCK docking is to make use of experimental information to guide the docking. Herein, we took advantage of the large amount of high quality *holo* structures of the SARS-CoV-2 3CLpro and related proteins (> 90% identity) published in the [Protein Data Bank](https://www.rcsb.org/). Among those crystallographic data, 66 molecules are non-covalent and covalent active-site fragments from the large XChem crystallographic fragment screen against 3CLpro performed by [Diamond](https://www.diamond.ac.uk/covid-19/for-scientists/Main-protease-structure-and-XChem.html). In total, we collected 92 molecules targeting the 3CLpro(-related) binding site. 

##### Shape based docking - HADDOCK 
We identified one crystallographic template to be used for the docking of every target compound in the virtual library. For the selection, we calculated the Tanimoto coefficient computed over the Maximum Common Substructure (MCS) between target and template compounds and selected the template with the highest Tanimoto coefficient. After superimposing all templates we transformed the heavy atoms of their compounds into shape beads and defined restraints between the beads and heavy atoms of the target compound to guide it in the binding pocket.

##### Pharmacophore based docking - HADDOCK 
Similarly, each coumpound in the virtual library was associated to the most similar crystallographic template in terms of 2D pharmacophore description. To do so, we calculated the pairwise Tanimoto coefficient between the 2D pharmacophore fingerprints of the compounds from the virtual library and tha template compounds. The binding information of the template compound was then used to build a shape in the 3CLpro binding site consisting of one bead per atom, each bead being associated to a pharmacophore feature (or no feature) as computed with RDKIT. Docking restraints were imposed to orient the pharmacophore features of the drugs and active metabolites towards the corresponding feature of their associated shape.
