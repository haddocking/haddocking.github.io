---
layout: page
title: "HADDOCK2.4 shape-restrained protein-small molecule tutorial"
excerpt: "A tutorial introducing shape restrains for the modelling of protein-small molecule complexes"
tags: [HADDOCK, shape, pharmacophore, protein-small molecule, rdkit]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>

## Introduction

This tutorial will demonstrate the use of HADDOCK for the modelling of protein-small molecule complexes. We will make
use of a recently developed protocol whose key element is the use of template-derived shapes to drive the modelling
process. More details about the method and the performance of the protocol when benchmarked on a fully unbound dataset
can be seen in a freely available [preprint](https://www.biorxiv.org/content/10.1101/2021.06.10.447890v1)
(not peer-reviewed).

For this tutorial we will make use of the [HADDOCK2.4 webserver](https://wenmr.science.uu.nl/haddock2.4).

A description of the previous major version of our web server [HADDOCK2.2](https://alcazar.science.uu.nl/services/HADDOCK2.2/)
can be found in the following publications:

* G.C.P van Zundert, J.P.G.L.M. Rodrigues, M. Trellet, C. Schmitz, P.L. Kastritis, E. Karaca, A.S.J. Melquiond, M. van Dijk, S.J. de Vries and  A.M.J.J. Bonvin.
[The HADDOCK2.2 webserver: User-friendly integrative modeling of biomolecular complexes](https://doi.org/doi:10.1016/j.jmb.2015.09.014).
_J. Mol. Biol._, *428*, 720-725 (2015).

* S.J. de Vries, M. van Dijk and A.M.J.J. Bonvin.
[The HADDOCK web server for data-driven biomolecular docking.](https://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html)
_Nature Protocols_, *5*, 883-897 (2010).  Download the final author version <a href="https://igitur-archive.library.uu.nl/chem/2011-0314-200252/UUindex.html">here</a>.

The current version of the webserver and standalone HADDOCK (v2.4) are under beta testing.

Throughout the tutorial, coloured text will be used to refer to questions or instructions, and/or PyMOL or terminal commands.

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

<hr>

## Setup

In order to run this tutorial you will need to have the following software installed: [PyMOL][https://www.pymol.org/].
Additionally, you will also need to run commands in a *nix terminal. If you are running this on a Mac or Linux system then
appropriate shells are already part of the system. Windows users might have to install additional software or activate the
[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10). We consider this to be an advanced
tutorial made with a specific application of HADDOCK in mind. Thus, it assumes familiarity with HADDOCK as well as the command
line.

Prior to getting started we need to setup our environment. The simplest way to do that would be to make use of `anaconda`.
Assuming an existing installation of anaconda the following command should take care of all required python packages.

<a class="prompt prompt-cmd">
  conda create tutorial_env -c conda-forge rdkit openbabel pandas <br>
  conda activate tutorial_env <br>
</a>

After activating the environment we also need to install the pdb-tools package which can be achieved with the following command:

<a class="prompt prompt-cmd">
  pip install pdb_tools <br>
</a>

Also, if not provided with special workshop credentials to use the HADDOCK portal, make sure to register in order to be
able to submit jobs. Use for this the following registration page:
[https://bianca.science.uu.nl/auth/register/haddock](https://bianca.science.uu.nl/auth/register/haddock).

<hr>

## HADDOCK general concepts

HADDOCK (see [https://www.bonvinlab.org/software/haddock2.4/](https://www.bonvinlab.org/software/haddock2.4/)) is a collection of python scripts derived from ARIA ([https://aria.pasteur.fr](https://aria.pasteur.fr)) that harness the power of CNS (Crystallography and NMR System – [https://cns-online.org](https://cns-online.org)) for structure calculation of molecular complexes. What distinguishes HADDOCK from other docking software is its ability, inherited from CNS, to incorporate experimental data as restraints and use these to guide the docking process alongside traditional energetics and shape complementarity. Moreover, the intimate coupling with CNS endows HADDOCK with the ability to actually produce models of sufficient quality to be archived in the Protein Data Bank.

A central aspect to HADDOCK is the definition of Ambiguous Interaction Restraints or AIRs. These allow the translation of raw data such as NMR chemical shift perturbation or mutagenesis experiments into distance restraints that are incorporated in the energy function used in the calculations. AIRs are defined through a list of residues that fall under two categories: active and passive. Generally, active residues are those of central importance for the interaction, such as residues whose knockouts abolish the interaction or those where the chemical shift perturbation is higher. Throughout the simulation, these active residues are restrained to be part of the interface, if possible, otherwise incurring in a scoring penalty. Passive residues are those that contribute for the interaction, but are deemed of less importance. If such a residue does not belong in the interface there is no scoring penalty. Hence, a careful selection of which residues are active and which are passive is critical for the success of the docking.
The docking protocol of HADDOCK was designed so that the molecules experience varying degrees of flexibility and different chemical environments, and it can be divided in three different stages, each with a defined goal and characteristics:

**1. Randomization of orientations and rigid-body minimization (it0)**
In this initial stage, the interacting partners are treated as rigid bodies, meaning that all geometrical parameters such as bonds lengths, bond angles, and dihedral angles are frozen. The partners are separated in space and rotated randomly about their centres of mass. This is followed by a rigid body energy minimization step, where the partners are allowed to rotate and translate to optimize the interaction. The role of AIRs in this stage is of particular importance. Since they are included in the energy function being minimized, the resulting complexes will be biased towards them. For example, defining a very strict set of AIRs leads to a very narrow sampling of the conformational space, meaning that the generated poses will be very similar. Conversely, very sparse restraints (e.g. the entire surface of a partner) will result in very different solutions, displaying greater variability in the region of binding.

<details >
<summary style="bold">
<b><i>See animation of rigid-body minimization (it0):</i></b>
</summary>
<figure align="center">
    <img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/haddock_mini.gif">
</figure>
</details>
<br>

**2. Semi-flexible simulated annealing in torsion angle space (it1)**
The second stage of the docking protocol introduces flexibility to the interacting partners through a three-step molecular dynamics-based refinement in order to optimize interface packing. It is worth noting that flexibility in torsion angle space means that bond lengths and angles are still frozen. The interacting partners are first kept rigid and only their orientations are optimized. Flexibility is then introduced in the interface, which is automatically defined based on an analysis of intermolecular contacts within a 5Å cut-off. This allows different binding poses coming from it0 to have different flexible regions defined. Residues belonging to this interface region are then allowed to move their side-chains in a second refinement step. Finally, both backbone and side-chains of the flexible interface are granted freedom. The AIRs again play an important role at this stage since they might drive conformational changes.

<details >
<summary style="bold">
<b><i>See animation of semi-flexible simulated annealing (it1):</i></b>
</summary>
<figure align="center">
    <img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/haddock_sa.gif">
</figure>
</details>
<br>

**3. Refinement in Cartesian space with explicit solvent (water)**
**Note:** This stage was part of the standard HADDOCK protocol up to (and including) v2.2. As of v2.4 it is no longer performed by default but the user still has the option of enabling it. In its place, a short energy minimisation is performed instead. The final stage of the docking protocol immerses the complex in a solvent shell so as to improve the energetics of the interaction. HADDOCK currently supports water (TIP3P model) and DMSO environments. The latter can be used as a membrane mimic. In this short explicit solvent refinement the models are subjected to a short molecular dynamics simulation at 300K, with position restraints on the non-interface heavy atoms. These restraints are later relaxed to allow all side chains to be optimized.

<details >
<summary style="bold">
<b><i>See animation of refinement in explicit solvent (water):</i></b>
</summary>
<figure align="center">
    <img src="/education/HADDOCK24/HADDOCK24-protein-protein-basic/haddock_water.gif">
</figure>
</details>
<br>

## Protocol outline

Briefly, the main steps of this protocol are the following:

1. Determine a target of interest.
2. Identify and download potential templates of interest for our target of choice.
3. Select one of the identified templates for the modelling of the complex.
4. Perform the docking.
5. Analyse and visualise the results.

**Note:** The shape-based protocol can be declined into a pharmacophore-based protocol. Step 3 can be adapted accordingly as described in the last section of this tutorial.


### 1. Target selection 

We have chosen the complex with PDB id `1d3g` which is part of the [DUD-E dataset](http://dude.docking.org) as our target.
This is a complex of an inhibitory brequinar analong bound to the human dihydroorotate dehydrogenase receptor.

<details >
<summary style="bold">
<b><i>Binding site of target complex (1d3g). The receptor is shown in white cartoon, whereas the brequinar analog
(BRE) in orange sticks. The binding site also contains Orotate (ORO - purple sticks) and Flavin Mononucleotide
(FMN - light blue sticks). BRE acts as an inhibitor of the oxidation of Dihydro-ORO -> ORO and the reduction of
FMN -> dihydro-FMN.</i></b>
</summary>
<figure align="center">
    <img src="/education/HADDOCK24/shape-small-molecule/binding_site.png">
</figure>
</details>
<br>

### 2. Template identification
The nature of the binding site makes it clear that if we are to reproduce the chemical environment of the target complex
then the template we choose must also contain ORO and FMN in its binding site.

The first step requires we search one of the PDB portals (in our case we will make use of [RCSB](https://rcsb.org)) for
templates to extract the shape information we will use throughout the docking. After landing on the homepage of the
aforementioned RCSB portal we activate the advanced search functionality by clicking on the 'Advanced Search' link
immediately below the search bar.

We will use the sequence of the receptor of our target complex as our primary search parameter. Clicking on the
'Sequence' tab of the advanced search parameters we are provided with two options to load the query sequence. Either
write/paste it manually using the large textbox or use a PDB id. We opt for the latter option. Writing `1d3g` in the
'PDB ID' box and clicking on the prompt loads the sequence in the larger textbox above. We also specify an 'Identity
Cutoff' of 100% to make sure we limit the results to only relevant hits.

Generating a tabular report using the "ligand" preset and saving it in CSV format allows us to gather all the data we
need to select a template for docking. The report can be found in the pregenerated file `ligands.csv`. A filtered version
of it with only the required data can be found in the `ligands_filtered.csv` file. To create the latter file we have
filtered out the unnecessary ligands from the original file (ie the compounds common to all complexes such as ORO and FMN
and also all the crystallisation artifacts such as SO4) and only kept the PDB id, ligand id and SMILES string for all
compounds.

### 3. Template selection and docking preparation

As is the case for any template-based modelling approach, the more similar the template is to the target complex the
higher the chance of a successful modelling outcome. In this protocol, we are emphasising ligand similarity over receptor
similarity, meaning we want the template and target compounds to be as similar as possible. The metric we have chosen as
our similarity measure is the [Tversky coefficient](https://en.wikipedia.org/wiki/Tversky_index) (with α, β = 0.2, 0.8,
respectively) computed over the Maximum Common Substructure (MCS) as calculated by the [RDKit implementation](https://www.rdkit.org/docs/GettingStartedInPython.html#maximum-common-substructure).
This metric can be computed in a time-efficient manner and most importantly without prior knowledge of the structure
of the target compound and all that is required is the compound encoded in SMILES format (see `target.smi` and `templates.smi`).

The `templates.smi` file can be created from the following command:

<a class="prompt prompt-cmd">
  grep -v SMILES ligands_filtered.csv | awk '{print $3,$1"_"$2}' > templates.smi <br>
</a>

The `target.smi` file we create manually by copying and pasting the SMILES string from its [RCSB page](https://www.rcsb.org/ligand/BRE).

The next step involves computing the similarity values between our target (reference) compound and all template compounds
we identified through the RCSB search portal. For this we will use an RDKit-based implementation of the MCS procedure described
above. We provide a python-based implementation in the script `calc_mcs.py`. Usage of the script is straightforward:

<a class="prompt prompt-cmd">
  ./calc_mcs.py -te templates.smi -ta target.smi | awk '{print $2}' > tmp <br>
</a>

We choose to only keep the second column because we are only interested in the Tversky metric and the first column of the output
is the Tanimoto metric. To create the similarities file:

<a class="prompt prompt-cmd">
  paste templates.smi tmp | awk '{print $2,$4}' | sed -e 's/_/ /' | sort -grk3 > similarities.txt <br>
  rm tmp <br>
</a>

These similarity values have also been precalculated and can be seen in the `similarities.txt` file.
The file has already been sorted according to similarity value meaning the compounds most similar to the target compound
are near the top of the file. From this point on, the selection of the most suitable template becomes a process of filtering out
the templates that are ill-suited for modelling (low quality, mutations near the binding site, missing density, etc...).
A closer examination of the binding site of template `2PRH` reveals missing density close to the ORO cofactor meaning this
template is not very well suited to our purposes. Thankfully, the next template on the list (`7K2U`) is a template of
equally high quality but has no issues that could interfere with our modelling efforts and thus becomes our template of
choice.

<details >
<summary style="bold">
<b><i>Comparison of the binding site for template 2prh (in green) and target complex (in orange).</i></b>
</summary>
<figure align="center">
    <img src="/education/HADDOCK24/shape-small-molecule/1d3g_vs_2prh.png">
</figure>
</details>
<br>

The docking-ready file is available as `template.pdb` with all the crystallisation artifacts and double occupancies removed).
To achieve that we can use the following command making use of the `pdb_selaltloc` and `pdb_keepcoord` utilities which are
part of the pdb_tools package.

<a class="prompt prompt-cmd">
  paste templates.smi tmp | awk '{print $2,$4}' | sed -e 's/_/ /' | sort -grk3 > similarities.txt <br>
  rm tmp <br>
</a>

The next step involves the creation of the shape (based on the template compound) that will be used for the docking. This
process requires the transformation of all heavy atoms of the template compound into shape beads.

<a class="prompt prompt-cmd">
  grep VU7 template.pdb | awk '{printf "ATOM   %4d  SHA SHA S %3d     %s  %s  %s  %s %s\n", NR, NR, $7, $8, $9, $10, $11}' > shape.pdb <br>
</a>

At the same time we also need to remove the compound present in the template structure since that space is now occupied
by the shape we just created.

<a class="prompt prompt-cmd">
  grep -v VU7 template.pdb > template-final.pdb <br>
</a>

We then need to create the restraints that will be used throughout the simulation to drive the generated compounds to the
binding pocket.

<a class="prompt prompt-cmd">
  for i in {1..27}; do echo "assi (segi B and resi ${i}) (segi S and resi *) 1.0 1.0 0.0"; done > shape_restraints.tbl <br>
</a>

Since there are fewer atoms in the target compound than there are in the shape we are defining the restraints from the
target compound to the shape.

In addition to the restraints that are meant to drive the compound to the binding pocket we also need to define restraints
between the cofactors and their coordinating residues to make sure they maintain their original geometry throughout the
simulation and don't drift away in the flexible stage.

This concludes the preparation steps required for the receptor. However, we still need to prepare the compound structures
we will be using for docking. In order to make this tutorial as close as possible to a real-world application of this
protocol, instead of using a bound form of the compound (from this complex or a different one) we have pregenerated 3D
conformers with RDKit using only the compound SMILES. The conformer ensemble can be found in the `conformers.pdb` file.

### 4. Docking

For the docking we will use the new portal of [HADDOCK2.4](https://wenmr.science.uu.nl/haddock2.4/). If you are already
registered with HADDOCK or have been provided with course credential then you can proceed to job submission immediately.
Alternatively, you can request an account through the registration portal. Keep in mind that for this tutorial you will
have to request "guru" level access.

After logging in you are greeted with the first part of the submission portal. Make sure to use an indicative name for the
run.

This is a three-body docking between the template receptor, the template shape and the generated conformers so we should
set the number of molecules to 3.

<a class="prompt prompt-info">
Number of molecules -> 3
</a>

<a class="prompt prompt-info">
Molecule 1 - input -> PDB structure to submit -> Upload the file named `template-final.pdb`
</a>

<a class="prompt prompt-info">
Molecule 1 - input -> Fix molecule at its original position during it0? -> True
</a>

<a class="prompt prompt-info">
Molecule 2 - input -> PDB structure to submit -> Upload the file named `conformers.pdb`
</a>

<a class="prompt prompt-info">
Molecule 2 - input -> What kind of molecule are you docking? -> Ligand
</a>

<a class="prompt prompt-info">
Molecule 3 - input -> PDB structure to submit -> Upload the file named `shape.pdb`
</a>

<a class="prompt prompt-info">
Molecule 3 - input -> Fix molecule at its original position during it0? -> True
</a>

<a class="prompt prompt-info">
Molecule 3 - input -> What kind of molecule are you docking? -> Shape
</a>

<a class="prompt prompt-info">
Molecule 3 - input -> Segment ID to use during the docking -> S
</a>

Then you can click "Next" to proceed to page 2 of the submission process. This part can be skipped entirely since we will
be defining our restraints through tbl files instead of doing it through the interface. Click on "Next".

<a class="prompt prompt-info">
Distance restraints -> Instead of specifying active and passive residues, you can supply a HADDOCK restraints TBL file (ambiguous restraints) -> Upload the `shape-restraints.tbl` file
</a>

<a class="prompt prompt-info">
Distance restraints -> You can supply a HADDOCK restraints TBL file with restraints that will always be enforced (unambiguous restraints) -> Upload the `cofactor-restraints.tbl` file
</a>

<a class="prompt prompt-info">
Distance restraints -> Remove non-polar hydrogens? -> False
</a>

<a class="prompt prompt-info">
Distance restraints -> Randomly exclude a fraction of the ambiguous restraints (AIRs) -> False
</a>

<a class="prompt prompt-info">
Sampling parameters -> Number of structures for rigid body docking -> 320
</a>

<a class="prompt prompt-info">
Sampling parameters -> Sample 180 degrees rotated solutions during rigid body EM -> False
</a>

<a class="prompt prompt-info">
Sampling parameters -> Perform final refinement? -> False
</a>

<a class="prompt prompt-info">
Energy and interaction parameters -> Scaling of intermolecular interactions for rigid body EM -> 0.001
</a>

<a class="prompt prompt-info">
Scoring parameters ->  Evdw 1 -> 0
</a>

<a class="prompt prompt-info">
Analysis parameters -> Full or limited analysis of results -> None
</a>

After which you can click "Submit". If everything went well your docking run has been added to the queue and might take
anywhere from a few hours to a few days to finish depending on the load on our servers.

### 5. Visualisation and analysis of results

While HADDOCK is running we can already start looking at precalculated results (which have been derived using the exact
same settings we used for our run). The compressed run directory can be downloaded from [here](https://wenmr.science.uu.nl/haddock2.4/run/4242424242/72017-shape-based-small-molecule.tgz)
and it is also part of the provided tutorial files. Using the following command we can expand the contents of the tgz
archive

<a class="prompt prompt-cmd">
  tar xf 72017-shape-based-small-molecule.tgz <br>
</a>

Which will create the `72017-shape-based-small-molecule` directory in the current working directory. The final models can
be found under the `structures/it1` subdirectory. There are 200 PDB files in total and their ranking along with their
scores can be seen in the `file.list` file.

<a class="prompt prompt-cmd">
  head file.list <br>
</a>

The scores of the top 5 models are almost indistinguishable so we will be examining all top 10 models in the hope that
one of them is a model of high quality, meaning it can reproduce the experimentally available structure with a high
degree of accuracy, or at the very least yieliding useful biological insights in the nature of the binding pocket.

<details >
<summary style="bold">
<b><i>Superimposition of the top scoring pose (in orange) on the reference complex (in white).</i></b>
</summary>
<figure align="center">
    <img src="/education/HADDOCK24/shape-small-molecule/top1.png">
</figure>
</details>
<br>

With the following command we can load the top 10 models (sorted by HADDOCK score) along with the reference compound for
closer examination.

<a class="prompt prompt-cmd">
  pymol 1d3g.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_2.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_6.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_9.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_5.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_1.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_26.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_14.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_31.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_27.pdb \ <br>
  72017-shape-based-small-molecule/structures/it1/complex_24.pdb <br>
</a>

After PyMOL has finished loading, we can remove all artifacts and superimpose all models on the reference compound with
the following PYMOL commands:

<a class="prompt prompt-pymol">
  remove resn hoh+so4+act+ddq <br>
  alignto 1d3g and chain A
</a>

And the following PyMOL commands allow us to get a better overview of the binding site:

<a class="prompt prompt-pymol">
  remove hydro <br>
  hide everything, resn sha <br>
  util.cbc <br>
  color white, 1d3g
  util.cnc
</a>

Running the commands above reveals that the top 5 compounds are not only close in terms of HADDOCK score but also in terms
of the pose they obtain in the binding site. Moving to the bottom half of the top reveals an entirely different story with
the models obtaining poses that are significantly different to the crystallographic one. In some cases, such as for model
26, the compound has rotated 180 degrees along the long axis, a problem common to many biomolecular modelling scenarios.
The top 5 poses however are all very close to the reference structure and capture all the details of the interaction with
a high degree of accuracy which of course means that our modelling effort can be considered a success.

As part of the analysis we can also compute the symmetry-corrected ligand RMSD for our model of choice. For example, for
the top-scoring compound the following command can be used:

<a class="prompt prompt-cmd">
  profit -f izone 1d3g.pdb 72017-shape-based-small-molecule/structures/it1/complex_2.pdb <br>
  grep UNK tmp.pdb | pdb_element > tmp_ligand.pdb <br>
  obrms 1d3g_ligand.pdb tmp_ligand.pdb <br>
  rm tmp_ligand <br>
</a>

Revealing a ligand RMSD value of 0.94 indicating excellent agreement between model and reference structures.



## Pharmacophore-based protocol adaptation

The shape-based protocol described above can be adapted into a pharmacophore-based protocol in which the beads used to drive the docking are assigned pharmacophore properties.

This protocol require modifications of the aforedescribed **Step 3**.

### 3.pharm  Template selection and docking preparation

In this protocol, we want template molecules to be as similar as possible as the target ligand in terms of pharmacophore properties. The metric we have chosen is the [Tanimoto coefficient](https://en.wikipedia.org/wiki/Jaccard_index) (Tc) computed over the 2D pharmacophore fingerprints as computed with [RDKIT](https://www.rdkit.org/docs/source/rdkit.Chem.Pharm2D.Generate.html).

To ensure correct 2D pharmacophore descriptor computation, we need to use SDF files as input files.

The `templates.smi` file can be created from the following command:
<a class="prompt prompt-cmd">
  grep -v SMILES ligands_filtered.csv | awk '{print $3,$1"_"$2}' > templates.smi <br>
</a>
The `target.smi` file we create manually by copying and pasting the SMILES string from its [RCSB page](https://www.rcsb.org/ligand/BRE).

SMILES can be converted into SDF files :
<a class="prompt prompt-cmd">
  obabel -ismi templates.smi -osdf -O templates.sdf --gen2D
  obabel -ismi target.smi -osdf -O target.sdf --gen2D<br>
</a>

The generated `templates.sdf` file contain multiple molecule. It must be splitted in a way to have one file per molecule.

<a class="prompt prompt-cmd">
  mkdir templates target  <br>
  mv target.sdf target  <br>
  mv templates.sdf templates  <br>
  # split multi-sdf file  <br>
  cd templates  <br>
  python ../split_sdf.py templates.sdf  <br>
  rm templates.sdf  <br>
  cd ..  <br>
   <br>
</a>

The next step involves computing the similarity values between our target (reference) compound and all template compounds we identified through the RCSB search portal. For this we will use an RDKit-based implementation of the 2D pharmacophore fingerprints computation. We provide a python-based implementation in the script `pharm2D_Tc.py`. Usage of the script is straightforward:

<a class="prompt prompt-cmd">
  python ./pharm2D_Tc.py target/ templates/<br>
</a>

The script will return a file entitled `sim.Tc` containing all Tc values. The line flagged with `best` highlights the most similar template.

<a class="prompt prompt-cmd">
  grep best sim.Tc<br>
</a>

These similarity values have also been precalculated and can be seen in the `sim.Tc` file.
A closer examination of the binding site of template `6cjf` reveals that the 2-chloro-6-methylpyridin group of `F54` ligand may adopt two distinct conformations. A thorough examination of the `6cjf` PDB file shows that the orientation A is associated to an occupancy factor of `0.66` against `0.34`for the conformation B.

Since the conformation A has been more observed than conformation B, we select it as our template of interest.

<a class="prompt prompt-cmd">
  grep 'F54' 6CJF.pdb | grep ' A '| grep -v 'BF54' | sed 's/AF54/ F54/g' > F54.pdb <br>
</a>

<details >
<summary style="bold">
<b><i>Comparison of the binding mode of the template F54 (6cjf) (in green) and the target ligand (in blue).</i></b>
</summary>
<figure align="center">
    <img src="/education/HADDOCK24/shape-small-molecule/1d3g_vs_6cjf.png">
</figure>
</details>
<br>

The docking-ready file is available as `template_pharm.pdb` with all the crystallisation artifacts and double occupancies removed).
To achieve that we can use the following command making use of the `pdb_selaltloc` and `pdb_keepcoord` utilities which are
part of the pdb_tools package.

The next step involves the creation of the **pharmacophore** shape (based on the template compound) that will be used for the docking. This
process requires the addition of pharmacophore information into the PDB file and transformation of all heavy atoms of the template compound into pharmacophore beads.

The pharmacophore information is encoded in the occupancy factor column of the PDB file : 
- Donor: 0.10
- Acceptor: 0.20
- NegIonizable: 0.30
- PosIonizable: 0.40
- ZnBinder: 0.50
- Aromatic: 0.60
- Hydrophobe: 0.70
- LumpedHydrophobe: 0.80

**Warnings**: Make sure that the atomic numbers of F54.pdb start at number 1. The provided `F54.pdb` has been renumbered.

The pharmacophore features can be added to the template ligand with the followng script. This is an essential to create the pharmacophore shape.
<a class="prompt prompt-cmd">
  python add_atom_features.py templates/6CJF_F54.sdf F54.pdb  <br>
</a>
The created `F54_features.pdb` file contains pharmacophore information in the occupancy factor column.

<a class="prompt prompt-cmd">
  lig2shape.py F54_features.pdb <br>
</a>

At the same time we also need to remove the compound present in the template structure since that space is now occupied by the shape we just created.

<a class="prompt prompt-cmd">
  grep -v F54 template_pharm.pdb > template-final_pharm.pdb <br>
</a>

We then need to create the restraints that will be used throughout the simulation to drive the generated compounds to the binding pocket. The pharmacophore restraints are defined from the target to the pharmacophore shape: 

Ex: assi (segid S and resid * and (attr q == 0.60)) (segid B and name C2) 1.0 1.0 0.0
The atom C2 from the target ligand should be guided toward an *Aromatic* bead from the shape

Provided that you generated 3D conformers for your target ligand, stored them in a file called `conformers.pdb`, and added the pharmacophore features information (with the `add_atom_features.py` script), you can generate the pharmacophore restraints to guide the docking. As mentioned earlier, this file is provided in this tutorial for convenience (conformers were generated with RDKIT).

<a class="prompt prompt-cmd">
  python generate_restraints_from_target.py conformers.pdb <br>
  mv conformers.tbl target.tbl
</a>

In addition to the restraints that are meant to drive the compound to the pharmacophore beads in the binding pocket we also need to define restraints
between the cofactors and their coordinating residues to make sure they maintain their original geometry throughout the 
simulation and don't drift away in the flexible stage.

Those restraints are pre-calculated (`cofactor_restraints_pharm.tbl`).

### 4.pharm  Docking
The docking preparation is detailed in **Step 4**. You simply need to adapt the following parameters: 

<a class="prompt prompt-info">
Molecule 1 - input -> PDB structure to submit -> Upload the file named `template-final_pharm.pdb`
</a>

<a class="prompt prompt-info">
Molecule 3 - input -> PDB structure to submit -> Upload the file named `shape_pharm.pdb`
</a>

On the page 3 of the submission process, you need to upload the restraints files of the pharmacophore-based protocol:

<a class="prompt prompt-info">
Distance restraints -> Instead of specifying active and passive residues, you can supply a HADDOCK restraints TBL file (ambiguous restraints) -> Upload the `target_pharm.tbl` file
</a>

<a class="prompt prompt-info">
Distance restraints -> You can supply a HADDOCK restraints TBL file with restraints that will always be enforced (unambiguous restraints) -> Upload the `cofactor-restraints_pharm.tbl` file
</a>