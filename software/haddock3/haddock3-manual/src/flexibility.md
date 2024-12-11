# Flexibility options in Haddock3

In the refinement modules of Haddock3, a molecule or parts of it (i.e., its segment(s)) can be treated as:

* **Rigid**: The entire chain is treated as rigid throughout all phases of the module's protocol.
* **Semi-flexible**: One or several segments of the chain are treated as rigid during the initial phases of the protocol and as fully flexible during the final phases.
* **Fully flexible**: One or more segments of the chain are treated as fully flexible during all phases of the protocol.

By default, semi-flexible and rigid segments of docking partners are determined automatically based on interface contacts. Automatically defined semi-flexible segments include residues within the interface, meaning residues that are 5Å or closer to residues in another molecule. The remaining segments comprising residues outside of the interface are automatically defined as rigid.
By default, no segments are defined as fully flexible.

Flexibility can be defined in any of the CNS model refinement modules, namely: `[emref]`, `[flexref]`, and `[mdref]`.
Check out schematic images of the refinement protocols employed in different [refinements modules](./modules/refinement.md):
* [`[flexref]`](./modules/refinement.md#flexref-module-simulated-annealing-protocol-scheme)
* [`[mdref]`](./modules/refinement.md#mdref-module-scheme)
* [`[emref]`](./modules/refinement.md#emref-module-scheme)

Below you can find explanations and examples on the definition of different types of segments:
* [Automatic Definition of Rigid and Semi-Flexible Segments)](#automatic-definition-of-rigid-and-semi-flexible-segments)
* [Manual definition:](#manual-definition)
  * [Rigid Molecule](#rigid-molecule)
  * [Semi-flexible Segment](#semi-flexible-segment)
  * [Fully flexible Segment](#fully-flexible-segment)

<hr>

## Automatic Definition of Rigid and Semi-Flexible Segments

As this behaviour is enabled by default, there is no need to add any parameters to the tolm file.

Internally, this behaviour is controlled by the `nsegX` parameter, which specifies the number of semi-flexible segments for molecule X. Here, `X` corresponds to the sequential number of the molecule in the input, i.e. the order in which input PDB files are given.

For example:
* If no manual flexibility is defined and two docking partners are provided, Haddock3 will proceed with:
`nseg1 = -1; nseg2 = -1`
* For three docking partners, the parameters will be:
`nseg1 = -1; nseg2 = -1; nseg3 = -1`

And so on, for additional molecules.
The default value of `-1` indicates that the semi-flexible and rigid segments are automatically defined based on the molecule's interface residues.

<hr>

## Manual definition
### Rigid Molecule
To keep an entire molecule rigid throughout the refinement, the `nsegX` parameter for that molecule should be set to 0.

#### Example: Keeping the Protein Molecule Rigid

Consider a docking protocol involving two molecules: DNA and protein, where DNA is the 1st molecule and protein is the 2nd by the order of the input. This order is important!  
To treat the protein as a rigid body during flexible refinement, set the parameter nseg2 to 0. The corresponding .cfg file would look as follows:
```toml
# Input molecules: DNA as the 1st molecule, and protein as the 2nd 
molecules = ["DNA.pdb", "protein.pdb"]

# ...

[flexref]
# Keep the protein rigid
nseg2 = 0

# No definition for nseg1, so it is set to -1 by default.
# This means the DNA molecule will have its rigid and semi-flexible segments
# automatically defined based on interface residues.
```

### Semi-flexible Segment

To manually define a semi-flexible segment, the user must specify the first and last residues of the segment using the parameters `seg_sta_X_Y` and `seg_end_X_Y`, respectively.
Parameter Details:
* `X` is the sequential number of the molecule (i.e. position of the PDB file in the input) to which the segment belongs. This follows the same logic as `X` in `nsegX` parameter, explained above. 
* `Y` is the sequential number of the segment being defined. This allows multiple semi-flexible segments to be defined within the same molecule.
* The values of `seg_sta_X_Y` and `seg_end_X_Y` must be integers and must correspond to residue indices present in the corresponding input PDB file.

#### Example: Two Semi-Flexible Segments of DNA

Consider a docking scenario with two partners: a DNA molecule and a protein, where two segments of the DNA are manually defined as semi-flexible.
* The first segment includes residues 2 to 19.
* The second segment includes residues 22 to 39.

The DNA molecule is defined as the 1st partner, and the protein as the 2nd. This order is important!

To define the semi-flexible segments:

* The first segment (suffix _1) starts at residue 2 and ends at residue 19.
* The second segment (suffix _2) starts at residue 22 and ends at residue 39.
The corresponding .cfg file would look as follows:

```toml
# Input molecules: DNA as the 1st molecule, and protein as the 2nd 
molecules = ["DNA.pdb", "protein.pdb"]

# ...

[flexref]
# Define the first segment (suffix _1) for DNA (X = 1) between residues 2 and 19
seg_sta_1_1 = 2
seg_end_1_1 = 19

# Define the second segment (suffix _2) for DNA (X = 1) between residues 22 and 39
seg_sta_1_2 = 22
seg_end_1_2 = 39
```

### Fully flexible Segment

Fully Flexible Segment
The manual definition of a fully flexible segment differs slightly from the definition of a semi-flexible segment. For fully flexible segments, the user must specify the first and last residues of the fully flexible segment using the parameters `fle_sta_Y` and `fle_end_Y`. On top of it, the user must define the chain ID (instead of the molecule's sequential number) using the parameter `fle_seg_Y`.

Parameter Details:
* `Y` defines the sequential number of the segment being defined. This allows multiple semi-flexible segments to be defined within the same chain.
* The value of `fle_seg_Y` is a string and must correspond to the chainID/segemntID present in one of the input PDB files.
* The values of `seg_sta_X_Y` and `seg_end_X_Y` must be integers and must correspond to residue indices present in chain/segment defined by `fle_seg_Y.


#### Example: Fully Flexible Glycan

Let's consider a docking scenario involving two partners, namely a protein (chain A) and a glycan (chain B, consisting of 4 residues, numbered strating from 1), where the entire chain of glycan is manually defined as fully flexible.

Let's define the protein as the 1st docking partner and the glycan as the 2nd docking partner in `.cfg` file.
Then, to define glycan as fully flexible, its entire chain should be treated a single segment, i.e.:
* the chainID is set to 'B'
* the starting residue is set to 1
* the ending residue is set to 4

The corresponding .cfg file would look as follows:

```toml
molecules = [
 "protein.pdb", # chain A
 "glycan.pdb"   # chain B, residues from 1 to 4
 ]

# ...

[flexref]
# Define chain ID of 1st fully flexible segment
fle_seg_1 = "B"
# Define the first residue for the 1st fully flexible segment 
fle_sta_1 = 1
# Define the last residue for the 1st fully flexible segment 
fle_end_1 = 4
```
