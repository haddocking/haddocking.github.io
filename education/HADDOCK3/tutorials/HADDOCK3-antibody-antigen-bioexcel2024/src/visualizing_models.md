### Visualization of the models

To visualize the models from the top cluster of your favorite run, start PyMOL and load the cluster representatives you want to view, e.g. this could be the top model from cluster1 for run `run1-CDR-NMR-CSP`.
These can be found in the `runs/run1/09_seletopclusts/` directory.

<a class="prompt prompt-pymol">File menu -> Open -> select cluster_1_model_1.pdb</a>

*__Note__* that the PDB files are compressed (gzipped) by default at the end of a run. You can uncompress those with the `gunzip` command. PyMOL can directly read the gzipped files.

If you want to get an impression of how well-defined a cluster is, repeat this for the best N models you want to view (`cluster_1_model_X.pdb`).
Also load the reference structure from the `pdbs` directory, `4G6M-matched.pdb`.

Once all files have been loaded, type in the PyMOL command window:

<a class="prompt prompt-pymol">
show cartoon
</a>
<a class="prompt prompt-pymol">
util.cbc
</a>
<a class="prompt prompt-pymol">
color yellow, 4G6M_matched
</a>

Let us then superimpose all models onto the reference structure:

<a class="prompt prompt-pymol">
alignto 4G6M_matched
</a>

<a class="prompt prompt-question">
How close are the top4 models to the reference? Did HADDOCK do a good job at ranking the best in the top?
</a>

Let’s now check if the active residues which we have defined (the paratope and epitope) are actually part of the interface. In the PyMOL command window type:

<a class="prompt prompt-pymol">
select paratope, (resi 31+32+33+34+35+52+54+55+56+100+101+102+103+104+105+106+151+152+169+170+173+211+212+213+214+216 and chain A)
</a>
<a class="prompt prompt-pymol">
color red, paratope
</a>
<a class="prompt prompt-pymol">
select epitope, (resi 72+73+74+75+81+83+84+89+90+92+94+96+97+98+115+116+117 and chain B)
</a>
<a class="prompt prompt-pymol">
color orange, epitope
</a>

<a class="prompt prompt-question">
Are the residues of the paratope and NMR epitope at the interface?
</a>

**Note:** You can turn on and off a model by clicking on its name in the right panel of the PyMOL window.

<details style="background-color:#DAE4E7">
 <summary style="bold">
  <b><i>See the overlay of the top ranked model onto the reference structure</i></b> <i class="material-icons">expand_more</i>
 </summary>
 <p> Top-ranked model of the top cluster superimposed onto the reference crystal structure (in yellow)</p>
 <figure style="text-align: center">
   <img width="75%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen-bioexcel2024/results-best-model.png">
 </figure>
 <br>
</details>
