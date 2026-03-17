## Analysis of docking results

In case something went wrong with the docking (or simply if you do not want to wait for the results) you can find the following precalculated runs in the `runs` directory:
- `run1`: docking run created using the unbound antibody.
- `run1-af2`: docking run created using the Alphafold-multimer antibody (see  3).
- `run1-abb`: docking run created using the Immunebuilder antibody (see  3).
- `run1-ens`: docking run created using an ensemble of antibody models (see  4).
- `run-scoring`: scoring run created using various models obtained at the previous stages (see  6).


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
- the `data` directory contains the input data (PDB and restraint files) for the various modules, as well as an input workflow  (in `configurations` directory)
- the `toppar` directory contains the force field topology and parameter files (only present when running in self-contained mode)
- the `traceback` directory contains `traceback.tsv`, which links all models to see which model originates from which throughout all steps of the workflow.

You can find information about the duration of the run at the bottom of the log file. 

Each sampling/refinement/selection module will contain PDB files.
For example, the `09_seletopclusts` directory contains the selected models from each cluster. The clusters in that directory are numbered based
on their rank, i.e. `cluster_1` refers to the top-ranked cluster. Information about the origin of these files can be found in that directory in the `seletopclusts.txt` file.

The simplest way to extract ranking information and the corresponding HADDOCK scores is to look at the `XX_caprieval` directories (which is why it is a good idea to have it as the final module, and possibly as intermediate steps). This directory will always contain a `capri_ss.tsv` single model statistics file, which contains the model names, rankings and statistics (score, iRMSD, Fnat, lRMSD, ilRMSD and dockq score). E.g. for `10_caprieval`:

<pre style="background-color:#DAE4E7">
                                   model	md5	caprieval_rank	score	irmsd	fnat	lrmsd	ilrmsd	dockq	rmsd	cluster_id	cluster_ranking	model-cluster_ranking	air	angles	bonds	bsa	cdih	coup	dani	desolv	dihe	elec	improper	rdcs	rg	sym	total	vdw	vean	xpcs
../09_seletopclusts/cluster_1_model_1.pdb	-	1	-140.319	0.908	0.897	2.205	1.451	0.855	1.016	3	1	1	133.760	0.000	0.000	2010.880	0.000	0.000	0.000	7.010	0.000	-605.174	0.000	0.000	0.000	0.000	-511.084	-39.671	0.000	0.000
../09_seletopclusts/cluster_1_model_2.pdb	-	2	-137.507	0.879	0.948	1.951	1.354	0.881	0.989	3	1	2	189.059	0.000	0.000	1913.390	0.000	0.000	0.000	3.243	0.000	-521.143	0.000	0.000	0.000	0.000	-387.512	-55.428	0.000	0.000
../09_seletopclusts/cluster_1_model_3.pdb	-	3	-126.481	1.052	0.914	3.038	1.958	0.824	1.293	3	1	3	127.044	0.000	0.000	1816.780	0.000	0.000	0.000	-2.884	0.000	-426.677	0.000	0.000	0.000	0.000	-350.599	-50.966	0.000	0.000
../09_seletopclusts/cluster_1_model_4.pdb	-	4	-102.227	1.334	0.793	2.331	2.292	0.760	1.341	3	1	4	128.628	0.000	0.000	1837.970	0.000	0.000	0.000	12.344	0.000	-410.669	0.000	0.000	0.000	0.000	-327.341	-45.299	0.000	0.000
../09_seletopclusts/cluster_2_model_1.pdb	-	5	-102.077	14.789	0.103	23.359	22.787	0.077	14.405	2	2	1	163.844	0.000	0.000	1888.310	0.000	0.000	0.000	2.575	0.000	-348.025	0.000	0.000	0.000	0.000	-235.613	-51.431	0.000	0.000
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
Based on these CAPRI criteria, what is the quality of the best model listed above (_cluster_1_model_1.pdb_)?
</a>

In case where the `caprieval` module is called after a clustering step, an additional `capri_clt.tsv` file will be present in the directory.
This file contains the cluster ranking and score statistics, averaged over the minimum number of models defined for clustering
(4 by default), with their corresponding standard deviations. E.g.:

<pre style="background-color:#DAE4E7">
cluster_rank    cluster_id  n   under_eval  score   score_std  irmsd   irmsd_std   fnat   fnat_std   lrmsd   lrmsd_std  dockq   dockq_std  ilrmsd  ilrmsd_std  rmsd    rmsd_std    air air_std bsa bsa_std desolv  desolv_std  elec    elec_std    total   total_std   vdw vdw_std caprieval_rank
           1    3           4   -          -126.634    15.010   1.044  0.180      0.888   0.058       2.381  0.403      0.830   0.045       1.764  0.382        1.160  0.159   144.623 25.775  1894.755    76.054  4.928   5.550   -490.916    78.318  -394.134    70.848  -47.841 5.927   1
           2    2           4   -           -98.425     2.624  14.572  0.524      0.095   0.009      23.293  0.233      0.074   0.002      22.593  0.371       14.300  0.194   159.227 8.415   1781.358    114.002 2.706   2.898   -340.312    32.395  -230.077    26.771  -48.992 5.015   2
           3    1           4   -           -91.137     1.918  10.249  0.530      0.056   0.007      19.692  0.505      0.078   0.005      18.190  0.649       10.554  0.495   173.598 42.201  1441.505    77.296  4.873   4.329   -389.212    18.467  -251.141    40.747  -35.527 5.170   3
...
</pre>


In this file you find the cluster rank (which corresponds to the naming of the clusters in the previous `seletop` directory), the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (n) in the cluster and the corresponding statistics (averages + standard deviations). The corresponding cluster PDB files will be found in the preceeding `09_seletopclusts` directory.

While these simple text files can be easily checked from the command line already, they might be cumbersome to read.
For that reason, we have developed a post-processing analysis that automatically generates html reports for all `caprieval` steps in the workflow.
These are located in the respective `analysis/XX_caprieval` directories and can be viewed using your favorite web browser.
