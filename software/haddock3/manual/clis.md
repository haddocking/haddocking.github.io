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


Haddock3 comes with several command line interfaces (CLIs), that are described and listed below.

## haddock3

The main command line, `haddock3` is used to launch a workflow from a [configuration file](/software/haddock3/manual/config_file).
It takes a positional argument, the path to the configuration file.

`haddock3 workflow.cfg`

Also two optional arguments can be used:

- `--restart <module_id>`: allows to restart the workflow restarting for the module id. Note that Previous folders from the selected step onward will be deleted.
- `--extend-run <run_directory>`: allows to start the new workflow from the last step of a previously computed run.



## haddock3-cfg

An other very interesting CLI is `haddock3-cfg`.
This CLI allows you to list the parameter names, their description and default values for each available modules.
Used without any option, the command `haddock3-cfg` will return all [Global parameters](/software/haddock3/manual/global_parameters).

To access the list of parameters for a given module, you should use the optinal argument `-m <module_name>`.
As an example, to list available parameters for the module `seletopclusts`, you should run the following command:

`haddock3-cfg -m seletopclusts`

Please note that all the parameters for each module is also available from [the documentation](https://www.bonvinlab.org/haddock3/modules/index.html).


## haddock3-restraints

The CLI `haddock3-restraints` is made to generate restraints used either a ambiguous restraints or unambiguous ones.
The `haddock3-restraints` CLI is composed of several sub-commands, each one dedicated to some specific actions.
As this CLI is more specialized, we have made a [special chapter in this manual](/software/haddock3/manual/restraints_cli) to explain all the functionalities.


## haddock3-score

The `haddock3-score` is a CLI made for scoring a single complex (from **two** upto **twenty** chains).
It is dedicated to the scoring of it and only returns the computed haddock score and its components.
To use it, ...
It is a short cut to a full configuration file that would contain the `topoaa` and `emscoring` modules.


## haddock3-analyse

## haddock3-traceback

## haddock3-re

## haddock3-copy

## haddock3-clean

## haddock3-unpack

## haddock3-mpitask

## haddock3-dmn

## haddock3-pp

## haddock3-bm
