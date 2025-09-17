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
wget https://surfdrive.surf.nl/files/index.php/s/Io1JF9FYiXz9NTb -O protein-peptide.zip<br>
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
This model model covers the full-length sequence of MDM2, but for docking we only need a its p53-binding domain.
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
File menu -> Open -> select protein-peptide/AF-P23804-F1-model_v4.pdb
</a> 

If starting PyMOL directly from the command line you can use instead:
<a class="prompt prompt-cmd">
cd protein-peptide <br>
pymol AF_MDM2_26_109.pdb AF-P23804-F1-model_v4.pdb
</a>

### Preparing peptide structure 

When modelling peptides with no experimental structure available, a common approach is to perform a molecular dynamics (MD) simulation to capture the peptide’s conformational variability. 
This process is computationally expensive and can be challenging in the absence of MD experience. 
A simpler alternative is to generate several idealized peptide conformations. 
While less robust, this approach still indirectly accounts for peptide's flexibility to some degree, and that can be just enough to build a model of acceptable quality.


The sequence of interest (residues 18-32 of the p53_mouse) is: 
<pre style="background-color:#DAE4E7">
SQETFSGLWKLLPPE
</pre>

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
pdb_mkensemble peptide_helix.pdb peptide_sheet.pdb peptide_ppii.pdb | pdb_chain -B | pdb_tidy -strict > peptide_ensemble.pdb
</a>

To quickly inspect the contents of the generated ensemble, you can look at the header of the file with:

<a class="prompt prompt-cmd">
head peptide_ensemble.pdb
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

