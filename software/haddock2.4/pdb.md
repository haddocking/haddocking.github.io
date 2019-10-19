---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK2.4</font> manual

##   <font color="RED">PDB</font>files 

* * *

In order to run HADDOCK you need to have the structures of the molecules (or fragments thereof) in PDB format. There are a few points to pay attention to when preparing the PDBs for HADDOCK.

*   Make sure that all PDB files end with an END statement

*   HADDOCK will check from breaks in the chain (e.g. missing density in crystal structures or between the two strands of a DNA molecules). In the case of multiple chains within one molecule (e.g. DNA) or in the presence of co-factors, it is however recommended to add a TER statement in between the chains/sub-molecules.

*   Remove the SEGIDs if present (the SEGID is a four character long string at columns 73-76 in the PDB format. This is particularly important for docking from an ensemble of starting conformations. If not blanked, the [topology and structure generation step](/software/haddock2.4/docking#topology) will give problems.

    For this purpose an awk script called **_pdb_blank_segid_** is provided in the **tools** directory. Its usage is:

<pre style="background-color:#DAE4E7" >    pdb_blank_segid infile > outfile
</pre>

*   When starting from an ensemble of structure like, for example, from an NMR PDB entry, split structures into single PDB files. Make sure that each structure file ends with an END statement and does not contain any SEGID.

*   HADDOCK can deal with ions. You will have however to make sure that the ion naming is consistent with the ion topologies provided in HADDOCK (check for this the **_ion.top_** file in the **toppar** directory. For example, a CA heteroatom with residue name CA will be interpreted as a neutral calcium atom. A doubly charged calcium ion should be name CA+2 with as residue name CA2 to be properly recognized by HADDOCK.

    (See also the [FAQ](/software/haddock2.4/faq#ions) for docking in the presence of ions).

* * *
