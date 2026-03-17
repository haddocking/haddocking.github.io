### Identifying the epitope of the antigen

The article describing the crystal structure of the antibody-antigen complex we are modeling also reports experimental NMR chemical shift titration experiments 
to map the binding site of the antibody (gevokizumab) on Interleukin-1β.
The residues affected by binding are listed in Table 5 of [Blech et al. JMB 2013](https://dx.doi.org/10.1016/j.jmb.2012.09.021){:target="_blank"}:

<figure style="text-align: center;">
  <img width="60%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/images/Table5-Blech.png">
</figure>

The list of binding site (epitope) residues identified by NMR is:

<pre style="background-color:#DAE4E7">
72,73,74,75,81,83,84,89,90,92,94,96,97,98,115,116,117
</pre>

We will now visualize the epitope on Interleukin-1β.
To do this, start PyMOL and open the provided PDB file of the antigen from the PyMOL File menu.

<a class="prompt prompt-pymol">
File menu -> Open -> select 4I1B_clean.pdb
</a>

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select epitope, (resi 72+73+74+75+81+83+84+89+90+92+94+96+97+98+115+116+117)<br>
color red, epitope<br>
</a>

Inspect the surface.

<a class="prompt prompt-question">
Do the identified residues form a well-defined patch on the surface?
</a>

The answer to that question should be yes, but we can see some residues not colored that might also be involved in the binding - there are some white spots around/in the red surface.

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See surface view of the epitope identified by NMR</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="60%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/images/antigen-epitope.png">
  </figure>
  <br>
</details>

<br>

In HADDOCK, we are dealing with potentially incomplete binding sites by defining surface neighbors as `passive` residues.
These passive residues are added in the definition of the interface but do not incur any energetic penalty if they are not part of the binding site in the final models. 
In contrast, residues defined as active (typically the identified or predicted binding site residues) will incur an energetic penalty.
When using the HADDOCK2.x webserver, `passive` residues will be automatically defined.
Here, since we are using a local version, we need to define those manually.

This can easily be done using a haddock3 command line tool in the following way:

<a class="prompt prompt-cmd">
haddock3-restraints passive_from_active 4I1B_clean.pdb 72,73,74,75,81,83,84,89,90,92,94,96,97,98,115,116,117
</a>

The command prints a list of solvent accessible passive residues, which you should save to a file for further use.

We can visualize the epitope and its surface neighbors using PyMOL:

<a class="prompt prompt-pymol">
File menu -> Open -> select 4I1B_clean.pdb
</a>

<a class="prompt prompt-pymol">
color white, all<br>
show surface<br>
select epitope, (resi 72+73+74+75+81+83+84+89+90+92+94+96+97+98+115+116+117)<br>
color red, epitope<br>
select passive, (resi 3+24+46+47+48+50+66+76+77+79+80+82+86+87+88+91+93+95+118+119+120)<br>
color green, passive<br>
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See the epitope and passive residues</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="60%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/images/antigen-active-passive.png">
  </figure>
  <br>
</details>
<br>

The NMR-identified residues and their surface neighbors generated with the above command can be used to define ambiguous interactions restraints, 
either using the NMR identified residues as active in HADDOCK, or combining those with the surface neighbors. 

The difference between `active` and `passive` residues in HADDOCK is as follows:

*__Active residues__*: These residues are "forced" to be at the interface. If they are not part of the interface in the final models, an energetic penalty will be applied. The interface in this context is defined by the union of active and passive residues on the partner molecules.

*__Passive residues__*: These residues are expected to be at the interface. However, if they are not, no energetic penalty is applied.


In general, it is better to be too generous rather than too strict in the definition of passive residues.
An important aspect is to filter both the active (the residues identified from your mapping experiment) and passive residues by their solvent accessibility.
This is done automatically when using the `haddock3-restraints passive_from_active` command: residues with less that 15% relative solvent accessibility (same cutoff as the default in the HADDOCK server) are discared.
This is, however, not a hard limit, and you might consider including even more buried residues if some important chemical group seems solvent accessible from a visual inspection.
