### Identifying the paratope of the antibody

Nowadays several computational tools can identify the paratope (the residues of the hypervariable loops involved in binding) from the provided antibody sequence.
In this tutorial, we are providing you with the corresponding list of residue obtained using [ProABC-2](https://github.com/haddocking/proabc-2){:target="_blank"}.
ProABC-2 uses a convolutional neural network to identify not only residues which are located in the paratope region 
but also the nature of interactions they are most likely involved in (hydrophobic or hydrophilic).
The work is described in [Ambrosetti, *et al* Bioinformatics, 2020](https://academic.oup.com/bioinformatics/article/36/20/5107/5873593){:target="_blank"}.

The corresponding paratope residues (those with either an overall probability >= 0.4 or a probability for hydrophobic or hydrophilic > 0.3) are:

<pre style="background-color:#DAE4E7">
31,32,33,34,35,52,54,55,56,100,101,102,103,104,105,106,151,152,169,170,173,211,212,213,214,216
</pre>

The numbering corresponds to the numbering of the `4G6K_clean.pdb` PDB file.

Let us visualize those onto the 3D structure.
For this start PyMOL and load `4G6K_clean.pdb`

<a class="prompt prompt-pymol">
File menu -> Open -> select 4G6K_clean.pdb
</a>

Alternatively, if PyMOL is accessible from the command line, simply type:

<a class="prompt prompt-cmd">
pymol 4G6K_clean.pdb
</a>

We will now highlight the predicted paratope residues in red. In PyMOL type the following commands:

<a class="prompt prompt-pymol">
color white, all<br>
select paratope, (resi 31+32+33+34+35+52+54+55+56+100+101+102+103+104+105+106+151+152+169+170+173+211+212+213+214+216)<br>
color red, paratope<br>
</a>

<a class="prompt prompt-question">
Can you identify the H3 loop? H stands for heavy chain (the first domain in our case with lower residue numbering). H3 is typically the longest loop.
</a>

Let us now switch to a surface representation to inspect the predicted binding site.

<a class="prompt prompt-pymol">
show surface<br>
</a>

Inspect the surface.

<a class="prompt prompt-question">
Do the identified paratope residues form a well-defined patch on the surface?
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See surface view of the paratope</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="60%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/images/antibody-paratope.png">
  </figure>
  <br>
</details>
