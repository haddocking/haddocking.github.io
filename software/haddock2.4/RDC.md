---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
title: HADDOCK2.4 manual - Residual Dipolar Couplings
image:
  feature: pages/banner_software.jpg
---

* table of contents
{:toc}

Residual dipolar couplings (RDCs) can provide useful information on the orientation of the molecules to be docked. They can be introduced in HADDOCK in two ways:

*   Directly as RDC restraints (SANI statement in CNS)
*   Indirectly by defining intervector projection angle restraints (VEAN statement in CNS)

From our experience, both approaches give good results for docking. The use of intervector projection angle restraints ( [Meiler et al. _J. Biomol. NMR_ **17**, 185 (2000)](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=10805131&dopt=Abstract){:target="_blank"}) avoids the burden of working with a tensor in the structure calculations. Another advantage is that one can distinguish between inter- and intra-molecular restraints. Considering that part of the system will typically be kept rigid during docking, the use of intra-molecular restraints might not make much sense anyway.  

* * *

### Determining the alignment tensor components

For using RDC restraints, the tensor components need first to be determined. In the case of complexes, this can be easily done by using the known structures of the single domains. The software [Pales](http://spin.niddk.nih.gov/bax/software/PALES/index.html){:target="_blank"} (Zweckstetter & Bax (2000). _J. Am. Chem. Soc._ **122**, 3791-3792) can be used for this purpose.  

You need for this to generate a [Pales input file](http://spin.niddk.nih.gov/bax/software/PALES/index.html#DF){:target="_blank"} containing your residual dipolar couplings.  

A csh script called _ana_pdb_Q-factor.csh_ is provided in the **haddock/tools** directory that will calculate from the experimental dipolar coupling the tensor parameters for all PDB files present in the current directory by best-fitting the dipolar coupling tensor to the corresponding 3D structures.  

Usage:

<pre style="background-color:#DAE4E7">   $HADDOCK/tools/ana_pdb_Q-factor.csh pales.inp
</pre>

The output will be written to files with extension _PDBfilename.pales_.  
The tensor parameters Axx, Ayy and Azz can then be extracted with the following command:  

<pre style="background-color:#DAE4E7">    grep Axx *.pales | gawk '{print $4,$5,$6}' > xx-yy-zz.dat
</pre>

The components from the structure giving the best fit to the experimental data can be used.  
Alternatively, the average values can then be calculated with:  

<pre style="background-color:#DAE4E7">   cat xx-yy-zz.dat | awk '{print $1}' | $HADDOCKTOOLS/average.perl
   cat xx-yy-zz.dat | awk '{print $2}' | $HADDOCKTOOLS/average.perl
   cat xx-yy-zz.dat | awk '{print $3}' | $HADDOCKTOOLS/average.perl
</pre>

Check the values in xx-yy-zz.dat to make sure they match (e.g. same sign) before averaging them.  
Similarly, the axial (Da) and rhombic (Dr) components can be extracted from the Pales1.2 output files and averaged with the following command:  

<pre style="background-color:#DAE4E7">   grep Da *.pales | awk '{print $3}' | $HADDOCKTOOLS/average.perl
   grep Dr *.pales | awk '{print $3}' | $HADDOCKTOOLS/average.perl
</pre>

***Note:*** For use in HADDOCK (and CNS), the tensor components should be expressed in Hertz and the Pales values should be scaled depending on the nuclei observed. For example, for N-H residual dipolar coupling the proper scaling factor is 21700\. **Also be careful in the conversion since different programs often use different conventions/notations/units**.  

* * *

### Direct use of RDCs as restraints for docking 

The proper format for RDC restraints is the following:

<pre style="background-color:#DAE4E7">assi ( resid 999 and name OO )
     ( resid 999 and name Z  )
     ( resid 999 and name X  )
     ( resid 999 and name Y  )
     ( resid   20 and name N and segid A )
     ( resid   20 and name HN and segid A )   2.981   0.200
</pre>



Given a file containing _residue_number RDC_value_ and _Segid_ a RDC restraint file in CNS format can be generated with the gawk script _generate_sani_ provided in the **HADDOCK/RDCtools** directory:

<pre style="background-color:#DAE4E7">    $HADDOCK/RDCtools/generate_sani rdc_data_file
</pre>

The error on the RDCs is set by default to 0.2 Hz. This can be overruled by giving the error value as argument:

<pre style="background-color:#DAE4E7">    $HADDOCK/RDCtools/generate_sani ERR=0.4 rdc_data_file
</pre>

The 2.4 version of HADDOCK supports up to 5 different SANI restraints sets. Each can have a separate tensor. The tensor residue number should be in the range 999-995\. You can edit and modify the _generate_sani_ script to change the tensor number. To use RDC restraints in HADDOCK, use _SANI_ in [run.cns](/software/haddock2.4/run) in the dipolar coupling section and define the proper Da and R parameters (R=Dr/Da). The RDC restraints are first used in the [rigid body energy minimization step](/software/haddock2.4/protocol) using as force constant the value defined for the hot phase. Keep this value small (the current default is 0.02) to keep a proper balance between the AIR and SANI energy terms.  


The RDC restraints should be defined by the __RDCX_FILE__ parameter in the `run.param` file used to setup a run, with X being the number of the restraint set. An example entry in `run.param` would be:  

<pre style="background-color:#DAE4E7">
  RDC1_FILE=./restraints/ubiDP_vean_inter.tbl
  RDC2_FILE=./restraints/ubiDP_vean_intra.tbl
  RDC3_FILE=./restraints/ubiDP_sani.tbl
</pre>

Here the two first restraint sets corresponds to [VEAN restraints](#vean) and the third one to SANI restraints (example take from the `protein-protein-rdc` example provided with HADDOCK2.4).



***Note 1:*** Only one set (corresponding to one alignment tensor) of dipolar couplings can be used as direct restraints (SANI) in HADDOCK since currently only one alignment tensor is supported. Multiple sets can however be used as intervector projection angle restraints (see below).

***Note 2:*** For proper docking results, dipolar couplings restraints of the various molecules should be input as one set (and thus not split in separate sets for each molecule). The assumption here is that the RDCs of the various components share one common alignment tensor.


* * *

### Intervector projection angle restraints for docking  

Intervector projection angle restraints ( [Meiler et al. _J. Biomol. NMR_ **17**, 185 (2000)](http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&db=PubMed&list_uids=10805131&dopt=Abstract){:target="_blank"}) are obtained by taking pairs of residual dipolar couplings and generating intervector projection angle restraints (somewhat equivalent to dihedral angle restraints). These restraints have the advantage that they do no longer depend on the orientation of the dipole vector with respect to the alignment tensor. Instead they restrain the angle between two dipolar vectors, allowing for two minima. Two force constants must be therefore defined: one for the border potential function and one for the central part (e.g. between the two minima).

Thanks to Helen Mott and Wayne Boucher from Cambridge University we are providing in the **HADDOCK/RDCtools** a python script, _dipole_segid.py_ that allows the generation of such restraints from RDC data. To use it, you need to have your RDC data in a tab separated file containing _residue_number, RDC_value_ and _Segid_ and provide the tensor components Dxx, Dyy and Dzz (in Hertz). For NH couplings, these components are equal to 21700 times the eigenvalues of the Saupe matrix given by Pales.

Usage:

<pre style="background-color:#DAE4E7">    python $HADDOCK/RDCtools/dipolar_segid.py rdc_data_file vean_output_file Dxx Dyy Dzz
</pre>

The resulting restraints file looks like:

<pre style="background-color:#DAE4E7">    assign (resid 19 and name N and segid     B ) (resid 19 and name HN and segid     B ) (resid 27 and name N and segid     B ) (resid 27 and name HN and segid     B ) 13.1 2.9 166.9 2.9 ! excluded 0.935
    assign (resid 75 and name N and segid     A ) (resid 75 and name HN and segid     A ) (resid 27 and name N and segid     B ) (resid 27 and name HN and segid     B ) 13.1 2.9 166.9 2.9 ! excluded 0.935
</pre>

The last column gives the fraction of angular space excluded by the restraint and can be used to select "significant" restraints, e.g. limiting more than 25% of the torsional space. Note that the number of restraints generated is very high since for N dipolar coupling there are N*(N-1) possible combinations.  
To select for example all inter- and intra-molecular restraint excluding more than 25% of the angular space type:

<pre style="background-color:#DAE4E7">    awk '{if ($27 == $9 && $44 > 0.25) {print $0}}' vean_output_file >vean_intra_25.tbl
    awk '{if ($27 != $9 && $44 > 0.25) {print $0}}' vean_output_file >vean_inter_25.tbl
</pre>

To use intervector projection angle restraints in HADDOCK, use _VANGLE_ in [run.cns](/software/haddock2.4/run) in the dipolar coupling section. The VANGLE restraints are introduced in the [rigid body energy minimization step](/software/haddock2.4/protocol) using as initial force constants the value defined for the hot phase. The restraints are activated in the second rotational minimization phase (thus earlier than the SANI restraints!)


The VEAN RDC restraints should be defined by the __RDCX_FILE__ parameter in the `run.param` file used to setup a run, with X being the number of the restraint set. An example entry in `run.param` would be:  

<pre style="background-color:#DAE4E7">
  RDC1_FILE=./restraints/ubiDP_vean_inter.tbl
  RDC2_FILE=./restraints/ubiDP_vean_intra.tbl
  RDC3_FILE=./restraints/ubiDP_sani.tbl
</pre>

Here the two first restraint sets corresponds to VEAN restraints and the third one to SANI restraints (example taken from the `protein-protein-rdc` example provided with HADDOCK2.4).


* * *
