### Outputs of your docking run

In case something went wrong with the docking (or simply if you do not want to wait for the results) you can find the following precalculated runs in the `runs` directory:
- `run1`: run created using the unbound antibody.
- `run1-af2`: run created using the Alphafold-multimer antibody (see BONUS 2).
- `run1-abb`: run created using the Immunebuilder antibody (see BONUS 2).
- `run1-ens`: run created using an ensemble of antibody models (see BONUS 3).


Once your run has completed - inspect the content of the resulting directory.
You will find the various steps (modules) of the defined workflow numbered sequentially starting at 0, e.g.:

{% highlight shell %}
> ls run1/
     00_topoaa/
     01_rigidbody/
     02_caprieval/
     03_seletop/
     04_flexref/
     05_caprieval/
     06_emref/
     07_caprieval/
     08_clustfcc/
     09_seletopclusts/
     10_caprieval/
     11_contactmap/
     analysis/
     data/
     log
     toppar/
     traceback/
{% endhighlight %}

In addition, there is a log file (text file) and four additional directories:

- the `analysis` directory contains various plots to visualize the results for each caprieval step and a general report (`report.html`) that provides all statistics with various plots. You can open this file in your preferred web browser
- the `data` directory contains the input data (PDB and restraint files) for the various modules
- the `toppar` directory contains the force field topology and parameter files (only present when running in self-contained mode)
- the `traceback` directory contains `traceback.tsv`, which links all models to see which model originates from which throughout all steps of the workflow.

You can find information about the duration of the run at the bottom of the log file. Each sampling/refinement/selection module will contain PDB files.

For example, the `09_seletopclusts` directory contains the selected models from each cluster. The clusters in that directory are numbered based
on their rank, i.e. `cluster_1` refers to the top-ranked cluster. Information about the origin of these files can be found in that directory in the `seletopclusts.txt` file.

The simplest way to extract ranking information and the corresponding HADDOCK scores is to look at the `10_caprieval` directories (which is why it is a good idea to have it as the final module, and possibly as intermediate steps). This directory will always contain a `capri_ss.tsv` single model statistics file, which contains the model names, rankings and statistics (score, iRMSD, Fnat, lRMSD, ilRMSD and dockq score). E.g.:

<pre style="background-color:#DAE4E7">
                  model  md5  caprieval_rank     score  irmsd   fnat  lrmsd  ilrmsd  dockq  cluster_id  cluster_ranking  model-cluster_ranking      air  angles  bonds       bsa   cdih   coup   dani  desolv   dihe      elec  improper   rdcs     rg    sym     total      vdw   vean   xpcs
../06_emref/emref_1.pdb    -               1  -142.417  1.193  0.862  2.242   2.261  0.803           -                -                      -   61.388   0.000  0.000  1884.490  0.000  0.000  0.000   6.496  0.000  -546.456     0.000  0.000  0.000  0.000  -530.829  -45.760  0.000  0.000
../06_emref/emref_2.pdb    -               2  -142.268  0.957  0.948  1.681   1.512  0.874           -                -                      -   78.754   0.000  0.000  1849.190  0.000  0.000  0.000   0.557  0.000  -497.733     0.000  0.000  0.000  0.000  -470.134  -51.154  0.000  0.000
../06_emref/emref_3.pdb    -               3  -142.107  1.040  0.931  1.985   1.675  0.852           -                -                      -   44.821   0.000  0.000  1886.680  0.000  0.000  0.000  -0.829  0.000  -491.378     0.000  0.000  0.000  0.000  -494.041  -47.484  0.000  0.000
../06_emref/emref_8.pdb    -               4  -133.948  1.063  0.931  2.135   1.719  0.846           -                -                      -  104.785   0.000  0.000  1746.970  0.000  0.000  0.000   3.183  0.000  -481.057     0.000  0.000  0.000  0.000  -427.670  -51.398  0.000  0.000
...
</pre>

If clustering was performed prior to calling the `caprieval` module, the `capri_ss.tsv` file will also contain information about to which cluster the model belongs to and its ranking within the cluster.

