## BONUS 4: Ensemble docking using a combination of exprimental and AI-predicted antibody structures


Instead of running haddock3 using a specific input structure of the antibody, we can also use an ensemble of all available models.
Such an ensemble can be created from the individual models using `pdb_mkensemble` from PDB-tools:

<a class="prompt prompt-cmd">
pdb_mkensemble 4G6K_clean.pdb 4G6K_abb_clean.pdb 4G6K_af2_clean.pdb > 4G6K-ensemble.pdb
</a>

This ensemble file is provided in the `pdbs` directory.

Now we can make use of the flexibility of haddock3 in defining workflows to add a clustering step after the rigid body docking step in order to make sure that models originating from all models will ideally be selected for the refinement steps (provided they do cluster). This modified workflow looks like:


{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen 
# ====================================================================

# directory in which the scoring will be done
run_dir = "run-ens-CDR-NMR-CSP"

# compute mode
mode = "local"
ncores = 50

# Post-processing to generate statistics and plots
postprocess = true
clean = true

molecules =  [
    "pdbs/4G6K-ensemble.pdb",
    "pdbs/4I1B_clean.pdb"
    ]

# ====================================================================
# Parameters for each stage are defined below, prefer full paths
# ====================================================================
[topoaa]

[rigidbody]
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
# Reduced sampling (150 instead of the default of 1000)
# Increased to 150 so that each conformation is sampled 50 times
sampling = 150

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[clustfcc]
plot_matrix = true

[seletopclusts]
top_models = 10

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[flexref]
tolerance = 5
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[emref]
tolerance = 5
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[clustfcc]
plot_matrix = true

[seletopclusts]
top_models = 4

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[contactmap]

# ====================================================================

{% endhighlight %}


Our workflow consists of the following 14 modules:

0. **`topoaa`**: *Generates the topologies for the CNS engine and builds missing atoms*
1. **`rigidbody`**: *Performs Rigid body energy minimisation* - with increased sampling (150 models - 50 per input model)
2. **`caprieval`**: *Calculates CAPRI metrics*
3. **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
4. **`seletopclusts`**: *Selects the top models of all clusters* - In this case, we select max 10 models per cluster.
5. **`caprieval`**: *Calculates CAPRI metrics* of the selected clusters
6. **`flexref`**: *Performs Semi-flexible refinement of the interface (`it1` in haddock2.4)*
7. **`caprieval`**
8. **`emref`**: *Performs a final refinement by energy minimisation (`itw` EM only in haddock2.4)*
9. **`caprieval`**
10. **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
11. **`seletopclusts`**: *Selects the top models of all clusters*
12. **`caprieval`**
13. **`contactmap`**: *Contacts matrix and a chordchart of intermolecular contacts*

Compared to the original workflow described in this tutorial we have added clustering and cluster selections steps after the rigid body docking.

Run haddock3 with this configuration file as described above.

A pre-calculated run is provided in the `runs` directory as `run1-ens`. 
Analyse your run (or the pre-calculated ones) as described previously.


<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See the cluster statistics </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1-ens//12_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  3  out of  11
Total number of medium or better clusters:      1  out of  11
Total number of high quality clusters:          1  out of  11

First acceptable cluster - rank:  1  i-RMSD:  0.981  Fnat:  0.918  DockQ:  0.850
First medium cluster     - rank:  1  i-RMSD:  0.981  Fnat:  0.918  DockQ:  0.850
Best cluster             - rank:  1  i-RMSD:  0.981  Fnat:  0.918  DockQ:  0.850
</pre>
 <br>
</details>
<br>


<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See single structure statistics </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1-ens//02_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  27  out of  150
Total number of medium or better models:      11  out of  150
Total number of high quality models:          1  out of  150

First acceptable model - rank:  2  i-RMSD:  1.422  Fnat:  0.586  DockQ:  0.631
First medium model     - rank:  2  i-RMSD:  1.422  Fnat:  0.586  DockQ:  0.631
Best model             - rank:  26  i-RMSD:  0.982  Fnat:  0.759  DockQ:  0.774
==============================================
== run1-ens//05_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  16  out of  83
Total number of medium or better models:      10  out of  83
Total number of high quality models:          1  out of  83

First acceptable model - rank:  2  i-RMSD:  1.422  Fnat:  0.586  DockQ:  0.631
First medium model     - rank:  2  i-RMSD:  1.422  Fnat:  0.586  DockQ:  0.631
Best model             - rank:  24  i-RMSD:  0.982  Fnat:  0.759  DockQ:  0.774
==============================================
== run1-ens//07_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  17  out of  83
Total number of medium or better models:      9  out of  83
Total number of high quality models:          4  out of  83

First acceptable model - rank:  1  i-RMSD:  0.836  Fnat:  0.931  DockQ:  0.878
First medium model     - rank:  1  i-RMSD:  0.836  Fnat:  0.931  DockQ:  0.878
Best model             - rank:  7  i-RMSD:  0.829  Fnat:  0.845  DockQ:  0.854
==============================================
== run1-ens//09_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  16  out of  83
Total number of medium or better models:      9  out of  83
Total number of high quality models:          3  out of  83

First acceptable model - rank:  1  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
First medium model     - rank:  1  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
Best model             - rank:  12  i-RMSD:  0.851  Fnat:  0.845  DockQ:  0.851
==============================================
== run1-ens//12_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  10  out of  44
Total number of medium or better models:      4  out of  44
Total number of high quality models:          2  out of  44

First acceptable model - rank:  1  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
First medium model     - rank:  1  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
Best model             - rank:  2  i-RMSD:  0.879  Fnat:  0.948  DockQ:  0.881
</pre>
 <br>
</details>
<br>


We started from three different conformations of the antibody: 1) the unbound crystal structure, 2) the ABodyBuilder2 model and 3) the AlphaFold2 model.

<a class="prompt prompt-question">
Using the information in the _traceback_ directory, try to figure out which of the three starting antibody models makes it into the best cluster at the end of the workflow.
</a>
