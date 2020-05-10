---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
title: HADDOCK2.4 manual - Defining a radius of gyration restraint
image:
  feature: pages/banner_software.jpg
---

A radius of gyration distance restraint can be turned on here. It will be active throughout the entire protocol, but can be effectively turned off by setting the force constant for a given stage to 0. The radius of gyration should be entered in angstrom. By default it is applied to the entire system, but can be restricted to part of the system using standard CNS atom selections.

For example to limit it to chains B and C define: "(segid B or segid C)".

To activate this type of restraints set *rgrest=true* in [*run.cns*](/software/haddock2.4/run){:target="_blank"} and specify the radius of gyration and the selection to which it applies.


<pre style="background-color:#D2AE4E7"> 
{=========================== radius of gyration restraint  ============}
{* Turn on/off and energy constants for Rg restraints *}
{* Do you want to define a radius of gyration restraint (e.g. from SAXS)? *}
{+ choice: true false +}
{===>} rgrest=false;

{* Radius of gyration *}
{===>} rgtarg=17.78;

{* Force constant for radius of gyration restraint *}
{===>} krg_hot=100.0;
{===>} krg_cool1=100.0;
{===>} krg_cool2=100.0;
{===>} krg_cool3=100.0;

{* Atom selections for the radius of gyration restraint *}
{===>} rgsele="all";
</pre>


A radius of gyration could be derived from SAXS data for example. This type of restraint, which has not been thorougly tested, does not seem to add much to the docking results.

* * *
