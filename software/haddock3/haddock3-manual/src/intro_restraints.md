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

# Docking restraints

HADDOCK relies on restraints to guide the sampling during the docking.
Various types of restraints are available, namely **Ambiguous**, **Unambiguous** and **Hydrogen** distance restraints.
Restraints are defined using the CNS syntax, basically defining two selections and a pseudo-distance that must be satisfied.
In case of unsatisfied restraints, a pseudo-energetical penalty is applied to the HADDOCK scoring function, therefore enabling to rank lower complexes that do not respect the restraints.


## Distance restraints

In the definition of restraints, we define two type of selection, *active* (first selection) and *passive* (second selection) and a pseudo-distance to be satisfied.

* The ***active*** residues are those experimentally identified to be involved in the interaction between the two molecules **AND** solvent accessible (either main chain or side chain relative accessibility should be typically > 40%, although a lower cutoff might be used as well).
* The ***passive*** residues are all solvent accessible surface neighbors of active residues **OR** group of atoms possibly part of the interaction.


A distance restraints is constructed as follow:

`assign (active selection) (passive selection) distance lower_boundary upper_boundary`

Where:
- `assign`: is the CNS syntax to define a new set of restraints (multiple assign statements can be found in the same restraints file)
- `active selection`: is the first selection statement.
- `passive selection`: is the second selection statement.
- `distance`: is the pseudo-distance where we hope to find the two selection together
- `lower_boundary`:
- `upper_boundary`: is the upper 

Basically a restraint is satisfied if the pseudo-distance is found between `distance - lower_boundary` and `distance + upper_boundary` (`distance - lower_boundary` <= pseudo-distance <= `distance - upper_boundary`).

By default, we usually use the following values:

- distance = 2.0
- lower_boundary = 2.0
- upper_boundary = 0.0

therefore expecting the find the pseudo-distance under 2.0 between the two selections for a restraint to be satisfied.

For a detailed explanation of the distance restraints, please refere to the following articles:

* R.V. Honorato, M.E. Trellet, B. Jiménez-García1, J.J. Schaarschmidt, M. Giulini, V. Reys,  P.I. Koukos, J.P.G.L.M. Rodrigues, E. Karaca, G.C.P. van Zundert, J. Roel-Touris, C.W. van Noort, Z. Jandová, A.S.J. Melquiond and A.M.J.J. Bonvin. [The HADDOCK2.4 web server: A leap forward in integrative modelling of biomolecular complexes](https://www.nature.com/articles/s41596-024-01011-0.epdf?sharing_token=UHDrW9bNh3BqijxD2u9Xd9RgN0jAjWel9jnR3ZoTv0O8Cyf_B_3QikVaNIBRHxp9xyFsQ7dSV3t-kBtpCaFZWPfnuUnAtvRG_vkef9o4oWuhrOLGbBXJVlaaA9ALOULn6NjxbiqC2VkmpD2ZR_r-o0sgRZoHVz10JqIYOeus_nM%3D). _Nature Prot._, Advanced Online Publication DOI: 10.1038/s41596-024-01011-0 (2024).
* A.M.J.J. Bonvin, E. Karaca, P.L. Kastritis & J.P.G.L.M. Rodrigues. Correspondence: [Defining distance restraints in HADDOCK](https://doi.org/10.1038/s41596-018-0017-6). _Nature Protocols_ *13*, 1503 (2018). [Free online only access](https://rdcu.be/1OyH)
* S.J. de Vries, M. van Dijk and A.M.J.J. Bonvin. [The HADDOCK web server for data-driven biomolecular docking.](https://www.nature.com/nprot/journal/v5/n5/abs/nprot.2010.32.html) _Nature Protocols_, *5*, 883-897 (2010).


## Ambiguous distance restraints

Ambiguous restraints are usually defined between two different chains, aiming at bringing them closer and guiding the docking procedure.
The use of ambiguous restraints is made by defining the `ambig_fname` parameter and providing the file path containing the restraints.

Because of the explicit ambiguity present in this file, two other parameters are also strongly linked to the ambiguous restraints file.
- `randremoval`: this binary parameter is stating that some of the distance restraints present in the ambiguous file should be randomly removed. By default, it is set to `true`. If set to `false`, ambiguous restraints will behave as any other distance restraints.
- `npart`: this parameter define the number of parts (splits) used to remove the ambiguous restraints. If set to `2` (default), for each complex, 50% of the restraints we be randomly removed, if set to `3`, 33% of the restraints will be randomly removed, etc...


Please note that you can provide a set of multiple restraints files, compressed in a `.tgz` archive.
In this scenario, we strongly advise to set the parameter `previous_ambig = true` in subsequent modules (instead of defining the path to the ambiguous file), so that the same ambiguous restraint file used to generate the first complex will be used again along the workflow for this specific complex.

The force constant of the ambiguous distance restraints can be tuned using the `ambig_scale` parameter or `ambig_hot`, `ambig_cool1`, `ambig_cool2` and `ambig_cool3` for simulated annealing stages in `[flexref]` module.


## Unambiguous distance restraints

In unambiguous restraints files, we often define distance restraints for which we are sure.
No random removal is applied on this set of restraints.
This type of restraints can be used to set distance between chain breaks, making sure that the two parts will not diverge during the simulation.
The use of unambiguous restraints is made by defining the `unambig_fname` parameter and providing the file path containing the restraints.

The force constant of the unambiguous distance restraints can be tuned using the `unambig_scale` parameter.


## Hydrogen distance restraints

Yet another type of restraint file, quite similar the the unambiguous ones, with no random removal applied.
This second type of unambiguous restraints can be defined using the `hbond_fname` parameter and providing the file path containing the restraints.

While unambiguous and hbond restraints are similar in their behavior, one can play with the scaling of the force constant (`hbond_scale`) to make them different, or define one or the other at various module stages in the workflow.


## Other type of restraints 

In the HADDOCK2.X series, other types of restraints were available, namely:
- Diffusion anisotropy (DANI)
- cryo-EM density maps
- Pseudo contact shifts (PCS)
- Radius of Gyration (Rg)
- Residual Dipolar Couplings (RDCs)

With the current version of haddock3, these restraints are not yet ported.
Stay tuned, as they will again show up in the near future.
