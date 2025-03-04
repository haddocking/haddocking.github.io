# PDB-Tools

PDB-tool is set of python scripts dedicated at manipulating PDB files, select and rename chains and segids, renumber residues... and much more! ([Rodrigues et al. *F1000 Research* (2018)](https://doi.org/10.12688/f1000research.17456.1))
The source code can be obtain from its [GitHub repository](https://github.com/haddocking/pdb-tools).
Alternatively you can also make use of our new [PDB-tools webserver](https://wenmr.science.uu.nl/pdbtools/).

In addition, it comes as one of the dependencies installed by default in your haddock3 environement.
Therefore, once the environement is activated, you will be able to access all the functionalities from the command line.

Here is a list of all available command line interface installed together with haddock3:

- [pdb_b](#pdb_b): Modifies the temperature factor column of a PDB file (default 10.0).
- [pdb_head](#pdb_head): Returns the first N coordinate (ATOM/HETATM) lines of the file.
- [pdb_rplchain](#pdb_rplchain): Performs in-place replacement of a chain identifier by another.
- [pdb_selhetatm](#pdb_selhetatm): Selects all HETATM records in the PDB file.
- [pdb_splitmodel](#pdb_splitmodel): Splits a PDB file into several, each containing one MODEL.
- [pdb_chain](#pdb_chain): Modifies the chain identifier column of a PDB file (default is an empty chain).
- [pdb_delres](#pdb_delres): Deletes a range of residues from a PDB file.
- [pdb_intersect](#pdb_intersect): Returns a new PDB file only with atoms in common to all input PDB files.
- [pdb_rplresname](#pdb_rplresname): Performs in-place replacement of a residue name by another.
- [pdb_selmodel](#pdb_selmodel): Extracts one or more models from a PDB file.
- [pdb_splitseg](#pdb_splitseg): Splits a PDB file into several, each containing one segment.
- [pdb_chainbows](#pdb_chainbows): 
- [pdb_delresname](#pdb_delresname): Removes all residues matching the given name in the PDB file.
- [pdb_keepcoord](#pdb_keepcoord): Removes all non-coordinate records from the file.
- [pdb_seg](#pdb_seg): Modifies the segment identifier column of a PDB file (default is an empty segment).
- [pdb_selres](#pdb_selres): Selects residues by their index, piecewise or in a range.
- [pdb_tidy](#pdb_tidy): Modifies the file to adhere (as much as possible) to the format specifications.
- [pdb_chainxseg](#pdb_chainxseg): Swaps the segment identifier for the chain identifier.
- [pdb_element](#pdb_element): Assigns the elements in the PDB file from atom names.
- [pdb_merge](#pdb_merge): Merges several PDB files into one.
- [pdb_segxchain](#pdb_segxchain): Swaps the chain identifier by the segment identifier.
- [pdb_selresname](#pdb_selresname): Selects all residues matching the given name in the PDB file.
- [pdb_tocif](#pdb_tocif): Rudimentarily converts the PDB file to mmCIF format.
- [pdb_chkensemble](#pdb_chkensemble): Checks all models in a multi-model PDB file have the same composition.
- [pdb_fetch](#pdb_fetch): Downloads a structure in PDB format from the RCSB website.
- [pdb_mkensemble](#pdb_mkensemble): Merges several PDB files into one multi-model (ensemble) file.
- [pdb_selaltloc](#pdb_selaltloc): Selects altloc labels for the entire PDB file.
- [pdb_selseg](#pdb_selseg): Selects all atoms matching the given segment identifier.
- [pdb_tofasta](#pdb_tofasta): Extracts the residue sequence in a PDB file to FASTA format.
- [pdb_delchain](#pdb_delchain): Deletes all atoms matching specific chains in the PDB file. 
- [pdb_fixinsert](#pdb_fixinsert): Fixes insertion codes in a PDB file.
- [pdb_occ](#pdb_occ): Modifies the occupancy column of a PDB file (default 1.0).
- [pdb_selatom](#pdb_selatom): Selects all atoms matching the given name in the PDB file.
- [pdb_shiftres](#pdb_shiftres): Shifts the residue numbers in the PDB file by a constant value.
- [pdb_uniqname](#pdb_uniqname): Renames atoms sequentially (C1, C2, O1, ...) for each HETATM residue.
- [pdb_delelem](#pdb_delelem): Deletes all atoms matching the given element in the PDB file.
- [pdb_fromcif](#pdb_fromcif): Rudimentarily converts a mmCIF file to the PDB format.
- [pdb_reatom](#pdb_reatom): Renumbers atom serials in the PDB file starting from a given value (default 1).
- [pdb_selchain](#pdb_selchain): Extracts one or more chains from a PDB file.
- [pdb_sort](#pdb_sort): Sorts the ATOM/HETATM/ANISOU/CONECT records in a PDB file.
- [pdb_validate](#pdb_validate): Validates the PDB file ATOM/HETATM lines according to the format specifications.
- [pdb_delhetatm](#pdb_delhetatm): Removes all HETATM records in the PDB file.
- [pdb_gap](#pdb_gap): Finds gaps between consecutive protein residues in the PDB.
- [pdb_reres](#pdb_reres): Renumbers the residues of the PDB file starting from a given number (default 1).
- [pdb_selelem](#pdb_selelem): Selects all atoms that match the given element(s) in the PDB file.
- [pdb_splitchain](#pdb_splitchain): Splits a PDB file into several, each containing one chain.
- [pdb_wc](#pdb_wc): Summarizes the contents of a PDB file, like the wc command in UNIX.



## pdb_b

Modifies the temperature factor column of a PDB file (default 10.0).

```bash
Usage:
    python pdb_b.py -<bfactor> <pdb file>

Example:
    python pdb_b.py -10.0 1CTF.pdb
```



## pdb_head

Returns the first N coordinate (ATOM/HETATM) lines of the file.

```bash
Usage:
    python pdb_head.py -<num> <pdb file>

Example:
    python pdb_head.py -100 1CTF.pdb  # first 100 ATOM/HETATM lines of the file
```


## pdb_rplchain

Performs in-place replacement of a chain identifier by another.

```bash
Usage:
    python pdb_rplchain.py -<from>:<to> <pdb file>

Example:
    python pdb_rplchain.py -A:B 1CTF.pdb # Replaces chain A for chain B
```


## pdb_selhetatm

Selects all HETATM records in the PDB file.

```bash
Usage:
    python pdb_selhetatm.py <pdb file>

Example:
    python pdb_selhetatm.py 1CTF.pdb
```


## pdb_splitmodel

Splits a PDB file into several, each containing one MODEL.

```bash
Usage:
    python pdb_splitmodel.py <pdb file>

Example:
    python pdb_splitmodel.py 1CTF.pdb
```


## pdb_chain

Modifies the chain identifier column of a PDB file (default is an empty chain).

```bash
Usage:
    python pdb_chain.py -<chain id> <pdb file>

Example:
    python pdb_chain.py -C 1CTF.pdb
```


## pdb_delres

Deletes a range of residues from a PDB file.

The range option has three components: start, end, and step. Start and end
are optional and if ommitted the range will start at the first residue or
end at the last, respectively. The step option can only be used if both start
and end are provided. Note that the start and end values of the range are
purely numerical, while the range actually refers to every N-th residue,
regardless of their sequence number.

```bash
Usage:
    python pdb_delres.py -[resid]:[resid]:[step] <pdb file>

Example:
    python pdb_delres.py -1:10 1CTF.pdb # Deletes residues 1 to 10
    python pdb_delres.py -1: 1CTF.pdb # Deletes residues 1 to END
    python pdb_delres.py -:5 1CTF.pdb # Deletes residues from START to 5.
    python pdb_delres.py -::5 1CTF.pdb # Deletes every 5th residue
    python pdb_delres.py -1:10:5 1CTF.pdb # Deletes every 5th residue from 1 to 10
```


## pdb_intersect

Returns a new PDB file only with atoms in common to all input PDB files.

Atoms are judged equal is their name, altloc, res. name, res. num, insertion
code and chain fields are the same. Coordinates are taken from the first input
file. Keeps matching TER/ANISOU records.

```bash
Usage:
    python pdb_intersect.py <pdb file> <pdb file>

Example:
    python pdb_intersect.py 1XYZ.pdb 1ABC.pdb
```


## pdb_rplresname

Performs in-place replacement of a residue name by another.

Affects all residues with that name.

```bash
Usage:
    python pdb_rplresname.py -<from>:<to> <pdb file>

Example:
    python pdb_rplresname.py -HIP:HIS 1CTF.pdb  # changes all HIP residues to HIS
```


## pdb_selmodel

Extracts one or more models from a PDB file.

If the PDB file has no MODEL records, returns the entire file.

```bash
Usage:
    python pdb_selmodel.py -<model id> <pdb file>

Example:
    python pdb_selmodel.py -1 1GGR.pdb  # selects model 1
    python pdb_selmodel.py -1,3 1GGR.pdb  # selects models 1 and 3
```


## pdb_splitseg

Splits a PDB file into several, each containing one segment.

```bash
Usage:
    python pdb_splitseg.py <pdb file>

Example:
    python pdb_splitseg.py 1CTF.pdb
```


## pdb_chainbows

Renames chain identifiers sequentially, based on TER records.

Since HETATM records are not separated by TER records and usually come together at the end of the PDB file, this script will attempt to reassign their chain identifiers based on the changes it made to ATOM lines.
This might lead to bad
output in certain corner cases.

```bash
Usage:
    python pdb_chainbows.py <pdb file>

Example:
    python pdb_chainbows.py 1CTF.pdb
```


## pdb_delresname

Removes all residues matching the given name in the PDB file.

Residues names are matched *without* taking into consideration spaces.

```bash
Usage:
    python pdb_delresname.py -<option> <pdb file>

Example:
    python pdb_delresname.py -ALA 1CTF.pdb  # removes only Alanines
    python pdb_delresname.py -ASP,GLU 1CTF.pdb  # removes (-) charged residues
```


## pdb_keepcoord

Removes all non-coordinate records from the file.

Keeps only MODEL, ENDMDL, END, ATOM, HETATM, CONECT.

```bash
Usage:
    python pdb_keepcoord.py <pdb file>

Example:
    python pdb_keepcoord.py 1CTF.pdb
```


## pdb_seg

Modifies the segment identifier column of a PDB file (default is an empty segment).

```bash
Usage:
    python pdb_seg.py -<segment id> <pdb file>

Example:
    python pdb_seg.py -C 1CTF.pdb
```


## pdb_selres

Selects residues by their index, piecewise or in a range.

The range option has three components: start, end, and step. Start and end
are optional and if ommitted the range will start at the first residue or
end at the last, respectively.

```bash
Usage:
    python pdb_selres.py -[resid]:[resid]:[step] <pdb file>

Example:
    python pdb_selres.py -1,2,4,6 1CTF.pdb # Extracts residues 1, 2, 4 and 6
    python pdb_selres.py -1:10 1CTF.pdb # Extracts residues 1 to 10
    python pdb_selres.py -1:10,20:30 1CTF.pdb # Extracts residues 1 to 10 and 20 to 30
    python pdb_selres.py -1: 1CTF.pdb # Extracts residues 1 to END
    python pdb_selres.py -:5 1CTF.pdb # Extracts residues from START to 5.
    python pdb_selres.py -::5 1CTF.pdb # Extracts every 5th residue
    python pdb_selres.py -1:10:5 1CTF.pdb # Extracts every 5th residue from 1 to 10
```


## pdb_tidy

Modifies the file to adhere (as much as possible) to the format specifications.

Expects a sorted file - REMARK/ATOM/HETATM/END - so use pdb_sort in case you are
not sure.

This includes:
    - Adding TER statements after chain breaks/changes
    - Truncating/Padding all lines to 80 characters
    - Adds END statement at the end of the file

Will remove all original TER/END statements from the file.

```bash
Usage:
    python pdb_tidy.py [-strict] <pdb file>

Example:
    python pdb_tidy.py 1CTF.pdb
    python pdb_tidy.py -strict 1CTF.pdb  # does not add TER on chain breaks
```


## pdb_chainxseg

Swaps the segment identifier for the chain identifier.

```bash
Usage:
    python pdb_chainxseg.py <pdb file>

Example:
    python pdb_chainxseg.py 1CTF.pdb
```


## pdb_element

Assigns the elements in the PDB file from atom names.

```bash
Usage:
    python pdb_element.py <pdb file>

Example:
    python pdb_element.py 1CTF.pdb
```


## pdb_merge

Merges several PDB files into one.

The contents are not sorted and no lines are deleted (e.g. END, TER
statements) so we recommend piping the results through `pdb_tidy.py`.

```bash
Usage:
    python pdb_merge.py <pdb file> <pdb file>

Example:
    python pdb_merge.py 1ABC.pdb 1XYZ.pdb
```


## pdb_segxchain

Swaps the chain identifier by the segment identifier.

If the segment identifier is longer than one character, the script will truncate it.
Does not ensure unique chain IDs.

```bash
Usage:
    python pdb_segxchain.py <pdb file>

Example:
    python pdb_segxchain.py 1CTF.pdb
```


## pdb_selresname

Selects all residues matching the given name in the PDB file.

Residues names are matched *without* taking into consideration spaces.

```bash
Usage:
    python pdb_selresname.py -<option> <pdb file>

Example:
    python pdb_selresname.py -ALA 1CTF.pdb  # keeps only Alanines
    python pdb_selresname.py -ASP,GLU 1CTF.pdb  # keeps (-) charged residues
```


## pdb_tocif

Rudimentarily converts the PDB file to mmCIF format.

Will convert only the coordinate section.

```bash
Usage:
    python pdb_tocif.py <pdb file>

Example:
    python pdb_tocif.py 1CTF.pdb
```


## pdb_chkensemble

Checks all models in a multi-model PDB file have the same composition.

Composition is defined as same atoms/residues/chains.

```bash
Usage:
    python pdb_chkensemble.py <pdb file>

Example:
    python pdb_chkensemble.py 1CTF.pdb
```


## pdb_fetch

Downloads a structure in PDB format from the RCSB website.

Allows downloading the (first) biological structure if selected.

```bash
Usage:
    python pdb_fetch.py [-biounit] <pdb code>

Example:
    python pdb_fetch.py 1brs  # downloads unit cell, all 6 chains
    python pdb_fetch.py -biounit 1brs  # downloads biounit, 2 chains
```


## pdb_mkensemble

Merges several PDB files into one multi-model (ensemble) file.

Strips all HEADER information and adds REMARK statements with the provenance
of each conformer.

```bash
Usage:
    python pdb_mkensemble.py <pdb file> <pdb file>

Example:
    python pdb_mkensemble.py 1ABC.pdb 1XYZ.pdb
```


## pdb_selaltloc

Selects altloc labels for the entire PDB file.

By default, selects the label with the highest occupancy value for each atom,
but the user can define a specific altloc label to select.

Selecting by highest occupancy removes all altloc labels for all atoms. If the
user provides an option (e.g. -A), only atoms with conformers with an altloc A
are processed by the script. If you select -A and an atom has conformers with
altlocs B and C, both B and C will be kept in the output.

```bash
Usage:
    python pdb_selaltloc.py [-<option>] <pdb file>

Example:
    python pdb_selaltloc.py 1CTF.pdb  # picks locations with highest occupancy
    python pdb_selaltloc.py -A 1CTF.pdb  # picks alternate locations labelled 'A'
```


## pdb_selseg

Selects all atoms matching the given segment identifier.

```bash
Usage:
    python pdb_selseg.py -<segment id> <pdb file>

Example:
    python pdb_selseg.py -C 1CTF.pdb  # selects segment C
    python pdb_selseg.py -C,D 1CTF.pdb  # selects segments C and D
```


## pdb_tofasta

Extracts the residue sequence in a PDB file to FASTA format.

Canonical amino acids and nucleotides are represented by their
one-letter code while all others are represented by 'X'.

The -multi option splits the different chains into different records in the
FASTA file.

```bash
Usage:
    python pdb_tofasta.py [-multi] <pdb file>

Example:
    python pdb_tofasta.py 1CTF.pdb
```


## pdb_delchain

Deletes all atoms matching specific chains in the PDB file.

```bash
Usage:
    python pdb_delchain.py -<option> <pdb file>

Example:
    python pdb_delchain.py -A 1CTF.pdb  # removes chain A from PDB file
    python pdb_delchain.py -A,B 1CTF.pdb  # removes chains A and B from PDB file
```


## pdb_fixinsert

Fixes insertion codes in a PDB file.

Works by deleting an insertion code and shifting the residue numbering of downstream residues.
Allows for picking specific residues to delete insertion codes for.

```bash
Usage:
    python pdb_fixinsert.py [-<option>] <pdb file>

Example:
    python pdb_fixinsert.py 1CTF.pdb  # delete ALL insertion codes
    python pdb_fixinsert.py -A9,B12 1CTF.pdb  # deletes ins. codes for res
                                              # 9 of chain A and 12 of chain B.
```


## pdb_occ

Modifies the occupancy column of a PDB file (default 1.0).

```bash
Usage:
    python pdb_occ.py -<occupancy> <pdb file>

Example:
    python pdb_occ.py -1.0 1CTF.pdb
```


## pdb_selatom

Selects all atoms matching the given name in the PDB file.

Atom names are matched *without* taking into consideration spaces, so ' CA ' (alpha carbon) and 'CA  ' (calcium) will both be kept if -CA is passed.

```bash
Usage:
    python pdb_selatom.py -<option> <pdb file>

Example:
    python pdb_selatom.py -CA 1CTF.pdb  # keeps only alpha-carbon atoms
    python pdb_selatom.py -CA,C,N,O 1CTF.pdb  # keeps only backbone atoms
```


## pdb_shiftres

Shifts the residue numbers in the PDB file by a constant value.

```bash
Usage:
    python pdb_shiftres.py -<number> <pdb file>

Example:
    python pdb_shiftres.py -10 1CTF.pdb  # adds 10 to the original numbering
    python pdb_shiftres.py --5 1CTF.pdb  # subtracts 5 from the original numbering
```


## pdb_uniqname

Renames atoms sequentially (C1, C2, O1, ...) for each HETATM residue.

Relies on an element column being present (see [pdb_element](#pdb_element)).

```bash
Usage:
    python pdb_uniqname.py <pdb file>

Example:
    python pdb_uniqname.py 1CTF.pdb
```


## pdb_delelem

Deletes all atoms matching the given element in the PDB file.

Elements are read from the element column.

```bash
Usage:
    python pdb_delelem.py -<option> <pdb file>

Example:
    python pdb_delelem.py -H 1CTF.pdb  # deletes all protons
    python pdb_delelem.py -N 1CTF.pdb  # deletes all nitrogens
    python pdb_delelem.py -H,N 1CTF.pdb  # deletes all protons and nitrogens
```


## pdb_fromcif

Rudimentarily converts a mmCIF file to the PDB format.

Will not convert if the file does not 'fit' in PDB format, e.g. too many chains, residues, or atoms.
Will convert only the coordinate section.

```bash
Usage:
    python pdb_fromcif.py <pdb file>

Example:
    python pdb_fromcif.py 1CTF.pdb
```


## pdb_reatom

Renumbers atom serials in the PDB file starting from a given value (default 1).

```bash
Usage:
    python pdb_reatom.py -<number> <pdb file>

Example:
    python pdb_reatom.py -10 1CTF.pdb  # renumbers from 10
    python pdb_reatom.py --1 1CTF.pdb  # renumbers from -1
```


## pdb_selchain

Extracts one or more chains from a PDB file.

```bash
Usage:
    python pdb_selchain.py -<chain id> <pdb file>

Example:
    python pdb_selchain.py -C 1CTF.pdb  # selects chain C
    python pdb_selchain.py -A,C 1CTF.pdb  # selects chains A and C
```


## pdb_sort

Sorts the ATOM/HETATM/ANISOU/CONECT records in a PDB file.

Atoms are always sorted by their serial number, meaning the original ordering of the atoms within each residue are not changed.
Alternate locations are sorted by default.

Residues are sorted according to their residue sequence number and then by their insertion code (if any).

Chains are sorted by their chain identifier.

Finally, the file is sorted by all keys, and the records are placed in the following order:
- ATOM/ANISOU, intercalated if the latter exist
- HETATM
- CONECT, sorted by the serial number of the central (first) atom

MASTER, TER, END statements are removed.
Headers (HEADER, REMARK, etc) are kept and placed first.
Does NOT support multi-model files.
Use pdb_splitmodel, then pdb_sort on each model, and then pdb_mkensemble.

```bash
Usage:
    python pdb_sort.py -<option> <pdb file>

Example:
    python pdb_sort.py 1CTF.pdb  # sorts by chain and residues
    python pdb_sort.py -C 1CTF.pdb  # sorts by chain (A, B, C ...) only
    python pdb_sort.py -R 1CTF.pdb  # sorts by residue number/icode only
```


## pdb_validate

Validates the PDB file ATOM/HETATM lines according to the format specifications.

Does not catch all the errors though... people are creative!

```bash
Usage:
    python pdb_validate.py <pdb file>

Example:
    python pdb_validate.py 1CTF.pdb
```


## pdb_delhetatm

Removes all HETATM records in the PDB file.

```bash
Usage:
    python pdb_delhetatm.py <pdb file>

Example:
    python pdb_delhetatm.py 1CTF.pdb
```


## pdb_gap

Finds gaps between consecutive protein residues in the PDB.

Detects gaps both by a distance criterion or discontinuous residue numbering.
Only applies to protein residues.

```bash
Usage:
    python pdb_gap.py <pdb file>

Example:
    python pdb_gap.py 1CTF.pdb
```


## pdb_reres

Renumbers the residues of the PDB file starting from a given number (default 1).

```bash
Usage:
    python pdb_reres.py -<number> <pdb file>

Example:
    python pdb_reres.py -10 1CTF.pdb  # renumbers from 10
    python pdb_reres.py --1 1CTF.pdb  # renumbers from -1
```


## pdb_selelem

Selects all atoms that match the given element(s) in the PDB file.

Elements are read from the element column.

```bash
Usage:
    python pdb_selelem.py -<option> <pdb file>

Example:
    python pdb_selelem.py -H 1CTF.pdb  # selects all protons
    python pdb_selelem.py -N 1CTF.pdb  # selects all nitrogens
    python pdb_selelem.py -H,N 1CTF.pdb  # selects all protons and nitrogens
```


## pdb_splitchain

Splits a PDB file into several, each containing one chain.

```bash
Usage:
    python pdb_splitchain.py <pdb file>

Example:
    python pdb_splitchain.py 1CTF.pdb
```


## pdb_wc

Summarizes the contents of a PDB file, like the wc command in UNIX.

By default, this tool produces a general summary, but you can use several
options to produce focused but more detailed summaries:
- [m] - no. of models.
- [c] - no. of chains (plus per-model if multi-model file).
- [r] - no. of residues (plus per-model if multi-model file).
- [a] - no. of atoms (plus per-model if multi-model file).
- [h] - no. of HETATM (plus per-model if multi-model file).
- [o] - presence of disordered atoms (altloc).
- [i] - presence of insertion codes.

```bash
Usage:
    python pdb_wc.py [-<option>] <pdb file>

Options:
    [m] - no. of models.
    [c] - no. of chains (plus per-model if multi-model file).
    [r] - no. of residues (plus per-model if multi-model file).
    [a] - no. of atoms (plus per-model if multi-model file).
    [h] - no. of HETATM (plus per-model if multi-model file).
    [o] - presence of disordered atoms (altloc).
    [i] - presence of insertion codes.

Example:
    python pdb_wc.py 1CTF.pdb
```

