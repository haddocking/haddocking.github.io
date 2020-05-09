---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK2.4</font> manual

## <font color="RED">U</font>sing <font color="RED">D</font>iffusion <font color="RED">A</font>nisotropy <font color="RED">D</font>ata

* * *

Diffusion anisotropy data (relaxation data) can provide useful information on the orientation of the molecules to be docked (comparable to RDCs). They can be introduced in HADDOCK as direct restraints (DANI statement in CNS).  
For this, the tensor components need first to be determined. In the case of complexes, this can be easily done by using the known structures of the single domains. The software [Tensor2](https://www.ibs.fr/research/scientific-output/software/tensor/){:target="_blank"} (Dosset, Marion and Blackledge (2000). _J. Biomol. NMR_ **16**, 23-28) can be used for this purpose.  

You need for this to generate a Tensor2 input file containing your relaxation data.  

A csh script called *uname -pana_pdb_tensor2.csh* is provided in the **haddock/DANItools** directory that will calculate from the experimental relaxation data the tensor parameters for all PDB files present in the current directory by best-fitting the data to the corresponding 3D structures.  

Usage:  

<pre style="background-color:#DAE4E7" >   $HADDOCK/DANItools/ana_pdb_tensor2.csh tensor2.inp
</pre>

Note that you have to define the fitting options in the tensor2 GUI manually. Tensor2 writes its output for each structure to a file called _resaniso.0_; each of these are moved to a subdirectory with directory name equal to the corresponding pdb file.  

The script extracts the tensor parameters Dx, Dy and Dz and the chi2-value of the fit; these can be combined with the following command:  

<pre style="background-color:#DAE4E7" >    paste D?_all.tmp chi2_all.tmp | awk '{print $1,$8,$16,$24,$27*100/100}' | sort -n +4 > tensor2_fit.lis
</pre>

The components from the structure giving the best fit to the experimental data can be used to calculate the tensor parameters that are needed in run.cns with the script _calc_tens.csh_ (provided in the **haddock/DANItools** directory).  

Usage:  

<pre style="background-color:#DAE4E7" >    $HADDOCK/DANItools/calc_tens.csh dx dy dz
</pre>

Where dx, dy and dz are the values from the file _tensor2_fit.lis_. The output of _calc_tens.csh_ can be used directly in run.cns as _dan1_tc_, _dan1_anis_ and _dan1_r_, the rotational correlation time, anisotropy and rhombicity of the rotational diffusion tensor, respectively. Alternatively, average values could be used; these can be calculated with:  

<pre style="background-color:#DAE4E7" >   cat tensor2_fit.lis | awk '{print $2}' | $HADDOCKTOOLS/average.perl
   cat tensor2_fit.lis | awk '{print $3}' | $HADDOCKTOOLS/average.perl
   cat tensor2_fit.lis | awk '{print $4}' | $HADDOCKTOOLS/average.perl
</pre>

Check the values in tensor2_fit.lis to make sure they match (e.g. same sign) before averaging them. Also make sure that an anisotropic model is in accordance with your data.  

<a name="dani">**<u>Use of relaxation data as restraints for docking</u>**</a>  

The proper format for DANI restraints is the following:  

<pre style="background-color:#DAE4E7" >assi ( resid 999 and name OO )
     ( resid 999 and name Z  )
     ( resid 999 and name X  )
     ( resid 999 and name Y  )
     ( resid   20 and name N and segid A )
     ( resid   20 and name HN and segid A )   8.705   0.200
</pre>

The restraints use the R2/R1 value; one should filter out residues where chemical exchange or mobility influences these values. Given a file containing _residue_number R2/R1value_ and _Segid_ a DANI restraint file in CNS format can be generated with the gawk script _generate_dani_ provided in the **HADDOCK/DANItools** directory:  

<pre style="background-color:#DAE4E7" >    $HADDOCK/DANItools/generate_dani dani_data_file
</pre>

The error on the R2/R1 values is set by default to 0.2\. This can be overruled by giving the error value as argument:  

<pre style="background-color:#DAE4E7" >    $HADDOCK/DANItools/generate_dani ERR=0.5 dani_data_file
</pre>

The 2.4 version of HADDOCK supports up to 5 different DANI restraints sets. Each can have a separate tensor. The tensor residue number should be in the range 999-995\. You can edit and modify the _generate_dani_ script to change the tensor number. To use DANI restraints in HADDOCK, use _DANI_ in [run.cns](/software/haddock2.4/run) in the diffusion anisotropy section and define the proper tensor parameters that are output by the _calc_tens.csh_ script. The DANI restraints are first used in the [rigid body energy minimization step](/software/haddock2.4/protocol) using as force constant the value defined for the hot phase.



The DANI restraints should be defined by the __DANIX_FILE__ parameter in the `run.param` file used to setup a run, with X being the number of the restraint set. An example entry in `run.param` would be:  

<pre style="background-color:#DAE4E7">
  DANI1_FILE=./dani.tbl
</pre>

Example taken from the `protein-protein-dani` example provided with HADDOCK2.4.





* * *
