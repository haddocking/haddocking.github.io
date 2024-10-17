## Restraints

<p align="right">
  <img src="/software/bpg/restraints_1.png" />
</p>


<p style='text-align: right; font-family: "PT Sans"; font-weight: 600;'> <font  size="6" color="RED" >Best practice guide</font></p>

As you probably saw in the [previous step](/software/bpg/structures/) there are many ways how to obtain structures of molecules that you want to dock. The next step is to define the way you expect these molecules to interact. HADDOCK is an information-driven tool, which means that the more available information about binding you have, the more meaningful your results will be. Based on the available information we distinguish between following options:

<hr>



### What information about binding is available? 

<img src="/software/bpg/interface.png" align="right" >

#### 1.) Information about the interface is available

#### Unambiguous Interaction restraints  

 If your predictions are highly reliable and you wish to have all of them applied during docking, define them a unambiguous restraints. These can be for example template-derived pairwise distance restraints ([tutorial](/education/HADDOCK24/HADDOCK24-CACA-guided/)),  MS crosslink data ([tutorial](/education/HADDOCK24/HADDOCK24-Xlinks/))  or cryo-EM connectivity data ([tutorial](/education/HADDOCK24/RNA-Pol-III/)).



#### [<font color="RED">A</font>mbiguous <font color="RED">I</font>nteraction <font color="RED">R</font>estraints (<font color="RED">AIR</font>s)](/software/haddock2.4/airs/)

