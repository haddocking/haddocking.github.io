---
layout: page
title: "Protein-peptide modeling tutorial using a local version of HADDOCK3"
excerpt: "A tutorial describing the use of HADDOCK3 in the low-sampling scenario to model an protein-peptide complex"
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, sampling]
image:
  feature: pages/banner_education-thin.jpg
---

This tutorial demonstrates the use of HADDOCK3 to predict the structure of a protein–peptide complex. 
The workflow makes use of pre-defined restraints (derived computationally from known interfaces of a similar protein), an AlphaFold model of the protein, and an ensemble of idealized peptide conformations.

This tutorial consists of the following sections:

* table of contents
{:toc}

<hr>
<hr>

## Introduction

In this tutorial, we will focus on docking the N-terminal peptide of p53 to the mouse MDM2 protein. 
The tumor suppressor p53 is often referred to as the guardian of the genome because of its central role in preventing tumor development. 
As a transcription factor, it regulates the cell cycle and can induce DNA repair or apoptosis in response to cellular stress. 
MDM2, an E3 ubiquitin ligase, is a key negative regulator of p53: by binding to its N-terminal transactivation domain (TAD) peptide, it inhibits p53 activity and promotes its degradation. 
The p53–MDM2 interaction is therefore of major biological and medical importance.


For the mouse MDM2–p53 system, no experimental structure of the complex is available. 
Modelling such interactions is challenging because protein–peptide docking is generally more difficult than protein–protein docking. 
This is primarily due to the intrinsic flexibility of peptides, which allows them to adopt multiple conformations, complicating prediction of the bound state.


