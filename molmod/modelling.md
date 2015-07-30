---
layout: page
title: "Homology Modelling of the mouse MDM2 protein"
excerpt: "Homology Modelling of the mouse MDM2 protein"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modelling, docking, p53, MDM2]
image:
  feature: pages/banner_education-thin.jpg
---
## General Overview
This tutorial is divided in 5 sections, each representing (roughly) a step of the homology modelling
procedure:  

- [A bite of theory](#a-bite-of-theory)  
- [Using Uniprot to retrieve sequence information](#using-uniprot-to-retrieve-sequence-information)  


## A bite of theory
The last decades of scientific advances in the fields of protein biology revealed the extent of both
the protein sequence and structure universes. Protein sequences databases currently hold tens of
millions of entries ([source](http://www.uniprot.org/statistics/)) and are foreseen to continue
growing exponentially, driven by high-throughput sequencing efforts. On the other hand, the number
of experimental protein structures is two orders of magnitude smaller ([source](http://www.rcsb.org/pdb/static.do?p=general_information/pdb_statistics/index.html)), and
that of unique folds has remained virtually unchanged since 2008. This apparent stagnation of the
protein structure universe is a boon for structure prediction enthusiasts, as finding a sequence
without a structurally characterized close homologue is, nowadays, quite rare.

<figure>
    <br>
    <a href="/images/molmod/rcsb-statistics.png">
        <img src="/images/molmod/rcsb-statistics.png">
    </a>
    <br>
    <figcaption>
        Growth of the protein structure database since its inception in 1974.
    </figcaption>
    <br>
</figure>

There are many methods for predicting the three-dimensional structure of proteins from their sequence,
most of which fall in one of three broad categories. Of this triumvirate, homology modelling is the
most reliable class of methods, with an estimated accuracy close to a low-resolution experimental
structure ([source](http://salilab.org/modeller/downloads/marc-bozi.pdf)). The two others, molecular
threading and _ab initio_ modelling, are usually of interest only if homology modelling is not an option.

Homology modelling is then a structure prediction method \- worth noting, not exclusively for proteins
\- that exploits the robustness of protein structure to changes in primary sequence. When protein
crystallography became routine in the 1980s, researchers started analysing and comparing
high-resolution structures. In doing so, they quickly realised that evolutionarily related proteins
shared common structural features and that the extent of this structural similarity directly
correlated with the sequence similarity ([source](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1166865/)).
To maintain structure and function, certain amino acids in the protein sequence suffer a stronger
selective pressure, evolving either slower than expected or within specific constraints, such as
chemical similarity. Combining these and other observations, early computational structural
biologists created the first homology modelling algorithms in the late 1980s/early 1990s.

## Using Uniprot to retrieve sequence information
Your goal is to create a model of the MDM2 mouse protein, in particular of its N-terminal region
that binds the p53 trans-activation domain. So, where do we start?

The Uniprot database is an online resource offering access to _all_ known protein sequences. Besides raw sequence data, Uniprot aggregates information from several other databases such as [RCSB PDB](http://www.rcsb.org) and its [European](http://www.ebi.ac.uk/pdbe) and [Japanese](http://www.pdbj.org) mirrors, NCBI [Pubmed](http://www.pubmed.org), [KEGG](http://www.genome.jp/kegg/), [Pfam](http://pfam.xfam.org/), and many others. This set of features makes Uniprot an obvious go-to resource when looking for information on any protein. There are two collections of sequences: Swiss-Prot, whose entries undergo manual annotation and revision, and TrEMBL, where the annotation is unsupervised. Consequently, if the entry for a particular protein of interest belongs to Swiss-Prot, it will be marked by a golden star/icon, and we can reliably (but not blindly!) trust its contents.

<a class="prompt prompt-info">
    Find the mouse MDM2 entry in Uniprot using the search box on the home page.
</a>

Take the time to browse through the Uniprot page of mouse MDM2. The header of the page lists the protein, gene, and organism names for this particular entry, as well as its unique Uniprot accession code. On the left, below the header, there is a sidebar listing the several sections of the page. We can use these to navigate directly to the 'Structure' section to verify if there are already published experimental structures for mouse MDM2. Fortunately, there aren't any; otherwise this tutorial would end here.

<a class="prompt prompt-question">
Given the lack of experimentally determined structures, how come there are plenty of structural annotations for mouse MDM2?
</a>

Besides reporting on experimental structures, Uniprot links to portals such as the [ProteinModelPortal](http://www.proteinmodelportal.org/), [SWISS-MODEL Repository](http://swissmodel.expasy.org/), and [ModBase](http://modbase.compbio.ucsf.edu/modbase-cgi/index.cgi), which regularly cross-reference sequence and structure databases in order to build homology models. These automated protocols are configured to create models only under certain conditions, such as sufficient sequence identity and coverage. Still, the template identification, target/template alignment, and modelling options are unsupervised, which may lead to severe errors in some cases. In general, these models offer a quick peek of what fold(s) a particular sequence can adapt and may as well serve as a starting point for further refinement and analyses. Nevertheless, if the model will be a central part of a larger study, it might be worth to invest time and effort in modelling a particular protein of interest with a set of dedicated protocols.

The following tab, "Family & Domains", lists structural and domain information derived either from experiments or by similarity to other entries. For the mouse MDM2 protein, it shows that it contains a SWIB domain and two zinc fingers and that it interacts with proteins such as USP2, PYHIN1, RFFL, RNF34, among others. Additional information displayed in the text offers additional insights on binding partners and interfaces.

<a class="prompt prompt-question">
Which region(s) of MDM2 bind p53 and which of those bind to the trans-activation domain?
</a>

From the introduction, we know that our region of interest in MDM2 interacts with the trans-activation region of p53 and does _not_ ubiquitinate it. The small print under the "Domain" header gives clues regarding possible p53 interfaces: "Region I is sufficient for binding p53"; "the RING finger domain [...] is also essential for [MDM2] ubiquitin ligase E3 activity toward p53". It seems, therefore, that _Region I_ is our modelling target, but besides this annotation, it is not listed anywhere on the Uniprot page. While this mystery has plenty of possible solutions, the easiest of which would be to search for a publication on the MDM2 domain organization, keep to the Uniprot page to find an answer.

Browsing further down the page, we find the "Sequences" tab and its listing of the several isoforms of this particular protein as they have been observed. One of these is classified as "canonical" while others are products of splicing events or mutations. The notes on isoform MDM2-p76 reveal that it lacks the first 47 amino acids and that it does _not_ bind p53. The interaction occurs then through the N-terminal of MDM2. Linking this information with that of the domain organization hints that the first region (positions 1-110) is very likely our modelling target. We can further refine this selection by choosing only the region comprising the SWIB domain (positions 27-107). Choose either the first region (positions 1-110), the SWIB domain, or whatever seems best in your opinion.

<a class="prompt prompt-question">
Why can the first ~20 amino acids of MDM2 be neglected for the modelling?
</a>

Clicking on the "position(s)" column of a particular region/domain opens a new window showing the corresponding sequence as well as the region in the context of the full sequence. Although this window provides a shortcut to launch a BLAST similarity search against the UniprotKB (or another) database, we will use other more sensitive methods for this purpose. For now, pay attention to the sequence and its format. Named FASTA after the software program it was first implemented in, it is perhaps the most widely used file format in bioinformatics, owing surely to its readability for both humans and machines.

{% highlight bash %}
>sp|P23804|1-110
MCNTNMSVSTEGAASTSQIPASEQETLVRPKPLLLKLLKSVGAQNDTYTMKEIIFYIGQY
IMTKRLYDEKQQHIVYCSNDLLGDVFGVPSFSVKEHRKIYAMIYRNLVAV
{% endhighlight %}

For each sequence in the file, it contains a header line starting with ```>``` followed by an identifier. In the Uniprot page, the identifier contains the entry's collection (sp - Swiss-Prot), accession code, and region of the sequence. The information on this header is used by several programs in many different ways, so it makes sense to keep it simple and readable.

<a class="prompt prompt-info">
Change the identifier to something more meaningful and human (e.g. MDM2_MOUSE).
</a>

The next line(s) contains the sequence in the standard one-letter code. Any character other than an upper case letter will cause some (not all) programs to throw an error about the format of the sequence. Although there is not a strictly enforced character limit, it is customary to split the sequence into multiple lines of 80 characters each. This limit, as many others based on character length, is a legacy from the old days when screen resolutions were small or terminals the only way of interfacing with the computer. Nevertheless, some programs will complain, or even worse, truncate, sequences longer than these 80 characters, so it is wise to respect this limit!

<a class="prompt prompt-info">
Copy the FASTA-formatted sequence to a text file and save it under an appropriate name (e.g. MDM2_MOUSE.fasta).
</a>
<a class="prompt prompt-attention">
Save the file in the home directory, Downloads/ folder, or any other easily accessible location.
</a>

Now that we have a sequence, the following step is to find a suitable homolog to use in the modeling protocol. The several homology modeling methods available online, such as the [HHpred web server](http://toolkit.tuebingen.mpg.de/hhpred), need only this sequence to start the entire procedure. After a few minutes or hours, depending on the protocol, these servers produce models and a set of quality criteria to help the user make a choice. The downside of using a web server is that, usually, the modeling protocol is a 'black box'. It is impossible to control settings beyond which templates and alignment to use. It is important, however, to understand what is happening behind the scenes, to make conscious choices and grasp the limitations of each method and model. Therefore, this tutorial uses a set of locally installed programs to search for templates, build the models, and evaluate their quality.
