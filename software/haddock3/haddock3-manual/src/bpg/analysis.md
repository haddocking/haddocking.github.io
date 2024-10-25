## Comparing your docking results to a known reference structure

The comparison to a reference structure has been streamlined, and can now be made simply by using the `[caprieval]` module.
This module will compute CAPRI criteria, of all the generated structures with respect to a reference one, with ligand-RMSD (l-RMSD), interface-ligand-RMSD (il-RMSD), Fraction of Native contacts (Fnat), DockQ and global-RMSD (RMSD) metrics.
This is also extended to the cluster level, enabling to rank clusters.

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

**Notes**:
- that without specifying the `reference_fname` in the `[caprieval]` module, the best scoring complex will be used as reference.
- If a clustering step is placed before the `[caprieval]` module, the analysis will also be extended to the cluster level, hense providing a more robust analysis.

<hr>

## Analysis command line interace

The `haddock3-analyse` command line allows to generate interactive plots from the data obtained by a `[caprieval]` module directory.

Here is [the documentation of the `haddock3-analyse`](../clis.md#haddock3-analyse)


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
| take scores as proxies of binding affinity to compare different complexes | compare scores only within the same system/complex (i.e. to distinguish models for one docking run), or run <code>[prodigy]</code> module |



<hr>

Any more questions about analysis of the HADDOCK run?

Have a look at:
- [F.A.Q](../faq.md)
- [Ask for help / find support](../info.md)
