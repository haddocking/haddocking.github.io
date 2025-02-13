## Protein-DNA docking

Haddock3 can also deal with nucleic acids, such as DNA and RNA molecules.
In this scenario, it is important to adjust the values of the following parameters from their defaults, as the default settings are optimized for protein-protein docking:
- keep the dielectric constant constant: `dielec = "cdie"`
- set the dielectric constant to a higher value: `epsilon = 78`
- remove the desolvation term from the scoring function (as otherwise this term exerts an excessively strong influence due to the presence of phosphate groups): `w_desolv = 0`.
- automatically generate restraints allowing to keep the double-stranded DNA 3' and 5' ends together: `dnarest_on = true`.


Here are some examples of configuration files specifically designed for protein-DNA docking:
- using a final energy minimisation step: [docking-protein-DNA-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-DNA/docking-protein-DNA-full.cfg)
- refining the interface using MD in a solvent shell: [docking-protein-DNA-mdref-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-DNA/docking-protein-DNA-mdref-full.cfg)
- with an intermediate clustering step after rigidbody docking: [docking-protein-DNA-cltsel-full.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-DNA/docking-protein-DNA-cltsel-full.cfg)
- using center of mass restraints instead of ambiguous restraints extracted from the literature: [docking-protein-DNA-cmrest-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/docking-protein-DNA/docking-protein-DNA-cmrest-test.cfg)
