---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
title: HADDOCK2.4 manual - the docking protocol
image:
  feature: pages/banner_software.jpg
---

The entire docking protocol in HADDOCK consists of five stages:

* table of contents
{:toc}


<hr>

## Topologies and structures generation 

#### Generation of all atoms topologies and coordinates for each molecule separately

The first step in HADDOCK in the generation of the CNS topologies and coordinates files for the various molecules and for the complex from the input PDB files. HADDOCK should automatically recognize chain breaks, disulphide bonds, cis-prolines, d-amino acids and even ions provided they are named as defined in the ion.top topology file located in the ***toppar*** directory. A number of modified amino acids is also supported. Those should be defined with the proper residue naming in the input PDB files. Refer for the list of supported modified amino acids to the [online page](ADD LINK) on the HADDOCK2.4 webserver.

First the topologies will be generated for each molecule separately and all missing atoms in the input PDB files will be generated. For each input structure

Job files will be generated in the ***run*** directory and the topologies, structures and output files will be generated in the ***begin*** directory. HADDOCK will use the fileroot names specified in the [*run.cns*](/software/haddock2.4/run) file by the `prot_root_molX` variable for each molecule and `fileroot` for the complex.  

The following scripts will be run:  

*   *__fileroot_generate_X.job__*: Generates the CNS topology and coordinates file(s) (if starting from an ensemble) for the various molecules (X indicated the molecule number).  

The correspond output files are:  

*   *__prot_root_molX.psf__*: topology file
*   *__prot_root_molX.pdb__*: coordinates file
*   *__prot_root_molX_1.pdb, prot_root_molX_2.pdb__* ...: coordinate files when starting from an ensemble of models
*   *__file_X.list__*: list of PDB coordinates files  
*   *__file_X.nam__*: list of PDB coordinates files  

CNS scripts called (depending on the options defined):  

*   *__generate_X.inp__*
    *   *__initialize.cns__*: 	Initialize the iteration variable
    *   *__iterations.cns__*: 	Defines the iteration variable
    *   *__run.cns__*: 			Reads in all parameter settings for the run
    *   *__build-missing.cns__*: Builds all missing atoms
    	*	*__flex_segment_back.cns__*: Defines semi-flexbible segments
    *   *__prot_break.cns__*: 	Detects chain breaks in the protein
    *   *__dna_break.cns__*: 	Detects chain breaks in nucleic acids
    *   *__covalheme.cns__*: 	Detects covalent bonds for heme groups
    *   *__coval-ace-cys.cns__*: Detects a cyclic structure connecting an acetylated N-ter to a cysteine
    *   *__auto-his.cns__*: 	Automatically defines the protonation state of histidines.

**Note:** If solvated docking is turned on, *generate-water_X.inp* will be used instead, which calls in addition *generate_water.cns,rotate_pdb.cns* and generates additional output pdb files containing the water (*prot_root_molX_1_water.pdbw, ...*)  



#### Generation of coarse grained topologies and coordinates for each molecule separately

This will only be performed if the coarse-graining option is turned on. In that case the following scripts will be run:  

*   *__fileroot_generate-cg_X.job__*: Generates the coarse grained CNS topology and coordinates file(s) (if starting from an ensemble) for the various molecules (X indicated the molecule number).  

The correspond output files in the `begin` directory are:  

*   *__prot_root_molX.psf__*: topology file
*   *__prot_root_molX.pdb__*: coordinates file
*   *__prot_root_molX_1.pdb, prot_root_molX_2.pdb__* ...: coordinate files when starting from an ensemble of models
*   *__file_X.list__*: list of PDB coordinates files  
*   *__file_X.nam__*: list of PDB coordinates files  

Note that the all atoms topologies and file are created into the `begin-aa` directory when coarse graining is turned on.

CNS scripts called (depending on the options defined):  