The relevant statistics are:

* **score**: *the HADDOCK score (arbitrary units)*
* **irmsd**: *the interface RMSD, calculated over the interfaces the molecules*
* **fnat**: *the fraction of native contacts*
* **lrmsd**: *the ligand RMSD, calculated on the ligand after fitting on the receptor (1st component)*
* **ilrmsd**: *the interface-ligand RMSD, calculated over the interface of the ligand after fitting on the interface of the receptor (more relevant for small ligands for example)*
* **dockq**: *the DockQ score, which is a combination of irmsd, lrmsd and fnat and provides a continuous scale between 1 (exactly equal to reference) and 0*

Various other terms are also reported including:

* **bsa**: *the buried surface area (in squared angstroms)*
* **elec**: *the intermolecular electrostatic energy*
* **vdw**: *the intermolecular van der Waals energy*
* **desolv**: *the desolvation energy*


The iRMSD, lRMSD and Fnat metrics are the ones used in the blind protein-protein prediction experiment [CAPRI](https://capri.ebi.ac.uk/){:target="_blank"} (Critical PRediction of Interactions).

In CAPRI the quality of a model is defined as (for protein-protein complexes):

* **acceptable model**: i-RMSD < 4Å or l-RMSD < 10Å and Fnat > 0.1 (0.23 < DOCKQ < 0.49)
* **medium quality model**: i-RMSD < 2Å or l-RMSD < 5Å and Fnat > 0.3 (0.49 < DOCKQ < 0.8)
* **high quality model**: i-RMSD < 1Å or l-RMSD < 1Å and Fnat > 0.5 (DOCKQ > 0.8)

<a class="prompt prompt-question">
Based on this CAPRI criterion, what is the quality of the best model listed above (emref_2.pdb)?
</a>

In case where the `caprieval` module is called after a clustering step, an additional `capri_clt.tsv` file will be present in the directory.
This file contains the cluster ranking and score statistics, averaged over the minimum number of models defined for clustering
(4 by default), with their corresponding standard deviations. E.g.:

<pre style="background-color:#DAE4E7">
cluster_rank  cluster_id  n  under_eval     score  score_std   irmsd  irmsd_std   fnat  fnat_std   lrmsd  lrmsd_std  dockq  dockq_std      air  air_std       bsa  bsa_std  desolv  desolv_std      elec  elec_std     total  total_std      vdw  vdw_std  caprieval_rank
           1           2  4           -  -140.185      3.603   1.063      0.085  0.918     0.033   2.011      0.211  0.844      0.026   72.437   22.198  1841.833   56.754   2.352       2.793  -504.156    25.137  -480.668     37.466  -48.949    2.407               1
           2           4  4           -  -104.627      9.604   4.985      0.167  0.159     0.022  10.983      0.735  0.206      0.017  140.887   17.004  1599.765  101.246   3.738       2.425  -267.555    26.639  -195.611     16.008  -68.943    5.880               2
           3           1  4           -   -90.803      5.270  10.263      0.837  0.086     0.017  19.261      1.307  0.091      0.012  139.801   40.076  1431.878   53.377   3.217       6.569  -335.970    38.177  -236.975     36.344  -40.806    2.883               3
           4           3  4           -   -90.321     12.145  14.645      0.132  0.099     0.007  23.305      0.134  0.076      0.003  154.818   25.452  1792.695   68.993   5.937       1.759  -308.110    28.984  -203.410     46.861  -50.118    6.689               4
...
</pre>


In this file you find the cluster rank, the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (n) in the cluster and the corresponding statistics (averages + standard deviations). The corresponding cluster PDB files will be found in the preceeding `09_seletopclusts` directory.

While these simple text files can be easily checked from the command line already, they might be cumbersome to read.
For that reason, we have developed a post-processing analysis that automatically generates html reports for all `caprieval` steps in the workflow.
These are located in the respective `analysis/XX_caprieval` directories and can be viewed using your favorite web browser.

