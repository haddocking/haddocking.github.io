---
layout: page
title: "Using the AlphaFold3 web server to model the MDM2-p53 complex"
excerpt: "Solving the complex with AlphaFold3"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modeling, docking, p53, MDM2, AlphaFold3]
image:
    feature: pages/banner_education-thin.jpg
---

## General Overview
{:.no_toc}
This extra module provides a quick guide on how to use the [AlphaFold Server](https://alphafoldserver.com/welcome){:target="_blank"} to predict a structure of the MDM2-p53 complex and on how to use the output metrics to evaluate the prediction. 

* table of contents
{:toc}

## Introduction 

The [press release](https://www.nobelprize.org/prizes/chemistry/2024/press-release/){:target="_blank"} issued on October 9th, 2024, announcing the Nobel Prize in Chemistry, states that "*The Nobel Prize in Chemistry 2024 is about pro­teins, life’s ingenious chemical tools. David Baker has succeeded with the almost impossible feat of building entirely new kinds of proteins.
Demis Hassabis and John Jumper have developed an AI model to solve a 50-year-old problem: predicting proteins’ complex structures. These discoveries hold enormous potential*".
This prize was awarded to the developers of AlphaFold2, a tool capable of predicting protein structures with an accuracy previously unseen
Many of AlphaFold2’s predictions at [Critical Assessment of Protein Structure Prediction](https://predictioncenter.org/index.cgi){:target="_blank"} (CASP) were so accurate as to be indistinguishable from experimentally solved protein structures. Shortly after the release of AlphaFold2, [AlphaFold-Multimer](https://www.biorxiv.org/content/10.1101/2021.10.04.463034v1){:target="_blank"}, was introduced, extending the approach to the prediction of **protein–protein complexes**() rather than individual protein structures.
More background on the evolution from DeepMind’s early work on game-playing AI to AlphaFold2, as well as practical guidance on running AlphaFold-Multimer in Google Colab, can be found [here](https://www.bonvinlab.org/education/molmod_online/alphafold/){:target="_blank"}.


By the time AlphaFold2 was awarded the Nobel Prize, an even more powerful model had already been published.[AlphaFold3](https://www.nature.com/articles/s41586-024-07487-w){:target="_blank"} (AF3), unlike its predecessors, it is designed to predict the structures of a broad range of macromolecular complexes, including not only protein–protein complexes but also complexes involving DNA, RNA, small molecules, and ions
DeepMind achieved this by large-scale training on structural data, drawing on essentially all relevant entries available in the Protein Data Bank up to 30/09/2021, as well as additional curated chemical and biological information.
Architecturally, AlphaFold3 differs from earlier versions by introducing a diffusion-based generative model for structure prediction.

Both AlphaFold3 and 2 are using attention-based neural networks for representation learning, but the the structure generation process differs between the models.
In AF2 it is done via the structure module which predicts per-residue rigid frames (rotation + translation) along the protein backbone, filling in side-chain atoms afterwards. On the contrary, AF3 uses a diffusion-based generative process to generate all atomic coordinates jointly.
What did not change is the reliance on evolutionary and structural context, i.e. multiple sequence alignments (MSA) and templates are still being used for modelling protein components, although their role is reduced or absent for non-protein partners. 

The detailed mechanics and intuitions behind the AlphaFold3 pipeline have been described many times in various online sources, and we can recommend: 
* [A talk on AF3 by Sergey Ovchinnikov](https://www.youtube.com/watch?v=qjFgthkKxcA){:target="_blank"}, one of the leading researchers in protein structure prediction. 
* [A non-ML expert breakdown of the AF3 pipeline](https://research.dimensioncap.com/p/an-opinionated-alphafold3-field-guide){:target="_blank"}.

## What is the AlphaFold Server? 

AlphaFold3 itself is a deep learning model, and while the inference pipeline, i.e. the code required to run the model, but not to train it, is publicly available on [GitHub](https://github.com/google-deepmind/alphafold3){:target="_blank"}, it cannot realistically be run on a regular PC.
The system is designed for datacenter-class GPUs and requires very large memory and storage resources, including up to ~1 TB of disk space to host the necessary databases, as well as hundreds of gigabytes of RAM for practical use. 

The AlphaFold Server is the most user-friendly way to use this tool.
It not only removes the burden of installing the pipeline but also provides the necessary resources for computations - free of charge!
However, there is a limit of 30 jobs per day (as of January 2026), and you need a Google account to register. 

### Using the AlphaFold Server to predict the p53-MDM2 complex

Generating a prediction with the AlphaFold Server is extremely straightforward and can be done in just a few clicks (just 4, if you use keyboard shortcuts to copy-paste the sequences and navigate :) ).
Once a set of 5 models has been generated, it is essential to examine the associated confidence metrics to assess the reliability of the predictions.
In this section, we will use the AlphaFold Server to predict the 3D structure of the p53–MDM2 complex and examine the confidence metrics provided by the server.

<a class="prompt prompt-info">
    Go to AlphaFold Server [https://alphafoldserver.com/welcome](https://alphafoldserver.com/welcome){:target="_blank"} and log in using the "Continue with Google" button.
</a>

<a class="prompt prompt-info">
    Scroll past the information block and several examples of structures until you see the input form.
</a>

<a class="prompt prompt-info">
    Copy-paste the sequence of the protein into the "Input" field, then click "Add entity" and paste the peptide sequence into the "Input" field of the newly created entity. 
</a>

<a class="prompt prompt-info">
    Press "Continue and preview job". In the new model window, you can either keep the auto-generated title and seed or enter your own. Then press "Confirm and submit job". 
</a>

You should see the job appearing in the panel at the bottom of the page.
Depending on the size of the molecules, the job can take several minutes to several hours. But once it's done you will be see the results. 

### Interpreting confidence metrics

On the result page you can see the 1st, i.e. top-ranked, predicted structure out of 5 and associated confidence metrics - pLDDT, PAE, pTM and ipTM scores.

You can find a description of the metrics online, for example:
* A practical guide to AlphaFold in the frame of the EMBL-EBI Training: [https://www.ebi.ac.uk/training/online/courses/alphafold/](https://www.ebi.ac.uk/training/online/courses/alphafold/){:target="_blank"}. Navigate to "How to assess the quality of AlphaFold 3 predictions" to see info about the metrics specifically. 
* An FAQ & Guides page of the AF Server: [https://alphafoldserver.com/guides#overview:](https://alphafoldserver.com/guides#overview:){:target="_blank"}.  Navigate to "Section 3: Interpreting results from AlphaFold Server" to see info about the metrics specifically.

Take a look at the result page:
<img src="education/molmod_online/p53_MDM2_AF3_Server.png" style="margin-left: auto;margin-right:auto">

<a class="prompt prompt-question">
Look at the pLDDT of MDM2. Can you trust this model? What about the N-ter? 
</a>
<details style="background-color:#DAE4E7">
 <summary style="bold">
   <i>Answer</i> <i class="material-icons">expand_more</i>
 </summary>
 <p>
   The majority of the MDM2-predicted structure has a pLDDT of 90 or higher, so the structure can, in principle, be trusted. AlphaFold3, like any of the currently existing deep learning models, cannot guarantee the absence of so-called artificial hallucination, i.e. false information presented with high confidence; however, given the abundance of information about MDM2 that you used to build a homology model, it's safe to trust AlphaFold3 in this case. 

   The N-ter of the model has a low pLDDT score. This is expected for the flexible long terminal stretches of proteins, often because those parts of the molecules are not experimentally resolved, or are resolved as an NMR ensemble with varied positions. This means that these termini are not as well presented in the online databases, meaning that AF3 is not as good in predicting them. This usually does not hinder the quality of the overall prediction. 
 </p>
</details>
<br>

<a class="prompt prompt-question">
Look at the ipTM and pTM scores - do they indicate that 3D structure of the complex is trustworthy?  
</a>
<details style="background-color:#DAE4E7">
 <summary style="bold">
   <i>Answer</i> <i class="material-icons">expand_more</i>
 </summary>
 <p>
    Both ipTM and pTM scores are above 0.8 which indicates a confidently predicted interaction.
 </p>
</details>
<br>

<a class="prompt prompt-question">
Look at the PAE matrix - what can you conclude given that a dark green colour dominates it? Can you explain why there is a vertical section of light green appearing in the vicinity of residue 23? 
</a>
<details style="background-color:#DAE4E7">
 <summary style="bold">
   <i>Answer</i> <i class="material-icons">expand_more</i>
 </summary>
 <p>
    A dark green colour is indicative of a low predicted position error, i.e. the relative position of the pairs of tokens. The area corresponding to the peptide structure shows a very low overall predicted error, with core residues having higher confidence than terminal ones. 

    The light-coloured vertical section corresponds to the N-ter of MDM2, residues 1-~16. This tail can flop and move around without impacting the overall structure, so its predicted position error is high. You can compare its position between all 5 generated models - it is extremely likely to differ between those.  
 </p>
</details>
<br>

<a class="prompt prompt-info">
    Download the results of the AF Server using a button above the plDDT scale.  
    Unpack the zip file. Open all 5 cif models in PyMOL, check the difference between all 5 models and their pLDDT values. 
</a>

Align the models, and colour them by b-factor visualize pLDDT values per atom. 
<a class="prompt prompt-pymol">
    alignto fold_p53_mdm2_model_0 and chain B
</a>
<a class="prompt prompt-pymol">
    spectrum b
</a>

<a class="prompt prompt-info">
    Examine the other files present in the results folder. If you need to refresh on the content of the files and/or the meaning of the metrics, don't hesitate to consult the server's Guide page or the EMBL guide.
</a>

As you can see, generating structural models with AF3 requires far less time and manual effort than classical structural modelling. 
This naturally raises an important question: how accurate are the models produced by AF3?

<a class="prompt prompt-info">
    Compare the AF3 prediction with your docking models and with the reference structure. 
    If the structures appear very similar in cartoon representation, consider switching to a lines or sticks representation to inspect side-chain conformations more closely.
</a>


In structural modelling, the quality of the predicted models depends on many factors, one of the most important being the amount of relevant information available. 
As you observed during homology modelling, there is extensive experimental information for both MDM2 and the p53–MDM2 complex, including experimentally solved structures of human MDM2 bound to p53 (PDB: 1YCR), which can serve as a modelling template. 
In such cases, producing an accurate prediction is relatively straightforward.
The situation is very different for more challenging targets, where experimental information is sparse or entirely absent. 
A useful way to assess the current state of the field is through community-wide blind prediction experiments such as CASP and the Critical Assessment of Predicted Interactions ([CAPRI](https://www.capri-docking.org/){:target="_blank"}).
In these challenges, participants are given only the sequences of the constituents of the complex, whose structure have been experimentally determined but not yet released, providing an objective benchmark for computational methods.

Looking at the results of the most recent analyzed round (CASP16/CAPRI - 2024), we see that the AlphaFold Server participates but is not among the top-performing approaches. 
In fact, several human teams consistently produce more accurate models. 
This is likely because they combine AlphaFold-based predictions with other modelling tools and, crucially, expert human judgment - the same types of skills you applied when performing homology modelling of MDM2, analyzing peptide MD simulations, and evaluating docking models.

<img src="education/molmod_online/CASP_CAPRI16.png" style="margin-left: auto;margin-right:auto">

These results also highlight a broader challenge in structural modelling, scoring. The plot includes results from MassiveFold, a dataset of 8,040 models per target generated using AlphaFold2. 
As shown by the “best-of-best” bar, a high-quality model is almost always present somewhere in this large set. 
However, identifying that model is far from trivial. The gap between the “best-of-best” and “MassiveFold-best” bars illustrates how difficult it is, even for expert teams, to reliably select the best model from a the pool.
This points to two key limitations of current approaches. Firstly, better scoring id needed to identify the best model out of the pool.
Secondly, generating thousands of models per target requires substantial computational resources. 
Ideally, future modelling tools will be able to produce a small number of high-quality models directly, reducing the need for exhaustive sampling.
In short, while tools like AlphaFold3 represent a major advance, they do not eliminate the need for careful analysis, complementary methods, and human expertise, especially for challenging targets.