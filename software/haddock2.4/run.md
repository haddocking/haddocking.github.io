---
layout: page
ags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified:
comments: false
title: HADDOCK2.4 manual - run.cns parameters
image:
  feature: pages/banner_software.jpg
---

The **run.cns** file contains all the parameters to run the docking. You need to edit this file to define a number of project-specific parameters such as the number of structures to generate at the various stages, which restraints to use for docking and various parameters governing the docking and scoring. Many parameters have default values which you do not need to change unless you want to experiment with parameters (and know what you are doing).

The **run.cns** is divided into several sections that will be detailed in the following:

* table of contents
{:toc}


* * *

### Number of molecules for docking

here you have to specify the number of molecules for docking. HADDOCK version 2.4 and higher currently supports up to 20 separate molecules, thus allowing multi-body (N>=2) docking. This should be set automatically by HADDOCK from the number defined in ***[run.param](/software/haddock2.4/docking/#defining-the-input-data---runparam){:target="_blank"}***.

**Note:** You can even specify only one molecule. This will no longer be called docking, but it allows to use HADDOCK for refinement purpose instead.

* * *

### Filenames

This section consist of all the files that will be used for the docking. If the ***run.param*** file has been set up properly, most fields will be set correctly. The only thing you might want to change is the name of the current project which is used as as rootname for all files.

<pre style="background-color:#DAE4E7">
{======================= filenames =========================}
{*  the name of your current project *}
{*  this will be used as name for the generated structures *}
{===>} fileroot="e2a-hpr";

{* RUN directory *}
{*  the absolute path of your current run, e.g. /home/haddock/run1*}
{===>} run_dir="./";
{* PDB file of molecule 1 *}
{===>} prot_coor_mol1="e2aP_1F3G.pdb";
{* PSF file of molecule 1 *}
{===>} prot_psf_mol1="e2aP_1F3G.psf";
{* segid of molecule 1 *}
{===>} prot_segid_mol1="A";
{* fileroot of molecule 1 *}
{===>} prot_root_mol1="e2aP_1F3G";
{* Fix Molecule at Origin during it0 *}
{+ choice: true false +}
{===>} fix_origin_mol1=false;
{* Is molecule 1 DNA? *}
{+ choice: true false +}
{===>} dna_mol1=false;
{* Is molecule 1 a cyclic peptide? *}
{+ choice: true false +}
{===>} cyclicpept_mol1=false;
{* Is molecule 1 a shape? *}
{+ choice: true false +}
{===>} shape_mol1=false;
{* Coarse grained molecule? *}
{+ choice: true false +}
{===>} cg_mol1=false;
</pre>


**Note 1:** Do not change the name of the input PDB file otherwise it will not be found by HADDOCK (this file corresponds to the one you previously defined in ***run.param***).


**Note 2:** Do not use similar names for the various molecules and the name of the current project.

HADDOCK2.4 has a number of new options:

* *__fix_origin_molX__*:	Allows to fix a molecule in its original position
* *__cyclicpept_molX__*:	Defines a cyclic peptide. If set to true HADDOCK will generate a cyclic topology provided the N- and C-termini are close enough in space (<3A) a peptide bond will be defined between the N- and C-terminal residues
* *__shape_molX__*:	Defines that a molecule is a shape represented by beads (reside name SHA and atom name SHA)
* *__cg_molX__*:	Defines if a molecule is coarse-grained (should already be defined in the ***run.param*** file)


At the end of this section there is also a parameter that defines if non-polar protons should be kept or not:

<pre style="background-color:#DAE4E7">{* Remove non-polar hydrogens? *}
{+ choice: true false +}
{===>} delenph=true;
</pre>

By default non-polar protons are deleted to speed-up the calculations. They are however accounted for in the heavy atoms parameters since the force field used (OPLS) is a united atom force field.

**Important:** In case you are defining distance restraints involving non-polar protons (e.g. NOE restraints), make sure to set delenph to false, otherwise your restraints will not be used! To make sure all your restraints are properly read, it is recommended to check one of the generated output file for a model (e.g. from the rigid body docking) and search for error messages related to the NOE restraints (NOESET-INFO).

* * *

### Definition of the protonation state of histidines

By default (*autohis=true*) (a new feature), HADDOCK2.4 will automatically define the protonation state of histidines when generating the topology and rebuilding any missing atoms by trying all three combinations (neutral with the proton on either the D or E nitrogen, or positively charged with a proton on both nitrogens). 

<pre style="background-color:#DAE4E7">{* Remove non-polar hydrogens? *}
{==================== histidine patches =====================}
{* Automatically define histidine protonation state based on energetics *}
{===>} autohis=true;

{* Patch to change doubly protonated HIS to singly protonated histidine (HD1) *}
{* just give the residue number of the histidines for the HISD patch, set them to zero if you don't want them *}

{* Number of HISD for molecule 1 *}
{===>} numhisd_1=0;

{===>} hisd_1_1=0;
{===>} hisd_1_2=0;
{===>} hisd_1_3=0;
{===>} hisd_1_4=0;
{===>} hisd_1_5=0;
...
</pre>


If this automatic option is turned off (*autohis=false*), you should specify the protonation state of histidines for each protein. In not defined all histidines will be protonated and thus carry a net positive charge. You only need thus to specify the neutral (uncharged) histidine residues, which can exist in two forms:

*   HISD: the imino proton is attached to the ND1 nitrogen
*   HISE: the imino proton is attached to the NE2 nitrogen

It is important that you take time to think about the possible protonation state of histidines when present since a charge difference of +/- 1 can make quite some difference in the docking results. 

The HADDOCK web server is for example using the **reduce** program from the **molprobity** software suite to select the histidines protonation states. To do the same manually we provide a script called _molprobity.py_ in our **[HADDOCK tools](https://github.com/haddocking/haddock-tools){:target="_blank"}** GitHUb repo.


* * *

### Definition of the semi-flexible interface

HADDOCK performs a [semi-flexible simulated annealing (SA) refinement](/software/haddock2.4/protocol/#semi-flexible-simulated-annealing){:target="_blank"} of the interfaces between molecules. Here you have to define the residues that will be considered flexible during the SA.

In HADDOCK 2.X, you have two options:

*   Automated mode (default) - *nseg_X=-1*
*   Manual definition of the semi-flexible segments

<pre style="background-color:#DAE4E7">
{========= Definition of semi-flexible interface ============}
{* Define the interface of each molecule.*}
{* Side-chains and backbone of these residues will be allowed to move during semi-flexible refinement*}

{* number of semi-flexible segments for molecule 1 (-1 for automated mode) *}
{* Note that current max is 10 (edit the run.cns to add more segments *}

{===>} nseg_1=-1;

{* Residues of molecule 1 at interface *}

{===>} start_seg_1_1="";
{===>} end_seg_1_1="";
{===>} start_seg_1_2="";
{===>} end_seg_1_2="";
...
</pre>


#### Automated mode (default)

HADDOCK 2.X offers the possibility to automatically define the semi-flexible residues. This is done automatically for each structure by selecting all residues that make intermolecular contacts within a default 5A cutoff (which can be changed in *run.cns*). 

To turn on the automated mode, the number of segments should be a negative number (default: -1). Since HADDOCK2.X also allows to randomly define ambiguous interaction restraints from the defined semi-flexible segments (see the [distance restraints](#disre) section below), this number could also be larger (e.g. -3 to define three segments from which to randomly define AIRs. As long as the number is negative, the semi-flexible residues will be defined automatically.

#### Manual definition of the semi-flexible segments

For each molecule, enter the number of flexible segments and then for each segment the starting and ending residue of each segment.

***Note*** that the maximum number of segments defined in run.cns is 10 for each molecule. To add more segments, edit the run.cns file (See the [FAQ](/software/haddock2.4/faq){:target="_blank"} section).


* * *

### Definition of fully flexible segments

HADDOCK allows the definition of fully flexible segments for each molecule. These will be fully flexible throughout the entire docking protocol except for the rigid body minimization (see [the protocol](/software/haddock2.4/protocol){:target="_blank"} section).

For each molecule, enter the number of fully flexible segments and then the starting and ending residue of each segment.


<pre style="background-color:#DAE4E7">
{=========== Definition of fully flexible segments ==========}
{* Define the fully flexible segment of each molecule.*}
{* These segments will be allowed to move at all stages of it1 *}

{* Number of fully flexible segments for molecule 1                  *}
{* Note that current max is 5 (edit the run.cns to add more segments *}

{===>} nfle_1=0;

{* Fully flexible segments of molecule 1 *}

{===>} start_fle_1_1="";
{===>} end_fle_1_1="";
{===>} start_fle_1_2="";
{===>} end_fle_1_2="";
{===>} start_fle_1_3="";
{===>} end_fle_1_3="";
{===>} start_fle_1_4="";
{===>} end_fle_1_4="";
{===>} start_fle_1_5="";
{===>} end_fle_1_5="";
...
</pre>


***Note*** that the maximum number of fully flexible segments is 5 for each molecule. To add more segments, edit the run.cns file (See the [FAQ](/software/haddock2.4/faq#segments) section).


* * *

### Membrane Z-positioning restraints

This is a new and rather experimental type of restraints in HADDOCK2.4. These Z-positioning restraints are defining an harmonic potential along the Z-axis (assume to be perpendicular to a membrane plane). These restraints are applied to selected segments defined by a start (*zres_sta_X*) and end (*zres_end_X*) residue numbers and the associated chainID/segID (*zres_seg_X*). This z-restraining potential can be applied to:

* keep segments within the defined Z coordinate range (*zres_type_X=inside*), or
* keep segments outside the defined Z coordinate range  (*zres_type_X=outside*).

Multiple segments can be defined as defined by the *numzres* parameter.

The width of the membrane region is defined by the *zresmaz* and *zresmin* values.

To activate this type of restraints set *zres_on=true*.

***Note*** that this restraining potential is not limited to describing a membrane but can be use generically.


<pre style="background-color:#DAE4E7">
{==================== membrane positioning restraints  ==================}
{* Do you want to use membrane positioning restraints ? *}
{+ choice: true false +}
{===>} zres_on=false;

{* Force constant for membrane positioning restraints ? *}
{===>} kzres=10.0;

{* Maximum z value for membrane positioning restraints ? *}
{===>} zresmax=0.0;

{* Minimum z value for membrane positioning restraints ? *}
{===>} zresmin=0.0;

{* Number of membrane positioning restrained segments *}
{===>} numzres=0;

{* Define the segment for membrane positioning restraints *}
{===>} zres_sta_1="";
{===>} zres_end_1="";
{===>} zres_seg_1="";
{+ choice: "inside" "outside"+}
{===>} zres_type_1="";
...
</pre>


* * *

### Non-crystallographic symmetry restraints (NCS)

The NCS option imposes non-crystallographic symmetry restraints: It enforces that two molecules, a fraction thereof or even two sub-domains within the same molecule should be identical without defining any symmetry operation between them. Basically this implies that the positional RMSD between the two defined molecules should be 0 (i.e. they have exactly the same conformation) without imposing a specific symmetry between those.

HADDOCK 2.X allows to define up to five pairs for which NCS restraints will be applied. The syntax is fully flexible since start and end residues can be defined together with the molecule SEGID. In that way both intermolecular and intra-molecular NCS restraints can be defined.

To activate this type of restraints set *ncs_on=true*.


<pre style="background-color:#DAE4E7">
{====================== NCS restraints  =====================}
{* Do you want to use NCS restraints? *}
{+ choice: true false +}
{===>} ncs_on=false;

{* Force constant for NCS restraints *}
{===>} kncs=1.0;

{* Number of NCS pairs *}
{===>} numncs=0;

{* Define the segments pairs for NCS restraints *}
{===>} ncs_sta1_1="";
{===>} ncs_end1_1="";
{===>} ncs_seg1_1="";
{===>} ncs_sta2_1="";
{===>} ncs_end2_1="";
{===>} ncs_seg2_1="";
...
</pre>


**Note** that since all atoms will be used for the definition of NCS restraints, it is important the NCS pairs contain exactly the same number of atoms.


* * *

### Symmetry restraints

HADDOCK 2.X offers the possibility to define multiple symmetry relationships within or in between molecules. This is done by using symmetry distance restraints (Nilges 1993). Symmetry distance restraints are a special class in CNS: for each restraint two distances are specified which are required to remain equal during the calculations, irrespective of the actual distance. They can be defined in CNS as:

<pre style="background-color:#DAE4E7">
noe
  class symm
  assign (resid 1 and name CA  and segid A) (resid 50 and name CA  and segid B) 0 0 0
  assign (resid 1 and name CA  and segid B) (resid 50 and name CA  and segid A) 0 0 0
  ...
end

noe
  potential symm symmetry
end
</pre>

By defining multiple pairs of distances between the CA atoms of two chains, various symmetries can be enforced.
In this section you can define various types of symmetry restraints:

*   C2 symmetry by define a pair of segments to which the symmetry restraints are applied
*   C3 symmetry by define a triple of segments to which the symmetry restraints are applied
*   C4 symmetry by define a quadruple of segments to which the symmetry restraints are applied
*   C5 symmetry by define a quintuple of segments to which the symmetry restraints are applied
*   S3 symmetry, a special case of C3 with a screw axis

HADDOCK will automatically define the symmetry restraints based of the defined segments (this is done in the _symmultimer.cns_ CNS script).
Those are applied to CA, BB and P atoms for proteins (CA or BB (coarse grained)) and nucleic acids, respectively.

To activate this type of restraints set *sym_on=true* and define the number of the various types of symmetry restraints.


<pre style="background-color:#DAE4E7">
{==================== Symmetry restraints  ==================}
{* Do you want to use symmetry restraints ? *}
{+ choice: true false +}
{===>} sym_on=false;

{* Force constant for symmetry restraints ? *}
{===>} ksym=10.0;

{* Number of C2 symmetry pairs *}
{===>} numc2sym=0;

{* Define the segment pairs C2 symmetry restraints *}
{===>} c2sym_sta1_1="";
{===>} c2sym_end1_1="";
{===>} c2sym_seg1_1="";
{===>} c2sym_sta2_1="";
{===>} c2sym_end2_1="";
{===>} c2sym_seg2_1="";
...
</pre>


**Note:**  By combining multiple symmetry restraints is is possible to enforce other symmetries. For example D2 symmetry in a tetramer can be defined by imposing six C2 symmetry pairs: A-B, B-C, C-D, D-A, A-C and B-D.


* * *

### Distance restraints

#### Ambiguous (AIRs) and unambiguous distance restraints

Ambiguous (AIRs) and unambiguous distance restraints specified in [*run.param*](/software/haddock2.4/docking/#defining-restraints){:target="_blank"} will always be read. In this section, however, you can specify the stage of the docking protocol at which a given type of distance restraint will be used for the first and last time:
*   0: rigid body EM (it0)
*   1: semi-flexible simulated annealing (SA) (it1)
*   2: explicit solvent refinement (water)

You should also specify the force constants for the various stages of the docking protocol:
*   _hot_: high temperature rigid body dynamics
*   _cool1_: first rigid body slow cooling SA
*   _cool2_: second slow cooling SA with flexible side-chains at interface
*   _cool3_: third slow cooling SA with flexible side-chains and backbone at interface.

The force constants in the various stages are scaled from the previous to the current value, e.g. from the _cool1_ to the _cool2_ value in the second simulated annealing. For the explicit solvent refinement the value of _cool3_ will be used.


<pre style="background-color:#DAE4E7">
{=========================== Distance restraints  ========================}
{* Turn on/off and energy constants for distance restraints *}

{===>} unamb_firstit=0;
{===>} unamb_lastit=2;
{===>} unamb_hot=10;
{===>} unamb_cool1=10;
{===>} unamb_cool2=50;
{===>} unamb_cool3=50;
{===>} amb_firstit=0;
{===>} amb_lastit=2;
{===>} amb_hot=10;
{===>} amb_cool1=10;
{===>} amb_cool2=50;
{===>} amb_cool3=50;
{===>} hbond_firstit=1;
{===>} hbond_lastit=2;
{===>} hbond_hot=10;
{===>} hbond_cool1=10;
{===>} hbond_cool2=50;
{===>} hbond_cool3=50;
</pre>


##### Random removal of AIRs

HADDOCK offer the possibility to randomly remove a fraction of the AIRs (only active on the ambiguous interaction restraints defined in _ambig.tbl_ for each docking trial. This option is particularly useful when the accuracy of the AIRs is questionable since by random removal bad restraints could be discarded, allowing for better docking solutions.

To enable random removal of restraints, set _noecv_ to _true_ and define the number of sets into which the AIRs will be partitioned; one set will be randomly discarded. By setting for example the number of partitions (_npart_) to 2, 50% of the AIRs will be discarded for each docking trial; for _npart=4_ 25% of the AIRs will be randomly discarded.


<pre style="background-color:#DAE4E7">
{* Do you want to randomly exclude a fraction of the ambiguous restraints (AIRs)? *}
{+ choice: true false +}
{===>} noecv=true;

{* Number of partitions for random exclusion (%excluded=100/number of partitions)? *}
{===>} ncvpart=2;
</pre>


#### Hydrogen bond restraints

Define here if you want to use hydrogen bond restraints. The restraint file should have been specified in [*run.param*](/software/haddock2.4/docking/#defining-restraints){:target="_blank"}.

To activate this type of restraints set *hbonds_on=true*.

<pre style="background-color:#DAE4E7">
{* Do you want to use hydrogen bond restraints? *}
{+ choice: true false +}
{===>} hbonds_on=false;
</pre>

**Note 1:**  Hydrogen bond restraints are by default not used during the initial rigid-body docking stage. This can be changed by modifying *hbond_firstit* (see above).

**Note 2:**  This type of restraints is not limited to hydrogen bonds. Any type of distance restraints can be included.


#### Random interaction restraints definition

Define here if you want to randomly define interaction restraints (AIRs) from solvent accessible residues. The sampling will be done from the defined [semi-flexible segments](#interface). To sample the entire surface, define the entire sequence as semi-flexible and use the automated semi-flexible segment definition to limit the amount of flexibility to the interface region.

To activate this type of restraints set *ranair=true*.


<pre style="background-color:#DAE4E7">
{* Do you want to define randomly ambiguous interaction restraints from accessible residues? *}
{* Only residues in the defined flexible segments will be considered *}
{* Note that this option is exclusive with any other distance restraints and only for it0    *}
{+ choice: true false +}
{===>} ranair=false;
</pre>

Random AIRs are only active during the rigid body stage of the [docking](/software/haddock2.4/protocol){:target="_blank"} protocol. For the semi-flexible refinement, one AIR will be automatically defined between all residues within 5A from another molecule. No AIRs will be active during the final explicit solvent refinement.


**Note:**  Random AIRs are exclusive with ambiguous, unambiguous and hydrogen bond restraints defined in new.html. They can however be combined with surface and center of mass restraints (see below).


#### Center of mass restraints

Define here if you want to use [center of mass restraints](/software/haddock2.4/airs/#random-air-definition-ab-initio-mode){:target="_blank"} and specify the corresponding force constant. Can be useful in combination with random interaction restraints definition (see above).

To activate this type of restraints set *cmrest=true*.

<pre style="background-color:#DAE4E7">
{* Do you want to define center of mass (CM) restraints to enforce contact between the molecules? *}
{* Note that these are only active during it0 and it1 *}
{+ choice: true false +}
{===>} cmrest=false;

{* Define tight CM restraints? *}
{+ choice: true false +}
{===>} cmtight=true;

{* Force constant for center of mass restraints *}
{===>} kcont=1.0;
</pre>


#### Surface contact restraints

Define here if you want to use [surface contact restraints](/software/haddock2.4/airs/#random-air-definition-ab-initio-mode){:target="_blank"} and specify the corresponding force constant. This can be useful in combination with random interaction restraints definition (see above).

To activate this type of restraints set *surfrest=true*.

<pre style="background-color:#DAE4E7">
{* Do you want to define surface contact restraints to enforce contact between the molecules? *}
{* Note that these are only active during it0 and it1 *}
{+ choice: true false +}
{===>} surfrest=false;

{* Force constant for surface contact restraints *}
{===>} ksurf=1.0;
</pre>


* * *

### Radius of gyration restraint

A radius of gyration distance restraint can be turned on here. It will be active throughout the entire protocol, but can be effectively turned off by setting the force constant for a given stage to 0. The radius of gyration should be entered in angstrom. By default it is applied to the entire system, but can be restricted to part of the system using standard CNS atom selections.

For example to limit it to chains B and C define: "(segid B or segid C)".

To activate this type of restraints set *rgrest=true* and specify the radius of gyration and the selection to which it applies.


<pre style="background-color:#D2AE4E7"> 
{=========================== radius of gyration restraint  ============}
{* Turn on/off and energy constants for Rg restraints *}
{* Do you want to define a radius of gyration restraint (e.g. from SAXS)? *}
{+ choice: true false +}
{===>} rgrest=false;

{* Radius of gyration *}
{===>} rgtarg=17.78;

{* Force constant for radius of gyration restraint *}
{===>} krg_hot=100.0;
{===>} krg_cool1=100.0;
{===>} krg_cool2=100.0;
{===>} krg_cool3=100.0;

{* Atom selections for the radius of gyration restraint *}
{===>} rgsele="all";
</pre>


* * *

### DNA/RNA restraints

Define here if you want to use DNA/RNA restraints. To use such restraints, edit the _dna-rna-restraints.cns_ file provided in the ***protocols*** directory, adapt it to your particular case, and place it in the ***data/sequence*** directory. This file allows you to define base-pair, backbone dihedral angle and sugar pucker restraints.

To activate this type of restraints set *dnarest_on=true*.

<pre style="background-color:#DAE4E7"> 
{======================DNA-RNA restraints ============================}
{* Use DNA/RNA restraints (dna-rna_restraints.def in data/sequence)? *}
{+ choice: true false +}
{===>} dnarest_on=false;
</pre>



* * *

### Dihedrals angle restraints

If dihedral angle restraints have been defined in the [*run.param*](/software/haddock2.4/docking/#defining-restraints){:target="_blank"} file, turn the flag *dihedrals_on* to true and specify the force constants for the various stages of the semi-flexible simulated annealing (for water the value of _cool3_ will be used).

HADDOCK2.4 offer a new option to automatically dihedral angle restraints from the input structures. By default it is turned off, but you can specify to define dihedral angle restraints for the entire backbone, alpha-helices only or alpha-helices and beta-sheets. The secondary structure elements are defined based on a simple phi/psi dihedral angle criterion and allowed range by +/- *error_dih*

<pre style="background-color:#DAE4E7"> 
{=========================== dihedrals restraints ====================}
{* energy constants *}

{+ choice: true false +}
{===>} dihedrals_on=false;
{===>} dihedrals_hot=5;
{===>} dihedrals_cool1=5;
{===>} dihedrals_cool2=50;
{===>} dihedrals_cool3=200;

{* Automatically define backbone dihedral angle restraints from structure? *}
{* Error treshold for restraint violation is defined by error_dih *}
{+ choice: none all alpha alphabeta +}
{+ define the error treshold for the restraint violation +}
{===>} ssdihed=none;
{===>} error_dih=10;
</pre>



* * *

### Residual Dipolar couplings

If RDC data are available and have been defined in the [*run.param*](/software/haddock2.4/docking/#defining-restraints){:target="_blank"} file, you can define them in this section. Five classes are supported. For each class you can specify the type of restraining energy function:
*   SANI: direct refinement against the dipolar couplings (a tensor will be included in the structures calculations)
*   VANGLE: refinement using intervector projection angle restraints
([Meiler et al. _J. Biomol. NMR_ **17**, 185 (2000)](https://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=10805131&dopt=Abstract){:target="_blank"})

You can specify the first and last stage at which the various RDCs will be used.
*   0: rigid body EM (it0)
*   1: semi-flexible simulated annealing (SA) (it1)
*   2: explicit solvent refinement (water)

This option allows for example to combine VANGLE and SANI type restraints. Intervector projection angle restraints lead to better convergence in the first phase of the docking (0,1) while direct RDC restraints can be used in the final explicit solvent refinement (2) to fine-tune the RDCs (see for details [van Dijk _et al._ _Proteins_, **60**, 367-381 (2005)](https://doi.org/doi:10.1002/prot.20476){:target="_blank"}).

For SANI Da (in Hz) and R (R=Dr/Da) should be specified. You should also specify the force constants for the various stages of the docking protocol:
*   _rdc_hot_: high temperature rigid body dynamics
*   _rdc_cool1_: first rigid body slow cooling SA
*   _rdc_cool2_: second slow cooling SA with flexible side-chains at interface
*   _rdc_cool3_: third slow cooling SA with flexible side-chains and backbone at interface.

<pre style="background-color:#DAE4E7"> 
{=========================== residual dipolar couplings ======================}

{* Parameters *}

{* Number of RDC restraint sets *}
{===>} numrdc=0;

{+ choice: "NO" "SANI" "VANGLE" +}
{===>} rdc_choice_1="NO";
{===>} rdc_firstIt_1=2;
{===>} rdc_lastIt_1=2;
{===>} rdc_hot_1=0.001;
{===>} rdc_cool1_1=0.02;
{===>} rdc_cool2_1=0.2;
{===>} rdc_cool3_1=0.2;
{===>} rdc_r_1=0.057;
{===>} rdc_d_1=-11.49;
{===>} ini_bor_hot_1=1.0;
{===>} fin_bor_hot_1=10.0;
{===>} ini_bor_cool1_1=10.0;
{===>} fin_bor_cool1_1=40.0;
{===>} ini_bor_cool2_1=40.0;
{===>} fin_bor_cool2_1=40.0;
{===>} ini_bor_cool3_1=40.0;
{===>} fin_bor_cool3_1=40.0;
{===>} ini_cen_hot_1=0.25;
{===>} fin_cen_hot_1=2.5;
{===>} ini_cen_cool1_1=2.5;
{===>} fin_cen_cool1_1=10.0;
{===>} ini_cen_cool2_1=10.0;
{===>} fin_cen_cool2_1=10.0;
{===>} ini_cen_cool3_1=10.0;
{===>} fin_cen_cool3_1=10.0;
...
</pre>

For more information on using RDC as restraints for docking see also the [RDC restraints](/software/haddock2.4/RDC){:target="_blank"} section of the online HADDOCK manual.


* * *

### Pseudo contact shifts

If pseudo contact shift data are available and have been defined in the [*run.param*](/software/haddock2.4/docking/#defining-restraints){:target="_blank"} file, you can define them in this section. Ten classes are supported. For each class you can specify the first and last stage at which the various PCS restraints will be used.
*   0: rigid body EM (it0)
*   1: semi-flexible simulated annealing (SA) (it1)
*   2: explicit solvent refinement (water)You should also specify the force constants for the various stages of the docking protocol:
*   _hot_: high temperature rigid body dynamics
*   _cool1_: first rigid body slow cooling SA
*   _cool2_: second slow cooling SA with flexible side-chains at interface
*   _cool3_: third slow cooling SA with flexible side-chains and backbone at interface and the tensor parameters R and D.

For each set of PCS restraints used, a tensor must be defined. Its axial (D) (*pcs_d_X*) and rhombic (R) (*pcs_rd_X*) components must be defined. The proper units for use in HADDOCK should be: 10<sup>-28</sup> / (12*pi) m<sup>3</sup> (which gives a scaling factor of 265.26 compared to values expressed in 10<sup>-32</sup> m<sup>3</sup>.


<pre style="background-color:#DAE4E7"> 
{=========================== pseudo contact shifts ===========================}

{* Number of PCS restraint sets *}
{===>} numpcs=0;

{+ choice: "NO" "XPCS" +}
{===>} pcs_choice_1="NO";
{===>} pcs_firstIt_1=0;
{===>} pcs_lastIt_1=2;
{===>} pcs_hot_1=100.0;
{===>} pcs_cool1_1=100.0;
{===>} pcs_cool2_1=100.0;
{===>} pcs_cool3_1=100.0;
{===>} pcs_r_1=1000;
{===>} pcs_d_1=10000;
...
</pre>

For more information on using diffusion anisotropy as restraints for docking see also the [PCS restraints](/software/haddock2.4/PCS) section of the online HADDOCK manual. Refer to the following publication for details of the implementation in HADDOCK:

C. Schmitz and A.M.J.J. Bonvin, [Protein-Protein HADDocking using exclusively Pseudocontact Shifts.](https://doi.org/doi:10.1007/s10858-011-9514-4){:target="_blank"}, *J. Biomol. NMR*, **50**,  263-266 (2011).


* * *

### Diffusion anisotropy restraints

If [diffusion anisotropy restraints (DANI)](/software/haddock2.4/DANI){:target="_blank"} (from <sup>15</sup>N relaxation measurements) are available and have been defined in the [*run.param*](/software/haddock2.4/docking/#defining-restraints){:target="_blank"} file, you can define them in this section. Five classes are supported (e.g. for measurements at different fields).

You can specify the first and last stage at which the various DANI restraint sets will be used.
*   0: rigid body EM (it0)
*   1: semi-flexible simulated annealing (SA) (it1)
*   2: explicit solvent refinement (water)

For each DANI set, the correlation time (ns) (*dan_tc_X*) , Da (in Hz) (*dan_d_X*) and R (R=Dr/Da) (*dan_r_X*) should be specified, together with the proton (*dan_wh_X*) and nitrogen 15 (*dan_wn_X*) frequencies (MHz). You should also specify the force constants for the various stages of the docking protocol:

*   _hot_: high temperature rigid body dynamics
*   _cool1_: first rigid body slow cooling SA
*   _cool2_: second slow cooling SA with flexible side-chains at interface
*   _cool3_: third slow cooling SA with flexible side-chains and backbone at interface


<pre style="background-color:#DAE4E7"> 
{=========================== relaxation data ======================}
{* Parameters *}

{* Number of DANI restraint sets *}
{===>} numdani=0;

{+ choice: "NO" "DANI" +}
{===>} dan_choice_1="DANI";
{===>} dan_firstIt_1=0;
{===>} dan_lastIt_1=2;
{===>} dan_hot_1=1;
{===>} dan_cool1_1=5;
{===>} dan_cool2_1=10;
{===>} dan_cool3_1=10;
{===>} dan_tc_1=9.771;
{===>} dan_anis_1=1.557;
{===>} dan_r_1=0.455;
{===>} dan_wh_1=599.91;
{===>} dan_wn_1=60.82;
...
</pre>

For more information on using diffusion anisotropy as restraints for docking see also the [DANI restraints](/software/haddock2.4/DANI){:target="_blank"} section of the online HADDOCK manual. Their implementation in HADDOCK is described in [van Dijk _et al._ _J. Biomol. NMR_, **34**, 237-244 (2006)](https://doi.org/doi:10.1007/s10858-006-0024-8){:target="_blank"}.


* * *

### Cryo-EM restraints

If [cryoEM restraints](/software/haddock2.4/cryoEM){:target="_blank"} are available and have been defined in the [*run.param*](/software/haddock2.4/docking/#defining-restraints){:target="_blank"} file, you can define them in this section. HADDOCK relies on the concept of centroids to guide the initial docking and only uses the cryo-EM map once the molecules have been docked using the centroid restraints. The centroids define the most likely position of the center of mass of a molecule into the density. Their positions (x,y,z coordinates) must be defined in this section (the *xcom_X, ycom_X, zcom_X* parameters. Those positions can be for example obtained using our [PowerFit webserver](https://alcazar.science.uu.nlservices/POWERFIT){:target="_blank"}.

If it is unclear which centroid corresponds to which molecule, it is possible to define those as ambiguous by setting *ambi_X=true*. Otherwise define them specifically for each molecule.
If centroids are used, the current implementation expect as many centroids to be defined as there are molecules.


<pre style="background-color:#DAE4E7"> 
{========================== Cryo-EM parameters ============================}

{* Centroid definitions *}
{+ choice: true false +}
{===>} centroid_rest=false;
{===>} centroid_kscale=50.0;

{* Placement of centroids in absolute coordinates *}
{===>} xcom_1=12.3;
{===>} ycom_1=0.8;
{===>} zcom_1=9.2;
...

{* Are the centroid retraints ambiguous *}
{+ choice: true false +}
{===>} ambi_1=false;
{+ choice: true false +}
...
</pre>


To use explicitly the cryo-EM density as a restraint in HADDOCK set *em_rest=true* and define the resolution, number of voxels in each dimension, the length of each dimension.

<pre style="background-color:#DAE4E7"> 
{* Density/XREF restraints *}
{+ choice: true false +}
{===>} em_rest=false;
{===>} em_kscale=15000;
{+ choice: true false +}
{===>} em_it0=true;
{+ choice: true false +}
{===>} em_it1=true;
{+ choice: true false +}
{===>} em_itw=true;

{* Resolution of data in angstrom *}
{===>} em_resolution=10.0;

{* Density parameters *}
{* Number of voxels in each dimension *}
{===>} nx=32;
{===>} ny=32;
{===>} nz=32;

{* Length of each dimension in angstrom *}
{===>} xlength=80.0;
{===>} ylength=80.0;
{===>} zlength=80.0;

{* Cryo-EM scoring weights *}
{===>} w_lcc_0=-400.0;
{===>} w_lcc_1=-10000.0;
{===>} w_lcc_2=-10000.0;
</pre>


For more information on using a cryo-EM map as restraints for docking see also the [cryoEM restraints](/software/haddock2.4/cryoEM) section of the online HADDOCK manual. Their implementation and use in HADDOCK is described in:


* M.E. Trellet, G. van Zundert and A.M.J.J. Bonvin. [Protein-protein modelling using cryo-EM restraints](https://dx.doi.org/10.1007/978-1-0716-0270-6_11){:target="_blank"}. In:  _Structural Bioinformatics. Methods in Molecular Biology_, vol 2112. Humana, New York, NY, (2020). A preprint is available [here](https://arxiv.org/abs/2005.00435){:target="_blank"}.

* G.C.P. van Zundert, A.S.J. Melquiond and A.M.J.J. Bonvin.
[Integrative modeling of biomolecular complexes: HADDOCKing with Cryo-EM data.](https://doi.org/10.1016/j.str.2015.03.014){:target="_blank"}
_Structure._ *23*, 949-960 (2015).


* * *

### Topology and parameters files

In this section the topology, linkage and parameter files are specified for each molecule. The default values are for proteins using the improved parameters of [Linge et al. 2003](https://www3.interscience.wiley.com/cgi-bin/abstract/102523901/START){:target="_blank"} and OPLSX non-bonded parameters.

For DNA and RNA use instead the _dna-rna-allatom-hj-opls-1.3.top_, _dna-rna-allatom-hj-opls-1.3_ and _dna-rna-1.3_ files in the **toppar** directory.


<pre style="background-color:#DAE4E7"> 
{===================== topology and parameter files ======================}

{* topology file for molecule 1 *}
{===>} prot_top_mol1="protein-allhdg5-4.top";
...

{* linkage file for molecule 1 *}
{===>} prot_link_mol1="protein-allhdg5-4-noter.link";
...

{* energy parameter file for molecule 1 *}
{===>} prot_par_mol1="protein-allhdg5-4.param";
...

{* type of non-bonded parameters *}
{* specify the type of non-bonded interaction *}
{+ choice: "PROLSQ" "PARMALLH6" "PARALLHDG" "OPLSX" +}
{===>} par_nonbonded="OPLSX";
</pre>


Also provided in the **toppar** directory are topologies and parameters for heme groups (only heme B and C are supported). 
See for this the _topallhdg.hemes_ and _parallhdg.hemes_ files. Those are read by default and for heme C covalent bonds to the coordinating Histidine are automatically defined.

Parameter and topology files for small ligands should be provided by the user and place in the ***toppar*** directory or each run (see also the [FAQ](/software/haddock2.4/faq) section of the online manual). Those files are also read by default.

Ions should be automatically recognized provided their naming is consistent with what is defined in the _ion.top_ topology file in the ***toppar*** directory. For the torsion angle dynamics part of the [docking protocol](/software/haddock2.4/docking){:target="_blank"} (it1), a covalent bond will be automatically defined to the closest ligand atom (only for cations). This is done in the _covalions.cns_ CNS script in the ***protocols*** directory. The list of supported ions can be found [here](https://wenmr.science.uu.nl/haddock2.4/library){:target="_blank"}.


* * *

### Coarse grained topology and parameters files

In this section the topology, linkage and parameter files are specified in case coarse graining is used. The implementation is based on the [Martini](https://cgmartini.nl){:target="_blank"} force field.

For DNA and RNA use instead the _dna-rna-CG-MARTINI-2-1p.top_, _dna-rna-CG-MARTINI-2-1p_ and _dna-rna-CG-MARTINI-2-1p_ files in the **toppar** directory.


<pre style="background-color:#DAE4E7"> 
{============coarse graining topology and parameter files ==================}

{* topology file for molecule 1 *}
{===>} prot_cg_top_mol1="protein-CG-Martini-2-2.top";
...

{* linkage file for molecule 1 *}
{===>} prot_cg_link_mol1="protein-CG-Martini-2-2.link";
...

{* energy parameter file for molecule 1 *}
{===>} prot_cg_par_mol1="protein-CG-Martini-2-2.param";
...
</pre>

Details of the implementation in HADDOCK can be found in the following publications:

* R.V. Honorato, J. Roel-Touris and A.M.J.J. Bonvin. [MARTINI-based protein-DNA coarse-grained HADDOCKing](https://doi.org/10.3389/fmolb.2019.00102){:target="_blank"}. _Frontiers in Molecular Biosciences_, *6*, 102 (2019).

* J. Roel-Touris, C.G. Don, R.V. Honorato, J.P.G.L.M Rodrigues and A.M.J.J. Bonvin. [Less is more: Coarse-grained integrative modeling of large biomolecular assemblies with HADDOCK](https://doi.org/10.1021/acs.jctc.9b00310){:target="_blank"}. _J. Chem. Theo. and Comp._, *15*, 6358-6367 (2019).


* * *

### Energy and interaction parameters

You can define in this section a number of parameters that control the electrostatic energy term during the docking process, that allow you to scale down the intermolecular interactions and sample 180 degrees rotated solutions.

#### Electrostatic treatment

The electrostatic energy term can be turned on or off for the first two stages of the docking, namely the [rigid body minimization](/software/haddock2.4/docking#mini) and the [semi-flexible simulated annealing](/software/haddock2.4/docking#sa). Two implementations are now supported to describe the solvent implicitly:
*   constant dielectric
*   distance dependent dielectric. The _epsilon_ constant should be defined.


<pre style="background-color:#DAE4E7"> 
{===================== energy and interaction parameters ==================}

{ Do you want to include dihedral angle energy terms? }
{ choice: true false }
dihedflag=true;

{* Do you want to include the electrostatic energy term for docking? *}
{* Note that it will be automatically included in the solvent refinement *}

{* Include electrostatic during rigid body docking (it0)? *}
{+ choice: true false +}
{===>} elecflag_0=true;

{* Give the epsilon constant for the electrostatic energy term in it0 *}
{===>} epsilon_0=10.0;

{* Use constant (cdie) or distance-dependent (rdie) dielectric in it0? *}
{+ choice: cdie rdie +}
{===>} dielec_0=rdie;

{* Include electrostatic during semi-flexible SA (it1)? *}
{+ choice: true false +}
{===>} elecflag_1=true;

{* Give the epsilon constant for the electrostatic energy term in it1 *}
{===>} epsilon_1=1.0;

{* Use constant (cdie) or distance-dependent (rdie) dielectric in it0? *}
{+ choice: cdie rdie +}
{===>} dielec_1=rdie;
...
</pre>


For the final stage, the [explicit solvent refinement](/software/haddock2.4/docking#water), a constant dielectric with an epsilon equal to one is used by default.



#### Scaling of intermolecular interactions

This section also allows you to specify scaling factors for the various stages of the docking:
*   rigid body EM
*   rigid body dynamic: high temperature and slow cooling SA rigid body dynamics
*   second slow cooling SA with flexible side-chains at interface
*   third slow cooling SA with flexible side-chains and backbone at interfaceThese scaling factors only affect the intermolecular van der Waals and electrostatic energy terms.


<pre style="background-color:#DAE4E7"> 
{* Scaling of intermolecular interactions for rigid body EM*}
{===>} inter_rigid=1.0;

{* Scaling of intermolecular interactions for semi-flexible SA*}
{+ table: rows=3 "Rigid body dynamic " "SA with flexible side-chains (cool2)" "SA with flexible backbone and side-chains (cool3)"
          cols=2 "Init value" "Final value" +}
{===>} init_rigid=0.001;
{===>} fin_rigid=0.001;
{===>} init_cool2=0.001;
{===>} fin_cool2=1.0;
{===>} init_cool3=0.05;
{===>} fin_cool3=1.0;
...
</pre>

**Note:**  It might be useful to scale down the intermolecular interactions during rigid-body docking in cases where a ligand has to penetrate in a deep and (partly) buried pocket of a protein. A value of 0.01 should already be sufficient for this.



#### Interaction matrix for non-bonded interactions

This option in HADDOCK2.4 allows to scale down or turn off interactions between specific molecules. It is useful for example in the context of ensemble-averaged docking where the distance restraints should be averaged over multiple binding poses, but the multiple copies of one molecule should not see each other. 


<pre style="background-color:#DAE4E7"> 
{* Interaction matrix for non-bonded interactions*}
{===>} int_1_1=1.0;
{===>} int_1_2=1.0;
{===>} int_1_3=1.0;
{===>} int_1_4=1.0;
{===>} int_1_5=1.0;
{===>} int_1_6=1.0;
{===>} int_1_7=1.0;
{===>} int_1_8=1.0;
...
</pre>


This option has been applied for example in ensemble-averaged docking of a peptide using PRE-derived distance restraints. See:

E. Escobar-Cabrera, Okon, D.K.W. Lau, C.F. Dart, A.M.J.J. Bonvin and L.P. McIntosh, [Characterizing the N- and C-terminal SUMO interacting motifs of the scaffold protein DAXX.](https://doi.org/doi:10.1074/jbc.M111.231647){:target="_blank"}, *J. Biol. Chem.*, **286**, 19816-19829 (2011).


* * *

### Number of structures to dock

The docking process is performed in three distinct steps:
1.  [rigid body minimization](software/haddock2.4/protocol/#randomization-of-starting-orientations-and-rigid-body-energy-minimization){:target="_blank"} (it0)
2.  [semi-flexible simulated annealing](/software/haddock2.4/protocol/#semi-flexible-simulated-annealing){:target="_blank"} (it1)
3.  [final refinement](/software/haddock2.4/protocol/#flexible-final-refinement){:target="_blank"} (water)

You can define here the number of structures to generate in the first two steps and the number of structures to analyze.


<pre style="background-color:#DAE4E7"> 
{===================== Number of structures to dock =======================}
{* Setting for the rigid-body (it0) and semi-flexible refiment (it1) *}

{* number of structures for rigid body docking *}
{===>} structures_0=1000;
       keepstruct_0=&structures_0;
{* number of structures for refinement *}
{===>} structures_1=200;
       keepstruct_1=&structures_1;
       keepstruct_2=&structures_1;
{* number of structures to be analysed*}
{===>} anastruc_1=200;
       anastruc_0=&anastruc_1;
       anastruc_2=&anastruc_1;
...
</pre>


#### Sampling of 180 degrees-rotated solutions

This option allows to sample 180 degrees-rotated solutions at both the rigid-body and semi-flexible docking stages. If turned on (default for rigid-body stage), for each model generated, a 180 degree rotated solution will be generated automatically by HADDOCK and either energy minimized (rigid-body) or submitted to the semi-flexible refinement protocol (it1). The rotation axis is automatically defined from the vector connecting the center of masses of the two interfaces, each interface being defined by all residues forming intermolecular contacts within 5A (this cutoff is defined in the *rotation180.cns* CNS script in the ***protocols*** directory.

Sampling of 180 degree rotated solutions in the rigid-body stage clearly improve the docking performance. If turned on during the semi-flexible refinement, both refined solutions will be written to disk, doubling the effective number of structures.


<pre style="background-color:#DAE4E7"> 
{* Sampling of symmetry related solutions                       *}

{* Sample 180 degrees rotated solutions during rigid body EM?   *}
{+ choice: true false +}
{===>} rotate180_it0=true;

{* Sample 180 degrees rotated solutions during semi-flexible SA?*}
{+ choice: true false +}
{===>} rotate180_it1=false;
</pre>


**Note 1:** The sampling of 180 degree-rotated solutions in the semi-flexible refinement is not advised since it might lead to unrealistic structures (e.g. with knots!). If used, carefully check the resulting structures for artifacts.

**Note 2:** If solvated docking (see below) is turned on, then the sampling of 180 degree-rotated solutions will be automatically turned off during the calculations.



* * *

### DOCKING protocol

Here you can define parameters that control the starting point for the docking and the rigid body and semi-flexible refinement [stages](software/haddock2.4/protocol){:target="_blank"} of the docking.


#### Starting point for the docking

This section allows you to control various starting setting:

* How the various starting models are combined (*crossdock*) in the case when an ensemble of conformations is given to HADDOCK (should be turned off for example if you only want to perform water refinement of a preformed complex)
* Randomization of the starting orientations or not (*randorien*)
* Expansion of the initial complex (to be used only for refinement purposes) (*expand*). This is a new option in HADDOCK2.4, which will take a complex, and expand it by translating each molecule along the axis defined by its center of mass and the overall center of mass of the complex. The amount of translation is expressed in a percentage (*expansion*). A random rotation can also be applied to each molecule (*ranangle*).
* Rebuilding of missing side-chains in the context of the complex (*rebuildcplx*) (only for refinement of an existing complex)

**Note** that the expansion refinement protocol is still experimental and as such has not been thoroughly tested.



<pre style="background-color:#DAE4E7"> 
{=========================== DOCKING protocol =============================}
{* Cross-dock all combinations in the ensembles of starting structures? *}
{* Turn off this option if you only want to dock structure 1 of ensemble A *}
{*   to structure 1 of ensemble B, structure 2 to structure 2, etc. *}
{+ choice: true false +}
{===>} crossdock=true;

{* Randomize starting orientations? *}
{+ choice: true false +}
{===>} randorien=true;

{* Expand starting orientations? *}
{+ choice: true false +}
{===>} expand=false;

{* Expansion percentage *}
{===>} expansion=0.4;

{* Random rotation angle *}
{===>} randangle=6;

{* Rebuild missing atoms in the context of the complex? (refinement mode) *}
{+ choice: true false +}
{===>} rebuildcplx=false;
...
</pre>


#### Rigid body minimization settings

This section allows you to turn on and off the rigid body minimization step. It also allows to turn off translation which can be useful when docking highly flexible small molecules and letting the docking occur during the flexible refinement stage, a protocol we have used in the past for docking flexible oligosaccharides. Use with care though!

You can also define here the **number of trials** for each starting configuration. This is done internally in CNS and only the best solution (according to the defined scoring function) will be written to disk. Note that each docked solution will also undergo the 180 rotation protocol if turned on (default for the rigid body minimization).
This option saves disk space, but the scoring scheme should be robust otherwise you might miss good solutions. For example, if you intend to optimize the scoring function for the rigid body docking it is better to write out all models.

The remaining parameter is this section is the random see used by the CNS random number generator.


<pre style="background-color:#DAE4E7"> 
{* Perform initial rigid body minimisation? *}
{+ choice: true false +}
{===>} rigidmini=true;

{* Allow translation in rigid body minimisation? *}
{+ choice: true false +}
{===>} rigidtrans=true;

{* Number of trials for rigid body minimisation? *}
{===>} ntrials=5;

{* initial seed for random number generator *}
{* change to get different initial velocities *}
{===>} iniseed=917;
</pre>


#### Semi-flexible refinement settings

In this section you can control the parameters the govern the semi-flexible simulated annealing protocol. You can define the start and end temperatures and the number of integration steps for the various stages of the annealing protocol (see [the docking protocol](/software/haddock2.4/protocol) section){:target="_blank"}.


<pre style="background-color:#DAE4E7"> 
{* temperature for rigid body high temperature TAD *}
{===>} tadhigh_t=2000;

{* initial temperature for rigid body first TAD cooling step *}
{===>} tadinit1_t=2000;

{* final temperature after first cooling step *}
{===>} tadfinal1_t=500;

{* initial temperature for second TAD cooling step with flexible side-chain at the inferface *}
{===>} tadinit2_t=1000;

{* finale temperature after second cooling step *}
{===>} tadfinal2_t=50;

{* initial temperature for third TAD cooling step with fully flexible interface *}
{===>} tadinit3_t=1000;

{* finale temperature after third cooling step *}
{===>} tadfinal3_t=50;

{* time step *}
{===>} timestep=0.002;

{* factor for timestep in TAD *}
{===>} tadfactor=8;

{* Number of EM steps for translational minimisation? *}
{===>} emstepstrans=1000;

{* number of MD steps for rigid body high temperature TAD *}
{===>} initiosteps=500;

{* number of MD steps during first rigid body cooling stage *}
{===>} cool1_steps=500;

{* number of MD steps during second cooling stage with flexible side-chains at interface *}
{===>} cool2_steps=1000;

{* number of MD steps during third cooling stage with fully flexible interface *}
{===>} cool3_steps=1000;
</pre>


**Note:** If solvated docking is turned on, then the number of MD steps for the rigid body stages of the semi-flexible refinement (high temperature rigid-body TAD and slow cooling annealing) will automatically be set to 0.



* * *

### Solvated docking

In this section you can turn on solvated docking. If turned on, the initial structures will first be solvated in a shell of TIP3P water (only water molecules within 5.5 A of the protein will be kept). The rigid-body docking will thus be performed from solvated proteins. Two methods for dealing with interfacial waters are implemented:

*   **database-based (db)** (_recommended upon restrained solvated docking_ (see below)): Interfacial water molecules will be removed in a biased Monte Carlo process until a user-defined fraction of water remain. This process can make use of two different propensity scales:

    *   propensities of finding water-mediated contacts between amino-acid pairs defined from a _statistical analysis of high-resolution crystal structures_. The water-mediated contact propensities can be found in the _db_statistical.dat_ CNS script in the ***protocols*** directory.

    For details see:

    A.D.J. van Dijk and A.M.J.J. Bonvin. [Solvated docking: introducing water into the modelling of biomolecular complexes.](https://doi.org/doi:10.1093/bioinformatics/btl395){:target="_blank"} *Bioinformatics*, **22**, 2340-2347 (2006).

    *   propensities of finding water-mediated contacts between amino-acid pairs defined from the _Kyte-Doolittle hydrophobicity scale_. The corresponding water-mediated contact propensities can be found in the _db_kyte-doolittle.dat_ CNS script in the ***protocols*** directory.


    For details see:

    P.L. Kastritis, K.M. Visscher, A.D.J. van Dijk and A.M.J.J. Bonvin. [Solvated docking using Kyte-Doolittle-based water propensities.](https://doi.org/doi:10.1002/prot.24210){:target="_blank"}, *Proteins: Struc. Funct. & Bioinformatic*, **81**, 510-518 (2013).

An important parameter to be defined for database-solvated docking is the **fraction of interfacial water** to be kept after the Monte Carlo removal process. This is currently set to 50% based on our analysis of water-mediated contacts. New in HADDOCK2.4, this percentage can now be defined separately for nucleic acids (currently 75%). This is coming from the observation that nucleic acids show typically higher solvation. For details regarding nucleic acids solvated docking see:

M. van Dijk, K. Visscher, P.L. Kastritis and A.M.J.J. Bonvin. [Solvated protein-DNA docking using HADDOCK.](https://doi.org/doi:10.1007/s10858-013-9734-x){:target="_blank"}, *J. Biomol. NMR*, **56**, 51-63 (2013).

Note that typically less than that (or even none) of the water molecules will be kept since an energy cut-off is applied after the Monte Carlo water removal step: all waters with unfavorable interaction energies (Evdw+Eelec>0) are removed. In some cases, this allows all interfacial waters to be removed at the end. The energy cutoff is defined in the _db1.cns_ CNS script in the ***protocols*** directory.

*   **restrained solvating (restraints)**: in this approach, water molecules are restrained to be at proximity of amino-acids found to form the most water-mediated contacts (arg, asn, asp, gln, glu, his, lys, pro, ser, thr and tyr). This is done by defining ambiguous distance restraints between each water and highly solvated amino-acids on both side on an interface. ***Note that this method has not been thoroughly tested***.

    If _restrained solvating_ is chosen, three additional parameters should be set:

    *   **initial distance cutoff**: all water molecules further away from a highly solvated amino-acid will be removed in the solvent shell generation step.
    *   **initial distance cutoff**: upper distance restraints for the definition of ambiguous water-amino-acid restraints.
    *   **force constant** for water-amino-acid distance restraints.

Another parameters that can be modified is the **water-protein surface cut-off** used to remove water molecules that are remote from the interface (a water must be with this cut-off distance from two chains to be kept).

It is also possible to turn off **water translation** during rigid-body energy minimization if desired.

Finally, to increase sampling, it is possible to start the docking from differently solvated molecules. The **number of initial solvation shells** can be define here. If more than 1 is defined, the protein will be randomly rotated and a new solvation shell will be generated.


<pre style="background-color:#DAE4E7"> 
{======================= Solvated rigid body docking=======================}
{* perform solvated docking ? *}
{+ choice: true false +}
{===>} waterdock=false;

{* which method to use for solvating? *}
{* db: database-based (recommended), restraints: for restrained solvating to amino-acid most often forming
water mediated contacts and blank (""): for uniform waterlayer *}
{+ choice: "db" "restraints" "" +}
{===>} solvate_method="db";

{* which propensity database to use? *}
{* statistical: based on an analysis of water-mediated contacts in the PDB, kyte-doolittle: based on the Kyte-Doolittle hydrophobicity scalte *}
{+ choice: "statistical" "kytedoolittle" +}
{===>} db_method="kytedoolittle";

{* initial cutoff for restraints solvating method *}
{* all waters further away from a highly occuring water solvated residue will be removed in the generation
of the initial solvation shell *}
{===>} water_restraint_initial=5.0;

{* cutoff for restraints solvating method *}
{* upper distance limit for defining distance restraints between water and amino-acids often found to be
involved in water-mediated contacts *}
{===>} water_restraint_cutoff=5.0;

{* force constant for restrainted solvating method *}
{===>} water_restraint_scale=25.0;

{* fraction of water to keep *}
{* this is the fraction of all interface water after the initial rigid body docking that will be kept
(note that more waters might be removed if the interaction energy is unfavorable  *}
{===>} water_tokeep=0.50;

{* fraction of water around DNA to keep *}
{* this is the fraction of interface water involving DNA phoshpates after the initial rigid body docking that will be kept
(note that more waters might be removed if the interaction energy is unfavorable  *}
{===>} dnap_water_tokeep=0.75;

{* random fraction to be added to the fraction of water to keep *}
{===>} water_randfrac=0.0;

{* water-protein surface-cutoff *}
{* waters further away than this cutoff distance from any component of the complex will be removed *}
{===>} water_surfcutoff=8.0;

{* do some water analysis *}
{+ choice: true false +}
{===>} water_analysis=false;

{* allows translation of water molecules during rigid-body docking, true or false: *}
{+ choice: true false +}
{===>} transwater=true;

{* number of different initial solvation shells to generate *}
{===>} waterensemble=1;
</pre>


* * *

### Final explicit solvent refinement

In this section you can define if the final refinement (/software/haddock2.4/protocol) should be performed (recommended since it does improve the docking solutions), with or without (default in 2.4) explicit solvation shell and on how many structures. Two solvent models are currently supported: water and DMSO. DMSO is a fair mimic for a membrane environment.

You can also specify here the number of MD integration steps for the heating, sampling and cooling phases of the explicit solvent refinement.

You can also specify to keep the solvent, in which case two additional PDB files will be created in the ***structures/it1/water*** directory with _h2o.pdb_ and _h2o-inter.pdb_ extensions. The first one contains the entire solvation shell, the second one only the interfacial solvent molecules.


<pre style="background-color:#DAE4E7"> 
{==================== final explicit solvent refinement  ==================}
{* Do you want to refine your docking models in explicit solvent? *}
{+ choice: "yes" "no" +}
{===>} firstwater="yes";

{* Build explicit solvent shell? (Can be turned off the large molecules or when morphing CG to AA models) *}
{* Only EM will then be performed                                                                         *}
{+ choice: true false +}
{===>} solvshell=false;

{* Which solvent do you want to use? *}
{+ choice: "water" "dmso" +}
{===>} solvent="water";

{* number of structures for the explicit solvent refinement *}
{* the n best structures will be refined                    *}
{===>} waterrefine=200;
       structures_2=&waterrefine;

{* number of steps for heating phase (100, 200, 300K)?      *}
{===>} waterheatsteps=100;

{* number of steps for 300K sampling phase?                 *}
{===>} watersteps=1250;

{* number of steps for cooling phase (300, 200, 100K)?      *}
{===>} watercoolsteps=500;

{* write additional PDB files including solvent ?           *}
{+ choice: true false +}
{===>} keepwater=false;
</pre>



* * *

### Scoring

In this section you can define individual weigths for the various terms used for the scoring. This can be done separately for the various docking stages (rigid body (it0), semi-flexible refinement (it1) and explicit solvent refinement(water)). You can also define the number of structures to analyze after the simulated annealing and explicit solvent refinement.

HADDOCK offers a fully flexible scoring scheme since the weight of the various energy terms can be defined separately for each phase of the docking. For details about the scoring refer to the [scoring section](/software/haddock2.4/scoring){:target="_blank"} of the HADDOCK2.4 manual.

In this section, you can also define a "skipping" parameter that allows you to sample more solutions from the rigid body EM docking (it0). If the value _x_ of this _skip_ parameter is larger than 0 then every _(x+1)th_ structure from it0 starting from the first structure will be further refined in the semi-flexible simulated annealing.

For example, if skip=1 and 200 structures should be refined in the semi-flexible simulated annealing, structures 1,3,5,7,... and 399 from the best 400 of it0 will be selected and written to the _file.nam_, _file.list_ and _file.cns_ files in the **structures/it0** directory. Three additional files (_file.nam_all_, _file.list_all_ and _file.cns_all_) containing the original sorting of all structures will be created.


<pre style="background-color:#DAE4E7"> 
{================================ Scoring =================================}
{* Settings for the scoring of the docking solutions *}

{* Define the weights for the various terms for the sorting of structures (scoring) *}
{+ table: rows=15 "Evdw" "Eelec" "Eair" "Erg" "Esani" "Exrdc" "Expcs" "Edani" "Evean" "Ecdih" "Esym" "Ezres" "BSA" "dEint" "Edesolv"
          cols=3 "Rigid body EM" "semi-flexible SA" "Water refinement" +}
{===>} w_vdw_0=0.01;
{===>} w_vdw_1=1.0;
{===>} w_vdw_2=1.0;

{===>} w_elec_0=1.0;
{===>} w_elec_1=1.0;
{===>} w_elec_2=0.2;

{===>} w_dist_0=0.01;
{===>} w_dist_1=0.1;
{===>} w_dist_2=0.1;

{===>} w_rg_0=0.1;
{===>} w_rg_1=1.0;
{===>} w_rg_2=1.0;

{===>} w_sani_0=0.1;
{===>} w_sani_1=0.1;
{===>} w_sani_2=0.1;

{===>} w_xrdc_0=0.1;
{===>} w_xrdc_1=0.1;
{===>} w_xrdc_2=0.1;

{===>} w_xpcs_0=0.1;
{===>} w_xpcs_1=0.1;
{===>} w_xpcs_2=0.1;

{===>} w_dani_0=0.01;
{===>} w_dani_1=0.1;
{===>} w_dani_2=0.1;

{===>} w_vean_0=0.1;
{===>} w_vean_1=0.1;
{===>} w_vean_2=0.1;

{===>} w_cdih_0=0.0;
{===>} w_cdih_1=0.0;
{===>} w_cdih_2=0.0;

{===>} w_sym_0=0.1;
{===>} w_sym_1=0.1;
{===>} w_sym_2=0.1;

{===>} w_zres_0=0.1;
{===>} w_zres_1=0.1;
{===>} w_zres_2=0.1;

{===>} w_bsa_0=-0.01;
{===>} w_bsa_1=-0.01;
{===>} w_bsa_2=0.0;

{===>} w_deint_0=0.0;
{===>} w_deint_1=0.0;
{===>} w_deint_2=0.0;

{===>} w_desolv_0=1.0;
{===>} w_desolv_1=1.0;
{===>} w_desolv_2=1.0;

{* It is possible to skip structures in the selection of structure in it0 *}
{* Give for this the number of structures to skip: *}
{===>} skip_struc=0;
</pre>


* * *

### Analysis and clustering

Version 2.4 of HADDOCK offers three options for the analysis (*runana*):

* No analysis at all (can be used to limit the running time)
* Only clustering
* Full analysis

<pre style="background-color:#DAE4E7">
{======================= analysis and clustering ==========================}
{* Full or limited analysis of results? *}
{+ choice: "full" "cluster" "none" +}
{===>} runana="cluster";
</pre>


#### Clustering

If clustering or full analysis are selected, HADDOCK will cluster the solutions are clustered. Two options for clustering are offered:

*   RMSD-based clustering using the ***tools/cluster_struc*** program (a small C++ program that needs to be compiled during [installation](/software/haddock2.4/installation){:target="_blank"}). *cluster_struc* reads the output of the rmsd.inp CNS analysis script that generates the pairwise rmsd matrix over all structures analyzed and perform clustering. The RMSDs are calculated on the interface residues of the second molecule after fitting on the interface residues of the first molecule, what can be termed: interface-ligand-RMSD. The interface residues are automatically defined based on an analysis of all contacts found in all analysed models. Note that RMSD clustering might not be very discriminative in case of multibody docking.

*   Fraction of native contacts (FCC) clustering (default) using the ***tools/cluster_fcc.py*** python script. This option does not require a-priori fitting of the structures, is more robust for multibody docking and much faster than RMSD-based clustering. For details see:

J.P.G.L.M. Rodrigues, M. Trellet, C. Schmitz, P.L. Kastritis, E. Karaca, A.S.J. Melquiond and A.M.J.J. Bonvin, [Clustering biomolecular complexes by residue contacts similarity.](https://doi.org/doi:10.1002/prot.24078){:target="_blank"}, *Proteins: Struc. Funct. & Bioinformatic*, **80**, 1810-1817 (2012).

For this clustering step you need to specify a clustering cut-off and a minimum cluster size (recommended 4). The recommended cutoffs for clustering are:

* RMSD clustering: 7.5A, which works fine in most cases, while this value should be reduced to 5A or less for short peptides and 2 to 1A for small ligand docking. 

* FCC clustering: 0.60 is recommended.

The FCC clustering offers the option to ignore chains when dealing with symmetrical oligomers. For example for a symmetrical trimer, this means that the ABC and ACB arrangements will cluster is the same cluster.

<pre style="background-color:#DAE4E7">
{* Clustering method (RMSD or Fraction of Common Contacts (FCC)) *}
{+ choice: "RMSD" "FCC" +}
{===>} clust_meth="FCC";

{* RMSD cutoff for clustering? (Recommended values: RMSD 7.5, FCC 0.60) *}
{===>} clust_cutoff=0.60;

{* Minimum cluster size? *}
{===>} clust_size=4;

{* Chain-Agnostic Algorithm (used for FCC clustering in symmetrical complexes) *}
{+ choice: "true" "false" +}
{===>} fcc_ignc=false;
</pre>


#### Full analysis

When full analysis is selected HADDOCK will perform a number of additional analysis as described in the [analysis](/software/haddock2.4/analysis){:target="_blank"} section, generating various files in ***it1/analysis*** and ***it1/water/analysis*** containing statistics about energetics, violations of restraint, intermolecular hydrogen bonds and intermolecular hydrophobic contacts. Refer to the [Analysis](/software/haddock2.4/analysis){:target="_blank"} section for more detail and instruction on how to perform further manual analysis of the results.

In *run.cns* you can define the cut-off distances in Angstrom to define a hydrogen bond and a hydrophobic contact. Note that the hydrogen bond detection is only based on a distance criterion.

<pre style="background-color:#DAE4E7">
{* Cutoff distance (proton-acceptor) to define an hydrogen bond? *}
{===>} dist_hb=2.5;

{* Cutoff distance (carbon-carbon) to define an hydrophobic contact? *}
{===>} dist_nb=3.9;
</pre>


* * *

### Cleaning

Since HADDOCK generates a lot of data and output files, there is a cleaning option. If turned on (default) all (except for the first structure of each stage) job, input and output files for the rigid-body, semi-flexible refinement and final refinement will be removed automatically upon completion. This saves a significant amount of space.

<pre style="background-color:#DAE4E7">
{======================= final clean-up ===================================}
{* Clean up the run directory after completion (only files for struct #1 are kept) ? *}
{+ choice: true false +}
{===>} cleanup=true;
</pre>


* * *

### Parallels jobs

In this section you can define the way the structure calculation will be run, and the location of the [CNS](https://cns.csb.yale.edu){:target="_blank"} executable. 
10 nodes or queues can be specified, but typically only one set of parameters is required.

<pre style="background-color:#DAE4E7">
{============================ parallel jobs ===============================}
{* How many nodes do you want to use in parallel? *}
{* leave unused fields blank, make sure that the queues are actually running *}
{+ table: rows=10 "1" "2" "3" "4" "5" "6" "7" "8" "9" "10"
 cols=3 "queue command" "cns executable" "number of jobs" +}

{===>} queue_1="/bin/csh";
{===>} cns_exe_1="/opt/nmr/cns_solve_1.31-UU/mac-intel-darwin/bin/cns";
{===>} cpunumber_1=4;

{===>} queue_2="";
{===>} cns_exe_2="";
{===>} cpunumber_2=0;
...
</pre>


If you are going to run HADDOCK on a multi-processor computer (or node) with for example 24 CPUs, the entries for the first row could be:
*   queue command: _csh_ (this will run the jobs in background on the local computer)
*   cns executable: _.../software/bin/cns_  (the exact path to the CNS executable)
*   number of jobs: _24_ (24 jobs in parallel)and all other entries empty.

If you are using a batch/queuing system (e.g. Torque or Slurm) that distribute the jobs on various linux clusters. The entry for this setup could be:
*   queue command: _qsub_ (or _sbatch_ for Slurm)
*   cns executable: _.../software/bin/cns_  (the exact path to the CNS executable)
*   number of jobs: _100_ (100 jobs will be submitted to the batch system)

**Note:** When using a batch system you should set *useLongJobFileNames = 1* in your HADDOCK installation by editing the *Haddock/Main/UseLongFileNames.py* file, and/or use a wrapper script for submission that will add information about the run directory. See the [FAQ](/software/haddock2.4/faq){:target="_blank"} section of the manual for example wrapper scripts.

* * *
