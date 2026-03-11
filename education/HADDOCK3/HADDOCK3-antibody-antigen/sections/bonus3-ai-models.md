## BONUS 3: How good are AI-based models of antibody for docking?

The release of [AlphaFold2 in late 2020](https://www.nature.com/articles/s41586-021-03819-2) has brought structure prediction methods to a new frontier, providing accurate models for the majority of known proteins. This revolution did not spare antibodies, with [Alphafold2-multimer](https://github.com/sokrypton/ColabFold){:target="_blank"} and other prediction methods (most notably [ABodyBuilder2](https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/abodybuilder2/){:target="_blank"}, from the ImmuneBuilder suite) performing nicely on the variable regions.

For a short introduction to AI and AlphaFold2 refer to this other tutorial [introduction](/education/molmod_online/alphafold/#introduction){:target="_blank"}.

For antibody modelings, CDR loops are clearly the most challenging region to be predicted given their high sequence variability and flexibility. 
Multiple Sequence Alignment (MSA)-derived information is also less useful in this context.

Here we will see whether the antibody models given by Alphafold2-multimer and ABodyBuilder2 can be used for generating reliable models of the antibody-antigen complex by docking, instead of the unbound form used in this tutorial, which, in many cases, will not be available.


### Analysing the AI models

We already ran the prediction with these two tools, and you can find the resulting models in the `pdbs` directory as:

- `4g6k_Abodybuilder2.pdb`
- `4g6k_AF2_multimer.pdb`


As was demonstrated in the tutorial, those files must be preprocessed for their use in HADDOCK. Docking-ready files are also provided in the `pdbs` directory:


- `4G6K_abb_clean.pdb`
- `4G6K_af2_clean.pdb`


Load the experimental unbound structure (`4G6K_clean.pdb`) and the two AI models in PyMOL to see whether they resemble the experimental unbound structure.

<a class="prompt prompt-info">
File menu -> Open -> select 4G6K_clean.pdb
</a>
<a class="prompt prompt-info">
File menu -> Open -> select 4G6K_abb_clean.pdb
</a>
<a class="prompt prompt-info">
File menu -> Open -> select 4G6K_af2_clean.pdb
</a>

Align the models to the experimental unbound structure

<a class="prompt prompt-pymol">
alignto 4G6K_clean
</a>

<a class="prompt prompt-question">
Which model is the closest to the unbound conformation?
</a>

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See the RMSD values</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
  4G6K_abb_clean       RMSD =    0.428 Å
  4G6K_af2_clean       RMSD =    0.765 Å
</pre>
 <br>
</details>
<br>

For docking purposes however, it might be more interesting to know how far are the models from the bound conformation, i.e. the conformation in the antibody-antigen complex.
The closer it is, the easier it should become to model the complex by docking.
To assess this, we can load the structure of the complex in PyMOL and align all other structures/models to it.

<a class="prompt prompt-info">
File menu -> Open -> select 4G6M_matched.pdb
</a>

<a class="prompt prompt-pymol">
color yellow, 4G6M_matched
</a>

Align now the models to the experimental bound structure

<a class="prompt prompt-pymol">
alignto 4G6M_matched and chain A
</a>

<a class="prompt prompt-question">
Which model is the closest to the bound conformation?
</a>

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See the RMSD values</i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
  4G6K_abb_clean       RMSD =    0.330 Å
  4G6K_af2_clean       RMSD =    0.675 Å
  4G6K_clean           RMSD =    0.393 Å
</pre>
 <br>
</details>
<br>


<hr>

### Docking performance using AI-based antibody models

We can repeat the docking as described above in our tutorial, but using this time either the ABodyBuilder2 or AlphaFold2 models as input.
For this, modify your haddock3 configuration file, changing the input PDB file of the first molecule (the antibody) using the respective HADDOCK-ready models provided in the `pdbs` directory.
You will also need to change the restraint filename used to keep the two parts of the antibody together (those files are present in the `restraints` directory.

Further, run haddock3 as described above.

Pre-calculated runs are provided in the `runs` directory. Analyse your run (or the pre-calculated ones) as described previously.

<a class="prompt prompt-question">
Which starting structure of the antibody gives the best results in terms of cluster quality and ranking?
</a>

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See the cluster statistics </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1/10_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  1  out of  3
Total number of medium or better clusters:      1  out of  3
Total number of high quality clusters:          0  out of  3

First acceptable cluster - rank:  1  i-RMSD:  1.049  Fnat:  0.879  DockQ:  0.815
First medium cluster     - rank:  1  i-RMSD:  1.049  Fnat:  0.879  DockQ:  0.815
Best cluster             - rank:  1  i-RMSD:  1.049  Fnat:  0.879  DockQ:  0.815

==============================================
== run1-abb/10_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  1  out of  5
Total number of medium or better clusters:      1  out of  5
Total number of high quality clusters:          0  out of  5

First acceptable cluster - rank:  1  i-RMSD:  1.134  Fnat:  0.841  DockQ:  0.796
First medium cluster     - rank:  1  i-RMSD:  1.134  Fnat:  0.841  DockQ:  0.796
Best cluster             - rank:  1  i-RMSD:  1.134  Fnat:  0.841  DockQ:  0.796

==============================================
== run1-af2/10_caprieval/capri_clt.tsv
==============================================
Total number of acceptable or better clusters:  2  out of  3
Total number of medium or better clusters:      0  out of  3
Total number of high quality clusters:          0  out of  3

First acceptable cluster - rank:  1  i-RMSD:  3.974  Fnat:  0.289  DockQ:  0.239
First medium cluster     - rank:   i-RMSD:   Fnat:   DockQ:
Best cluster             - rank:  3  i-RMSD:  3.305  Fnat:  0.302  DockQ:  0.290
</pre>
 <br>
</details>
<br>

<a class="prompt prompt-question">
Which starting structure of the antibody gives the best overall model (irrespective of the ranking)?
</a>

*__Hint__*: Use the `extract-capri-stats.sh` script to analyse the various runs and find the best (lowest i-RMSD or highest Dock-Q score) as the `emref` stage.

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <i>See single structure statistics </i> <i class="material-icons">expand_more</i>
 </summary>
<pre>
==============================================
== run1/07_caprieval/capri_ss.tsv
==============================================
...
First acceptable model - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
First medium model     - rank:  1  i-RMSD:  1.037  Fnat:  0.931  DockQ:  0.841
Best model             - rank:  11  i-RMSD:  0.841  Fnat:  0.897  DockQ:  0.875

==============================================
== run1-abb/07_caprieval/capri_ss.tsv
==============================================
...
First acceptable model - rank:  1  i-RMSD:  0.990  Fnat:  0.931  DockQ:  0.860
First medium model     - rank:  1  i-RMSD:  0.990  Fnat:  0.931  DockQ:  0.860
Best model             - rank:  1  i-RMSD:  0.990  Fnat:  0.931  DockQ:  0.860

==============================================
== run1-af2/07_caprieval/capri_ss.tsv
==============================================
...
First acceptable model - rank:  1  i-RMSD:  3.246  Fnat:  0.362  DockQ:  0.389
First medium model     - rank:   i-RMSD:   Fnat:   DockQ:
Best model             - rank:  21  i-RMSD:  2.474  Fnat:  0.362  DockQ:  0.468
</pre>
 <br>
</details>
<br>


<hr>

### Conclusions - AI-based docking

All three antibody structures used in input give good to reasonable results.
The unbound and the ABodyBuilder2 antibodies provided better results, with the best cluster showing models within 1 angstrom of interface-RMSD with respect to the unbound structure.
Using the Alphafold2 structure in this case is not the best option, as the input antibody is not perfectly modelled in its H3 loop.