In this tutorial, we will use HADDOCK3 to model the MDM2–p53 complex. 
Docking will be guided by pre-defined restraints derived from known interfaces of the human homolog of MDM2. 
As input structures, we will use an AlphaFold model of mouse MDM2 together with an ensemble of idealized peptide conformations. 
This combination will allow us to sample and predict plausible binding modes for the p53 peptide.
Since no experimentally solved structure is available this complex, the human MDM2–p53 complex will be used as a reference for assessing the docking results (PDB ID: [**1YCR**](https://www.rcsb.org/structure/1YCR){:target="_blank"}).

<figure align="center">
<img width="65%" src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/1ycr_pretty.png">
</figure>

Throughout the tutorial, colored text will be used to refer to questions, instructions, and PyMOL commands:

<a class="prompt prompt-question">This is a question prompt: try answering it!</a>
<a class="prompt prompt-info">This an instruction prompt: follow it!</a>
<a class="prompt prompt-pymol">This is a PyMOL prompt: write this in the PyMOL command line prompt!</a>
<a class="prompt prompt-cmd">This is a Linux prompt: insert the commands in the terminal!</a>

<hr>
<hr>

## Setup/Requirements

In this tutorial we will use the PyMOL molecular visualisation system. If not already installed, download and install PyMOL from [here](https://pymol.org/){:target="_blank"}. You can use your favourite visualisation software instead, but be aware that instructions in this tutorial are provided only for PyMOL.

We assume that you have a working installation of HADDOCK3 on your system. If HADDOCK3 is not pre-installed in your system, you will have to install it. To obtain HADDOCK3, fill the [registration form](https://docs.google.com/forms/d/e/1FAIpQLScDcd0rWtuzJ_4nftkDAHoLVwr1IAVwNJGhbaZdTYZ4vWu25w/viewform?){:target="_blank"}, and then follow the [installation instructions](https://www.bonvinlab.org/haddock3-user-manual/install.html){:target="_blank"} or you can install it through:

```bash
pip install haddock3
```

Further, we are providing pre-processed haddock-compatible PDB and configuration files, as well as pre-computed docking results. Please download and unzip the provided [zip archive](https://surfdrive.surf.nl/files/index.php/s/Io1JF9FYiXz9NTb) and make sure to note the location of the extracted folder on your system. There is also a linux command for it:

<a class="prompt prompt-cmd">
wget https://surfdrive.surf.nl/files/index.php/s/Io1JF9FYiXz9NTb/download -O protein-peptide.zip<br>
unzip protein-peptide.zip
</a>
 
Unzipping the file will create the `protein-peptide` directory, which contains the following directories and files:

* `pdbs`: Contains the pre-processed PDB files, both the docking input, and bound reference.
* `restraints`: Contains the interface information and the correspond restraint files for HADDOCK.
* `runs`: Contains pre-computed docking results for each scenario defined in `workflows` directory, useful for comparison with your own run, or if you prefer to skip the computationally intensive steps.
* `scripts`: Contains two analysis scripts used in this tutorial.
* `workflows`: Contains HADDOCK3 workflow used for the docking.

<hr>
<hr>

## Preparing PDB files for docking

The accuracy of docking results in HADDOCK3 depends heavily on the quality of the input structures. In this section, we will prepare the PDB files of the protein and peptide for docking. The protein model is created using AlphaFold, and multiple conformations of the peptide are generated using [**PyMOL**](https://www.pymol.org){:target="_blank"}. We will use `pdb-tools` to manipulate the structures to make them HADDOCK-ready, e.g. to renumber residues, assign chain IDs and generate ensemble file. By default, `pdb-tools` are being installed on your machine together with haddock3. `pdb-tools` documentation is available [here](http://www.bonvinlab.org/pdb-tools/){:target="_blank"}. 

_**Note:**_ that pdb-tools is also available as a [web service](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"}.

_**Note:**_ Before starting to work on the tutorial, make sure to activate an appropriate virtual environment. If haddock3 was installed using `conda`:

<a class="prompt prompt-cmd">
conda activate haddock3
</a>

For more information about accepted file formats and preparation steps, refer to the [HADDOCK3 user manual – structure requirements](https://www.bonvinlab.org/haddock3-user-manual/structure_requirements.html){:target="_blank"}.

### Preparing the protein structure 

One of the easiest ways to find information about a protein, including its structure, is to explore the [UniProt](https://www.uniprot.org){:target="_blank"} database. 
UniProt provides detailed protein sequence and functional data, including annotations, sequence features, and links to structural information. 

<a class="prompt prompt-info"> Open the UniProt home page (https://www.uniprot.org) and search for "mouse MDM2".
</a>

You should see the entry "P23804 · MDM2_MOUSE". Feel free to take you time and explore the page. 

<a class="prompt prompt-info"> Click on the section ‘Structure’ (left side of the page) or scroll down until you reach it.
</a>

This protein has no experimentally solved 3D structure, only AlphaFold model is available. 
This model model covers the full-length sequence of MDM2, but for docking we only need its p53-binding domain.
This domain corresponds to residues 26 to 109. Check out [Family & Domains](https://www.uniprot.org/uniprotkb/P23804/entry#family_and_domains){:target="_blank"} section of the UniProt to see all other regions of the protein. 
The remaining regions, particularly the disordered one, are known not to interact with the peptide, so it's a good idea remove them, both to make the docking problem easier, and to reduce the computational cost of the docking.

<a class="prompt prompt-info"> Click on the download icon (right end of the yellow ribbon) to obtain this model (file name **AF-P23804-F1-model_v4.pdb**).
</a>
<a class="prompt prompt-info"> Move downloaded model **AF-P23804-F1-model_v4.pdb** to your work directory, e.g. **protein-peptide/**
</a>

To prepare this model for docking, we will: 
1. Keep only the coordinates lines, i.e and remove REMARK and other irrelevant lines (`pdb_keepcoord`),
2. Keep only residues of interest (`pdb_selres`),
3. Assign chain ID (`pdb_chain`), and 
4. Apply pdb-formatting to the file (`pdb_tidy`).

<a class="prompt prompt-cmd">
pdb_keepcoord AF-P23804-F1-model_v4.pdb | pdb_selres -26:109 | pdb_chain -A | pdb_tidy -strict > AF_MDM2_26_109.pdb
</a>

_**Note**_ when working with the experimentally solved structures, preparation algorithm would be different, e.g. we would use 
`pdb_delhetatm` and `pdb_selaltloc`.

_**Note**_ `pdb_tidy` attempts to correct formatting only, e.g. ensure each line is long enough (padded with spaces), not the actual content of the PDB file.   

It's a good practice to verify resulting structure visually using PyMOL. Start PyMOL and load the PDB file as followed:
<a class="prompt prompt-info"> 
File menu -> Open -> select protein-peptide/AF_MDM2_26_109.pdb
</a> 

Feel free to compare this structure with initial AlphaFold model:
<a class="prompt prompt-info"> 
File menu -> Open -> select protein-peptide/AF-P23804-F1-model_v4.pdb <br>
</a> 
And to align two models:
<a class="prompt prompt-pymol">
align AF-P23804-F1-model_v4, AF_MDM2_26_109
</a>

If starting PyMOL directly from the command line, you can load multiple PDB files in one go:

<a class="prompt prompt-cmd">
cd protein-peptide <br>
pymol AF_MDM2_26_109.pdb AF-P23804-F1-model_v4.pdb
</a>

### Preparing peptide structure 

When modelling peptides with no experimental structure available, a common approach is to perform a molecular dynamics (MD) simulation and cluster the trajectory to capture the peptide’s conformational variability. 
This process is computationally expensive and can be challenging in the absence of MD experience. 
A simpler alternative is to generate several idealized peptide conformations. 
While less robust, this approach still indirectly accounts for peptide's flexibility to some degree, and that can be just enough to build a model of acceptable quality.


The sequence of interest (residues 18-32 of the p53_mouse) is: 
<pre style="background-color:#DAE4E7">
SQETFSGLWKLLPPE
</pre>

_**Note**_ this sequence can be found on the UniProt page for `P02340 · P53_MOUSE`, under the 'Structure' section.  

We will generate three idealized peptide conformations: α-helix, β-sheet, and polyproline II (ppII). 
This can be done using PyMOL’s built-in fab command. To see a usage example: 

<a class="prompt prompt-info">Open PyMOL
</a>
<a class="prompt prompt-pymol"> help fab
</a>

Generate all 3 conformations:
<a class="prompt prompt-pymol">
fab SQETFSGLWKLLPPE, peptide_helix, ss=1 <br>
fab SQETFSGLWKLLPPE, peptide_sheet, ss=2 <br>
fab SQETFSGLWKLLPPE, peptide_ppii, ss=0 <br>
</a>

You can save each of them either using PyMOL command line (remember to move `peptide_helix.pdb` to your work directory):
<a class="prompt prompt-pymol">
save peptide_helix.pdb, peptide_helix
</a>
Or, alternatively:
<a class="prompt prompt-info"> File menu -> Export Structure... -> Export Molecule... -> Selection "peptide_helix" -> Save -> as PDB
</a>

Once all 3 PDB files are saved in your work directory, save them as a single ensemble PDB (`pdb-mkensemble`) and assign chain B (`pdb_chain`):
<a class="prompt prompt-cmd">
pdb_mkensemble peptide_helix.pdb peptide_sheet.pdb peptide_ppii.pdb | pdb_chain -B | pdb_tidy -strict > peptide_ens.pdb
</a>

To quickly inspect the contents of the generated ensemble, you can look at the header of the file with:

<a class="prompt prompt-cmd">
head peptide_ens.pdb
</a>

<hr>
<hr>

## Defining restraints for docking

HADDOCK relies on restraints to guide the sampling process during docking. 
Several types of restraints can be defined, including unambiguous and ambiguous distance restraints (AIRs). 
These restraints are specified using [CNS (Crystallography & NMR System)](https://cns-online.org/v1.3/){:target="_blank"} syntax, which defines two atom selections and a distance range that must be satisfied. 
If a restraint is not fulfilled, a penalty is applied to the HADDOCK scoring function, lowering the rank of the model that violate the restraints.

To simplify, restraints are defined by specifying two types of residue selections, active and passive, together with a distance range that must be satisfied.
**Active** residues are those known to be present in the interface and solvent accessible. 
If an active residues is not in the interface of a model, then energetic penalty is applied.
**Passive** residues are typically all solvent-accessible surface neighbors of active residues, or other atoms that may plausibly be involved in the interaction. 
Yet if a passive residue is not part of the interface - no penalty is applied. 

A distance restraint is then expressed using CNS syntax as follows:
```bash
assign (selection_1) (selection_2) target_distance, lower_margin, upper_margin
```
The allowed range for the distance is then:
```bash
target_distance - lower_margin  ≤  distance  ≤  target_distance + upper_margin
```

Selections can be customized using keywords such as `segid` (chain ID), `resid` (residue number), and `name` (atom name). 
These can be combined with logical operators AND, OR to construct more complex definitions. 
Please refer for that to the [online CNS manual](http://cns-online.org/v1.3/){:target="_blank"} for more info.


AIRs file (`.tbl`) can be generated using the `haddock3-restraints` command line tool (installed with haddock3) or a version [web version](https://rascar.science.uu.nl/haddock-restraints){:target="_blank"}. 
We will explain how to use this tool shortly, but first we need to identify which residues participate in the interaction - both active and passive.

### Defining active residues for protein

[ARCTIC-3D](https://rascar.science.uu.nl/arctic3d/){:target="_blank"} is a data-mining tool that clusters all known interfaces of a protein, grouping similar interaction sites into residue sets that are likely to participate in binding.
For mouse MDM2, no structural information is currently available, however, such data exists for its human homolog.
To define plausible active residues in mouse MDM2, we applied ARCTIC-3D to the human protein and transferred the results onto mouse variant.
Resulting residues were filtered based on their solvent accessibility:
<pre style="background-color:#DAE4E7"> 54 55 58 59 62 67 72 73 93 94 100 
</pre>

For more details, take a look at the bonus section: [How to use ARCTIC-3D?](#bonus-how-to-use-arctic-3d-to-predict-interface-residues)

Let's visualize predicted active residues on the protein structure we prepared:
<a class="prompt prompt-info">Open PyMOL <br>
File menu -> Open -> select protein-peptide/AF_MDM2_26_109.pdb
</a> 
<a class="prompt prompt-pymol">
color green <br>
show surface <br>
select active, (resid 54+55+58+59+62+67+72+73+93+94+100) <br>
color red, active <br>
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Click to see mouse MDM2 is surface representation with active residues highlighted in red</i></b> <i class="material-icons">expand_more</i>
  </summary>
  <br>
  <figure style="text-align: center;">
    <img width="70%" src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/active-prot.png">
  </figure>
<br>
</details>
<br>


### Defining passive residues for peptide
Since no experimental data or reliable predictions are available to identify which peptide residues are directly involved in the interface, we do not define any active residues for the peptide. Instead, we assign all peptide residues as passive, allowing HADDOCK to explore possible interaction sites during docking:
<pre style="background-color:#DAE4E7"> 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
</pre>


### Using haddock3-restraints to generate restraint file 

To generate AIRs with `haddock3-restraints`, you need to use its sub-option `active_passive_to_ambig` and provide an `.act-pass` file that lists the active and/or passive residues for each docking partner. This file has the following syntax: 
- Active residues are written on the first line, separated by spaces.
- Passive residues are written on the second line, also separated by spaces.
If no active residues are defined, the first line should remain empty. The same applies to the second line if no passive residues are used.

In our case, this is the file for MDM2, `protein-AR3D-active.act-pass`:
```bash
54 55 58 59 62 67 72 73 93 94 100

```
And the file for p53, `peptide-ens-passive.act-pass`:
```bash

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
```
Create these files manually, or access pre-made ones in `restraints/`.


This files can then be used as input to `haddock3-restraints active_passive_to_ambig` to generate the restraint file:

<a class="prompt prompt-cmd">
haddock3-restraints active_passive_to_ambig protein-AR3D-active.act-pass peptide-ens-passive.act-pass > protein-peptide_ambig.tbl
</a> 

_**Note**_ that _passive_ residues on partner 1 should only be defined if _active_ residues have been specified on partner 2, and vice versa. 

Typically, active residues are complemented by nearby passive residues on the same molecule to account for uncertainties in the binding site definition. But if there's no active residues on the partner 2 - passive residues of partner 1 have nothing to interact with. In this tutorial, active residues are defined only for MDM2, while no active residues are defined for the peptide. Thus, we only assign the peptide residues as passive.

### Restraints validation

After generating `protein-peptide_ambig.tbl`, one can validate the syntax of this file using:

<a class="prompt prompt-cmd">
haddock3-restraints validate_tbl protein-peptide_ambig.tbl \-\-silent
</a>
If the file is valid, there will be no output.

_**Note:**_ This command checks only the file’s formatting, not the biological correctness or content of the restraints.

<hr>
<hr>

## Setting up the docking with HADDOCK3

Having now all the required input files and restraints, we can proceed with the docking setup!

### HADDOCK3 workflow definition

The first step is to create a HADDOCK3 configuration file that will define the docking workflow. We will follow a classic HADDOCK workflow that include topology generation, rigid-body minimization, semi-flexible interface refinement, and final refinement, followed by model selection, clustering, and evaluation. 
We will include multiple evaluation instances (`caprieval` module) to compare models to either the best scoring model (if no reference is given) or a reference structure, which in our case we have at hand. This will allow us to assess the performance of the protocol. 

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


The configuration file can be found in `workflow/protein_peptide_docking.cfg` and is as follows:

{% highlight toml %}
 # ============================================
# Protein–Peptide Docking in HADDOCK3
# ============================================

# Output directory
run_dir = "runs/run1"

# Compute mode and resources
mode = "local"
# HADDOCK will use maximum of 40 cores, or as many, as available on the system
ncores = 40

# Post-processing
postprocess = true
clean = true

# Input files
molecules = [
   "pdbs/AF_MDM2_26_109.pdb",    # Protein
   "pdbs/peptide_ens.pdb"        # Peptide
]

# ============================================
# Workflow
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
clust_cutoff = 5
plot_matrix = true

[caprieval]
reference_fname = "pdbs/1YCR.pdb"

[seletopclusts]
# Selection of the top 4 best scoring complexes from each cluster
top_models = 4

[caprieval]
reference_fname = "pdbs/1YCR.pdb"

{% endhighlight %}

You might've noticed that some of the modules do not have any parameters defined. In this case, HADDOCK will use default values, which can be displayed per module. For example, to see all parameters for `clustrmsd`, type:
<a class="prompt prompt-cmd">
haddock3-cfg -m clustrmsd
</a>


This workflow is ready-to-run, and can be executed as-is, using pre-made PDB and restraint files. To use your own files, make sure you provide correct relative or absolute path for each file used during the run (`molecules`, `ambig_fname` and `reference_fname`). 
If you are using your own reference, make sure the PDB file is adequately preprocessed.

### Running HADDOCK3

To run the docking (in `local` mode), open the terminal, activate your haddock3 environment, navigate to `protein-pepitde/` and execute: 

<a class="prompt prompt-cmd">
haddock3 workflows/protein_peptide_docking.cfg
</a>

In this case docking log will appear on the screen. Alternative, you can run the docking in the background and save output log to a file, e.g. `haddock.log`, and any kind of error message to `haddock.err`:

<a class="prompt prompt-cmd">
haddock3 ./workflows/protein_peptide_docking.cfg > haddock.log 2> haddock.err
</a>


On a Max OSX M2 processor using 8 cores the full workflow completes in about 2h10m55s. 
<a class="prompt prompt-info">
Pre-computed results are available in **runs/run1/**
</a>

### Best practices in protein–peptide docking (and tutorial choices)

For optimal peptide docking with HADDOCK, the following settings are recommended:
2. In `flexref`, set `mdsteps_cool1` to 2000 (default: 500);
1. In `flexref`, set `mdsteps_rigid` to 2000 (default: 500);
3. In `flexref`, set `mdsteps_cool2` to 4000 (default: 500);
4. In `flexref`, set `mdsteps_cool3` to 4000 (default: 500);
5. Use `clustrmsd` for clustering instead of the defailt `clustfcc` and 
6. In `clustrmsd`, set `clust_cutoff` to 5 (default: 7.5).

Additionally, when dealing with an ensemble docking with HADDOCK, one should consider increasing the number of models to be sampled (`rigidbody` module, parameter `sampling`) with respect to the number of ensemble conformers. 
HADDOCK distributes the sampling evenly across all possible combinations of input conformers.
If you set `sampling = X` and provide an input ensemble of `n` peptide conformers and `m` protein conformers, each peptide–protein pair will be sampled `X/(n·m)` times, minus rounding error.
E.g. with `sampling = 1000`, 3 peptide conformers and 1 protein conformer, HADDOCK will generate a total of 999 models, with each protein–peptide conformer combination sampled 1000/(3·1) = 333.33(3) ≈ 333 times. 


On the contrary, both increasing `sampling` and `mdsteps_` parameters will lead to the heafty increase of the computational resourses required. 
To balance efficiency and accuracy in this tutorial, we keep the best-practice settings for clustering but chose not to increase sampling or MD step counts.
Despite these simplifications, the use of reliable restraints and asseptable input PDBs ensures that the docking still produces meaningful models.

_**Note**_ that pre-computed best-practice run - with all recommended settings applied - can be found in `runs/run_bp/`.


<hr>
<hr>

## Analysis of docking results

Once your run has completed (or oncw you open precomputed `runs/run1/`), inspect the content of the resulting directory. You will find the various steps (modules) of the defined workflow numbered sequentially:

{% highlight shell %}
> ls runs/
  00_topoaa/
  01_rigidbody/
  02_caprieval/
  03_flexref/
  04_caprieval/
  05_emref/
  06_caprieval/
  07_seletop/
  08_caprieval/
  09_rmsdmatrix/
  10_clustrmsd
  11_caprieval/
  12_seletopclusts/
  13_caprieval/
  analysis/
  data/
  log
  traceback/
{% endhighlight %}

In addition to the various modules defined in the workflow file, you will also find a `log` file (text file) and three additional directories:

  * `data` directory containing the input data (PDB and restraint files) for the various modules, as well as original workflow configuration file;
  * `analysis`directory containing various plots to visualise the results for each caprieval step;
  * `traceback` directory containing the names of the generated models for each step, allowing to trace back a model and it's rank throughout the various stages.

You can find information about the duration of the run at the bottom of the log file. Each sampling/refinement/selection module will contain PDB files - models produced by this module.

For example, the `12_seletopclusts` directory contains the best models from top-ranked clusters. The clusters in that directory are numbered based on their rank, i.e. `cluster_1` refers to the best-ranked cluster. Information about the origin of these files can be found in that directory in the `seletopclusts.txt` file.

### Overview docking run via visual statistics

The quickest way (though not the most detailed) to get an overview of a docking run is through the visual statistics provided by the caprieval module. 
Each caprieval step generates a summary table and multiple plots, bundled into a `report.html` file. 
These reports can be found in the corresponding analysis directories, e.g. `analysis/XX_caprieval_analysis/`. 
This is one of the reasons why the caprieval module is included after almost every step of the workflow.

The content of `report.html` depends on where in the workflow the corresponding caprieval module is placed. 
If it follows an early step, the report describes unclustered models and details 10 top-ranked models (e.g. `analysis/13_caprieval_analysis/report.html`). 
If it follows clustering, the report summarizes clusters and their top models (e.g. `analysis/04_caprieval_analysis/report.html`).

To open `report.html` in a web-browser, [click here](plots/report.html){:target="_blank"}, or type: 
<a class="prompt prompt-cmd">
open run1/analysis/13_caprieval_analysis/report.html
</a>

At the top of the page, you will find a summary table of the cluster statistics (taken from the `13_caprieval/capri_clt.tsv` file). 
By default, the table is sorted by cluster rank, which is based on the HADDOCK score. 
The table is interactive anf you can re-sort columns (corresponding to the various clusters) by clicking the arrow icon (⇄) in the header rows.

<figure style="text-align: center;">
  <img src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/Analysis_report.png">
</figure>

The table reports averages and standard deviations for the HADDOCK score, its components, and evaluation metrics. Some key statistics are:
  * `HADDOCK score`: The HADDOCK score (arbitrary units)
  * `Interface RMSD`: The interface RMSD (irmsd), calculated over the interfaces the molecules.
  * `Fraction of Common Contacts`: The fraction of common contacts (fcc) between given model and top-ranked model. In case reference strucutre is povided, this metric displays the fraction of native contacts (fnat) - between given model and reference strucutre.
  * `Ligand RMSD`: The ligand RMSD (lrmsd), calculated on the ligand after fitting on the receptor (1st component).
  * `Interface-ligand RMSD`: The interface-ligand RMSD (ilrmsd), calculated over the interface of the ligand after fitting on the interface of the receptor (more relevant for small ligands for example).
  * `DockQ`: The DockQ score, which is a combination of irmsd, lrmsd and fnat and provides a continuous scale between 1 (exactly equal to reference) and 0.


The iRMSD, lRMSD and Fnat metrics are the ones used in the blind protein-protein prediction experiment CAPRI (Critical PRediction of Interactions).

In CAPRI the quality of a model is defined as (for protein-protein complexes):

  * **acceptable model:** i-RMSD < 4Å or l-RMSD<10Å and Fnat > 0.1 (or DockQ > 0.23)
  * **medium quality model:** i-RMSD < 2Å or l-RMSD<5Å and Fnat > 0.3 (or DockQ > 0.49)
  * **high quality model:** i-RMSD < 1Å or l-RMSD<1Å and Fnat > 0.5 (or DockQ > 0.8)

<a class="prompt prompt-question">
Examine the table. Does the cluster with the lowest average score has lowest average irmsd?
</a>

Below the table, a variety of plots displaying the HADDOCK score vs its components against various metrics with a color-coded representation of the clusters. These are interactive plots, one can toggle which clusters are displayed, zoom in and out, etc. - using a menu on the top right of the first row (you might have to scroll to the right to see it). 

<figure style="text-align: center;">
  <img src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/models-plots.png">
</figure>

<a class="prompt prompt-info">
Examine the plots - do open report.html in the browser, as images above do not show all the plots. Remember that higher DockQ values and lower iRMSD values correspond to better models.
</a>

Finally, the very bottom plots diplayes the cluster statistics:
<figure style="text-align: center;">
  <img src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/cluster-plots.png">
</figure>

<a class="prompt prompt-question">
Examine report.html for one of the unclustered steps. Are any of the top-10 models as good as cluster_1_model_1 based on their iRMSD?
</a>

### Detailed information about models and clusters

To extract most of the avalilable information about the model(s), one should look at the `XX_caprieval` directories. 
This directory will always contain a `capri_ss.tsv` file, which contains the model names, rankings and statistics, e.g. `11_caprieval/capri_ss.tsv`:

<pre style="background-color:#DAE4E7">
                    model	md5	caprieval_rank	score	    irmsd	fnat	lrmsd	  ilrmsd	dockq	rmsd	cluster_id	cluster_ranking	model-cluster_ranking	air	angles	bonds	bsa	cdih	coup	dani	desolv	dihe	elec	improper	rdcs	rg	sym	total	vdw	vean	xpcs
../05_emref/emref_175.pdb	-	1	-108.487	1.978	0.229	4.403	  4.433	  0.461	1.700	1	1	1	9.126	0.000	0.000	1440.260	0.000	0.000	0.000	-17.7640.000	-333.853	0.000	0.000	0.000	0.000	-349.593	-24.865	0.000	0.000
../05_emref/emref_692.pdb	-	2	-100.478	3.890	0.188	9.510	  9.464	  0.254	3.324	5	2	1	4.749	0.000	0.000	1476.810	0.000	0.000	0.000	-21.4630.000	-164.223	0.000	0.000	0.000	0.000	-206.119	-46.645	0.000	0.000
../05_emref/emref_98.pdb	-	3	-100.226	5.959	0.083	14.636	14.611	0.132	5.034	1	1	2	2.106	0.000	0.000	1174.060	0.000	0.000	0.000	-31.1890.000	-118.077	0.000	0.000	0.000	0.000	-161.604	-45.633	0.000	0.000
../05_emref/emref_292.pdb	-	4	-95.360	  4.446	0.167	10.556	10.589	0.221	3.742	2	3	1	10.580	0.000	0.000	1147.310	0.000	0.000	0.000	-25.872	0.000	-210.751	0.000	0.000	0.000	0.000	-228.566	-28.396	0.000	0.000
../05_emref/emref_505.pdb	-	5	-94.092	  3.799	0.146	9.326	  9.281	  0.245	3.252	5	2	2	35.123	0.000	0.000	1410.450	0.000	0.000	0.000	-19.475	0.000	-103.134	0.000	0.000	0.000	0.000	-125.514	-57.503	0.000	0.000
../05_emref/emref_305.pdb	-	6	-92.845	  5.424	0.062	12.809	12.828	0.146	4.541	2	3	2	8.091	0.000	0.000	1283.300	0.000	0.000	0.000	-7.136	0.000	-231.428	0.000	0.000	0.000	0.000	-263.570	-40.233	0.000	0.000
../05_emref/emref_501.pdb	-	7	-92.499	  6.364	0.167	16.694	16.620	0.142	5.520	9	4	1	38.783	0.000	0.000	1291.390	0.000	0.000	0.000	-20.593	0.000	-192.180	0.000	0.000	0.000	0.000	-190.745	-37.348	0.000	0.000
../05_emref/emref_248.pdb	-	8	-92.432	  2.317	0.229	5.352	  5.367	  0.414	1.988	1	1	3	16.925	0.000	0.000	1376.260	0.000	0.000	0.000	-18.819	0.000	-179.963	0.000	0.000	0.000	0.000	-202.352	-39.313	0.000	0.000
../05_emref/emref_61.pdb	-	9	-91.648	  3.427	0.104	8.856	  8.849	  0.248	2.990	1	1	4	5.463	0.000	0.000	1164.080	0.000	0.000	0.000	-27.465	0.000	-84.313	0.000	0.000	0.000	0.000	-126.716	-47.867	0.000	0.000
...
</pre>


In case where the caprieval module was called after a clustering step, an additional `capri_clt.tsv` file will be present in the directory. This file contains the cluster ranking and score statistics, averaged over the minimum number of models defined for clustering (4 by default), with their corresponding standard deviations, e.g. `11_caprieval/capri_clt.tsv`:

<pre style="background-color:#DAE4E7">
cluster_rank	cluster_id	n	under_eval	score	score_std	irmsd	irmsd_std	fnat	fnat_std	lrmsd	lrmsd_std	dockq	dockq_std	ilrmsd	ilrmsd_std	rmsd	rmsd_std	air	air_std	bsa	bsa_std	desolv	desolv_std	elec	elec_std    	total	total_std	vdw	vdw_std	caprieval_rank
1	1	90	-	-98.198	6.822	3.420	1.561	0.161	0.068	8.312	4.011	0.314	0.131	8.315	3.990	2.928	1.307	8.405	5.510	1288.665	121.768	-23.809	5.685	-179.05195.731	-210.066	84.887	-39.419	8.969	1
2	5	12	-	-87.901	10.237	3.329	0.576	0.182	0.056	8.046	1.507	0.299	0.065	8.010	1.495	2.853	0.486	17.886	11.509	1278.430	172.834	-21.787	6.034	-137.80822.462	-160.262	29.104	-40.340	12.703	2
3	2	29	-	-87.896	6.834	5.759	1.265	0.099	0.050	13.673	3.101	0.155	0.040	13.682	3.075	4.833	1.064	14.920	11.076	1210.532	78.007	-16.600	12.142	-184.88883.105	-205.779	86.544	-35.810	9.490	3
4	9	6	-	-77.482	8.980	6.432	1.325	0.120	0.040	16.392	3.663	0.135	0.037	16.344	3.631	5.516	1.143	24.593	16.023	1092.057	118.002	-24.420	3.408	-92.25458.414	-104.731	52.843	-37.070	2.519	4
5	3	14	-	-76.449	7.822	9.812	0.673	0.094	0.010	25.283	2.176	0.073	0.007	25.240	2.158	8.321	0.597	13.161	15.804	1153.420	99.208	-10.555	4.474	-194.41873.604	-209.584	58.464	-28.326	11.725	5
6	4	14	-	-75.768	8.698	8.656	0.051	0.031	0.010	22.081	0.196	0.063	0.004	22.155	0.181	7.331	0.046	9.422	2.845	1180.285	94.733	-7.799	2.862	-149.28135.997	-178.914	34.066	-39.055	5.437	6
7	7	9	-	-74.858	4.797	6.942	0.582	0.078	0.017	17.108	1.215	0.108	0.015	17.093	1.214	5.891	0.458	25.698	16.927	1160.588	81.306	-19.064	9.579	-127.49268.554	-134.659	79.410	-32.865	8.559	7
8	6	11	-	-63.640	1.862	7.323	0.773	0.042	0.026	19.234	1.937	0.083	0.018	19.289	1.951	6.206	0.656	7.153	3.709	948.450	112.263	-10.060	8.375	-128.485	47.644	-149.931	50.337	-28.598	3.513	8
9	8	6	-	-63.561	3.071	6.482	0.648	0.073	0.056	16.731	1.737	0.111	0.032	16.730	1.735	5.538	0.570	14.238	6.930	1013.990	34.855	-13.123	5.508	-75.58332.708	-98.090	36.421	-36.745	2.992	9
</pre>

In this file you find the cluster rank (which corresponds to the naming of the clusters in the previous `seletop` directory), the cluster ID (which is related to the size of the cluster, 1 being always the largest cluster), the number of models (column `n`) in the cluster and the corresponding statistics (averages + standard deviations). 

These simple text files can be somewhat cumbersome to read "as-is", but they can be easily manipulated using command line. The following commands will extract the best 3 models based on the DockQ score:
<a class="prompt prompt-cmd">
sort -r -k9 run1/02_caprieval/capri_ss.tsv | head -4
</a>


### Performance analysis (when reference is available)

In case a reference structure is available, one may want to analyse the performance of the docking protocol, for example to count how many models of different quality were generated at each step of the workflow.
This can be done with a simple bash script provided in `protein-peptide/scripts/`. 
This script extracts CAPRI statistics per model and reports the number of models of acceptable or better models from each `caprieval` steps. 
To use it, run the script with the path to the run directory you want to analyse as its argument:

<a class="prompt prompt-cmd">
bash ./scripts/extract-capri-stats.sh ./runs/run1
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

<a class="prompt prompt-question">
Look at the single structure statistics. How does the quality of the best model change after flexible refinement? After final energy minimisation?
Consider all 3 metrics. 
</a>

_**Note:**_ To extract similar statistics per cluster, use `scripts/extract-capri-stats-clt.sh`.

<hr>
<hr>


## Visualisation and comparison with the reference structure

It’s time to visualise some of the docking models! This part is not only nice and colorful, but also quite important. 
Model visualisation allows you to check whether the models look as expected, if the clusters well-defined, zoom in on the interface, etc.

To visualize the models from top cluster of your favorite run, start PyMOL and load the cluster representatives you want to view, e.g. this could be the top models from cluster1. These can be found in the `runs/run1/12_seletopclusts/` directory. Each run has a similar directory. Alternatively, in `analysis/XX_caprieval_analysis` you can find `summary.tgz` with either top-models of best clusters (decompress with `tar -xf summary.tgz`), or top-10 models among all unclustered ones. 


<a class="prompt prompt-info">
File menu -> Open -> cluster_1_model_1.pdb
</a>

_**Note**_ that the PDB files are compressed (gzipped) by default at the end of a run. PyMOL can read the gzipped files, but you can decompress those with the `gunzip` command. 

If you want to get an impression of how well-defined a cluster is, repeat this for the best X models you want to view (`cluster_1_model_X.pdb`).

Load the reference structure `1YCR.pdb` from `pdbs/`. 
Alternatively, if reference has been used in caprieval, it can be found in corresponding `run1/data/XX_caprieval/`
<a class="prompt prompt-info">
File menu -> Open -> select 1YCR.pdb
</a>

Once all files have been loaded, display models in cartoon representatin and colour by chain:
<a class="prompt prompt-pymol">
show cartoon<br>
util.cbc<br>
</a>

For proteins and other large molecules, colouring by chains is usually sufficient, as their 3D structure makes it easy to distinguish the N- and C-termini.
However, for small peptides in near-idealised conformations, the structure alone often makes it difficult to tell which terminus is which.
To overcome this, we can color the peptide sequentially, with one terminus in blue and the other in red:
<a class="prompt prompt-pymol">
select (1YCR and chain B)<br>
spectrum count, rainbow, sele <br>
</a>
Repeat for each loaded model. 

Now, to superimpose all models onto the reference structure using both chains:
<a class="prompt prompt-pymol">
alignto 1YCR  
</a>

To maximize the differences you can superimpose all models using a single chain. For example to fit all models on the protein of the reference structure use:
<a class="prompt prompt-pymol">
alignto 1YCR and chain A 
</a>

_**Note:**_ You can hide or display a model by clicking on its name in the right panel of the PyMOL window.

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See the overlay of the selected model onto the reference structure </i></b> <i class="material-icons">expand_more</i>
  </summary>
  <i>Top-ranked model of the top cluster (cluster_1_model_1) superimposed onto the reference structure.</i>
  <br>
  <figure style="text-align: center;">
    <img width="95%" src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/aligned.png">
  </figure>
<br>
</details>
<br>

<hr>
<hr>

## BONUS: How to use ARCTIC-3D to predict interface residues?

ARCTIC-3D, is a tool and a [web-server](https://wenmr.science.uu.nl/arctic3d/){:target="_blank"} for automatic retrieval and clustering of protein–ligand interfaces from available 3D structures. It can be used to predict interface residues, which in turn can be used as active (or passive) residues to guide docking.

Our target complex is the mouse variant of MDM2 binding to p53m for which no structural data are available, as mouse MDM2 in not solved experimentally.
Fortunately, its close homolog, the human MDM2 protein, has been extensively studied experimentally.
This information can be leveraged with ARCTIC-3D to infer likely interface residues for the mouse protein. 

In a nutshell, ARCTIC-3D will retrieve available on [PDB](https://www.ebi.ac.uk/pdbe/){:target="_blank"} complexes involving input protein (idenified via its UniProtID), cluster all available interfaces, and output a list of residues that are likely to be present in the binding site of each cluster, along with corresponding probabilities. As different binding interfaces are often associated with different protein functions, it’s a good idea to take these functions into account while clustering. For more details, please refer to the original [publication](https://www.nature.com/articles/s42003-023-05718-w){:target="_blank"}. 

<a class="prompt prompt-question">
Can you find UniProtID for MDM2_human?
</a>
<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See answer</i></b> <i class="material-icons">expand_more</i>
  </summary>
Q00987
</details>
<br>

<a class="prompt prompt-info">
Open ARCTIC-3D web-server and enter the UniProt_ID of MDM2_human.
</a>
<a class="prompt prompt-info">
Check “Cluster partners by protein function” 
</a>
<a class="prompt prompt-info">
Click on "Submit". 
</a>

In a few seconds or a few minutes, ARCTIC-3D will return a set of clusters representing possible binding surfaces with respect to protein functions. Take a look at the “ARCTIC3D clustering” plot: you’ll see that some amino acids are found in the interfaces of the multiple clusters, e.g. 91-F - clusters 2, 3 and 1, while some residues are found only in a single cluster e.g. 105-R - cluster 3 only. 

_**NOTE**_ this ARCTIC-3D run was performed in September 2025 and thus used strucutes available online at that time.
With the time, new structures of MDM2_human may became available, which may lead to the change in the number and numbering of clusters.
So if you're running ARCTIC-3D in the future, don't be surprised if the output looks a bit different! 

<figure align="center">
<img width="100%" src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/arctic-plot.png">
</figure>

Inspect each of the 3 clusters by clicking on the corresponding tab. Click on the “Load model” to see visual representations of the interfaces. Can you spot a difference?

<a class="prompt prompt-question">
What is the most relevant cluster in our case? Pay attention to the protein function!
</a>
<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See answer</i></b> <i class="material-icons">expand_more</i>
  </summary>
Cluster 2, as p53 binding is one of the dominant functions.
  <br>
  <figure style="text-align: center;">
    <img width="100%" src="/education/HADDOCK3/HADDOCK3-protein-peptide/png/arctic-prot-func.png">
  </figure>
</details>
<br>

Each residue within these clusters is assigned a contact probability score, which is saved in the B-factor column of the output PDB file. These values allow a visual inspection of the predicted interfaces using PyMOL. 

<a class="prompt prompt-info">
Download zip results, decompress **output.zip**. Then load PDB model of the most appropriate cluster to PyMOL
</a>

To color model by values of B-factor column, cyan for low vlues and red for high values: 
<a class="prompt prompt-pymol">
spectrum b, cyan_red
</a>


We used probability threshold of 0.5 to select candidates for active residues, which resulted in the following list: 
```bash
72 62 67 93 58 96 54 61 73 57 100 94 75 99 55
```
Since our docking input is a mouse MDM2 model, not the human reference structure, we should align both structures in PyMOL and map residues from ARCTIC-3D stucutre to mouse MDM2 model (`AF_MDM2_26_109.pdb`). 

As you may remember from the definition of active residues, they should be solvent accessible. 
Relative solvent accessibility (RSA) measures the percentage of a residue’s surface that is exposed to solvent, typically water. 
It reflects how accessible a residue is to potential binding partners.
Buried residues are unlikely to contribute directly to binding, as they are often simply unreachabe for the docking partner.
Default RSA threshlod for active residues is 40%; for passive - 15%. Therse values are a suggestions, not a hard rule. 

In our case, we chose a cutoff of 25% for the active residues.
Many tools are available for calculating RSA, e.g. PyMOL’s built-in function `get_sasa_relative`, the Biopython module `Bio.PDB.SASA` etc.
We used [FreeSASA](http://freesasa.github.io/){:target="_blank"}, an open-source tool that computes RSA and related solvent accessibility values directly from PDB structures.

After installing FreeSASA, you can run it with the following command:  
<a class="prompt prompt-cmd">
freesasa --format=rsa AF_MDM2_26_109.pdb
</a>
<details style="background-color:#DAE4E7">
<summary>
<i>View freesasa output</i> <i class="material-icons">expand_more</i>
 </summary>
 The column of interest is `All-atoms`, sub-column `REL`
<pre>
REM  FreeSASA 2.1.2
REM  Absolute and relative SASAs for AF_MDM2_26_109.pdb
REM  Atomic radii and reference values for relative SASA: ProtOr
REM  Chains: A
REM  Algorithm: Lee & Richards
REM  Probe-radius: 1.40
REM  Slices: 20
REM RES _ NUM      All-atoms   Total-Side   Main-Chain    Non-polar    All polar
REM                ABS   REL    ABS   REL    ABS   REL    ABS   REL    ABS   REL
RES PRO A  30    29.26  21.3   5.87   5.4  23.39  85.0   5.87   4.8  23.39 145.4
RES LYS A  31    87.65  42.8  87.13  53.5   0.52   1.2  45.91  41.3  41.74  44.5
RES PRO A  32   109.77  80.0 102.81  93.7   6.96  25.3 104.24  86.1   5.53  34.4
RES LEU A  33    95.62  53.3  95.57  68.4   0.05   0.1  95.57  67.1   0.05   0.1
RES LEU A  34     0.00   0.0   0.00   0.0   0.00   0.0   0.00   0.0   0.00   0.0
RES LEU A  35    32.31  18.0  32.31  23.1   0.00   0.0  32.31  22.7   0.00   0.0
RES LYS A  36   131.57  64.2 122.34  75.1   9.23  22.0  79.53  71.6  52.04  55.4
RES LEU A  37     0.00   0.0   0.00   0.0   0.00   0.0   0.00   0.0   0.00   0.0
RES LEU A  38     0.00   0.0   0.00   0.0   0.00   0.0   0.00   0.0   0.00   0.0
RES LYS A  39    87.79  42.8  69.98  42.9  17.81  42.4  45.42  40.9  42.37  45.1
...
</pre>
</details>
<br>



<hr>
<hr>

## Congratulations!
You’ve reached the end of this basic protein-peptide docking tutorial! We hope it has been informative and helps you get started with your own docking projects.
What more protein-peptide docking workflow examples, this time with explicit flexibility? Check [this page](https://www.bonvinlab.org/haddock3-user-manual/docking_scenarios/prot-peptide.html){:target="_blank"}.