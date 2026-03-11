### Restraints validation

If you modify manually this generated restraint files or create your own, it is possible to quickly check if the format is valid using the following `haddock3-restraints` sub-command:

<a class="prompt prompt-cmd">
haddock3-restraints validate_tbl ambig-paratope-NMR-epitope.tbl \-\-silent
</a>

No output means that your TBL file is valid.

*__Note__* that this only validates the syntax of the restraint file, but does not check if the selections defined in the restraints are actually existing in your input PDB files.