*   *__generate_X.inp__*
    *   *__initialize.cns__*: 	Initialize the iteration variable
    *   *__iterations.cns__*: 	Defines the iteration variable
    *   *__run.cns__*: 			Reads in all parameter settings for the run
    *   *__patch-types-cg.cns__*: Defines secondary structure-specific beads type based on the encoding in the B-factor column in the input coarse grained PDB files.
    *   *__patch-bb-cg.cns__*: Defines secondary structure-specific backbone angles based on the encoding in the B-factor column in the input coarse grained PDB files.
    *   *__charge-beads-interactions.cns__*: Turns off vdw interactions for the fake charged beads; turns off electrostatic interactions between the fake charges beads within one residue
    *   *__prot_break.cns__*: 	Detects chain breaks in the protein
    *   *__dna_break.cns__*: 	Detects chain breaks in nucleic acids
    *   *__patch-breaks-cg-dna__*: 	Detects covalent bonds for heme groups
    *	*__flex_segment_back.cns__*: Defines semi-flexbible segments



#### Generation of topologies and starting coordinates for the complex

Once the individual topologies and PDB files have been generated, these will be merged to generate the starting models of the complex.

The following scripts will be run:  

*   *__fileroot_generate_complex.job__*: Generates the CNS topology and coordinates file(s) for the complex by merging the various topologies and coordinates files. When starting from ensembles, all combinations will be generated.  

Output files:  

*   *__fileroot.psf__*: topology file
*   *__fileroot.pdb__*:	coordinates file
*   *__fileroot_1.pdb, fileroot_2.pdb__*, ... : coordinates files when starting from an ensemble of structures
*   *__file.cns, file.list, file.nam__*: list of PDB coordinates files 

CNS scripts called:  

*   *__generate_complex.inp__*
    *   *__initialize.cns__*: 	Initialize the iteration variable
    *   *__iterations.cns__*: 	Defines the iteration variable
    *   *__run.cns__*: 			Reads in all parameter settings for the run
    *   *__rebuild-unknown.cns__*: Rebuilds missing atoms in the context of the complex (if turned on for refinement mode).


**Note:** If solvated docking is turned on, *__generate_complex-water.inp__* will be used instead which will generates additional output pdb files containing the water (*__fileroot_1_water.pdbw__* ,...)  
In case of problems (*and in general to make sure that everything is OK*) look into the output files generated (.out) for error messages (search for ERR).  


<hr>

## Randomization of starting orientations and rigid body energy minimization  

The first docking step in HADDOCK is a rigid body energy minimization.  

First the molecules are separated by a minimum of 25Å and rotated randomly around their center of mass. This randomization step can be turned off in the [*run.cns*](/software/haddock2.4/run) parameter file. If you wish to decrease (or increase) the separation distance between the two molecules, edit in the ***protocols*** directory the ***separate.cns*** CNS script and change the value of the *$minispacing* parameter.  
The rigid body minimization is performed in multiple steps:  

*   four cycles of rotational minimization in which each molecule (molecule+associated solvent in case of solvated docking) is allowed to rotate in turn  

*   two cycles of rotational and translational rigid body minimization in which each molecule+associated solvent is treated as one rigid body  

If ***solvated docking is turned on*** the following additional steps will be performed:  

  *   rotational and translational rigid bogy minimization with each molecule and water molecule treated as separate rigid bodies

  *   Biased Monte Carlo removal of water molecules based on propensity of finding a water mediated contact until a user-defined percentage of water molecules remains

  *   rotational and translational rigid bogy minimization with each molecule and water molecule treated as separate rigid bodies


For details of the solvated docking protocol refer to:

  *   A.D.J. van Dijk and A.M.J.J. Bonvin  
"[Solvated docking: introducing water into the modelling of biomolecular complexes](https://doi.org/doi:10.1093/bioinformatics/btl395){:target="_blank"}".  
*Bioinformatics*, **22** 2340-2347 (2006).

  *   M. van Dijk, K. Visscher, P.L. Kastritis and A.M.J.J. Bonvin  
"[Solvated protein-DNA docking using HADDOCK](https://doi.org/doi:10.1007/s10858-013-9734-x){:target="_blank"}."  
*J. Biomol. NMR*, **56**, 51-63 (2013).

  *   P.L. Kastritis, K.M. Visscher, A.D.J. van Dijk and <font color="#333333"> A.M.J.J. Bonvin </font>  
