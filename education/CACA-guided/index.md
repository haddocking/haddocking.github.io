---
layout: page
title: "HADDOCK tutorial for the use of template-derived pairwise distance restraints to guide docking"
excerpt: "A tutorial on the use of pairwise distance restraints in HADDOCK."
tags: [templates, CA-CA, pairwise distance restraints, PS-HomPPI, PyMol, HADDOCK, Visualisation]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}



<hr>
## Introduction
Although many advanced and sophisticated ab initio approaches for modeling protein-protein complexes have been proposed 
in past decades, template-based modeling remains the most accurate and widely used approach, given a reliable template 
is available. This tutorial will demonstrate the use of HADDOCK for modelling the 3D structure of a protein-protein complex 
from pairwise interfacial residue distances derived from multiple structural templates. The case we will be investigating is the 
complex between bonvine chymotrypsinogen\*A and a recombinant variant of human pancreatic secretory trypsin inhibitor (PDB ID: 
1ACB). This is one of the cases in [Docking Benchmark 5.0 (BM5)](https://zlab.umassmed.edu/benchmark/). This case is classified as
 a difficult case by BM5, due to its large conformational changes upon binding: RMSD of CA atoms of interface residues calculated after finding the best superposition of bound and unbound interfaces is 2.26 Å, and change in accessible surface area upon complex formation is 1544 Å<sup>2</sup>. 

We will use the following web servers:
* [PS-HomPPI v2.0 webserver](http://ailab1.ist.psu.edu/PSHOMPPIv2.0/): A partner-specific homology based protein-protein interface predictor. We use PS-HomPPI to search structural templates from the PDB databank, cluster them and calculate one set of distance restraints from the interfaces of each template cluster.
* [HADDOCK2.2 webserver](http://haddock.science.uu.nl/services/HADDOCK2.2): to model 3D structures of the query complex using the distance restraints derived by PS-HomPPI v2.0 to guide docking. 

References:

* Li C Xue, João P G L M Rodrigues, Drena Dobbs, Vasant Honavar, Alexandre M J J Bonvin. [Template-based protein–protein docking exploiting pairwise interfacial residue restraints.](https://academic.oup.com/bib/article/18/3/458/2562753) _Briefings in bioinformatics_ 18.3 (2017): 458-466

* S.J. de Vries, M. van Dijk and A.M.J.J. Bonvin.
[The HADDOCK web server for data-driven biomolecular docking.](http://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html)
_Nature Protocols_, *5*, 883-897 (2010).  Download the final author version <a href="http://igitur-archive.library.uu.nl/chem/2011-0314-200252/UUindex.html">here</a>.

_Note: To follow this tutorial, very basic understandings of linux commands and bash scripting are expected._

Throughout the tutorial, colored text will be used to refer to questions or 
instructions, and/or PyMOL commands.

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>


<hr>
## Setup/Requirements

In order to follow this tutorial you only need a **web browser**, a **text editor**, and [**PyMOL**][link-pymol]{:target="\_blank"} 
(freely available for most operating systems) on your computer in order to visualize the input and output data.  


<hr>
## HADDOCK general concepts

HADDOCK (see [http://www.bonvinlab.org/software/haddock2.2/haddock.html](http://www.bonvinlab.org/software/haddock2.2/haddock.html)) 
is a collection of python scripts derived from ARIA ([http://aria.pasteur.fr](http://aria.pasteur.fr)) that harness the 
power of CNS (Crystallography and NMR System – [http://cns-online.org](http://cns-online.org)) for structure 
calculation of molecular complexes. What distinguishes HADDOCK from other docking software is its ability, inherited 
from CNS, to incorporate experimental data as restraints and use these to guide the docking process alongside 
traditional energetics and shape complementarity. Moreover, the intimate coupling with CNS endows HADDOCK with the 
ability to actually produce models of sufficient quality to be archived in the Protein Data Bank. 

A central aspect to HADDOCK is the definition of Ambiguous Interaction Restraints or AIRs. These allow the translation 
of raw data such as NMR chemical shift perturbation or mutagenesis experiments into distance restraints that are 
incorporated in the energy function used in the calculations. AIRs are defined through a list of residues that fall 
under two categories: active and passive. Generally, active residues are those of central importance for the 
interaction, such as residues whose knockouts abolish the interaction or those where the chemical shift perturbation is 
higher. Throughout the simulation, these active residues are restrained to be part of the interface, if possible, 
otherwise incurring in a scoring penalty. Passive residues are those that contribute for the interaction, but are 
deemed of less importance. If such a residue does not belong in the interface there is no scoring penalty. Hence, a 
careful selection of which residues are active and which are passive is critical for the success of the docking. 

The docking protocol of HADDOCK was designed so that the molecules experience varying degrees of flexibility and 
different chemical environments, and it can be divided in three different stages, each with a defined goal and 
characteristics:

* **1. Randomization of orientations and rigid-body minimization (it0)** <BR>
In this initial stage, the interacting partners are treated as rigid bodies, meaning that all geometrical parameters 
such as bonds lengths, bond angles, and dihedral angles are frozen. The partners are separated in space and rotated 
randomly about their centers of mass. This is followed by a rigid body energy minimization step, where the partners are 
allowed to rotate and translate to optimize the interaction.
The role of AIRs in this stage is of particular importance. Since they are included in the energy function being 
minimized, the resulting complexes will be biased towards them. For example, defining a very strict set of AIRs leads 
to a very narrow sampling of the conformational space, meaning that the generated poses will be very similar. 
Conversely, very sparse restraints (e.g. the entire surface of a partner) will result in very different solutions, 
displaying greater variability in the region of binding.

* **2. Semi-flexible simulated annealing in torsion angle space (it1)** <BR>
The second stage of the docking protocol introduces flexibility to the interacting partners through a three-step 
molecular dynamics-based refinement in order to optimize interface packing. It is worth noting that flexibility in 
torsion angle space means that bond lengths and angles are still frozen. The interacting partners are first kept rigid 
and only their orientations are optimized. Flexibility is then introduced in the interface, which is automatically 
defined based on an analysis of intermolecular contacts within a 5Å cut-off. This allows different binding poses coming 
from it0 to have different flexible regions defined. Residues belonging to this interface region are then allowed to 
move their side-chains in a second refinement step. Finally, both backbone and side-chains of the flexible interface 
are granted freedom.
The AIRs again play an important role at this stage since they might drive conformational changes.

* **3. Refinement in Cartesian space with explicit solvent (water)** <BR>
The final stage of the docking protocol immerses the complex in a solvent shell so as to improve the energetics of the 
interaction. HADDOCK currently supports water (TIP3P model) and DMSO environments. The latter can be used as a membrane 
mimic. In this short explicit solvent refinement the models are subjected to a short molecular dynamics simulation at 
300K, with position restraints on the non-interface heavy atoms. These restraints are later relaxed to allow all side 
chains to be optimized.

The performance of this protocol of course depends on the number of models generated at each step. Few models are less 
probable to capture the correct binding pose, while an exaggerated number will become computationally unreasonable. The 
standard HADDOCK protocol generates 1000 models in the rigid body minimization stage, and then refines the best 200 – 
regarding the energy function - in both it1 and water. Note, however, that while 1000 models are generated by default 
in it0, they are the result of five minimization trials and for each of these the 180º symmetrical solution is also 
sampled. Effectively, the 1000 models written to disk are thus the results of the sampling of 10.000 docking solutions.

The final models are automatically clustered based on a specific similarity measure - either the *positional interface 
ligand RMSD* (iL-RMSD) that captures conformational changes about the interface by fitting on the interface of the 
receptor (the first molecule) and calculating the RMSDs on the interface of the smaller partner, or the *fraction of 
common contacts* (current default) that measures the similarity of the intermolecular contacts. For RMSD clustering, 
the interface used in the calculation is automatically defined based on an analysis of all contacts made in all models. 

<hr>
## Data for this tutorial 
Data for this tutorial can be downloaded from [here](/education/CACA-guided/1ACB.tar.gz). It contains INPUT data to PS-HomPPI and HADDOCK, pre-calculated PS-HomPPI and HADDOCK outputs, and scripts for the evaluation of 3D HADDOCK models. 

1.  INPUT data to PS-HomPPI v2.0 (under `1ACB/PSHomPPI_results/input` of the data you just downloaded):
    *  The full sequences of the two individual proteins (`query.fasta.txt`)
    *  The zipped file of unbound structures of the two individual proteins (`query_pdbFLs.tar.gz`)
    *  The deletion file, which allows users to exclude some specific structural templates (`delete.lst`)

2.  INPUT data to HADDOCK (under `1ACB/HADDOCK_results/input`):
    *  Distance restraints (`xxx.tbl` files. They are generated by PS-HomPPI). `xxx.tbl` will be used as input of HADDOCK to guide docking. 
    *   The unbound structures of the two individual proteins (`A.pdb`, `B.pdb`)

3.  OUTPUT data from PS-HomPPI and HADDOCK (under `1ACB/PSHomPPI_results/output` and `1ACB/HADDOCK_results/output`)
    *   Predicted pairwise interfacial residues (CA-CA distances) by PS-HomPPI
    *   HADDOCK docked models

4.  Data for EVALUTIONS (under `1ACB/evaluation`):
    *  Target structure (`1ACB_target.pdb`). 

_Note: For analysis simplicity, the unbound and bound structures are matched, i.e., sharing the same chain IDs and the same residue numbers._

Let’s download [the data](/education/CACA-guided/1ACB.tar.gz) and unzip it. 

<a class="prompt prompt-cmd">
tar -xzvf 1ACB.tar.gz
</a>

First, let’s define a variable in our bash environment pointing to the starting directory of the unzipped file so that we can easily run our commands later:

<pre>
<a class="prompt prompt-cmd"># export dataDIR=the_path_to_the_downloaded_data. Here is an example:
export dataDIR='/home/users/CACA_tutorial'
</a>
</pre>


<hr>
## Derive CA-CA (alpha carbon-alpha carbon) distance restraints from structural templates


Let’s use PS-HomPPI v2.0 to 1) search for structural templates, 2) cluster them, and 3) derive interfacial CA-CA distance restraints from each cluster of templates. 

We input the sequences of the two proteins to PS-HomPPI v2.0, and upload the unbound structures of the individual proteins to PS-HomPPI, too. The structures of the individual proteins are optional but **recommended**. It helps PS-HomPPI 1) to better align the template structures to the query structures, hence more accurate CA-CA distance restraints, and 2) to map the CA-CA distance restraints to the residue numbering of the query proteins. In other words, if the query protein structures are not provided to PS-HomPPI, the output CA-CA distance restraints need to be renumbered according to the query PDB files in order to be used by HADDOCK in the next step. The “CA-CA (Alpha carbon-Alpha carbon) distance Threshold” is set to **15 Å**. 


To objectively evaluate the performance of PS-HomPPI, let’s also create a deletion file (`delete.lst`), in which we specify that we want to exclude our target 1ACB from being used by PS-HomPPI when making interface predictions. You can use your favorite text editor to create `delete.lst`. The content should look like this:

<pre style="background-color:#DAE4E7">
A:B=>1acb&ast;
</pre>

For more details of the format for the deletion file, see [the overview page of the PS-HomPPI 2.0 web server](http://ailab1.ist.psu.edu/PSHOMPPIv2.0/overview.html).

PS-HomPPI v2.0 is powered by the [HHpred suite](https://github.com/soedinglab/hh-suite/tree/master/scripts/hhpred) to search for homologs. Here are the default HHpred parameters used by PS-HomPPI v2.0:

<figure align="center">
<img src="/education/CACA-guided/Fig/PSHomPPI-param.png">
</figure>

Once finished, PS-HomPPI will send a result email to your email address. It typically takes PS-HomPPI v2.0 about 5-10 minutes for one pair of query proteins. 

<figure align="center">
<img src="/education/CACA-guided/Fig/PSHomPPI_result_page.png">
<p> Example of PS-HomPPI result email</p>
</figure>

From links provided in the email, you can download the predicted CA-CA distances for our query proteins A and B (the `cluster1_Ca_Ca_distance.txt` file. You can also find this file in the data you just downloaded under `1ACB/PSHomPPI_results/output/Ca_Ca_distances/A:B`):

<pre style="background-color:#DAE4E7">
 Mode = SafeMode
 chnID_Qry1 aa_Qry1 chnID_Qry2 aa_Qry2 mean min max
 A 40 B 51 14.34 14.12 14.83
 A 40 B 45 12.47 12.26 12.69
 A 40 B 49 9.88 9.38 10.57
 A 40 B 70 11.72 11.24 12.14
 </pre>

PS-HomPPI v2.0 reports 4 types of prediction confidence based on the sequence similarity between the query proteins and the templates: Safe zone, Twilight zone 1, Twilight zone 2 and Dark zone, ranging from the highest to the lowest confidence levels.  For the case in this tutorial, the interface prediction confidence from PS-HomPPI v2.0 is Safe Mode, which indicates the structural templates are quite reliable. This file describes the predicted pairwise CA-CA distances for the predicted interface residues of the query protein pairs. PS-HomPPI v2.0 typically provides multiple CA-CA distance files, one file for one cluster of templates. For this tutorial, only one cluster of templates is identified by PS-HomPPI, hence only one CA-CA distance file: `cluster1_Ca_Ca_distance.txt`.

In addition to this, PS-HomPPI v2.0 also provides us with distance-restraint files that can be directly used by HADDOCK (the `cluster1_restraints.tbl` file under the same folder):

<figure align="center">
<img src="/education/CACA-guided/Fig/CA-CA-tbl.png">
</figure>

Distance restraints are defined as:

<pre style="background-color:#DAE4E7">
    assign (selection1) (selection2) distance, lower-bound correction, upper-bound correction
</pre>

The lower limit for the distance is calculated as: distance minus lower-bound correction, and the upper limit as: distance plus upper-bound correction. 

Here would be an example of a distance restraint between the alpha carbons (CAs) of residues 128 and 21 in chains A and B with an allowed distance range between 13.263 (= 13.999-0.736) and 14.708 (= 13.999+0.709) Å:

<pre style="background-color:#DAE4E7">
assign (name ca and segid A and resi 128) (name ca and segid B and resi 21) 13.999 0.736 0.709 
</pre>

<a class="prompt prompt-question">
Can you write a new distance restraint for the CA atom of residue 34 in chain A and the CA atom of residue 100 in chain B so that the average distance is 8 Å, and the minimum distance is 6 Å and the maximum distance is 11 Å?
</a>

<details style="background-color:#DAE4E7">
<summary>See solution:
</summary>
<pre style="background-color:#DAE4E7">
    assign (name ca and segid A and resi 34) (name ca and segid B and resi 100) 8 2 3
</pre>
</details>
<p></p>
From `1ACB/PSHomPPI_results/output/A:B/templates_used_in_prediction.lst` (you can use your favoriate text editor, such as vim, TextEdit, Word, to open this file), we can see the templates used by PS-HomPPI when making interface predictions:

<pre style="background-color:#DAE4E7">
#Template_ID    predicted_CC
4b2aA,396:4b2aB,7   0.720
4b2aC,396:4b2aD,7   0.720
4h4fA,442:4h4fB,2   0.710
3rdzB,392:3rdzD,58  0.710
3rdzA,392:3rdzC,58  0.710
</pre>

The column of “Template\_ID” are the PDB IDs and chain IDs of the templates. The integers after the commas are just unique identifiers for the alignments between the query and a template, and can be ignored. The column of  “predicted\_CC” is the prediction confidence of PS-HomPPI v2.0. It ranges from 0 to 1, where 0 is the lowest confidence and 1 the highest confidence.

<hr>
## Visualize CA-CA distance restraints on structural templates

Before we use the CA-CA distances predicted by PS-HomPPI v2.0 to guide docking, let’s visually check these CA-CA distances on structural templates (many times visual check can easily identify wrong CA-CA restraints, if there is any). We are going to use `xxx.pml` files generated by PS-HomPPI to do that. `xxx.pml` files are PyMol scripts and will add dashes in PyMol between predicted interfacial residue pairs. `xxx.pml` files can be opened in any text editor and can be run directly in PyMol.

The residue numbers in the CA-CA distance restraint files (`clusterXX_Ca_Ca_distance.txt` and the corresponding `xxx.tbl` and `xxx.pml` files) are the same as those in the query PDB files (if they are uploaded by the users to PS-HomPPI) or the same as the numbering in the query sequences (if query PDB files are not provided by the users to PS-HomPPI). In this tutorial, we uploaded the query PDB files, so the residue numbering of the distance restraints is the same as the query PDB files. This makes the visualization in PyMol straight-forward. 

To visualize the CA-CA distances, let’s use the superimposed models generated by superimposing the individual query structures to the template structures. These superimposed models are automatically generated by PS-HomPPI v2.0. They are under `1ACB/PSHomPPI_results/output/A:B/superimposed_models/supUnbound2TemplatePDB/final/cluster1/finalSup.xxx.pdb` (one cluster, one pml file). 

Let’s first check how many templates PS-HomPPI used when making interface predictions.

<pre><a class="prompt prompt-cmd">cd $dataDIR/1ACB/PSHomPPI_results/output/A:B/superimposed_models/supUnbound2TemplatePDB/final/template_pdbs
ls &ast;pdb | wc -l

</a></pre>

We can see that PS-HomPPI used 5 dimer templates (from 3 unique PDB entries: 4b2a, 4h4f, and 3rdz) when making interface predictions. They are:

<pre style="background-color:#DAE4E7">
4b2aA_4b2aB
4b2aC_4b2aD
4h4fA_4h4fB
3rdzB_3rdzD
3rdzA_3rdzC
</pre>

Now, let’s visually check the predicted CA-CA restraints on the superimposed models:
<pre><a class="prompt prompt-cmd"># enter the folder where the superimposed models are stored
cd $dataDIR/1ACB/PSHomPPI_results/output/A:B/superimposed_models/supUnbound2TemplatePDB/final/cluster1
# open the superimposed models in PyMol
$path_to_pymol/pymol finalSup&ast;.pdb  
</a></pre>

In Pymol, align all superimposed models. Type the following command in the Pymol console. 
<pre><a class="prompt prompt-pymol">PyMOL>alignto finalSup.3rdzA_3rdzC.template5, 
PyMOL>zoom
PyMOL>util.cbc
</a></pre>

At this point we can see that the superimposed models in cluster 1 have similar structures, as we expected. 

<figure align="center">
<img src="/education/CACA-guided/Fig/superim_models.png">
<p>Models generated by superimposition</p>
</figure>

Now let’s show the CA-CA distance restraints on these models.
<pre><a class="prompt prompt-pymol">PyMOL>@final_caca.pml
PyMOL>hide labels
</a></pre>

We can see that the CA-CA distance restraints (yellow dashes in Figure below) are mostly at the interface between the two proteins, hence they are reasonable.
<figure align="center">
<img src="/education/CACA-guided/Fig/CACA-restraints-3D.png">
<p>CA-CA restraints mapped to the superimposed model</p>
</figure>



<hr>
## Setting up the docking with the CA-CA restraints
_Note: To perform CA-CA guided docking runs using HADDOCK, you will need to
register as a user with an Expert or Guru level access._

We will now launch the docking run. For this scenario we will make us of the
expert interface of the HADDOCK web server:
   [http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-expert.html](http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-expert.html)

For the case in this tutorial, the interface prediction confidence from
PS-HomPPI v2.0 is Safe Mode, which indicates the structural templates are quite
reliable. Therefore, we will use the CA-CA distance restraints as “unambiguous
restraints” in HADDOCK.

For CA-CA guided docking, to save the docking time we can reduce the number of
docked models to 50, 50, 50 for the rigid-body stage, the semi-flexible
refinement stage, and the explicit solvent refinement stage, respectively.  To
further save running time, “Number of trials for rigid body minimization” is
also set to 1. “Sample 180 degrees rotated solutions during rigid body EM” is
turned off. The docking process may take 20 min to hours depending on how busy
the queuing system is. 

<hr>
## First analysis of the docking results

Once your run has completed you will be presented with a result page showing
the cluster statistics and some graphical representation of the data (and you
will also be notified by email). 

We already pre-calculated full docking runs. The full runs for the scenario
described above can be accessed at: 
 [http://milou.science.uu.nl/services/HADDOCK2.2/Files/CACA_guided_1ACB_tutorial/](http://milou.science.uu.nl/services/HADDOCK2.2/Files/CACA_guided_1ACB_tutorial/)

<figure align="center">
<img src="/education/CACA-guided/Fig/haddock_result_html1.png">
<img src="/education/CACA-guided/Fig/haddock_result_html2.png">
<p>Example of result page</p>
</figure>

In order to check if any of the docking models we obtained makes sense, we will
compare them to the experimentally determined target structure (PDB ID: 1ACB).
This structure has been solved by X-ray crystallography at 2 Å resolution. The
corresponding PDB file is available in the downloaded tutorial data as
`1ACB_target.pdb`.

We will visualize the top 4 models and compare those to the crystal structure
of the target structure (PDB ID: 1ACB). 

<pre><a class="prompt prompt-cmd">cd $dataDIR/1ACB/HADDOCK_results/output
$path_to_pymol/pymol cluster&ast;.pdb
</a></pre>

<pre><a class="prompt prompt-pymol">PyMOL> load $dataDIR/1ACB/evaluation/1ACB_target.pdb
PyMOL> select 1ACB_A, 1ACB_target and chain A
PyMOL>alignto 1ACB_A
PyMOL>zoom
PyMOL>util.cbc
PyMOL>color pink, 1ACB_target and chain A
PyMOL>color red, 1ACB_target and chain B
</a></pre>

<figure align="center">
<img src="/education/CACA-guided/Fig/top4_and_target.png">
<p> top 4 haddock models compared with the target structure</p>
</figure>

We can see that the docked models (green and blue) have similar interfaces as
those in the X-ray structure of the target (pink and red). 

<hr>
## Comparison with superimposition

Superimposition is one of the simplest and widely used template-based modelling
methods. It is based on global structure–structure alignments, and generates
models by superimposing unbound 3D component protein (or domain) structures
onto structure templates. However, superimposition typically treat individual
unbound structures as rigid, thus cannot model the conformational changes upon
binding, and tends to generate large numbers of steric clashes at the
interface. 

In contrast, the CA-CA guided docking protocol treats the interface as
flexible. At the second stage of HADDOCK, HADDOCK uses the simulated annealing
to optimize the conformation of the backbone and sidechains of the docked
interface. At the third stage, HADDOCK puts the docked models in explicit
solvent and runs short molecular dynamics (MD) to optimize the interface. In
[Xue et al. 2017](https://academic.oup.com/bib/article/18/3/458/2562753), we show that our CA-CA guided docking protocol is
superior to superimposition for cases with medium to large conformations upon
binding. 

Now let’s compare the superimposed models with our CA-CA guided models. 

PS-HomPPI v2.0 automatically generates superimposed models. They are stored
under
`$dataDIR/1ACB/PSHomPPI_results/output/A:B/superimposed_models/supUnbound2TemplatePDB/final/finalSup`. 

<pre><a class="prompt prompt-cmd">cd
$dataDIR/1ACB/PSHomPPI_results/output/A:B/superimposed_models/supUnbound2TemplatePDB/final/finalSup
$path_to_pymol/pymol finalSup&ast;.pdb

</a></pre>

<a class="prompt prompt-pymol">
PyMOL>load $dataDIR/1ACB/evaluation/1ACB_target.pdb
</a>

<figure align="center">
<img src="/education/CACA-guided/Fig/superim_models_and_target.png">
<p>Superimposition models compared with the target structure</p>
</figure>

We can see that the superimposed models (green and blue) are different from the
target structure (pink and red) at the interface, failing to model
conformational changes upon binding. 

<hr>
## Calculate i-RMSD (interface RMSD) between models and the target complex

Let’s further calculate the interface RMSD between the target structure and the
docked models/superimposed models. We have put the scripts under
`$dataDIR/1ACB/evaluation/scripts`. To calculate i-RMSD, we will also need to
install [ProFit](http://www.bioinf.org.uk/programs/profit/). Please download
ProFit and install it.

First, let’s calculate the i_zone file, which will be used ProFit to calculate
i-RMSD. 

<pre><a class="prompt prompt-cmd">cd $dataDIR/1ACB/evaluation
scripts/i_zone.sh 1ACB_target.pdb 
</a></pre>

This step generates the 1ACB_target.izone file. You can use your favorite text
editor to open this file. This file defines the interfacial residues, upon
which i-RMSD will be calculated. For more information, please check the online
document of ProFit.

**Note**: 
1. For easy analysis, we have matched the unbound PDB files with the
target PDB file before running PS-HomPPI v2.0 and HADDOCK (i.e., the residue
numbering of the PDB files are the same and the chain IDs are the same).

2.  `i_zone.sh` calls `contact-chainID_allAtoms`, a cpp executable for
    calculating the pairwise distance between atoms at the interface. If
    `contact-chainID_allAtoms` is not working, the
    `contact-chainID_allAtoms.cpp` needs to be recompiled. An example of
    compling on i-mac:

        g++ contact-chainID_allAtoms.cpp -o contact-chainID_allAtoms


Then we can calculate i-RMSD for CA-CA guided docked models using `$dataDIR/1ACB/evaluation/scripts/i-rmsd-calc_oneCase.sh`. 

_Note: Before running i-rmsd-calc_oneCase.sh, you will need to modify the ProFit path in `i-rmsd-calc_oneCase.sh` and point it to the profit executable on your computer._

The usage of `i-rmsd-calc_oneCase.sh` is:

    Usage: i-rmsd-calc_oneCase refe_pdb izoneFL decoy_DIR output_DIR

We will use the target PDB file (1ACB_target.pdb) as our refe_pdb. 

1. Calculate i-RMSD for CA-CA models.

<pre><a class="prompt prompt-cmd">cd $dataDIR/1ACB/evaluation
scripts/i-rmsd-calc_oneCase.sh 1ACB_target.pdb 1ACB_target.izone $dataDIR/1ACB/HADDOCK_results/output .
</a></pre>

The commands above will generate a file called i-RMSD.dat under `evaluation`. Let’s rename it to `CACA.irmsd`. 

<pre><a class="prompt prompt-cmd">mv i-RMSD.dat CACA.irmsd
</a></pre>

This file can be opened by any text editor:

<pre style="background-color:#DAE4E7">
cluster1_3.pdb 1.742
cluster1_1.pdb 1.759
cluster1_2.pdb 1.767
cluster1_4.pdb 1.851
</pre>

2. Calculate i-RMSD for superimposed models.


<pre>
<a class="prompt prompt-cmd">
cd $dataDIR/1ACB/evaluation
superim_model_DIR="$dataDIR/1ACB/PSHomPPI_results/output/A:B/superimposed_models/supUnbound2TemplatePDB/final/finalSup"
scripts/i-rmsd-calc_oneCase.sh 1ACB_target.pdb 1ACB_target.izone $superim_model_DIR .
mv i-RMSD.dat superim.irmsd
</a>
</pre>


A file named as “superim.irmsd” will be generated. It contains the i-RMSD for each superimposed model:

<pre style="background-color:#DAE4E7">
finalSup.4b2aC_4b2aD.template2.pdb 2.282
finalSup.3rdzA_3rdzC.template5.pdb 2.288
finalSup.4b2aA_4b2aB.template1.pdb 2.288
finalSup.3rdzB_3rdzD.template4.pdb 2.316
finalSup.4h4fA_4h4fB.template3.pdb 2.616
</pre>

By comparing the i-RMSDs of CA-CA models (`CACA.irmsd`) and those of superimposed
models (`superim.irmsd`), we can see that the CA-CA models have smaller i-RMSDs
even when the same set of templates are used. 

<a class="prompt prompt-question">
Can you repeat this tutorial after changing the “CA-CA (Alpha carbon-Alpha
carbon) distance Threshold” parameter of PS-HomPPI v2.0 from 15 Å to 8.5 Å?
Did you see the difference of docked models of your new docking run with the
docked models generated with 15 Å in our tutorial?
</a>

<details style="background-color:#DAE4E7">
<summary>See solution:
</summary>

The precalculated PS-HomPPI and HADDOCK results are under
`$dataDIR/1ACB/QN_ANS`. Using 8.5 Å cutoff, the CA-CA models are of less
quality than CA-CA models with 15 Å. 

</details>



<hr>
## Conclusions
We have demonstrated the use of CA-CA distance restraints from multiple
templates to guide the docking process in HADDOCK. The CA-CA distance
restraints are derived from PS-HomPPI v2.0. We have shown the superiority of
CA-CA guided flexible docking over simple superimposition on a case with large
conformational changes upon binding. 

<hr>
## Congratulations!

Thank you for following this tutorial. If you have any questions or suggestions, feel free to contact us via email, or post your question to 
our [HADDOCK forum](http://ask.bioexcel.eu/c/haddock){:target="_blank"} hosted by the 
[<img width="70" src="/images/Bioexcel_logo.png">](http://bioexcel.eu){:target="_blank"} Center of Excellence for Computational Biomolecular Research.

[link-cns]: http://cns-online.org "CNS online"
[link-data]: http://milou.science.uu.nl/cgi/services/DISVIS/disvis/disvis-tutorial.tgz "DisVis tutorial data"
[link-disvis]: http://milou.science.uu.nl/services/DISVIS "DisVis webserver"
[link-pymol]: http://www.pymol.org/ "PyMOL"
[link-haddock]: http://bonvinlab.org/software/haddock2.2 "HADDOCK 2.2"
[link-haddock-web]: http://haddock.science.uu.nl/services/HADDOCK2.2 "HADDOCK 2.2 webserver"
[link-haddock-easy]: http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-easy.html "HADDOCK2.2 webserver easy interface"
[link-haddock-expert]: http://haddock.science.uu.nl/services/HADDOCK2.2/haddockserver-expert.html "HADDOCK2.2 webserver expert interface"
[link-haddock-register]: http://haddock.science.uu.nl/services/HADDOCK2.2/register.html "HADDOCK web server registration"
[link-xwalk]: http://www.xwalk.org
