## Protein Peptide docking

The protein-peptide docking example makes use of the knowledge of the binding site on the protein to guide the docking.
The active site residues are defined as active and the peptide as passive (the corresponding AIRs are defined in the `ambig.tbl` file in the `data` directory).
This example follows the protocol described in our protein-peptide docking article ([Trellet et. al. PLoS ONE 8, e58769 (2013)](https://dx.plos.org/10.1371/journal.pone.0058769)).
For the peptide, an ensemble of three conformations (alpha-helix, polyproline-II and extended) is provided as starting point for the docking.
Those were built using PyMol (instructions on how to do that can be found [here](https://www.bonvinlab.org/education/molmod_online/simulation/#preparing-the-system)).

Three different workflows are illustrated:

- 3000 rigidbody docking models, selection of top 400 and flexible refinement and energy minimisation of those ([docking-protein-peptide-full.cfg](https://github.com/haddocking/haddock3/tree/main/examples/docking-protein-peptide/docking-protein-peptide-full.cfg)
- 3000 rigidbody docking models, selection of top 400 and flexible refinement followed by a final refinement in explicit solvent (water) of those ([docking-protein-peptide-mdref-full.cfg](https://github.com/haddocking/haddock3/tree/main/examples/docking-protein-peptide/docking-protein-peptide-mdref-full.cfg)
- 3000 rigidbody docking models, FCC clustering and selection of max 20 models per cluster followed by flexible refinement and energy minimisation ([docking-protein-peptide-cltsel-full.cfg](https://github.com/haddocking/haddock3/tree/main/examples/docking-protein-peptide/docking-protein-peptide-cltsel-full.cfg)).

__Note__ how the peptide is defined as fully flexible for the refinement phase in `[flexref]` (`fle_sta_1`, `fle_end_1`, `fle_seg_1`) and dihedral angle restraints are automatically defined to maintain secondary structure elements (`ssdihed = "alphabeta"`)

The `[caprieval]` module is called at various stages during the workflow to assess the quality of the models with respect to the known reference structure.
