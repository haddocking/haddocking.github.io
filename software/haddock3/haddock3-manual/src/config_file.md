# Workflow configuration file

Haddock3 uses a configuration file to define the workflow to be performed.
A workflow is defined in simple configuration text files, similar to the [TOML](https://toml.io/en/) format but with extra features.

It basically contains two main parts:
* [Global parameters](./global_parameters.md): General parameters to be applied to the workflow, including input molecules and location where to run the docking protocol.
* [List of modules](./modules_parameters.md): Sequence of [module names], defining the sequential order in which each module must be performed. Each module has several parameters, that can be defined to fine-tune them, or left untouched therefore using default parameters.

Examples of workflow configuration files are [available here !](https://github.com/haddocking/haddock3/tree/main/examples)


## Schematic representation of a haddock3 workflow configuration file

Let's consider the definition of a Haddock3 configuration file named `schematic_workflow.cfg`:

```toml
###############################################
# First, we will define the GLOBAL PARAMETERS #
###############################################
### MANDATORY PARAMETERS
# The run directory
run_dir = "super_example"
# The input molecules
molecules = ["antibody.pdb", "antigen.pdb"]
### EXECUTION PARAMETERS
# Running in 'local' mode (also default)
mode = "local"
# Setting the number of cores to 10
ncores = 10
### POST PROCESSING AND CLEANING PARAMETERS
postprocess = true  # will run `haddock3-analyse` and generate graphs
clean = true  # Will compress output pdb files

#############################################################
# Now, we define the list of [modules] and their parameters #
#############################################################
# Using moduleX as first module in the workflow
[moduleX]
param1 = "super_string"
param2 = 2
param3 = [2, 3, 4]

# Using moduleY as second module in the workflow
[moduleY]
param1 = 5.5
param2 = "fine_tune"

# Re-using moduleX as last module in the workflow with different parameters
[moduleX]
param1 = "other_string"
param4 = 3.33
```
**_note_** that this configuration file is only schematic and not functional as modules `[moduleX]` and `[moduleY]` do not exist in haddock3.


This configuration file can then be executed by running:

```bash
haddock3 schematic_workflow.cfg
```

[Click here](./clis.md#haddock3) for more details about the `haddock3` command line interface.
