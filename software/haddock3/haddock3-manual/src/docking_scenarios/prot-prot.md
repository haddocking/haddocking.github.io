## Protein-protein docking

### Two body docking

Here we provide various examples using the standard HADDOCK2.X workflows, now well established and banchmarked, using `[rigidbody]` docking (former *it0*), followed by flexible refinement in torsional angle space with the `[flexref]` module (former *it1*), with a final refinement step using molecular dynamics simulation in an explicit solvent shell (`[mdref]`, former *itw*) or an energy minimisation step (`[emref]`).
The final set of complexes is later clustered using Fraction of Common Contacts clustering (FCC) with the `[clustfcc]` module.

The protein-protein docking example makes use of the NMR chemical shift perturbation data providing information on the residues of binding site to guide the docking.
The NMR-identified residues are defined as active with their surface neighbors as passive (the corresponding AIRs are defined in the [e2a-hpr_air.tbl](../examples/docking-protein-protein/data/e2a-hpr_air.tbl) file in the `data` directory).
This system is the same as described in our [HADDOCK2.4 basic protein-protein docking tutorial](https://www.bonvinlab.org/education/HADDOCK24/HADDOCK24-protein-protein-basic/).
For the second molecule (HPR), an ensemble of 10 conformations (taken from the NMR solution structure of this protein) is used as starting point for the docking.
Refer to above tutorial for more details about the system and restraints.

Here are some examples:
- with molecular dynamics simulation in an explicit solvent shell -> [docking-protein-protein-mdref-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-protein/docking-protein-protein-mdref-full.cfg)
- with an energy minimisation step only: [docking-protein-protein-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-protein/docking-protein-protein-full.cfg)

Due to the flexibility allowed by haddock3, a clustering step can now be performed right after the rigidbody sampling, allowing to capture a higher structural diversity by not only relying on the HADDOCK scoring function to select the top ranked models.
Here is an example with an intermediate clustering step after the `[rigidbody]` docking: [docking-protein-protein-cltsel-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-protein/docking-protein-protein-cltsel-full.cfg).


### Symmetrical homotrimer docking 

The homotimer docking scenario, [available here](https://github.com/haddocking/haddock3/tree/main/examples/docking-protein-homotrimer), is first performing `[rigidbody]` docking, followed by `[flexref]` refinement and a final `[emref]` energy minimisation step of the complexe.
It also makes use of two types of symmetry restraints:
- [non-crystallographic symmetry restraints](../symmetry_restraints.md#non-crystallographic-symmetry): to make sure the three chains are having the same conformation.
- [C3 symmetry restraints](../symmetry_restraints.md#rotational-symmetry): to obtain solutions respecting the C3 symmetry.


### Multiple ambiguous files

In some case, restraints could be obtained from various sources; different experimental methods or multiple predictions.
In this case, knowing which AIR file will be leading to the correct complex can only be assessed once the docking is performed, and maybe some of them will lead to the same solutions.

It is possible to input multiple ambiguous restraints files in a single `.tgz` archive.
When providing the kind of input, each sampled docking solution will use an other AIR file contained in the archive.
A particular parameter should later be set in the downstream protocol, `previous_ambig = true`, enabling to use the AIR file used at the `[rigidbody]` stage and so on.

An example is [provided here](https://github.com/haddocking/haddock3/tree/main/examples/docking-multiple-ambig).

This example shows how to use HADDOCK3 when several restraint files are available.
It is built upon the results obtained running [arctic3d](https://github.com/haddocking/arctic3d) on two proteins forming the complex `2GAF`.
The presence of multiple interfaces in both structures allows to define several `.tbl` ambiguous restraint files to be used in the calculations.
At first, these files must be compressed in a `.tbl.tgz` archive.
During the workflow, the Haddock3 machinery unzips the archive and evenly assigns each `.tbl` file to a number of models to be generated.
Even if only one sixth of the restraint files contain reasonable information on the interface, Haddock3 is still able to retrieve good docking models in the best-scoring positions.

__Note__ how the information about restraint files is propagated during the workflow (`previous_ambig = true` for `flexref` and `emref` modules), so that each model is always refined with its corresponding `.tbl` file.

Importantly, in the [docking-multiple-tbls-clt-full.cfg](https://github.com/haddocking/haddock3/tree/main/examples/docking-multiple-ambig/docking-multiple-tbls-clt-full.cfg) example the clustering is performed right after the `rigidbody` module, so as to lump together solutions resulting from the application of different sets of restraints.

The `caprieval` module is called at various stages during the workflow to assess the quality of the models with respect to the known reference structure.
