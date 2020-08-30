---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
title: HADDOCK2.4 manual - Analysis
image:
  feature: pages/banner_software.jpg
---


The analysis of the docking results are performed after the [semi-flexible simulated annealing step](/software/haddock2.4/protocol) and after the final refinement](/software/haddock2.4/protocol). A number of standard CNS analysis scripts are automatically run by HADDOCK and the results are placed in the **analysis** directory in **runX/structures/it1** and **runX/structures/it1/water**, respectively. Some of the generated output files are parsed automatically by HADDOCK to generate for example violations statistics (see violation analysis). Another important step consists in a post-docking manual analysis of the generated structures and their clusters. This is the critical step for the classification of the docking solutions and the identification of the best(s) cluster(s).  

* table of contents
{:toc}


* * *

### Standard analysis performed by HADDOCK


The following CNS analysis scripts are run by HADDOCK in the full analysis mode. If clustering mode is defined, only the average structure and either RMSD or FCC matrix are generated.


#### Average structure

The ***get_average.inp*** script will calculate an average structure by superimposing the structures on the backbone atoms of the interface residues defined over all models (automatic mode) or from the defined semi-flexible region in [run.cns](/software/haddock2.4/run){:target="_blank"} parameter file.  

  **_Note1:_** If less than three atoms are selected when using the defined semi-flexible segments, then the entire backbone will used. If still less than three atoms are selected, then all heavy atoms will be used for the fitting. This makes sure that at least three atoms are selected for any molecule, including small ligands.


The structures are fitted onto the average structures and written to disk in the **analysis** directory. Various average rmsds calculated over the ensemble of structure and rmsds from the average for each structure are output to file.  

Output files:
*   _fileroot_ave.pdb_: average structure  

