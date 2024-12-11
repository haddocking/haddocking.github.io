# Input files

Over the years, HADDOCK was updated to increase the range of biomolecular entities to deal with.
Currently, we support a broad range of molecular types, such as protein, DNA, RNA, glycans, cyclic-peptides and small-molecules.
In addition, several modified residues/nucleotides are also available.
For the full list of supported molecules, please refer to [https://wenmr.science.uu.nl/haddock2.4/library](https://wenmr.science.uu.nl/haddock2.4/library).
If you wish to work with a molecule type that is not present in this list, please refer to the [Dealing with non-standard molecules section](#dealing-with-non-standard-molecules).


In the following sections, we will tackle the variety and specificity of each of the molecule types.


## Supported file format

Haddock3 currently supports files in PDB and mmCIF format.
The PDB format is quite strict, and all characters must be well positioned in the file.

To make sure your file is correctly formatted, you can use the `pdbtools` library (which should be already installed in your `haddock3-env` virtual environment),
or read [this online resource](https://cupnet.net/pdb-format/) where it is well explained.

Please refer to the [pdb-tools](./pdbtools.md) section for more information on how to use it.

### PDB format

In order to run HADDOCK you need to have the structures of the molecules (or fragments thereof) in PDB format.
There are a few points to pay attention to when preparing the PDBs for HADDOCK.

* Make sure that all PDB files end with an END statement

* If providing a conformational ensemble (e.g.: from an NMR PDB entry, or out of a MD simulation), each model should start with a MODEL statement and end with an ENDMDL statement and the file should terminate with a END.

* haddock3 will **not** check for breaks in the chain (e.g. missing density in crystal structures or between the two strands of a DNA molecules).
 In the case of multiple chains within one molecule (e.g. DNA) or in the presence of co-factors, it is recommended to add a TER statement in between the chains/sub-molecules.
 Also, consider using the `haddock3-restraints restrain_bodies` command line to generate restraints and input them as unambiguous restraints using the `unambig_fname` parameter.

* If your input molecule consists of multiple chains with overlapping numbering you will have to renumber those (or shift the numbering of some parts) in order to avoid overlapping numbering.
 HADDOCK will treat each molecule with a single chainID and overlap in numbering will lead to problems.

* Higher-resolution crystal structures often contain multiple occupancy side-chain conformations, which means one residue might have multiple conformations present in the crystal structure, each with a partial occupancy.
 The definition of alternative conformations is often reflected by the presence of a `A` and `B` before the residue name for the atoms having multiple conformations.
 To avoid problems, only one conformation should be retained (the web server will raise an error for such cases).
 This can be easily done using our [PDB-tools](https://github.com/haddocking/pdb-tools).
 Alternatively, you can also make use of our new [PDB-tools webserver](https://wenmr.science.uu.nl/pdbtools/){:target="_blank"} for this.
 The script that allows you to remove double occupancies is `pdb_selaltloc`.
 Its default behavior is to only keep the first (`A`) conformation, but you can select other conformations if wanted.

* HADDOCK can deal with ions.
 You will have however to make sure that the ion naming is consistent with the ion [topologies provided in HADDOCK](https://wenmr.science.uu.nl/haddock2.4/library).
 For example, a CA heteroatom with a residue name CA will be interpreted as a neutral calcium atom.
 A doubly charged calcium ion should be named CA+2 with CA2 as residue name to be properly recognized by HADDOCK.
 (See also the [FAQ](./faq.md) for docking in the presence of ions).

A list of [supported modified amino acids and ions is available online](https://wenmr.science.uu.nl/haddock2.4/library).


**Note:** Most of the tasks mentioned above can also be performed using our PDB-tools python scripts ([Rodrigues et al. *F1000 Research* (2018)](https://doi.org/10.12688/f1000research.17456.1)) to manipulate PDB files, select and rename chains and segids, renumber residues... and much more!
It should be installed by default in your haddock3 environment.
And a [dedicated section is present in this manual](./pdbtools.md).

For more details, see for this our [GitHub repository](https://github.com/haddocking/pdb-tools).
Alternatively, you can also make use of our new [PDB-tools webserver](https://wenmr.science.uu.nl/pdbtools/).


<hr>

## Number of input molecules 

Haddock3 currently supports up to 20 separate input molecules, thus allowing multi-body (1 <= N <= 20) docking.
Each input molecule can be composed of an [ensemble of conformations](#conformational-ensemble), allowing to implicitly represent the conformational sampling.
Input molecules can also be composed of multiple chains, allowing for their evaluation using scoring and analysis modules.

To input molecules, use the [global parameter](/software/haddock3/manual/global_parameters) `molecules = ["path/to/mol1.pdb", "path/to/mol2.pdb"]`.


## Definition of a chain

A chain is defined by a letter in the 22<sup>nd</sup> position in the PDB file format.
Within the same file, two chains must be separated by a `TER` statement.
Do not worry if you have gaps (missing resiudes) in your chain, it will be automatically detected by HADDOCK.
To make sure the structure do not fall appart during molecular dynamics steps, you can add [`body-restraints`](/software/haddock3/manual/restraints_cli.md#body-restraints) ensuring the constant distance originally observed in the input file.


## Conformational ensemble

Conformational ensembles are detected using the `MODEL` and `ENDMDL` keywords in the PDB file.
Note that if in your ensemble, we detect two types of `REMARK` statements when providing an ensemble:

- `REMARK     MODEL X FROM conformationX.pdb`: as generated by `pdb_mkensemble`, we will keep track of the origin of the conformation.
- `REMARK   X MODEL Y MD5 XXXXXXXXXXXXXXXXXX`: as provided by CAPRI scoring set, we will keep track of the MD5 checksum of the input conformation/model.


## Dealing with non-standard molecules

If you wish to work with a molecule type that is not present in the [list of supported molecules](https://rascar.science.uu.nl/haddock2.4/library), do not worry, as you will still be able to use HADDOCK.
To properly function, HADDOCK requires to have access to the topology and parameters of a molecule to run the molecular dynamics protocols.
The force field must therefore be updated by user-provided topology and parameter files.

In modules that use CNS, you can provide such files with the `ligand_top_fname` (for ligand topology filename) and `ligand_param_fname` (for ligand parameters filename) parameters, specifying the location where to find those two files.


### How to generate topology and parameters for my ligand

Generating topology and parameters for your ligand is not trivial.
For this, you will need to use dedicated tools, such as `acpype` or [`ccp4-prodrg`](https://www.ccp4.ac.uk/html/index.html), or dedicated libraries such as [`BioBB`](https://mmb.irbbarcelona.org/biobb/).

Here are some useful resources on how to generate those:

- **BioBB using acpype**: The [BioExcel BioBuildingBlock (BioBB)](https://mmb.irbbarcelona.org/biobb/) library is hosting several tutorials on how to perform computations with a variety of different tools.
 Here is a link to the workflow used to parametrize ligands: [https://mmb.irbbarcelona.org/biobb/workflows/tutorials/biobb_wf_ligand_parameterization](https://mmb.irbbarcelona.org/biobb/workflows/tutorials/biobb_wf_ligand_parameterization).
- **Automated Topology Builder (ATB)**: Repository developed in Prof. Alan Mark's group at the University of Queensland in Brisbane: [https://atb.uq.edu.au/](https://atb.uq.edu.au/).
