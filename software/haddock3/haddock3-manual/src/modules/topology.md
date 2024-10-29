# Topology modules

- [`[topoaa]` module](#topoaa-module)

## `[topoaa]` module

The `[topoaa]` module is dedicated to the generation of CNS compatible parameters (.param) and topologies (.psf) for each of the input structures.

It will:
- Detect missing atoms, including hydrogens
- Re-build them when missing
- Build and write out topologies (`.psf`) and coordinates (`.pdb`) files

This module is a prerequisite to run any downstream modules using CNS.
Having access to parameters and topology is mandatory for any kind of EM/MD related tasks.
Therefore this is the reason why the module `[topoaa]` is often used as first module in a workflow.

Note that for non-standard bio-molecules (apart from standard amino-acids, some modified ones, DNA, RNA, ions and carbohydrates ... see [detailed list of supported molecules](https://wenmr.science.uu.nl/haddock2.4/library)), such as small-molecules, parameters and topology must be obtained and provided by the user, as there is currently no built-in solution to generate them on the fly.

More information about `[topoaa]` parameters can be accessed [here](https://bonvinlab.org/haddock3/modules/topology/haddock.modules.topology.topoaa.html#default-parameters) or retrieved by running:

```bash
haddock3-cfg -m topoaa
```

Here an example configuration file snapshot of a typical execution of the
`[topoaa]` module in which a user specifies the protonation state of the histidine
residues:

```toml
# ...
molecules = [
 "1abc.pdb",
 "2xyz.pdb"
]

[topoaa]
autohis = false
[topoaa.mol1]
nhisd = 0
nhise = 1
hise_1 = 75
[topoaa.mol2]
nhisd = 1
hisd_1 = 76
nhise = 1
hise_1 = 15

# Workflow continues
# ...
```

<hr>
