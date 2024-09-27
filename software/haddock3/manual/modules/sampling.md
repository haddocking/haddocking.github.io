---
layout: page
title: ""
excerpt: ""
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, manual, usage]
image:
  feature: pages/banner_software.jpg
---

# rigidbody module

This module does a **randomization of orientations and rigid-body
minimization.** It corresponds to the classical ``it0`` step in the HADDOCK2.x
series.

In this module, the interacting partners are treated as rigid bodies, meaning
that all geometrical parameters such as bond lengths, bond angles, and dihedral
angles are frozen. The partners are first separated in space and randomly
rotated around their respective centres of mass. Afterwards, the molecules are
brought together by rigid-body energy minimisation with rotations and
translation as the only degrees of freedom.

The driving force for this energy minimisation is the energy function, which
consists of the intermolecular van der Waals and electrostatic energy terms and
the restraints defined to guide the docking. The restraints are distance-based
and can consist of unambiguous or ambiguous interactions restraints (AIRS). In
*ab-initio* docking mode those restraints can be automatically defined in
various ways; e.g. between center of masses (CM restraints) or between randomly
selected patches on the surface (random AIRs).

The definition of those restraints is particularly important as they effectively
guide the minimisation process. For example, with a stringent set of AIRs or
unambiguous distance restraints, the solutions of the minimisation will converge
much better and the sampling can be limited. In *ab-initio* mode, however, very
diverse solutions will be obtained and the sampling should be increased to make
sure to sample enough the possible interaction space.


#### Notable parameters

The most important parameters for the ``[rigidbody]`` module are:

- `ambig_fname`: file containing the ambiguous interaction restraints (AIRs)
- `unambig_fname`: file containing the unambiguous interaction restraints
- `randremoval`: whether or not to activate the random removal of restraints (default: True)
- `cmrest`: whether or not to use center of mass restraints (default: False)
- `sampling`: number of rigid body models to generate (default: 1000)

More information about ``[rigidbody]`` parameters can be accessed [here](bonvinlab.org/haddock3/modules/sampling/haddock.modules.sampling.rigidbody.html#default-parameters) or retrieved by running
```bash
haddock3-cfg -m rigidbody
```

Here an example configuration file snapshot of a typical execution of the
``[rigidbody]`` module:

```bash
...
molecules = [
    "1abc.pdb",
    "2xyz.pdb"
]

[topoaa]
[rigidbody]
ambig_fname = "ambig.tbl"
unambig_fname = "unambig.tbl"
sampling = 2000 # higher sampling if information is limited
[caprieval]
...
```
<hr>

# lightdock module

# gdock module
