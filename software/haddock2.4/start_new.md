---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK2.4</font>

## <font color="RED">S</font>tart a <font color="RED">N</font>ew <font color="RED">P</font>roject

* * *

You have to specify **absolute** paths for all files and directories. Unused fields should be **blank**. You need to specify at least one PDB file (although this will not be called "docking"...).  

<form action="http://milou.science.uu.nl/cgi/servicesdevel/HADDOCK2.2/start_haddock_project.cgi" method="POST">

<table border="1" cellpadding="5">

<tbody>

<tr rowspan="1" align="center">

<td colspan="2" align="left" >  <b>HADDOCK and project setup:</b> </td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Current HADDOCK program directory:</td>

<td colspan="1" align="left"><input type="text" name="HADDOCK_DIR" value="/home/software/haddock2.4" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Path of the new project:</td>

<td colspan="1" align="left"><input type="text" name="PROJECT_DIR" value="/home/software/haddock2.4/examples/protein-protein" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Run number:</td>

<td colspan="1" align="left"><input type="text" name="RUN_NUMBER" value="1" size="3"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Number of molecules for docking (max. 6):</td>

<td colspan="1" align="left"><input type="text" name="N_COMP" value="2" size="3"></td>

</tr>

<tr>

<td colspan="2"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="2" align="left"> <b>Define the various molecules for docking:</b> </td>

</tr>

<tr>

<td colspan="2"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PDB file of 1st molecule:</td>

<td colspan="1" align="left"><input type="text" name="PDB_FILE1" value="/home/software/haddock2.4/examples/protein-protein/e2a_1F3G.pdb" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PDB file of 2nd molecule:</td>

<td colspan="1" align="left"><input type="text" name="PDB_FILE2" value="/home/software/haddock2.4/examples/protein-protein/hpr_1.pdb" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PDB file of 3rd molecule:</td>

<td colspan="1" align="left"><input type="text" name="PDB_FILE3" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PDB file of 4th molecule:</td>

<td colspan="1" align="left"><input type="text" name="PDB_FILE4" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PDB file of 5th molecule:</td>

<td colspan="1" align="left"><input type="text" name="PDB_FILE5" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PDB file of 6th molecule:</td>

<td colspan="1" align="left"><input type="text" name="PDB_FILE6" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 1st molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_1" value="A" size="4"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 2nd molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_2" value="B" size="4"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 3rd molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_3" value="C" size="4"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 4th molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_4" value="D" size="4"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 5th molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_5" value="E" size="4"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 6th molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_6" value="F" size="4"></td>

</tr>

<tr rowspan="2">

<td colspan="1"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="2" align="left"> <i>The next six entries are optional and only required to run HADDOCK from ensemble of structures. The list files should contain the full path and each filename (including path) should be between quotes. </i> </td>

</tr>

<tr rowspan="2">

<td colspan="1"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">file list for 1st molecule (opt.):</td>

<td colspan="1" align="left"><input type="text" name="PDB_LIST1" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">file list for 2nd molecule (opt.):</td>

<td colspan="1" align="left"><input type="text" name="PDB_LIST2" value="/home/software/haddock2.4/examples/protein-protein/hpr-files.list" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">file list for 3rd molecule (opt.):</td>

<td colspan="1" align="left"><input type="text" name="PDB_LIST3" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">file list for 4th molecule (opt.):</td>

<td colspan="1" align="left"><input type="text" name="PDB_LIST4" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">file list for 5th molecule (opt.):</td>

<td colspan="1" align="left"><input type="text" name="PDB_LIST5" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">file list for 6th molecule (opt.):</td>

<td colspan="1" align="left"><input type="text" name="PDB_LIST6" value="" size="60"></td>

</tr>

<tr>

<td colspan="2"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="2" align="left"> <b>Define the various restraint files:</b> </td>

</tr>


<tr rowspan="1">

<td colspan="2"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">AIR restraints:</td>

<td colspan="1" align="left"><input type="text" name="AMBIG_TBL" value="/home/software/haddock2.4/examples/protein-protein/e2a-hpr_air.tbl" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">distance restraints:</td>

<td colspan="1" align="left"><input type="text" name="UNAMBIG_TBL" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Dihedral angle restraints:</td>

<td colspan="1" align="left"><input type="text" name="DIHED_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Hbonds restraints:</td>

<td colspan="1" align="left"><input type="text" name="HBOND_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Residual dipolar couplings 1:</td>

<td colspan="1" align="left"><input type="text" name="RDC1_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Residual dipolar couplings 2:</td>

<td colspan="1" align="left"><input type="text" name="RDC2_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Residual dipolar couplings 3:</td>

<td colspan="1" align="left"><input type="text" name="RDC3_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Residual dipolar couplings 4:</td>

<td colspan="1" align="left"><input type="text" name="RDC4_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Residual dipolar couplings 5:</td>

<td colspan="1" align="left"><input type="text" name="RDC5_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 1:</td>

<td colspan="1" align="left"><input type="text" name="PCS1_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 2:</td>

<td colspan="1" align="left"><input type="text" name="PCS2_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 3:</td>

<td colspan="1" align="left"><input type="text" name="PCS3_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 4:</td>

<td colspan="1" align="left"><input type="text" name="PCS4_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 5:</td>

<td colspan="1" align="left"><input type="text" name="PCS5_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 6:</td>

<td colspan="1" align="left"><input type="text" name="PCS6_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 7:</td>

<td colspan="1" align="left"><input type="text" name="PCS7_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 8:</td>

<td colspan="1" align="left"><input type="text" name="PCS8_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 9:</td>

<td colspan="1" align="left"><input type="text" name="PCS9_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS restraints 10:</td>

<td colspan="1" align="left"><input type="text" name="PCS10_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">PCS tensor distance restraints file:</td>

<td colspan="1" align="left"><input type="text" name="TENSOR_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Diffusion anisotropy restraints 1:</td>

<td colspan="1" align="left"><input type="text" name="DANI1_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Diffusion anisotropy restraints 2:</td>

<td colspan="1" align="left"><input type="text" name="DANI2_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Diffusion anisotropy restraints 3:</td>

<td colspan="1" align="left"><input type="text" name="DANI3_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Diffusion anisotropy restraints 4:</td>

<td colspan="1" align="left"><input type="text" name="DANI4_FILE" value="" size="60"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Diffusion anisotropy restraints 5:</td>

<td colspan="1" align="left"><input type="text" name="DANI5_FILE" value="" size="60"></td>

</tr>

</tbody>

</table>

<br>

<b>Save the updated parameters somewhere in a directory as <i>new.html</i></b>
(use your browser *save as* menu if necessary).  

<input type="SUBMIT" name="submit_save" value="Save updated parameters"> <input type="RESET" value="Reset">  

<hr>

Type <b>haddock2.4</b> on the UNIX command line in the directory where you have saved your <i>new.html</i> file.

<hr>

</form>
