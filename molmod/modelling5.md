---
layout: page
title: "Homology Modelling of the mouse MDM2 protein"
excerpt: "Homology Modelling module of the Molecular Modelling course"
tags: [sample post, images, test]
image:
  feature: pages/banner_education-thin.jpg
---

### Using MODELLER for protein homology modelling
Having chose a template for our MDM2 mouse protein sequence model, it is time to focus on building
the model itself. There are many homology modelling methods in the literature, but one truly stands
out and forms the core of the overwhelming majority of servers, services, pipelines, etc. 
[MODELLER](https://salilab.org/modeller) has been developed by Andrej Šali and a host of co-workers
since the early 1990s. It builds a structural model from a set of automatically generated spatial
restraints, but it also allows the user to define other types of restraints such as secondary
structure definitions, generic distance restraints from NMR or cross-linking mass spectrometry,
angle and dihedral angle restraints, and also Cryo-EM density maps. If you wish to learn more about 
MODELLER, have a look at the [online manual](https://salilab.org/modeller/manual/) and the 
[tutorial pages](https://salilab.org/modeller/tutorial/). 

<a class="prompt prompt-attention">
  MODELLER requires users to register and obtain an installation key. There are no costs for academic
	users though, so go ahead and get one.
</a>

For comparative modelling, MODELLER needs only an alignment and the structure of the template(s) 
in PDB or mmCIF formats. We already have all the information we need then, it only needs some 
massaging into the right formats.

#### Preparing the query/template alignment and template PDB file
MODELLER uses a modified PIR format for the alignment between the query sequence and the template
sequence. This format is quite unusual and requires particular attention. From experience, 98% of
the errors MODELLER throws at the user come from inconsistencies in the alignment. For an in-depth
description of the format, see the [MODELLER manual webpage](https://salilab.org/modeller/manual/node494.html).

{% highlight bash %}
# Example PIR alignment
>P1;5fd1
structureX:5fd1:1    :A:106  :A:ferredoxin:Azotobacter vinelandii: 1.90: 0.19
AFVVTDNCIKCKYTDCVEVCPVDCFYEGPNFLVIHPDECIDCALCEPECPAQAIFSEDEVPEDMQEFIQLNAELA
EVWPNITEKKDPLPDAEDWDGVKGKLQHLER*

>P1;1fdx
sequence:1fdx:1    : :54   : :ferredoxin:Peptococcus aerogenes: 2.00:-1.00
AYVINDSC--IACGACKPECPVNIIQGS--IYAIDADSCIDCGSCASVCPVGAPNPED-----------------
-------------------------------*
{% endhighlight %}

HMMER produced a local alignment between the query and the template. We can extract it from the 
```phmmer.out``` file directly and paste it in a new file, creating a scaffold for the PIR alignment.
Be sure to remove all the unnecessary information, such as alignment statistics, numbering, and the
'matches' line in-between both sequences. HMMER also write the query sequence in lowercase, which
MODELLER will complain about, so we have to convert it. Luckily, Linux comes with batteries included
and this conversion is one ```sed```` command evocation away.

<a class="prompt prompt-info">
  Create a new file named alignment.pir and paste in the corresponding alignment between your sequence
	and your template. Convert this file to uppercase.
</a>

<a class="prompt prompt-cmd">
  sed -i -e 's/\([a-z]\)/\U\1/g' alignment.pir
</a>

{% highlight bash %}
sp|P23804|1-110
MSVSTEGAASTSQIPASEQETLVRPKPLLLKLLKSVGAQNDTYTMKEIIFYIGQYIMTKRLYDEKQQHIVYCSNDLLGDVFGVPSFSVKEHRKIYAMIYRNLVAV
4ode_A
MSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQYIMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLVVV
{% endhighlight %}

At the top, our MDM2 mouse sequence, needs to be reformatted into the format shown above in the 
example PIR alignment, as well as moved to the bottom of the file. We have to add a header line
with a name. This name will be used also when creating the structural models, so choose something
meaningful such as ```MDM2_MOUSE```. The second line starts with ```sequence``` and is followed by
several fields separated by colons (:). The fields are explain in detail in the description of the 
format, so take your time to read it if you haven't done so. The first field is the name of the 
sequence, matching the line before; the second and fourth are the first and last residue numbers of
the sequence, usually 1 and the length of the sequence. The remaining fields are optional. The 
remaining lines are for the sequence itself. It can span as many lines as necessary or aesthetically
pleasant, although it is suggested is to keep the lines around 80 characters long. The sequence must
be terminated with an asterisk symbol '*'.

The template sequence follows a similar pattern, except it indicates ```structureX``` at the beginning
of the second line and the residue numbering fields have to match the PDB file. Additionally, as 
RCSB deposited structures are properly formatted (mostly anyway), we need to populate the third and 
fifth fields with the chain identifiers that we want to extract the structural information from.
Finally, the name of the structure *must* match the names of the PDB files without the extension, so
pay special attention to that. 

Now it's also a good time to clean the ```4ode``` PDB file. MODELLER will only need the coordinates
for the residues included in the sequence identified by HMMER, so chain A. Remove also all the water
molecules and ligand atoms as we are not interested in modelling them. Finally, pay attention to 
multiple occupancies, or atoms whose position could not be unambiguously determined in the electron
density map. Keep only the highest occupancy position, usually the first to appear in the file. You
can do all this either manually in Leafpad (or Pymol) or you can use the scripts bundled with the
Virtual Image and available on GitHub: [pdb-tools](https://github.com/haddocking/pdb-tools).

<a class="prompt prompt-cmd">
	pdb\_selchain.py -A 4odepdb1 | pdb\_delocc.py | pdb\_striphet.py > 4ODE\_A.pdb
</a>

<a class="prompt prompt-info">
  Reformat the sequences in the alignment file, according to the documentation and the example shown
	above.
</a>

{% highlight bash %}
>P1;4ODE_A
structureX:4ODE_A: 6: A: 110: A:::: 
MSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQYIMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLVVV*

>P1;MDM2_MOUSE
sequence:MDM2_MOUSE: 1: : 110: ::::
MSVSTEGAASTSQIPASEQETLVRPKPLLLKLLKSVGAQNDTYTMKEIIFYIGQYIMTKRLYDEKQQHIVYCSNDLLGDVFGVPSFSVKEHRKIYAMIYRNLVAV*
{% endhighlight %}

#### Generating the models using MODELLER
Using MODELLER requires some programming knowledge. The software exposes a very complete Python API
that allows users to create simple scripts to control all parameters of the modelling protocol. There
are plenty of example scripts to get you started on the documentation and tutorial pages of MODELLER,
but for convenience, we provide one ourselves.

<a class="prompt prompt-info">
  Start the modelling process using the cmd_modeller.py script. Keep on reading while it runs.
</a>

<a class="prompt prompt-cmd">
  python /opt/course/homology/cmd\_modeller.py -a alignment.pir -t 4ODE\_A.pdb --use\_dope --num\_models 25
</a>

The protocol and settings we will use is what we use in our group during CAPRI for example. It uses 
the MODELLER routine ```automodel``` to generate models, which automates most of the protocol and 
does *not* perform any loop modelling. Loop modelling is necessary when parts of the query sequence
do not have a matching region in the template. In these cases, MODELLER will try to model the 
conformation of the region - the loop - from first principles. The accuracy of this protocol is 
comparable to that of *ab initio* modelling methods, as for loops longer than 5-6 residues, falls 
short most of the time. 

MODELLER starts by reading and validating your alignment against the PDB file(s) of the template(s).
If your PDB file is missing some fragment of the sequence HMMER found, for example because it could 
not be observed in the electron density, then your alignment will have to be corrected. MODELLER is
quite verbose when it comes to error messages. In this particular case, of alignment mismatch, it 
will show exactly where the discrepancy occurs. The solution is to edit the alignment and change this
region to gaps ('-') in the template sequence. To avoid multiple iterations of trial and error, you
can simply extract the sequence directly from the ```ATOM``` lines of the PDB file using the utility
script ```pdb_toseq.py``` and align it to the sequence given by HMMER. This will highlight any 
missing regions.

<a class="prompt prompt-question">
	Why would some regions be missing in the electron density map of a crystal structure?
</a>

The next step in the modelling protocol is to calculate the coordinates of the atoms of an initial
model. Equivalent atoms between query and template will be simply copied, and in the case of multiple
templates, their positions averaged over all templates. The remaining atoms will be built from 
scratch using internal coordinates and the CHARMM topology library. Afterwards, MODELLER will create
all the spatial restraints it will use to refine the model. These include, but are not limited to,
stereochemical (bonds, angles, dihedrals, impropers) and homology-derived (distances between 
residues) restraints. The stereochemical restraints are derived from statistical analyses of many 
pairs of homologous structures. For each requested model, MODELLER will apply an optimization 
algorithm to fit the model as best as possible to all the restraints. Each model will be slightly 
randomized before this optimization, so that there is some variability at the end of the protocol. 
The optimization is done in several steps, first taking into account only restraints between atoms 
close in sequence, and later all other restraints. The optimization is carried out via a combination
of conjugate gradients and molecular dynamics with simulated annealing. All models are then evaluated
according to their stereochemical quality and the degree of restraints violations. The resulting PDB
files end in ```.B9999*.pdb```. MODELLER also includes other scoring functions to gauge the quality
of the models and their resemblance to 'native' structures. In our protocol, we asked to use the DOPE
energy potential, which was derived from existing structures, on top of the standard ```molpdf``` 
score. 

If we had any gapped regions in our alignment, we would need to refine the models using the
loop modelling routines of MODELLER. These would position the unknown atoms in a line connecting the
carbonyl oxigen and amide nitrogen of the flanking residues and then refine their conformation using
an atomistic distance-dependent statistical potential for non-bonded interactions. The final step 
includes the refinement of the loop atoms in context of the rest of the protein, that is, 'feeling'
the rest of the protein.

<a class="prompt prompt-question">
  Loop modelling has a length dependent accuracy. Can you think of alternative strategies to model
	long(er) loops in case they are missing in your template?
</a>

Once MODELLER is finished, it will produce a listing of the models it created together with the
values of whichever scoring functions we asked it to include. Backbone models come first, any loop
models follow after. The models are not ranked by energy or quality, but by filename. The following
is an excerpt of the first ten models produced from the 4ODE template for the 1-110 region of the
MDM2 mouse sequence.

{% highlight bash %}
>> Summary of successfully produced models:
Filename                          molpdf     DOPE score
-------------------------------------------------------
MDM2_MOUSE.B99990001.pdb       546.60236   -11802.42871
MDM2_MOUSE.B99990002.pdb       583.46625   -11945.81641
MDM2_MOUSE.B99990003.pdb       496.98846   -12110.54297
MDM2_MOUSE.B99990004.pdb       491.99567   -12092.36523
MDM2_MOUSE.B99990005.pdb       494.38525   -12074.32617
MDM2_MOUSE.B99990006.pdb       551.16998   -11953.63574
MDM2_MOUSE.B99990007.pdb       473.55539   -12075.31543
MDM2_MOUSE.B99990008.pdb       519.01727   -11768.70605
MDM2_MOUSE.B99990009.pdb       602.65222   -11901.05078
MDM2_MOUSE.B99990010.pdb       555.77435   -11917.25098
....
{% endhighlight %}

<a class="prompt prompt-info">
  Open the models and the template structure in Pymol.
</a>
<a class="prompt prompt-cmd">
	pymol 4ODE\_A.pdb MDM2\_MOUSE.B9999*pdb
</a>
<a class="prompt prompt-pymol">
	alignto 4ODE\_A.pdb
	show cartoon
	zoom vis
</a>
<a class="prompt prompt-question">
  Are there any differences between the models and the template? In which regions are these differences
	concentrated? Do you think the differences in energy scores between models are significant?
</a>

As you can see, the ```molpdf``` and ```DOPE``` scores are not entirely correlated. The best model, 
as scored by either function, is not always the same. The ```molpdf``` score reflects the agreement
of the model with the restraints, while the ```DOPE``` tries to determine which model is more 
*native-like* based on parameters derived from real structures. Which will we trust better then? The
 ```DOPE``` score, as it has been shown in several benchmarks to significantly outperform ```molpdf```.

Besides the scores given by MODELLER, it is also wise to quickly check the best model(s) using 
dedicated software for structure validation. We will use PROCHECK, which is commonplace in X-ray
crystallography and NMR, as it provides a graphical overview of the quality of a structure. You can
also use one of the many online servers for structure validation, namely [PSVS](http://psvs-1_5-dev.nesg.org/)
and [Molprobity](http://molprobity.biochem.duke.edu/).

<a class="prompt prompt-info">
	Evaluate the stereochemical quality of the lowest scoring model using PROCHECK.
</a>
<a class="prompt prompt-cmd">
  /opt/course/homology/run\_procheck.sh MDM2\_MOUSE.B99990014.pdb
</a>

PROCHECK produces several PDF files that show in detail the Ramachandran plot for all the residues
in the structure, a comparison of particular bond lengths and angles with values from experimentally
determined structures, and several geometry criteria. Explore these files and judge if your model is
of sufficient good quality. You can start also by looking at the summary file produced by PROCHECK.

{% highlight bash %}
 +----------<<<  P  R  O  C  H  E  C  K     S  U  M  M  A  R  Y  >>>----------+
 |                                                                            |
 | MDM2_MOUSE.B99990014.pdb   1.5                                105 residues |
 |                                                                            |
 | Ramachandran plot:   94.7% core    5.3% allow     .0% gener     .0% disall |
 |                                                                            |
 | All Ramachandrans:    0 labelled residues (out of 103)                     |
 | Chi1-chi2 plots:      0 labelled residues (out of  65)                     |
 | Main-chain params:    6 better     0 inside      0 worse                   |
 | Side-chain params:    5 better     0 inside      0 worse                   |
 |                                                                            |
*| Residue properties: Max.deviation:     2.4              Bad contacts:    1 |
*|                     Bond len/angle:    6.9    Morris et al class:  1  1  2 |
 |                                                                            |
 | G-factors           Dihedrals:    .23  Covalent:   -.11    Overall:    .10 |
 |                                                                            |
 | M/c bond lengths: 99.6% within limits    .4% highlighted                   |
 | M/c bond angles:  94.2% within limits   5.8% highlighted                   |
 | Planar groups:   100.0% within limits    .0% highlighted                   |
 |                                                                            |
 +----------------------------------------------------------------------------+
   + May be worth investigating further.  * Worth investigating further.
{% endhighlight %}

Given the simple alignment and high sequence identity between our query and template sequences, this
modelling exercise is extremely straightforward and the selection of the models is a trivial task. In
fact, any model of the 25 is good, regardless of the differences in energy. Nevertheless, this 
exercise of model validation, both visually and automatically, is extremely important in any real-case
modelling scenario.

As a final exercise, compare the human and mouse proteins.

<a class="prompt prompt-info">
  Open the best model and the template structure in Pymol, and find the different amino acids between
	the two proteins.
</a>
<a class="prompt prompt-cmd">
  pymol 4ODE\_A.pdb MDM2\_MOUSE.B99990014.pdb
</a>
<a class="prompt prompt-pymol">
	alignto 4ODE\_A.pdb
	zoom vis
	show cartoon
	set seq\_view, on
</a>
<a class="prompt prompt-question">
  Where are the mutations located? To they cluster together in a particular region? If so, which 
	implications could this possibly have for its function?
</a>

####Congratulations! 
You started with a sequence of a protein and went all the way from finding possible templates, to 
evaluating which to use, to building a model and attesting its stereochemical quality. This model can
now be used to offer insights on the binding of MDM2 to p53, or on the structure of the mouse MDM2
protein, or to seed new computational analysis such as docking.