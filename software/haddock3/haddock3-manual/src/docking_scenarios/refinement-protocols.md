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

