# Clustering methods implemented in Haddock3

Clustering of conformations and complexes is a key step in most workflows, as it allows us to observe convergence, redundancies, or even remove noise from singletons.
Yet, two clustering methods are available in Haddock3:
- Clustering by **R**oot **M**ean **S**quared **D**eviation: [`[clustrmsd]`](#rmsd-clustering)
- Clustering by **F**raction of **C**omon **C**ontacts: [`[clustfcc]`](#fcc-clustering)

Also, have a look at
- the [shared clustering parameters section](#shared-clustering-parameters)
- the [selecting cluster members section](#selecting-cluster-members)

<hr>

## RMSD clustering

In Haddock3, RMSD clustering module `[clustrmsd]` must always be preceded by the building of the RMSD matrix.
Indeed, the modules take the resulting RMSD matrix as input to build the dendrogram and cluster it.
Two modules can compute the RMSD matrix:
- [`[rmsdmatrix]`](../modules/analysis.md#rmsdmatrix-module): Calculates of the RMSD matrix between all the models generated in the previous step.
- [`[ilrmsdmatrix]`](../modules/analysis.md#ilrmsdmatrix-module): Calculates the Interface Ligand Root Mean Square Deviation (ILRMSD) matrix.

Those two modules must be followed by the `[clustrmsd]` module; otherwise, only the pair-wise RMSD matrix will be computed, and clustering will not be performed.

### [rmsdmatrix] module

The `[rmsdmatrix]` module allows you to define a subset of residues used to perform both the structural alignment and the RMSD computation.
For this, you need to specify a list of residues for each chain, using the parameter `resdic_*`, where `*` is the chainID.
As an example, to perform the selection of residues 12, 13, 14 and 15 from chain A and 1, 2, 3 from chain B, refine the following parameters:
```toml
[rmsdmatrix]
resdic_A = [12, 13, 14, 15]
resdic_B = [1, 2, 3]
```
This will result in the selection of those 7 residues to perform the structural alignment onto the reference and then compute the RMSD.

Full documentation about `[rmsdmatrix]` module is accessible [here](../modules/analysis.md#rmsdmatrix-module).

### [ilrmsdmatrix] module

For the `[ilrmsdmatrix]` module, a different approach is taken.
Two parameters must be defined
- `receptor_chain`: defining the chainID of the receptor. By default "A".
- `ligand_chains`: a list of other chain IDs that should represent the "ligands". If not set, all the remaining chains will be considered as ligand.

During the computational workflow, first, all the residue-residue contacts between the receptor and ligand are selected.
This selection is then used to perform later structural alignment and RMSD computation.

Full documentation about `[ilrmsdmatrix]` module is accessible [here](../modules/analysis.md#ilrmsdmatrix-module).

### [clustrmsd] module

Once the matrix has been computed, the clustering can be performed using the `[clustrmsd]` module.
The clustering is performed by first building a dendrogram, and then pruning the tree given two methods, accessible using the `criterion` parameter:
- `criterion = "maxclust"`: Pruning the tree to provide a defined number of clusters.
- `criterion = "distance"`: Pruning the tree so members of the same cluster will share an RMSD distance between themselves inferior to the one defined.

When setting the `criterion` to `"maxclust"`, the parameter `n_clusters` will be used to allow the definition of how many clusters you want.

While tuning the `criterion` to `"distance"`, the parameter `clust_cutoff` will be used to set the threshold where to prune the tree. By doing so, you do not yet know how many clusters you will get in the end.

Remember that as this relies on manipulating the dendrogram, the way it is built will influence the results.
You can tune the linkage using the `linkage` parameter.

Full documentation about `[clustrmsd]` module is accessible [here](../modules/analysis.md#clustrmsd-module).

<hr>


## FCC clustering

Clustering by Fraction of Comon Contacts does not rely on rotation and translations but simply on the analysis of contacts.
This is therefore much faster.

Full documentation about `[clustfcc]` module is accessible [here](../modules/analysis.md#clustfcc-module).

<hr>

## Shared clustering parameters

Various parameters are shared between `[clustrmsd]` and `[clustfcc]` modules:
- `min_population`: Threshold value employed to exclude clusters with less than this number of members. By default is 4.
- `plot_matrix`: Generates a plot displaying the matrix and the clustered members forwarded to the next step. By default is false.


<hr>

## Selecting cluster members

The module `[seletopcluts]` can be used to select clusters and their members.
Therefore, this module should be used after a clustering step (either `[clustrmsd]` or `[clustfcc]`).

This module holds three parameters:
- `top_cluster`: how many clusters should be selected
- `top_models`: how many models in each selected cluster must be forwarded to the next step
- `sortby`: How to sort clusters, by HADDOCK score or size

Full documentation about `[seletopcluts]` module is accessible [here](../modules/analysis.md#seletopclusts-module).

<hr>

## Dos and Don'ts

<style>
table, th, td {
  padding: 5px;
  table-layout: fixed ;
  width: 100% ;
}
</style>

| <font size="10" color="RED">Don't</font> | <font size="10" color="GREEN">Do instead</font> |
|:---:|:---:|
| set a too-loose or too-strict clustering cutoff | choose the right clustering cutoff for your system, help yourself by plotting the matrix |
| blindy accept the results of your clustering | if too many structures were left unclusters and you have few clusters, lower the clustering cutoff distance and/or the min_population parameters |
| take blindly the first ranked model/cluster | consider/examine multiple models/clusters, especially if they overlap within standard deviations in their score|
| consider the size of the cluster as an indication of its quality | use the cluster score and not its size for selecting best solutions (of course it is nice if the largest cluster is also the best scoring one) |
| consider/look only at the best model of a cluster | within one cluster, do visualize and compare several models (e.g. the top4) to get an idea of the precision and make sure the clustering worked properly |
| use RMSD matrix and clustering on >5000 models | use [clustfcc] instead |

<hr>


Any more questions about clustering in Haddock3?

Have a look at:
- [F.A.Q](../faq.md)
- [Ask for help / find support](../info.md)
