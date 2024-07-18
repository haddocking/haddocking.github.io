---
layout: page
title: ""
excerpt: ""
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, manual, usage]
image:
  feature: pages/banner_software.jpg
---

* table of contents
{:toc}

<hr>


# Command line interfaces

Haddock3 is a software that can read configuration files and compute data.
While there will be [a web application](), haddock3 do not have interface, and you must use it from the command line.
While this may have some negative impact for some unexperienced user, it is also very powerful as it allows custom scripts to launch haddock, and therefore integrate it in your own pipelines.


To use the command line interface, you must open a terminal:
* [iTerm / Terminal]: for Mac users, defaults terminals are available and fully functional.
* [WindowsPowerShell]: The windows solution to open a terminal.
* [VSCode](): an integrated developping environnment (IDE) that allows you to run command lines in the terminal.


Haddock3 comes with several Command Line Interfaces (CLIs), that are described and listed below.


## haddock3

The main command line, `haddock3` is used to launch a Haddock3 workflow from a [configuration file](/software/haddock3/manual/config_file).
It takes a positional argument, the path to the configuration file.

```bash
haddock3 workflow.cfg
```

Also two optional arguments can be used:

- `--restart <module_id>`: allows to restart the workflow restarting for the module id. Note that previously generated folders from the selected step onward will be deleted.
- `--extend-run <run_directory>`: allows to start the new workflow from the last step of a previously computed run.



## haddock3-cfg

An other very interesting CLI is `haddock3-cfg`.
This CLI allows you to list the parameter names, their description and default values for each available modules.
Used without any option, the command `haddock3-cfg` will return all [Global parameters](/software/haddock3/manual/global_parameters).

To access the list of parameters for a given module, you should use the optinal argument `-m <module_name>`.
As an example, to list available parameters for the module `seletopclusts`, you should run the following command:

```bash
haddock3-cfg -m seletopclusts
```

Please note that all the parameters for each module are also available from the [online documentation](https://www.bonvinlab.org/haddock3/modules/index.html).


## haddock3-restraints

The CLI `haddock3-restraints` is made to generate restraints used either a ambiguous restraints or unambiguous ones.
The `haddock3-restraints` CLI is composed of several sub-commands, each one dedicated to some specific actions, such as:

- Searching for solvent accessible residues
- Gathering neighbors of a selection
- Maintaining the conformation of a single chain with potential gap
- Generating ambiguous restraints from active and passive resiudes
- Generating plans and corresponding restraints

As this CLI is more specialized, we have made a [special chapter in this manual](/software/haddock3/manual/restraints_cli) to explain all the functionalities.


## haddock3-score

The `haddock3-score` is a CLI made for scoring a single complex.
The topologies are created and a small energy minimization is performed on the complex before the evalutation of the haddock score components.
It is dedicated to the scoring of it and only returns the computed haddock score and its components.
It is a short cut to a full configuration file that would contain the `topoaa` and `emscoring` modules.

To use it, provide the path to the complex to be scored:

```bash
haddock3-score path/to/complex.pdb
```

This CLI can take optional parameters using the `-p` flag, where the user can provide the set of parameter and values to tune the weights of the Haddock scoring function.
Be aware that only parameters available for the `emscoring` module are accepted.

To tune the haddock3 scoring function weights, there are basically only 5 parameters to be tuned.

- **w_vdw**: to tune the weight of the Van der Walls term
- **w_elec**: to tune the weight of the Electrostatic term
- **w_desolv**: to tune the weight of the Desolvation term
- **w_air**: to tune the weight of the Ambiguous Restraints term
- **w_bsa**: to tune the weight of the Burried Surface Area term

Note that, if a parameter is not tuned, the defaults scoring function weights are used.


As an example, this command would tune the Van der Walls term during the evaluation of the complex:

```bash
haddock3-score path/to/complex.pdb -p w_vdw 0.5
```

Note how the parameter name and its new value are separated by a space.

To modify multiple parameters, just add the new parameter separate by a space:

```bash
haddock3-score path/to/complex.pdb -p w_vdw 0.5 w_bsa 0.2
```

## haddock3-analyse

## haddock3-traceback

## haddock3-re

## haddock3-copy

The `haddock3-copy` CLI allows one to copy the content of a run to an other run directory.

It takes three arguments:
- **`-r run_directory`** is the directory of a previously computed haddock3 run.
- **`-o new_run_directory`** is the new directory where to make to copy of the old run.
- **`-m module_id_X module_id_Y`** is the list of modules you wish to copy (separated by spaces).

As an example, considering your previous run directory is named `run1` and contains the following modules:
```
run1/
  0_topoaa/
  1_rigidbody/
  2_caprieval/
  3_seletop/
  4_flexref/
  (etc...)
```

You may want to use `4_flexref` step folder as a starting point for a new run names `run2`.
To do so, run the following command:

```bash
haddock3-copy -r run1 -m 0 4 -o run2
```

**Notes**:
- the flag `-m` allows to define which modules must be copied, and modules `0` (for `0_topoaa`) and `4`  (for `4_flexref`) are space separated.
- in this case, we also copy the content of `0_topoaa`, this is because topologies are stored in this module directory, and we must have access to them if we are using an other module requiering CNS topology to run.

**WARNING**:
To copy the content of a run and modify the paths, we are using the `sed` command, searching to replace the previous run directory name (`run1`) to the new one (`run2`) in all the generated files to make sure that paths will be functional in the new run directory.
In some cases, this can lead to some artefacts, such as the modification of attribute names if your run directory contain a name that is used by haddock3.

Here is a list of run directory names **NOT** to use:
- topology
- score
- emref
- etc...

The best solution is to always use a unique name that describe the content of the run.


## haddock3-clean

## haddock3-unpack

## haddock3-mpitask

## haddock3-dmn

## haddock3-pp

## haddock3-bm
