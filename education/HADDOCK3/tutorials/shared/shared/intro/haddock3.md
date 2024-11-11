
## A brief introduction to HADDOCK3

HADDOCK3 is the next generation integrative modelling software in the long-lasting HADDOCK project.
It represents a complete rethinking and rewriting of the HADDOCK2.X series, implementing a new way to interact with HADDOCK and offering new features to users who can now define custom workflows.

In the previous HADDOCK2.x versions, users had access to a highly parameterisable yet rigid simulation pipeline composed of three steps:
`rigid-body docking (it0)`, `semi-flexible refinement (it1)`, and `final refinement (itw)`.

<figure style="text-align: center;">
<img width="75%" src="../images/HADDOCK2-stages.png">
</figure>

In HADDOCK3, users have the freedom to configure docking workflows into
functional pipelines by combining the different HADDOCK3 modules, thus
adapting the workflows to their projects.
HADDOCK3 has therefore developed to truthfully work like a puzzle of many pieces (simulation modules) that users can
combine freely.
To this end, the “old” HADDOCK machinery has been modularized, and several new modules added, including third-party software additions.
As a result, the modularization achieved in HADDOCK3 allows users to duplicate steps within one workflow (e.g., to repeat twice the `it1` stage of the HADDOCK2.x rigid workflow).

Note that, for simplification purposes, at this time, not all functionalities of HADDOCK2.x have been ported to HADDOCK3, which does not (yet) support NMR RDC, PCS and diffusion anisotropy restraints, cryo-EM restraints and coarse-graining.
Any type of information that can be converted into ambiguous interaction restraints can, however, be used in HADDOCK3, which also supports the *ab initio* docking modes of HADDOCK.

<figure style="text-align: center;">
<img width="75%" src="../images/HADDOCK3-workflow-scheme.png">
</figure>

To keep HADDOCK3 modules organized, we catalogued them into several categories.
However, there are no constraints on piping modules of different categories.

The main module categories are "topology", "sampling", "refinement", "scoring", and "analysis".
There is no limit to how many modules can belong to a category.
Modules are added as developed, and new categories will be created if/when needed.
You can access the HADDOCK3 documentation page for the list of all categories and modules.
Below is a summary of the available modules:

* **Topology modules**
    * `topoaa`: *generates the all-atom topologies for the CNS engine.*
* **Sampling modules**
    * `rigidbody`: *Rigid body energy minimization with CNS (`it0` in haddock2.x).*
    * `lightdock`: *Third-party glow-worm swam optimization docking software.*
* **Model refinement modules**
    * `flexref`: *Semi-flexible refinement using a simulated annealing protocol through molecular dynamics simulations in torsion angle space (`it1` in haddock2.x).*
    * `emref`: *Refinement by energy minimisation (`itw` EM only in haddock2.4).*
    * `mdref`: *Refinement by a short molecular dynamics simulation in explicit solvent (`itw` in haddock2.X).*
* **Scoring modules**
    * `emscoring`: *scoring of a complex performing a short EM (builds the topology and all missing atoms).*
    * `mdscoring`: *scoring of a complex performing a short MD in explicit solvent + EM (builds the topology and all missing atoms).*
* **Analysis modules**
    * `alascan`: *Performs a systematic (or user-define) alanine scanning mutagenesis of interface residues.*
    * `caprieval`: *Calculates CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ) with respect to the top-scoring model or reference structure if provided.*
    * `clustfcc`: *Clusters models based on the fraction of common contacts (FCC)*
    * `clustrmsd`: *Clusters models based on pairwise RMSD matrix calculated with the `rmsdmatrix` module.*
    * `contactmap`: *Generate contact matrices of both intra- and intermolecular contacts and a chordchart of intermolecular contacts.*
    * `rmsdmatrix`: *Calculates the pairwise RMSD matrix between all the models generated in the previous step.*
    * `ilrmsdmatrix`: *Calculates the pairwise interface-ligand-RMSD (il-RMSD) matrix between all the models generated in the previous step.*
    * `seletop`: *Selects the top N models from the previous step.*
    * `seletopclusts`: *Selects the top N clusters from the previous step.*

The HADDOCK3 workflows are defined in simple configuration text files, similar to the TOML format but with extra features.
Contrary to HADDOCK2.X which follows a rigid (yet highly parameterisable) procedure, in HADDOCK3, you can create your own simulation workflows by combining a multitude of independent modules that perform specialized tasks.
