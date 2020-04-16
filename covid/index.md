---
layout: page
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
virus replication process by screening ~2000 compounds against this particular
protein. We used for that [HADDOCK2.4](/software), following a shape-based strategy adapted from
our successful participation to the [D3R Grand Challanges](https://drugdesigndata.org)
and described in the following paper:

* P.I. Koukos, L.C. Xue and  A.M.J.J. Bonvin. [Protein-ligand pose and affinity prediction. Lessons from D3R Grand Challenge 3](https://doi.org/10.1007/s10822-018-0148-4).  _J. Comp. Aid. Mol. Des._ *33*, 83-91 (2019).

More details of the protocol will be provided at a later stage.

The results of our effort can be seen in the tables and graphs below.
The top part presents the results based on top cluster rankings, while the bottom part is based on single structure rankings.
The scores (in arbitrary units) correspond to the HADDOCK score calculated as:

    HADDOCKscore =  1.0 Evdw + 0.1 Eelec + 1.0 Edesol
    
where:
 
* _Evdw_ is the van der Waals intermolecular energy
* _Eelec_ is the electrostatic intermolecular energy
* _Edesol_ is an empirical desolvation energy term.


The plots show one data point per compound. In total there are 1966 compounds, grouped into one of four categories 'Protease Inhibitors', 'Antivirals', 'Antiinfectives' and 'Other'. The first is made up compounds that are known to inhibit proteases, the second antiviral medications, the third general antiinfectives and the last everything else. The 'NA' group corresponds to compounds that have no specific associations - these tend to be things like dietary supplements, aminoacid residues, etc... These are not shown in the plots but are listed in the tables. 


The plots are zoomable and clickable and groups can be hidden by clicking on them in the legend.
Hovering over points in the plot will reveal the name of the compounds.


The tables are sorted based on the HADDOCK score. They are also dynamic, sortable and searchable.


(If the tables and/or plots are not visible you can access them directly by
following [this link](http://131.211.55.120:8080)).

<iframe seamless frameborder="0" width="1200" height="2200" src="http://131.211.55.120:8080"></iframe>
