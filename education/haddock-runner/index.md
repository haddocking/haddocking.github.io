---
layout: page
title: "Running HADDOCK with haddock-runner"
excerpt: ""
tags: [HADDOCK, benchmark, docking]
image:
  feature: pages/banner_education-thin.jpg
---

***

This tutorial consists of the following sections:

* table of contents
{:toc}

***

## Introduction

### What is `haddock-runner`?

The `haddock-runner` are an effort to reduce code duplication and to streamline the execution of HADDOCK benchmark. It is a standalone program written in [`go`](https://en.wikipedia.org/wiki/Go_(programming_language)){:target="_blank"}that can be used to run HADDOCK on a set of benchmark targets. It is designed to be used with both the production-ready [HADDOCK2.4](/software/haddock2.4){:target="_blank"}, the pre-release _HADDOCK2.5_ and the experimental (unpublished) [HADDOCK3](/software/haddock3) versions.

When running a benchmark, users/developers may be interested in the following (in no specific order):

* The quality of the docking results when using different parameters
* Comparing the results of different versions
* The time it takes to run HADDOCK on a set of targets

However the `haddock-runner` can be used to run HADDOCK on a large set of targets such as for virtual screening.

### How does `haddock-runner` work?

The execution of a HADDOCK benchmark consists of a few steps:

1. Setup the benchmark
  * Copy the target structures to the location where the HADDOCK run will be executed
2. Setup the HADDOCK run
  * For HADDOCK2.4, writing the `run.param` file and executing the `haddock2.4` program once to setup the folder structure
  * For HADDOCK3, writing the `run.toml`
3. Distribute several HADDOCK runs in a HPC-friendly manner

`haddock-runner` aim to automate all these steps, additionally giving the user the possibility of setting up various *scenarios*. A scenario is a set of parameters that will be used to run HADDOCK. For example, a user may want to run HADDOCK against a set of targets with different sampling values, different restraints, different parameters, etc.


### Who is `haddock-runner` for?

The tool is designed for users/students/developers that are familiar with HADDOCK, command-line scripting and with access to a HPC infrastructure. If this is the first time you are using HADDOCK, please familiarize first yourself with the software by running the basic [HADDOCK2.4](/education/HADDOCK24/index.md){:target="_blank"} or [HADDOCK3 tutorials](/education/HADDOCK3/index.md){:target="_blank"}. `haddock-runner` is not meant to be used by end-users who want to run a single target, or a small set of targets; for that purpose we recommend instead using the [HADDOCK2.4 web server](https://wenmr.science.uu.nl/haddock2.4/){:target="_blank"}.

***

## Installation

> Note: You need to have HADDOCK installed on your system. Please refer to the [HADDOCK2.4 installation instructions](/software/haddock2.4/installation){:target="_blank"} or [HADDOCK3.0 repository](https://github.com/haddocking/haddock3){:target="_blank"} for more information, or refer to the local installation tutorials for [HADDOCK2.4](/education/HADDOCK24/HADDOCK24-local-tutorial/){:target="_blank"} and [HADDOCK3](/education/HADDOCK3/HADDOCK3-antibody-antigen/){:target="_blank"}.

`haddock-runner` is open-source, licensed under Apache 2.0 and freely available from the following repository: [github.com/haddocking/haddock-runner](https://github.com/haddocking/haddock-runner){:target="_blank"}.

Simply download the latest binary from the [releases page](https://github.com/haddocking/haddock-runner/releases){:target="_blank"}, for example:

{% highlight bash %}
> wget https://github.com/haddocking/haddock-runner/releases/download/v1.0.0/haddock-runner_1.0.0_linux_386.tar.gz
> tar -zxvf haddock-runner_1.0.0_linux_386.tar.gz
> ./haddock-runner -version
haddock-runner version v1.0.0
{% endhighlight %}

Additionally, you can build the latest version from source, make sure [`go` is installed](https://go.dev/doc/install){:target="_blank"} and run the following commands:

{% highlight bash %}
> git clone https://github.com/haddocking/haddock-runner.git
> cd haddock-runner
> go build -o haddock-runner
> ./haddock-runner -version
haddock-runner version v1.0.0
{% endhighlight %}

***

## Setting up the benchmark

The setup consists of the following steps:

1. Writing the input file list of the targets `input.list`
2. Writing a `run-haddock.sh` script
3. Preparing the configuration file, `benchmark.yaml`
4. Running `haddock-runner`


### 1. Creating the `input.list` file

The input list is a flat text file with the paths of the targets;

{% highlight bash %}
/home/rodrigo/projects/haddock-benchmark/data/complex1_r_u.pdb
/home/rodrigo/projects/haddock-benchmark/data/complex1_l_u.pdb
/home/rodrigo/projects/haddock-benchmark/data/complex1_ti.tbl
# comments are allowed, use it to organize your file
/home/rodrigo/projects/haddock-benchmark/data/complex2_r_u.pdb
/home/rodrigo/projects/haddock-benchmark/data/complex2_l_u.pdb
/home/rodrigo/projects/haddock-benchmark/data/complex2_ti.tbl
/home/rodrigo/projects/haddock-benchmark/data/complex2_ligand.top
/home/rodrigo/projects/haddock-benchmark/data/complex2_ligand.param
{% endhighlight %}

Note that this file **must** follow the pattern:
{% highlight bash %}
path/to/the/structure/NAME_receptor_suffix.pdb
path/to/the/structure/NAME_ligand_suffix.pdb
{% endhighlight %}

In the above example, `complex1` and `complex2` correspond thus to `NAME`, identifying the complex which is modelled.
Each PDB file (indicated by the `.pdb` extension) has a **suffix**, this is extremely important as it will be used to organize the data. For example, the file `complex1_r_u.pdb` is the receptor of the target `complex1` and `complex1_l_u` is the ligand of the same target.

In this example the suffixes are: `receptor_suffix: "_r_u"` and `ligand_suffix: "_l_u"`. The suffixes are defined in the `benchmark.yaml` file.

The same logic applies to the restraints files, in the example above the pattern for the ambiguous restraint can be defined as `ambig: "ti"`, so the file `complex1_ti.tbl` will be used as the ambiguous restraint for the target `complex1`, `complex2_ti.tbl` for the target `complex2`, etc. See section 3.2.2 for information specific to the definition of restraints when setting up a HADDOCK3.0 run.

HADDOCK supports many modified amino acids/bases/glycans/ions (check the [full list](https://wenmr.science.uu.nl/haddock2.4/library){:target="_blank"}). However if your target molecule is not present in this library, you can also provide it following the same logic; `topology: "_ligand.top"` and `param: "_ligand.param"` will use the files `protein2_ligand.top` and `protein2_ligand.param` for the target `protein2`.

> **IMPORTANT**: For ensembles, *provide each model individually* and append a number to the suffix, for example: `complex1_l_u_1.pdb`, `complex1_l_u_2.pdb`, etc.

See below a full example:

{% highlight bash %}
# -------------------------------- #
# 1A2K
./example/1A2K/1A2K_r_u.pdb
./example/1A2K/1A2K_l_u.pdb
./example/1A2K/1A2K_ligand.top
./example/1A2K/1A2K_ligand.param
./example/1A2K/1A2K_ti.tbl
./example/1A2K/1A2K_unambig.tbl
# 1GGR
./example/1GGR/1GGR_r_u.pdb
./example/1GGR/1GGR_l_u_1.pdb
./example/1GGR/1GGR_l_u_2.pdb
./example/1GGR/1GGR_l_u_3.pdb
./example/1GGR/1GGR_l_u_4.pdb
./example/1GGR/1GGR_l_u_5.pdb
./example/1GGR/1GGR_ti.tbl
# 1PPE
./example/1PPE/1PPE_l_u.pdb
./example/1PPE/1PPE_r_u.pdb
./example/1PPE/1PPE_ti.tbl
./example/1PPE/1PPE_hb.tbl
./example/1PPE/1PPE_unambig.tbl
# 2OOB
./example/2OOB/2OOB_l_u.pdb
./example/2OOB/2OOB_r_u.pdb
./example/2OOB/2OOB_ti.tbl
./example/2OOB/2OOB_hb.tbl
# -------------------------------- #
{% endhighlight %}

### 2. Writing the `run-haddock.sh` script

The `run-haddock.sh` script is a bash script that will be executed by `haddock-runner` for each target. The purpose of this script is to provide an "adapter" to account for different HADDOCK versions and/or different python versions and even different operating systems and configurations on your cluster.

This script should contain all the commands necessary to run HADDOCK and it must be customized for your installation, for example:

> `haddock24.sh`
{% highlight bash %}
#!/bin/bash
#===============================================================================
# HADDOCK2.4 runs on python2.7, which is EOL.
# This script is a workaround to run HADDOCK with a custom python2 installation

## With pyenv
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv shell 2.7.18

## With Anaconda
# source $HOME/miniconda3/etc/profile.d/conda.sh
# conda create -n haddock24_env python=2.7
# conda activate haddock24_env

#===============================================================================
# Configure HADDOCK2.4
export HADDOCK="$HOME/repos/haddock24"
export HADDOCKTOOLS="$HADDOCK/tools"
export PYTHONPATH="${PYTHONPATH}:$HADDOCK"

python "$HADDOCK/Haddock/RunHaddock.py"
#===============================================================================
{% endhighlight %}

> `haddock3.sh`
{% highlight bash %}
#!/bin/bash
#===============================================================================
HADDOCK3_DIR="$HOME/repos/haddock3"

# Activate the virtual environment
source "$HADDOCK3_DIR/venv/bin/activate" || exit

### Or if installed with conda
## source $HOME/miniconda3/etc/profile.d/conda.sh
## conda activate haddock3

# Mind the "$@" at the end, this is necessary to pass the arguments to the script
haddock3 "$@"
#===============================================================================
{% endhighlight %}


### 3. Writing the `benchmark.yaml` file

The `benchmark.yaml` file is a configuration file in [`YAML`](https://yaml.org/){:target="_blank"} format that will be used by `haddock-runner` to run the benchmark. This file is divided in 2 main sections; `general` and `scenarios`

#### 3.1. General section

Here you must define the following:

* `executable`: the path to the `run-haddock.sh` script (see above for more details)
* `max_concurrent`: the maximum number of runs that can be executed at a given time (a run is a target in a given scenario)
* `haddock_dir`: the path to the HADDOCK installation
* `receptor_suffix`: the suffix used to identify the receptor files
* `ligand_suffix`: the suffix used to identify the ligand files
* `input_list`: the path to the input list (see above for more details)
* `work_dir`: the path to the benchmark output

{% highlight yaml %}
general:
  executable: /trinity/login/rodrigo/projects/benchmarking/haddock24.sh
  max_concurrent: 2
  haddock_dir: /trinity/login/abonvin/haddock_git/haddock2.4
  receptor_suffix: _r_u
  ligand_suffix: _l_u
  input_list: /trinity/login/rodrigo/projects/benchmarking/input.txt
  work_dir: /trinity/login/rodrigo/projects/benchmarking
{% endhighlight %}


#### 3.2. Scenario section

Here you must define the scenarios that you want to run, it is slightly different for HADDOCK2.4 and HADDOCK3.0.

##### 3.2.1 HADDOCK2.4

For HADDOCK2.4 you must define the following:

* `name`: the name of the scenario
* `parameters`: the parameters to be used in the scenario
  * `run_cns`: parameters that will be used in the `run.cns` file
  * `restraints`: patterns used to identify the restraints files
    * `ambig`: pattern used to identify the ambiguous restraints file
    * `unambig`: pattern used to identify the unambiguous restraints file
    * `hbonds`: pattern used to identify the hydrogen bonds restraints file
  * `custom_toppar`: patterns used to identify the custom topology files
    * `topology`: pattern used to identify the topology file
    * `param`: pattern used to identify the parameter file

{% highlight yaml %}
# HADDOCK2.4
scenarios:
  - name: true-interface
    parameters:
      run_cns:
        noecv: false
        structures_0: 1000
        structures_1: 200
        waterrefine: 200
      restraints:
        ambig: ti

{% endhighlight %}


##### 3.2.2 HADDOCK3.0

> Note: HADDOCK3.0 is still under development and is not meant to be used for production runs! Please use HADDOCK2.4 instead.

> For information about the available modules, please refer to the [HADDOCK3 tutorial](/education/HADDOCK3/HADDOCK3-antibody-antigen/#a-brief-introduction-to-haddock3){:target="_blank"} and the [documentation](https://www.bonvinlab.org/haddock3){:target="_blank"}.

For HADDOCK3.0 you must define the following:

* `name`: the name of the scenario
* `parameters`: the parameters to be used in the scenario
  * `general`: general parameters; those are the ones defined in the "top" section of the `run.toml` script
  * `modules`: this subsection is related to the parameters of each module in HADDOCK3.0
    * `order`: the order of the modules to be used in HADDOCK3.0
    * `<module-name>`: parameters for the module


{% highlight yaml %}
# HADDOCK3.0
scenarios:
  - name: true-interface
    parameters:
      general:
        # execution mode using a batch system
        mode: hpc
        # batch queue name to use
        queue: short
        # number of jobs to submit to the batch system
        queue_limit: 100
        # number of models to concatenate within one job
        concat: 5

      modules:
        order: [topoaa, rigidbody, seletop, flexref, emref]
        topoaa:
          autohis: true
        rigidbody:
          ambig_fname: "_ti.tbl"
        seletop:
          select: 200
        flexref:
        emref:

 {% endhighlight %}


#### 3.2 Full example

Here is a full example of the `benchmark.yaml` file:

> `HADDOCK2.4`

{% highlight yaml %}
general:
  executable: /Users/rodrigo/repos/haddock-runner/haddock24.sh
  max_concurrent: 2
  haddock_dir: /Users/rodrigo/repos/haddock
  receptor_suffix: _r_u
  ligand_suffix: _l_u
  input_list: /Users/rodrigo/repos/haddock-runner/example/input_list.txt
  work_dir: /Users/rodrigo/repos/haddock-runner/bm-goes-here

scenarios:
  - name: true-interface
    parameters:
      run_cns:
        noecv: false
        structures_0: 1000
        structures_1: 200
        waterrefine: 200
      restraints:
        ambig: ambig
        unambig: restraint-bodies
        hbonds: hbonds
      custom_toppar:
        topology: _ligand.top
        param: _ligand.param

  - name: center-of-mass
    parameters:
      run_cns:
        cmrest: true
        structures_0: 10000
        structures_1: 400
        waterrefine: 400
        anastruc_1: 400
      custom_toppar:
        topology: _ligand.top
        param: _ligand.param

  - name: random-restraints
    parameters:
      run_cns:
        ranair: true
        structures_0: 10000
        structures_1: 400
        waterrefine: 400
        anastruc_1: 400
      custom_toppar:
        topology: _ligand.top
        param: _ligand.param

  #-----------------------------------------------
{% endhighlight %}

> `HADDOCK3.0`
{% highlight yaml %}
general:
  executable: /Users/rvhonorato/repos/haddock-runner/haddock3.sh
  max_concurrent: 4
  haddock_dir: /Users/rvhonorato/repos/haddock3
  receptor_suffix: _r_u
  ligand_suffix: _l_u
  input_list: /Users/rvhonorato/repos/haddock-runner/example/input_list.txt
  work_dir: /Users/rvhonorato/repos/haddock-runner/bm-goes-here

scenarios:
  - name: true-interface
    parameters:
      general:
        mode: hpc
        queue: short
        queue_limit: 100
        concat: 5

      modules:
        order: [topoaa, rigidbody, seletop, flexref, emref, clustfcc, seletopclusts]
        topoaa:
          autohis: true
        rigidbody:
          ambig_fname: _ambig.tbl
          unambig_fname: _restraint-bodies.tbl
          ligand_param_fname: _ligand.param
          ligand_top_fname: _ligand.top
        seletop:
          select: 200
        flexref:
          ambig_fname: _ambig.tbl
          unambig_fname: _restraint-bodies.tbl
          ligand_param_fname: _ligand.param
          ligand_top_fname: _ligand.top
        emref:
          ambig_fname: _ambig
        clustfcc:
        seletopclusts:

  - name: center-of-mass
    parameters:
      general:
        mode: hpc
        queue: short
        queue_limit: 100
        concat: 5

      modules:
        order: [topoaa, rigidbody, seletop, flexref, emref, clustfcc, seletopclusts]
        topoaa:
          autohis: true
        rigidbody:
          sampling: 10000
          cmrest: true
          ligand_param_fname: _ligand.param
          ligand_top_fname: _ligand.top
        seletop:
          select: 400
        flexref:
          ligand_param_fname: _ligand.param
          ligand_top_fname: _ligand.top
        emref:
        clustfcc:
        seletopclusts:

  - name: random-restraints
    parameters:
      general:
        mode: hpc
        queue: short
        queue_limit: 100
        concat: 5

      modules:
        order: [topoaa, rigidbody, seletop, flexref, emref, clustfcc, seletopclusts]
        topoaa:
          autohis: true
        rigidbody:
          sampling: 10000
          ranair: true
          ligand_param_fname: _ligand.param
          ligand_top_fname: _ligand.top
        seletop:
          select: 400
        flexref:
          contactairs: true
          ligand_param_fname: _ligand.param
          ligand_top_fname: _ligand.top
        emref:
          contactairs: true
          ligand_param_fname: _ligand.param
          ligand_top_fname: _ligand.top
        clustfcc:
        seletopclusts:

  #-----------------------------------------------
{% endhighlight %}


### 3.3 Running the benchmark

Considering the config input file and the config `.yaml` file have been properly set, you can run the benchmark by executing the `haddock-runner` simply with:

{% highlight bash %}
$ ./haddock-runner my-benchmark-config-file.yml &
{% endhighlight %}

`haddock-runner` will read the input file, create the working directory, copy the input files to a `data/` directory and start the benchmark. Make sure you have enough space in your disk to store the input files and the results.

**VERY IMPORTANT:** In the current version, `haddock-runner` does not submit jobs to the queue, instead it leverages the internal scheduling routines of HADDOCK2.4/HADDOCK3.0. This means that the number of concurrent runs is related to the number of docking runs at a given time, not to the total number of processors being used by HADDOCK! The actual number of processors being used depends on how HADDOCK was configured. For HADDOCK2.4 this depends on parameters defined in the `run.cns` (`queue_N`/`cpunumber_N`) and for HADDOCK3, the number of processors (or queue slots) to use and the running mode is defined in the config file under the `general` section (see examples above).

**Example:** `max_concurrent: 10` with `scenarios.parameters.mode: local` and `scenarios.parameters.ncores: 10` means 10x10 processors will be required!


## Setting up a benchmark experiment with the Docking benchmark 5 (BM5)

The Protein-Protein docking benchmark v5 ([Vreven, 2015](https://doi.org/10.1016/j.jmb.2015.07.016){:target="_blank"}), namely BM5, contains a is a large set of non-redundat high-quality structures, check [here](https://zlab.umassmed.edu/benchmark/){:target="_blank"} the full set.

The BonvinLab provides a HADDOCK-ready sub-version of the BM5 which can be easily used as input for `haddock-runner`. This version is available the following repository; [github.com/haddocking/BM5-clean](https://github.com/haddocking/BM5-clean){:target="_blank"}. Below we will go over step-by-step instructions on how to use it as input.

### 1. Downloading the BM5-clean

Clone the repository and checkout a version. Note that its always recomended to use a specific version, as the main branch might change and for reproducibility.

{% highlight bash %}
> git clone https://github.com/haddocking/BM5-clean.git && cd BM5-clean
> git checkout v1.1
{% endhighlight %}

### 2. Create `bm5-input.list`

As previously mentioned, the `BM5-clean` repository is already an organized sub-version, thus its very simple to create the `bm5-input.list` file with a few bash commands;

{% highlight bash %}
> ls `pwd`/HADDOCK-ready/**/*.{pdb,tbl} | grep -v "ana_scripts\|matched\|cg" | sort > bm5-input.list
> head bm5-input.list && echo "..." && tail bm5-input.list
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1A2K/1A2K_ambig.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1A2K/1A2K_ambig5.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1A2K/1A2K_hbonds.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1A2K/1A2K_l_u.pdb
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1A2K/1A2K_l_u_GDP.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1A2K/1A2K_r_u.pdb
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1A2K/1A2K_restraint-bodies.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1A2K/1A2K_target.pdb
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1ACB/1ACB_ambig.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/1ACB/1ACB_ambig5.tbl
...
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/BP57/BP57_r_u.pdb
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/BP57/BP57_restraint-bodies.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/BP57/BP57_target.pdb
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/CP57/CP57_ambig.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/CP57/CP57_ambig5.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/CP57/CP57_hbonds.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/CP57/CP57_l_u.pdb
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/CP57/CP57_r_u.pdb
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/CP57/CP57_restraint-bodies.tbl
/Users/rvhonorato/projects/benchmarking/BM5-clean/HADDOCK-ready/CP57/CP57_target.pdb
{% endhighlight %}

### 3. Add `bm5-input.list` to the `haddock-runner` configuration file

{% highlight yaml %}
general:
  # ...
  input_list: /Users/rvhonorato/projects/benchmarking/BM5-clean/bm5-input.list
  # ...
{% endhighlight %}

***

## Getting help

If you encounter any issues or have any questions, please open an issue on the [GitHub repository](https://github.com/haddocking/haddock-runner){:target="_blank"}, contact us at *software.csb [at] gmail.com* or join the [BioExcel forum](https://ask.bioexcel.eu){:target="_blank"} and post your question there.

## Final considerations

The `haddock-runner` is under active development and we have a list of planned features, such as an option to resume/restart the benchmark and a full suite of analysis.

If you have any suggestions, or feedback please let us know! 🤓
