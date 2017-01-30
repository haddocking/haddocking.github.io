---
layout: page
title: "HADDOCKing of the p53 N-terminal peptide to MDM2"
excerpt: "HADDOCKing of the p53 N-terminal peptide to MDM2"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modeling, docking, p53, MDM2]
image:
  feature: pages/banner_education-thin.jpg
---
## General Overview
This tutorial introduces protein-protein docking using the HADDOCK web server. It also introduces 
the CPORT web server for interface prediction, based on evolutionary conservation and other 
biophysical properties. By the end of this tutorial, you should know how to setup a HADDOCK run and 
interpret its results in terms of biological insights.

- [A bite of theory](#a-bite-of-theory)  
- [Predicting the interface of p53 on Mdm2](#predicting-the-interface-of-p53-on-mdm2)  
- [Preparing the structures for the docking calculation](#preparing-the-structures-for-the-docking-calculation)  
- [Setting up the docking calculation using the HADDOCK web server](#setting-up-the-docking-calculation-using-the-haddock-web-server)
- [Analyzing the docking calculation results](#analyzing-the-docking-calculation-results)

##A bite of theory
Protein-protein interactions mediate most cellular processes in the cell, such as differentiation, 
proliferation, signal transduction, and cell death. Their structural characterization is however 
not always trivial, even with the constant developments in x-ray crystallography and nuclear 
magnetic resonance spectroscopy. The culprits widely vary, ranging from the native environment of 
the complexes, which might make them hard to purify or crystallize, to the size of the system being 
too large for current methodologies to grasp. More importantly, homeostasis often depends on very 
tightly regulated transient interactions, yet another hindrance to the purification and 
characterization of these complexes. Nevertheless, three decades of spectacular progress in 
structural biology have shown that the protein fold space is finite and the rules of the folding 
game are well defined. This prompted the development of several computational methods aimed at 
complementing experimental techniques in their quest for a full 3D view of the proteome.  A widely 
used computational method for the prediction of the protein-protein complexes is molecular docking, 
which aims at generating the structure of such a complex starting from the structures (or models) 
of its native constituents.

This tutorial will introduce HADDOCK (High Ambiguity Driven DOCKing) as a method to predict the 
three-dimensional structure of protein-protein complexes in silico using a variety of sources of 
information to guide the docking process and score the predicted models. 
[HADDOCK](http://www.bonvinlab.org/software/haddock2.2/haddock.html) is a collection of python 
scripts derived from [ARIA](http://aria.pasteur.fr) that harness the power of 
[CNS](http://cns-online.org) (Crystallography and NMR System) for structure calculation of 
molecular complexes. What distinguishes HADDOCK from other docking software is its ability, 
inherited from CNS, to incorporate experimental data as restraints and use these to guide the 
docking process alongside traditional energetics and shape complementarity. Moreover, the intimate 
coupling with CNS endows HADDOCK with the ability to actually produce models of sufficient quality 
to be archived in the Protein Data Bank.

A central aspect to HADDOCK is the definition of ambiguous interaction restraints or AIRs. These 
allow the translation of raw data such as NMR chemical shift perturbation or mutagenesis 
experiments into distance restraints that are incorporated in the energy function used in the 
calculations. AIRs are defined through a list of residues that fall under two categories: active 
and passive. Generally, active residues are those of central importance for the interaction, such 
as residues whose knockouts abolish the interaction or those where the chemical shift perturbation 
is higher. Throughout the simulation, these active residues are restrained to be part of the 
interface, if possible, otherwise incurring in a scoring penalty. Passive residues are those that 
contribute for the interaction, but are deemed of less importance. If such a residue does not 
belong in the interface there is no scoring penalty. Hence, a careful selection of which residues 
are active and which are passive is critical for the success of the docking.

The docking protocol of HADDOCK was designed so that the molecules experience varying degrees of 
flexibility and different chemical environments, and it can be divided in three different stages, 
each with a defined goal and characteristics:

1.	Randomization of orientations and rigid-body minimization (it0).
In this initial stage, the interacting partners are treated as rigid bodies, meaning that all 
geometrical parameters such as bonds lengths, bond angles, and dihedral angles are frozen. The 
partners are separated in space and rotated randomly about their centers of mass. This is followed 
by a rigid body energy minimization step, where the partners are allowed to rotate and translate to 
optimize the interaction.
The role of AIRs in this stage is of particular importance. Since they are included in the energy 
function being minimized, the resulting complexes will be biased towards them. For example, 
defining a very strict set of AIRs leads to a very narrow sampling of the conformational space, 
meaning that the generated poses will be very similar. Conversely, very sparse restraints (e.g. the 
entire surface of a partner) will result in very different solutions, displaying greater 
variability in the region of binding.

2.	Semi-flexible simulated annealing in torsion angle space (it1)
The second stage of the docking protocol introduces flexibility to the interacting partners through 
a three-step molecular dynamics-based refinement in order to optimize interface packing. It is 
worth noting that flexibility in torsion angle space means that bond lengths and angles are still 
frozen. The interacting partners are first kept rigid and only their orientations are optimized. 
Flexibility is then introduced in the interface, which is automatically defined based on an 
analysis of intermolecular contacts within a 5Å cut-off. This allows different binding poses coming 
from it0 to have different flexible regions defined. Residues belonging to this interface region 
are then allowed to move their side-chains in a second refinement step. Finally, both backbone and 
side-chains of the flexible interface are granted freedom.
The AIRs again play an important role at this stage since they might drive conformational changes.

3.	Refinement in Cartesian space with explicit solvent (water)
The final stage of the docking protocol immerses the complex in a solvent shell so as to improve 
the energetics of the interaction. HADDOCK currently supports water (TIP3P model) and DMSO 
environments. The latter can be used as a membrane mimic. In this short explicit solvent refinement 
the models are subjected to a short molecular dynamics simulation at 300K, with position restraints 
on the non-interface heavy atoms. These restraints are later relaxed to allow all side chains to be 
optimized.

The performance of this protocol of course depends on the number of models generated at each step. 
Few models are less probable to capture the correct binding pose, while an exaggerated number will 
become computationally unreasonable. The standard HADDOCK protocol generates 1000 models in the 
rigid body minimization stage, and then refines the best 200 – regarding the energy function - in 
both it1 and water. Note, however, that while 1000 models are generated by default in it0, they are 
the result of five minimization trials and for each of these the 180º symmetrical solution is also 
sampled. Effectively, the 1000 models written to disk are thus the results of the sampling of 
10.000 docking solutions.

The final models are automatically clustered based on a specific similarity measure – positional 
interface ligand RMSD (iL-RMSD) – that captures conformational changes about the interface by 
fitting on the interface of the receptor (the first molecule) and calculating the RMSDs on the 
interface of the smaller partner. The interface used in this calculation is automatically defined 
based on an analysis of all contacts made in all models.

## Predicting the interface of p53 on Mdm2
HADDOCK excels at predicting the structure of the protein complexes given there is some sort of 
information to guide the docking. In the absence of experimental information, it is possible to use 
features such as sequence conservation and biophysical characteristics of surface residues to infer 
putative interfaces on a protein surface. Since the homology modeling module created a list of 
homologues of mouse MDM2, it is possible to assess which residues are more conserved.

The assess sequence conservation, the homologous sequences have first to be aligned using a 
multiple sequence alignment algorithm, such as [Clustal](http://www.clustal.org/). HMMER calculates 
*pairwise* sequence alignments between the query and all the hits. In the homology modeling 
module, these alignments were converted to a FASTA format and stored in the `psa.fasta` file. All 
it takes to build a multiple sequence alignment is then to combine the original `MDM2_MOUSE.fasta` 
file with this other FASTA file and submit it to Clustal Omega. To visualize the alignment, and 
which positions are more conserved, the easiest way is to generate a sequence *logo*. For each 
position in the sequence, the logo identifies the most frequently occurring residues and scales its 
one-letter code according to a conservation score. We will be using the 
[weblogo server](http://weblogo.threeplusone.com/create.cgi), in order the generate the sequence
logo for the alignment produced by `clustalo`.

<a class="prompt prompt-info">
  Generate a multiple sequence alignment of the MDM2 homologous sequences and create a web logo to 
inspect which residues are highly conserved.
</a>

<a class="prompt prompt-cmd">
    cat MDM2_MOUSE.fasta psa.fasta > MDM2_family.fasta  
    clustalo -i MDM2_family.fasta --dealign -o MDM2_family.aln  
</a>

<a class="prompt prompt-question">
  Which regions of the sequence are highly conserved? And which are less conserved?
</a>

<a class="prompt prompt-info">
  Visualize the homology model of mouse MDM2 in Pymol.
</a>

<a class="prompt prompt-question">
  Based on the conservation analysis and on the model, is there a region of the structure you could 
discard?
</a>
<a class="prompt prompt-question">
  Can you draw a conclusion about which region of the protein can be important for binding, based 
solely on the evolutionary conservation analysis?
</a>

Besides sequence conservation, other features can be used to predict possible interfaces on protein 
structures. For example, certain residues tend to be overrepresented at protein-protein interfaces. 
This information, combined with evolutionary conservation and with a surface clustering algorithm 
that finds groups of surface residues meeting both the previous criteria results in reasonably 
accurate predictions. This is the basis of the 
[WHISCY](http://www.nmr.chem.uu.nl/Software/whiscy/startpage.htm) algorithm. A more advanced 
predictor, the [CPORT](http://haddock.science.uu.nl/services/CPORT/) web server, judiciously 
combined (up to) 6 different predictors to provide a a consensus prediction that is more robust and 
more reliable than any of the individual predictors alone. CPORT was designed to provide 
predictions for HADDOCK and as such, its output consists of a listing of residues predicted to be 
at the interface with a high degree of confidence. The server also returns a PDB file of the 
original structure loaded with the predictions in the temperature factor column. This is extremely 
helpful to visualize the predictions in Pymol.

<a class="prompt prompt-info">
  Submit the homology model of mouse MDM2 to the CPORT web server and load the resulting PDB file 
in Pymol.
</a>
<a class="prompt prompt-pymol">
    spectrum b, cyan_red, cport
</a>
<a class="prompt prompt-question">
    Do the predictions highlight a particular region of the homology model?
</a>

<a class="prompt prompt-info">
  Note down the list of residues predicted by CPORT to be part of an interface.
</a>

## Preparing the structures for the docking calculation
In order to perform a docking calculation with HADDOCK, the initial structures of both MDM2 and p53 
must fulfill a few requirements. First, the PDB files must have an `END` statement as a last line. 
The files cannot contain also atoms with multiple occupancies. It is also possible to submit an 
ensemble of structures, which is useful for the representatives of p53 extracted from the molecular 
dynamics simulation. However, all members must contain exactly the same atoms. Luckily, both the 
files produces by MODELLER and by GROMACS respect the `END` statement and multiple occupancy 
requirement, so no action is necessary here.

Then, when performing a docking calculation, it is wise to remove any unstructured or flexible 
termini that might obstruct the binding of the partner, particularly if there is no flexibility 
allowed and little information on the role of these termini in the binding. These long unstructured 
or flexible regions probably flop about in space, making their conformation in the model very 
likely artificial. The previous conservation analysis showed that the first 16 residues are not 
conserved in the MDM2 alignment, which contains 169 members. In the structure of the homology 
model, these 16 residues correspond to the N-terminal region that was modeled using the 
`loopmodel` protocol, and which scored badly at the validation stage. It seems safe then, to remove 
this region of the homology model before the docking calculations.

<a class="prompt prompt-info">
  Edit the MDM2_MOUSE structure in Pymol to remove the first 16 residues of the unstructured 
N-terminal.
</a>
<a class="prompt prompt-pymol">
  remove resi 1-16 and MDM2_MOUSE.BL00070001
</a>

The structures of the p53 peptide originating from the molecular dynamics simulation can be 
submitted as a single ensemble to HADDOCK. The `pdb_join.py` utility of the `pdb-tools` set 
provides a quick way of building such an ensemble structure from isolated PDB files. It also adds 
the proper `END` statement to the PDB file. Finally, it has a built-in check for the integrity of 
the ensemble, i.e. that all members have exactly the same atomic constitution.

<a class="prompt prompt-info">
  Concatenate different representatives of the MD simulation of the p53 peptide into an ensemble 
structure.
</a>
<a class="prompt prompt-cmd">
  pdb_join.py p53_cluster_1.pdb p53_cluster_2.pdb p53_cluster_3.pdb > p53_ensemble.pdb
</a>

## Setting up the docking calculation using the HADDOCK web server
Having prepared the initial structures and constructed a list of putative interface residues, it is 
time to submit the docking calculation using the 
[HADDOCK web server interface](haddock.science.uu.nl/services/HADDOCK2.2/haddock.php). Under the 
header *HADDOCK Webserver* there are links to all the interfaces: Easy, Expert, Guru, Prediction, 
Multibody, and File Upload. It also lists both the default settings of the webserver 
([here](http://haddock.science.uu.nl/services/HADDOCK2.2/settings.html)), which are important to 
understand how restraints for example are handled, as well as a listing of supported modified 
amino acids. Proceed to the *Guru* interface by clicking on the appropriate link.

<a class="prompt prompt-attention">
  If you are following the Molecular Modeling course, ask the instructors for the web server 
credentials. Otherwise, please register for an (free for academics) account.
</a>

The *Guru* interface presents several foldable tabs and text input fields for a custom run name, 
the registered username and password. To submit the starting structures, click on the red tab names 
to unfold them. The larger structure should be defined in the *First Molecule* tab, for a good 
performance on the post-docking clustering step. Each molecule submission tab has two subsections 
and three foldable menus. In *Structure definition*, we can specify where the structure is coming 
from in dropdown menu, which chains are to be extracted from the PDB file and, in case we choose to 
directly take a structure deposited in the Protein Data Bank, its PDB ID. In *Restraints 
definition*, two text fields are available to write down comma-separated lists of residues (e.g. 
1,2,3,4 ). It also allows to automatically selecting passive residues based on those neighboring 
the active residues. Again, while passive residues are optional, we must always submit active 
residues – at least for one partner, the other partner can have only passive for example - for the 
docking to start. For MDM2, uncheck the two boxes at the end of the tab concerning the charge of 
the termini. For the p53 peptide, unfold the *Fully flexible segments* tab and in *First segment* 
write down the numbering of the termini of the peptide: *First Number* -- 1 and *Last Number* -- 
14. This will cause HADDOCK to consider the peptide atoms flexible during all stages of the 
simulated annealing refinement stage and therefore increase sampling.

<a class="prompt prompt-info">
  Submit the structures of mouse MDM2 and p53 by choosing "I am submitting it" from the dropdown 
menu and uploading the PDB files using the form. Define the chains to use as "All".
</a>

The restraints definitions require some thought. Active residues in HADDOCK are those that are 
absolutely required to be at the interface. Ambiguous Interaction Restraints, or AIRs, are created 
between active residues of both partners. Passive residues, on the other hand, are those that 
*might* be at the interface. The webserver creates AIRs between active residues of one partner and 
passive residues of the other, but never between passive residues only. Further, restraints between 
two active residues **must** be respected or there is an energy penalty. Restraints between active 
and passive residues are more flexible and can be violated freely without an energetic penalty. For 
the docking of MDM2 and p53, given the nature of the interface data and of the system 
(protein/peptide interaction), the recommended course of action is to classify residues on the protein as 
*active* and those on the peptide as *passive* following the recepee with published in our [Structure 2013](http://dx.plos.org/10.1371/journal.pone.0058769) paper.

<a class="prompt prompt-info">
  Define as active residues of MDM2 the active ones provided by CPORT. Remember to remove from the list 
numbers 1-16, as these were removed from the PDB file. For the p53 peptide, list as passive all 
residues (1 to 15).
</a>

The use of an ensemble of structures translates to a worse sampling at the rigid-body stage. The 
total number of models generated during this first stage is divided by the number of models in the 
ensemble. With the default values of 1000 rigid-body models, an ensemble of 10 members translates 
to 100 models generated per member of the ensemble. This reduction in sampling might deteriorate 
the accuracy of the docking calculations, particularly if the restraints are fuzzy, as is the case 
of bioinformatics predictions. As such, we need to increase the number of structures generated at 
the several stages of the docking protocol. As a rule of thumb, 1000 rigid-body models per member 
of the ensemble is a good number. The number of models selected to it1 and water can simply be 
doubled. The computational cost of these refinement stages does not allow a proportional increase. 
These numbers can be edited in the *Sampling parameters* tab. Likewise, the number of structures to 
be analyzed must be adapted to reflect these changes. You can find this in the last tab of all: 
*Analysis parameters*.

<a class="prompt prompt-info">
  Change the number of models generated at the rigid-body stage to 10.000, and of the semi-flexible 
and water refinement stages to 400. Change also the number of structures to analyze to 400.
</a>

The clustering algorithm must also be adjusted to accommodate the small size of the peptide. The 
default cutoff of 7.5Å (interface-ligand RMSD) is very likely too broad and will generate very 
large and diverse clusters. This setting can be changed in the *Parameters for clustering* tab.

<a class="prompt prompt-info">
  Set the clustering cutoff to 5.0Å to accommodate the small size of the peptide.
</a>

Having filled all the necessary fields, running the docking simulation is one click away. Choose a 
name to give to the simulation and type it in the *Name* field at the top of the *First Molecule* 
section. If no name is given, the webserver will attribute the simulation a generic identifier 
(e.g. run1). After double-checking all options, type in the webserver credentials -- username and 
password -- and click *Submit*.

After submission, the webserver redirects to a confirmation page that contains two links. The first 
prompts the download of the docking parameter file – haddockparam.web – that contains all the 
settings and data necessary to reproduce the simulation and is therefore recommended to save. It 
can be used through the *File Upload* interface of the webserver. The second link points to the 
results page of the simulation. Since a regular docking simulation lasts, on average, a couple of 
hours, this page displays its current status while not complete: PROCESSING, QUEUED, or RUNNING. In 
case a critical error prevents the simulation from continuing, whether because of problems with the 
input data, or problems during the simulation itself, the webpage displays an ERROR message. Most 
of these status changes are accompanied by an e-mail that is sent to the address linked to the user 
account. In case of errors, this e-mail also offers additional details on the cause(s). For 
students, since all accounts are pre-configured, the email notification is turned off.

## Analyzing the docking calculation results
After the simulation is complete, the results page is generated and a notification email sent to 
the user. This results page entails an overview of the top ten clusters, ranked by average HADDOCK 
score of their four best structures, including statistics of energetic terms and other structural 
measures for each cluster. This allows a quick assessment of the quality of the generated models. 
Furthermore, at the bottom of the page, several plots of different quality-control measures of the 
models also give the opportunity of, at a glance checking the quality of the docking simulation.

<a class="prompt prompt-question">
    How many of the final water-refined models cluster? How many clusters did the docking produce? 
Can you provide an explanation for these numbers?
</a>

<a class="prompt prompt-question">
    Focus on the il-RMSD vs. HADDOCK score plot: does the scoring of HADDOCK provide an unambiguous 
answer of which conformation is more likely to be realistic?
</a>

### Visual inspection of the cluster representatives
Any molecular simulation, docking included, lacks the accuracy to produce one single good model. 
However, with sufficient attempts, reasonable models are likely to populate the results. HADDOCK in 
particular, given its data-driven character, produces a much higher quantity models if the quality 
of the data is good enough. At the end of the simulation, all the models are clustered so as to 
filter out the isolated structures that resemble few others in the pool of models. The models are 
then analyzed on a cluster basis and the best models of the best clusters are considered the best 
representative models of the simulation. Nevertheless, a careful visual inspection is of paramount 
importance and should always be the first step of any simulation analysis. To better visualize the 
differences between each cluster, superimpose all models onto the backbone of the largest partner, 
in this case the MDM2 molecule.  For this we have to select a *reference* model, which we 
arbitrarily define as that of cluster1_1.


<a class="prompt prompt-info">
    If your simulation produced several clusters, download the top-ranking model of each cluster 
and open them in Pymol. If there is only one cluster, open the top four best models of that cluster.
</a>
<a class="prompt prompt-pymol">
    select refe, cluster1_1 and chain A  
    align cluster2_1, refe  
    align cluster3_1, refe  
    ...
</a>

<a class="prompt prompt-question">
    Do the models have any unreasonable feature, such as atomic clashes or unphysical interactions?
</a>
<a class="prompt prompt-question">
    Based on the best scoring clusters, can you advance a putative binding interface for p53 on 
MDM2? Can you identify key residues that might be "hotspots" of this interaction?
</a>

## Congratulations!
The docking calculation of MDM2 and the p53 N-terminal transactivation peptide was the culmination 
of a three-stage computational exercise that involved the three major methods in the repertoire of 
a Computational Structural Biologist. As you have seen, in modeling, there are rarely any 
certainties and you must always operate with extreme care and a constant sense of (self-)criticism. 
Nevertheless, you started with only two sequences and have now three-dimensional models of 
interactions that can be put to the test in the lab. Who knows? Maybe one of your models is 
actually correct and it will help researchers to spare the life of a few of our mice friends!

Thank you for following this tutorial. We welcome any feedback to improve it. For the students 
following the course Molecular Modeling and Simulation, please feel free to voice any criticism 
and/or suggestions to the instructors. You won't be negatively judged for it :) Others may send 
comments to the email on the right side of the page, under the head of Captain HADDOCK!
