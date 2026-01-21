---
layout: page
title: "Using AlphaFold3 web server to model the MDM2-p53 complex"
excerpt: "Solving the complex with AlphaFold3"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modeling, docking, p53, MDM2, AlphaFold3]
image:
    feature: pages/banner_education-thin.jpg
---

## General Overview
{:.no_toc}
This extra module provides an quick guide to on how to use [AlphaFold Server](https://alphafoldserver.com/welcome){:target="_blank"} to predict a structure of the MDM2-p53 complex and on how to use the output metrics to evaluate the prediction. 

* table of contents
{:toc}

## Introduction 

The [press release](https://www.nobelprize.org/prizes/chemistry/2024/press-release/){:target="_blank"} issued on October 9th, 2024, announcing the Nobel Prize in Chemistry, states that "*The Nobel Prize in Chemistry 2024 is about pro­teins, life’s ingenious chemical tools. David Baker has succeeded with the almost impossible feat of building entirely new kinds of proteins. Demis Hassabis and John Jumper have developed an AI model to solve a 50-year-old problem: predicting proteins’ complex structures. These discoveries hold enormous potential*".
This prize was given to the developers of AlphaFold2, a tool capable of predicting protein structures with unseen before accuracy. Many of AlphaFold2’s predictions at [Critical Assessment of Protein Structure Prediction](https://predictioncenter.org/index.cgi){:target="_blank"} were so accurate as to be indistinguishable from experimentally solved protein structures. Shortly after the release of AlphaFold2, [AlphaFold-Multimer](https://www.biorxiv.org/content/10.1101/2021.10.04.463034v1){:target="_blank"}, was introduced, extending the approach to the prediction of **protein–protein complexes**() rather than individual protein structures. More background on the evolution from DeepMind’s early work on game-playing AI to AlphaFold2, as well as practical guidance on running AlphaFold-Multimer in Google Colab, can be found [here](https://www.bonvinlab.org/education/molmod_online/alphafold/){:target="_blank"}.


By the time AlphaFold2 was awarded the Nobel Prize, an even more powerful model had already been published.[AlphaFold3](https://www.nature.com/articles/s41586-024-07487-w){:target="_blank"} (AF3), unlike its predecessors, is designed to predict the structures of a broad range of macromolecular complexes, including not only protein–protein complexes but also complexes involving DNA, RNA, small molecules, and ions. Deep Mind achieved this by large-scale training on structural data, drawing on essentially all relevant entries available in the Protein Data Bank up to 30/09/2021, as well as additional curated chemical and biological information. Architecturally, AlphaFold3 differs from earlier versions by introducing a diffusion-based generative model for structure prediction. While attention-based neural networks remain central to representation learning (in both AF3 and AF2), diffusion models are used to generate atomic structures, reflecting a broader trend in machine learning that originated in image generation. What did not change is the reliance on evolutionary and structural context, i.e. multiple sequence alignments (MSA) and templates are still being used for modelling protein components, although their role is reduced or absent for non-protein partners. 

The detailed mechanics and intuitions behind the AlphaFold3 pipeline have been described many times in various online sources, and we can recommend: 
* [A talk on AF3 by Sergey Ovchinnikov](https://www.youtube.com/watch?v=qjFgthkKxcA){:target="_blank"}, one of the leading researchers in protein structure prediction. 
* [A non-ML expert breakdown of AF3 pipeline](https://research.dimensioncap.com/p/an-opinionated-alphafold3-field-guide){:target="_blank"}.

## What is the AlphaFold Server? 

AlphaFold3 itself is a deep learning model, and while the inference pipeline, i.e. the code required to run the model, but not to train it, is publicly available on [GitHub](https://github.com/google-deepmind/alphafold3){:target="_blank"}, it cannot realistically be run on a regular PC. The system is designed for datacenter-class GPUs and requires very large memory and storage resources, including up to ~1 TB of disk space to host the necessary databases, as well as hundreds of gigabytes of RAM for practical use. 

AlphaFold Server is a most user-friendly way to use this tool. It not only removes the burden of installing the pipeline, but also provides necessary resources for the computations - free of charge! However, there is a limit of 30 jobs per day (as of January of 2026) and you need a Google account to register. 

### Using the AlphaFold Server to predict the p53-MDM2 complex

Generating a prediction with the AlphaFold Server is extremely straightforward and can be done in just a few clicks (exactly 4, if one would use keyboard shortcuts to copy-paste the sequences and for navigation:). Once a set of 5 models has been generated, it is essential to examine the associated confidence metrics in order to assess how reliable the prediction is. In this section, we will use the AlphaFold Server to predict the 3D structure of the p53–MDM2 complex and examine the confidence metrics provided by the server.

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
    Press "Continue and preview job". In the new modal window, you can either leave auto-generated title and seed, or put your own. Then press "Confirm and submit job". 
</a>

You should see the job appearing in the panel at the bottom part of the page. Once it's done, which can take from several minutes to several hours, depending on the size of the molecules, you will be able to see the results.  

### Interpreting confidence metrics

On the result page you can see the 1st predicted structure out of 5 and associated confidence metrics - pLDDT, PAE, pTM and ipTM scores.

You can find a description of there metrics online, for example:
* A practical guide to AlphaFold in the frame of the EMBL-EBI Training: [https://www.ebi.ac.uk/training/online/courses/alphafold/](https://www.ebi.ac.uk/training/online/courses/alphafold/){:target="_blank"}. Navigate to "How to assess the quality of AlphaFold 3 predictions" to see info about the metrics specifically. 
* An FAWQ & Guides page of AF Server: [https://alphafoldserver.com/guides#overview:](https://alphafoldserver.com/guides#overview:){:target="_blank"}.  Navigate to "Section 3: Interpreting results from AlphaFold Server" to see info about the metrics specifically.

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
   The majority of MDM2 predicted structure has pLDDT of 90 or higher, so the structure in principle can be trusted. AlphaFold3, as any of the currently existing deep learning models, cannot guarantee absence of so-called artificial hallucination, i.e. false information presented with high confidence, however, given the abundance of information about MDM2, that you used to build a a homology model, it's save to trust AlphaFold3 in this case. 

   The N-ter of the model has low pLDDT. It is expected for the flexible long terminal stretches of amino acids, often because those parts of the molecules are not resolved experimentally, or resolved as NMR ensemble with varied positions. It is usually does not hinder the quality of the prediction. 
 </p>
</details>
<br>

<a class="prompt prompt-question">
Look at the ipTM and pTM scores - do they indicate the 3D structure of the complex is trustworthy?  
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
Look at the PAE matrix - what can you conclude given dark green colour dominates it? Can you explain why there a vertical section of light green appearing in the vicinity of residue 23? 
</a>
<details style="background-color:#DAE4E7">
 <summary style="bold">
   <i>Answer</i> <i class="material-icons">expand_more</i>
 </summary>
 <p>
    Dark green colour is indicative of a low predicted position error, i.e. the relative position of the pairs of tokens. The area corresponding to the peptide structure displaying very low predicted error, overall, with code residues having higher confidence compared to the terminal ones. 

    A light-coloured vertical section corresponding to the N-ter of MDM2, residues 1 to ~16. This tail can flop move around without impacting overall structure, so its' predicted position error is high. You can compare its' position between all 5 generated models - it is extremely likely to differ between those models.  
 </p>
</details>
<br>

<a class="prompt prompt-info">
    Download results of AF Server using a button above the plDDT scale.  
    Unpack zip file. Open all 5 cif models in PyMOL, check the difference between all 5 models and their pLDDT values. 
</a>

Align models, and colour them by b-factor visualize pLDDT values per atom. 
<a class="prompt prompt-pymol">
    alignto fold_p53_mdm2_model_0 and chain B
</a>
<a class="prompt prompt-pymol">
    spectrum b
</a>

<a class="prompt prompt-info">
    Examine the other files present in the results folder. If you need a refreshment on the content of the files and/or meaning behind the metrics - don't hesitate to consult a Guide page of the server or EMBL guide.
</a>

*add paragraph about limitations of AF3 and other tools and knowledge on classical modelling is required*