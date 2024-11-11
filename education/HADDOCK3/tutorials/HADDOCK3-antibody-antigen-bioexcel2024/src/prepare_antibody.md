### Preparing the antibody structure

Using PDB-tools we will download the unbound structure of the antibody from the PDB database (the PDB ID is [4G6K](https://www.ebi.ac.uk/pdbe/entry/pdb/4g6k)) and then process it to have a unique chain ID (A) and non-overlapping residue numbering by renumbering the merged pdb (starting from 1).

This can be done from the command line with:

<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy \-strict | pdb_selchain \-H | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_selres \-1:120 | pdb_tidy -strict > 4G6K_H.pdb
</a>
<a class="prompt prompt-cmd">
pdb_fetch 4G6K | pdb_tidy \-strict | pdb_selchain -L | pdb_delhetatm | pdb_fixinsert | pdb_keepcoord | pdb_selres \-1:107 | pdb_tidy \-strict > 4G6K_L.pdb
</a>
<a class="prompt prompt-cmd">
pdb_merge 4G6K_H.pdb 4G6K_L.pdb | pdb_reres \-1 | pdb_chain \-A | pdb_chainxseg | pdb_tidy \-strict > 4G6K_clean.pdb
</a>

The first command fetches the PDB ID, selects the heavy chain (H) (`pdb_selchain`) and removes water and heteroatoms (`pdb_delhetatm`) (in this case no co-factor is present that should be kept).

An important part for antibodies is the `pdb_fixinsert` command that fixes the residue numbering of the HV loops: Antibodies often follow the [Chothia numbering scheme](https://pubmed.ncbi.nlm.nih.gov/9367782/?otool=inluulib) and insertions created by this numbering scheme (e.g. 82A, 82B, 82C) cannot be processed by HADDOCK directly (if not done those residues will not be considered resulting effectively in a break in the loop).
As such, renumbering is necessary before starting the docking. 

Then, the command `pdb_selres` selects only the residues from 1 to 120, so as to consider only the variable domain (FV) of the antibody. This allows to save a substantial amount of computational resources.

The second command does the same for the light chain (L) with the difference that the light chain is slightly shorter and we can focus on the first 107 residues.

The third and last command merges the two processed chains, renumber the residues starting from 1 (`pdb_reres`) and assign them unique chain and segIDs (`pdb_chain` and `pdb_chainxseg`), resulting in the HADDOCK-ready `4G6K_clean.pdb` file. You can view its sequence by running:

<a class="prompt prompt-cmd">
pdb_tofasta 4G6K_clean.pdb
</a>

_**Note**_ The ready-to-use file can be found in the `pdbs` directory of the provided tutorial data.
