* * *

layout: page
title: "Solving the complex with AlphaFold"
excerpt: "Homology Modeling of the mouse MDM2 protein"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modeling, docking, p53, MDM2, AlphaFold]
image:

## feature: pages/banner_education-thin.jpg

## General Overview

{:.no_toc}

This tutorial is divided into various sections, each representing (roughly) a step of the homology modeling
procedure.

-   table of contents
    {:toc}

<hr>

## Intro

DeepMind Technologies is an artificial intelligence subsidiary of Alphabet Inc. (Google). It broke the news in 2016 presenting AlphaGo, a computer program that plays the board game [Go](https://en.wikipedia.org/wiki/Go_(game){:target="_blank"}) and managed to beat world's top player Lee Sedol ([news article](https://www.bbc.com/news/technology-35785875){:target="\_blank"} this competition has also been made into a [movie](https://www.imdb.com/title/tt6700846/){:target="\_blank"}). Some might say that Go is the most complex game in the world due to its vast number of variations in individual games and because its large board and lack of restrictions allow great scope in strategy and expression of players' individuality. Decisions in one part of the board may be influenced by an apparently unrelated situation in a distant part of the board.

Later, in 2019 DeepMind unveiled [AlphaStar](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii){:target="\_blank"}, a computer program designed to play the game Starcraft II. This was also considered a major breakthrough since StarCraft is a real-time game (not turn-based) with partial information (you cannot see the whole board, the map, at once) with no single dominant strategy and complex rules. This was met with some controversy by top-players with allegations that AlphaStar had an unfair advantage because it could click faster than a human. :)

In DeepMind's its most recent effort, AlphaFold aims to tackle the challenging _protein folding problem_, this problem is illustrated clearly via the [Levinthal Paradox](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC48166/pdf/pnas01075-0036.pdf){:target="\_blank"}, firstly proposed in 1969 by the molecular biologist Cyrus Levinthal:

> (...) each bond connecting amino acids can have several (e.g., three) possible states, so that a protein of, say, 101 amino acids could exist in 310 = 5 X 107 configurations. Even if the protein is able to sample new configurations at the rate of 1013 per second, or 3 x 1020 per year, it will take 1027 years to try them all. Levinthal concluded that random searches are not an effective way of finding the correct state of a folded protein. Nevertheless, proteins do fold, and in a time scale of seconds or less. This is the paradox.

