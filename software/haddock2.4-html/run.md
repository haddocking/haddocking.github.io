--- layout: page tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure] modified: comments: false image: feature: pages/banner_software.jpg ---

# <font color="RED">HADDOCK2.2</font> manual

## <font color="RED">R</font>un.cns

* * *

The **run.cns** file contains all the parameters to run the docking. You need to edit this file to define a number of project-specific parameters such as the number of structures to generate at the various stages, which restraints to use for docking and various parameters governing the docking and scoring. Many parameters have default values which you do not need to change unless you want to experiment.  

Using a web browser, go to the project setup section of the HADDOCK home-page ([http://www.bonvinlab.org/software/haddock2.2/haddock-start](/software/haddock2.2/haddock-start)) , enter the path of your **run.cns** file and click on **"edit file"**.  

The **run.cns** is divided into several sections that will be detailed in the following:

1.  [Number of molecules for docking](#nummol)
2.  [Filenames](#names)
3.  [Definition of the protonation state of histidines](#histidines)
4.  [Definition of the semi-flexible interface](#interface)
5.  [Definition of fully flexible segments](#flex)
6.  [Symmetry restraints](#sym)
7.  [Distance restraints](#disre)
8.  [Radius of gyration restraint](#rgre)
9.  [DNA/RNA restraints](#dna)
10.  [Dihedral angle restraints](#dihre)
11.  [Karplus coupling restraints](#karplus)
12.  [Residual dipolar couplings](#dipo)
13.  [Pseudo contact shifts](#pcs)
14.  [Diffusion anisotropy restraints](#dani)
15.  [Topology and parameters files](#topo)
16.  [Energy and interaction parameters](#param)
17.  [Number of structures to dock](#numstruc)
18.  [DOCKING protocol](#dock)
19.  [Solvated docking](#solvdock)
20.  [Final explicit solvent refinement](#water)
21.  [Scoring](#scoring)
22.  [Analysis and clustering](#anal)
23.  [Cleaning](#clean)
24.  [Parallels jobs](#jobs)

* * *

<a name="nummol">**1\. <u>Number of molecules for docking</u>**</a>  

here you have to specify the number of molecules for docking. HADDOCK version 2.0 and higher currently supports up to six separate molecules, thus allowing multi-body (N>=2) docking. This should be set automatically by HADDOCK from the number defined in _**[new.html](/software/haddock2.2/start_new_help)**_.  

**_Note:_**

* * *

<a name="names">**2\. <u>Filenames</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/filenames.png)  

This section consist of all the files that will be used for the docking. If the _**new.html**_ file has been set up properly, most fields will be set correctly. The only thing you might want to change is the name of the current project which is used as as rootname for all files.  

If one of the molecules is DNA (_and not RNA!_), set the DNA flag to true. This is needed since the building blocks in the DNA/RNA topology file correspond to RNA. When DNA is set to _true_, a patch will be applied to remove 2' hydroxyl groups.  

Also check that the HADDOCK directory, defining the path to the HADDOCK programs, is correct.  

**Note 1:**

_**new.html**_

**Note 2:**

In that section there is also a paramater that defines if non-polar protons should be kept or not:

<pre>{* Remove non-polar hydrogens? *}
{+ choice: true false +}
{===>} delenph=true; 
</pre>

By default non-polar protons are deleted to speed-up the calculations. They are however accounted for in the heavy atoms parameters since the force field used (OPLS) is a united atom force field.

**Important:**

* * *

<a name="histidines">**3\. <u>Definition of the protonation state of histidines</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/histidines.png)  

By default, all histidines are protonated and thus carry a net positive charge. In this section you can specify the protonation state of histidines for each protein. A neutral histidine can exist in two forms:

*   HISD: the imino proton is attached to the ND1 nitrogen
*   HISE: the imino proton is attached to the NE2 nitrogen

It is important that you take time to think about the possible protonation state of histidines when present since a charge difference of +/- 1 can make quite some difference in the docking results. If no information is available on the pH of the solution and/or the pka of your histidines, one reasonable option is to use **[WhatIF](http://www.cmbi.kun.nl/whatif/)** to generate the protons on your molecule and check what choices were made for the protonation state of the various histidines. For this purpose you can use the [WhatIF web server](https://swift.cmbi.umcn.nl/whatif/). Alternatively you can use the **reduce** program from the **molprobity** software suite (this is what the HADDOCK web portal is currently using). We even provide a script called _molprobity.py_ to extract this info in our **[HADDOCK tools](https://github.com/haddocking/haddock-tools)** GitHUb repo.  

* * *

<a name="interface">**4\. <u>Definition of the semi-flexible interface</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/interface.png)  

HADDOCK performs a semi-flexible simulated annealing (SA). Here you have to define the residues that will be allowed to move during the SA.  

In HADDOCK 2.X, you have two options:  

*   Manual definition of the semi-flexible segments*   Automated mode (default)  

    _<u>Manual definition of the semi-flexible segments</u>_  

    Usually we define as **flexible residues** all **active and passive residues +/- 2 sequential residues**.  

    For each molecule, enter the number of flexible segments and then the starting and ending residue of each segment.  

    **_Note_**

    [FAQ](/software/haddock2.2/faq#segments)

    _<u>Automated mode (default)</u>_  

    HADDOCK 2.X offers the possibility to automatically define the semi-flexible residues. This is done automatically for each structure by selecting all residues that make intermolecular contacts within a 5A cutoff. You can change this cutoff value by editing the _flexauto.cns_ CNS script in the _**protocols**_ directory.  

    To turn on the automated mode, the number of segments should be a negative number (default: -1). Since HADDOCK2.X also allows to randomly define ambiguous interaction restraints from the defined semi-flexible segments (see the [distance restraints](#disre) section below), this number could also be larger (e.g. -3 to define three segments from which to randomly define AIRs. As long as the number is negative, the semi-flexible residues will be defined automatically.  

    * * *

    <a name="flex">**5\. <u>Definition of fully flexible segments</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/flexible.png)  

    HADDOCK allows the definition of fully flexible segments for each molecule. These will be fully flexible throughout the entire docking protocol except for the rigid body minimization (see [the docking](/software/haddock2.2/docking) section).  

    For each molecule, enter the number of fully flexible segments and then the starting and ending residue of each segment.  

    **_Note_**

    [FAQ](/software/haddock2.2/faq#segments)

    * * *

    <a name="sym">**6\. <u>Symmetry restraints</u>**</a>  

    This section allows to define two types of restraints to enforce symmetry either within or between molecules:
    *   non-crystallographic symmetry restraints (NCS)
    *   C2, C3, S3, C4 and C5 symmetry restraints  
    <u>_Non-crystallographic symmetry restraints (NCS)_</u> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/ncs.gif)  

    The NCS option imposes non-crystallographic symmetry restraints: it enforces that two molecules, a fraction thereof or even two sub-domains within the same molecule should be identical without defining any symmetry operation between them.  

    HADDOCK 2.X allows to define up to five pairs for which NCS restraints will be applied. The syntax is fully flexible since start and end residues can be defined together with the molecule SEGID. In that way both intermolecular and intra-molecular NCS restraints can be defined.  

    **Note:**

    <u>_C2, C3, S3, C4 and C5 symmetry restraints_</u> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/symmetry.png)  

    HADDOCK 2.X offers the possibility to define multiple symmetry relationships within or in between molecules. This is done by using symmetry distance restraints (Nilges 1993). Symmetry distance restraints are a special class in CNS: for each restraint two distances are specified which are required to remain equal during the calculations, irrespective of the actual distance. They can be defined in CNS as:

    <pre>noe 
        class symm
        assign (resid 1 and name CA  and segid A)
                (resid 50 and name CA  and segid B) 0 0 0
        assign (resid 1 and name CA  and segid B)
                (resid 50 and name CA  and segid A) 0 0 0
    end
    noe
       potential  symm symmetry
    end
    </pre>

    By defining multiple pairs of distances between the CA atoms of two chains, C2 symmetry can be enforced.  

    This can be easily extended to higher symmetries by defining multiple pairs of symmetry restraints:
    *   for C3, one can define three pairs of distances that should be equal:

    *   C5 symmetry can be enforced by defining five pairs:

    HADDOCK will automatically define the symmetry restraints based of the segments defined in _run.cns_ (this is done in the _symmultimer.cns_ CNS script). Currently 10 C2 pairs, 2 C3 triplets, 4 S3 tiplet, 2 C4 quaduple and 1 C5 quintuplet can be defined.  

    **Note:**

    * * *

    <a name="disre">**7\. <u>Distance restraints</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/distances.gif)  

    <u>_Ambiguous (AIRs) and unambigous distance restraints_</u>  

    Ambiguous (AIRs) and unambigous distance restraints specified in _new.html_ will always be read. In this section, however, you can specify the stage of the docking protocol at which a given type of distance restraint will be used for the first and last time:
    *   0: rigid body EM (it0)
    *   1: semi-flexible simulated annealing (SA) (it1)
    *   2: explicit solvent refinement (water)You should also specify the force constants for the various stages of the docking protocol:
    *   _hot_: high temperature rigid body dynamics
    *   _cool1_: first rigid body slow cooling SA
    *   _cool2_: second slow cooling SA with flexible side-chains at interface
    *   _cool3_: third slow cooling SA with flexible side-chains and backbone at interfaceThe force constants in the various stages are scaled from the previous to the current value, e.g. from the _cool1_ to the _cool2_ value in the second simulated annealing. For the explicit solvent refinement the value of _cool3_ will be used.  

    <u>_Random removal of AIRs_</u>  

    HADDOCK offer the possibility to randomly remove a fraction of the AIRs (only active on the ambiguous interaction restraints defined in _ambig.tbl_ for each docking trial. This option is particularly useful when the accuracy of the AIRs is questionable since by random removal bad restraints could be discarded, allowing for better docking solutions.  

    To enable random removal of restraints, set _noecv_ to _true_ and define the number of sets into which the AIRs will be partitioned; one set will be randomly discarded. By setting for example the number of partitions (_npart_) to 2, 50% of the AIRs will be discarded for each docking trial; for _npart=4_ 25% of the AIRs will be randomly discarded.  

    <u>_Hydrogen bond restraints_</u>  

    Define here if you want to use hydrogen bond restraints. The restraint file should have been specified in _new.html_.  

    <u>_Random interaction restraints definition_</u>  

    Define here if you want to randomly define interaction restraints (AIRs) from solvent accessible residues. The sampling will be done from the defined [semi-flexible segments](#interface). To sample the entire surface, define the entire sequence as semi-flexible and use the [automated semi-flexible segment](/software/haddock2.2/run.cns#interface) definition to limit the amount of flexibility to the interface region. For more details see the [AIR restraints](/software/haddock2.2/generate_air_help#ranair) section of the online manual.  

    Random AIRs are only active during the rigid body stage of the [docking](/software/haddock2.2/docking) protocol. For the [semi-flexible refinement](/software/haddock2.2/docking#sa), one AIR will be automatically defined between all residues within 5A from another molecule. No AIRs will be active during the final [explicit solvent refinement](/software/haddock2.2/docking#water).
    **Note1:**

    _new.html_
    <u>_Center of mass restraints_</u>  

    Define here if you want to use [center of mass restraints](/software/haddock2.2/generate_air_help#cm) and specify the corresponding force constant. Can be useful in combination with random interaction restraints definition (see above).  

    <u>_Surface contact restraints_</u>  

    Define here if you want to use [surface contact restraints](/software/haddock2.2/generate_air_help#surf) and specify the corresponding force constant. This can be useful in combination with random interaction restraints definition (see above).  

    <u>_Automatic weighting of distance restraints_</u>  

    Also available is an option to automatically adjust the force constant of the distance restraints (sum of distance and AIRs) to balance the distance restraint energy with the sum of the force field energy terms (bonds, angles, dihedrals, electrostatic and van der Waals) such as the ratio of force field energy versus distance restraint energy is equal to 2. For this you need to specify the number of distance and AIR restraints. The automatic scaling option will not appear when editing the **run.cns** file in a web browser. You will have to edit the file manually for this.  

    **_Note:_**

    _set_noe_scale.cns_

    _**protocols**_

    * * *

    <a name="rgre">**8\. <u>Radius of gyration restraint</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/rg.png)  

    A radius of gyration distance restraint can be turned on here. It will be active throughout the entire protocol, but can be effectively turned off by setting the force constant for a given stage to 0\. The radius of gyration should be entered in angstrom. By default it is applied to the entire system, but can be restricted to part of the system using standard CNS atom selections.  

    For example to limit it to chains B and C define:  

    * * *

    <a name="dna">**9\. <u>DNA/RNA restraints</u>**</a>  

    Define here if you want to use DNA/RNA restraints. To use such restraints, edit the _dna-rna-restraints.cns_ file provided in the _**protocols**_ directory (you can use the same mechanism for that as for editing the _run.cns_ parameter file from the [project setup](/software/haddock2.2/haddock-start) menu of HADDOCK), adapt it to your particular case, and place it in the _**data/sequence**_ directory. This file allows you to define base-pair, backbone dihedral angle and sugar pucker restraints.  

    * * *

    <a name="dihre">**10\. <u>Dihedrals</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/dihedrals.png)  

    If dihedral angle restraints have been defined in the **new.html** file, turn the flag **"use"** to true and specify the force constants for the various stages of the semi-flexible simulated annealing (for water the value of _cool3_ will be used).  

    HADDOCK2.2 offer a new option to automatically dihedral angle restraints from the input structures. By default it is turned off, but you can specify to define dihedral angle restraints for the entire backbone, alpha-helices only or alpha-helices and beta-sheets. The secondary structure elements are defined based on a simple phi/psi dihedral angle criterion.  

    * * *

    <a name="karplus">**11\. <u>Karplus coupling restraints</u>**</a>  

    You can specify in this section the Karplus coefficients and force constants for J-coupling restraints. This should directly be edited in the run.cns and will not show up in a browser window.  

    * * *

    <a name="dipo">**12\. <u>Residual Dipolar couplings</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/RDCs.gif)  

    If RDC data are available and have been defined in the **new.html** file, you can define them in this section. Five classes are supported. For each class you can specify the type of function:  

    *   SANI: direct refinement against the dipolar couplings (a tensor will be included in the structures calculations)  

    *   VANGLE: refinement using intervector projection angle restraints  
        ([Meiler et al. _J. Biomol. NMR_ **17**, 185 (2000)](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=10805131&dopt=Abstract))  
    You can specify the first and last stage at which the various RDCs will be used.
    *   0: rigid body EM (it0)
    *   1: semi-flexible simulated annealing (SA) (it1)
    *   2: explicit solvent refinement (water)This option allows for example to combine VANGLE and SANI type restraints. Intervector projection angle restraints lead to better convergence in the first phase of the docking (0,1) while direct RDC restraints can be used in the final explicit solvent refinement (2) to fine-tune the RDCs (see for details [van Dijk _et al._ _Proteins_, **60**, 367-381 (2005)](https://doi.org/doi:10.1002/prot.20476)).  

    For SANI Da (in Hz) and R (R=Dr/Da) should be specified. You should also specify the force constants for the various stages of the docking protocol:
    *   _hot_: high temperature rigid body dynamics
    *   _cool1_: first rigid body slow cooling SA
    *   _cool2_: second slow cooling SA with flexible side-chains at interface
    *   _cool3_: third slow cooling SA with flexible side-chains and backbone at interfaceFor more information on using RDC as restraints for docking see also the [RDC restraints](/software/haddock2.2/RDC_help) section of the online HADDOCK manual.  

    * * *

    <a name="pcs">**13\. <u>Pseudo contact shifts</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/pcs.png)  

    If pseudo contact shift data are available and have been defined in the **new.html** file, you can define them in this section. Ten classes are supported. For each class you can specify the first and last stage at which the various RDCs will be used.
    *   0: rigid body EM (it0)
    *   1: semi-flexible simulated annealing (SA) (it1)
    *   2: explicit solvent refinement (water)You should also specify the force constants for the various stages of the docking protocol:
    *   _hot_: high temperature rigid body dynamics
    *   _cool1_: first rigid body slow cooling SA
    *   _cool2_: second slow cooling SA with flexible side-chains at interface
    *   _cool3_: third slow cooling SA with flexible side-chains and backbone at interfaceand the tensor parameters R and D.  

    For more information on using diffusion anisotropy as restraints for docking see also the [PCS restraints](/software/haddock2.2/PCS_help)section of the online HADDOCK manual. Refer to the following publication for details of the implementation in HADDOCK:

    [Protein-Protein HADDocking using exclusively Pseudocontact Shifts.](https://doi.org/doi:10.1007/s10858-011-9514-4)

    _J. Biomol. NMR_

    **50,**

    * * *

    <a name="dani">**14\. <u>Diffusion anisotropy restraints</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/DANI.gif)  

    If [diffusion anisotropy restraints (DANI)](/software/haddock2.2/DANI_help) (from <sup>15</sup>N relaxation measurements) are available and have been defined in the **new.html** file, you can define them in this section. Five classes are supported (e.g. for measurements at different fields).  

    You can specify the first and last stage at which the various DANI restraint sets will be used.
    *   0: rigid body EM (it0)
    *   1: semi-flexible simulated annealing (SA) (it1)
    *   2: explicit solvent refinement (water)For each DANI set, the correlation time (ns), Da (in Hz) and R (R=Dr/Da) should be specified, together with the proton and nitrogen 15 frequencies (MHz). You should also specify the force constants for the various stages of the docking protocol:
    *   _hot_: high temperature rigid body dynamics
    *   _cool1_: first rigid body slow cooling SA
    *   _cool2_: second slow cooling SA with flexible side-chains at interface
    *   _cool3_: third slow cooling SA with flexible side-chains and backbone at interfaceFor more information on using diffusion anisotropy as restraints for docking see also the [DANI restraints](/software/haddock2.2/DANI_help) section of the online HADDOCK manual. Their implementation in HADDOCK is described in [van Dijk _et al._ _J. Biomol. NMR_, **34**, 237-244 (2006)](https://doi.org/doi:10.1007/s10858-006-0024-8).  

    * * *

    <a name="topo">**15\. <u>Topology and parameters files</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/topology.gif)  

    In this section the topology, linkage and parameter files are specified for each molecule. The default values are for proteins using the improved parameters of [Linge et al. 2003](http://www3.interscience.wiley.com/cgi-bin/abstract/102523901/START) and OPLSX non-bonded parameters.  

    For dna use instead the _dna-rna-allatom.top_, _dna-rna-allatom.param_ and _dna-rna.link_ files in the **toppar** directory.  

    Also provided in the **toppar** directory in this version of HADDOCK are topologies and parameters for heme groups. See for this the _topallhdg.hemes_ and _parallhdg.hemes_ files. An example of distance restraints to maintain non-covalently attached heme in place is given in _metalcenter.tbl_ in the _**toppar**_ directory.  

    _topallhdg.hemes_ also contains a number of patches to covalently attach the heme group to CYS and HIS residues. These patches should be added manually to the _generate_X.inp_ when needed (an example is provided but currently commented out; search for heme in the file). (These files were kindly provided by Gabriele Cavallaro, CERM Firenze).  

    Parameter and topology files for small ligands should be provided by the user and place in the _**toppar**_ directory (see also the [FAQ](/software/haddock2.2/faq) section of the online manual).  

    In this version of HADDOCK, ions should be automatically recognized provided their naming is consistent with what is defined in the _ion.top_ topology file in the _**toppar**_ directory. For the torsion angle dynamics part of the [docking protocol](/software/haddock2.2/docking) (it1), a covalent bond will be automatically defined to the closest ligand atom (only for cations). This is done in the _covalions.cns_ CNS script in the _**protocols**_ directory; the following cations are currently defined: MG<sup>+2</sup>, CA<sup>+2</sup>, FE<sup>+2</sup>, FE<sup>+3</sup>, NI<sup>+2</sup>, CO<sup>+2</sup>, CO<sup>+3</sup>, CU<sup>+1</sup>, CU<sup>+2</sup> and ZN<sup>+2</sup>. If your system contains other ions add them to the _covalions.cns_ file (they should however be defined in _ion.top_).  

    * * *

    <a name="param">**16\. <u>Energy and interaction parameters</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/energy.gif)  

    You can define in this section a number of parameters that control the electrostatic energy term during the docking process, that allow you to scale down the intermolecular interactions and sample 180 degrees rotated solutions.  

    <u>_Electrostatic treatment_</u>  

    The electrostatic energy term can be turned on or off for the first two stages of the docking, namely the [rigid body minimization](/software/haddock2.2/docking#mini) and the [semi-flexible simulated annealing](/software/haddock2.2/docking#sa). Two implementations are now supported to describe the solvent implicitly:
    *   constant dielectric
    *   distance dependent dielectricThe _epsilon_ constant should be defined.  

    For the final stage, the [explicit solvent refinement](/software/haddock2.2/docking#water), a constant dielectric with an epsilon equal to one is used by default.  

    <u>_Scaling of intermolecular interactions_</u>  

    This section also allows you to specify scaling factors for the various stages of the docking:
    *   rigid body EM
    *   rigid body dynamic: high temperature and slow cooling SA rigid body dynamics
    *   second slow cooling SA with flexible side-chains at interface
    *   third slow cooling SA with flexible side-chains and backbone at interfaceThese scaling factors only affect the intermolecular van der Waals and electrostatic energy terms.
    **Note:**

    <u>_Interaction matrix for non-bonded interactions_</u>[![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/interaction-matrix.png)  

    This is a new feature in HADDOCK2.2 which allows to scale down or turn off interactions between specific molecules. It is useful for example in the context of ensemble-averaged docking where the distance restraints should be averaged over multiple binding poses. This option has been applied for example in ensemble-averaged docking of a peptide using PRE-derived distance restaints. See:  

    [Characterizing the N- and C-terminal SUMO interacting motifs of the scaffold protein DAXX.](https://doi.org/doi:10.1074/jbc.M111.231647)

    _J. Biol. Chem._

    **286**

    * * *

    <a name="numstruc">**17\. <u>Number of structures to dock</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/numstruc.gif)  

    The docking process is performed in three distinct steps:
    1.  [rigid body minimization](/software/haddock2.2/docking#mini) (it0)
    2.  [semi-flexible simulated annealing](/software/haddock2.2/docking#sa) (it1)
    3.  [explicit solvent refinement](/software/haddock2.2/docking#water) (water)You can define here the number of structures to generate in the first two steps and the number of structures to analyze (for the explicit solvent refinement see [below](#water)).  

    <u>_Sampling of 180 degrees-rotated solutions_</u>  

    This is a new option in HADDOCK 2.X that allows sampling of 180 degrees-rotated solutions at both the [rigid-body](/software/haddock2.2/docking#rigid) and [semi-flexible](/software/haddock2.2/docking#sa) docking stages. If turned on (default for rigid-body stage), for each model generated, a 180 degree rotated solution will be generated automatically by HADDOCK and either energy minimized (rigid-body) or submitted to the semi-flexible refinement protocol (it1). The rotation axis is automatically defined from the vector connecting the center of masses of the two interfaces, each interface being defined by all residues forming intermolecular contacts within 5A (this cutoff is defined in the _rotation180.cns_ CNS script in the _**protocols**_ directory.  

    Sampling of 180 degree rotated solutions in the rigid-body stage clearly improve the docking performance (unpublished data). If turned on during the semi-flexible refinement, both refined solutions will be written to disk, doubling the effective number of structures.
    **Note1:**

    **Note2:**

    [solvated docking](#solvdock)

    * * *

    <a name="dock">**18\. <u>DOCKING protocol</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/docking.png)  

    Here you can define parameters for the [rigid-body](/software/haddock2.2/docking#mini) docking step (it0) if you want to:
    *   cross-dock all combinations in the ensembles of starting structures (should be turned off for example if you only want to perform water refinement of a preformed complex)
    *   randomize the starting orientations or not
    *   perform the rigid body minimization or not
    *   allow translation during the minimization (it can be useful to turn it off for docking highly flexible small molecules (see the [docking section of the online manual)).](/software/haddock2.2/docking#mini)[During the rigid body minimization you can define the **number of trials** for each starting configuration. Only the best solution (according to your sorting criterion (see](/software/haddock2.2/docking#mini) [scoring](#scoring))) will be kept. This option saves disk space, but the sorting scheme should be robust otherwise you might select out good solutions. This is typically a cheap step in terms of CPU requirements.  

    The next parameters govern the [semi-flexible simulated annealing](/software/haddock2.2/docking#sa) protocol. You can define the start and end temperatures and the number of integration steps for the various stages of the annealing protocol (see [the docking](/software/haddock2.2/docking#sa) section).
    **Note:**

    [solvated docking](#solvdock)

    * * *

    <a name="solvdock">**19\. <u>Solvated docking</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/solvdock.png)  

    In this section you can turn on solvated docking. If turned on, the initial structures will first be solvated in a shell of TIP3P water (only water molecules within 5.5 A of the protein will be kept). The rigid-body docking will thus be performed from solvated proteins. Two methods for dealing with interfacial waters are implemented:  

    *   **database-based (db)** (_recommended upon restrained solvated docking_ (see below)): interfacial water molecules will be removed in a biased Monte Carlo process until a user-defined fraction of water remain. This process can make use of two different propensity scales:
        *   propensities of finding water-mediated contacts between amino-acid pairs defined from a _statistical analysis of high-resolution crystal structures_. The water-mediated contact propensities can be found in the _db_statistical.dat_ CNS script in the _**protocols**_ directory.  

            For details see:  

            [Solvated docking: introducing water into the modelling of biomolecular complexes.](https://doi.org/doi:10.1093/bioinformatics/btl395)

            _Bioinformatics_

            **22**

        *   propensities of finding water-mediated contacts between amino-acid pairs defined from the _Kyte-Doolittle hydrophobicity scale_. The corresponding water-mediated contact propensities can be found in the _db_kyte-doolittle.dat_ CNS script in the _**protocols**_ directory.  

            For details see:

            [Solvated docking using Kyte-Doolittle-based water propensities.](https://doi.org/doi:10.1002/prot.24210)

            _Proteins: Struc. Funct. & Bioinformatic_

            **81**

        An important parameter to be defined for database-solvated docking is the **fraction of interfacial water** to be kept after the Monte Carlo removal process. This is currently set to 50% based on our analysis of water-mediated contacts. New in HADDOCK2.2, this percentage can now be defined separately for nucleic acids (currently 75%). This is coming from the observation that nucleic acids show typically higher solvation. For details regarding nucleic acids solvated docking see:

        [Solvated protein-DNA docking using HADDOCK.](https://doi.org/doi:10.1007/s10858-013-9734-x)

        _J. Biomol. NMR_

        **56**

        Note that typically less than that (or even none) of the water molecules will be kept since an energy cut-off is applied after the Monte Carlo water removal step: all waters with unfavorable interaction energies (Evdw+Eelec>0) are removed. In some cases, this allows all interfacial waters to be removed at the end. The energy cutoff is defined in the _db1.cns_ CNS script in the _**protocols**_ directory.  

    *   **restrained solvating (restraints)**: in this approach, water molecules are restrained to be at proximity of amino-acids found to form the most water-mediated contacts (arg, asn, asp, gln, glu, his, lys, pro, ser, thr and tyr). This is done by defining ambiguous distance restraints between each water and highly solvated amino-acids on both side on an interface. _**Note that this method has not been thoroughly tested**_.  

        If _restrained solvating_ is chosen, three additional parameters should be set:  

        *   **initial distance cutoff**: all water molecules further away from a highly solvated amino-acid will be removed in the solvent shell generation step.
        *   **initial distance cutoff**: upper distance restraints for the definition of ambiguous water-amino-acid restraints.
        *   **force constant** for water-amino-acid distance restraints.Another parameters that can be modified is the **water-protein surface cut-off** used to remove water molecules that are remote from the interface (a water must be with this cut-off distance from two chains to be kept).  

    It is also possible to turn off **water translation** during rigid-body energy minimization if desired.  

    Finally, to increase sampling, it is possible to start the docking from differently solvated molecules. The **number of initial solvation shells** can be define here. If more than 1 is defined, the protein will be randomly rotated and a new solvation shell will be generated.  

    * * *

    <a name="water">**20\. <u>Final explicit solvent refinement</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/waterref.gif)  

    In this section you can define if the final [explicit solvent refinement](/software/haddock2.2/docking#water) should be performed (recommended since it does improve the docking solutions) and on how many structures. Two solvent models are currently supported: water and DMSO. DMSO is a fair mimic for a membrane environment.  

    You can also specify here the number of MD integration steps for the heating, sampling and cooling phases of the explicit solvent refinement.  

    You can also specify to keep the solvent, in which case an additional PDB file will be created in the _**structures/it1/water**_ directory with a __h2o.pdb_ extension containing both your complex and the solvent molecules.  

    * * *

    <a name="scoring">**21\. <u>Scoring</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/scoring.png)  

    In this section you can define individual weigths for the various terms using in scoring. This can be done separately for the various docking stages (rigid body (it0), semi-flexible refinement (it1) and explicit solvent refinement(water)). You can also define the number of structures to analyze after the simulated annealing and explicit solvent refinement.  

    This version of HADDOCK offers a fully flexible scoring scheme since the weight of the various energy terms can be defined separately for each phase of the docking. The scoring is performed according to the **weighted sum** (HADDOCK score) of the following terms:
    *   **Evdw**: van der Waals energy
    *   **Eelec**: electrostatic energy
    *   **Eair**: distance restraints energy (only unambiguous and AIR (ambig) restraints)
    *   **Erg**: radius of gyration restraint energy
    *   **Esani**: direct RDC restraint energy
    *   **Evean**: intervector projection angle restraints energy
    *   **Epcs**: pseudo contact shift restraint energy
    *   **Edani**: diffusion anisotropy energy
    *   **Ecdih**: dihedral angle restraints energy
    *   **Esym**: symmetry restraints energy (NCS and C2/C3/C5 terms)
    *   **BSA**: buried surface area
    *   **dEint**: binding energy (Etotal complex - Sum[Etotal components] )
    *   **Edesol**: desolvation energy calculated using the empirical atomic solvation parameters from Fernandez-Recio _et al._ _JMB_ **335**:843 (2004)The structure with the smallest weighted sum will be ranked first.
    **Note 1**

    **Note 2**

    **Note 3**

    [treatment of electrostatics](#param)

    The default scoring function settings of HADDOCK are for protein-protein complexes and use the following weights:  

    <pre>     HADDOCKscore-it0   = 0.01 Evdw + 1.0 Eelec + 1.0 Edesol + 0.01 Eair - 0.01 BSA

         HADDOCKscore-it1   =  1.0 Evdw + 1.0 Eelec + 1.0 Edesol +  0.1 Eair - 0.01 BSA

         HADDOCKscore-water =  1.0 Evdw + 0.2 Eelec + 1.0 Edesol +  0.1 Eair
    </pre>

    **Note:**

    **Note:**

    **Note:**

    In this section, you can also define a "skipping" parameter that allows you to sample more solutions from the rigid body EM docking (it0). If the value _x_ of this _skip_ parameter is larger than 0 then every _(x+1)th_ structure from it0 starting from the first structure will be further refined in the semi-flexible simulated annealing.  

    For example, if skip=1 and 200 structures should be refined in the semi-flexible simulated annealing, structures 1,3,5,7,... and 399 from the best 400 of it0 will be selected and written to the _file.nam_, _file.list_ and _file.cns_ files in the **structures/it0** directory. Three additional files (_file.nam_all_, _file.list_all_ and _file.cns_all_) containing the original sorting of all structures will be created.  

    * * *

    <a name="anal">**22\. <u>Analysis and clustering</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/analysis.png)  

    When performing the [analysis](/software/haddock2.2/analysis), HADDOCK will check [intermolecular hydrogen bonds](/software/haddock2.2/analysis#hb) and [intermolecular hydrophobic contacts](/software/haddock2.2/analysis#nb).  

    Here you can define the cut-off distances in Angstrom to define a hydrogen bond and a hydrophobic contact. Note that the hydrogen bond detection is only based on a distance criterion. For a more detailed analysis we recommend to use LIGPLOT (see [software links](/software/haddock2.2/software).  

    At the end of the calculation, the solutions are clustered. Two options for clustering are offered:
    *   RMSD-based clustering using the **_tools/cluster_struc_** program (a small C++ program that needs to be compiled during [installation](/software/haddock2.2/installation)). cluster_struc reads the output of the rmsd.inp CNS analysis script that generates the pairwise rmsd matrix over all structures analyzed and perform clustering. The RMSDs are calculated on the interface residues of the second molecule after fitting on the interface residues of the first molecule, what can be termed: interface-ligand-RMSD. The interface residues are automatically defined based on an analysis of all contacts found in all analysed models. Note that RMSD clustering might not be very discriminative in case of multibody docking.

    *   Fraction of native contacts (FCC) clustering using the **_tools/cluster_fcc.py_** python script. This option does not require a-priori fitting of the structures and is more robust for multibody docking. For details see:  

        [Clustering biomolecular complexes by residue contacts similarity.](https://doi.org/doi:10.1002/prot.24078)

        _Proteins: Struc. Funct. & Bioinformatic_

        **80**
        For this clustering step you need to specify a clustering cut-off and a minimum cluster size (recommended 4). For the cutoff, 7.5A works fine in most cases, while this value should be reduced to 5A or less for short peptides and 2 to 1A for small ligand docking. When using FCC clustering, a cutoff of 0.75 (or higher) is recommended.  

    The new FCC clustering offers the option to ignore chains when dealing with symmetrical oligomers. For example for a symmetrical trimer, this means that the ABC and ACB arrangements will cluster is the same cluster.  

    (For further details for manual analysis see [Analysis](/software/haddock2.2/analysis#cluster) for details).  

    * * *

    <a name="clean">**23\. <u>Cleaning</u>**</a>  

    Since HADDOCK does generate a lot of data and output files, we now built in a cleaning option. If turned on (default) all (except for the first structure of each stage) job, input and output files for the rigid-body, semi-flexible refinement and final explicit solvent refinement will be removed automatically upon completion. This saves a significant amount of space.  

    * * *

    <a name="jobs">**25\. <u>Parallels jobs</u>**</a> [![(screenshot)](http://www.bonvinlab.org/software/haddock2.2/camera.jpg)](/software/haddock2.2/jobs.gif)  

    In this section you can define the way the structure calculation will be run, and the location of the [CNS](http://cns.csb.yale.edu) executable. Currently 10 nodes or queues can be specified.  

    If you are going to run HADDOCK on a multi-processor computer with for example 4 CPUs, the entries for the first row could be:
    *   queue command: _csh_ (this will run the jobs in background on the local computer)
    *   cns executable: _/software/bin/cns_
    *   number of jobs: _4_ (four jobs in parallel)and all other entries empty.  

    In Utrecht we are using two different batch queuing system (DQS and openPBS) that distribute the jobs on various linux clusters. Our entry for this setup is:
    *   queue command: _ssub linux_ (ssub is a wrapper script for submitting to the batch queuing system and linux is the queue destination)
    *   cns executable: _/software/bin/cns_
    *   number of jobs: _10_ (10 jobs in parallel)and all other entries empty.  

    Other ways of distributing jobs over a cluster are addressed in the [FAQ](/software/haddock2.2/faq#batch) section of the manual.

    * * *
