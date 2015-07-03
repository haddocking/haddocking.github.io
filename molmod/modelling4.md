---
layout: page
title: "Homology Modelling of the mouse MDM2 protein"
excerpt: "Homology Modelling module of the Molecular Modelling course"
tags: [sample post, images, test]
image:
  feature: pages/banner_education-thin.jpg
---

### Choosing the right template for homology modelling
Now that we have collected a number of interesting candidates for templates, how do we proceed? What
criteria should be taken into account, beyond sequence identity and similarity? Since we do have the
three-dimensional structures of the templates, we can critically judge their quality from a structural
biology point of view. 

Using the search bar at the top-right corner of the page, search for the several structures that 
HMMER reported. The identitifers used by HMMER (e.g. ```1z1m_A```) are a mixture of the PDB code (```1z1m```) and
the chain in the structure that has that particular sequence (```A```). In the search bar, type only the 
four-character PDB code.

<a class="prompt prompt-info">
  In different tabs (if possible), search for the top 5 hits of your HMMER search.
</a>

Modellers tend to prefer X-ray over NMR as a method for structure determination. NMR spectroscopists
determine their structures using a set of distance restraints extracted while the protein is tumbling
in solution. As you can imagine, the distances collected by the spectroscopist reflect therefore a
multitude of states, which are represented in NMR structures by an ensemble of possible conformations.
Indeed, open any NMR structure and you will find multiple models. As there is no 'best' conformation,
it is hard to make a choice on which ensemble member to use as a template and therefore, modellers 
tend to *prefer* static X-ray structures. Note the emphasis on *prefer*: if there is nothing else
available, then by all means do use the NMR structure as a template. 

Unlike NMR, X-ray structures have pretty simple quality criteria: the resolution and the R-free 
metrics. The resolution is a measure of the level of detail in the diffraction pattern, which
translates to the detail that can be seen upon calculating the electron density map. The higher the
resolution, the lower the value, and the more you can trust the atomic model. Values below 2Å are
acceptable and structures below 1Å resolution are considered ultra-high resolution. The R-free 
reflects the agreement of the final atomic model with a part of the raw diffraction data that not
used to build the structure. Again, the lower the value, the better, with 0.26 being considered 
'average' ([source](http://www.rcsb.org/pdb/101/static101.do?p=education_discussion/Looking-at-Structures/resolution.html)).

Unfortunately, the first three hits (```1z1m_A```, ```2lzg_A```, and ```2mps_A```) are all NMR 
structures. The fourth, ```4ode_A```, is a crystal structure and given its very reasonable sequence 
identity value of 85%, it is still a perfectly suitable candidate. If you scroll down to the 
'Molecular Description' section of the web page of the ```4ode``` entry at RCSB, you find that the
structure belongs to the E3 ubiquitin-protein ligase Mdm2 of *Homo sapiens*. Looking at the 
'Experimental Details' (right sidebar) and 'Structure Validation' (under Molecular Description) 
sections, we also learn that this is a high-quality structure with a resolution of 1.80Å and an 
R-free value and overall stereochemistry parameters above average for all structures of similar
resolution.

Another factor to take into account when choosing a template is the conformation it shows in the 
crystal structure. If a protein is co-crystallized with a co-factor, ligand, or other protein, how
sure can you be that its conformation reflects the one you are truly looking for? In our case, we
want to model MDM2 in order to study its interaction with p53. Should we take *any* crystal structure
or should we be picky? One way of circumventing this problem is to analyze *all* possible template
structures. Superimposing a set of structures and analyzing the resulting atomic RMSD values is a way
of checking if there is significant conformational change between them. If there is, then you must
be extremely careful about which template to choose. Optimally, you might even make several models, 
each using a different template, hoping you cover enough of the conformational space that you can
make informed guesses about your own protein of interest. For the sake of time, do this only for 5 
templates. Let's also use Pymol, a freely available molecular visualization software that runs on 
Windows, MacOS X, and Linux. You can download it [here](http://pymol.org/dsc/) and visit the 
[community-maintained Wiki](www.pymolwiki.org) for any help with the commands. It is already 
pre-installed in the Virtual Image.

<a class="prompt prompt-info">
  Open Pymol via the command-line in your homology_modelling folder and use it to analyse the 5 best
  templates determined by X-ray crystallography.
</a>
<a class="prompt prompt-cmd">
  pymol
</a>

First, use Pymol's ```fetch``` command to download the structures directly from the PDB website. To
avoid downloading the crystal units, which may contain extra copies of the protein and hinder our 
analysis, use the optional ```type``` keyword to download only the biological unit 
([source](http://www.rcsb.org/pdb/101/static101.do?p=education_discussion/Looking-at-Structures/bioassembly_tutorial.html)).

<a class="prompt prompt-pymol">
  fetch 4ode 4odf 4ogn 4ogt 4wt2, type=pdb1
</a>

Align all the structures onto the backbone atoms of ```4ode``` and change the representation of the
protein to 'cartoon' and that of any ligand or ion to spheres. Also, remove all water molecules from
the structures.

<a class="prompt prompt-pymol">
  select 4ode_backbone, 4ode and name CA+C+N+O  
	alignto 4ode_backbone  
	as cartoon  
	show spheres, het  
  remove solvent  
</a>

If you click on the black background and press the ```escape``` key (Esc), you will stop seeing the 
molecules and will see the gritty log file of your Pymol instructions. Pressing ```Esc``` again will
revert to the normal view. The log shows you the RMSD values of the fitting you performed with the 
```alignto``` command, ordered by object name (```4ode```, ```4odf```, ...). 

{% highlight bash %}
RMSD 0.000000 over 104 residues
RMSD 0.699095 over 96 residues
RMSD 0.677597 over 96 residues
RMSD 0.786586 over 96 residues
RMSD 0.395698 over 104 residues
{% endhighlight %}

As you can see, the structures hardly from each other. This is valuable information for the 
modelling: even with different binding partners, the conformation of MDM2 does not seem to change
significantly.

<a class="prompt prompt-question">
  Where do you observe the larger changes in the protein structure? Do you think this will have a
	significant impact in the modelling protocol?
</a>
<a class="prompt prompt-question">
  Bonus question: do you agree with the RMSD values produced by Pymol? Why?
</a>

From this analysis, we can finally make a choice for a template. Given its resolution, overall
structure quality, and the (apparent) conformational rigidity of MDM2, ```4ode``` is a good template
to model the mouse MDM2 protein.

As a side note, choosing *one* single template might not be ideal in all cases. When modelling a 
multi-domain protein, for example, or when a single domain is not complete in any template, it is
wise to use multiple templates simultaneously to build the model. Some also defend that using
multiple templates for a single domain might help eliminating errors from the crystal structures,
although this is disputed. Regardless, this is beyond the scope of this course, so we won't go in 
further detail. [Have a look here](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2386743/) if you want
to explore this issue further.

When you are ready to proceed, [click here]({{site.url}}/molmod/modelling5.html).