"[Solvated docking using Kyte-Doolittle-based water propensities](https://doi.org/doi:10.1002/prot.24210){:target="_blank"}."  
*Proteins: Struc. Funct. & Bioinformatic.*, **81**, 510-518 (2013).  


If ***RDC, PCS or diffusion anisotropy restraints are used*** two additional minimization steps are carried out to optimize the orientation of the molecules with respect to the alignment tensor(s).  


For each starting structure combination, the rigid body minimisation step is repeated a number of times (given by the *Ntrials* parameter in the *[run.cns](/software/haddock2.4/run)* parameter file. In addition, 180 degree rotated solutions are systematically sampled if the *rotate180_0* parameter in the *[run.cns](/software/haddock2.4/run)* parameter file is set to *true* (default behavior). Only the best solution from these docking trials is written to disk.  


**Note:** The translational minimization can be turned off in *[run.cns](/software/haddock2.4/run)* by setting `rigidmini` to `false` (default is `true`). This option can be useful for example for small flexible molecules to perform the docking during the simulated annealing stage allowing conformational changes to take place during the docking process. The number of steps in the first two stages of the simulated annealing should then be increased by at least a factor four to allow the molecules to approach each other.  

The ***refine.inp*** CNS script is used for the rigid body minimisation step and the resulting models are written as *fileroot_1.pdb, fileroot_2.pdb, ...* in the ***structures/it0*** directory

***Note1:*** If solvated docking is turned on (`waterdock=true` in [*run.cns*](/software/haddock2.4/run#iter), additional output pdb files will be written to disk containing the water (*fileroot_1_water.pdbw* ,...).

***Note2:*** If random removal of restraints is turned on (`noecv=true` in [*run.cns*](/software/haddock2.4/run#iter)), additional files will be written to disk containing the random number seed (*fileroot_1.seed* ,...). This seed is used in the refinement to make sure that the same restraints are removed.

***Note3:*** If random AIR definition is turned on (`ranair=true` in [*run.cns*](/software/haddock2.4/run#iter)), additional files will be written to disk containing the list of residues selected for the AIR definition (*fileroot_1.disp* ,...)..


The CNS scripts called in sequential order for the rigid body EM are (depending on the options selected):


*   *__initialize.cns__*: 	Initializes the iteration variable
*   *__iterations.cns__*: 	Defines the iteration variable
*   *__run.cns__*: 			Reads in all parameter settings for the run
*   *__read_struc.cns__*:	Reads in the topologies and parameters
*   *__centroids_initialize.cns__*:	Initialize dummy residues for centroids EM restraints
*   *__covalions.cns__*:	Defines covalent bonds to single ions
*   *__setflags.cns__*:		Defines the active energy terms
*   *__read_data.cns__*:	Reads the various restraints
*   *__em_read_data.cns__*:	Reads the EM restraints
*   *__centroids_set_restraints__*:	Defines centroid restraints for EM
*   *__read_water1.cns__*	Reads water coordinates for solvated docking
*   *__water_rest.cns__*	Define restraints between interfacial waters and highly solvated amino acids
*   *__read_data.cns__*:	Reads the various restraints
*   *__setflags.cns__*:		Defines the active energy terms
*   *__randomairs.cns__*:	Defines ambiguous restraints based on random patches
*   *__symmultimer.cns__*:	Defines symmetry restraints
*   *__zrestrainting.cns__*: 	Defines harmonic Z-restraints
*   *__cm-restraints.cns__*: 	Defines center-of-mass distance restraints
*   *__surf-restraints.cns__*:	Defines surface restraints
*   *__centroids_initialize.cns__*: Initializes the centroids for EM restraining
*   *__centroids_set_map__*: 	Defines map centroids for EM restraining
*   *__separate.cns__*:			Separates the molecules in space
*   *__random_rotations.cns__*: Applies random rotations to each molecule
*   *__centroids_init_placement.cns__*: Sets the initial positions of molecules in case of EM restraints
*   *__scale_inter_mini.cns__*: Defines the scaling of intermolecular interactions for rigid-body EM
*   *__mini_tensor.cns__*:		Optimizes the tensor orientation for RDC restraints
*   *__mini_tensor_para.cns__*: Optimizes the tensor orientation for PCS restraints
*   *__mini_tensor_dani.cns__*: Optimizes the tensor orientation for diffusion anisotropy restraints
*   *__waterdock_remove-water.cns__*: Remove interfacial waters following a Monte Carlo approach
*   *__db0.cns__*:			Used in the removal of water for solvated docking
*   *__db00.cns__*:			Used in the removal of water for solvated docking
*   *__db1.cns__*:			Used in the removal of water for solvated docking
*   *__waterdock_mini.cns__*:	Minimizes the interfacial waters
*   *__em_orien_search.cns__*:	Performs a search to orient the complex properly in the EM density
*   *__bestener.cns__*:		Keeps track of the best generated model so far
*   *__rotation180.cns__*:	Performs a 180 rotation around a vector perpendicular to the interface and minimize the complex again
*   *__em_orien_search.cns__*:	Performs a search to orient the complex properly in the EM density
*   *__bestener.cns__*:			Keeps track of the best generated model so far
*   *__scale_inter_only.cns__*:	Turns on only intermolecular interactions
*   *__mini_tensor.cns__*:		Optimizes the tensor orientation for RDC restraints
*   *__mini_tensor_para.cns__*: Optimizes the tensor orientation for PCS restraints
*   *__mini_tensor_dani.cns__*: Optimizes the tensor orientation for diffusion anisotropy restraints
*   *__scale_intra_only.cns__*:	Defines only intremolecular interactions
*   *__read_noes.cns__*:		Reads again the distance restraints
*   *__symmultimer.cns__*:		Defines symmetry restraints
*   *__read_noes.cns__*:		Reads again the distance restraints
*   *__scale_inter_final.cns__*:	Turns on only intermolecular interactions and apply final scaling factor
*   *__scale_intra_only.cns__*:		Defines only intremolecular interactions
*   *__print_coorheader.cns__*:	Defines the remarks with energy statistics for the output PDB files
*   *__waterdock_out0.cns__*:	Writes output PDB files for water in case of solvated docking


When all structures have been generated (typically in the order of 1000 to 10000 depending on the number of starting conformations, the protocol settings and your CPU resources), HADDOCK will sort them accordingly to the criterion defined in the [*run.cns*](/software/haddock2.4/run) parameter file and write the sorted PDB filenames into *file.cns, file.list* and *file.nam* in the ***structures/it0*** directory. These will be used for the next step (semi-flexible simulated annealing).  


<hr>

### Semi-flexible simulated annealing  

The best XXX structures after rigid body docking (typically 200, but this is left to the user's choice (see the [run.cns file](/software/haddock2.4/run) section)) will be subjected to a semi-flexible simulated annealing (SA) in torsion angle space. This semi-flexible annealing consists of several stages:  

*   High temperature rigid body search
*   Rigid body SA
*   Semi-flexible SA with flexible side-chains at the interface
*   Semi-flexible SA with fully flexible interface (both backbone and side-chains)  

The temperatures and number of steps for the various stages are defined in the [*run.cns*](/software/haddock2.4/run) parameter file.  


HADDOCK allows to automatically define the semi-flexible regions by considering all residues within 5A of another molecule. To use this option, set *nseg_X* to -1 in [run.cns](/software/haddock2.4/run) (or another negative number if you still want to define manually segments for [random AIRs](/software/haddock2.4/generate_air_help#ranair) definition from a limited region of the surface). This can be set for each molecule separately.  


HADDOCK also allows the definition of fully flexible regions (defined by the *nfle_X* parameter in [run.cns](/software/haddock2.4/run)). Those remain fully flexible throughout all four stages. This should be useful for cases where part of a structure are disordered or unstructured or when docking small flexible ligands or peptides onto a protein. This option also allows the use of HADDOCK for structure calculations of complexes when classical NMR restraints are available to drive the folding.  


The generated output files are:

*   *fileroot_1.pdb, fileroot_2.pdb, ... written in the ***structures/it1*** directory  
*   *fileroot_runX_it1_refine_1.out, ... written in the run directory

***Note1:*** If solvated docking is turned on (*waterdock=true* in [*run.cns*](/software/haddock2.4/run#iter)), additional output pdb files will be written to disk containing the water (*fileroot_1_water.pdbw* ,...).  

***Note2:*** If random removal of restraints is turned on (*noecv=true* in [*run.cns*](/software/haddock2.4/run#iter)), additional files will be written to disk containing the random seed number (*fileroot_1.seed* ,...). This seed is used in the explicit solvent refinement to make sure that the same restraints are removed.


The ***refine.inp*** CNS script is used for this step and the CNS scripts called in sequential order for this semi-flexible refinement stage are (depending on the options selected):


*   *__initialize.cns__*: 	Initialize the iteration variable
*   *__iterations.cns__*: 	Defines the iteration variable
*   *__run.cns__*: 			Reads in all parameter settings for the run
*   *__read_struc.cns__*:	Reads in the topologies and parameters
*   *__centroids_initialize.cns__*:	Initializes dummy residues for centroids EM restraints
*   *__covalions.cns__*:	Defines covalent bonds to single ions
*   *__setflags.cns__*:		Defines the active energy terms
*   *__read_data.cns__*:	Reads the various restraints
*   *__em_read_data.cns__*:	Reads the EM restraints
*   *__centroids_set_restraints__*:	Defines centroid restraints for EM
*   *__read_water1.cns__*	Reads water coordinates for solvated docking
*   *__water_rest.cns__*	Define restraints between interfacial waters and highly solvated amino acids
*   *__read_data.cns__*:	Reads the various restraints
*   *__setflags.cns__*:		Defines the active energy terms
*   *__centroids_initialize.cns__*: Initializes the centroids for EM restraining
*   *__centroids_set_restraints.cns__*: Sets the centroid-based distance restraints
*   *__expand.cns__*:		Expands the initial structure and randomly rotates each component. Saves the initial center of mass positions
*   *__contactairs.cns__*:	Defines ambiguous distance restraints between contacting surfaces
*   *__water_rest.cns__*	Define restraints between interfacial waters and highly solvated amino acids
*   *__symmultimer.cns__*:	Defines symmetry restraints
*   *__zrestrainting.cns__*: 	Defines harmonic Z-restraints
*   *__cm-restraints.cns__*: 	Defines center-of-mass distance restraints
*   *__contactairs.cns__*:	Defines ambiguous distance restraints between contacting surfaces instead of surface resrtaints if defined
*   *__protein-ss-restraints-all.def__:	Defines secondary structure restraints for all residues if defined
*   *__protein-ss-restraints-alpha.def__:	Defines secondary structure restraints for alpha helices if defined
*   *__protein-ss-restraints-alpha-beta.def__:	Defines secondary structure restraints for alpha helices and beta sheets if defined

TODO

*   *__bestener.cns__*:		Keeps track of the best generated model so far
*   *__rotation180.cns__*:	Performs a 180 rotation around a vector perpendicular to the interface and minimize the complex again
*   *__em_orien_search.cns__*:	Performs a search to orient the complex properly in the EM density
*   *__bestener.cns__*:			Keeps track of the best generated model so far
*   *__scale_inter_only.cns__*:	Turns on only intermolecular interactions
*   *__mini_tensor.cns__*:		Optimizes the tensor orientation for RDC restraints
*   *__mini_tensor_para.cns__*: Optimizes the tensor orientation for PCS restraints
*   *__mini_tensor_dani.cns__*: Optimizes the tensor orientation for diffusion anisotropy restraints
*   *__scale_intra_only.cns__*:	Defines only intremolecular interactions
*   *__read_noes.cns__*:		Reads again the distance restraints
*   *__symmultimer.cns__*:		Defines symmetry restraints
*   *__read_noes.cns__*:		Reads again the distance restraints
*   *__scale_inter_final.cns__*:	Turns on only intermolecular interactions and apply final scaling factor
*   *__scale_intra_only.cns__*:		Defines only intremolecular interactions
*   *__print_coorheader.cns__*:	Defines the remarks with energy statistics for the output PDB files
*   *__waterdock_out0.cns__*:	Writes output PDB files for water in case of solvated docking




*  *initialize.cns*
*   *iterations*
*   *run.cns*
*   *read_struc.cns*
*   *covalions.cns*
*   *flags_new.cns*
*   *read_data.cns*
*   *calc_free-ene.cns*
*   *read_water1.cns*
*   *water_rest.cns*
*   *flags_new.cns*
*   *contactairs.cns*
*   *water_rest.cns*
*   *symmultimer.cns*
*   *cm-restraints.cns*
*   *surf-restraints.cns*
*   *dna-rna_restraints.def
*   *set_noe_scale.cns*
*   *mini_tensor.cns*
*   *mini_tensor_dani.cns*
*   *scale_inter_only.cns*
*   *rotation180.cns*
*   *flags_new.cns*
*   *flex_segment_back.cns*
*   *torsiontop.cns*  
*   *sa_ltad_hightemp.cns*
    - *set_noe_scale.cns*
    - *scale_inter.cns*
*   *sa_ltad_cool1.cns*
    - *set_noe_scale.cns*
    - *scale_inter.cns*
*   *torsiontop_flex.cns*
    - *flex_segment_side.cns*
    - *numtrees.cns*
*   *sa_ltad_cool2.cns*
    - *set_noe_scale.cns*
    - *scale_inter.cns*
*   *torsiontop_flex_back.cns*
    - *flex_segment_back.cns*
    - *numtrees.cns*
*   *sa_ltad_cool3.cns*
    - *set_noe_scale.cns*
    - *scale_inter.cns*
*   *set_noe_scale.cns*
*   *flex_segment_back.cns*
*   *scale_intra_only.cns*
*   *scale_inter_only.cns*
*   *symmultimer.cns*
*   *read_noes.cns*
*   *dna-rna_restraints.def*
*   *print_coorheader.cns*
*   *waterdock_out1.cns*

At the end of the calculation, HADDOCK generates the *file.cns, file.list* and *file.nam* files containing the filenames of the generated structures sorted accordingly to the criterion defined in the [run.cns](/software/haddock2.4/run#iter) parameter file.  
At the end of this stage, the structures are analyzed and the results are placed in the ***structures/it1/analysis*** directory (see the [analysis](/software/haddock2.4/analysis) section).  

* * *

<a name="water">**4\. <u>Flexible explicit solvent refinement</u>**</a>  

In this final step, the structures obtained after the semi-flexible simulated annealing are refined in an explicit solvent layer (8A for water, 12.5A for DMSO). In this step, no spectacular changes are expected, however, the scoring of the various structures is improved.  

The ***re_h2o.inp*** or ***re_dmso.inp*** CNS script is used for this step.

*   *fileroot_1w.pdb, fileroot_2w.pdb, ... written in the ***structures/it1/water*** directory  

***Note1:*** The numbering of the structures from it1 is kept.  

***Note2:*** If *keepwater* is set to true in [*run.cns*](/software/haddock2.4/run#iter), additional output pdb files will be written to disk containing the water (*fileroot_1_h2o.pdb* ,...).

*   *initialize.cns*
*   *iterations.cns*
*   *run.cns*
*   *read_struc.cns*
*   *flags_new.cns*
*   *calc_free-solv-ene.cns*
*   *calc_free-ene.cns*
*   *read_water1.cns*
*   *generate_water.cns (or generate_dmso.cns*)
*   *water_rest.cns*
*   *symmultimer.cns*
*   *set_noe_scale.cns*
*   *dna-rna_restraints.def*
*   *mini_tensor.cns*
*   *mini_tensor_dani.cns*
*   *flex_segment_side.cns*
*   *set_noe_scale.cns*
*   *flex_segment_back.cns*
*   *set_noe_scale.cns*
*   *scale_intra_only.cns*
*   *scale_inter_only.cns*
*   *symmultimer.cns*
*   *read_noes.cns*
*   *dna-rna_restraints.def*
*   *print_coorheader.cns*


At the end of the explicit solvent refinement, HADDOCK generates the *file.cns, file.list* and *file.nam* files containing the filenames of the generated structures sorted accordingly to the criterion defined in the [run.cns](/software/haddock2.4/run#iter) parameter file.  

Finally, the structures are analyzed and the results are placed in the ***structures/it1/water/analysis*** directory (see the [analysis](/software/haddock2.4/analysis) section).  

* * *
