---
layout: page
title: ""
excerpt: ""
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, manual, usage]
image:
  feature: pages/banner_software.jpg
---

* table of contents
{:toc}

<hr>

# Flexibility Options in Haddock3

A molecule or a part of it, i.e., its segment, can be defined as:
* rigid;
* semi-flexible;
* fully flexible.

By default, rigid and semi-flexible segments of docking partners are automatically defined based on interface contacts. By default, none of the segments are defined as fully flexible.

Flexibility can be defined in any of the Model Refinement modules (emref, flexref, and mdref).

The process for manual definition is detailed below.

<hr> 

## Manual Definition of Rigid or Semi-Flexible Segments

Parameters `nsegX = <integer>` are used to define:

* the docking partner (`X`) to which the segments of interest belong;
* the type of flexibility (`<integer>`)of the segments of interest;
* the number of these segments.

The docking partner to which the segments belong is encoded in the name of the parameter itself. For example, if the segments belong to the 1st docking partner, the parameter `nseg1` should be used (defined in .cfg file). If the segments belong to the 2nd docking partner, then `nseg2` should be used, and if they belong to the 3rd docking partner, then `nseg3`, etc. Haddock3 allows up to 20 docking partners simultaneously.

The value of the chosen parameter simultaneously defines the type of flexibility and the number of segments:
* If `nsegX = -1`, then the Xth docking partner will be defined as rigid or semi-flexible automatically (default setting);
* If `nsegX = 0`, then the Xth docking partner is defined as rigid;
* If `nsegX = y` with `y > 0`, then:
  - The segments of interest are defined as semi-flexible;
  - The number of these segments is equal to `y`. In this case, the first and last residues of each segment should be defined using pairs of parameters `seg_sta_X_1`, `seg_end_X_1`, and consequently `seg_sta_X_2`, `seg_end_X_2`, etc., until all `y` segments are defined. Haddock3 allows for up to 1000 segments, with residues numbered up to 9999.


#### Example: Two Semi-Flexible Segments of a DNA

Let's consider a docking scenario involving two partners, namely a DNA and a protein, with two segments of DNA defined manually as semi-flexible. Suppose the first segment contains residues 2 to 19, and the second segment contains residues 22 to 39.

Since the order of the docking partner is important, let's define DNA as the 1st partner and protein as the 2nd partner in .cfg file, like so:

```
molecules = ["DNA.pdb", "protein.pdb"]
```

To define two segments of DNA (1st partner), we should assign 2 to the parameter `nseg1`:

```toml
nseg1 = 2
```

The last step is to define the first and last residues of each segment. The first segment starts with residue 2 and ends with residue 19, and the second segment starts with residue 22 and ends with residue 39:
```toml
seg_sta_1_1 = 2
seg_end_1_1 = 19

seg_sta_1_2 = 22
seg_end_1_2 = 39
```

<hr>

## Manual Definition of Fully Flexible Segments

This definition is very similar to the semi-flexible definition. Parameters `nfleX` are used to define:
* the docking partner to which the segments of interest belong;
* the type of flexibility of the segments of interest;
* the number of these segments.
  
The docking partner to which the segments belong is encoded in the name of the parameter itself. For example, if the segments belong to the 1st docking partner, the parameter `nfle1` should be used. If the segments belong to the 2nd docking partner, then `nfle2` should be used, etc. Haddock3 allows for up to 20 docking partners simultaneously.

The value of the chosen parameter simultaneously defines the type of flexibility and the number of segments:
* If `nfleX = 0`, then the Xth docking partner is defined as rigid (default setting);
* If `nfleX = y` with `y > 0`, then:
  - The segments of interest are defined as fully flexible;
  - The number of these segments is equal to `y`. In this case, the first and last residues of each segment should be defined using pairs of parameters `fle_sta_X_1`, `fle_end_X_1`, and consequently `fle_sta_X_2`, `fle_end_X_2`, etc., until all y segments are defined. Haddock3 allows for up to 1000 segments, with residues numbered up to 9999.


#### One Fully Flexible Segment of a Glycan

Let's consider a docking scenario involving two partners, namely a protein (chain A) and a glycan (chain B, consisting of 4 residues), with the latter being fully flexible.
Let's define the protein as the 1st docking partner and the glycan as the 2nd docking partner in .cfg file like so:

```toml
molecules = ["protein.pdb", "glycan.pdb"]
```

To be defined as fully flexible, the entire glycan (2nd partner) should be defined as a single segment, where we will define the starting resiude (`sta`), ending residue (`end`) and the chainID/segmentID (`seg`).
For this, three parameter must be tuned:

```toml
# Starting resiude for the flexibility
fle_sta_1 = 1
# Ending resiude for the flexibility
fle_end_1 = 4
# ChaindID/segmentID of the molecule
fle_seg_1 = "B"
```




