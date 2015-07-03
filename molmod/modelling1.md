---
layout: page
title: "Homology Modelling of the mouse MDM2 protein"
excerpt: "Homology Modelling module of the Molecular Modelling course"
tags: [sample post, images, test]
image:
  feature: pages/banner_education-thin.jpg
---

### A bite of theory
Of the triumvirate in computational structure prediction, homology modelling is the most accurate 
and reliable method for building the three-dimensional structure of a protein sequence of interest
([source](http://salilab.org/modeller/downloads/marc-bozi.pdf)). The other two, molecular threading 
and *ab initio* modelling, are usually only of interest when the sequence of interest does not have
a close homologue with an experimentally determined structure. However, the last decades revealed 
that the protein structure universe is finite and that the sequence universe is still expanding quite 
rapidly. Indeed, there are millions of known protein sequences, two orders of magnitude more than 
structures and many more than unique folds currently deposited in the RCSB PDB. As such, the 
chances of *not* finding such a homologue are quite small and thus, homology modelling is often the
first computational method to try when predicting protein structure.

<figure>
    <a href="/images/molmod/rcsb-statistics.png"><img src="/images/molmod/rcsb-statistics.png"></a>
    <figcaption>Growth of the protein structure database since its inception in 1974.</figcaption>
</figure>

Homology modelling exploits the fact that protein tertiary structure is more conserved than the 
primary structure, or the amino acid sequence. When looking at sequences of evolutionarily related 
proteins, certain residues are observed to evolve slower than expected, or evolving within certain
constraints, such as chemical similarity (i.e. same charge, aromatic character). These are usually 
associated with key structural features necessary for protein function, be it the catalytic center of
an enzyme or residues that mediate interactions with partner molecules. As such, in similar proteins,
these residues ought to occupy similar structural positions - this is the basis of homology modelling
algorithms since their inception in the late 80s/early 90s.

When you are ready to proceed, [click here]({{site.url}}/molmod/modelling2.html).