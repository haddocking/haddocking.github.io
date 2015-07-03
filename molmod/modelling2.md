---
layout: page
title: "Homology Modelling of the mouse MDM2 protein"
excerpt: "Homology Modelling module of the Molecular Modelling course"
tags: [sample post, images, test]
image:
  feature: pages/banner_education-thin.jpg
---

### Finding the right sequence in Uniprot

Our goal is to create a model of the MDM2 mouse protein, in particular of its N-terminal region that
we know binds the p53 trans-activation domain. So, where do we start?

<a class="prompt prompt-info">
	Find the MDM2 mouse protein in the Uniprot database using the search box on the home page.
</a>

The [Uniprot database](http://www.uniprot.org) is an online resource that offers access to *all* the
known protein sequences and aggregates information from several other databases such as:
[RCSB PDB](http://www.rcsb.org) and its [European](http://www.ebi.ac.uk/pdbe) and 
[Japanese](http://www.pdbj.org) mirrors, NCBI [Pubmed](http://www.pubmed.org), [KEGG](http://www.genome.jp/kegg/),
[Pfam](http://pfam.xfam.org/), and many many others. This makes it an obvious first stop when looking
for information on any protein. Uniprot entries are divided in two collections: the high-quality 
Swiss-Prot, which is manually annotated and reviewed, and TrEMBL, where the annotation and revision 
are automated. If your protein of interest is marked with a golden icon/star, then it belongs to the
Swiss-Prot collection, and you can reliably (but not blindly!) trust the information therein.

<a class="prompt prompt-question">
	Despite not having an experimentally determined structure, there are plenty of structural 
	annotations for the MDM2 mouse protein in Uniprot. How is this possible?
</a>

Take your time to browse through the Uniprot page of mouse MDM2. Since our aim is to model its 3D
structure, you can use the blue sidebar to quickly navigate to the 'Structure' tab. Unfortunately,
there is no experimentally determined structure. There have been, however, automated efforts at
modelling this protein. Portals such as the [ProteinModelPortal](http://www.proteinmodelportal.org/),
[SWISS-MODEL Repository](http://swissmodel.expasy.org/), and
[ModBase](http://modbase.compbio.ucsf.edu/modbase-cgi/index.cgi) regularly cross-reference sequence 
and structure databases in order to build homology models for sequences without experimental
structures. Given the degree of automation in these protocols, it is often better to take these 
models with a grain of salt and if necessary, invest some time in modelling the protein yourself.

The 'Family & Domains' tab lists structural and domain information derived either from experiments 
or by similarity to other entries. MDM2 is a 50 kDa protein containing a SWIB domain spanning the 
first 100 residues and two zinc-fingers in the middle and C-terminal regions. 

<a class="prompt prompt-question">
	Which region of MDM2 is sufficient to bind the trans-activation domain of p53?
</a>
<a class="prompt prompt-attention">
	Note that MDM2 also interacts with p53 as part of an ubiquitination reaction, which is not of
	interest to us!
</a>

Clicking on the residue range of a particular region (e.g. 1-110) opens a new page showing that 
region in FASTA format, ready to be used in a BLAST similarity search, as well that fragment in 
context of the full sequence. This is particularly useful to directly look for homologues with known
structure. Unfortunately for you, we will take another more in-depth and less automated route.

Once you found our MDM2 region of interest, open a new file in your computer using a text editor 
(LeafPad is a text editor in our Virtual Image) and save the sequence in FASTA format. It doesn't
matter much where you save it, as long as the file is easily accessible in the command-line: your
$HOME or Downloads/ folders are good places.

The FASTA format is extremely simple: for each sequence in the file, it contains a header line 
starting with '>' followed by an alphanumerical identifier. This identifier should be meaningful to 
you and to others, not random gibberish! The next line contains the sequence. It is costumary, 
however, to split the sequence in multiple lines of 80 characters each. You will understand why when
dealing with these files through the command line. Below is an example of a sequence in FASTA format.

<a class="prompt prompt-info">
	Save the sequence of interest in FASTA format to a file in your computer.
</a> 

{% highlight bash %}
>MDM2_MOUSE
MCNTNMSVSTEGAASTSQIPASEQETLVRPKPLLLKLLKSVGAQNDTYTMKEIIFYIGQY
IMTKRLYDEKQQHIVYCSNDLLGDVFGVPSFSVKEHRKIYAMIYRNLVAV
{% endhighlight %}

Now that you have your sequence, the next step is to find a suitable homologue to use in the 
modelling protocol. If you are looking for an easy way out (not possible if you are a student!),
have a look at the [HHpred web server](http://toolkit.tuebingen.mpg.de/hhpred).

When you are ready to proceed, [click here]({{site.url}}/molmod/modelling3.html)  .