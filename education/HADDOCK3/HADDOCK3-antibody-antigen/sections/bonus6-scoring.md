## BONUS 6: Running a scoring scenario

This section demonstrates the use of HADDOCK3 to score the various models obtained at the previous stages (ensemble docking and AlphaFold predictions) 
and observe if the HADDOCK scoring function is able to detect the quality of the models.

To this end the following workflow is defined:

1. Generate the topologies for the various models.
2. Energy Minimise all complexes.
3. Cluster the models using Fraction of Common Contacts:
  - set the parameter `min_population` to 1 so that all models, including singletons (models that do not cluster with any others), will be forwarded to the next steps.
  - set the parameter `plot_matrix` to true to generate a matrix of the clusters for a visual representation.
4. Comparison of the models with the reference complex `4G6M_matched.pdb` using CAPRI criteria.

For this, two ensembles must be scored and one structure will be used as a reference. You can find them in the `pdbs/` directory:
- `07_emref_and_top5af2_ensemble.pdb`: An ensemble of models obtained from the ensemble run, combined with top5 AlphaFold2 predictions.
- `af3server_15052024_top5ens.pdb`: An ensemble of top5 AlphaFold3 predictions.
- `4G6M_matched.pdb`: The reference structure for quality assessments.


{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen 
# ====================================================================
run_dir = "scoring-haddock3-alphafold2and3-ensemble"

molecules =  [
    "pdbs/haddock3-ens-emref-ensemble.pdb",
    "pdbs/af2-models.pdb",
    "pdbs/af3-models.pdb",
    ]

# ====================================================================
# Parameters for each stage are defined below
# ====================================================================

[topoaa]

[emscoring]

[clustfcc]
# Reduce the min_population to define a cluster to 1 so that models
# that do not cluster with any other will define singlotons
min_population = 1
# Generate a matrix of the clusters
plot_matrix = true

[caprieval]
reference_fname = "4G6M_matched.pdb"

# ====================================================================

{% endhighlight %}


A scoring scenario configuration file is provided in the `workflows/` directory as `scoring-antibody-antigen.cfg, precomputed results in `runs/run-scoring`.

You can again look at the `capri_ss.tsv` file in the `4_caprieval` directory. It contains the energy minimised statistics:

<pre>
              model md5 caprieval_rank   score      irmsd   fnat    lrmsd   ilrmsd  dockq   rmsd    cluster_id  cluster_ranking model-cluster_ranking   air angles  bonds   bsa cdih    coup    dani    desolv  dihe    elec    improper    rdcs    rg  sym total   vdw vean    xpcs
../1_emscoring/emscoring_82.pdb -   1   -157.149    0.910   0.897   2.201   1.456   0.855   1.016  3   1   1   0.000   0.000   0.000   2000.130    0.000  0.000   0.000   7.345   0.000   -599.183  0.000   0.000   0.000   0.000   -643.841        -44.658 0.000   0.000
../1_emscoring/emscoring_2.pdb  -   2   -156.452    0.880   0.948   1.949   1.355   0.881   0.989  3   1   2   0.000   0.000   0.000   1914.860    0.000  0.000   0.000   3.125   0.000   -504.372  0.000   0.000   0.000   0.000   -563.075        -58.703 0.000   0.000
../1_emscoring/emscoring_64.pdb -   3   -138.214    1.052   0.914   3.039   1.955   0.824   1.294  3   1   3   0.000   0.000   0.000   1784.350    0.000  0.000   0.000   -2.359  0.000   -424.542  0.000   0.000   0.000   0.000   -475.489        -50.947 0.000   0.000
../1_emscoring/emscoring_40.pdb -   4   -135.230    1.085   0.897   1.866   1.756   0.836   1.144  3   1   4   0.000   0.000   0.000   1875.210    0.000  0.000   0.000   3.490   0.000   -429.067  0.000   0.000   0.000   0.000   -481.973        -52.906 0.000   0.000
../1_emscoring/emscoring_37.pdb -   5   -134.569   13.624  0.069   22.589  21.764  0.068   13.881  5   2   1   0.000   0.000   0.000   1802.890    0.000  0.000   0.000   6.081   0.000   -426.815  0.000   0.000   0.000   0.000   -482.102        -55.287 0.000   0.000

...
</pre>

<a class="prompt prompt-question">
Did the HADDOCK scoring do a good job at putting the best models on top (consider for example the DockQ score)? 
</a>

The `emscoring` module renames all models, which makes it difficult to know what was the original model. 
You can however trace back a model to its original file by looking into the `traceback/traceback.tsv` file:

<pre>
00_topoaa                                               1_emscoring             1_emscoring_rank
emref_9_from_haddock3-ens-emref-ensemble_83_haddock.psf emscoring_82.pdb        1
emref_10_from_haddock3-ens-emref-ensemble_2_haddock.psf emscoring_2.pdb         2
emref_7_from_haddock3-ens-emref-ensemble_67_haddock.psf emscoring_64.pdb        3
emref_5_from_haddock3-ens-emref-ensemble_45_haddock.psf emscoring_40.pdb        4
...
</pre>

<a class="prompt prompt-question">
Try to locate the AlphaFold2 and AlphaFold3 models (their filenames start with _abag_test_ and _af3server_, respectively)
</a>

A simple way to extra this information is to use `grep`:

<a class="prompt prompt-cmd">
grep abag traceback.tsv
</a>

<details style="background-color:#DAE4E7">
  <summary style="font-weight: bold">
    <i>See the output of grep for the AlphaFold2 models</i>
  <br>
  </summary>
  <pre>
> grep abag traceback.tsv
abagtest_2d03e_unrelaxed_rank_001_alphafold2_multimer_v3_model_3_seed_000_from_af2-models_1_haddock.psf	emscoring_84.pdb	86
abagtest_2d03e_unrelaxed_rank_005_alphafold2_multimer_v3_model_2_seed_000_from_af2-models_5_haddock.psf	emscoring_88.pdb	90
abagtest_2d03e_unrelaxed_rank_004_alphafold2_multimer_v3_model_4_seed_000_from_af2-models_4_haddock.psf	emscoring_87.pdb	91
abagtest_2d03e_unrelaxed_rank_003_alphafold2_multimer_v3_model_1_seed_000_from_af2-models_3_haddock.psf	emscoring_86.pdb	92
abagtest_2d03e_unrelaxed_rank_002_alphafold2_multimer_v3_model_5_seed_000_from_af2-models_2_haddock.psf	emscoring_85.pdb	93
  </pre>
</details>
<br>


<a class="prompt prompt-cmd">
grep af3server traceback.tsv
</a>

<details style="background-color:#DAE4E7">
  <summary style="font-weight: bold">
    <i>See the output of grep for the AlphaFold3 models</i>
  <br>
  </summary>
  <pre>
> grep abag traceback.tsv
af3server_15052024_2_ready_from_af3-models_2_haddock.psf	emscoring_90.pdb	40
af3server_15052024_1_ready_from_af3-models_1_haddock.psf	emscoring_89.pdb	81
af3server_15052024_4_ready_from_af3-models_4_haddock.psf	emscoring_92.pdb	87
af3server_15052024_3_ready_from_af3-models_3_haddock.psf	emscoring_91.pdb	88
af3server_15052024_5_ready_from_af3-models_5_haddock.psf	emscoring_93.pdb	89
  </pre>
</details>
<br>

<a class="prompt prompt-question">
What are their ranks?
</a>

We have already seen in the previous section that none of the AlphaFold models were close to the real complex. 
This is however also the case for some of the HADDOCK models.
Still the AlpaFold models score very badly, toward the end of the ranked list of models.

<a class="prompt prompt-question">
Having found their ranks, can you figure out from the statistics in _capri_ss.tsv_ which component of the HADDOCK score causes in particular this bad scoring?
</a>


<details style="background-color:#DAE4E7">
  <summary style="font-weight: bold">
    <i>See the answer</i>
  <br>
  </summary>
  <p> The bottom eight models (the worst ranking ones) are all AlphaFold3/2 models. Looking at the componenents of the score 
  (some were left out in the table below for simplicity) one can see that it is mainly the van der Waals energy that causes the high scores, 
  which is indicative of clashes in the models.</p>
  <pre>
model               md5 caprieval_rank  score    irmsd   fnat    lrmsd   ilrmsd  dockq   rmsd    bsa        desolv    elec      vdw vean    xpcs
...
../1_emscoring/emscoring_84.pdb -   86  -67.914  11.123  0.000   22.413  18.626  0.048   12.213  3535.520   -67.537  -150.913    29.806 
../1_emscoring/emscoring_92.pdb -   87  -63.263  11.426  0.000   22.104  21.035  0.049   11.048  1383.920    -9.924   -88.656   -35.607
../1_emscoring/emscoring_91.pdb -   88  -50.990  13.665  0.000   23.793  22.150  0.042   13.796  1492.150    -8.962  -167.236    -8.581 
../1_emscoring/emscoring_93.pdb -   89  -46.871   6.644  0.000   10.617  11.333  0.146   6.455   1740.990    -8.906   -35.623   -30.841
../1_emscoring/emscoring_88.pdb -   90   48.283  12.919  0.000   20.484  19.885  0.053   14.706  3914.250   -68.786  -129.461   142.961
../1_emscoring/emscoring_87.pdb -   91  180.468  12.447  0.000   22.153  19.299  0.048   14.160  3639.430   -66.857  -240.130   295.351
../1_emscoring/emscoring_86.pdb -   92  240.307  12.572  0.000   21.662  19.799  0.049   14.187  3535.820   -69.380  -154.703   340.628
../1_emscoring/emscoring_85.pdb -   93  781.210  15.174  0.000   23.497  24.993  0.042   17.151  3278.340   -61.261   -86.026   859.677
  </pre>
</details>
<br>

<a class="prompt prompt-question">
Inspect more closely the reported scores above? Can you discover something peculiar with the buried surface area?
</a>

<a class="prompt prompt-question">
How can you explain that?
</a>

**_Hint 1_**: The HADDOCK score is calculated over all existing interfaces defined by different chainIDs.

**_Hint 2_**: Visualise two of the models with very different BSA values, color-coding the chains.