Nevertheless, as in life, in science one also needs to be somewhat critical to the data one works with. If you are not 100% sure about the interaction information and want to be cautious while incorporating it into your docking, use ambiguous interaction restraints, unique for HADDOCK. Here, for each docking trial a fraction of these restraints will be [randomly removed](/software/haddock2.4/run/#random-removal-of-airs), which ensures a wider sampling satisfying always a different subset of predefined restraints. Thus, if some of the restraints are artificial, these can be filtered out if the complex satisfying them is unfavorable. 

For AIRs, it is important to define the residues at the interface for each molecule based on experimental data that provides information on the interaction interface.  

In the definition of those residues, one distinguishes between ***<font color="RED">"active"</font>*** and ***<font color="GREEN">"passive"</font>*** residues.  

 *   The ***<font color="RED">"active"</font>*** residues are of central importance for the interaction between the two molecules **AND** are solvent accessible. 
  Either main chain or side chain relative accessibility should be typically > 40%, sometimes a lower cutoff might be used as well, for example the HADDOCK server uses by default 15%. Throughout the simulation, these active residues are restrained to be part of the interface, if possible, otherwise incurring in a scoring penalty.    

 *   The ***<font color="GREEN">"passive"</font>*** residues are all solvent accessible surface neighbors of active residues (<6.5Å). They contribute for the interaction, but are deemed of less importance. If such a residue does not belong in the interface there is no scoring penalty.


In general, an AIR is defined as an ambiguous intermolecular distance between any atom of an active residue of molecule A and any atom of both active and passive residues of molecule B (and inversely for molecule B).

Ambiguous distance restraints are described in the [**HADDOCK manual**](/software/haddock2.4/airs/) and more about parameters in the *run.cns* file is written [here](/software/haddock2.4/run/#distance-restraints).

Using ambiguous restraints for docking is described in several tutorials: [local installation tutorial](/education/HADDOCK24/HADDOCK24-local-tutorial/#defining-restraints-for-docking), [basic protein-protein tutorial](/education/HADDOCK24/HADDOCK24-protein-protein-basic/#definition-of-restraints), [small molecule docking tutorial](/education/HADDOCK24/HADDOCK24-binding-sites/) or [antibody-antigen docking tutorial](/education/HADDOCK24/HADDOCK24-antibody-antigen/#definition-of-restraints).


#### Other kinds of restraints

* [Hydrogen bonds restraints](/software/haddock2.4/run/#hydrogen-bond-restraints)

* [DNA/RNA restraints](/software/haddock2.4/run/#dnarna-restraints)

* [Dihedral angles restraints](/software/haddock2.4/run/#dihedrals-angle-restraints)


HADDOCK can utilize plenty of experimental information. Here we describe other types of restraints supported by HADDOCK:

* [Residual Dipolar Couplings](/software/haddock2.4/RDC/)  

* [Pseudo Contact Shifts](/software/haddock2.4/PCS/)  

* [Diffusion Anisotropy Restraints](/software/haddock2.4/DANI/)

* [Cryo-EM restraints](/software/haddock2.4/cryoEM/)

* [Radius of gyration restraints](/software/haddock2.4/Rg/)

<hr>

<img src="/software/bpg/all_passive.png" align="right" >

### 2.)  Information about the interface is not available


If there is no direct information about the interacting residues available, one can still browse through the available literature or employ bionformatic prediction to gain some information about the potential complex. HADDOCK offers a plethora of ways for these scenarios.   



#### Information about the quaternary structure of proteins (symmetry)

##### [Symmetry restraints](/software/haddock2.4/run/#symmetry-restraints)

HADDOCK offers the possibility to define multiple symmetry relationships within or in between molecules. This is done by using symmetry distance restraints. By defining multiple pairs of distances between the CA atoms of two chains, various symmetries can be enforced. 
Symmetry restraints are described in the manual [here](/software/haddock2.4/run/#symmetry-restraints). 

Ab-initio multi-body docking with symmetry restraints is described this [ab-initio tutorial](/education/HADDOCK24/HADDOCK24-CASP-CAPRI-T70/).

##### [Non-crystallographic symmetry restraints (NCS)](/software/haddock2.4/run/#non-crystallographic-symmetry-restraints-ncs)

The NCS option imposes non-crystallographic symmetry restraints: It enforces that two molecules, a fraction thereof or even two sub-domains within the same molecule should be identical without defining any symmetry operation between them. 
Non-crystallographic symmetry restraints are described in the manual [here](/software/haddock2.4/run/#non-crystallographic-symmetry-restraints-ncs). 

Ab-initio multi-body docking with NCS restraints is described [here](/education/HADDOCK24/HADDOCK24-CASP-CAPRI-T70/).

##### [Membrane Z-positioning restraints](/software/haddock2.4/run/#membrane-z-positioning-restraints)

These restraints do not deal with symmetry, but can be useful in guiding the docking of membrane proteins. This type of restraints is used to keep segments within or outside of a defined Z-coordinate range. They can be used for docking of membrane proteins but can be use generically as well.

They are described in the HADDOCK manual [here](/software/haddock2.4/run/#membrane-z-positioning-restraints).

#### Ab-initio docking

##### [Random interaction restraints](/haddock2.4/airs/#random-air-definition-ab-initio-mode)

HADDOCK offers to define [random AIRs](/haddock2.4/airs/#random-air-definition-ab-initio-mode)  from solvent accessible residues (>20% relative accessibility) in case there is no experimental information. The sampling will be done from the defined semi-flexible segments. This can be useful for ab-initio docking to sample the entire protein surface. To ensure a thorough sampling of the surface, the number of structures generated at the rigid-body stage (it0) should be increased (e.g. 10000), depending on the extent of the surface to be sampled. These random restraints are described [here](/software/haddock2.4/run/#random-interaction-restraints-definition). 

Random interaction restraints are used in the [binding site tutorial](/education/HADDOCK24/HADDOCK24-binding-sites/).


##### [Surface contact restraints](/haddock2.4/airs/#surface-contact-restraint)

[Surface contact restraints](/software/haddock2.4/airs/#surface-contact-restraints) can be useful in multi-body (N>2) docking to ensure that all molecules are in contact and thus promote compactness of the docking solutions. As for the random AIRs, surface contact restraints can be used in ab-initio docking; in such a case it is important to have enough sampling of the random starting orientations and this significantly increases the number of structures for rigid-body docking. They can be useful in combination with random interaction restraints definition (see above) or in refinement of molecular complexes. They are described in the manual [here](/software/haddock2.4/run/#surface-contact-restraints).

##### [Center of mass restraints](/software/haddock2.4/airs/#center-of-mass-restraints)

[Center of mass (COM) restraints](/software/haddock2.4/airs/#center-of-mass-restraints) are distance restraints that ensure close proximity of two molecules. Such restraints can be useful in multi-body (N>2) docking to ensure that all molecules are in contact and thus promote compactness of the docking solutions. Similarly to the contact surface restraints they can be useful in combination with random interaction restraints definition (see above) or in refinement of molecular complexes.

COM restraints are mentioned in multiple tutorials, for example: [Refining the interface of the cryo-EM fitted models with HADDOCK](/education/HADDOCK24/RNA-Pol-III/#refining-the-interface-of-the-cryo-em-fitted-models-with-haddock),  [HADDOCK 2.4 CASP-CAPRI T70 ab-initio docking tutorial](/education/HADDOCK24/HADDOCK24-CASP-CAPRI-T70/#definition-of-restraints), [Modelling a homo-oligomeric complex from MS cross-links](/education/HADDOCK24/XL-MS-oligomer/#definition-of-restraints).


<hr>

### [Optimal settings for docking using bioinformatics predictions](/software/haddock2.4/tips/bioinformatics-prediction-mode/)

When we are less certain about the  of the interacting residues, it is better to enhance sampling by [increasing the number of structures](/software/haddock2.4/tips/bioinformatics-prediction-mode/) generated in each phase of docking.  


<style>
table, th, td {
    padding: 5px;
}
</style>


|<font size="4" color="#203A98">Parameter</font>|<font size="4" color="#203A98">run.cns name</font>| <font size="4" color="#203A98">default value</font>|<font size="4" color="#203A98">optimal value</font> |
|-|:-:|:-:|:-:| 
|**Number of partitions for random exclusion**|<code>ncvpart</code>|2.0| **1.1428**|
|**Number of trials for rigid body minimisation**| <code>ntrials</code>|5| **1**|
|**Number of structures for rigid body docking (it0)**|<code>structures_0</code>| 1000| **10000**|
|**Number of structures for semi-flexible refinement (it1)**| <code>structures_1</code>| 200| **400**|
|**Number of structures for the final refinement (itw)**|<code>waterrefine</code>| 200 |**400**|
|**Number of structures to analyze**|<code>anastruc_1</code> | 200| **400**|

**IMPORTANT NOTE**: The non-integer value of `ncvpart` can only be used in the web server. What the server is then doing is to pre-generate `ambig.tbl_XXX` files, where `XXX` indicated the model number. Those are then placed into the `structures/it0` directory and `noecv` is set to false.
When such files are present, they will be read instead of the regular `ambig.tbl`.  The automatic partioning into sets of restraints in CNS can only handle an integer number, meaning that the largest possible random removal is 50% (`ncvpart=2`). For more than 50% random removal custom `ambig.tbl_XXX` files must be generated prior to docking.


More about optimal settings for different docking scenarios can be found [here](https://wenmr.science.uu.nl/haddock2.4/settings#bioinfo).

<hr>

## Getting restraints HADDOCK-ready

In [HADDOCK2.4 webserver](https://wenmr.science.uu.nl/haddock2.4/) active and passive residues can be entered manually or in a *tbl* file of ambiguous and unambiguous restraints. 

Such restraints file can be generated in the [GenTBL server](https://alcazar.science.uu.nl/services/GenTBL/) and can be further used when using HADDOCK locally, since it is already CNS-formatted.

**[Haddock tools](https://github.com/haddocking/haddock-tools)** a bunch of useful tool available on [Github](https://github.com/haddocking/haddock-tools) a bunch of useful tool available on github for use with local version of HADDOCK.
* *contact-chain*, *contact-segID* - programs to calculate all heavy atom interchain contacts within a given distance cutoff - useful to define active/passive residues based on a template structure
* *passive_from_active.py*, *active-passive_to_ambig.py* - these scripts will automatically calculate a list of surface residues from the PDB to filter out buried residues and create an ambiguous interaction restraints file based on the list of active and passive residues 
* *restrain_bodies.py*, *restrain_ligand.py* - scripts that will keep multiple chains or ligands keep together during the flexible parts of docking
*  *validate_tbl.py* - this script checks the correctness of your restraints (CNS format) for HADDOCK.
 
 Use of the HADDOCK tools is also described in the [local HADDOCK tutorial](/education/HADDOCK24/HADDOCK24-local-tutorial/#defining-restraints-for-docking).



More information about distance restraints:

* [HADDOCK2.4 manual - defining restraints](/software/haddock2.4/docking/#defining-restraints)



<hr>

## Dos and Don'ts

<style>
table, th, td {
    padding: 5px;
}
</style>

| <font size="10" color="RED">Don't</font> | <font size="10" color="GREEN">Do instead</font> |
|:---:|:---:|
| define the entire protein as **active** | define only key interacting residues as **active**, if they are not know, define the surface of one molecule as **passive**  |


<hr>

#  Complimentary software related to restraints for HADDOCK

In bonvinlab a number of complementary webservers have been developed to help users to reevaluate restraints. 

## [CPORT](http://alcazar.science.uu.nl/services/CPORT/) 

[CPORT](http://alcazar.science.uu.nl/services/CPORT/) is an algorithm for the prediction of protein-protein interface residues. It combines six interface prediction methods into a consensus predictor.

Tutorials using CPORT:

* [HADDOCKing of the p53 N-terminal peptide to MDM2](/education/molmod/docking/)


## [DISVIS](https://wenmr.science.uu.nl/disvis/) 

[DISVIS](https://wenmr.science.uu.nl/disvis/) visualizes and quantifies the information content of distance restraints between macromolecular complexes.

Tutorial describing DisVis: 

* [DisVis tutorial](/education/Others/disvis-webserver/)
* [HADDOCK2.4 tutorial for the use of MS crosslinks](/education/HADDOCK24/HADDOCK24-Xlinks/#setting-up-the-docking-with-the-disvis-derived-interfaces-scenario-2)
* [Integrative modelling of the RNA polymerase III apo complex](/education/HADDOCK24/RNA-Pol-III)


## [SPOTON](http://alcazar.science.uu.nl/cgi/services/SPOTON/spoton/) 

[SPOTON](http://alcazar.science.uu.nl/cgi/services/SPOTON/spoton/submit) determines Hot-Spot residues at protein-protein interfaces.

<hr>

Any more questions about restraints for HADDOCK? Have a look at the **[HADDOCK bioexcel forum](https://ask.bioexcel.eu/search?q=restraint%20%23haddock)**  hosted by [<img width="70" src="/images/Bioexcel_logo.png">](https://bioexcel.eu). There is a very high chance that your problem has already been addressed. 
