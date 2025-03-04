# Command line interfaces

Haddock3 is a software that can read configuration files and compute data.
While there will be [a web application](https://github.com/i-VRESSE/haddock3-webapp), haddock3 does not have a graphical user interface and must used from the command line.
While this may have some negative impact for some inexperienced users, it is also very powerful as it allows custom scripting to launch haddock3, and therefore integrating it in your own pipelines is easier.


To use the command line interface, you must open a terminal:
* [iTerm / Terminal]: for Mac users, default terminals are available and fully functional.
* [WindowsPowerShell]: The Windows solution to open a terminal.
* [VSCode](): an integrated developing environment (IDE) that allows you to run command lines in the terminal.


Haddock3 comes with several Command Line Interfaces (CLIs), that are described and listed below:

- [haddock3](#haddock3): Main CLI for running a workflow.
- [haddock3-cfg](#haddock3-cfg): Obtain information about module parameters
- [haddock3-restraints](#haddock3-restraints): Generation of restraints.
- [haddock3-score](#haddock3-score): Scoring CLI.
- [haddock3-analyse](#haddock3-analyse): Analysis of output.
- [haddock3-traceback](#haddock3-analyse): Traceback of generated docking models.
- [haddock3-re](#haddock3-re): Recomputing modules with different parameters.
  - [haddock3-re score](#-re-score): To modify scoring function weights.
  - [haddock3-re clustfcc](#-re-clustfcc): To modify `[clustfcc]` parameters.
  - [haddock3-re clustrmsd](#-re-clustrmsd): To modify `[clustrmsd]` parameters.
- [haddock3-copy](#haddock3-copy): To copy a haddock3 run.
- [haddock3-clean](#haddock3-clean): Archiving a run.
- [haddock3-unpack](#haddock3-unpack): Uncompressing an archived a run.
- [haddock3-pp](#haddock3-pp): Pre-processing of input files.


## haddock3

The main command line, `haddock3` is used to launch a Haddock3 workflow from a [configuration file](./config_file.md).
It takes a positional argument, the path to the configuration file.

```bash
haddock3 workflow.cfg
```

Also, two optional arguments can be used:

- `--restart <module_id>`: allows to restart the workflow restarting for the module id. Note that previously generated folders from the selected step onward will be deleted.
- `--extend-run <run_directory>`: allows to start the new workflow from the last step of a previously computed run.

<hr>

## haddock3-cfg

Another very interesting CLI is `haddock3-cfg`.
This CLI allows you to list the parameter names, their description, and default values for each available module.
Used without any option, the command `haddock3-cfg` will return all [Global parameters](/software/haddock3/manual/global_parameters).

To access the list of parameters for a given module, you should use the optional argument `-m <module_name>`.
As an example, to list available parameters for the module `seletopclusts`, you should run the following command:

```bash
haddock3-cfg -m seletopclusts
```

Please note that all the parameters for each module are also available in the [online documentation](https://www.bonvinlab.org/haddock3/modules/index.html).

<hr>

## haddock3-restraints

The CLI `haddock3-restraints` is made to generate restraints used either as ambiguous restraints or unambiguous ones.
The `haddock3-restraints` CLI is composed of several sub-commands, each one dedicated to some specific actions, such as:

- Searching for solvent-accessible residues
- Gathering neighbors of a selection
- Maintaining the conformation of a single chain with a potential gap
- Generating ambiguous restraints from active and passive residues
- Generating planes and corresponding restraints

As this CLI is more specialized, we have made a [special chapter in this manual](./restraints_cli.md) to explain all the functionalities.

<hr>

## haddock3-score

The `haddock3-score` is a CLI made for scoring a single complex.
The topologies are created and a small energy minimization is performed on the complex before the evaluation of the haddock score components.
It is dedicated to the scoring of it and only returns the computed haddock score and its components.
It is a shortcut to a full configuration file that would contain the `topoaa` and `emscoring` modules.

To use it, provide the path to the complex to be scored:

```bash
haddock3-score path/to/complex.pdb
```

This CLI can take optional parameters using the `-p` flag, where the user can provide the set of parameters and values to tune the weights of the Haddock scoring function.
Be aware that only parameters available for the `emscoring` module are accepted.

To tune the haddock3 scoring function weights, there are basically only 5 parameters to be tuned.

- **w_vdw**: to tune the weight of the Van der Waals term
- **w_elec**: to tune the weight of the Electrostatic term
- **w_desolv**: to tune the weight of the Desolvation term
- **w_air**: to tune the weight of the Ambiguous Restraints term
- **w_bsa**: to tune the weight of the Buried Surface Area term

Note that, if a parameter is not tuned, the default scoring function weights are used.


As an example, this command would tune the Van der Waals term during the evaluation of the complex:

```bash
haddock3-score path/to/complex.pdb -p w_vdw 0.5
```

Note how the parameter name and its new value are separated by a space.

To modify multiple parameters, just add the new parameter separated by a space:

```bash
haddock3-score path/to/complex.pdb -p w_vdw 0.5 w_bsa 0.2
```

<hr>

## haddock3-analyse

Haddock3 contains functionalities that allow the analysis of various steps of the workflow, even after it has been completed. The `haddock3-analyse` command is the main tool for the analysis of one or more workflow steps. Typically it runs automatically at the end of a HADDOCK3 workflow (activated by the [`postprocess`](#the-postprocess-option) option), but it can be run independently as well.

```
haddock3-analyse -r my-run-folder -m 2 5 6
```

Here `my-run-folder` is the run directory and 2, 5, and 6 are the steps that you want to analyze.

The command will inspect the folder, looking for the existing models. If the selected module is a `caprieval` module, `haddock3-analyse` simply loads the `capri_ss.tsv` and `capri_clt.tsv` files
produced by the `caprieval` module. Otherwise, `haddock3-analyse` runs a `caprieval` analysis of the models.
You can provide some [caprieval-specific parameters](https://github.com/haddocking/haddock3/blob/main/src/haddock/modules/analysis/caprieval/defaults.yaml)
using the following syntax:

```
haddock3-analyse -r my-run-folder -m 2 5 6 -p reference_fname my_ref.pdb receptor_chain F
```

Here the `-p` key tells the code that you are about to insert `[caprieval]` parameters, whose name should match the parameter name of the module. Each parameter name and the corresponding value must be separated by a space character.

Another parameter that can be specified is `top_cluster`, which defines how many of the first N clusters will be considered in the analysis.
This value is set to 10 by default.

```
haddock3-analyse -r my-run-folder -m 2 5 6 --top_cluster 12
```

This number is meaningless when dealing with models with no cluster information, that is, models that have never been clustered before.

By default `haddock3-analyse` produces [plotly](https://plotly.com/python/) plots in the HTML `format`, but the user can select 
one of the formats available [here](https://plotly.github.io/plotly.py-docs/generated/plotly.io.write_image.html), 
while also adjusting the resolution with the `scale` parameter:

```
haddock3-analyse -r my-run-folder -m 2 5 6 --format pdf --scale 2.0
```

#### The analysis folder

After running `haddock3-analyse` you can check the content of the `analysis` directory in your run folder.
If everything went successfully, one of the above commands should have produced an analysis folder structured as

```
my-run-folder/
|--- analysis/
 |--- 2_caprieval_analysis
 |--- 5_seletopclusts_analysis
 |--- 6_flexref_analysis
```

Each subfolder contains all the analysis plots related to that specific step of the workflow.

By default `haddock3-analyse` produces a set of scatter plots that compare each HADDOCK energy term 
(i.e., the HADDOCK score and its components) to the different metrics used to evaluate the quality of a model,
such as the interface-RMSD, Fnat, DOCKQ, and so on. An example is available [here](https://www.bonvinlab.org/education/HADDOCK3/HADDOCK3-antibody-antigen/plots/scenario1-surface/irmsd_score.html).

For each of the energy components and the metrics mentioned above `haddock3-analyse` produces also a box plot, in which each cluster 
is considered separately. An example is available [here](../../../education/HADDOCK3/HADDOCK3-antibody-antigen/plots/scenario1-surface/score_clt.html).

#### The report

Scatter plots, box plots, CAPRI statistics, and interactive visualization of the models are available in the `report.html` file, present
in each analysis subfolder. In order to visualize the models it is necessary to start a local server at the end of the `haddock3-analyse` run,
following the indications provided in the log file:

```
[2023-08-24 10:09:09,552 cli_analyse INFO] View the results in analysis/12_caprieval_analysis/report.html
[2023-08-24 10:09:09,552 cli_analyse INFO] To view structures or download the structure files, in a terminal run the command
`python -m http.server --directory /haddock3/examples/docking-antibody-antigen/run1-CDR-acc-cltsel-test`.
By default, http server runs on `http://0.0.0.0:8000/`. Open the link
http://0.0.0.0:8000/analysis/12_caprieval_analysis/report.html in a web browser.
```

Launch this command to open the report:
```
python -m http.server --directory path-to-my-run
```

In the browser, you can navigate to each analysis subfolder and open the `report.html` file. If you are not interested in
visualizing the models, you can simply open the `report.html` file in a standard browser. An example report can be visualized [here](../../../education/HADDOCK3/HADDOCK3-protein-glycan/plots/report.html).


<hr>

## haddock3-traceback

HADDOCK3 is highly customizable and modular, as the user can introduce several refinement, clustering, and scoring steps in a workflow.
Quantifying the impact of the different modules is important while developing a novel docking protocol. The `haddock3-traceback` command
is developed to assist the user in this task, as it allows to "connect" all the models generated in a HADDOCK3 workflow:

```
haddock3-traceback my-run-folder
```

`haddock3-traceback` creates a traceback subfolder within the `my-run-folder` directory, containing a `traceback.tsv` table:

```
00_topo1     00_topo2        01_rigidbody            01_rigidbody_rank       04_seletopclusts        04_seletopclusts_rank   06_flexref      06_flexref_rank 
4G6K.psf     4I1B.psf        rigidbody_10.pdb        3                       cluster_1_model_1.pdb   1                       flexref_1.pdb   2       
4G6K.psf     4I1B.psf        rigidbody_11.pdb        10                      cluster_1_model_2.pdb   3                       flexref_3.pdb   1       
4G6K.psf     4I1B.psf        rigidbody_18.pdb        4                       cluster_2_model_1.pdb   2                       flexref_2.pdb   4      
4G6K.psf     4I1B.psf        rigidbody_20.pdb        15                      cluster_2_model_2.pdb   4                       flexref_4.pdb   3       
```

In this table, each row represents a model that has been produced by the workflow.
The (typically) two used topologies are reported first,
and then each module has its own column, containing the name and rank of the model at that stage.
As an example, in the first row of the
table above `rigidbody_10.pdb` is ranked 3rd at the `rigidbody` stage.
Then, it becomes `cluster_1_model_1.pdb` (ranked 1st) after 
the `seletopclusts` module.
This model is then refined in `flexref_1.pdb`, which turns out to be the 2nd best model at the end of the workflow.

The table can be easily parsed and used to evaluate the impact of different refinement steps on the different models.

## The postprocess option

You may want to run the `haddock3-analyse` and `haddock3-traceback` commands by default at the end of the workflow.
The `postprocess` option of a standard HADDOCK3 configuration (.cfg) file is devoted to this task. At first, it forces HADDOCK3 
to execute `haddock3-analyse` on all the `XX_caprieval` folders found in the workflow, therefore loading data present in the CAPRI tables.
Second, it executes the `haddock3-traceback` command.

By default, `postprocess` is set to `true` but can also be de-activated at the beginning of your configuration file:

```
 ====================================================================
# This is a HADDOCK3 configuration file

# directory in which the docking will be done
run_dir = "my-run-folder"

# postprocess the run
postprocess = false

...
```

**Note**: If speed is an issue, please turn the postprocess option off for your run!


You can find additional help by running the command: `haddock3-analyse -h` and `haddock3-traceback -h` and reading
the parameters' explanations. Otherwise, ask us in the ["issues" forum](https://github.com/haddocking/haddock3/issues).

<hr>

## haddock3-re

The `haddock3-re` CLI is dedicated to **re**computing some steps in your workflow.
This can be very useful as it allows us to fine-tune parameters and evaluate the impact on the results.

`haddock3-re` takes two mandatory positional arguments:

- **1: **The name of the subcommand
- **2: **Path to the module on which to apply the modifications in your run

By running `haddock3-re`, a new directory will be created, with the `_interactive` suffix, where the new results are stored.
Relaunching several times `haddock3-re` on the same directory will update the content in the `_interactive` one.

For now, three modules can be **re**computed and tuned, `[caprieval]`, `[clustfcc]` and `[clustrmsd]`.

### -re score

The subcommand `haddock3-re score`, allows to tune the weights of the [HADDOCK scoring function](./haddocking#haddock-scoring-function).
It takes a `[caprieval]` step folder as positional argument and the tuned weights for the scoring function.

Note that if you do not provide new weights as optional arguments, previous weights used in the run are used.

Usage:
```bash
haddock3-re clustrmsd <path/to/the/module/step/X_caprieval>

optional arguments:
  -e W_ELEC, --w_elec W_ELEC
                        weight of the electrostatic component.
  -w W_VDW, --w_vdw W_VDW
                        weight of the van-der-Waals component.
  -d W_DESOLV, --w_desolv W_DESOLV
                        weight of the desolvation component.
  -b W_BSA, --w_bsa W_BSA
                        weight of the BSA component.
  -a W_AIR, --w_air W_AIR
                        weight of the AIR component.
```

### -re clustfcc

The subcommand `haddock3-re clustfcc`, allows to tune the clustering parameters of the `[clustfcc]` module.
It takes a `[clustfcc]` step folder as a positional argument and the tuned parameters for the module.

Note that if you do not provide new parameters as optional arguments, previous ones will be used instead.

Usage:
```bash
haddock3-re clustfcc <path/to/the/module/step/X_clustfcc>

optional arguments:
  -f CLUST_CUTOFF, --clust_cutoff CLUST_CUTOFF
                        Minimum fraction of common contacts to be considered in a cluster.
  -s STRICTNESS, --strictness STRICTNESS
                        Strictness factor.
  -t MIN_POPULATION, --min_population MIN_POPULATION
                        Clustering population threshold.
  -p, --plot_matrix     Generate the matrix plot with the clusters.
```

### -re clustrmsd

The subcommand `haddock3-re clustrmsd`, allows to tune the clustering parameters of the `[clustrmsd]` module.
It takes a `[clustrmsd]` step folder as a positional argument, and the tuned parameters for the module.

Note that if you do not provide new parameters as optional arguments, previous ones will be used instead.

Usage:
```bash
haddock3-re clustrmsd <path/to/the/module/step/X_clustrmsd>

optional arguments:
  -n N_CLUSTERS, --n_clusters N_CLUSTERS
                        number of clusters to generate.
  -d CLUST_CUTOFF, --clust_cutoff CLUST_CUTOFF
                        clustering cutoff distance.
  -t MIN_POPULATION, --min_population MIN_POPULATION
                        minimum cluster population.
  -p, --plot_matrix     Generate the matrix plot with the clusters.
```

Please note that parameters `--n_clusters` (defining the number of clusters you want)
and `--clust_cutoff` are mutually exclusive,
as the former is cutting the dendrogram at a height satisfying the number of desired clusters
while the latter is cutting the dendrogram at the `--clust_cutoff` value height.


<hr>

## haddock3-copy

The `haddock3-copy` CLI allows one to copy the content of a run to another run directory.

It takes three arguments:
- **`-r run_directory`** is the directory of a previously computed haddock3 run.
- **`-o new_run_directory`** is the new directory where to make to copy of the old run.
- **`-m module_id_X module_id_Y`** is the list of modules you wish to copy (separated by spaces).

As an example, consider your previous run directory is named `run1` and contains the following modules:

```bash
run1/
  0_topoaa/
  1_rigidbody/
  2_caprieval/
  3_seletop/
  4_flexref/
 (etc...)
```

You may want to use `4_flexref` step folder as a starting point for a new run named `run2`.
To do so, run the following command:

```bash
haddock3-copy -r run1 -m 0 4 -o run2
```

**Notes**:
- the flag `-m` allows to define which modules must be copied, and modules `0` (for `0_topoaa`) and `4` (for `4_flexref`) are space separated.
- in this case, we also copy the content of `0_topoaa`, this is because topologies are stored in this module directory, and we must have access to them if we are using another module requiring CNS topology to run.
- it is often recommended to **always** copy the `topoaa` directory, as we will often require the topologies later in the workflow.

**WARNING**:
To copy the content of a run and modify the paths, we are using the `sed` command, searching to replace the previous run directory name (`run1`) with the new one (`run2`) in all the generated files to make sure that paths will be functional in the new run directory.
In some cases, this can lead to some artifacts, such as the modification of attribute names if your run directory contains a name that is used by haddock3.

Here is a list of run directory names **NOT** to use:
- topology
- score
- emref
- etc...

The best solution is to always use a unique name that describes the content of the run.

<hr>

## haddock3-clean

The` haddock3-clean` CLI performs file archiving and file compressing operations on the output of a haddock3 run directory.
This CLI can save you some hard drive storage space, as the multiple files generated by HADDOCK can lead to several gigabytes of data, therefore compressing them allows you to keep them while saving some precious place.

All `.inp` and `.out` files are deleted except for the first one, which is compressed to `.gz`.
On the other hand, all `.seed` and `.con` files are compressed and archived into `.tgz` files.
Finally, `.pdb` and `.psf` files are compressed to `.gz`.

The <run_directory> can either be a whole HADDOCK3 run folder or a specific folder of the workflow step. <ncores> defines the number of threads to use; by default uses a single core.

Please note that by default this CLI is launched automatically at the end of a workflow.
It is exposed as a general parameter `clean = true`.
To switch off this behavior, you can set it to false in your configuration file.


Usages:
```bash
# Display help
haddock3-clean -h
haddock3-clean run1 # Where run1 is a path to a haddock3 run directory
haddock3-clean run1/1_rigidbody  # Where 1_rigidbody is the output of the rigidbody module
haddock3-clean run1 -n  # uses all cores
haddock3-clean run1 -n 2  # uses 2 cores
```

Here is the list of arguments:
```bash
positional arguments:
  run_dir               The run directory.

optional arguments:
  -n [NCORES], --ncores [NCORES]
                        The number of threads to use. Uses 1 if not specified. Uses all available threads if `-n` is given. Else,
                        uses the number indicated, for example: `-n 4` will use 4 threads.
  -v, --version         show version
```

<hr>

## haddock3-unpack

The `haddock3-unpack` CLI is the opposite of the `haddock3-clean` one.
It takes a haddock3 run directory as input (or the output directory of a module), and uncompresses any archived file.

This CLI can be especially useful when your run has been archived, but you would like to open a PDB file using a molecular viewer.

The unpacking process performs file unpacking and file decompressing operations.
Files with extensions `seed` and `con` are unpacked from their `.tgz` files.
While files with `.pdb.gz` and `.psf.gz` extensions are uncompressed.
If `--all` is given, unpack also `.inp.gz` and `.out.gz` files.


Usage:
```bash
# To display help
haddock3-unpack -h
# To unpack the entire run directory
haddock3-unpack run1
# To unpack the output directory of a specific module
haddock3-unpack run1/1_rigidbody
# Define the number of cores to use
haddock3-unpack run1 -n  # uses all cores
haddock3-unpack run1 -n 2  # uses 2 cores
# Add the -a or --all to specify that all compressed files must be unpacked
haddock3-unpack run1 -n 2 -a
haddock3-unpack run1 -n 2 --all
```

Arguments:

```bash
positional arguments:
  run_dir               The run directory.

optional arguments:
  -h, --help            show this help message and exit
  --all, -a             Unpack all files (including `.inp` and `.out`).
  -n [NCORES], --ncores [NCORES]
                        The number of threads to use. Uses 1 if not specified. Uses all available threads if `-n` is given. Else,
                        uses the number indicated, for example: `-n 4` will use 4 threads.
  -v, --version         show version
```

<hr>

## haddock3-pp

The `haddock3-pp` is a pre-processing (-pp) CLI, dedicated to processing PDB files for agreement with HADDOCK3 requirements.

You can use the `--dry` option to report on the performed changes without actually performing the changes.

Corrected PDBs are saved to new files named after the `--suffix` option.
Original PDBs are never overwritten unless the `--suffix` is given an empty string.

You can pass multiple PDB files to the command line.

Usage:
```bash
haddock-pp file1.pdb file2.pdb
haddock-pp file1.pdb file2.pdb --suffix _new
haddock-pp file1.pdb file2.pdb --dry
```

Arguments:

```bash
positional arguments:
  pdb_files             Input PDB files.

options:
  -h, --help            show this help message and exit
  -d, --dry             Perform a dry run. Informs changes without modifying files.
  -t [TOPFILE ...], --topfile [TOPFILE ...]
                        Additional .top files.
  -s SUFFIX, --suffix SUFFIX
                        Suffix to output files. Defaults to '_processed'
  -odir OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        The directory where to save the output.
```
