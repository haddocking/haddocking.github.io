---
layout: page
title: "Protein-peptide modeling tutorial using a local version of HADDOCK3"
excerpt: "A tutorial describing the use of HADDOCK3 in the low-sampling scenario to model an protein-peptide complex"
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, sampling]
image:
  feature: pages/banner_education-thin.jpg
---
This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>
<hr>

## Introduction

The tumor suppressor protein **p53** plays a central role in controlling cell cycle arrest, apoptosis, and DNA repair. Its activity is tightly regulated by **MDM2**, an E3 ubiquitin ligase that binds to the transactivation domain of p53 and targets it for degradation. This interaction is a key node in cancer biology, as overexpression of MDM2 leads to functional inactivation of p53 in many tumors.

The **N-terminal region of p53 (residues 18–32)** adopts a short α-helical conformation when bound to the hydrophobic pocket of MDM2. Although short, this peptide region forms several crucial contacts at the interface, making it an ideal candidate for structure-based drug design and peptide inhibitor development.

However, modeling such interactions is not trivial. Peptides are inherently flexible and may adopt different conformations in solution. Capturing this flexibility is essential to predict realistic binding modes. Therefore, this tutorial uses three idealized peptide conformations which are **α-helix, β-sheet, and polyproline-II** combined into a single ensemble. While the docking itself is not explicitly flexible, using an ensemble of pre-generated conformations is a common strategy to implicitly capture some degree of peptide flexibility. This approach increases the chances of identifying binding modes that align with the experimentally known interaction interface.

In this tutorial, you will model the interaction between MDM2 and these peptide models using **ensemble docking**. The aim is to predict plausible binding modes and evaluate which peptide conformers are most compatible with the modeled MDM2 structure. Since there is no experimentally determined interface for mouse MDM2, we use the human MDM2–p53 interaction as a reference to guide restraint definition and assess the docking results. 

