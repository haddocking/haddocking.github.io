## BONUS 1: Dissecting the interface energetics: what is the impact of a single mutation? 

Mutations at the binding interfaces can have widely varying effects on binding affinity - some may be negligible, while others can significantly strengthen or weaken the interaction. Exploring these mutations helps identify critical amino acids for redesigning structurally characterized protein-protein interfaces, which paves the way for developing protein-based therapeutics to deal with a diverse range of diseases.
To pinpoint such amino acids positions, the residues across the protein interaction surfaces are either randomly or strategically mutated. Scanning mutations in this manner is experimentally costly. Therefore, computational methods have been developed to estimate the impact of an interfacial mutation on protein-protein interactions. 
These computational methods come in two main flavours. One involves rigorous free energy calculations, and, while highly accurate, these methods are computationally expensive. The other category includes faster, approximate approaches that predict changes in binding energy using statistical potentials, machine learning, empirical scoring functions etc. Though less precise, these faster methods are practical for large-scale screening and early-stage analysis. In this bonus exercise, we will take a look at two quick ways of estimating the effect of a single mutation in the interface.


### PROT-ON and haddock3-scoring to inspect a single mutation

PROT-ON (Structure-based detection of designer mutations in PROTein-protein interface mutatiONs) is a tool and [online server](http://proton.tools.ibg.edu.tr:8001/about){:target="_blank"} that scans all possible interfacial mutations and **predicts ΔΔG score** by using EvoEF1 (active in both on the web server and stand-alone versions) or FoldX (active only in the stand-alone version) with the aim of finding the most mutable positions. The original publication describing PROT-ON can be found [here](https://www.frontiersin.org/journals/molecular-biosciences/articles/10.3389/fmolb.2023.1063971/full){:target="_blank"}. 

Here we will use PROT-ON to analyse the interface of our antibody-antigen complex. For that, we will use the provided matched reference structure (`4G6M-matched.pdb`) in which both chains of the antibody have the same chainID (A), which allows us to analyse all interface residues of the antibody at once.

__Note:__ Pre-calculated PROT-ON results for this system can be accessed [here](http://proton.tools.ibg.edu.tr:8001/result/4G6M_matched_chain_A_EvoEF1){:target="_blank"}.

<a class="prompt prompt-info">
Connect to the PROT-ON server page (link above) and fill in the following fields:
</a>

<a class="prompt prompt-info">
Specify your run name* --> 4G6M_matched
</a>

<a class="prompt prompt-info">
Choose / Upload your protein complex* --> Select the provided _4G6M-matched.pdb_ file
</a>

<a class="prompt prompt-info">
Which dimer chains should be analyzed* --> Select chain A for the 1st molecule and B for the 2nd
</a>
<a class="prompt prompt-info">
Pick the monomer for mutational scanning* --> Select the first molecule - the antibody (toggle the switch ON under the chain A)
</a>

<a class="prompt prompt-info">
Click on the Submit button
</a>

Your run should complete in 5-10 minutes. Once finished, you will be presented with a result page summarising the most depleting (ones that decrease the binding affinity) and most enriching (ones that increase the binding affinity) mutations.

<a class="prompt prompt-question">
Which possible mutation would you propose to improve the binding affinity of the antibody?
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See answer</i></b> <i class="material-icons">expand_more</i>
  </summary>
The most enriching mutation is S150W with a -3.69 ΔΔG score.
</details>
<br>

<a class="prompt prompt-question">
Inspect the proposed amino acid in PyMol. Can you rationalise why it might increase the affinity?
</a>

With HADDOCK3, it is possible to take a step further. To perform the mutation, simply rename the desired residue and score such model - HADDOCK will take care of the topology regardless of the side chain differences and energy minimisation of the model. To do so, first either edit _4G6M-matched.pdb_ in your favourite text editor and save this new file as _4G6M_matched_S150W.pdb_, or use the command line: 
<a class="prompt prompt-cmd">
sed 's/SER\ A\ 150/TRP\ A\ 150/g' 4G6M_matched.pdb > 4G6M_matched_S150W.pdb
</a>

Next, score the mutant using the command-line tool `haddock3-score`. 
This tool performs a short workflow composed of the `topoaa` and `emscoring` modules. Use flag `--outputpdb` to save energy-minimized model:
<a class="prompt prompt-cmd">
haddock3-score 4G6M_matched_S150W.pdb \-\-outputpdb
</a>

<a class="prompt prompt-question">
Use _haddock3-score_ to calculate the score of the 4G6M-matched.pdb. Do you see a difference between wild-type and mutant scores? 
Might such single-residue mutation affect the binding affinity? 
</a>

<a class="prompt prompt-info">
Inspect the energy-minimized mutant model (4G6M_matched_S150W_hs.pdb) visually.
Can you rationalise why such a mutation might increase the affinity?
</a>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Zoom in on the mutated residue</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
   <img width="100%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/images/mutant-stacking.png">
   <center>
   <i>TRP150 is stacking with TYR24 </i>
   </center>
  </figure>
  <br>
</details>
<br>


### Alanine Scanning module 

Another way of exploring interface energetics is by using the `alascan` module of HADDOCK3. `alascan` stands for "Alanine Scanning module". 

This module is capable of mutating interface residues to Alanine and calculating the **Δ HADDOCK score** between the wild-type and mutant, thus providing a measure of the impact of each individual mutation. It is possible to scan all interface residues one by one or limit this scanning to a selected by user set of residues. By default, the mutation to Alanine is performed, as its side chain is just a methyl group, so side chain perturbations are minimal, as well as possible secondary structure changes. It is possible to perform the mutation to any other amino acid type - at your own risk, as such mutations may introduce structural uncertainty. 

**Important**: 1/ `alascan` calculates the difference between wild-type score vs mutant score, i.e. positive `Δscore` indicative of the enriched (stronger) binding and negative `Δscore` is indicative of the depleted (weaker) binding; 2/ Inside `alascan`, a short energy minimization of an input structure is performed, i.e. there's no need to include an additional refinement module prior to `alascan`. 

Here is an example of the workflow to scan interface energetics:
{% highlight toml %}
# ====================================================================
# Scanning interface residues with haddock3
# ====================================================================

# directory in which the scoring will be done
run_dir = "run-energetics-alascan"

# compute mode
mode = "local"
ncores = 50

# Post-processing to generate statistics and plots
postprocess = true
clean = true

molecules =  [
    "pdbs/4G6M_matched.pdb",
    ]

# ====================================================================
# Parameters for each stage are defined below
# ====================================================================
[topoaa]

[alascan]
# mutate each interface residue to Alanine 
scan_residue = 'ALA'
# generate plot of delta score and its components per each mutation
plot = true

# ====================================================================
{% endhighlight %}

A scoring scenario configuration file is provided in the `workflows/` directory as `interaction-energetics.cfg`, and precomputed results are in `runs/run-energetics-alascan`.
The output folder contains, among others, a directory titled `1_alascan` with a file `scan_4G6M_matched_haddock.tsv` that lists each mutation, corresponding score and individual terms:
<pre>
##########################################################
# `alascan` results for 4G6M_matched_haddock.pdb
#
# native score = -145.5891
#
# z_score is calculated with respect to the other residues
##########################################################
chain	res	ori_resname	end_resname	score	vdw	elec	desolv	bsa	delta_score	delta_vdw	delta_elec	delta_desolv	delta_bsa	z_score
A	212	LYS	ALA	-136.33	-66.16	-367.66	3.37	1660.53	-9.26	2.52	-75.12	3.24	37.57	-0.48
A	103	ASP	ALA	-129.64	-59.93	-365.23	3.34	1677.97	-15.95	-3.71	-77.56	3.27	20.13	-1.41
A	54	TRP	ALA	-138.18	-58.34	-435.53	7.27	1690.80	-7.41	-5.30	-7.26	-0.66	7.30	-0.22
A	32	SER	ALA	-143.66	-60.55	-447.37	6.36	1691.72	-1.93	-3.09	4.59	0.24	6.38	0.55
A	58	ASP	ALA	-121.65	-63.49	-306.77	3.20	1639.20	-23.94	-0.15	-136.01	3.41	58.90	-2.52
A	33	GLY	ALA	-148.50	-61.56	-473.22	7.71	1693.18	2.91	-2.08	30.43	-1.10	4.92	1.22
...
</pre>

<a class="prompt prompt-question">
Can you identify the most enriching/depleting mutation of each chain? 
Take a look at _scan_clt_-.tsv_ and open its visualisation _scan_clt_-.html_ in the web browser. 
</a>

You can use an additional script `/scripts/get-alascan-extrema.sh` to check your answer:
<a class="prompt prompt-cmd">
bash scripts/get-alascan-extrema.sh run-energetics-alascan/1_alascan/scan_4G6M_matched_haddock.tsv 
</a>

Mutation of the residue ASP58 turned out to be the most depleting within chain A. 
Let us visualise it in PyMol to analyse its contribution to the binding:
<a class="prompt prompt-pymol">
File menu -> Open -> 4G6M_matched.pdb 
</a>

Display ASP58 as sticks and colour it by atom:
<a class="prompt prompt-pymol">
util.cbc <br>
select asp58, (resi 58 and chain A) <br>
show sticks, asp58 <br>
util.cbao asp58
</a>

Now visualise its neighbouring residues:
<a class="prompt prompt-pymol">
select asp58_neighbour_atoms_4A, (resi 58 and chain A) around 4 and chain B <br>
select asp58_neighbour_residues, byres asp58_neighbour_atoms_4A
show sticks, asp58_neighbour_residues <br>
util.cbao asp58_neighbour_residues <br>
</a>


Let us display contacts using [show contacts plugin](https://pymolwiki.org/index.php/Show_contacts):
<figure style="text-align: center;">
  <img width="100%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/images/asp58_contacts.png">
  <center>
  <i>ASP58 makes h-bonds with two neighbouring residues</i>
  </center>
</figure>

We can see one hydrogen bond between ASP58 and LYS98, and two hydrogen bonds ASP58 and LYS94. 
Mutating ASP58 to ALA should result in the disappearance of those h-bonds, and the overall depletion of the binding. 
This is reflected by the high negative value (-136.01) of `delta_elec` in either of .tsv files. 

Let us test several mutations to confirm our hypothesis. 
Here is an example of the workflow to perform such mutations and save generated models:

{% highlight ini %}
# ====================================================================
# Mutating selected interface residue with haddock3
# ====================================================================

# directory in which the scoring will be done
run_dir = "run-energetics-mutations"

# compute mode
mode = "local"
ncores = 50

# Post-processing to generate statistics and plots
postprocess = true
clean = true

molecules =  ["pdbs/4G6M_matched.pdb"]

# ====================================================================
# Parameters for each stage are defined below
# ====================================================================
[topoaa]

[alascan]
# mutate residue 58 of chain A to Arginine 
scan_residue = "ARG"
resdic_A = [58]
# save energy-minimised mutant model 
output_mutants= true 

[alascan]
scan_residue = "GLY"
resdic_A = [58]
output_mutants= true 

[alascan]
scan_residue = "TRP"
resdic_A = [58]
output_mutants= true 

{% endhighlight %}

Configuration file for this scenario can be found in `workflows/single-residue-mutations.cfg`, precomputed results are in `run-residue-mutations`. The output folder contains, among others, an energy-minimised mutant model `1_alascan/4G6M_matched_haddock-A_D58R.pdb.gz`, and tables `.tsv` with energetics.
 
<a class="prompt prompt-question">
Take a look at the scores of the mutants. Which mutation depletes binding the most? 
</a>

<a class="prompt prompt-question">
Inspect the mutant vs wild-type complex. Can you see the difference at the interface level? 
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See the overlay of the mutant onto the wild-type structure </i></b> <i class="material-icons">expand_more</i>
  </summary>
  <figure style="text-align: center;">
    <img width="100%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/images/mutant-ref-overlay-alascan.png">
    <center>
    <i>wild-type residue ASP58 is displayed in pink, and mutant residue AGR58 is displayed in orange</i>
    </center>
  </figure>
  <br>
</details>
<br>


<a class="prompt prompt-question">
Compare values obtained with [alascan] to the corresponding values obtained with PROT-ON. Are they different? If yes, can you think of a reason why?
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See answer</i></b> <i class="material-icons">expand_more</i>
  </summary>
The values themselves are expected to differ, because [alascan] calculates ΔHADDOCK score, while PROT-ON predicts ΔΔG. 
Moreover, both tools are making predictions using different methods, so it is normal to have different results. 
However, if both tools consistently identify the same mutations as binding enriching or depleting - this may signal that selected residues indeed play a key role in binding affinity.
</details>
<br>

Now let us consider how sensitive this kind of analysis is to the quality of the docking model.
Instead of using the crystal structure, repeat this analysis using the best model of the top-ranked cluster or the best model with the lowest LRMSD value. 

<a class="prompt prompt-question">
Consider the most binding-enrishing/-depleting mutations predicted based on your favourite docking model. 
How different are those compared to the mutations, predicted based on the crystal structure?
</a>