*   _filerootfit_1.pdb, filerootfit_2.pdb, ..._: superimposed structures  

  **_Note2:_** The numbering of the superimposed PDB files does not correspond with the numbering in the it1 or water directories, but to the position of the structure in the sorted file.list file, i.e. structure number 1 in the analysis directory is the first (best) in file.list and structure number 50 is at position 50 in that file. The numbering of the superimposed PDB files does not correspond with the numbering in the **it1** or **water** directories, but to the position of the structure in the sorted _file.list_ file, i.e. structure number 1 in the **analysis** directory is the first (best) in _file.list_ and structure number 50 is at position 50 in that file.  

  *   _rmsave.disp_: contains the RMSD from the average structure for each structure and the average values over the ensemble. For this, the structures are superimposed on the backbone atoms of the flexible interface (see **_Note1_** above) and the following average RMSD values from the average structure are calculated and written to file:
      *   RMSD backbone interface of all molecules
      *   RMSD complete backbone of all molecules
      *   backbone interface of molecule A
      *   backbone interface of molecule B
      *   backbone interface of molecule C
      *   ...  

      In addition to the average RMSD calculated from the entire ensemble, the corresponding single structure RMSD values are listed in _rmsave.disp_  

  *   _rmsdseq.disp_: per residue RMSDs (backbone heavy atoms (N,CA,C), extended backbone heavy atoms (N,CA,CB,C,O), side-chain heavy atoms and all heavy atoms.  

  *   _fileroot-reduced.crd_: trajectory file containing only the coordinates of the flexible interface backbone atoms (see **_Note1_** above); this reduced file is used to calculate the [pairwise RMSD matrix](#rmsd) and thereby speed up the calculations.
  

* * *

#### Pairwise RMSD matrix

The ***rmsd.inp*** calculates the pairwise RMSD matrix over all structures. For this the structures are first superimposed on the flexible interface backbone atoms of molecule A and the RMSD is calculated on the flexible interface backbone atoms of the other molecules (see **_Note1_** above). This RMSD can be termed: "ligand interface RMSD".  

  Output files:  

  *   _fileroot_rmsd.disp_: this file contains the pairwise RMSD matrix with on each line three number: the structure numbers of the two structures being compared and the corresponding RMSD value.  

      **_Note3:_** The numbering of the structures corresponds to the position of the structure in the sorted _file.list_ file.  

      This file is used as input for the RMSD [clustering](#clusterrmsd).

  * * *

#### Energetics

The ***energy.inp*** script performs the analysis of bonded and non-bonded energies per structure and averaged over the ensemble. Various energy terms are calculated:
  *   over the entire complex
  *   over the flexible interface only (as defined in the [run.cns](/software/haddock2.4/run){:target="_blank"} parameter file)
  *   only the intermolecular energies (vdw and elec)In addition, the buried surface area is also reported. The buried surface area is calculated by taking the difference between the sum of the solvent accessible surface area for each molecule separately and the solvent accessible area of the complex. The solvent accessible area is calculated using a 1.4A water probe radius and an accuracy of 0.075A (in case of memory problems for very large complexes increase this value, e.g. 0.1 or higher).  

  Output files:
  *   _energies.disp_: this file contains the various energy terms per structure and averaged over the ensemble  

      *   Complex statistics: _Etot, Ebond, Eangle, Eimpr, Edihed, Evdw, Eelec_
      *   Flexible interface statistics: _Etot, Evdw, Eelec_
      *   Intermolecular statistics: _Etot, Evdw, Eelec_
      *   Buried surface area
      
      
* * *

#### Desolvation energy

The ***edesolv.inp*** script performs the analysis desolvation energy per structure and averaged over the ensemble. The desolvation energy is calculated using the empirical atomic solvation parameters from Fernandez-Recio _et al._ _JMB_ **335**:843 (2004). These are defined in the _def_solv_param.cns_ CNS script in the _**protocols**_ directory.  

  Output files:
  *   _edesolv.disp_: this file contains the desolvation energy per structure and averaged over the ensemble


* * *

#### Per-residue energy analysis

The ***ene-residue.inp*** script performs a per-residue intermolecular interaction energy analysis for all residues which make intermolecular contacts. A residue is selected for analysis if it makes at least one contact within 5A within the ensemble analysed. Van der Waals, electrostatic and total interaction energies are reported per structure and as averages over the ensemble. They are calculated using the default 8.5A cutoff and a dielectric constant of 1 (all defined in the _read_struc.cns_ CNS script.  

  Output files:
  *   _ene-residue.disp_: this file contains the various energy terms per structure and averaged over the ensemble  

      Example:

  <pre style="background-color:#DAE4E7" >   
      #Residue ASP 38 A - intermolecular energies
      #file Etot Evdw Eelec
      # PREVIT:e2a-hpr_161.pdb -16.7601 -3.41526 -13.3448
      # PREVIT:e2a-hpr_189.pdb -42.4061 -1.83788 -40.5682
      ...
      # mean values for interaction with residue ASP 38 A
      # ASP 38 A : Etot   -34.528 (+/- 21.4012 ) [kcal/Mol]
      # ASP 38 A : Evdw   -1.34906 (+/- 0.967306 ) [kcal/Mol]
      # ASP 38 A : Eelec  -33.179 (+/- 21.1375 ) [kcal/Mol]
      ...
  </pre>

  The average per-residue values can be easily extracted from this file and sorted in decreasing contribution with the following command:

  <pre style="background-color:#DAE4E7" >
  grep ": Evdw" ene-residue.disp |sort -gk7
  grep ": Eele" ene-residue.disp |sort -gk7
  grep ": Etot" ene-residue.disp |sort -gk7
  </pre>

 
* * *

#### Covalent geometry analysis

The ***print_geom.inp*** script performs the analysis of the covalent geometry, reporting on the deviations from ideal values for bonds, angles, impropers and dihedrals. The deviations per structure and averaged over the ensemble are reported.  

  Output files:
  *   _geom.disp_: this file contains the averaged deviations from ideal geometry per structure and averaged over the ensemble.  

  *   _print_geom.out_: this file contains the listing of covalent terms deviating from the ideal geometry:
      *   bonds > 0.025 A
      *   angles > 2.5 degrees
      *   improper dihedrals > 2.5 degrees
      *   dihedral angles > 30 degrees

 
* * *

#### Distance restraints violation analysis

The ***print_noes.inp*** script performs the analysis of distance (including AIR) restraint violations, generating output for all restraints combined and for each type of restraints (unambiguous, ambiguous (or AIRs) and hbonds) separately.  

  Output files:
  *   _noe.disp_: this file contains the number of distance restraints violations per structure and averaged over the ensemble over all distance restraint classes and for each class (unambiguous, ambiguous, hbonds) separately. Distance restraints violation > 0.5, 0.3 and 0.1 A are reported.  
  *   _print_dist_all.out_: this file contains the violation listing for all distance restraints including hbond restraints.  
  *   _print_dist_noe.out_: this file contains the violation listing for all distance distance restraints (unambiguous and ambiguous classes).  
  *   _print_noe_unambig.out_: this file contains the violation listing for the unambiguous distance restraints.  
  *   _print_noe_ambig.out_: this file contains the violation listing for the ambiguous distance restraints (typically the class used to define Ambiguous Interaction Restraints).  
  *   _print_dist_hbonds.out_: this file contains the violation listing for the hydrogen bond distance restraints.  

      **_Note4:_** The above five files (print_....out) are parsed automatically by HADDOCK to generate statistics on a restraint basis over all structures in the ensemble using the **ana_noe_viol.csh** script provided in the **tools** directory (see violation analysis).

 
* * *

#### Dihedral angle restraints violation analysis

The ***print_dih.inp*** script performs the analysis of dihedral angle restraint violations, listing per structure the violations above 5 degree and the average violations over the entire ensemble.  

  Output files:
  *   _dihedrals.disp_: this file contains the number of dihedral restraints violations per structure and averaged over the ensemble.  
  *   _print_dih.out_: this file contains the violation listing for all dihedral restraints. This file is parsed automatically by HADDOCK to generate statistics on a restraint basis over all structures in the ensemble using the **ana_dihed_viol.csh** script provided in the **tools** directory (see [violation analysis](#viol)).

 
* * *

#### RDC (SANI) restraints violation analysis

The ***print_sani.inp*** script performs the analysis of [dipolar coupling restraint](/software/haddock2.4/RDC){:target="_blank"} violations, listing per structure the average rms violations and the number of violations above 1.0, 0.5 and 0.2 Hz, respectively. It also reports the average rms violation over the entire ensemble.  

  Output files:
  *   _sani.disp_: this file contains the number of dipolar coupling violations per structure and averaged over the ensemble.  
  *   _print_sani.out_: this file contains the dipolar couplings violation listing. (No automatic parsing of this file is currently implemented).

 
* * *

#### RDC (VEAN) restraints violation analysis

The ***print_vean.inp<*** script performs the analysis of [intervector projection angle restraint](/software/haddock2.4/RDC){:target="_blank"} violations, listing per structure the violations above 5 degrees. It also reports the average rms violation over the entire ensemble.  

  Output files:
  *   _vean.disp_: this file contains the number of intervector projection angle restraints violations per structure and averaged over the ensemble.  
  *   _print_vean.out_: this file contains the intervector projection angle restraints violation listing. (No automatic parsing of this file is currently implemented).

 
* * *

#### Diffusion anisotroyp restraints violation analysis

The ***print_dani.inp*** script performs the analysis of [diffusion anisotropy restraint](/software/haddock2.4/DANI){:target="_blank"} violations, listing per structure the average rms violations and the number of violations above 1.0, 0.5 and 0.2, respectively. It also reports the average rms violation over the entire ensemble.  

  Output files:
  *   _dani.disp_: this file contains the number of diffision anisotropy violations per structure and averaged over the ensemble.  
  *   _print_dani.out_: this file contains the diffision anisotropy violation listing. (No automatic parsing of this file is currently implemented).

 
* * *

#### Intermolecular hydrogen bond analysis

The ***print_hbonds.inp*** script performs the analysis of intermolecular hydrogen bonds. The definition of an hydrogen bond is however a crude one since it is only based on the proton-acceptor distance. This distance can be specified in the [run.cns](/software/haddock2.4/run#hbnb) parameter file (default is 2.5A).  

  Output files:
  *   _hbonds.disp_: this file contains a listing of all intermolecular hydrogen bonds over the ensemble of structures. It is automatically parsed by HADDOCK using the _ana_hbonds.csh_ script located in the **tools** directory. This scripts generate a listing (_ana_hbonds.lis_) of intermolecular hydrogen bonds including the number of occurrences and the average hydrogen bond distance.  

      **_Note5:_**  The _ana_hbonds.csh_ can also be run manually. For this simply copy the _ana_hbonds.csh_ and _count_hbonds.awk_ scripts from the **tool** directory into the analysis directory and type:


<pre style="background-color:#DAE4E7" >
./ana_hbonds.csh hbonds.disp
</pre>

 
* * *

#### Intermolecular non-bonded contact analysis

The ***print_nb.inp*** script performs the analysis of intermolecular hydrophobic contacts. An hydrophobic contact is identified when two carbon atoms are at less than a user-defined distance, typically 3.9A. This distance cut-off can be specified in the [run.cns](/software/haddock2.4/run#anal) parameter file (default is 3.9A).  

  Output files:
  *   _nbcontacts.disp_: this file contains a listing of all intermolecular hydrophobic contacts over the ensemble of structures. It is automatically parsed by HADDOCK using the _ana_hbonds.csh_ script located in the **tools** directory. This scripts generate a listing (_ana_nbconbtacts.lis_) of intermolecular hydrophobic contacts including the number of occurrences and the average C-C distance.  

      **_Note6:_** The _ana_hbonds.csh_ script can also be run manually. For this simply copy the _ana_hbonds.csh_ and _count_hbonds.awk_ scripts from the  **tool** directory into the analysis directory and type:


<pre style="background-color:#DAE4E7" >
  ./ana_hbonds.csh nbcontacts.disp
</pre>


* * *
* * *

### Violations analysis

HADDOCK performs automatically a number of violations analysis, generating a listing of violations including the number of times a restraint is violated and the average distance and violation per restraint. This is done for distance restraints (all distances (distances + Hbonds), distances only, unambiguous distances only, ambiguous distances only, dihedral angle restraints). A number of _.lis_ files are generated in the _**analysis**_ directory:  

  *   _ana_dihed_viol.lis_: dihedral angles violations if a dihedral file has been defined  
  *   _ana_dist_viol.lis_: all distance (including Hbonds) restraints violations
  *   _ana_hbond_viol.lis_: hydrogen bond restraints violations
  *   _ana_noe_viol_all.lis_: all distance restraints violations
  *   _ana_noe_viol_unambig.lis_: unambiguous distance restraint violations
  *   _ana_noe_viol_ambig.lis_: ambiguous distance restraints (this is the restraint type typically used for the ambiguous interaction restraints (AIRs).Distance restraint violations > 0.3 A and dihedral angle restraints violations > 5 degree are reported. All atoms belonging to one restraints are listed, which in the case of ambiguous interaction restraints can be a very large number exceeding 1000! A new line always starts with _Rexp=_.  

  Example:

<pre style="background-color:#DAE4E7" > <font size="-1">
Rexp=   2.000 Rave=   4.739 Viol=  -2.739 #viol=  200 (    B    36   HIS     N ...
Rexp=   2.000 Rave=   4.626 Viol=  -2.626 #viol=  200 (    B    65   ASP     N ...
Rexp=   2.000 Rave=   4.345 Viol=  -2.345 #viol=  200 (    B    33   GLN     N ...
Rexp=   2.000 Rave=   4.037 Viol=  -2.037 #viol=    1 (    B    92   GLY     N ...
Rexp=   2.000 Rave=   3.225 Viol=  -1.225 #viol=   63 (    A    37   SER     N ...
...
</font></pre>

  _Rexp= 2.000_ corresponds to the upper distance restraint (in Angstrom) defined in the AIR restraint file).  

  _Rave= 4.739_ corresponds to the average distance (in Angstrom) in the calculated structures.  

  _Viol= -2.739_ corresponds to the violation in Angstrom.  

  _#viol= 200_ corresponds to the number of structures in which the restraint is violated.  
  
  
* * *
* * *

### Manual post-docking analysis

An important part of the analysis, namely the analysis of the clusters, needs to be performed manually when using a local version of HADDOCK.
A number of scripts are provided for this purpose in the **runX/tools** directory.  


* * *

#### Collection of single structures statistics

This can be done by executing the ***ana_structures.csh** script once the _file.list_ file has been created. It extracts from the header of the PDB files various energy terms, violation statistics and buried surface area and calculates the RMSD of each structure compared to the lowest energy one (if the location of ProFit is defined (see [installation](/software/haddock2.4/installation){:target="_blank"} and [software links](/software/haddock2.4/software){:target="_blank"})).  

To run it type:

<pre style="background-color:#DAE4E7" >
   $HADDOCKTOOLS/ana_structures.csh
</pre>

in the directory where _file.list_ has been created (e.g. _**structures/it1**_ or _**structures/it1/water**_).  

Ten files are created:
  *   _**structures_haddock-sorted.stat**_: sorting based on [haddock score](/software/haddock2.4/scoring){:target="_blank"} (as in _file.list_)
  *   _structures_air-sorted.stat_:sorting based on distance restraint energy
  *   _structures_airviol-sorted.stat_: sorting based on number of distance violations
  *   _structures_bsa-sorted.stat_: sorting based on buried surface area
  *   _structures_dH-sorted.stat_: sorting based on total energy difference calculated as total energy of the complex - Sum of total energies of the individual components
  *   _structures_Edesolv-sorted.stat_: sorting based on desolvation energy calculated using the empirical atomic solvation parameters from Fernandez-Recio _et al._ _JMB_ **335**:843 (2004)
  *   _structures_ene-sorted.stat_: sorting based on total energy (only intermolecular components for vdw and elec energies) structures_nb-sorted.stat
  *   _structures_nb-sorted.stat_: sorting based on non-bonded intermolecular energy
  *   _structures_nbw-sorted.stat_: sorting based on weighted non-bonded intermolecular energy ( 1*vdw + 0.1*elec)
  *   _structures_rmsd-sorted.stat_: sorting based on RMSD from best (lowest) HADDOCK score structure


The content of these files looks like:

<pre style="background-color:#DAE4E7" > <font size="-1">#struc haddock-score RMSD-Emin Einter Enb Evdw+0.1Eelec Evdw Eelec Eair Ecdih Ecoup Esani Evean Edani #NOEviol #Dihedviol #Jviol #Saniviol #veanviol #Daniviol bsa dH Edesolv
e2a-hpr_71w.pdb -164.13017 0.000 -629.446 -635.908 -107.853 -49.1804 -586.728 6.4629 0 0 0 0 0 0 0 0 0 0 0 1613.82 -8593.04 1.74954
e2a-hpr_171w.pdb -156.04058 0.748 -613.411 -624.683 -103.675 -45.7858 -578.897 11.2722 0 0 0 0 0 0 0 0 0 0 0 1663.99 -8501.99 4.3974
e2a-hpr_38w.pdb -150.756688 0.624 -574.337 -587.378 -97.1234 -42.6507 -544.727 13.0407 0 0 0 0 0 0 0 0 0 0 0 1688.07 -8600.72 -0.464658
...
</font></pre>

The first line of those files gives the description of the columns, e.g. the first column corresponds to the pdb file, the second column to the combined HADDOCK score, the third to the backbone RMSD from the lowest energy structure, the third column to the total intermolecular energy (sum of all energy terms), the fourth column to the intermolecular non-bonded energy (vdw+elec),...  

You can generated a plot of the HADDOCK score as a function of the RMSD (using XmGrac for example).  

A simple script called _make_ene-rmsd_graph.csh_ is provided in $HADDOCKTOOLS which allows you to generate an input file for [Xmgr/XmGrace](https://plasma-gate.weizmann.ac.il/Grace/){:target="_blank"}. Simply specify two columns to extract data from and a filename:

<pre style="background-color:#DAE4E7" >
$HADDOCKTOOLS/make_ene-rmsd_graph.csh 3 2 structures_unsorted.stat
</pre>

This will generate a file called _ene_rmsd.xmgr_ which you can display with xmgr or xmgrace:

<pre style="background-color:#DAE4E7" >
grace ene_rmsd.xmgr
</pre>


* * *

#### Cluster-based analysis

##### RMSD-based clustering of solutions using cluster_struc

If selected this clustering is run automatically by HADDOCK in _**it1/analysis**_ and _**it1/water/analysis**_ based on the criteria defined in the [run.cns](/software/haddock2.4/run){:target="_blank"} file. In case RMSD-based clustering has been selected, a reasonable cutoff value to start with for protein-protein complexes is 7.5A. We recommend however that you try using different cut-offs for the clustering since it is difficult to know a priori the best cut-off. This will depend on the system under study and the number of experimental restraints used to drive the docking. If only a small fraction of the structures cluster, try increasing the cut-off.  

**cluster_struc** is a simple C++ program provided in the _**tools**_ directory that read the _fileroot_rmsd.disp_ file containing the pairwise rmsd matrix and generates clusters. This program should have been compiled for your system during [installation](/software/haddock2.4/installation){:target="_blank"}.  

Two clustering algorithms are implemented:

  1.  using an algorithm as described in Daura et al. _Angew. Chem. Int. Ed._ **38**:236-240 (1999): count number of neighbors using cut-off, take structure with largest number of neighbors with all its neighbors as cluster and eliminate it from the pool of clusters. Repeat for remaining structures in pool.  

  2.  full linkage: add a structure to a cluster when its distance to any element of the cluster is less than the cutoff.The full linkage option generates thus larger clusters and the structures within a cluster can thus differ more. It is called by using the _-f_ option. The default option used by HADDOCK is the first one (algorithm of Daura et al.). To use full linkage rerun the clustering manually.  

The usage is:

<pre style="background-color:#DAE4E7" ><font size="-1">
cluster_struc [-f]  fileroot_rmsd.disp cut-off  min_cluster_size >cluster.out
</font></pre>

  Example for its use:

<pre style="background-color:#DAE4E7" ><font size="-1">
cluster_struc e2a-hpr_rmsd.disp 7.5 4 >cluster.out
</font></pre>

will create clusters using a 7.5 A RMSD cut-off requiring a minimum of four structures per cluster.  

The output looks like:

<pre style="background-color:#DAE4E7" >
Cluster 1 -> <font color="RED">8</font> 1 2 3 5 6 7 9 10 11 12 13 14 15 ...
Cluster 2 -> 23 25 26 29 39 62 66 67 72 74 78 ...
Cluster 3 -> 153 4 32 43 96 131 147 158 163 ..
</pre>

The numbers correspond to the structure number in the analysis file. For example **<font color="red">8</font>** corresponds to structure number 8 in analysis, i.e, the eigth structure in _file.list_ in _**it1/water**_. The first structure of each cluster above corresponds to the cluster center. The remaining structures are sorted according to their index.  

##### Contact-based clustering of solutions using cluster_fcc.py

If selected this clustering is run automatically by HADDOCK in _**it1/analysis**_ and _**it1/water/analysis**_ based on the criteria defined in the [run.cns](/software/haddock2.4/run) file. In case FCC clustering has been chosen (which means clustering based on the fraction of common contacts), a reasonable cutoff value to start with for protein-protein complexes is 0.75. We recommend however that you try using different cut-offs for the clustering since it is difficult to know a priori the best cut-off. This will depend on the system under study and the number of experimental restraints used to drive the docking. If only a small fraction of the structures cluster, try decreasing the cut-off.  

  **cluster_fcc.py** is a python code provided in the _**tools**_ directory that read the _fileroot_fcc.disp_ file containing the pairwise fraction of common contact matrix and generates clusters. The clustering algorithm is described in Rodrigues et al. [_Proteins: Struc. Funct. & Bioinformatic_, **80** 1810-1817 (2012)](https://doi.org/doi:10.1002/prot.24078){:target="_blank"}.  

The usage is:

<pre style="background-color:#DAE4E7" ><font size="-1">
  Usage: cluster_fcc.py <matrix file=""> <threshold [float]="">[options]

  Options:
    -h, --help            show this help message and exit
    -o OUTPUT_HANDLE, --output=OUTPUT_HANDLE
                          Output File [STDOUT]
    -c CLUS_SIZE, --cluster-size=CLUS_SIZE
                          Minimum number of elements in a cluster [4]</threshold> </matrix>
</font></pre>

Example for its use:

<pre style="background-color:#DAE4E7" > <font size="-1">
python2.7 cluster_fcc.py e2a-hpr_fcc.disp 0.75 -c 4 >cluster.out
</font> </pre>

will create clusters using a 0.75 FCC cut-off requiring a minimum of four structures per cluster.  

The output looks the same as for the RMSD-based clustering explained above  


* * *

#### Cluster-based scoring

This can be done using the **ana_clusters.csh** script which takes the output of **cluster_struc** or **cluster_fcc.py** to perform an analysis of the various clusters, calculating average energies, RMSDs and buried surface area per cluster.  

To run it, type with as argument the output file of the clustering, e.g.:

<pre style="background-color:#DAE4E7">
$HADDOCKTOOLS/ana_clusters.csh [-best #] analysis/cluster.out
</pre>

The **[-best #]** is an optional (but recommended!) argument to generate additional files with cluster averages calculated only on the best **#** structures of a cluster. The best structures are selected based on the HADDOCK score calculated based on the weights defined in [run.cns](/software/haddock2.4/run){:target="_blank"}, i.e. the sorting found in _file.list_. This allows to remove the dependency of the cluster averages upon the size of the respective clusters. The following example will calculate cluster averages over the best 45 structures.

<pre style="background-color:#DAE4E7" >
$HADDOCKTOOLS/ana_clusters.csh -best 4 analysis/cluster.out
</pre>

The **ana_clusters.csh** script analyzes the clusters in a similar way as the **ana_structures.csh** script, but in addition generates average values over the structures belonging to one cluster. It creates a number of files for each cluster containing the cluster number _clustX_ in the name:

  *   _file.cns_clustX_: contains the name of all the pdb files that belong to the cluster X (CNS format)
  *   _file.nam_clustX_: contains the name of all the pdb files that belong to the cluster X
  *   _file.list_clustX_: contains the name of all the pdb files that belong to the cluster X (list format)

      And in addition if the option _-best Y_ is used:  

  *   _file.cns_clustX_bestY_: contains the name of the best Y pdb files that belong to the cluster X (CNS format)
  *   _file.nam_clustX_bestY_: contains the name of the best Y pdb files that belong to the cluster X
  *   _file.list_clustX_bestY_: contains the name of the best Y pdb files that belong to the cluster X (list format)

      **_Note7:_** Those files can be used to repeat the HADDOCK analysis for a single cluster (see below).  

  *   _file.nam_clustX_bsa_: contains the buried surface area of each structure of cluster X
  *   _file.nam_clustX_dH_: contains the total energy difference calculated as total energy of the complex - Sum of total energies of the individual components
  *   _file.nam_clustX_Edesol_: contains the desolvation energy calculated using the empirical atomic solvation parameters from Fernandez-Recio _et al._ _JMB_ **335**:843(2004)
  *   _file.nam_clustX_ener_: contains all the energy terms (intermolecular, Van der Waals, electrostatic and AIR) for each structures of cluster X
  *   _file.nam_clustX_haddock-score_: contains the combined [haddock score](/software/haddock2.4/scoring){:target="_blank"}
  *   _file.nam_clustX_rmsd_: contains the RMSD of each structure of cluster X from the best (lowest) HADDOCK score structure of cluster X.
  *   _file.nam_clustX_rmsd-Emin_: contains the RMSD of each structure of cluster X from the best (lowest) HADDOCK score structure of all calculated structures
  *   _file.nam_clustX_viol_: contains the number of AIR and dihedral violations per structure

      **_Note8:_** The ordering of the structures in those files follows the HADDOCK score ranking.  

      Eight files containing various averages over clusters are created:

  *   _cluster_bsa.txt_: contains the average buried surface area of each cluster and the standard deviation
  *   _cluster_dH.txt_: contains the average total energy difference calculated as total energy of the complex - Sum of total energies of the individual components
  *   _cluster_Edesolv.txt_: contains the average desolvation energy calculated using the empirical atomic solvation parameters from Fernandez-Recio _et al._ _JMB_ **335**:843(2004)
  *   _cluster_ener.txt_: contains the average energy terms of each cluster and the standard deviations
  *   _cluster_haddock.txt_: contains the average combined [haddock score](/software/haddock2.4/scoring){:target="_blank"}
  *   _cluster_rmsd.txt_: contains the average RMSD and standard deviation from the best (lowest) HADDOCK score structure of cluster of the structures belonging to that cluster
  *   _cluster_rmsd-Emin.txt_: contains the average RMSD and standard deviation of the clusters from the best (lowest) HADDOCK score structure of all calculated structures
  *   _cluster_viol.txt_: contains the average AIR and dihedral violations for each cluster and the standard deviations


and twelve files combining all the above information and sorted based on various criteria:

  *   **_clusters_haddock-sorted.stat_**: contains the various cluster averages sorted as a function of the combined [haddock score](/software/haddock2.4/scoring){:target="_blank"}
  *   _clusters.stat_: contains the various cluster averages sorted as a function of the cluster number
  *   _clusters_air-sorted.stat_: contains the various cluster averages sorted accordingly to the AIR energy
  *   _clusters_bsa-sorted.stat_: contains the various cluster averages accordingly to the buried surface area
  *   _clusters_dani-sorted.stat_: contains the various cluster averages accordingly to the diffusion anisotropy restraint energy
  *   _clusters_dH-sorted.stat_: contains the various cluster averages accordingly to the total energy difference calculated as total energy of the complex - Sum of total energies of the individual components
  *   _clusters_Edesolv-sorted.stat_: contains the various cluster averages accordingly to the desolvation energy calculated using the empirical atomic solvation parameters from Fernandez-Recio  _et al._ _JMB_ **335**:843(2004)
  *   _clusters_ene-sorted.stat_: contains the various cluster averages accordingly to the intermolecular energy (restraints+vdw+elec)
  *   _clusters_nb-sorted.stat_: contains the various cluster averagesd accordingly to the intermolecular non-bonded energy (vdw+elec)
  *   _clusters_nbw-sorted.stat_: contains the various cluster averages accordingly to the weighted intermolecular non-bonded energy (vdw+0.1*elec)
  *   _clusters_sani-sorted.stat_: contains the various cluster averages accordingly to the RDC (direct, SANI) restraint energy
  *   _clusters_vean-sorted.stat_: contains the various cluster averages accordingly to the RDC (intervector projection angles, VEAN) restraint energy

      If the option **-best** is given with a number of structures, additional files with as extension **_best#** will be created containing the average values over the best # structures.  

You can plot the HADDOCK score of the clusters as a function of their RMSD from the lowest energy structure (using [xmgr/xmgrace](https://plasma-gate.weizmann.ac.il/Grace/){:target="_blank"} for example).  

<img width="500" src="/software/haddock2.4/haddock-score_vs_rmsd.png"  >

The gray circles correspond to the individual structures and the filled circles correspond to the cluster averages with the standard deviation indicated by bars.  

The assumption is then that the best (lowest) HADDOCK score structures of the best (lowest) HADDOCK score cluster are the best solution generated by HADDOCK. It is then up to you to confirm that using any kind of information you can get such as for example:
  *   mutagenesis data
  *   conservation of given residues from multiple alignments
  *   ...


* * *
* * *

### Rerunning the analysis for a given cluster

It is possible to rerun the HADDOCK analysis for a given cluster. For this, the _file.cns_, _file.list_ and _file.nam_ files should be renamed by adding for example a suffix __all_. These three files contain the sorted list of all structures calculated. Similarly, the **analysis** directory should be renamed. Create then an empty analysis directory and cope the files containing the PDB file listings for a given cluster (these are created when performing the analysis of the clusters with _ana_clusters.csh to _file.cns_, _file.list_ and _file.nam_, respectively.  

To simplify this entire procedure, we are providing a csh script named **make_links.csh** in the **tools** directory (defined by the environment variable $HADDOCKTOOLS). To make the links type:

<pre style="background-color:#DAE4E7" >
$HADDOCKTOOLS/make_links.csh clust1
</pre>

This will automatically move the original files (_file.cns_, _file.list_ and _file.nam_) and rename the **analysis** directory. A new analysis directory called **analysis_clust1** will be created and a link to it will be created as **analysis**. Similarly, links will be created for the three listing files:  

<pre style="background-color:#DAE4E7" >
file.cns  -> file.cns_clust1
file.list -> file.list_clust1
file.nam  -> file.nam_clust1
</pre>

To rerun the analysis go back to the **runX** directory and restart HADDOCK.  

**_Warning:_** In case you wish to experiment with different clustering cut-offs restore first the original files containing the information for all calculated structures with the command:

<pre style="background-color:#DAE4E7" >
$HADDOCKTOOLS/make_links.csh all
</pre>

* * *
