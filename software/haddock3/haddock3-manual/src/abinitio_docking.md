# Ab-initio / naive docking protocols

While HADDOCK is ment to use information from coming from experiments, literature or bioinformatic predictions to guide the sampling during the docking, sometimes you cannot obtain such kind of data.
For this reasons, dedicated parameters can be turned **on** to perform *ab-inito* docking.

Three different ways of doing *ab-inito* docking in haddock3 are discussed below.


### Prior considerations

- As ab-initio docking contains very loose information on how the various chains involed should interact, we strongly advise to increase the sampling at `[rigidbody]` docking stage (using `sampling` parameter) as finind a good solution relies on trials and errors.
- The next trhee *ab-inito* docking solution described below are incompatible with each other, and you should not turn **on** multiple of them at the same time.


## Center of mass restraints

Turning **on** the center of mass restraints parameter (`cmrest = true`), will automatically generates restraints between the center of masses of the different chains present the system, and use those during the docking.

This parameter goes together with the `cmtight` paraemter, which controls how the upper limit distance is defined for the center of mass restraints between molecules.
Each molecule is oriented along its principle components and the x, y and z dimensions are calculated.
If `cmtight=true`, the molecule distance (size) is set to the average of its smallest two half dimensions.
If `cmtight=false`, the molecule distance (size) is set to the average of its three half dimensions.
In case of DNA, RNA, small ligands or glycans, the molecule distance (size) is set to 0.
The effective upper distance limit for the center of mass distance restraint is the sum of the two molecule distances.

`cmrest` and `cmtight` parameters are accessible in `[rigidbody]` and `[flexref]` modules.

This parameter goes together with its force constant (`kcm`), that can be tuned as well.

Please note that setting `cmrest = true` is more suited for globular structures.
As for example, for a long bDNA structure, the restraint will be defined to the center of the DNA.


## Random Ambiguous Restraints

An other solution is to generate random ambiguous restraints.
This is performed by turning **on** the `ranair` parameter (`ranair = true`) in the `[rigidbody]` module.

By doing so, for each rigidbody sampling performed, residues on the surface of each chains will be randomly picked together with surrounding ones to define a patch.
Ambiguous restraints will then be generated between all the patches and rigidbody minimisation performed.

We suggest to turn on `contactairs = true` parameters in later stages of the workflow for CNS modules (`[flexref]`, `[emref]`, `[mdref]`).

__*Note*__ that `ranair` is limitted to the docking of two chains only, and no other type of restraints will be considered (even tho specified in the configuration file).


## Surface restraints

An alternative solution is to turn **on** the `surfrest` parameter (`surfrest = true`).
By doing so, surface residues are first detected and contact restraints between molecules are generated on the fly.
These are defined as an ambiguous distance restraint between all backbone (CA, BB or N1) atoms of two molecules (for small ligands all atoms are considered).
If less than 3 CA and P atoms are found, all atoms will be selected instead.
The upper limit is set to 7A (or 4.5A in case of small ligands).

Such restraints can be useful in multi-body (N>2) docking to ensure that all molecules are in contact and thus promote compactness of the docking solutions.
As for the [random AIRs](#random-ambiguous-restraints), surface contact restraints can be used in ab-initio docking; in such a case it is important to have enough sampling of the random starting orientations and this significantly increases the number of structures for rigid-body docking.

Note that this option is computationally more expensive than the [center of mass restraints](#center-of-mass-restraints) and [random AIRs](#random-ambiguous-restraints), as the number of restraints is increasing by the power of the number of resiudes present in the system.
Also, because of the high number of restraints, the physico-chemical components of the scoring function can be masked by the noise of the AIRs component.
Therefore setting the weight of the AIR component to 0 (`w_air = 0`), could help the scoring function to better decipher between model conformations.

This parameter goes along with its force constant `ksurf`, that can be tuned.
