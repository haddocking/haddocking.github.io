### Some single structure analysis


Going back to command line analysis, we are providing in the `scripts` directory a simple script that extracts some model statistics for acceptable or better models from the `caprieval` steps.
To use it, simply call the script with as argument the run directory you want to analyze, e.g.:

<a class="prompt prompt-cmd">
./scripts/extract-capri-stats.sh ./runs/run1
</a>

<details style="background-color:#DAE4E7">
<summary>
<i>View the output of the script</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== runs/run1/02_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  25  out of  100
Total number of medium or better models:      15  out of  100
Total number of high quality models:          1  out of  100

First acceptable model - rank:  1  i-RMSD:  1.196  Fnat:  0.672  DockQ:  0.741
First medium model     - rank:  1  i-RMSD:  1.196  Fnat:  0.672  DockQ:  0.741
Best model             - rank:  17  i-RMSD:  0.982  Fnat:  0.759  DockQ:  0.774
==============================================
== runs/run1/05_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  14  out of  40
Total number of medium or better models:      14  out of  40
Total number of high quality models:          5  out of  40

First acceptable model - rank:  1  i-RMSD:  0.992  Fnat:  0.897  DockQ:  0.834
First medium model     - rank:  1  i-RMSD:  0.992  Fnat:  0.897  DockQ:  0.834
Best model             - rank:  11  i-RMSD:  0.789  Fnat:  0.776  DockQ:  0.842
==============================================
== runs/run1/07_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  14  out of  40
Total number of medium or better models:      14  out of  40
Total number of high quality models:          3  out of  40

First acceptable model - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
First medium model     - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
Best model             - rank:  11  i-RMSD:  0.841  Fnat:  0.897  DockQ:  0.875
==============================================
== runs/run1/10_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  4  out of  12
Total number of medium or better models:      4  out of  12
Total number of high quality models:          1  out of  12

First acceptable model - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
First medium model     - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
Best model             - rank:  3  i-RMSD:  0.908  Fnat:  0.897  DockQ:  0.855
</pre>
</details>
<br>

_**Note**_ that this kind of analysis only makes sense when we know the reference complex and for benchmarking / performance analysis purposes.

<a class="prompt prompt-info">Look at the single structure statistics provided by the script</a>

<a class="prompt prompt-question">How does the quality of the best model changes after flexible refinement? Consider here the various metrics.</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
  In terms of iRMSD values, we only observe very small differences in the best model.
  The fraction of native contacts and the DockQ scores are however improving much more after flexible refinement but increases again slightly after final minimisation.
  All this will of course depend on how different are the bound and unbound conformations and the amount of data used to drive the docking process.
  In general, from our experience, the more and better data at hand, the larger the conformational changes that can be induced.
  </p>
</details>
<br>

<a class="prompt prompt-question">Is the best model always ranked first?</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>Answer</i> <i class="material-icons">expand_more</i>
  </summary>
  <p>
    This is not the case. The scoring function is not perfect, but does a reasonable job at ranking models of acceptable or better quality on top in this case.
  </p>
</details>
<br>

**_Note_**: A similar script to extract cluster statistics is available in the `scripts` directory as `extract-capri-stats-clt.sh`.
