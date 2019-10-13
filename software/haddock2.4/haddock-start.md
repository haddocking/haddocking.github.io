---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK2.4</font>

## <font color="RED">P</font>roject <font color="RED">S</font>etup

* * *



* **[Generate AIR restraint file](/software/haddock2.4/generate_air)**    ([Help](/software/haddock2.4/generate_air_help))



* **[Generate AIR restraint file for multibody docking](http://haddock.science.uu.nl/services/GenTBL)**



* **[Start a new project](/software/haddock2.4/start_new)**     ([Help](/software/haddock2.4/start_new_help))


* **Edit your run.cns file**      ([Help](/software/haddock2.4/run))


    **For editing your run.cns file enter the absolute path of your run.cns file** (e.g. */software/haddock/example/e2a-hpr/run1/run.cns*)

<form method="POST" action="http://milou.science.uu.nl/cgi/servicesdevel/HADDOCK2.2/cns_inp2form_0.3.cgi" target="newwindow" enctype="multipart/form-data"><input name="cns_file" type="file" size="25">

<br>
<br>
<input type="SUBMIT" value="Edit file"><input type="RESET">
(Note: if the file does not display try using Firefox)
<br>
<br>
Type <b>haddock2.4</b> on the UNIX command line in the directory where you have saved your <i>run.cns</i>.

<HR>

HADDOCK also offers support for DNA. If one of the molecules is DNA and defined as DNA
in <i>run.cns</i> HADDOCK expects to find a file called
<i>dna-rna_restraints.def</i> in the <i>data/sequence</i> directory</i>. This file allows
you to define standard A-, B- or custom restraints for DNA such as base-pairing,
puckering and backbone dihedral angles. You can edit using the same
mechanism as for <i>run.cns</i> (see above) a template file that can be found in
the <i>protocols</i> directory. Save the file as <i>dna-rna_restraint.def</i> into the
<i>data/sequence</i> directory.
<BR>
<BR>

<b>Note:</b> This dna-rna_restraint.def is automatically generated when using our <u><a href="http://haddock.science.uu.nl/enmr/services/3DDART">3D-DART web server</a></u> to create and manipulate DNA models.