For more details, take a look at the bonus section: [How to use ARCTIC-3D?](#bonus-how-to-use-arctic-3d-to-predict-active-residues-of-protein)

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

### Restraints Validation
After generating `protein-peptide_ambig.tbl`, one can validate the syntax of this file using:

<a class="prompt prompt-cmd">
haddock3-restraints validate_tbl protein-peptide_ambig.tbl --silent
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


To run the docking, open the terminal, navigate to `protein-pepitde/` and execute: 
<a class="prompt prompt-cmd">
haddock3 workflows/protein_peptide_docking.cfg
</a>

In this case docking log will appear on the screen. Alternative, you can run the docking in the background and save output log to a file, e.g. `haddock.log`, and any kind of error message to `haddock.err`:

<a class="prompt prompt-cmd">
haddock3 ./workflows/protein_peptide_docking.cfg > haddock.log 2> haddock.err
</a>

**THE MATERIAL BELOW THIS POINT HAS NOT BEEN VERIFIED**



### Best Practice of Protein-Peptide Docking

HADDOCK will use default parameter values for each module, unless different values is defined in the workflow. 
Optimal settings for peptide docking are:
1. Number of sampling models in `rididbody` should be increased by the number of input conformers of the peptide.
2. Number of MD steps in `flexref` for rigid body high temperature TAD: mdsteps_rigid = 2000 (default is 500)
3. Number of MD steps in `flexref` during first rigid body cooling stage:	mdsteps_cool1 = 2000 (default is 500)
4. Number of MD steps in `flexref` during second cooling stage with flexible side-chains at interface:	mdsteps_cool2	=	4000 (default is 500)
5. Number of MD steps in `flexref` during third cooling stage with fully flexible interface: mdsteps_cool3 = 4000 (default is 500)
6. Clustering method: `clustrmsd` (default clustering method is `clustfcc`);
7. Cutoff for clustering: clust_cutoff= 5 (default value is 7.5)

However, increasing number of MD steps in `fexref` will increase computational significantly, as well as increasing number of models to sample. Thus, for the purpose of this tutorial, we will keep default number models to be sampled, as well as number of MD steps, but use `clustrmsd` with optimal cutoff. 

_**Note**_ that pre-computed best-practice run can be found in `runs/run_bp`.


To optimize performance while maintaining sampling quality, we set `sampling = 1000` in the `rigidbody` stage and selected the top 200 models (`select = 200`) for downstream refinement (default values). Clustering was performed using the RMSD metric, and the top 4 models from each cluster were selected.

Model evaluation (`aprieval`) was performed using a reference structure (`pdbs/1YCR.pdb`) to assess structural similarity via CAPRI metrics such as i-RMSD, l-RMSD, and Fnat. If reference_fname parameter would not be defined, then the same metrics would’ve been calculated using lowest-score structure. 

On a Max OSX M2 processor using 8 cores the full workflow completes in about 2h10m55s.

### Sampling Strategy Consideration

We used the default sampling size of **1000 models**, which corresponds to HADDOCK’s default behavior. In our case, this value was applied across all input conformers in the peptide ensemble.

_**Note:**_ HADDOCK distributes the sampling across each input conformer. This means that if you set `sampling = X` and provide an ensemble of n peptide conformers, the total number of models generated will still be X, but each conformer will be sampled X / n times.For example, with `sampling = 300` and 3 peptide conformations, a total of 300 models will be generated, with each conformation sampled **300 / 3 = 100** times.

Although ideally one should aim for 1000 models per peptide conformation (i.e., sampling = 3000), such computations are rather heavy for 8 cores  . Given that our restraints were defined with high confidence, this reduces sampling deemed a reasonable compromise. A full-size precomputed run with sampling=3000 is available in runs/name.

In a real-case docking scenario, especially when restraint quality is uncertain it is advisable to increase the sampling accordingly, if computational resources allow. However, for very large ensembles (e.g., MD trajectory ), **prior clustering** to reduce ensemble size is highly recommended before attempting full-scale sampling.



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
../12_seletopclusts/cluster_1_model_1.pdb       -       1       -108.487        1.978   0.229   4.403   4.433   0.461   1.700   1       1       1       9.126   0.000   0.000   1440.260        0.000   0.000   0.000   -17.764 0.000   -333.853        0.000   0.000   0.000   0.000       -349.593        -24.865 0.000   0.000
../12_seletopclusts/cluster_2_model_1.pdb       -       2       -100.478        3.890   0.188   9.510   9.464   0.254   3.324   5       2       1       4.749   0.000   0.000   1476.810        0.000   0.000   0.000   -21.463 0.000   -164.223        0.000   0.000   0.000   0.000       -206.119        -46.645 0.000   0.000
../12_seletopclusts/cluster_1_model_2.pdb       -       3       -100.226        5.959   0.083   14.636  14.611  0.132   5.034   1       1       2       2.106   0.000   0.000   1174.060        0.000   0.000   0.000   -31.189 0.000   -118.077        0.000   0.000   0.000   0.000       -161.604        -45.633 0.000   0.000
../12_seletopclusts/cluster_3_model_1.pdb       -       4       -95.360 4.446   0.167   10.556  10.589  0.221   3.742   2       3       1       10.580  0.000   0.000   1147.310        0.000   0.000   0.000   -25.872 0.000   -210.751        0.000   0.000   0.000   0.000   -228.566    -28.396 0.000   0.000
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
What is based on this criterion the quality of the top ranked model listed above (cluster_1_model_1.pdb)?
</a>

In case where the `caprieval` module is called after a clustering step, an additional `capri_clt.tsv` file will be present in the directory. This file contains the cluster ranking and score statistics, averaged over the minimum number of models defined for clustering (4 by default), with their corresponding standard deviations. E.g.:

<pre style="background-color:#DAE4E7">
cluster_rank    cluster_id  n   under_eval  score   score_std  irmsd   irmsd_std   fnat   fnat_std   lrmsd   lrmsd_std  dockq   dockq_std  ilrmsd  ilrmsd_std  rmsd    rmsd_std    air air_std bsa bsa_std desolv  desolv_std  elec    elec_std    total   total_std   vdw vdw_std caprieval_rank
          1       1       4       -       -98.198 6.822   3.420   1.561   0.161   0.068   8.312   4.011   0.314   0.131   8.315   3.990   2.928   1.307   8.405   5.510   1288.665        121.768 -23.809 5.685   -179.051        95.731  -210.066        84.887  -39.419 8.969   1
          2       5       4       -       -87.901 10.237  3.329   0.576   0.182   0.056   8.046   1.507   0.299   0.065   8.010   1.495   2.853   0.486   17.886  11.509  1278.430        172.834 -21.787 6.034   -137.808        22.462  -160.262        29.104  -40.340 12.703  2
          3       2       4       -       -87.896 6.834   5.759   1.265   0.099   0.050   13.673  3.101   0.155   0.040   13.682  3.075   4.833   1.064   14.920  11.076  1210.532        78.007  -16.600 12.142  -184.888        83.105  -205.779        86.544  -35.810 9.490   3

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
File menu -> Open -> select cluster_1_model_1.pdb
</a>

_**Note**_ that the PDB files are compressed (gzipped) by default at the end of a run. You can decompress those with the `gunzip` command. PyMOL can directly read the gzipped files.

If you want to get an impression of how well-defined a cluster is, repeat this for the best N models you want to view (`cluster_1_model_X.pdb`). Also load the reference structure from the `pdbs` directory, `4G6M-matched.pdb`.

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
  <i>Top-ranked model of the top cluster (cluster_1_model_1) superimposed onto the reference structure (in yellow).</i>
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

### SASA: Solvent Accessible Surface Area

In addition to ARCTIC-3D predictions, we further validated candidate residues by calculating their solvent accessible surface area (SASA). SASA measures the surface of a biomolecule that is accessible to a solvent (e.g. water), which is directly related to how exposed a residue is. Buried residues, with low SASA, are unlikely to contribute directly to binding, while surface-exposed residues, with higher SASA, are typically more relevant in protein–protein or protein–peptide interactions.

Both active and passive residues should have a relative solvent accessibility (RSA) of at least 15% to be considered in HADDOCK docking setups.

For calculating SASA, we used [FreeSASA](http://freesasa.github.io/){:target="_blank"}, an open-source tool that computes SASA values directly from PDB structures. By applying this criterion, we filtered ARCTIC-3D predicted residues and retained only those with sufficient solvent exposure for docking.

<hr>
<hr>




