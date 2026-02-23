## Preparing PDB files for docking

In this section we will prepare the PDB files of the antibody and antigen for docking.
Crystal structures of both the antibody and the antigen in their free forms are available from the
[PDBe database](https://www.pdbe.org){:target="_blank"}. 

__Important:__ For a docking run with HADDOCK, each molecule should consist of a single chain with non-overlapping residue numbering within the same chain.

As an antibody consists of two chains (L+H), we will have to prepare it for use in HADDOCK. For this we will be making use of `pdb-tools` from the command line.

_**Note**_ that `pdb-tools` is also available as a [web service](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.
