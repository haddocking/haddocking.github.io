---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK 2.4</font> manual

## <font color="RED">A</font>mbiguous <font color="RED">I</font>nteraction <font color="RED">R</font>estraints (<font color="RED">AIR</font>s)

* * *

*   [General](#general)  
*   [Use of bioinformatic interface predictions](#predictions)   
*   [Random AIR definition (ab-initio mode)](#ranair)
*   [Surface contact restraints](#surf)
*   [Center of mass restraints](#cm)
*   [Use of NMR chemical shift perturbation data](#CSP)  


    <a name="predictions">**General:**</a>  

    Before starting HADDOCK, <font color="RED">A</font>mbiguous <font color="RED">I</font>nteraction <font color="RED">R</font>estraints (<font color="RED">AIR</font>s) should be generated. For this, it is important to define the residues at the interface for each molecule based on NMR chemical shift perturbation data, mutagenesis data or any kind of data that provides information on the interaction interface.  
    In the definition of those residues, one distinguishes between ***"active"*** and ***"passive"*** residues.  

    *   The ***"active"*** residues are those experimentally identified to be involved in the interaction between the two molecules **AND** solvent accessible (either main chain or side chain relative accessibility should be typically > 40-50%).
    **Note**

    *   The ***"passive"*** residues are all solvent accessible surface neighbors of active residues.  

    **Note** that the active and passive residues have to be defined by the users based on their own interpretation of the experimental data, especially in the case of NMR titration data. One way to interpret the significance of the shift is to calculate the average perturbation and to consider that all perturbations higher than the average are significant.  

    Once you have defined your active and passive residues,
    *   go to the [HADDOCK online page](/software/haddock2.4/haddock-start) (http://www.bonvinlab.org/software/haddock2.4/haddock-start)  

    *   and click on "Generate AIR restraint file" (or in case of multibody docking, use the specific option)  

    *   Enter the residue numbers corresponding to the active and passive residues for each molecule.  

    *   Define the upper distance limit for AIRs (maximum distance between any atom of an active residue of one molecule to any atom of an active or passive residue of the second molecule).  

        **Note** that the current upper distance limit default value is 2A, which might seem quite short, BUT remember that the effective distance d<sub>eff</sub> will always be shorter than the shortest distance entering the sum:  

        d<sub>eff</sub>=[Sum(1/r<sup>6</sup>)]<sup>-1/6</sup>

        In addition since the degree of ambiguity is very high (several thousands distances can enter the sum), the effective distance can be quite shorter than the shortest distance entering the sum!!!  

    *   Finally, click on generate AIR restraints. An AIR restraint file in CNS format is generated. Use "copy and paste" or save the generate AIR restraints to disk using "file save as".

    * * *

    <a name="predictions">**Use of bioinformatic interface predictions:**</a>  

    In absence of any experimental information on the interaction surfaces, you might want to try to predict them based on sequence conservation and other properties. We have developed for this purpose interface prediction softwares called [WHISCY](http://www.nmr.chem.uu.nl/whiscy) and [CPORT](http://haddock.science.uu.nl/services/CPORT). They has been designed to provide an easy interface to HADDOCK and will output, among others, lists of active and passive residues for HADDOCK. CPORT is a meta predictor that integrates results from various other servers.

    For more information refer to:  

    *   S.J. de Vries, A.D.J. van Dijk and A.M.J.J. Bonvin  
        [WHISCY: WHat Information does Surface Conservation Yield? Application to data-driven docking.](https://doi.org/doi:10.1002/prot.20842), _Proteins: Struc. Funct. & Bioinformatics_, **63**, 479-489 (2006).  

    *   S.J. de Vries and A.M.J.J. Bonvin  
        [CPORT: a Consensus Interface Predictor and its Performance in Prediction-driven Docking with HADDOCK.](https://doi.org/doi:10.1371/journal.pone.0017695), _PlosONE_, **6** e17695 (2011).

    * * *

    <a name="ranair">**Random AIR definition (ab-initio mode):**</a>  

    In the absence of any experimental and/or bioinformatic information to drive the docking, HADDOCK 2.x now offers the possibility to randomly define AIRs from solvent accessible residues (>20% relative accessibility). For each docking trial another set of AIRs will be used. These restraints are defined in the _randomairs.cns_ CNS script.  

    The sampling of residues is limited to the defined semi-flexible segments (_nseg_X_ and following parameters in [run.cns](/software/haddock2.4/run)). If no semi-flexible segment is defined, then all solvent accessible residues will be sampled (provided enough structures are generated in the rigid-body docking stage (it0)). By defining semi-flexible segments in combination with random AIR definition (_ranair=true_ in [run.cns](/software/haddock2.4/run)), it is possible to limit the sampling to a selected region of the surface (e.g. the CDR loops in an antibody-antigen complex).  

    The random AIRs are defined (in the _randomairs.cns_ CNS script) as follow (only for the rigid-body energy minimization stage):
    1.  One residue on each molecule is selected randomly (Ai,Bi)
    2.  All surface neighbors within 5A are also selected
    3.  AIRs are defined between each residue selected from molecule A (Ai + 5A neighbors) and the first residue randomly selected from molecule B and all its surface neighbors within a 7.5A cutoff (Bi + 7.5A neighbors)
    4.  AIRs are defined between each residue selected from molecule B (Bi + 5A neighbors) and the first residue randomly selected from molecule A and all its surface neighbors within a 7.5A cutoff (Ai + 7.5A neighbors)AIRs are thus defined from a 5A radius patch randomly selected from one molecule to a 7.5A radius patch randomly selected on the second molecule and vice-versa. The selected residues are written to disk in _**structures/it0**_ as _fileroot_1.disp,..._.  

    For the semi-flexible refinement stage, contact AIRs are automatically defined between all residues within 5A across the interface. In the final explicit solvent refinement, no AIR restraints will be defined.  
    *   **Note1:** To ensure a thorough sampling of the surface, the number of structures generated at the rigid-body stage (it0) should be increased (e.g. 10000), depending on the extent of the surface to be sampled.   

        **Note2:** The use of random AIRs is not compatible with other distance restraints (including unambiguous and hydrogen bond restraints).  

    * * *

    <a name="surf">**Surface contact restraints:**</a>  

    Surface contact restraints between the various molecules can be automatically defined in HADDOCK 2.x (_surfrest=true_ in [run.cns](/software/haddock2.4/run)). These restraints are defined in the _surf-restraint.cns_ CNS script. This option is fully compatible with all other types of restraints.

    If turned on, one surface contact restraint will be defined between each molecule as an ambiguous distance restraint with sum averaging (as for the AIRs) between all CA or P atoms (protein and/or DNA) of one molecule and all CA or P atoms of the other molecule. If less than 3 CA and P atoms are found, all atoms will be selected instead. The upper distance limit is set to either 7A (both molecules contain CA and/or P atoms) or 4.5A (only one molecule contains CA and/or P atoms) or 2A (no molecule contains CA and/or P atoms).

    Such restraints can be useful in multi-body (N>2) docking to ensure that all molecules are in contact and thus promote compactness of the docking solutions. As for the [random AIRs](#ranair), surface contact restraints can be used in ab-initio docking; in such a case it is important to have enough sampling of the random starting orientations and this significantly increases the number of structures for rigid-body docking.  

    * * *

    <a name="cm">**Center of mass restraints:**</a>  

    Center of mass restraints between the various molecules can be automatically defined in HADDOCK 2.x (_cmrest=true_ in [run.cns](/software/haddock2.4/run)). These restraints are defined in the _cm-restraint.cns_ CNS script. This option is fully compatible with all other types of restraints.

    If turned on, one center of mass restraint will be defined between each molecule as an ambiguous distance restraint with center averaging between all CA or P atoms (protein and/or DNA) of one molecule and all CA or P atoms of the other molecule. If less than 3 CA and P atoms are found, all atoms will be selected instead. The upper distance limit is automatically defined as the sum of the "effective radius" of each molecule. The "effective radius" is defined as half the average length of the three principal components.  
    Such restraints can be useful in multi-body (N>2) docking to ensure that all molecules are in contact and thus promote compactness of the docking solutions. As for the [random AIRs](#ranair), center of mass restraints can be used in ab-initio docking; in such a case it is important to have enough sampling of the random starting orientations and this increase significantly the number of structures for rigid-body docking.  

    * * *

    <a name="CSP">**Use of NMR chemical shift perturbation data:**</a>  

    We will here illustrate the process of defining AIRs in the case of NMR chemical shift perturbation data (CSP) describing the following steps:
    *   [Defining residues with _"significant"_ chemical shift perturbations](#define)
    *   [Filtering active residues with solvent accessibility](#filter)
    *   [Defining passive residues](#passive)
    *   [Residue filtering from an ensemble of structures](#ensemble)
    *   [Generating the AIR restraint file](#generate)    
<br>

    **1.** <a name="define">**Defining residues with _"significant"_ chemical shift perturbations**</a>  

    We will assume that we have a file called _csp.dat_ containing the combined proton/nitrogen chemical shift changes as obtained from 15N HSQC titration experiments in the following format:

    <pre style="background-color:#DAE4E7" >    1 0.0
        2 0.0
        3 0.06
        4 0.3
        ...
    </pre>

    The first column corresponds to the residue number and the second to the combined chemical shift perturbation.  
    HADDOCK comes with a number of awk,csh and perl scripts to handle and analyze data. To calculate the average perturbation use the average.perl script located in $HADDOCKTOOLS (see [installation](/software/haddock2.4/installation)). The following command will give you the average of the second column of the above file:

    <pre style="background-color:#DAE4E7" >    awk '{print $2}' csp.dat | $HADDOCKTOOLS/average.perl
    </pre>

    Select then all residues that have a combined chemical shift perturbation larger than for example the average value _avcsp_:

    <pre style="background-color:#DAE4E7" >   awk '{if ($2>avcsp) print $0}' csp.dat
    </pre>

    This will list you all the residues selected.  
    The next step consists of filtering those residues according to their solvent accessibility.  

    **2.** <a name="filter">**Filtering active residues with solvent accessibility**</a>  
    An important parameter in defining AIRs consists of the relative residue solvent accessibility. It can be calculated with the program [NACCESS](http://wolf.bms.umist.ac.uk/naccess) (see [software links](/software/haddock2.4/software)).

    NACCESS will output a file with extension _.rsa_ containing the per- residue solvent accessibilities divided into various classes:

    <pre style="background-color:#DAE4E7" > <font size="-2">REM RES _ NUM      All-atoms   Total-Side   Main-Chain    Non-polar    All polar
        REM                ABS   REL    ABS   REL    ABS   REL    ABS   REL    ABS   REL
        RES MET     1   125.45  64.6  75.64  48.3  49.81 132.8  75.64  47.9  49.81 137.1
        RES PHE     2    83.49  41.9  83.49  50.9   0.00   0.0  83.49  50.5   0.00   0.0
        RES GLN     3    79.31  44.4  62.47  44.2  17.04  45.4  17.75  34.0  61.56  48.7
        RES GLN     4    83.82  47.0  83.82  59.4   0.00   0.0  15.03  28.8  68.79  54.5
        RES GLU     5   133.48  77.5 100.65  74.7  32.83  87.5  34.78  57.7  98.70  88.2
        RES VAL     6    20.78  13.7  20.78  18.2   0.00   0.0  20.78  18.0   0.00   0.0
        ...</font>
    </pre>

    Only the high solvent accessible amino acids should be selected. The selection can be done either on the all-atoms accessibilities (e.g. >40%) using the following command at the Unix prompt:

    <pre style="background-color:#DAE4E7">    awk '{if (NF==13 && $5>40) print $0; if (NF==14 && $6>40) print $0}' pdb_filename.rsa
    </pre>

    or by requesting that either the main-chain or the side-chain relative accessibility be larger than 50%:

    <pre style="background-color:#DAE4E7">   awk '{if (NF==13 && ($7>40 || $9>40)) print $0; if (NF==14 && ($8>40 || $10>40)) print $0}' pdb_filename.rsa
    </pre>

    By combining the experimental data (mutagenesis or chemical shift perturbation) and the solvent accessibility, you should be able to define precisely the active residues to use in HADDOCK.  

    **3.** <a name="passive">**Defining passive residues**</a>  
    The passive residues are all solvent accessible surface neighbors of active residues. To define them you can display your molecule in space-filling model ([rasmol](http://www.umass.edu/microbio/rasmol) will do) and color the active residues for example in red.


    |<img src="/software/haddock2.4/hpr-csp-filtered.gif"  width="250"> |  Then, filter out the residues having a low solvent accessibility   (colored yellow in the figure). |
    |<img src="/software/haddock2.4/hpr-passive-filtered.gif"  width="250">| Select then all surface neighbors to define the passive residues (colored green in the figure). |
    |<img src="/software/haddock2.4/hpr-passive.gif" width="250">|  and filter them with the solvent accessibility criterion (see above).|




    **Note:** If you are using an ensemble of structures as the starting point, you should use the average solvent accessibility to filter your active and passive residues (see [below](#ensemble)).  

    **4.** <a name="ensemble">**Residue filtering from an ensemble of structures**</a>  
    If you perform the docking from an ensemble of structures, the solvent accessibility filtering should be performed using the average relative accessibilities ASAav over the ensemble. In such a case we are using the following accessibility cut-off:  

    **ASAav + SD > 40%**

    where SD corresponds to the standard deviation.  
    We are providing in the $HADDOCKTOOLS directory a csh script called _calc_ave_asa.csh_ that will allow you to calculate the average accessibilities from an ensemble of structures using [NACCESS](http://wolf.bms.umist.ac.uk/naccess).  
    To do so, you should split your pdb file into different files containing each one structure and then use calc_ave_rsa.csh:

    <pre style="background-color:#DAE4E7" >    $HADDOCKTOOLS/calc_ave_rsa.csh *.pdb
    </pre>

    A file named *"rsa_ave.lis"* will be created that contains the average solvent accessibility and the standard deviation for each residue:

    <pre style="background-color:#DAE4E7" > <font size="-2"># resnam resnum < rsa_all > (sd) < rsa_back > (sd) < rsa_side > (sd)
    MET      1  69.323   10.370  125.390   13.626   55.903   12.599
    PHE      2  37.490    5.216    0.320    0.753   45.500    6.390
    GLN      3  53.793    8.246   50.147   14.108   54.770   10.873
    GLN      4  40.907    5.578    0.070    0.306   51.757    7.042
    GLU      5  70.330    6.312   68.017   15.608   70.963    7.614
    VAL      6  16.183    4.345    0.133    0.483   21.397    5.791
    ...</font> </pre>

    To select the residues that satisfy the 40% accessibility cut-off type:

    <pre style="background-color:#DAE4E7" >    awk '{if (($5+$6)>=40 || ($7+$8)>=40) print $0}' rsa_ave.lis
    </pre>

    **Note** that the 40% cut-off is not a hard limit and is left to the user choice.  

    **5.** <a name="generate">**Generating the AIR restraints file**</a>  
    Once you have defined your active and passive residues, go to the [HADDOCK online page](/software/haddock2.4/haddock-start) (http://www.bonvinlab.org/software/haddock2.4/haddock-start) and click on "Generate AIR restraint file"  
    Enter the residue numbers corresponding to the active and passive residues for each molecule.  

    You can define the upper distance limit for AIRs (maximum distance between any atom of an active   residue of one molecule to any atom of an active or passive residues of the second molecule).  

    click on generate AIR restraints. An AIR restraint file in CNS format is generated. Use "copy and paste" or save the generate AIR restraints to disk using "file save as".

* * *
