## Analysis scenario

The addition and inclusion of analysis modules in haddock3 is one of its major new strength, as it allows to perform various kind of analysis directly during the workflow.
For the complete list of analysis modules and their capabilities, please refere to the [Analysis Modules section](software/haddock3/manual/modules/analysis.md).


### Comparison to a reference structure

The `[caprieval]` module is dedicated to the computation of the CAPRI metrics (rmsd, interface-rmsd, ligand-rmsd, interface-ligand rmsd and dockq) on a set of input models. A reference structure can be provided using the `reference_fname` parameter. If this parameter is not defined, the best scoring model will be used as reference.

An example is provided here: [topoaa-caprieval-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/analysis/topoaa-caprieval-test.cfg).


### Hot spot detection

The analysis of hot-spots and key residues involved in the interaction between two chain can be of valuable information for mutagenesis or design purposes.
The `[alascan]` module is designed to perform point mutation of residues at the interface of a complex, and evaluate the difference in HADDOCK score with respect to the original input complex. It also splits the scoring function in its various components and generate an interactive graph allowing for a visual representation of the scanned resiudes contributions.

An example is provided here: [alascan-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/analysis/alascan-test.cfg).


### Generation of contact maps

While HADDOCK is producing 3D atomistic models, having the opportunity to have a 2D representation of the complexes can allow to understand at the sequence level the contacts involved in the compelex.
The `[contactmap]` module is specially designed to produce interactive plots describing the contacts observed in the structures.
It will produce two types of figures:
- a pair-wise distance matrix between all residues
- a chord chart recapitulating the residue-residue contacts observed

An example is provided here: [contmap-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/analysis/contmap-test.cfg)


### Fine tuning clustering parameters

Finding the appropriate threshold for the clustering parameters can be quite tricky, and often requires a first trial, followed by manual inspection to understand the content of the dataset.
We are providing examples (for `clustrmsd` and `clustfcc`) fine tuning of the parameters with visualisation of the matrices, to help you understand how to investigate the results you obtained after clustering.

Here are the two important step to analyse the structural diversity of you set of complexes in a clustering module:
- turn on the `plot_matrix` parameter to obtain a visual representation of the distance matrix.
- set the `min_population` to 1, so even singloton complexes will be forwarded to the next module and displayed on the plot.

Here are some examples:
- [fine tuning of the `clustrmsd` parameters](https://github.com/haddocking/haddock3/blob/main/examples/analysis/plot-finetune-ilrmsdmatrix-clustrmsd.cfg).
- [fine tuning of the `clustfcc` parameters](https://github.com/haddocking/haddock3/blob/main/examples/analysis/plot-finetune-clustfcc.cfg).


Note that fine tuning of clustering parameters can also be performed with the `haddock3-re` command, as both `[clustfcc]` and `[clustrmsd]` modules are subcommands of the `haddock3-re` CLI.

