## Protein glycan docking

A protein-glycan docking example making use of the knowledge of the binding site on the protein to guide the docking. The conformation of the glycan has been obtained from the [GLYCAM webserver](http://glycam.org/){:target="_blank"}, while the structure of the protein is taken from the PDB in its unbound form. In the proposed workflows, a clustering step is always performed after initial docking stage, so as to increase the diversity of the ensemble of models to be refined.

Three different workflows are illustrated:
- [docking-protein-glycan-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-glycan/docking-protein-glycan-full.cfg){:target="_blank"}: 1000 rigidbody docking models, RMSD clustering to select 50 clusters, flexible refinement of the top 5 models of each cluster, final RMSD clustering for cluster-based scoring. The RMSD clustering assumes a good knowledge of the interface, as the user has to define the residues involved in the binding site by means of the resdic_ parameter.
- [docking-protein-glycan-ilrmsd-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/examples/docking-protein-glycan/docking-protein-glycan-ilrmsd-full.cfg){:target="_blank"}: 1000 rigidbody docking models, interface-ligand-RMSD (`ilrmsd`) clustering to select 50 clusters, flexible refinement of the top 5 models of each cluster, final ilRMSD clustering for cluster-based scoring. The interface-ligand-RMSD clustering is a more general approach, as it does not require the user to define the residues involved in the binding site. The interface is automatically defined by the residues involved in the protein-glycan interaction in the input models.
- [docking-flexref-protein-glycan-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/examples/docking-protein-glycan/docking-flexref-protein-glycan-full.cfg){:target="_blank"}: 500 flexible docking runs + final RMSD clustering for cluster-based scoring. In this case, the rigidbody docking is skipped and the docking is performed at the flexible refinement level. In this case the flexible refinement has more steps than usual (`mdsteps_rigid = 5000`, `mdsteps_cool1 = 5000` and so on) and the glycan is defined as fully flexible (`fle_sta_1`, `fle_end_1`, `fle_seg_1`).

__Note__ the modified weight of the Van der Waals energy term for the scoring of the rigidbody docking models (`w_vdw = 1.0`), as in the [protein-ligand example](./prot-ligand.md).