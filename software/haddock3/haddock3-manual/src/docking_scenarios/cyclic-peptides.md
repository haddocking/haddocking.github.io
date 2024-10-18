## Peptide cyclisation

The generation of cyclic peptides usually involve the formation of a disulphide bridge between two cysteins or the formation of a peptide bond between the N-terminus and C-terminus residues.
This can be performed by haddock3 in a two step process, by first generating restraints between the two resiudes involved to induce a pre-cyclic conformation, and then re-generating the topology with an increased range of chemical bond detection (tuning `cyclicpept_dist`, `disulphide_dist` and turning on the `cyclicpept` parameters in `[topoaa]` module), therefore detecting and creating the covalent cyclic bond and refining again.

Protocol described in: [https://doi.org/10.1021/acs.jctc.2c00075](https://doi.org/10.1021/acs.jctc.2c00075)

Two examples are provided in [`examples/peptide-cyclisation/`](https://github.com/haddocking/haddock3/blob/main/examples/peptide-cyclisation/):
- 1SFI, a 14 residue cyclic peptide with both backbone and disulphide bridge cyclisation: [cyclise-peptide-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/peptide-cyclisation/cyclise-peptide-full.cfg)
- 3WNE, a 6 residue backbone cyclic peptide


The input peptide was generated using PyMOL, using beta and polyproline initial conformation (available in [`examples/peptide-cyclisation/data/1sfi_peptide-ensemble.pdb`](https://github.com/haddocking/haddock3/blob/main/examples/peptide-cyclisation/data/1sfi_peptide-ensemble.pdb)).

The first step is using the `[flexref]` module, setting the `unambig_fname` to [1sfi_unambig.tbl](https://github.com/haddocking/haddock3/blob/main/examples/peptide-cyclisation/data/1sfi_unambig.tbl) to drive both the backbone and disulphide bridge cyclisation, giving full flexibility to the peptide (with `fle_sta_1`, `fle_end_1`, `fle_seg_1` parameters), increasing the number steps by a factor 10 to allow for more flexible refinement (`mdsteps_rigid`, `mdsteps_cool1`, `mdsteps_cool2`, `mdsteps_cool3`), turning off the electrostatic `elecflag = false`. By setting `sampling_factor = 200`, we will generate 200 replicas with different initial seeds for each of the input conformations (in this case 2).
This is followed by an short molecular dynamics simulation in explicit solvent `[mdref]`, also giving full flexibility to the peptide (with `fle_sta_1`, `fle_end_1`, `fle_seg_1` parameters).

A RMSD clustering step is perfomed using `[rmsdmatrix]`, `[clustrmsd]` (with `criterion="maxclust"` and `n_clusters=50`) to generate a subset of 50 clusters, finalized by `[seletopclusts]` module setting `top_models=1`, to only extract one single model per clusters.

`[topoaa]` module is then used again to re-generate the topology. In this case the three **important** parameters (`cyclicpept_dist`, `disulphide_dist`, and `cyclicpept`) are set, allowing for the detection of the disulphide bridge and peptide bond at higher distance, therefore generating the proper cyclicised topology.

A second round of `[emref]`, `[flexref]` and `[mdref]` is then performed, allowing to reduce the length of the newly formed chemical bonds and optimise the cyclic peptide conformation.

The `[caprieval]` module is called at various stages during the workflow to assess the conformation of the peptide with respect to the known reference structure. Note that in this case, only the `global_rmsd` value is computed, as the structure is not a complex.
