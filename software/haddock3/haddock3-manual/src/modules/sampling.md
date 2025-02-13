# Sampling modules

- [`[rigidbody]` module](#rigidbody-module)
- [`[lightdock]` module](#lightdock-module)
- [`[gdock]` module](#gdock-module)


## `[rigidbody]` module

The `[rigidbody]` module does a **randomization of orientations and rigid-body minimization.**
It corresponds to the classical `it0` step in the HADDOCK2.x series.

In this module, the interacting partners are treated as rigid bodies, meaning that all geometrical parameters such as bond lengths, bond angles, and dihedral angles are frozen.
The partners are first separated in space and randomly rotated around their respective centers of mass.
Afterward, the molecules are brought together by rigid-body energy minimisation with rotations and translation as the only degrees of freedom.

The driving force for this energy minimization is the energy function, which consists of the intermolecular van der Waals and electrostatic energy terms and the restraints defined to guide the docking.
The restraints are distance-based and can consist of unambiguous or ambiguous interactions restraints (AIRS).
In *ab-initio* docking mode those restraints can be automatically defined in various ways; e.g. between the center of masses ([CM restraints](../abinitio_docking.md#center-of-mass-restraints)) or between randomly
selected patches on the surface (random AIRs).

The definition of those restraints is particularly important as they effectively guide the minimization process.
For example, with a stringent set of AIRs or unambiguous distance restraints, the solutions of the minimization will converge much better and the sampling can be limited.
In *ab-initio* mode, however, very diverse solutions will be obtained and the sampling should be increased to make sure to sample enough the possible interaction space.

<details >
<summary style="bold">
<b><i>See animation of the rigidbody protocol:</i></b>
</summary>
<figure align="center">
  <img src="./images/haddock_mini.gif">
</figure>
</details>
<br>

The default HADDOCK scoring function in the rigid-body module is the following:

![equ](https://latex.codecogs.com/gif.latex?HS=0.01E_{vdw}&plus;1.0E_{elec}&plus;0.01E_{air}&plus;1.0E_{desolv}-0.01BSA)

For a detailed explanation of the components of the scoring function, please have a look [here](../haddocking.md#haddock-scoring-function).

Throughout the years, the weights of the scoring function have been optimized for various systems.
For example, when dealing with small molecules or glycans, it is recommended to scale up the van der Waals term from 0.1 to 1:

```toml
# ...
[rigidbody]
w_vdw = 1.0
# ...
```

![equ](https://latex.codecogs.com/gif.latex?HS_{small}=1.0E_{vdw}&plus;1.0E_{elec}&plus;0.01E_{air}&plus;1.0E_{desolv}-0.01BSA)

Please refer to the [different docking scenarios](../docking_scenarios.md) for more information about how to tune the scoring function for your specific system.

#### Notable parameters

The most important parameters for the `[rigidbody]` module are:

- `ambig_fname`: file containing the ambiguous interaction restraints (AIRs)
- `unambig_fname`: file containing the unambiguous interaction restraints
- `randremoval`: whether or not to activate the random removal of restraints (default: True)
- `cmrest`: whether or not to use center of mass restraints (default: False)
- `sampling`: number of rigid body models to generate (default: 1000)

More information about `[rigidbody]` parameters can be accessed [here](https://www/bonvinlab.org/haddock3/modules/sampling/haddock.modules.sampling.rigidbody.html#default-parameters) or retrieved by running:

```bash
haddock3-cfg -m rigidbody
```

Here an example configuration file snapshot of a typical execution of the
`[rigidbody]` module:

```toml
# ...
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
# ...
```
<hr>

## `[lightdock]` module

<hr>

## `[gdock]` module

<hr>