### Additional restraints for multi-chain proteins

As an antibody consists of two separate chains, it is important to define a few distance restraints
to keep them together during the high temperature flexible refinement stage of HADDOCK otherwise they might slightly drift appart. This can easily be done using the `haddock3-restraints restrain_bodies` sub-command.

<a class="prompt prompt-cmd">
haddock3-restraints restrain_bodies 4G6K_clean.pdb > antibody-unambig.tbl
</a>

The result file contains two CA-CA distance restraints with the exact distance measured between two randomly picked CA atoms pairs:

<pre style="background-color:#DAE4E7">
  assign (segid A and resi 110 and name CA) (segid A and resi 132 and name CA) 26.326 0.0 0.0
  assign (segid A and resi 97 and name CA) (segid A and resi 204 and name CA) 19.352 0.0 0.0
</pre>

This file is also provided in the `restraints` directory.
