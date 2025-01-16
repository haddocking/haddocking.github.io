# Analysis modules

- [`[alascan]` module](#alascan-module)
- [`[caprieval]` module](#caprieval-module)
- [`[clustfcc]` module](#clustfcc-module)
- [`[clustrmsd]` module](#clustrmsd-module)
- [`[contactmap]` module](#contactmap-module)
- [`[ilrmsdmatrix]` module](#ilrmsdmatrix-module)
- [`[rmsdmatrix]` module](#rmsdmatrix-module)
- [`[seletop]` module](#seletop-module)
- [`[seletopclusts]` module](#seletopclusts-module)

## `[alascan]` module

HADDOCK3 module for alanine scanning.

This module is responsible for the alanine scan analysis of the models
generated in the previous step of the workflow. For each model, the module
will mutate the interface residues and calculate the energy differences
between the wild type and the mutant, thus providing a measure of the impact
of such mutation.

If cluster information is available, the module will also calculate the
average energy difference for each cluster of models.



#### Notable parameters

The most important parameters for the ``[alascan]`` module are:

- `scan_residue`: the probe residue used for the scanning (alanine by default)
- `resdic_`: list of residues to be mutated (by default all the interface residues). For example, to mutate only residues 2 and 3 of chain A, add resdic_A = [2,3]
- `plot`: plot scanning data (default: False)

More information about ``[alascan]`` parameters can be accessed [here](https://bonvinlab.org/haddock3/modules/analysis/haddock.modules.analysis.alascan.html#default-parameters) or retrieved by running
```bash
haddock3-cfg -m alascan
```

Here is an example configuration file snapshot performing glycine scanning on some residues after Molecular Dynamics refinement:

```toml
# ...
[mdref]
ambig_fname = ambiguous_restraints.tbl
[alascan]
scan_residue = "GLY"
resdic_A = [2,3]
resdic_B = [24,25]

# ...
```
<hr>

## `[caprieval]` module

Calculate CAPRI metrics for the input models.

By default the following metrics are calculated:

- FNAT (fraction of native contacts), namely the fraction of
 intermolecular contacts in the docked complex that are also
 present in the reference complex.
- IRMSD (interface root mean square deviation), namely the RMSD
 of the interface of the docked complex with respect
 to the reference complex.
- LRMSD (ligand root mean square deviation), namely the RMSD of the
 ligand of the docked complex with respect to the
 reference complex upon superposition of the receptor.
- DOCKQ, a measure of the quality of the docked model obtained
 by combining FNAT, I-RMSD and L-RMSD (see
 Basu and Wallner 2016,  11 (8), e0161879).
- ILRMSD (interface ligand root mean square deviation), the RMSD of the
 ligand of the docked complex with respect to the reference complex
 upon superposition of the interface of the receptor.
- GLOBAL_RMSD, the full RMSD between the reference and the model.

The following files are generated:

- **capri_ss.tsv**: a table with the CAPRI metrics for each model.
- **capri_clt.tsv**: a table with the CAPRI metrics for each cluster of models (if clustering information is available).

These files are at the core of the [analysis report produced by HADDOCK3](https://bonvinlab.org/software/haddock3/manual/clis#the-report).

#### Notable parameters

The most important parameters for the ``[caprieval]`` module are:

- `allatoms`: whether to use all the atoms for the analysis (default: False)
- `reference_fname`: the reference structure to compare the models to. It can be the reference structure of the complex or another model (for example, an Alphafold model).
- `receptor_chain`: the chain to be considered as the receptor (default: A)
- `ligand_chains`: the chains to be considered as the ligands (default: all but the receptor chain)

More information about ``[caprieval]`` parameters can be accessed [here](https://bonvinlab.org/haddock3/modules/analysis/haddock.modules.analysis.caprieval.html#default-parameters) or retrieved by running
```bash
haddock3-cfg -m caprieval
```

<hr>

## `[clustfcc]` module

Cluster modules with Fraction of Common Contacts (FCC) similarity.

The module takes the models generated in the previous step and calculates the
contacts between them. Then, the module calculates the FCC matrix and clusters
the models based on the calculated contacts.

For more details please check *Rodrigues, J. P. et al. Proteins: Struct. Funct. Bioinform. 80, 1810–1817 (2012)*.

Typically, the module is run at the end of the docking protocol to cluster the
models and identify the best clusters. Alternatively, ``[clustfcc]`` can also be
used to cluster models generated in a sampling step (such as ``[rigidbody]``) to 
perform a [cluster-based selection](#seletopclusts-module) before proceeding to the next steps (e.g. [refinement modules](./refinement)).

#### Notable parameters

The most important parameters for the ``[clustfcc]`` module are:
- `clust_cutoff`: Minimum fraction of common contacts to be considered in a cluster (default: 0.6). *Tip* In case you retrieve only one cluster with the default value, try to increase this value.
- `min_population`: Threshold employed to exclude clusters with less than this number of members (default: 4)
- `plot_matrix`: whether to plot the FCC matrix (default: False)


<hr>

## `[clustrmsd]` module

RMSD clustering module.

This module takes in input the [RMSD](#rmsdmatrix-module) (or the [ILRMSD](#ilrmsdmatrix-module)) matrix calculated in the previous step and
performs a hierarchical clustering procedure on it, leveraging [scipy routines](https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html) for this purpose.

Essentially, the procedure amounts at lumping the input models in a
progressively coarser hierarchy of clusters, called the dendrogram.

Typically, the module is run at the end of a protein-small molecule docking protocol to cluster the
models and identify the best clusters. In these workflows, ``[clustrmsd]`` is more appropriate than ``[clustfcc]`` 
as most models will share a consistent fraction of contacts, while still being structurally different.
In [this paper](https://www.biorxiv.org/content/10.1101/2024.07.31.605986v1), we show that, in the context of protein-glycan docking, RMSD clustering performed after 
``[rigidbody]`` docking increases the success rate. A detailed tutorial on this specific case is available [here](https://www.bonvinlab.org/education/HADDOCK3/HADDOCK3-protein-glycan/).

Example application of the ``[clustrmsd]`` module after rigid-body docking, retrieving 50 clusters:

```toml
# ...
[rigidbody]
ambig_fname = ambiguous_restraints.tbl
[rmsdmatrix]
resdic_A = [1,2,3,4]
resdic_B = [2,3,4,5]
[clustrmsd]
n_clusters = 50
# ...
```

#### Notable parameters

The most important parameters for the ``[clustrmsd]`` module are:
* `linkage`: governs the way clusters are merged together in the creation of
 the dendrogram
* `criterion`: defines the prescription to cut the dendrogram and obtain the
 desired clusters
* `n_clusters`: number of desired clusters (if `criterion` is `maxclust`).
* `clust_cutoff`: value of distance that separates distinct clusters (if `criterion` is
  ``distance``)
* `min_population`: analogously to the `clustfcc` module, it is the minimum number
 of models that should be present in a cluster to consider it. If criterion is
  `maxclust`, the value is ignored.
- `plot_matrix`: whether to plot the matrix of cluster members (default: False)

<hr>

## `[contactmap]` module

Compute contacts between chains in complexes.

The `[contactmap]` module aims at generating heatmaps and chordcharts of
the contacts observed in the input complexes.

If complexes are clustered, the analysis of contacts will be performed
based on all structures from each cluster.

**Heatmaps** are describing the probability of contacts (<5A) between two
residues (both intramolecular and intermolecular).

**Chordcharts** are describing only intermolecular contacts in circles,
connecting with *chords* the two residues that are contacting.


<hr>

## `[ilrmsdmatrix]` module

Calculate the Interface Ligand Root Mean Square Deviation (ILRMSD) matrix.

This module calculates of the interface-ligand RMSD (ilRMSD) matrix between all
the models generated in the previous step.

As all the pairwise ilRMSD calculations are independent, the module distributes
them over all the available cores in an optimal way.

**IMPORTANT**: the module assumes coherent numbering for all the receptor and ligand
chains, as no sequence alignment is performed. The user must ensure that the numbering
is coherent.

#### Notable parameters

The most important parameters for the ``[ilrmsdmatrix]`` module are:

- `contact_distance_cutoff`: the distance cutoff to consider a contact (default: 5.0)
- `allatoms`: whether to use all the atoms for the ILRMSD calculation (default: False)
- `receptor_chain`: the chain to be considered as the receptor (default: A)
- `ligand_chains`: the chains to be considered as the ligands (default: all but the receptor chain)

More information about ``[ilrmsdmatrix]`` parameters can be accessed [here](https://bonvinlab.org/haddock3/modules/analysis/haddock.modules.analysis.ilrmsdmatrix.html#default-parameters) or retrieved by running
```bash
haddock3-cfg -m ilrmsdmatrix
```

Here an example configuration file snapshot using ILRMSD-based clustering after flexible refinement:

```toml
# ...
[flexref]
ambig_fname = ambiguous_restraints.tbl
[ilrmsdmatrix]
[clustrmsd]
clust_cutoff = 2.5
# ...
```

<hr>

## `[rmsdmatrix]` module

RMSD matrix module.

This module calculates of the RMSD matrix between all the models
generated in the previous step.

As all the pairwise RMSD calculations are independent, the module distributes
them over all the available cores in an optimal way.

**IMPORTANT**: the module assumes coherent numbering for all the receptor and ligand
chains, as no sequence alignment is performed. The user must ensure that the numbering
is coherent.

#### Notable parameters
- `allatoms`: whether to use all the atoms for the ILRMSD calculation (default: False)
- `resdic_` : an expandable parameter to specify which residues must be
 considered for the alignment and the RMSD calculation. If there are
 two proteins denoted by chain IDs A and B, then the user can operate
 such selection in the following way inside the configuration file

```toml
resdic_A = [1,2,3,4]
resdic_B = [2,3,4]
```

thus telling the module to consider residues from 1 to 4 of chain A and from 2
to 4 of chain B for the alignment and RMSD calculation.

More information about ``[rmsdmatrix]`` parameters can be accessed [here](https://bonvinlab.org/haddock3/modules/analysis/haddock.modules.analysis.rmsdmatrix.html#default-parameters) or retrieved by running
```bash
haddock3-cfg -m rmsdmatrix
```

Here an example configuration file snapshot using RMSD-based clustering after energy minimization refinement:

```toml
# ...
[emref]
ambig_fname = ambiguous_restraints.tbl
[rmsdmatrix]
resdic_A = [1,2,3,4]
resdic_B = [2,3,4]
[clustrmsd]
clust_cutoff = 3.0
# ...
```

<hr>

## `[seletop]` module

Select a number of models.

This module selects a number of models from the input models. By default, the
selection is based on the HADDOCK score of the models.

The number of models to be selected is defined by the parameter `select`.
In the standard HADDOCK protocol, this number is 200, but this number can be increased if more models should be refined (which is the recommended approach when limited experimental information is available).

```toml
# ...
[topoaa]
[rigidbody]
ambig_fname = "ambiguous_restraints.tbl"
[seletop]
select = 400
# ...
```


<hr>

## `[seletopclusts]` module

Select models from the top clusters.

This module selects a number of models from a number of clusters. The
selection is based on the score of the models within the clusters.

In the standard HADDOCK analysis, the top 4 models of the top 10 clusters are shown.
In case `[seletopclusts]` is run after a sampling module, we can keep a few models from all the clusters to have more diversity at the
refinement stage(s).

#### Notable parameters

The most important parameters for the ``[seletopclusts]`` module are:
- `top_cluster`: the number of top clusters to consider
- `top_models`: the number of top models to select from each cluster

Here an example selection of the top 10 models of the top 50 clusters after ``[rigidbody]`` docking:

```toml
# ...
[topoaa]
[rigidbody]
ambig_fname = ambiguous_restraints.tbl
[clustfcc]
[seletopclusts]
top_cluster = 50
top_models = 10
# ...
```
