## BONUS 3: Ensemble docking using a combination of exprimental and AI-predicted antibody structures


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

# Self contained rundir (to avoid problems with long filename paths)
self_contained = true

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
# Increased sampling so each conformation is sampled 50 times
sampling = 150

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

A pre-calculated run is provided in the `runs` directory as `run1-ens-clst`. 
Analyse your run (or the pre-calculated ones) as described previously.


<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See the cluster statistics </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== runs/run-ens-CDR-NMR-CSP/11_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  4  out of  11
Total number of medium or better clusters:      1  out of  11
Total number of high quality clusters:          0  out of  11
 
First acceptable cluster - rank:  1  i-RMSD:  1.188  Fnat:  0.862  DockQ:  0.795
First medium cluster     - rank:  1  i-RMSD:  1.188  Fnat:  0.862  DockQ:  0.795
Best cluster             - rank:  1  i-RMSD:  1.188  Fnat:  0.862  DockQ:  0.795
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
== runs/run-ens-CDR-NMR-CSP/04_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  25  out of  83
Total number of medium or better models:      10  out of  83
Total number of high quality models:          0  out of  83
 
First acceptable model - rank:  3  i-RMSD:  1.238  Fnat:  0.672  DockQ:  0.725
First medium model     - rank:  3  i-RMSD:  1.238  Fnat:  0.672  DockQ:  0.725
Best model             - rank:  6  i-RMSD:  1.074  Fnat:  0.707  DockQ:  0.731
==============================================
== runs/run-ens-CDR-NMR-CSP/06_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  27  out of  83
Total number of medium or better models:      10  out of  83
Total number of high quality models:           5  out of  83
 
First acceptable model - rank:  1  i-RMSD:  1.492  Fnat:  0.741  DockQ:  0.697
First medium model     - rank:  1  i-RMSD:  1.492  Fnat:  0.741  DockQ:  0.697
Best model             - rank:  4  i-RMSD:  0.857  Fnat:  0.897  DockQ:  0.872
==============================================
== runs/run-ens-CDR-NMR-CSP/08_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  26  out of  83
Total number of medium or better models:      10  out of  83
Total number of high quality models:           3  out of  83
 
First acceptable model - rank:  1  i-RMSD:  1.504  Fnat:  0.776  DockQ:  0.708
First medium model     - rank:  1  i-RMSD:  1.504  Fnat:  0.776  DockQ:  0.708
Best model             - rank:  4  i-RMSD:  0.902  Fnat:  0.914  DockQ:  0.871
</pre>
 <br>
</details>
<br>


We started from three different conformations of the antibody: 1) the unbound crystal structure, 2) the ABodyBuilder2 model and 3) the AlphaFold2 model.

<a class="prompt prompt-question">
Using the information in the _traceback_ directory, try to figure out which of the three starting antibody models makes it into the best cluster at the end of the workflow.
</a>