Since there is no experimentally determined interface for mouse MDM2, we use the human MDM2–p53 interaction as a reference to guide restraint definition and assess the docking results. Specifically, we refer to the [**1YCR**](https://www.rcsb.org/structure/1YCR){:target="_blank"} structure from the Protein Data Bank, which is the crystallographic complex of human MDM2 bound to the N-terminal transactivation domain of p53. This structure provides high-resolution information about the binding interface and serves as a reliable template for identifying key interaction residues in our docking setup.

For background information on the differences between HADDOCK2.4 and HADDOCK3, see this [web-page](https://www.bonvinlab.org/haddock3/intro.html){:target="_blank"}.

<hr>
<hr>

Throughout the tutorial, colored text will be used to refer to questions or
instructions, and/or PyMOL commands.

<a class="prompt prompt-attention"> This is an attention prompt: pay special attention to this!</a>
<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>


<hr>
<hr>

## Setup/Requirements

In order to follow this tutorial you will need to work on a Linux or MacOSX system. We will also make use of [PyMOL](https://www.pymol.org/){:target="_blank"} (freely available for most operating systems) in order to visualize the input and output data.

We assume that you have a working installation of HADDOCK3 on your system. If not, provided you have a working Python version (3.9 to 3.13), you can install it through:

```bash
pip install haddock3
```

or refer to the HADDOCK3 installation [instructions](https://www.bonvinlab.org/haddock3/INSTALL.html){:target="_blank"} for more details.

Further, we are providing pre-processed haddock-compatible PDB and configuration files, as well as pre-computed docking results. Please download and unzip the provided [zip archive](https://surfdrive.surf.nl/files/index.php/s/vqpRJHi5Io6R3a0) and make sure to **note the location of the extracted files** on your system.There is also a linux command for it:

<a class="prompt prompt-cmd">
wget https://surfdrive.surf.nl/files/index.php/s/vqpRJHi5Io6R3a0/download -O Protein-peptide.zip<br>
unzip Protein-peptide.zip
</a>
 
Unzipping the file will create the `protein-peptide` directory ,which should contain the following directories and files:

* `pdbs`: Contains the pre-processed protein and peptide PDB structures required for docking, as well as bound reference (i.e. experimentally obtained structure).
* `restraints`: Contains interface definition files and the corresponding ambiguous restraint files to guide the docking process.
* `runs`: Contains pre-computed docking results for each scenario as defined in `workflows` directory, useful for comparison or if you prefer to skip the computationally intensive runs.
* `scripts`: A directory containing various scripts used in this tutorial.
* `workflows`: Contains HADDOCK3 configuration files used for the docking scenarios in this tutorial.

<hr>
<hr>

## Preparing PDB Files for Docking

In this section, we will prepare the PDB files of the protein and peptide for docking. The protein model is obtained using **AlphaFold**, and multiple conformations of the peptide are generated using [**PyMOL**](https://www.pymol.org){:target="_blank"}. We will use `pdb-tools` to process the structures, including residue selection, renumbering, and ensemble generation. By default, `pdb-tools` are being installed on your machine together with haddock3. `pdb-tools` documentation is available [here](http://www.bonvinlab.org/pdb-tools/){:target="_blank"}. 

_**Note:**_ that pdb-tools is also available as a [web service](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.

_**Note:**_ Before starting to work on the tutorial, make sure to activate an appropriate virtual environment. If haddock3 was installed using `conda`:

<a class="prompt prompt-cmd">
conda activate haddock3
</a>

For more information about accepted file formats and preparation steps, refer to the [HADDOCK3 user manual – structure requirements](https://www.bonvinlab.org/haddock3-user-manual/structure_requirements.html){:target="_blank"}.

### Protein Structure Preparation 

The accuracy of docking results in HADDOCK3 depends heavily on the quality of the input structures. For this tutorial, we will prepare the **MDM2 mouse protein** (UniProt ID: P23804). [UniProt](https://www.uniprot.org){:target="_blank"} is a comprehensive protein sequence and functional information database, providing access to annotations, sequence features, and structural data.

<a class="prompt prompt-info">Find the mouse MDM2 entry in UniProt using the search box on the home page.
</a>

The correct UniProt entry is **“P23804 – E3 ubiquitin-protein ligase Mdm2 [Mus musculus]**”. This protein has no experimentally solved 3D structure. Therefore, we will use a predicted model from AlphaFold.

<a class="prompt prompt-info">Click on the section ‘Structure’ (on the left) or scroll down until you reach it, and click on “AlphaFold predicted structure” to download the .pdb file.
</a>

<a class="prompt prompt-question">Which part of MDM2 should be kept for docking instead of using the full model, and why might removing irrelevant regions be beneficial?
</a>

This model covers the **full-length sequence**, but for docking we only need a specific part. We are specifically interested in the p53-binding domain ,which corresponds to **residues 26 to 109**. The remaining regions, particularly the disordered parts, are known not to interact with the peptide, so it is advisable to remove them. This also has the advantage of reducing computational cost by making the receptor smaller.

<a class="prompt prompt-info">Scroll further down to the “Family & Domains” section of the same UniProt entry and see the “Domain”
</a>

Once you’ve downloaded the .pdb model,move the downloaded structure file (e.g., AF-P23804-F1-model_v4.pdb) into your working directory (here named Protein-peptide). Then extract the binding domain and replace chain id with `A` using:

<a class="prompt prompt-cmd">
pdb_selres -26:109 AF-P23804-F1-model_v4.pdb | pdb_chain -A | pdb_tidy > AF_MDM2_26_109.pdb
</a>

Command `pdb_selres -26:109` keeps only residues from 26 to 109 out of the entire file. Then, command `pdb_chain -A` modifies the chain id to A. This is done to ensure there will be no overlap between chain id of the receptor with the chain id of the ligand to avoid issues during docking. Lastly, the command `pdb_tidy` ensures the PDB file corresponds to the format specifications. 

_**Note**_ pdb_tidy attempts to correct formatting only, not the actual content of the PDB file.   

### Peptide Structure Preparation
In this section, we will prepare the peptide component of the docking system. The peptide used corresponds to the **N-terminal transactivation domain of mouse p53**, residues **18–32**. The sequence of this peptide is given below, in FASTA format:

<pre style="background-color:#DAE4E7">
>sp|P53_MOUSE|18-32
SQETFSGLWKLLPPE
</pre>

Since p53 is a flexible linear peptide and is not available in structural databases, we will generate three idealized conformations: **α-helix , β-sheet and Polyproline II (ppII)**. These conformations will be combined into a **single ensemble file** suitable for HADDOCK3.

You will use PyMOL’s built-in `fab` command to build the idealized conformations. `fab` generates a structure from a sequence and applies a specified secondary structure.

<a class="prompt prompt-info">Generate an ideal structure for the peptide sequence using the fab script in PyMOL.
</a>

Helical conformation:
<a class="prompt prompt-pymol">
fab SQETFSGLWKLLPPE, peptide_helix, ss=1 <br>
save peptide_helix.pdb, peptide_helix
</a>
Beta-sheet conformation:
<a class="prompt prompt-pymol">
fab SQETFSGLWKLLPPE, peptide_sheet, ss=2 <br>
save peptide_sheet.pdb, peptide_sheet
</a>
 Polyproline II conformation (random coil):
<a class="prompt prompt-pymol">
fab SQETFSGLWKLLPPE, peptide_ppii, ss=0 <br>
save peptide_ppii.pdb, peptide_ppii
</a>

<a class="prompt prompt-question">Why do we simulate multiple conformations of the peptide instead of just one?
</a>

*_Note_*: Once you created pdb files, move saved files to the working directory.

Once you’ve generated the three conformations, use `pdb-mkensemble` from `pdb-tools` to arrange all 3 structures in a single ensemble file:

<a class="prompt prompt-cmd">
pdb_mkensemble peptide_helix.pdb peptide_sheet.pdb peptide_ppii.pdb|pdb_tidy > peptide_ensemble.pdb
</a>

To quickly inspect the contents of the generated ensemble, you can look at the header of the file with:

<a class="prompt prompt-cmd">
head peptide_ensemble.pdb
</a>

#### Examine Ensemble in PyMOL(Optional)
Before moving on to docking, it’s a good practice to **inspect the generated peptide ensemble visually**. This step helps you ensure that all three conformations have been included correctly and that the file structure is clean and consistent.

To open the ensemble in PyMOL, use:
<a class="prompt prompt-info">File >> Open >> peptide_ensemble.pdb
</a>

<a class="prompt prompt-pymol">
split_states all<br>
as cartoon<br>
color yellow, all<br>
</a>

This command loads the ensemble, **splits it into separate model**, and displays each one as a **cartoon** representation in PyMOL.

<hr>
<hr>

## Defining Restraints for Docking

In this section, we describe how to define restraints that guide the docking process in **HADDOCK3**. The restraints specify which regions of the molecules are expected to be involved in the interaction and help focus the docking calculation on relevant interfaces.

_**Note:**_ HADDOCK uses the [**CNS (Crystallography & NMR System)**](https://cns-online.org/v1.3/){target:blank} engine for energy calculations, and thus restraint files must follow a CNS-compatible format. 

We use the `haddock3-restraints` command line tool to generate **ambiguous interaction restraints in** `.tbl` **format**, which is the required format for HADDOCK3. Before generating the `.tbl` file, which contains the 
ambiguous interaction restraints for HADDOCK3, we first need to prepare the active/passive residue lists that define which residues on the interacting molecules are expected to be in contact.

**Active residues:** These residues are “forced” to be at the interface. If they are not part of the interface in the final models, an energetic penalty will be applied. The interface in this context is defined by the union of active and passive residues on the partner molecules. Active residues are typically identified by wet-lab experiments (e.g. mutagenesis, NMR data) or predicted using various software tools such as ARCTIC-3D.
**Passive residues:** These residues are expected to be at the interface. However, if they are not, no energetic penalty is applied.
 
These **restraint files** guide the docking process by constraining the conformational search around used-defined interfaces.

To generate **AIRs** from active/passive residue files, use the following general syntax:

* `file_actpass_protein` and `file_actpass_peptide`: act/pass files for each molecule
*  `--segid-one`, `--segid-two`: specify segment/chain identifiers (optional, but recommended for multi-chain systems).

 <a class="prompt prompt-cmd">
haddock3-restraints active_passive_to_ambig file_actpass_one file_actpass_two [--segid-one] [--segid-two] > output.tbl
</a>

We will now describe how to prepare `.act-pass` files for peptide and protein in detail for each molecule in the following sections.

### Defining Active Residues for Protein

To define the active residues on the protein side, we used [**ARCTIC-3D**](https://rascar.science.uu.nl/arctic3d/){target:blank}, a data-mining software, which can cluster all known interfaces of a protein, grouping similar interfaces in interacting surfaces, i.e. list of amino acids that are likely to participate in the binding. No structural information of the **mouse MDM2** is available, however, such information is present for a **human MDM2**. The list of probable binding site residues identified by **ARCTIC-3D** is:  

<pre style="background-color:#DAE4E7">
54 57 58 61 62 67 72 73 75 93 94 100
</pre>

These residues were specifically chosen considering high probability values over 0.5-0.4 and the known p53 binding interface and were cross-validated in PyMOL using the reference structure 1YCR.

_**Note:**_ See the [BONUS: ARCTIC-3D](#bonushow-to-use-arctic-3d-to-predict-active-residues-of-protein)section to learn how to extract interface clusters from structural prediction.

Precited Active Residue and Associated probability values:

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Interface Residues Identified by ARCTIC-3D</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <br>
  <figure style="text-align: center;">
    <img width="50%" src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/Cluster2_residues.png">
  </figure>
<br>
</details>
<br>

**Check In PyMol:**
Before finalizing the actives, visually confirm that the selected residues correspond to the **p53 binding region** in the MDM2 structure, using the **reference complex 1YCR**.

See which protein residues are within interaction distance of the peptide in the reference complex:

<a class= "prompt prompt-info">
For this in PyMol select the peptide chain, then go to A → modify → around → within 4Å
</a>

This allows you to see which protein residues are within interaction distance (4A) of the peptide in the reference complex.

Then use this command to highlight predicted interface residues on the protein:

<a class="prompt prompt-pymol">
load AF_MDM2_26_109.pdb <br>
color green <br>
show surface <br>
select active, (resi 54+57+58+61+62+67+72+73+75+93+94+100) <br>
color red, active <br>
</a>

Optionally, you can align this structure with 1YCR to verify that the selected residues correspond to the known p53 binding site.

<a class="prompt prompt-question">
Do the selected residues overlap with the p53 peptide-binding site in the MDM2 structure?
</a>

Add these residues to the protein-AR3D-active.act-pass file on the first line, while the second line was left empty because passive should only be defined if active residues are defined for the second molecule.

<a class= "prompt prompt-info">
Add these residues to the "protein-AR3D-active.act-pass" file on the first line, while the second line was left empty because passive should only be defined if active residues are defined for the second molecule.
</a>

### Defining Passive Residues for the Peptide
Since we do not have experimental data or a reliable way to predict which residues of the peptide are directly at the interface, we do not define any active residues. Instead, passive residues are declared manually.

<a class= "prompt prompt-info">
Add all the residues to the peptide-ens-passive.act-pass file on the second line, while the first line was left empty.
</a>

<a class="prompt prompt-attention"> 
Passive residues must only be defined if actives were specified on the other molecule (which we did for MDM2). Typically, active residues are surrounded by passive residues to account for uncertainties in binding site definition and to provide flexibility. In this specific case, however, no active residues are defined on the peptide, so only passive residues are specified. 
</a>

### Restraints Validation
After generating `protein-peptide_ambig.tbl`, validate it using:

<a class="prompt prompt-cmd">
haddock3-restraints validate_tbl protein-peptide_ambig.tbl --silent
</a>

If the file is valid, there will be no output. Otherwise syntax errors will be printed to fix.

_**Note:**_ This command checks only the file’s formatting, not the biological correctness or content of the restraints.

<hr>
<hr>

## Setting Up the Docking with HADDOCK3

After preparing the input structures and defining the interaction restraints, we proceed with setting up and running the docking using the HADDOCK3. In this section, we describe the configuration and execution of a protein–peptide docking workflow involving the MDM2 protein and an ensemble of peptide conformations.

### Defining the Modeling Workflow

We use a standard HADDOCK3 workflow adapted to protein–peptide docking. This workflow includes topology generation, rigid-body minimization, semi-flexible interface refinement, and final refinement, followed by model selection, clustering, and evaluation. Our configuration is stored in the protein_peptide_docking.cfg file.

The modules included in this workflow are:

  * `topoaa`: *Generates the topologies for the CNS engine and builds missing atoms.*
  * `rigidbody`: *Rigid body energy minimization with CNS (`it0` in HADDOCK2.x).*
  * `caprieval`: *Evaluates the rigid-body models using CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ).*
  * `flexref`: *Semi-flexible refinement of the interface (`it1` in haddock2.4).*
  * `caprieval`: *Evaluates the `flexref` models using CAPRI metrics.*
  * `emref`: *Final refinement by energy minimisation (`itw` EM only in HADDOCK2.X).*
  * `caprieval`: *Evaluates the `emref` models using CAPRI metircs.*
  * `seletop`: *Selects the top models based on scoring.*
  * `rmsdmatrix`: *Generates the pairwisw RMSD matrix for all models to asses structural similarity.*
  * `clustrmsd`: *Clustering of models based on the RMSD.*
  * `caprieval`: *Evaluates the clustered models using CAPRI metrics.*
  * `seleoptclusts`: *Selects the top models of all clusters.*
  * `caprieval`: *Evaluates the final selected models using CAPRI metrics.*

The workflow is as follows (file `workflow/protein_peptide_docking.cfg`) looks like:

{% highlight toml %}
 # ============================================
# Protein–Peptide Docking in HADDOCK3
# ============================================

# Directory for scoring
run_dir = "runs/run1"

# Compute mode and resources
mode = "local"
ncores = 50

# Post-processing
postprocess = true
clean = true

# Molecule files (provide correct relative or absolute paths)
molecules = [
   "pdbs/AF_MDM2_26_109.pdb",           # Protein
   "pdbs/peptide_ens.pdb"        # Peptide
]

# ============================================
# Stages Configuration
# ============================================

[topoaa]

[rigidbody]
ambig_fname = "restraints/protein-peptide_ambig.tbl"

sampling = 1000

[caprieval]
reference_fname = "pdbs/1YCR.pdb"

[flexref]
tolerance = 5
ambig_fname = "restraints/protein-peptide_ambig.tbl"

[caprieval]
reference_fname = "pdbs/1YCR.pdb"

[emref]
tolerance = 5
ambig_fname = "restraints/protein-peptide_ambig.tbl"

[caprieval]
reference_fname = "pdbs/1YCR.pdb"

[seletop]
select = 200

[caprieval]
reference_fname = "pdbs/1YCR.pdb"

[rmsdmatrix]

[clustrmsd]
clust_cutoff= 5
plot_matrix = true

[caprieval]
reference_fname = "pdbs/1YCR.pdb"

[seletopclusts]
# Selection of the top 4 best scoring complexes from each cluster
top_models = 4

[caprieval]
reference_fname = "pdbs/1YCR.pdb"

{% endhighlight %}

_**Note:**_Change the `run_dir` name in the `.cfg` file if re-running or using multiple workflows ,HADDOCK won’t start if the directory (e.g., `run2`) already exists.

This workflow is ready-to-run, and can be executed as-is. To use PDB files and restraints, generated during the previous steps of the tutorial, replace values of the parameters `molecules` and `ambig_fname` with corresponding files on your machine. 

### Running HADDOCK

We ran the docking locally (`mode = "local"`) with `ncores = 8`  cores. The docking was executed using the following command:

<a class="prompt prompt-cmd">
haddock3 ./workflows/protein_peptide_docking.cfg
</a>

In this case docking log will appear on the screen. Alternative, you can run the docking in the background and save output log to a file, e.g. `haddock.log`, and any kind of error message to `haddock.err`:

<a class="prompt prompt-cmd">
haddock3 ./workflows/protein_peptide_docking.cfg > haddock.log 2> haddock.err
</a>

This command launches the docking process, and all output is stored in the specified `run_dir` (here: `"run2"`).

To optimize performance while maintaining sampling quality, we set `sampling = 1000` in the `rigidbody` stage and selected the top 200 models (`select = 200`) for downstream refinement (default values). Clustering was performed using the RMSD metric, and the top 4 models from each cluster were selected.

Model evaluation (`aprieval`) was performed using a reference structure (`pdbs/1YCR.pdb`) to assess structural similarity via CAPRI metrics such as i-RMSD, l-RMSD, and Fnat. If reference_fname parameter would not be defined, then the same metrics would’ve been calculated using lowest-score structure. 

<a class="prompt prompt-info">
On a Max OSX M2 processor using 8 cores the full workflow completes in about 2h 10m 55s.
</a>

### Sampling Strategy Consideration

We used the default sampling size of **1000 models**, which corresponds to HADDOCK’s default behavior. In our case, this value was applied across all input conformers in the peptide ensemble.

_**Note:**_ HADDOCK distributes the sampling across each input conformer. This means that if you set `sampling = X` and provide an ensemble of n peptide conformers, the total number of models generated will still be X, but each conformer will be sampled X / n times.For example, with `sampling = 300` and 3 peptide conformations, a total of 300 models will be generated, with each conformation sampled **300 / 3 = 100** times.

Although ideally one should aim for 1000 models per peptide conformation (i.e., sampling = 3000), such computations are rather heavy for 8 cores  . Given that our restraints were defined with high confidence, this reduces sampling deemed a reasonable compromise. A full-size precomputed run with sampling=3000 is available in runs/name.

In a real-case docking scenario, especially when restraint quality is uncertain it is advisable to increase the sampling accordingly, if computational resources allow. However, for very large ensembles (e.g., MD trajectory ), **prior clustering** to reduce ensemble size is highly recommended before attempting full-scale sampling.

### Best Practice of Protein-Peptide Docking

For completeness, we also carried out a **full-scale docking run** using the optimal settings for peptide docking recommended. We generated 1000 models per peptide conformer (3000 in total for three conformations), employed **RMSD-based clustering** with a cutoff of 5, and extended the MD phases (e.g., 2000 steps during the high-temperature TAD and first cooling stage, and 4000 steps during the subsequent cooling stages). This configuration gave a slight improvement in model diversity and interface quality compared to the reduced-sampling run. The results of this 3000-model run are provided under the `runs` directory as `run_bp`.

**Higher sampling** and longer simulations are most beneficial when the correct binding pose is unknown, when restraints are derived from predicted rather than experimental data, when the peptide is highly flexible, or when there could be multiple binding sites. In our case, the difference was modest because the restraints were high-confidence and targeted a single known binding interface; the reduced-sampling run (**~333 models per conformer**) still produced results very similar to those of the larger run.

In practice, **1000 models per conformer** is a good default when computational resources allow. For exploratory work, or when restraint quality is high, the reduced sampling used in this tutorial remains a valid and efficient alternative.

<hr>
<hr>

## Analysis of Docking Results
The docking run was configured with `sampling = 1000` in the `rigidbody` stage and used a peptide ensemble containing **3 conformers**.HADDOCK generates an equal number of rigid-body models for each input conformer combination. With `sampling = 1000`, this results in approximately 1000 total models.

In practice, the `1_rigidbody/` output contained **999 models**, indicating that HADDOCK evenly distributed the sampling across the three conformers, generating about **333 models per conformer**.

### Examine the Results of the Docking Run

In case something went wrong with the docking (or simply if you do not want to wait for the results) you can find the following precalculated runs in the `runs` directory:
- `run1`: Results from the reduced-sampling tutorial run (~333 models/conformer).
- `run_bp_capri`: Results from the full-scale run (1000 models/conformer, 3000 total) with extended MD refinement.

After the docking run was completed, the result directory was inspected. HADDOCK3 automatically generated numbered folders corresponding to each module of the workflow:

{% highlight shell %}
> ls runs/
  0_topoaa/
  1_rigidbody/
  2_caprieval/
  3_flexref/
  4_caprieval/
  5_emref/
  6_caprieval/
  7_seletop/
  8_caprieval/
  9_rmsdmatrix/
  10_clustrmsd
  11_caprieval/
  12_seletopclusts/
  13_caprieval/
  analysis/
  data/
  log
  traceback/
{% endhighlight %}

There is in addition to the various modules defined in the config workflow a log file (text file) and three additional directories:

  * the `data` directory containing the input data (PDB and restraint files) for the various modules.
  * the `analysis`directory containing various plots to visualise the results for each caprieval step.
  * the `traceback` directory containing the names of the generated models for each step, allowing to trace back a model throughout the various stages.

You can find information about the duration of the run at the bottom of the log file. Each sampling/refinement/selection module will contain PDB files - models produced by this module.

For example, the `12_seletopclusts` directory contains the selected models from top-ranked clusters. The clusters in that directory are numbered based on their rank, i.e. `cluster_1` refers to the best-ranked cluster. Information about the origin of these files can be found in that directory in the `seletopclusts.txt` file.

### Finding Ranking, Scores and Model Quality Information

The simplest way to extract ranking information and the corresponding HADDOCK scores per model is to look at the X_caprieval directories (which is why it is a good idea to have it as the final module, and possibly as intermediate steps, even when no reference structures are known). This directory will always contain a capri_ss.tsv file, which contains the model names, rankings and statistics (score, iRMSD, Fnat, lRMSD, ilRMSD and DockQ score). E.g.:

<pre style="background-color:#DAE4E7">
                                   model	md5	caprieval_rank	score	irmsd	fnat	lrmsd	ilrmsd	dockq	rmsd	cluster_id	cluster_ranking	model-cluster_ranking	air	angles	bonds	bsa	cdih	coup	dani	desolv	dihe	elec	improper	rdcs	rg	sym	total	vdw	vean	xpcs
../12_seletopclusts/cluster_2_model_1.pdb       -       1       -102.990        5.349   0.083   12.607  12.622  0.156   4.485   1       2       1       2.323   0.000   0.000   1429.890        0.000   0.000   0.000   -18.001 0.000   -213.378        0.000   0.000   0.000   0.000   -253.600        -42.545 0.000   0.000
../12_seletopclusts/cluster_1_model_1.pdb       -       2       -95.638 2.110   0.375   4.829   4.804   0.489   1.847   2       1       1       51.169  0.000   0.000   1304.920        0.000   0.000   0.000   -36.536 0.000   -120.294        0.000   0.000   0.000   0.000   -109.285        -40.160 0.000   0.000
../12_seletopclusts/cluster_1_model_2.pdb       -       3       -93.064 2.140   0.188   5.251   5.231   0.414   1.844   2       1       2       1.653   0.000   0.000   1246.410        0.000   0.000   0.000   -13.950 0.000   -186.916        0.000   0.000   0.000   0.000   -227.159        -41.896 0.000   0.000
../12_seletopclusts/cluster_1_model_3.pdb       -       4       -91.247 2.406   0.188   5.510   5.498   0.391   2.127   2       1       3       63.658  0.000   0.000   1301.090        0.000   0.000   0.000   -14.069 0.000   -178.029        0.000   0.000   0.000   0.000   -162.309        -47.938 0.000   0.000
../12_seletopclusts/cluster_4_model_1.pdb       -       5       -90.971 6.200   0.083   15.148  15.162  0.126   5.236   5       4       1       42.373  0.000   0.000   1368.080        0.000   0.000   0.000   -27.050 0.000   -130.441        0.000   0.000   0.000   0.000   -130.138        -42.071 0.000   0.000
../12_seletopclusts/cluster_1_model_4.pdb       -       6       -90.247 1.803   0.438   3.839   3.880   0.559   1.555   2       1       4       20.889  0.000   0.000   1177.880        0.000   0.000   0.000   -33.332 0.000   -137.283        0.000   0.000   0.000   0.000   -147.941        -31.547 0.000   0.000
../12_seletopclusts/cluster_3_model_1.pdb       -       7       -86.083 3.542   0.104   8.477   8.440   0.253   3.030   3       3       1       4.620   0.000   0.000   1024.940        0.000   0.000   0.000   -15.482 0.000   -198.277        0.000   0.000   0.000   0.000   -225.065        -31.408 0.000   0.000
</pre>


The relevant statistics are:

  * `score`: *The HADDOCK score (arbitrary units)*
  * `irmsd`: *The interface RMSD, calculated over the interfaces the molecules.*
  * `fnat`: *The fraction of native contacts.*
  * `lrmsd`: *The ligand RMSD, calculated on the ligand after fitting on the receptor (1st component).*
  * `ilrmsd`: *The interface-ligand RMSD, calculated over the interface of the ligand after fitting on the interface of the receptor (more relevant for small ligands for example).*
  * `dockq`: *The DockQ score, which is a combination of irmsd, lrmsd and fnat and provides a continuous scale between 1 (exactly equal to reference) and 0.*

Various other terms are also reported including:

  * `bsa`: *the buried surface area (in squared angstroms).*
  * `elec`: *the intermolecular electrostatic energy.*
  * `rmsdmatrix`: *Generates the pairwisw RMSD matrix for all models to asses structural similarity.*
  * `vdw`: *The intermolecular van der Waals energy.*
  * `desolv`: *The desolvation energy.*
  * various intramolecular covalent energy terms, e.g. bond, angle, dihedral and improper.

The iRMSD, lRMSD and Fnat metrics are the ones used in the blind protein-protein prediction experiment CAPRI (Critical PRediction of Interactions).

In CAPRI the quality of a model is defined as (for protein-protein complexes):

  * **acceptable model:** i-RMSD < 4Å or l-RMSD<10Å and Fnat > 0.1 (or DockQ > 0.23)
  * **medium quality model:** i-RMSD < 2Å or l-RMSD<5Å and Fnat > 0.3 (or DockQ > 0.49)
  * **high quality model:** i-RMSD < 1Å or l-RMSD<1Å and Fnat > 0.5 (or DockQ > 0.8)

You can use **DockQ**, a [combination of i-RMSD](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0161879){:target="_blank"}, l-RMSD, and Fnat to assess the quality of the models. It corresponds to column 9 in the capri_ss.tsv file. Since DockQ is the column number nine in the caprieval files…

<a class="prompt prompt-question">
What is based on this criterion the quality of the top ranked model listed above (cluster_2_model_1.pdb)?
</a>

In case where the `caprieval` module is called after a clustering step, an additional `capri_clt.tsv` file will be present in the directory. This file contains the cluster ranking and score statistics, averaged over the minimum number of models defined for clustering (4 by default), with their corresponding standard deviations. E.g.:

<pre style="background-color:#DAE4E7">
cluster_rank    cluster_id  n   under_eval  score   score_std  irmsd   irmsd_std   fnat   fnat_std   lrmsd   lrmsd_std  dockq   dockq_std  ilrmsd  ilrmsd_std  rmsd    rmsd_std    air air_std bsa bsa_std desolv  desolv_std  elec    elec_std    total   total_std   vdw vdw_std caprieval_rank
          1       2       4       -       -92.549 2.050   2.115   0.214   0.297   0.112   4.857   0.636   0.463   0.066   4.853   0.614   1.843   0.202   34.342  24.455  1257.575        51.505  -24.472 10.524  -155.630        27.685  -161.673        42.491  -40.385 5.863   1
          2       1       4       -       -86.021 9.942   5.870   0.403   0.078   0.043   14.473  1.568   0.134   0.014   14.477  1.558   4.951   0.365   16.346  17.505  1235.268        123.291 -20.531 7.156   -204.655        33.674  -214.503        49.019  -26.194 9.634   2
          3       3       4       -       -83.784 1.  997   6.213   1.759   0.125   0.044   14.976  4.162   0.158   0.061   14.955  4.177   5.265   1.463   53.286  28.875  1193.743        126.378 -27.998 7.317   -108.220        56.725  -94.405 76.812  -39.470 6.008   3
          4       5       4       -       -80.317 8.413   6.172   0.753   0.141   0.034   15.146  1.935   0.148   0.026   15.148  1.928   5.223   0.630   47.955  19.714  1186.205        105.492 -28.845 3.245   -72.285 36.060  -66.141 39.395  -41.811 4.617   4
          5       6       4       -       -72.185 6.513   8.515   0.057   0.057   0.009   21.768  0.091   0.073   0.003   21.821  0.106   7.217   0.043   12.402  3.527   1133.517        66.538  -6.189  1.700   -135.169        23.515  -162.969        18.713  -40.202 7.728   5
</pre>

In this file you find the cluster rank (which corresponds to the naming of the clusters in the previous `seletop` directory), the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (n) in the cluster and the corresponding statistics (averages + standard deviations). The corresponding cluster PDB files will be found in the preceding `7_seletopclusts` directory.

While these simple text files can be easily checked from the command line already, they might be cumbersome to read. For that reason, we have developed a post-processing analysis that automatically generates html reports for all `caprieval` steps in the workflow. These are located in the respective `analysis/XX_caprieval` directories and can be viewed using your favorite web browser.

### Cluster Statistics

Let us now analyse the docking results. Use for that either your own run or a pre-calculated run provided in the `runs` directory. Go into the `analysis/13_caprieval_analysis` directory of the respective run directory and open in a web browser the `report.html` file. Be patient as this page contains interactive plots that may take some time to generate.

On the top of the page, you will see a table that summarises the cluster statistics (taken from the `capri_clt.tsv` file). The columns (corresponding to the various clusters) are sorted by default on the cluster rank, which is based on the HADDOCK score (found on the 4th row of the table). As this is an interactive table, you can sort it as you wish by using the arrows present in the first column. Simply click on the arrows of the term you want to use to sort the table (and you can sort it in ascending or descending order). A snapshot of this table is shown below:

**Analysis report of step 13_caprieval:**
<figure style="text-align: center;">
  <img src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/Analysis_report.png">
</figure>

You can also view this report online [here](plots/report.html){:target="_blank"}.

Since for this tutorial we have at hand the crystal structure of the complex, we provided it as reference to the `caprieval` modules. This means that the iRMSD, lRMSD, Fnat and DockQ statistics report on the quality of the docked model compared to the reference crystal structure.

### Visualizing the Scores and Their Components
Next to the cluster statistic table shown above, the `report.html` file also contains a variety of plots displaying the HADDOCK score and its components against various CAPRI metrics (i-RMSD, l-RMSD, Fnat, Dock-Q) with a color-coded representation of the clusters. These are interactive plots. A menu on the top right of the first row (you might have to scroll to the right to see it) allows you to zoom in and out in the plots and turn on and off clusters.

<figure style="text-align: center;">
  <img src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/plot_1.png">
</figure>

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>

Finally, the report also shows plots of the cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank):

<figure style="text-align: center;">
  <img src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/newplot-2.png">
</figure>

### Some Single Structure Analysis

Going back to command line analysis, we are providing in the `scripts` directory a simple script that extracts some model statistics for acceptable or better models from the `caprieval` steps. To use it, simply call the script with as argument the run directory you want to analyze, e.g.:

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
Total number of acceptable or better models:  82  out of  999
Total number of medium or better models:      2  out of  999
Total number of high quality models:          0  out of  999
 
First acceptable model - rank:  1  i-RMSD:  2.232  Fnat:  0.271  DockQ:  0.425
First medium model     - rank:  2  i-RMSD:  1.845  Fnat:  0.271  DockQ:  0.491
Best model             - rank:  2  i-RMSD:  1.845  Fnat:  0.271  DockQ:  0.491
==============================================
== runs/run1/04_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  82  out of  999
Total number of medium or better models:      1  out of  999
Total number of high quality models:          0  out of  999
 
First acceptable model - rank:  2  i-RMSD:  3.983  Fnat:  0.167  DockQ:  0.230
First medium model     - rank:  12  i-RMSD:  1.843  Fnat:  0.438  DockQ:  0.551
Best model             - rank:  12  i-RMSD:  1.843  Fnat:  0.438  DockQ:  0.551
==============================================
== runs/run1/06_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  83  out of  999
Total number of medium or better models:      1  out of  999
Total number of high quality models:          0  out of  999
 
First acceptable model - rank:  2  i-RMSD:  2.110  Fnat:  0.375  DockQ:  0.489
First medium model     - rank:  7  i-RMSD:  1.803  Fnat:  0.438  DockQ:  0.559
Best model             - rank:  7  i-RMSD:  1.803  Fnat:  0.438  DockQ:  0.559
==============================================
== runs/run1/08_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  44  out of  200
Total number of medium or better models:      1  out of  200
Total number of high quality models:          0  out of  200
 
First acceptable model - rank:  2  i-RMSD:  2.110  Fnat:  0.375  DockQ:  0.489
First medium model     - rank:  7  i-RMSD:  1.803  Fnat:  0.438  DockQ:  0.559
Best model             - rank:  7  i-RMSD:  1.803  Fnat:  0.438  DockQ:  0.559
==============================================
== runs/run1/11_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  44  out of  198
Total number of medium or better models:      1  out of  198
Total number of high quality models:          0  out of  198
 
First acceptable model - rank:  2  i-RMSD:  2.110  Fnat:  0.375  DockQ:  0.489
First medium model     - rank:  6  i-RMSD:  1.803  Fnat:  0.438  DockQ:  0.559
Best model             - rank:  6  i-RMSD:  1.803  Fnat:  0.438  DockQ:  0.559
==============================================
== runs/run1/13_caprieval/capri_ss.tsv
==============================================
Total number of acceptable or better models:  5  out of  36
Total number of medium or better models:      1  out of  36
Total number of high quality models:          0  out of  36
 
First acceptable model - rank:  2  i-RMSD:  2.110  Fnat:  0.375  DockQ:  0.489
First medium model     - rank:  6  i-RMSD:  1.803  Fnat:  0.438  DockQ:  0.559
Best model             - rank:  6  i-RMSD:  1.803  Fnat:  0.438  DockQ:  0.559
</pre>
</details>
<br>

_**Note**_ that this kind of analysis only makes sense when we know the reference complex and for benchmarking / performance analysis purposes.

<a class="prompt prompt-info">
Look at the single structure statistics provided by the script.
</a>

<a class="prompt prompt-question">
How does the quality of the best model change after flexible refinement? Consider here the various metrics.
</a>

<details style="background-color:#DAE4E7">
  <summary style="font-style:italic">
    <b><i>Answer</i></b> 
    <i class="material-icons">expand_more</i>
  </summary>
  <p>In terms of iRMSD values, we only observe very small differences in the best model. The fraction of native contacts and the DockQ scores are however improving much more after flexible refinement but increases again slightly after final minimisation. All this will of course depend on how different are the bound and unbound conformations and the amount of data used to drive the docking process. In general, from our experience, the more and better data at hand, the larger the conformational changes that can be induced.
  </p>
</details>
<br>

_**Note:**_ A similar script to extract cluster statistics is available in the `scripts` directory as `extract-capri-stats-clt.sh`.

<hr>
<hr>

## Visualisation and Comparison with the Reference Structure

To visualize the models from the top cluster of your favorite run, start PyMOL and load the cluster representatives you want to view, e.g. this could be the top model of cluster 1, 2 or 3, located in `XX_seletopclusts` directory of the run. Precalculated models can be found in the `runs/run2/7_seletopclusts/` directory.

**Visual examination of the best models** is a crucial step. This allows you to check whether the model(s) look as expected, identify any unphysical geometries, and assess whether there is meaningful diversity between clusters. Such inspection often reveals issues or interesting variations that may not be apparent from numerical scores alone.

<a class="prompt prompt-info">
File menu -> Open -> select cluster_2_model_1.pdb
</a>

_**Note**_ that the PDB files are compressed (gzipped) by default at the end of a run. You can decompress those with the `gunzip` command. PyMOL can directly read the gzipped files.

If you want to get an impression of how well-defined a cluster is, repeat this for the best N models you want to view (`cluster_2_model_X.pdb`). Also load the reference structure from the `pdbs` directory, `4G6M-matched.pdb`.

<a class="prompt prompt-info">
File menu -> Open -> select 1YCR.pdb
</a>

Once all files have been loaded, type in the PyMOL command window:

<a class="prompt prompt-pymol">
show cartoon<br>
util.cbc<br>
</a>

Next, **select the peptide sequences** in the viewer or command line and apply coloring for better visualization and understand the direction of the alignment:

<a class="prompt prompt-pymol">
select peptide, (chain B)<br>
spectrum count, rainbow, peptide<br>
</a>

Let us color and then superimpose all models onto the reference structure:
<a class="prompt prompt-pymol">
alignto  1YCR  
</a>

In addition to comparing the top 4 clustered models to the reference, it might be interesting to examine **unclustered models.** Very seldom, good-quality models may not be included in the top clusters. To find unclustered models, navigate to traceback/ directory and open traceback.tsv, find 1st models with no value for cluster column. In this case it’s  emref_890.pdb with 05_emref_rank rank of 4. Feel free to examine this model in PyMOL.

<a class="prompt prompt-question">
How close are the top4 models to the reference? Did HADDOCK do a good job at ranking the best in the top?
</a>

_**Note:**_You can turn on and off a model by clicking on its name in the right panel of the PyMOL window.

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See the overlay of the selected model onto the reference structure </i></b> <i class="material-icons">expand_more</i>
  </summary>
  <i>Top-ranked model of the top cluster (cluster_2_model_1) superimposed onto the reference structure (in yellow).</i>
  <br>
  <figure style="text-align: center;">
    <img width="50%" src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/aligned_structure.png">
  </figure>
<br>
</details>
<br>

<hr>
<hr>

## Conclusion
This tutorial demonstrated the use of **HADDOCK3** for protein–peptide docking, making use of AlphaFold model of the protein, and simulating peptide flexibility indirectly by using an ensemble of idealized input conformations. Active residues on the protein were defined using **ARCTIC-3D** predictions, while the whole peptide was treated as passive due to lack of structural information. HADDOCK3 offers control over the docking workflow through flexible restraint definitions and advanced ensemble handling.
We hope you have enjoyed this tutorial and that you have learned something new. If you have any questions or feedback, please do not hesitate to contact us on the [HADDOCK](https://ask.bioexcel.eu/c/haddock){:target="_blank"} forum.

<hr>
<hr>

## BONUS: How to Use ARCTIC-3D to Predict Active Residues of Protein?

Predicting residues that participate in the binding  is an essential step in integrative docking when no experimental interaction data is available. In this section, we explain how to use [ARCTIC-3D](https://wenmr.science.uu.nl/arctic3d/){:target="_blank"}, a structure-based tool that identifies and clusters interface residues based on homologous protein complexes. These predicted residues are then used as active residues in HADDOCK3.

In this tutorial, the target protein is MDM2_mouse (UniProt ID: P23804) for which no structural information is available. Fortunately, it has a close homolog (i.e. another protein with similar sequence), MDM2_human (UniProt ID: Q00987), with extensive experimental data. This MDM2_human experimental data can be leveraged to gain insights into MDM2_mouse binding - using ARCTIC-3D. 

In a nutshell, ARCTIC-3D will retrieve available on [PDB](https://www.ebi.ac.uk/pdbe/){:target="_blank"} complexes involving input protein, cluster all available interfaces, and output a list of residues that are likely to be present in the binding site of each cluster, along with corresponding probabilities. As different binding interfaces are often associated with different protein functions, it’s a good idea to take these functions into account while clustering. For more details, please refer to the original [publication](https://www.nature.com/articles/s42003-023-05718-w){:target="_blank"}.

<a class="prompt prompt-info">
Go to ARCTIC-3D website and enter the UniProt ID of your reference protein (in our case enter Q00987 - MDM2_human).
</a>
<a class="prompt prompt-info">
Check “Cluster partners by protein function” 
</a>
<a class="prompt prompt-info">
Then click submit. 
</a>

ARCTIC-3D will return a set of clusters representing possible binding surfaces with respect to protein functions. Take a look at the “ARCTIC3D clustering” plot - you’ll see that some amino acids are found in the interfaces of the multiple clusters, e.g. 93-V - clusters 2, 3 and 4, while some residues are found only in a single cluster e.g. 105-R - cluster 2. 

Inspect each of the 4 clusters by clicking on the corresponding tab. Click on the “Load model” to see visual representations of the interfaces. Can you spot a difference?

<a class="prompt prompt-question">
What is the most relevant cluster in our case? Pay attention to the protein function!
</a>
<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See answer</i></b> <i class="material-icons">expand_more</i>
  </summary>
Cluster 4, as p53 binding is one of the dominant functions.
</details>
<br>

Each residue within these clusters is assigned a contact probability score, which is saved in the B-factor column of the output PDB file. These values allow a visual inspection of the predicted interfaces using PyMOL. 

<a class="prompt prompt-info">
Download zip results, decompress… 
</a>

Also, as shown in the Protein Function output, we specifically checked for the presence of "p53 binding" among the top-ranked functional terms. If “p53 binding” does not appear in the top 3–5 functions, then that cluster may not be suitable for your docking setup, even if the contact probabilities appear high. Always cross-check the biological relevance of the predicted partner. 
The list of selected residues should then be extracted and saved.

<a class="prompt prompt-question">
What is the most relevant cluster for your biological system? How many residues exceed the 0.5 probability threshold? 
</a>

After identifying a suitable cluster, we downloaded the corresponding PDB file. ARCTIC-3D encodes contact probabilities in the B-factor column, allowing easy visualization in PyMOL.

<a class="prompt prompt-pymol">
spectrum b, cyan_red
</a>

This command color-codes residues by contact probability (cyan = low, red = high). We selected residues above the 0.5 probability threshold as candidates for active residues.

Do not rely solely on interface probability values. Always validate clusters by checking whether the functional annotation of the binding partner makes sense. For example, “p53 binding” should be explicitly listed in systems involving MDM2. ARCTIC-3D provides both structural and functional filters; using both ensures that your docking setup remains biologically meaningful.

Since our docking model uses mouse MDM2, not the human reference structure, we aligned the two structures in PyMOL to ensure consistent residue mapping.

<a class="prompt prompt-pymol">
align AF_MDM_26_109, 1YCR
</a>

After alignment, we visually transferred the predicted active residues from the ARCTIC-3D output to our own model and recorded them for use in HADDOCK3.

<hr>
<hr>




