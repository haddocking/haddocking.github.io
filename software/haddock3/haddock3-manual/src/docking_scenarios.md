# Examples of docking scenario

As creating a new workflow can be complex at the beginning, we are providing a set of pre-defined haddock3 scenarios.
These examples are encompassing a wide range of applications, such as:

- [Protein-protein docking](#protein-protein-docking)
- [Protein-peptide docking](#protein-peptide-docking)
- [Protein-DNA docking](#protein-dna-docking)
- [Antibody-antigen docking](#antibody-antigen-docking)
- [Protein-glycan docking](#protein-glycan-docking)
- [Small-molecule docking](#small-molecule-docking)
- [Complexes refinement protocols](#refinement-protocols)
- [Building cyclic peptide](#cyclic-peptide)
- [Scoring workflow](#scoring-workflow)
- [Analysis pipelines](#analysis-scenario)


Alternatively, up-to-date examples can also be found:
- in your local installation of haddock3: `haddock3/examples/`.
- online, on our [GitHub repository `haddock3/examples/`](https://github.com/haddocking/haddock3/tree/main/examples).


Please note the extension scheme we are using in the provided configuration file examples:
- __*-full.cfg__: we are using the `*-full.cfg` suffix on protocols that have proper sampling, and therefore could be used in production. These are nice baseline workflow with appropriate parameters, but will obviously require more time to terminate the run. Examples making use of MPI are also provided in some cases, together with an associated job file that should be submitted to the slurm batch system (__*-full-mpi.cfg__ and __*-full-mpi.job__). Make sure to adapt the full config files to your own system.
- __*-test.cfg__: we are using the `*-test.cfg` suffix on protocols that have low sampling, allowing for fast test of the functionalities present in the workflow. Of note, on a daily basis, we are running most of the `*-test.cfg` configuration files to make sure the `main` branch of haddock3 is functional.


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
- [non-crystallographic symmetry restraints](/software/haddock3/manual/symmetry_restraints.md#non-crystallographic-symmetry): to make sure the three chains are having the same conformation.
- [C3 symmetry restraints](/software/haddock3/manual/symmetry_restraints.md#rotational-symmetry): to obtain solutions respecting the C3 symmetry.


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

## Protein DNA docking

Haddock3 can also deal with nucleic acids, such as DNA and RNA molecules.
In such senario, various important parameters must be set, allowing to:
- keep the dielectric constant constant: `dielec = "cdie"`
- set the dielectric constant to an higher value: `epsilon = 78`
- remove the desolvation term from the scroing function, otherwise having a too strong influence due to the phosphate groups: `w_desolv = 0`.
- automatically generate restraints allowing to keep the double stranded DNA 3' and 5' ends together: `dnarest_on = true`.


Here are some examples:
- using a final energy minimisation step: [docking-protein-DNA-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-DNA/docking-protein-DNA-full.cfg)
- refining the interface using MD in a solvent shell: [docking-protein-DNA-mdref-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-DNA/docking-protein-DNA-mdref-full.cfg)
- with an intermediate clustering step after rigidbody docking: [docking-protein-DNA-cltsel-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-DNA/docking-protein-DNA-cltsel-full.cfg)
- using center of mass restraints instead of ambiguous restraints extracted from the literature: [docking-protein-DNA-cmrest-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-DNA/docking-protein-DNA-cmrest-test.cfg)


## Antibody-antigen docking

Multiple antibody - antigen docking configuration files are [available here](https://github.com/haddocking/haddock3/tree/main/examples/docking-antibody-antigen).
They encompass various aspects of docking, mainly related to the information available to guide the docking:

- [No information about the paratop](#no-information-about-the-paratop): No information is known about the paratop, therefore tagetting the entire surface accessible resiude of the antigen.
- [Experimental knowledge of the paratop resiudes](#nmr-informed-paratop): NMR data was aquired and allowed to obtain information about residues involded in the binding on the antigen side.


### No information about the paratop

When no information is known about the paratop on the antigen side, our only solution is to rely on the CDR loops of the antibody, as we know that a least a subset of the resiudes on those loops will be part of the interaction.
Two appoaches can then be used:
- One where a distance restraints file is generated, where CDR loops resiudes are targetting all surface residues on the antigen side.
- The other one defining random distance restraints between the CDR loops and random patches on the antigen side.

#### Using surface accessible resiudes

Generating restraints guiding the antibody CDR loops towards surface resiudes on the antigen side is a solution that will sample the entire surface of the antigen. For this, two major information must be extracted:

- The residue indices of the antibody CDR loops: can be predicted using bioinformatics tools such as [proABC2](https://wenmr.science.uu.nl/proabc2).
- The surface residue indices of the antigen: can be predicted computed using `haddock3-restraints calc_accessibility antigen.pdb`.

Defining the CDR loops as `active` residues and all surface residues on the antigen as `passive`, we can create an ambiguous restraints file `ambig.tbl`, that will guide the docking sampling the entire surface of the antigen while making sure the CDR loops are interacting. For more details on how to generate restraints, please refere to the [`haddock3-restraints` documention](/software/haddock3/manual/restraints_cli.md).

For such kind of naive approach, increasing the sampling at the `[rigidbody]` level is important.

Various examples are available:

- standard HADDOCK workflow: [docking-antibody-antigen-CDR-accessible-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-full.cfg)
- with intermediate clustering steps: [docking-antibody-antigen-CDR-accessible-clt-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-clt-full.cfg)
- using MPI to spread the workload:
  - [docking-antibody-antigen-CDR-accessible-full-mpi.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-full-mpi.cfg)
  - [docking-antibody-antigen-CDR-accessible-full-mpi.job](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-full-mpi.job)



#### Using random distance restraints

An other alternative for pseudo-naive antibody-antigen docking is to define random restraints.
In this case, we will define segments on the antibody CDR loops to limit the search on the antibody side, and do not provide any definition on the antigen side.
By doing so, random residues on the CDR loops will be restraints to random patches on the antigen surface accessible residues.
This is performed in the `[rigidbody]` module by:
- turning on the `randair` parameter
- defining 6 segments to define what are the CDR loops residues
- increasing the sampling

```toml
# Turning on the randair parameter
randair = true
# About to define 6 random segments for the antigen
nrair_1 = 6
# Start and end of first CDR loop
rair_sta_1_1 = 26
rair_end_1_1 = 32
# Start and end of second CDR loop
rair_sta_1_2 = 55
rair_end_1_2 = 57
# Start and end of third CDR loop
rair_sta_1_3 = 101
rair_end_1_3 = 108
# Start and end of fourth CDR loop
rair_sta_1_4 = 146
rair_end_1_4 = 152
# Start and end of fifth CDR loop
rair_sta_1_5 = 170
rair_end_1_5 = 172
# Start and end of sixth CDR loop
rair_sta_1_6 = 212
rair_end_1_6 = 215

# Increasing the sampling
sampling = 10000

###
# ....
# Insert other modules here if you want
# ....
###

[flexref]
contactairs = true
```

In this case, no AIR restraints files can be accepted (nor `unambig` and `hbond` ones).

Note that after random air definition, we will use `contactairs = true` in later stage modules such as `[flexref]` and `[emref]`, generating restraints based on resiudes already in contact, ensuring the complex will not detach.


Here are some examples:
- standard HADDOCK workflow: [docking-antibody-antigen-ranairCDR-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-full.cfg)
- with intermediate clustering steps: [docking-antibody-antigen-ranairCDR-clt-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-clt-full.cfg)
- using MPI to spread the workload:
  - [docking-antibody-antigen-ranairCDR-full-mpi.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-full-mpi.cfg)
  - [docking-antibody-antigen-ranairCDR-full-mpi.job](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-full-mpi.job)


### NMR informed paratop

An ideal case would be to have information about the antigen paratop.
Coming from experimental methods or bioinformatic predictions, this information is extremly valuable as it will focus the  search by sampling comformations near key residues involed in the interaction.
By generating a dedicated ambiguous restraint file (`ambig-CDR-NMR-CSP.tbl`), only antigen CDR residues and few residues on the antigen side will be interacting.

Here is an  example: [docking-antibody-antigen-CDR-NMR-CSP-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-NMR-CSP-full.cfg)


## Protein glycan docking

A protein-glycan docking example making use of the knowledge of the binding site on the protein to guide the docking. The conformation of the glycan has been obtained from the [GLYCAM webserver](http://glycam.org/), while the structure of the protein is taken from the PDB in its unbound form. In the proposed workflows, a clustering step is always performed after initial docking stage, so as to increase the diversity of the ensemble of models to be refined.

Three different workflows are illustrated:
- [docking-protein-glycan-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-glycan/docking-protein-glycan-full.cfg): 1000 rigidbody docking models, RMSD clustering to select 50 clusters, flexible refinement of the top 5 models of each cluster, final RMSD clustering for cluster-based scoring. The RMSD clustering assumes a good knowledge of the interface, as the user has to define the residues involved in the binding site by means of the resdic_ parameter.
- [docking-protein-glycan-ilrmsd-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/examples/docking-protein-glycan/docking-protein-glycan-ilrmsd-full.cfg): 1000 rigidbody docking models, interface-ligand-RMSD (`ilrmsd`) clustering to select 50 clusters, flexible refinement of the top 5 models of each cluster, final ilRMSD clustering for cluster-based scoring. The interface-ligand-RMSD clustering is a more general approach, as it does not require the user to define the residues involved in the binding site. The interface is automatically defined by the residues involved in the protein-glycan interaction in the input models.
- [docking-flexref-protein-glycan-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/examples/docking-protein-glycan/docking-flexref-protein-glycan-full.cfg): 500 flexible docking runs + final RMSD clustering for cluster-based scoring. In this case, the rigidbody docking is skipped and the docking is performed at the flexible refinement level. In this case the flexible refinement has more steps than usual (`mdsteps_rigid = 5000`, `mdsteps_cool1 = 5000` and so on) and the glycan is defined as fully flexible (`fle_sta_1`, `fle_end_1`, `fle_seg_1`).

__Note__ the modified weight of the Van der Waals energy term for the scoring of the rigidbody docking models (`w_vdw = 1.0`), as in the [protein-ligand example](#small-molecule-docking).


## Small molecule docking

Small molecule docking can also be performed using haddock3.
It requires the use of custom topology and paramter files for the ligand, as it they are out of the scope of the OPLS force-field.
To generate them, please refere to the section: [How to generate topology and parameters for my ligand ?](/software/haddock3/manual/structure_requirements.md#How-to-generate-topology-and-parameters-for-my-ligand)

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


## Refinement protocols

All refinements examples can be found [here](https://github.com/haddocking/haddock3/tree/main/examples/refine-complex).

### Short molecular dynamics symulation in explicit solvent

This example illustrates the refinement of a complex.
In this case (workflow `refine-complex-test.cfg`) the molecules are kept in their original positions and the complex is subjected to a short flexible refinement in explicit solvent with the `[mdref]` module.
The same complex as for the `docking-protein-protein` example is used.
The molecules are defined separately in the config file (and could consist each of an ensemble, provided the two ensembles have exactly the same number of models).

In this example all parameters are left to their default settings, except for manually defining the histidines' protonation states and setting the `sampling_factor` to 10, which means that from each starting complex 10 models will be generated with different random seeds for initiating the molecular dynamics phase.

The `caprieval` module is called at the end to assess the quality of the models with respect to the known reference structure.

Here is an example:
```toml
run_dir = "mdref_complex_5replicas"
molecules = "model.pdb"

[topoaa]
autohis = false
[topoaa.mol1]
nhisd = 0
nhise = 1
hise_1 = 75
[topoaa.mol2]
nhisd = 1
hisd_1 = 76
nhise = 1
hise_1 = 15

[mdref]
# Setting sampling factor to 10 will generate 
# 10 replicas with different initial seeds to set the velocities
sampling_factor = 10
```

[Here is a full example](https://github.com/haddocking/haddock3/blob/main/examples/refine-complex/refine-complex-test.cfg) with provided input file and also using an experimental reference to track the evolution of the refinement.


### OpenMM MD simulation

The OpenMM molecular dynamics engine has its own module in haddock3, where users can setup short molecular dynamics similation using openMM.
It can be used as a refinement module, in implicit or explicit solvent.
Note that the use of the `[openmm]` module is a thirdparty module that requires its own installation procedure that is not part of the standard haddock3 suite.


#### As quality assessment of a docking pose

Using the `[openmm]` module allows to run unbiased molecular dynamics simulations in explicit solvent.
Previous work of [Z. Jandova, *et al.*, _J. Chem. Theo. and Comp._ 2021](https://doi.org/10.1021/acs.jctc.1c00336), showed that near-native complexes have less deviation from their input structure after 10 ns of simulation.
Setting up such kind of experiment with haddock3 is extremely easy, as it simply requires to use the `[openmm]` module with an input complex model, followed by the `[caprieval]` using the same input complex as reference structure.
This will allow to track how far from the original pose the final frame reached.

Here is an example configuration file:
```toml
# General parameters
run_dir = "md_to_the_rescue"
molecules = "model_1.pdb"

[topoaa]
[openmm]
# Define the timesteps
timestep_ps = 0.002  # default parameter
# Increase the simulation timesteps (500000 * 0.002 = 10 ns)
simulation_timesteps = 5000000
# Save 100 intermediate frames
save_intermediate = 100
# Define force-field
forcefield = 'amber14-all.xml'  # default parameter
# Use TIP3P explicit water model
explicit_solvent_model = 'amber14/tip3p.xml'  # default parameter
# Keep HBonds rigid
constraints = 'HBonds'  # default parameter
# Generate a final ensemble composed of all the frames
generate_ensemble = true  # default parameter

[topoaa]
# Compare the generated ensemble with the initial model
[caprieval]
reference_fname = "model_1.pdb"
sort_by = "dockq"
```

This protocol has been used during CAPRI round 55 for target 231, to validate the docking poses of the FLAG-peptide on the antibody (see: [CAPRI rounds 47-55 paper](https://www.biorxiv.org/content/10.1101/2024.09.16.613212v2)).


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

## Scoring workflow

## Defining a haddock3 configuration file

This example illustrates the use of Haddock3 for scoring purposes.
In contrast to HADDOCK2.X, Haddock3 can score a heterogenous set of complexes within one run/workflow.
In this example, four different types of complexes are scored within the same workflow:

- an ensemble of 5 models taken from CAPRI Target161
- a protein-DNA complex (model taken from our protein-DNA docking example)
- two models of a protein-protein complex (taken from our protein-protein docking example)
- a homotrimer model (taken from our protein-homotrimer docking examples)

Three scoring workflows are illustrated:

- [emscoring-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/scoring/emscoring-test.cfg): Only a short energy minimisation is performed on each model using `[emref]` module.
- [mdscoring-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/scoring/mdscoring-test.cfg): A short molecular dynamics simulation in explicit solvent (water) is performed on each model using `[mdref]` module. In that case contact AIRs (`contactairs = true`), dihedral angle restraints on secondary structure element (`ssdihed = alphabeta`) and DNA restraints (`dnarest_on = true`) are automatically defined.
- [capri-scoring-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/scoring/capri-scoring-test.cfg): An example scoring pipeline using in the CAPRI55 competition, where energy minimisation ()`[emref]`) is followed by FCC clustering (`[clustfcc]`) and selection of the top 2 models per cluster (`[seletopclusts]` with `top_models = 2`). Then a short molecular dynamics simulation in explicit solvent (water) is performed on each model using `[mdref]` module and the models are clustered again.

The model listings with their associated HADDOCK scores can be found in a `.tsv` file in the stage `01_xxx` directory of the respective runs.


### Using scoring command line


Haddock3 also contain a simple command line interface that allows you to score a single pdb file.
To do so, just run:
```bash
haddock3-score complex.pdb
```

This command is a short-cut to the following parameter file, and therefore can be really handy, as it simplify a lot the procedure, but is limitted to the scoring of a single model.
```toml
run_dir = "tmp_score"
molecules = "complex.pdb"
[topoaa]
[emscoring]
```

For more details on the `haddock3-score` CLI, please refere to [this section](/software/haddock3/module/clis.md#haddock3-score).


## Analysis scenario

The addition and inclusion of analysis modules in haddock3 is one of its major new strength, as it allows to perform various kind of analysis directly during the workflow.
For the complete list of analysis modules and their capabilities, please refere to the [Analysis Modules section](software/haddock3/manual/modules/analysis.md).


### Comparison to a reference structure

The `[caprieval]` module is dedicated to the computation of the CAPRI metrics (rmsd, interface-rmsd, ligand-rmsd, interface-ligand rmsd and dockq) on a set of input models. A reference structure can be provided using the `reference_fname` parameter. If this parameter is not defined, the best scoring model will be used as reference.

An example is provided here: [topoaa-caprieval-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/analysis/topoaa-caprieval-test.cfg).


### Hot spot detection

The analysis of hot-spots and key residues involved in the interaction between two chain can be of valuable information for mutagenesis or design purposes.
The `[alascan]` module is designed to perform point mutation of residues at the interface of a complex, and evaluate the difference in HADDOCK score with respect to the original input complex. It also splits the scoring function in its various components and generate an interactive graph allowing for a visual representation of the scanned resiudes contributions.

An example is provided here: [alascan-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/analysis/alascan-test.cfg).


### Generation of contact maps

While HADDOCK is producing 3D atomistic models, having the opportunity to have a 2D representation of the complexes can allow to understand at the sequence level the contacts involved in the compelex.
The `[contactmap]` module is specially designed to produce interactive plots describing the contacts observed in the structures.
It will produce two types of figures:
- a pair-wise distance matrix between all residues
- a chord chart recapitulating the residue-residue contacts observed

An example is provided here: [contmap-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/analysis/contmap-test.cfg)


### Fine tuning clustering parameters

Finding the appropriate threshold for the clustering parameters can be quite tricky, and often requires a first trial, followed by manual inspection to understand the content of the dataset.
We are providing examples (for `clustrmsd` and `clustfcc`) fine tuning of the parameters with visualisation of the matrices, to help you understand how to investigate the results you obtained after clustering.

Here are the two important step to analyse the structural diversity of you set of complexes in a clustering module:
- turn on the `plot_matrix` parameter to obtain a visual representation of the distance matrix.
- set the `min_population` to 1, so even singloton complexes will be forwarded to the next module and displayed on the plot.

Here are some examples:
- [fine tuning of the `clustrmsd` parameters](https://github.com/haddocking/haddock3/blob/main/examples/analysis/plot-finetune-ilrmsdmatrix-clustrmsd.cfg).
- [fine tuning of the `clustfcc` parameters](https://github.com/haddocking/haddock3/blob/main/examples/analysis/plot-finetune-clustfcc.cfg).


Note that fine tuning of clustering parameters can also be performed with the `haddock3-re` command, as both `[clustfcc]` and `[clustrmsd]` modules are subcommands of the `haddock3-re` CLI.


# Web-application pre-defined scenario


*comming soon...*
