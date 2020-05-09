---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK2.4</font> manual

## <font color="RED">U</font>sing <font color="RED">P</font>seudo <font color="RED">C</font>ontact <font color="RED">S</font>hifts

* * *

Pseudo contact shifts (PCS) can provide useful information on both the distances and the orientation of the molecules to be docked. They can be used directly as restraints in HADDOCK using the XPCS energy term in CNS. Note that for this the standard CNS version needs to be recompiled with the files provided in the cns1.3 directory in the HADDOCK distribution.  

For each set of PCS restraints used, a tensor must be defined. Its axial (D) and rhombic (R) components must be defined.

**Note** that the proper units for use in HADDOCK should be: 10<sup>-28</sup> / (12*pi) m<sup>3</sup> (which gives a scaling factor of 265.26 compared to values expressed in 10<sup>-32</sup> m<sup>3</sup>)

For pseudo contact shifts, R and D this can be obtained using for example the [Numbat](http://www.nmr.chem.uu.nl/~christophe/numbat.html){:target="_blank"} software (Schmitz C, Stanton-Cook MJ, Su XC, Otting G, Huber T (2008) Numbat: an interactive software tool for fitting delta chi-tensors to molecular coordinates using pseudocontact shifts. _J Biomol NMR_ **41**:179-189).  

The position of the tensor also needs to be defined by specifying distance restraints with respect to the protein to which it is attached. These restraints should be defined by the TENSOR_FILE in the `run.param` file used to setup a run. The entry in `run.param` looks like:  

<pre style="background-color:#DAE4E7">
  TENSOR_FILE=tensor_basic.tbl
</pre>

and this tensor restraint file contains distance restraints. For example, if the tensor is attached to a metal ion in the case of a metallo-protein (as in the protein-protein-pcs example in HADDOCK2.4) it looks like:  

<pre style="background-color:#DAE4E7">assi (resid  999 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
assi (resid  998 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
assi (resid  997 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
assi (resid  996 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
assi (resid  995 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
assi (resid  994 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
assi (resid  993 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
assi (resid  992 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
assi (resid  991 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
assi (resid  990 and resn XAN and name  OO ) (resid 190 and segid A ) 0.0 0.0 0.0
</pre>

The distances are thus all set to 0 to keep the tensor on top of the metal ion. 10 such distances are defined, one for each PCS set and its associated tensor (numbered from 990 to 999).  

The proper format for PCS restraints is the following:

<pre style="background-color:#DAE4E7">assign ( resid 999  and name OO )
       ( resid 999  and name Z )
       ( resid 999  and name X )
       ( resid 999  and name Y )
       ( resid 7 and name N and segid A ) -0.119906 0.15
</pre>

where the last two numbers are the PCS value and its associated error.  


The 2.4 version of HADDOCK supports up to 10 differentPCS restraints sets. Each can have a separate tensor. The tensor residue number should be in the range 999-990. For each class you can specify the first and last stage at which the various RDCs will be used:

*   0: rigid body EM (it0)
*   1: semi-flexible simulated annealing (SA) (it1)
*   2: explicit solvent refinement (water)


The PCS restraints should be defined by the __PCSX_FILE__ parameter in the `run.param` file used to setup a run, with X being the number of the restraint set. An example entry in `run.param` would be:  

<pre style="background-color:#DAE4E7">
  PCS1_FILE=./DATA/Dy_eps_HOT_0.15_.tbl
  PCS2_FILE=./DATA/Er_eps_HOT_0.15_.tbl
  PCS3_FILE=./DATA/Tb_eps_HOT_0.15_.tbl
  TENSOR_FILE=./DATA/tensor_basic.tbl
</pre>


Example taken from the `protein-protein-pcs` example provided with HADDOCK2.4.



* * *
