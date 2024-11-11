# High Ambiguity Driven DOCKing

## HADDOCK general concepts

HADDOCK (see [https://www.bonvinlab.org/software/haddock2.4](https://www.bonvinlab.org/software/haddock2.4)) is a collection of python scripts derived from ARIA ([https://aria.pasteur.fr](https://aria.pasteur.fr)) that harness the power of CNS (Crystallography and NMR System – [https://cns-online.org](https://cns-online.org)) for structure calculation of molecular complexes.
What distinguishes HADDOCK from other docking software is its ability, inherited from CNS, to incorporate experimental data as restraints and use these to guide the docking process alongside traditional energetics and shape complementarity.
Moreover, the intimate coupling with CNS endows HADDOCK with the ability to actually produce models of sufficient quality to be archived in the Protein Data Bank.

A central aspect of HADDOCK is the definition of Ambiguous Interaction Restraints or AIRs.
These allow the translation of raw data such as NMR chemical shift perturbation or mutagenesis experiments into distance
restraints that are incorporated into the energy function used in the calculations.
AIRs are defined through a list of residues that fall under two categories: active and passive.
Generally, active residues are those of central importance for the interaction, such as residues whose knockouts abolish the interaction or those where the chemical shift perturbation is higher.
Throughout the simulation, these active residues are restrained to be part of the interface, if possible, otherwise incurring a scoring penalty.
Passive residues are those that contribute to the interaction but are deemed of less importance.
If such a residue does not belong in the interface there is no scoring penalty.
Hence, a careful selection of which residues are active and which are passive is critical for the success of the docking.
