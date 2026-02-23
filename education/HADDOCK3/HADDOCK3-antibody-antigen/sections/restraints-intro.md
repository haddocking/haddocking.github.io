## Defining restraints for docking

Before setting up the docking, we first need to generate distance restraint files in a format suitable for HADDOCK.
HADDOCK uses [CNS][link-cns]{:target="_blank"} as computational engine.
A description of the format for the various restraint types supported by HADDOCK can be found in our [Nature Protocol 2024][nat-pro]{:target="_blank"} paper, Box 1.

Distance restraints are defined as follows:

<pre style="background-color:#DAE4E7">
assign (selection1) (selection2) distance, lower-bound correction, upper-bound correction
</pre>

The lower limit for the distance is calculated as: distance minus lower-bound correction
and the upper limit as: distance plus upper-bound correction.

The syntax for the selections can combine information about:

* chainID - `segid` keyword
* residue number - `resid` keyword
* atom name - `name` keyword.

Other keywords can be used in various combinations of OR and AND statements. Please refer for that to the [online CNS manual][link-cns]{:target="_blank"}.

E.g.: a distance restraint between the CB carbons of residues 10 and 200 in chains A and B with an
allowed distance range between 10Å and 20Å would be defined as follows:

<pre style="background-color:#DAE4E7">
assign (segid A and resid 10 and name CB) (segid B and resid 200 and name CB) 20.0 10.0 0.0
</pre>

<a class="prompt prompt-question">
Can you think of a different way of defining the distance and lower and upper corrections while maintaining the same
allowed range?
</a>
