## Antibody-antigen docking

Multiple antibody - antigen docking configuration files are [available here](https://github.com/haddocking/haddock3/tree/main/examples/docking-antibody-antigen).
They encompass various aspects of docking, mainly related to the information available to guide the docking:

- [No information about the epitope](#no-information-about-the-epitope): No information is known about the epitope, therefore targetting the entire surface accessible resiude of the antigen.
- [Experimental knowledge of the epitope residues](#nmr-informed-epitope): NMR data was aquired and allowed to obtain information about residues involded in the binding on the antigen side.


### No information about the epitope

When no information is known about the epitope on the antigen side, our only solution is to rely on the CDR loops of the antibody, as we know that a least a subset of the residues on those loops will be part of the interaction.
Two appoaches can then be used:
- One where a distance restraints file is generated, where CDR loops residues are targetting all surface residues on the antigen side.
- The other one defining random distance restraints between the CDR loops and random patches on the antigen side.

#### Using surface accessible residues

Generating restraints guiding the antibody CDR loops towards surface residues on the antigen side is a solution that will sample the entire surface of the antigen. For this, two major information must be extracted:

- The residue indices of the antibody CDR loops: can be predicted using bioinformatics tools for paratope prediction such as [proABC2](https://wenmr.science.uu.nl/proabc2).
- The surface residue indices of the antigen: can be predicted computed using `haddock3-restraints calc_accessibility antigen.pdb`.

Defining the CDR loops as `active` residues and all surface residues on the antigen as `passive`, we can create an ambiguous restraints file `ambig.tbl`, that will guide the docking sampling the entire surface of the antigen while making sure the CDR loops are interacting. For more details on how to generate restraints, please refer to the [`haddock3-restraints` documention](/software/haddock3/manual/restraints_cli.md).

For such kind of naive approach, increasing the sampling at the `[rigidbody]` level is important.

Various examples are available:

- standard HADDOCK workflow: [docking-antibody-antigen-CDR-accessible-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-full.cfg)
- with intermediate clustering steps: [docking-antibody-antigen-CDR-accessible-clt-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-clt-full.cfg)
- using MPI to spread the workload:
  - [docking-antibody-antigen-CDR-accessible-full-mpi.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-full-mpi.cfg)
  - [docking-antibody-antigen-CDR-accessible-full-mpi.job](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-accessible-full-mpi.job)



#### Using random distance restraints

An other alternative for pseudo-naive antibody-antigen docking is to define random restraints.
In this case, we will define segments on the antibody CDR loops to limit the search on the antibody side, and do not provide any definition on the antigen side.
By doing so, random residues on the CDR loops will be restrained to random patches on the antigen surface accessible residues.
This is performed in the `[rigidbody]` module by:
- turning on the `ranair` parameter
- defining 6 segments to define what are the CDR loops residues
- increasing the sampling

```toml
# Turning on the ranair parameter
ranair = true
# About to define 6 random segments for the antigen
nrair_1 = 6
# Start and end of first CDR loop
rair_sta_1_1 = 26
rair_end_1_1 = 32
# Start and end of second CDR loop
rair_sta_1_2 = 55
rair_end_1_2 = 57
# Start and end of third CDR loop
rair_sta_1_3 = 101
rair_end_1_3 = 108
# Start and end of fourth CDR loop
rair_sta_1_4 = 146
rair_end_1_4 = 152
# Start and end of fifth CDR loop
rair_sta_1_5 = 170
rair_end_1_5 = 172
# Start and end of sixth CDR loop
rair_sta_1_6 = 212
rair_end_1_6 = 215

# Increasing the sampling
sampling = 10000

###
# ....
# Insert other modules here if you want
# ....
###

[flexref]
contactairs = true
```

In this case, no AIR restraints files can be accepted (nor `unambig` and `hbond` ones).

Note that after random air definition, we will use `contactairs = true` in later stage modules such as `[flexref]` and `[emref]`, generating restraints based on residues already in contact, ensuring the complex will not detach.


Here are some examples:
- standard HADDOCK workflow: [docking-antibody-antigen-ranairCDR-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-full.cfg)
- with intermediate clustering steps: [docking-antibody-antigen-ranairCDR-clt-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-clt-full.cfg)
- using MPI to spread the workload:
  - [docking-antibody-antigen-ranairCDR-full-mpi.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-full-mpi.cfg)
  - [docking-antibody-antigen-ranairCDR-full-mpi.job](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-ranairCDR-full-mpi.job)


### NMR informed epitope

An ideal case would be to have information about the antigen epitope.
Coming from experimental methods or bioinformatic predictions, this information is extremly valuable as it will focus the search by sampling comformations near key residues involved in the interaction.
By generating a dedicated ambiguous restraint file (`ambig-CDR-NMR-CSP.tbl`), only antibody CDR residues and few residues on the antigen side will be interacting.

Here is an  example: [docking-antibody-antigen-CDR-NMR-CSP-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-antibody-antigen/docking-antibody-antigen-CDR-NMR-CSP-full.cfg)

