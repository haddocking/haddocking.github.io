
### Defining ambiguous restraints

Once you have identified your active and passive residues for both molecules, you can proceed with the generation of the ambiguous interaction restraints (AIR) file for HADDOCK.
For this you can either make use of our online [GenTBL][gentbl] web service, entering the list of active and passive residues for each molecule, the chainIDs of each molecule and saving the resulting restraint list to a text file, or use another `haddock3-restraints` sub-command.

To use our `haddock3-restraints active_passive_to_ambig` script, you need to
create for each molecule a file containing two lines:

* The first line corresponds to the list of active residues (numbers separated by spaces)
* The second line corresponds to the list of passive residues (numbers separated by spaces).

*__Important__*: The file must consist of two lines, but a line can be empty (e.g., if you do not want to define active residues for one molecule). However, there must be at least one set of active residue defined for one of the molecules.


* For the antibody we will use the predicted paratope as active and no passive residues defined. The corresponding file can be found in the `restraints` directory as `antibody-paratope.act-pass`:

<pre style="background-color:#DAE4E7">
1 32 33 34 35 52 54 55 56 100 101 102 103 104 105 106 151 152 169 170 173 211 212 213 214 216

</pre>

* For the antigen we will use the NMR-identified epitope as active and the surface neighbors as passive. The corresponding file can be found in the `restraints` directory as `antigen-NMR-epitope.act-pass`:

<pre style="background-color:#DAE4E7">
72 73 74 75 81 83 84 89 90 92 94 96 97 98 115 116 117
3 24 46 47 48 50 66 76 77 79 80 82 86 87 88 91 93 95 118 119 120
</pre>

Using those two files, we can generate the CNS-formatted Ambiguous Interaction Restraints (AIRs) file with the following command:

<a class="prompt prompt-cmd">
haddock3-restraints active_passive_to_ambig ./restraints/antibody-paratope.act-pass ./restraints/antigen-NMR-epitope.act-pass \-\-segid-one A \-\-segid-two B > ambig-paratope-NMR-epitope.tbl
</a>

This generates a file called `ambig-paratope-NMR-epitope.tbl` that contains the AIRs. 

<a class="prompt prompt-question">
Inspect the generated file and note how the ambiguous distances are defined.
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>View an extract of the AIR file</i></b> <i class="material-icons">expand_more</i>
  </summary>
<pre>
assign (resi 31 and segid A)
(
       (resi 72 and segid B)
        or
       (resi 73 and segid B)
        or
       (resi 74 and segid B)
        or
       (resi 75 and segid B)
        or
       (resi 81 and segid B)
        or
       (resi 83 and segid B)
        or
       (resi 84 and segid B)
        or
       (resi 89 and segid B)
        or
       (resi 90 and segid B)
        or
       (resi 92 and segid B)
        or
       (resi 94 and segid B)
        or
       (resi 96 and segid B)
        or
       (resi 97 and segid B)
        or
       (resi 98 and segid B)
        or
       (resi 115 and segid B)
        or
       (resi 116 and segid B)
        or
       (resi 117 and segid B)
        or
       (resi 3 and segid B)
        or
       (resi 24 and segid B)
        or
       (resi 46 and segid B)
        or
       (resi 47 and segid B)
        or
       (resi 48 and segid B)
        or
       (resi 50 and segid B)
        or
       (resi 66 and segid B)
        or
       (resi 76 and segid B)
        or
       (resi 77 and segid B)
        or
       (resi 79 and segid B)
        or
       (resi 80 and segid B)
        or
       (resi 82 and segid B)
        or
       (resi 86 and segid B)
        or
       (resi 87 and segid B)
        or
       (resi 88 and segid B)
        or
       (resi 91 and segid B)
        or
       (resi 93 and segid B)
        or
       (resi 95 and segid B)
        or
       (resi 118 and segid B)
        or
       (resi 119 and segid B)
        or
       (resi 120 and segid B)
) 2.0 2.0 0.0
...
</pre>
  <br>
</details>
<br>

<a class="prompt prompt-question">
Refering to the way the distance restraints are defined (see above), what is the distance range for the ambiguous distance restraints?
</a>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>See answer</i></b> <i class="material-icons">expand_more</i>
  </summary>
The default distance range for those is between 0 and 2Å, which 
might seem short but makes senses because of the 1/r^6 summation in the AIR
energy function that makes the effective distance to be significantly shorter than
the shortest distance entering the sum.
<br>
<br>
The effective distance is calculated as the SUM over all pairwise atom-atom
distance combinations between an active residue and all the active+passive on
the other molecule: SUM[1/r^6]^(-1/6).
</details>
<br>