Nature is extremely efficient at optimizing processes, and the solution of this paradox allowed complex life to exist, not all of the aforementioned 5x107 conformations would be _thermodynamically stable_ an biologically functional. Protein folding is mainly guided by hydrophobic interactions via the formation of a hydrogen bond network, then stabilized by van der Waals forces and electrostatic interactions and hence follow a _folding path_ which is not random - this is also known as the [Thermodynamic Hypothesis](https://www.pnas.org/content/47/9/1309){:target="_blank"}. There are several experimental techniques to study protein folding such as Fluorescence spectroscopy, circular dichroism and of course Nuclear Magnetic Resonance (NMR) spectroscopy. In the computational side of things, \_ab initio_ (or _de novo_) protein structure prediction software may aim to obtain the folded state of a protein by simulating the protein dynamics via long molecular dynamics simulations, in a process analogous to what is observed in nature; this is a computationally expensive process usually tackled by large-scale computational projects such as [Rosetta@home](https://boinc.bakerlab.org/rosetta/){:target="\_blank"} and [Folding@home](https://foldingathome.org/?lng=en){:target="\_blank"}. Alternatively different heuristics can be applied, which commonly use information from structures that have been solved experimentally such as: fragment-based methods (Rosetta), evolutionary co-variation (EVFold) and protein threading (I-TASSER).

## Machine-learning

According to the [Thermodynamic Hypothesis](https://www.pnas.org/content/47/9/1309){:target="_blank"}, all the information that governs how proteins fold is contained in their respective primary sequences, this paradigm was the catalyst for the development of several computational algorithms to score protein conformations in the search of the lowest free energy state (also named the \_native state_). The main issue with this energy-driven approach is that the search space size is a function of the protein's length. The common approach for protein structure prediction is to use intermediate simplified steps that reduce the complexity of the structure but retain information, this step is called Protein Structure Annotation (PSA). PSAs can be 2-dimensional: secondary structure elements or 1-dimensional; solvent accessibility, contact maps and torsional angles. With steady growth of experimentally determined protein structures, an increasing number of PSAs are available. These annotations or can then be used in a variety of deep learning methods, such as AlphaFold.

<img src="/education/molmod_online/psa.jpg">
<!-- figure from https://www.sciencedirect.com/science/article/pii/S2001037019304441 -->


_Deep learning_ is a sub-field of _machine learning_ which is based on _artificial neural networks_ (which may seem like a new thing but was idealized in the 40's!), it uses multiple connected layers to transform inputs (PSAs in our case) into features that are then used to predict a corresponding output. Neural networks attempt to simulate the behavior of the human brain—albeit far from matching its ability—allowing it to “learn” from large amounts of data. A neural network with a single layer can still make approximate predictions, but additional hidden layers - deep learning - can help to optimize and refine for accuracy.

If you are interested in the field of machine learning, refer to the links in the bottom of the page for a starting point in your AI journey since that an in-depth explanation of machine learning is out of the scope of this course. In this extra module we will focus solely in the uses and applications of AlphaFold. Keep in mind that despite being famous for both its astonishing performance (discussed below) and great marketing department, AlphaFold is not the only one and other researchers have been applying neural networks to the issue of protein-folding such as shown in [this one published in Cell](https://www.cell.com/cell-systems/fulltext/S2405-4712(19)30076-6){:target="_blank"} that uses a recurrent geometrical network.

## AlphaFold 2

Briefly put, DeepMind trained AlphaFold on more than 170 000 proteins available in the the protein data bank; it compared multiple sequences in the data bank and looked for pairs of amino acids that often end up close together in folded structures. It then uses this data to guess the distance between pairs of amino acids in structures that are not yet known. Training took “a few weeks,” using computing power equivalent to between 100 and 200 GPUs - graphical processing units (or video cards). It uses a form of attention network, which is a deep-learning technique that allows the program to focus on smaller parts of a larger problem.


<img src="/education/molmod_online/psa.jpg">
This image is an overview of the main neural network model architecture. The model operates over homologous protein sequences as well as amino acid residue pairs, iteratively passing information between both representations to generate a 3D structure.


Given this introduction, what is the buzz all about? Many of us saw the news that AlphaFold **solved the folding problem**, which can be easily misinterpreted. The folding problem refers to the process, it refers to the _thermodynamic pathway_ that a protein takes to get to its _native state_ it is not simply the generation of a final structure. However, indeed AlphaFold provided the necessary software to obtain the 3D structure of many proteins that would not feasible via _ab initio_ or comparative modelling techniques.

This was demonstrated by the results obtained by AlphaFold on the Critical Assessment of protein Structure Prediction (CASP). This assessment  is a community-wide, worldwide experiment for protein structure prediction taking place every two years since 1994 and functions as a benchmark in the field of protein prediction. On every round, it provides research groups with one or more _targets_, the sequence of a protein that has been solved experimentally but that it is not yet available publicly. The research groups must then apply their methods to predict the structure of this protein and by the end of the round, the predictions are compared to the experimental structure.


For two years in a row (2018 and 2020), DeepMind's AlphaFold was placed first in CASP and in the latter edition it made the best prediction for 88 out of the 97 targets. It achieved a median accuracy score of 92.4 (out of 100) in the global distance test, this level of accuracy is equivalent to experimental techniques...!

<hr>

## Congratulations!

You started with a sequence of a protein and went all the way from finding possible templates, to
evaluating which to use, to building several models, assessing their quality, and finally selecting
one representative. This model can now be used to offer insights on the binding of MDM2 to p53, or
on the structure of the mouse MDM2 protein, or to seed new computational analysis such as docking.

You might want to continue with the  tutorial on
[molecular dynamics simulations](/education/molmod_online/simulation)!
