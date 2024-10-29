# Clustering methods implemented in Haddock3

The clustering of conformations, complexes is a key step in most of the workflows, as it allows to observe convergence, redundancies, or even remove noise coming from singlotons.
Yet, two clustering methods are available in Haddock3:
- Clustering by **R**oot **M**ean **S**quared **D**eviation: [`[clustrmsd]`](#rmsd-clustering)
- Clustering by **F**raction of **C**omon **C**ontacts: [`[clustfcc]`](#fcc-clustering)


<hr>

## RMSD clustering

In Haddock3, RMSD clustering module `[clustrmsd]` must always be preceeded by the building of the RMSD matrix.
Indeed, the modules takes the resulting RMSD matrix as input to build the dendrograme and cluster it.
Two modules can compute the RMSD matrix:
- [`[rmsdmatrix]`](../modules/analysis.md#rmsdmatrix-module): Calculates of the RMSD matrix between all the models generated in the previous step.
- [`[ilrmsdmatrix]`](../modules/analysis.md#ilrmsdmatrix-module): Calculates the Interface Ligand Root Mean Square Deviation (ILRMSD) matrix.

Those two modules must be followed by the `[clustrmsd]` module, otherwise only the pair-wise RMSD matrix will be computed, and clustering not performed.

### [rmsdmatrix] module

The `[rmsdmatrix]` module allows you to define a subset of resiudes used to perform both the structural alignment and the RMSD computation.
For this, you need to specify a list of residues for each chain, using the parameter `resdic_*`, where `*` is the chainID.
As an example, to perform the selection of residues 12, 13, 14 and 15 from chain A and 1, 2, 3 from chain B, refine the following parameters:
```toml
[rmsdmatrix]
resdic_A = [12, 13, 14, 15]
resdic_B = [1, 2, 3]
```
This will result in the selection of those 7 residues to perform the structural alignment onto the reference and then compute the RMSD.

Full documentation about `[rmsdmatrix]` is accessible [here](../modules/analysis.md#rmsdmatrix-module).

### [ilrmsdmatrix] module

For the `[ilrmsdmatrix]` module, a different approach is taken.
Two parameters must be defined
- `receptor_chain`: defining the chainID of the receptor. By default "A".
- `ligand_chains`: a list of other chain IDs that should represent the "ligands". If not set, all the remaining chains will be considered as ligand.

During the computational workflow, first, all the residue-residue contacts between the receptor and ligand are selected.
This selection is then used to perform later structural alignment and RMSD computation.

Full documentation about `[ilrmsdmatrix]` is accessible [here](../modules/analysis.md#ilrmsdmatrix-module).

### [clustrmsd] module

Once the matrix has been computed, the clustering can be performed using the `[clustrmsd]` module.
The clustering is performed by first building a dendrograme, and then prunning the tree given two methods, accessible using the `criterion` parameter:
- `criterion = "maxclust"`: Prunning the tree to provide a defined number of clusters.
- `criterion = "distance"`: Prunning the tree so members of the same cluster will share a RMSD distance between themselves inferior to the one defined.



<hr>

## FCC clustering




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
| take blindly the first ranked model/cluster | consider/examine multiple models/clusters, especially if they overlap within standard deviations in their score|
| consider the size of the cluster as an indication of its quality | use the cluster score and not its size for selecting best solutions (of course it is nice if the largest cluster is also the best scoring one) |
| consider/look only at the best model of a cluster | within one cluster, do visualise and compare several models (e.g. the top4) to get an idea of the precision and make sure the clustering worked properly |
| take scores as proxies of binding affinity to compare different complexes | compare scores only within the same system/complex (i.e. to distinguish models for one docking run), or in the case of mutations |

<HR>

## [Advanced model refinement](/software/haddock2.4/tips/advanced_refinement/)

The HADDOCK2.4 server provides a dedicated web interface to run a [refinement on a molecular complex](https://wenmr.science.uu.nl/haddock2.4/refinement/1) (still experimental). As input, only a PDB file for each partner of the complex is needed. In case one wants to tune the default parameters, it is possible to run the refinement also locally or using the regular [submission interface](https://wenmr.science.uu.nl/haddock2.4/submit/1). Then following settings need to be adjusted: 

### Settings to run water refinement locally

<style>
table, th, td {
    padding: 5px;}
</style>

|<font size="4" color="#203A98">Parameter</font>|<font size="4" color="#203A98">run.cns name</font>| <font size="4" color="#203A98">default value</font>|<font size="4" color="#203A98">optimal value</font> |
|-|:-:|:-:|:-:| 
|**Center of mass restraints** | <code> cmrest</code>|false|**true**|  
|**Surface contact restraints** | <code>surfrest</code>|false|**true**|  
|**Number of structures for rigid body docking (it0)**|<code>structures_0</code>|1000|**same as itw structures**|
|**Number of structures for semi-flexible refinement (it1)**| <code>structures_1</code>|200| **same as itw structures**|
|**Sample 180 degrees rotated solutions during rigid body EM** |<code>rotate180_0</code>|true| **false**|
|**Refine with short molecular dynamics in explicit solvent?** |<code>solvshell</code>|false| **true**|
|**Perform cross-docking** | <code>crossdock</code>| true| **false**|
|**Multiply the number of calculated structures by all combination** | <code>ensemble_multiply<sup>*</sup></code>| false| **true**|
|**Randomize starting orientations** | <code>randorien</code>| true| **false**|
|**Perform initial rigid body minimisation** | <code>rigidmini</code>| true| **false**|
|**Allow translation in rigid body minimisation** | <code>rigidtrans</code>| true| **false**|
|**Number of MD steps for rigid body high temperature TAD**| <code>initiosteps</code> | 500| **0**|
|**Number of MD steps during first rigid body cooling stage**| <code>cool1_steps</code> | 500| **0**|
|**Number of MD steps during second cooling stage with flexible side-chains at interface**|<code>cool2_steps</code> | 500 |**0**|
|**Number of MD steps during third cooling stage with fully flexible interface**| <code>cool3_steps</code> |500 | **0**|

<sup>\*</sup> - only in *json* files, needs to be modified by hand in *run.cns*

 <HR>

Any more questions about analysis of the HADDOCK run? Have a look at our **[HADDOCK bioexcel forum](https://ask.bioexcel.eu/search?q=ana%20%23haddock)**  hosted by [<img width="70" src="/images/Bioexcel_logo.png">](https://bioexcel.eu). There is a very high chance that your problem has already been addressed. 
