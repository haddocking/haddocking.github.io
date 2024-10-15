## Small molecule docking

Small molecule docking can also be performed using haddock3.
It requires the use of custom topology and paramter files for the ligand, as it they are out of the scope of the OPLS force-field.
To generate them, please refere to the section: [How to generate topology and parameters for my ligand ?](../structure_requirements.md#How-to-generate-topology-and-parameters-for-my-ligand)

Two protocols have been proposed:
- [By homology docking using experimental template](#template-based-shape-docking)
- [By defining a binding site](#using-binding-site-definition)


### Template-based shape docking

The use of experimental structure as template for docking have been shown to provide helpful information to guide the conformation of the ligand towards both the binding site and an adequate conformation (see: [D3R Grand Challenge 4](https://doi.org/10.1007/s10822-019-00244-6), [@TOME 3.0](https://www.sciencedirect.com/science/article/pii/S0022283624003139) and [CAPRI16 (soon)]())

A protein-ligand docking example making use of the knowledge of a template ligand (a ligand similar to the ligand we want to dock and bind to the same receptor).
The template ligand information is used in the form of shape consisting of dummy beads and positioned within the binding site to which distance restraints are defined.
More details about the method and the performance of the protocol when benchmarked on a fully unbound dataset
can be seen in our freely available [paper on JCIM](https://pubs.acs.org/doi/full/10.1021/acs.jcim.1c00796).

As explained in our [shape small molecule HADDOCK2.4 tutorial](https://www.bonvinlab.org/education/HADDOCK24/shape-small-molecule/), during the docking and refinement the protein and the shape are kept in their original positions (see the `mol_fix_origin_X` parameters in the config file) and ambiguous distance restraints between the ligand and the shape beads are defined (the corresponding AIRs are defined in the `shape-restraints-from-shape-1.tbl` file in the `data` directory).
This is effectively a three body docking.
For the ligand an ensemble of 10 different conformations is provided as starting point for the docking (`ligand-ensemble.pdb` in the `data` directory).
Please refer to our [shape small molecule tutorial](https://www.bonvinlab.org/education/HADDOCK24/shape-small-molecule/) for information on how to generate such an ensemble.

The [docking-protein-ligand-shape-full.cfg](https://github.com/haddocking/haddock3/tree/main/examples/docking-protein-ligand-shape/docking-protein-ligand-shape-full.cfg) workflow consists of the generation of 1000 rigidbody docking models with the protein and shape kept in their origin position, selection of top200 and flexible refinement of those.

__Note__ the modified weight of the van der Waals energy term for the scoring of the rigidbody docking models (`w_vdw = 1.0`).
To allow the ligand to penetrate better into the binding site the intermolecular energy components are scaled down during the rigidbody docking phase (`inter_rigid = 0.001`).
As for the protein-ligand example, parameter and topology files must be provided for the ligand (`ligand_param_fname = "data/ligand.param"` and `ligand_top_fname = "data/ligand.top"`).
Those were obtained with a local version of PRODRG ([Schüttelkopf and van Aalten Acta Crystallogr. D 60, 1355−1363 (2004)](http://scripts.iucr.org/cgi-bin/paper?S0907444904011679)).

The `[caprieval]` module is called at various stages during the workflow to assess the quality of the models with respect to the known reference structure.


### Using binding site definition

A protein-ligand docking example making use of the knowledge of the binding site on the protein to guide the docking.

As explained in our [protein-ligand HADDOCK2.4 tutorial](https://www.bonvinlab.org/education/HADDOCK24/HADDOCK24-binding-sites/), in the rigidbody docking phase all residues of the binding site are defined as active to draw the ligand into it (the corresponding AIRs are defined in the [ambig-active-rigidbody.tbl](https://github.com/haddocking/haddock3/tree/main/examples/docking-protein-ligand/data/ambig-active-rigidbody.tbl) file in the `data` directory).
For the flexible refinement only the ligand is defined as active and the binding site as passive to allow the ligand to explore the binding site (the corresponding AIRs are defined in the [ambig-passive.tbl](https://github.com/haddocking/haddock3/tree/main/examples/docking-protein-ligand/data/ambig-passive.tbl) file in the `data` directory).

The [docking-protein-ligand-full.cfg](https://github.com/haddocking/haddock3/tree/main/examples/docking-protein-ligand/docking-protein-ligand-full.cfg) workflow consists of the generation of 1000 rigidbody docking models, selection of top200 and flexible refinement of those.

__Note__ the modified weight of the Van der Waals energy term for the scoring of the `[rigidbody]` docking models (`w_vdw = 1.0`) and the skipping of the high temperature first two stages of the simulated annealing protocol during the `[flexref]` refinement (`mdsteps_rigid = 0` and `mdsteps_cool1 = 0`).
Parameter and topology files must be provided for the ligand (`ligand_param_fname = "data/ligand.param"` and `ligand_top_fname = "data/ligand.top"`).
Those were obtained with a local version of PRODRG ([Schüttelkopf and van Aalten Acta Crystallogr. D 60, 1355−1363 (2004)](http://scripts.iucr.org/cgi-bin/paper?S0907444904011679)).

The `[caprieval]` module is called at various stages during the workflow to assess the quality of the models with respect to the known reference structure.

