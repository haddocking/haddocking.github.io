---
layout: page
title: ""
excerpt: ""
tags: [HADDOCK, HADDOCK3, installation, preparation, proteins, docking, analysis, workflows, manual, usage]
image:
  feature: pages/banner_software.jpg
---

* table of contents
{:toc}

<hr>

# Workflow configuration file

Haddock3 is using a configuration file to define the workflow to be performed.
A workflow is defined in simple configuration text files, similar to the [TOML](https://toml.io/en/) format but with extra features.

It basically contains two main parts:
* [Global parameters](/software/haddock3/manual/global_parameters): General parameters to be applied to the workflow, including input molecules and location where to run the docking protocol.
* [List of modules](/software/haddock3/manual/modules_parameters): Sequence of [module names], defining the sequential order in which each module must be perfromed. Each module has several parameters, that can be defined to fine tune them, or left untouched therefore using default parameters.

Examples of workflow configuration files are [available here !](https://github.com/haddocking/haddock3/tree/main/examples)
