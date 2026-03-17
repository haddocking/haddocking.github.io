### Preparing the antibody structure

Using PDB-tools we will download the unbound structure of the antibody from the PDB database (the PDB ID is [4G6K](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k){:target="_blank"}) 
and then process it to have a unique chain ID (A) and non-overlapping residue numbering by renumbering the merged pdb (starting from 1). For this we will concatenate the following PDB-tools commands:

1. fetch the PDB entry from the PDB database (`pdb_fetch`)
2. clean the PDB file (`pdb_tidy`)
3. select the chain (`pdb_selchain`),
4. remove any hetero atoms from the structure (e.g. crystal waters, small molecules from the crystallisation buffer and such) (`pdb_delhetatm`),
5. fix residue numbering insertion in the HV loops (often occuring in antibodies - see note below) (`pdb_fixinsert`)
6. remove any possible side-chain duplication (can be present in high-resolution crystal structures in case of multiple conformations of some side chains) (`pdb_selaltloc`)
7. keep only the coordinates lines (`pdb_keepcoord`),
8. select only the variable domain (FV) of the antibody (to reduce computing time) (`pdb_selres`)
9. clean the PDB file (`pdb_tidy`)

**_Note_** that the `pdb_tidy -strict` commands cleans the PDB file, add TER statements only between different chains). 
Without the -strict option TER statements would be added between each chain break (e.g. missing residues), which should be avoided.

**_Note_**: An important part for antibodies is the `pdb_fixinsert` command that fixes the residue numbering of the HV loops: 
Antibodies often follow the [Chothia numbering scheme](https://pubmed.ncbi.nlm.nih.gov/9367782/?otool=inluulib){:target="_blank"} 
and insertions created by this numbering scheme (e.g. 82A, 82B, 82C) cannot be processed by HADDOCK directly 
(if not done those residues will not be considered resulting effectively in a break in the loop).
As such, renumbering is necessary before starting the docking. 


This can be done from the command line with:

<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy \-strict | pdb_selchain \-H | pdb_delhetatm | pdb_fixinsert | pdb_selaltloc | pdb_keepcoord | pdb_selres \-1:120 | pdb_tidy -strict > 4G6K_H.pdb
</a>
<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy \-strict | pdb_selchain -L | pdb_delhetatm | pdb_fixinsert | pdb_selaltloc | pdb_keepcoord | pdb_selres \-1:107 | pdb_tidy \-strict > 4G6K_L.pdb
</a>

We then combined the heavy and light chain into one, renumbering the residues starting at 1 to avoid overlap in residue numbering between the chains and assigning a unique chainID/segID:

<a class="prompt prompt-cmd">
pdb_merge 4G6K_H.pdb 4G6K_L.pdb | pdb_reres \-1 | pdb_chain \-A | pdb_chainxseg | pdb_tidy \-strict > 4G6K_clean.pdb
</a>

_**Note**_ The ready-to-use file can be found in the `pdbs` directory of the provided tutorial data.
