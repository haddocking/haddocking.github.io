## Comparing your docking results to a known reference structure

The comparison to a reference structure has been streamlined, and can now be made simply by using the `[caprieval]` module.
See here the [full documentation related to the `[caprieval]` module](../modules/analysis.md#caprieval-module).


Here is an schematic example on how to use the `[caprieval]` module:

```toml
# Some previous modules in the workflow
# ...

# Use caprieval to compare previously generated models to a reference
[caprieval]
reference_fname = "target_complex.pdb"

# Some more modules until the end of the workflow
# ...
```

**Note** that without specifying the `reference_fname` in the `[caprieval]` module, the best scoring complex will be used as reference.

<hr>

## Analysis manual


Analysis of docking results are described in the [HADDOCK2.4 manual](/software/haddock2.4/analysis/) and more about parameters in the *run.cns* file is written [here](/software/haddock2.4/run/#analysis-and-clustering).


<HR>

## Clustering and scoring

The HADDOCK scoring function is explained [here](/software/haddock2.4/scoring/).

The cluster-based HADDOCK analysis is explained [here](/software/haddock2.4/analysis/#cluster-based-analysis).

A short section about key default analysis parameters is provided [here](https://wenmr.science.uu.nl/haddock2.4/settings).


<HR>

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
