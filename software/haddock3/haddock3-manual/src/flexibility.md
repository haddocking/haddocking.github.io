# Flexibility options in Haddock3

A molecule or a part of it, i.e., its segment, can be defined as:
* rigid: Where the full chain will be treated as rigid.
* semi-flexible: Where segments of the chains can be defined as flexible during the last two cooling phases of the simulated annealing protocol.
* fully flexible: Where segments of the chains can be defined as flexible during all phases of the protocol.

By default, rigid and semi-flexible segments of docking partners are automatically defined based on interface contacts.
Interface residues (detected when distance <5A) are defined as semi-flexible, while the other residues are kept rigid, as there is no point in refining non-contacting regions.
By default, none of the segments are defined as fully flexible.

Flexibility can be defined in any of the CNS model refinement modules, namely `[emref]`, `[flexref]`, and `[mdref]`.

The process for manual definition is detailed below:
* [Defining semi-flexible segments](#definition-of-semi-flexible-segments)
  * [Automatic definiton](#automatic-definiton-of-semi-flexible-segments-based-on-contact)
  * [Keeping a chain rigid](#treating-the-chain-as-rigidbody)
  * [Custom definiton](#custom-definiton-of-semi-flexible-segments)
* [Defining fully-flexible segments](#manual-definition-of-fully-flexible-segments)

<hr>

## Definition of semi-flexible segments

Parameters `nsegX` (standing for **n**umber of semi-flexible **seg**ments for molecule **X**) are is used to define:

* the docking partner (`X`) to which the segments of interest belong, where `X` is an integer corresponding to the position of the input molecule in the configuration file;
* an integer describing if it must be automatic (-1) or kept rigid (0), used in [automatic definition](#automatic-definiton-of-semi-flexible-segments-based-on-contact) and to [keep a molecule rigid](#treating-the-molecule-as-rigidbody)

The two parameters, `seg_sta_X_Y` and `seg_end_X_Y`, are used to [define custom semi-flexible segments](#custom-definiton-of-semi-flexible-segments).


For a better understanding of the definition of **semi-flexible segments** in [refinements modules](./modules/refinement.md), please check the schemes for the various modules:
* [`[flexref]`](./modules/refinement.md#flexref-module-simulated-annealing-protocol-scheme)
* [`[mdref]`](./modules/refinement.md#mdref-module-scheme)
* [`[emref]`](./modules/refinement.md#emref-module-scheme)


Here you can access the various types of semi-flexible definitions:
* [Automatic definiton](#automatic-definition-of-semi-flexible-segments-based-on-contact)
* [Keeping a chain rigid](#treating-the-molecule-as-a-rigidbody)
* [Custom definiton](#custom-definition-of-semi-flexible-segments)


### Automatic definition of semi-flexible segments based on contact

Nothing is to be done, this is the default behavior.

To your knowledge, this is understood by haddock3 when the parameter `nsegX = -1`, which will trigger an internal search of what are the residues in contact with, and automatically turn their flexibility for the last two cooling stages of the simulated annealing protocol (*semi*-flexible).


### Treating the molecule as a rigidbody

To keep a molecule rigid for the entire process, you must tune the parameter `nsegX` (standing for **n**umber of semi-flexible **seg**ments for molecule **X**) and set it to `0`.


#### Example: Keeping the protein rigid

In this case, the file `protein.pdb` is the second input molecule, and therefore will hold the index `2`, therefore we will use the parameter name `nseg2`, and set its value to `0`.

```toml
# Input two molecules, DNA as the first one, and protein as the second
molecules = ["DNA.pdb", "protein.pdb"]
# ...
# ...
[flexref]
# To maintain the protein rigid during the flexible refinement,
# we must set the 'nseg2' parameter to '0'.
nseg2 = 0
```


### Custom definition of semi-flexible segments

If you want to provide an explicit definition of semi-flexbile segments, two parameters must be used.
These parameters are well structured and are composed of 4 parts, enabling HADDOCK to understand to which molecules you are defining semi-flexible segments.

Here is a schematic representation of the two parameters:

```toml
seg_sta_X_Y = 1
seg_end_X_Y = 10
```

Here is an explannation of the parameters:
* It always starts with the `seg_` prefix
* it is followed by either the `sta_` (to define the starting residue) or `end_` (to define the final residue)
* a first index `X` corresponding the to input molecule position
* a final suffix index `_Y` used to match the start and end position of a segment, thus allowing to define multiple segments for the same molecule.
* The final integer value, corresponds the residue index in the input PDB file.

Haddock3 allows for the definition of up to 1000 segments, with residues numbered ranging from -999 to 9999.


#### Example: Two Semi-Flexible Segments of a DNA

Let's consider a docking scenario involving two partners, namely a DNA and a protein, with two segments of DNA manually defined as semi-flexible.
Suppose the first segment contains residues 2 to 19, and the second segment contains residues 22 to 39.

Since the order of the docking partner is important, let's define DNA as the 1st partner and protein as the 2nd partner in .cfg file.
In this case, the file `DNA.pdb` is first input molecule, and therefore will hold the index `1`.
The next step is to define the first and last residues of each segment.
The first segment (with suffix `_1`) `sta`rts with residue `2` and `end`s with residue `19`, and the second segment (with suffix `_2`) `sta`rts with residue `22` and `end`s with residue `39`:

```toml
molecules = ["DNA.pdb", "protein.pdb"]
# ...
# ...
[flexref]
# Defining a first segment (suffix _1) for DNA between residues 2 and 19
seg_sta_1_1 = 2
seg_end_1_1 = 19

# Defining a second (suffix _2) segment for DNA between residues 22 and 39
seg_sta_1_2 = 22
seg_end_1_2 = 39
```

<hr>

## Manual Definition of Fully Flexible Segments

This definition is quite similar to the custom semi-flexible definition.
This time the definition does not use the molecule index but its chain ID / Segment ID.
It therefore requires the definition of 3 parameters for each fully flexible segment:
* `fle_sta_X`: defining the starting residue of the `X`th fully-flexible segment
* `fle_end_X`: defining the ending residue of the `X`th fully-flexible segment
* `fle_seg_X`: defining the chainID/segmentID of the `X`th fully-flexible segment

Here is a detailed explanation of how this parameter is built:
- It starts with the prefix `fle_`, used to trigger the definition of a fully-flexible parameter
- It continues with infix `sta`, `end` or `seg` defining the starting residue, end residue and chainID/segmentID of the fully-flexible segment
- It terminates with the suffix `_X` defining the index of this segment, allowing to group together the fully flexible parameters together.


#### Example: Giving full-flexibility to a Glycan

Let's consider a docking scenario involving two partners, namely a protein (chain A) and a glycan (chain B, consisting of 4 residues), with the latter being set to fully flexible.

Let's define the protein as the 1st docking partner and the glycan as the 2nd docking partner in `.cfg` file.
Then, to be defined as fully flexible, the entire glycan (2nd partner, chain B) should be defined as a single segment, where we will define the starting residue (`sta`), ending residue (`end`) and the chainID/segmentID (`seg`).


```toml
molecules = [
 "protein.pdb", # chain A
 "glycan.pdb"   # chain B
 ]
# ...
# ...
[flexref]
# Starting residue for the flexibility
fle_sta_1 = 1
# Ending residue for the flexibility
fle_end_1 = 4
# ChaindID/segmentID of the molecule
fle_seg_1 = "B"
```
