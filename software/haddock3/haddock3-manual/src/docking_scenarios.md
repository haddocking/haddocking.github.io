# Examples of docking scenario

As creating a new workflow can be complex at the beginning, we are providing a set of pre-defined haddock3 scenarios.
These examples are encompassing a wide range of applications, such as:

- [Protein-protein docking](./docking_scenarios/prot-prot.md)
- [Protein-peptide docking](./docking_scenarios/prot-peptide.md)
- [Protein-DNA docking](./docking_scenarios/prot-DNA.md)
- [Antibody-antigen docking](./docking_scenarios/antibody-antigen.md)
- [Protein-glycan docking](./docking_scenarios/prot-glycan.md)
- [Small-molecule docking](./docking_scenarios/prot-ligand.md)
- [Complexes refinement protocols](./docking_scenarios/refinement-protocols.md)
- [Building cyclic peptide](./docking_scenarios/cyclic-peptides.md)
- [Scoring workflow](./docking_scenarios/scorings.md)
- [Analysis pipelines](./docking_scenarios/analyses.md)


Alternatively, up-to-date examples can also be found:
- in your local installation of haddock3: `haddock3/examples/`.
- online, on our [GitHub repository `haddock3/examples/`](https://github.com/haddocking/haddock3/tree/main/examples).


Please note the extension scheme we are using in the provided configuration file examples:
- __*-full.cfg__: we are using the `*-full.cfg` suffix on protocols that have proper sampling, and therefore could be used in production. These are nice baseline workflows with appropriate parameters, but will obviously require more time to terminate the run. Examples making use of MPI are also provided in some cases, together with an associated job file that should be submitted to the slurm batch system (__*-full-mpi.cfg__ and __*-full-mpi.job__). Make sure to adapt the full config files to your own system.
- __*-test.cfg__: we are using the `*-test.cfg` suffix on protocols that have low sampling, allowing for fast test of the functionalities present in the workflow. Of note, on a daily basis, we are running most of the `*-test.cfg` configuration files to make sure the `main` branch of haddock3 is functional.


# Web-application pre-defined scenario

*comming soon...*
