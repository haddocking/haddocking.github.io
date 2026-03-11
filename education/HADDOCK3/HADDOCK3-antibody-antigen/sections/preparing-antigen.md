### Preparing the antigen structure

Using PDB-tools, we will now download the unbound structure of Interleukin-1β from the PDB database (the PDB ID is [4I1B](https://www.ebi.ac.uk/pdbe/entry/pdb/4i1b){:target="_blank"}), 
remove the hetero atoms and then process it to assign it chainID B.

*__Important__: Each molecule given to HADDOCK in a docking scenario must have a unique chainID/segID.*

<a class="prompt prompt-cmd">
pdb_fetch 4I1B | pdb_tidy \-strict | pdb_delhetatm  | pdb_selaltloc | pdb_keepcoord | pdb_chain \-B | pdb_chainxseg | pdb_tidy \-strict > 4I1B_clean.pdb
</a>
