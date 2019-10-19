---
layout: page
tags: [Jekyll, HADDOCK, Bonvin, Docking, Simulation, Molecular Dynamics, Structural Biology, Computational Biology, Modelling, Protein Structure]
modified: 2014-08-08T20:53:07.573882-04:00
comments: false
image:
  feature: pages/banner_software.jpg
---

# <font color="RED">HADDOCK2.4</font> manual

## <font size="+2">G</font>enerate <font size="+2" color="RED">A</font>mbiguous <font size="+2" color="RED">I</font>nteraction <font size="+2" color="RED">R</font>estraints (<font size="+2" color="RED">AIR</font>s)

<table>

<tbody>

<tr>

<td width="550">  

<form action="http://milou.science.uu.nl/cgi/servicesdevel/HADDOCK2.2/generate_multidock_air.cgi" method="GET">

Define the active and passive residues for each molecule.  
Use blank spaces or commas between residue numbers.

E.g.


<table border="1" cellpadding="5">

<tbody>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Active residues for 1st molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_ACTIVE_1" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Passive residues for 1st molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_PASSIVE_1" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 1st molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_1" value="A" size="4"></td>

</tr>

<tr>

<td colspan="2"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Active residues for 2nd molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_ACTIVE_2" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Passive residues for 2nd molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_PASSIVE_2" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 2nd molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_2" value="B" size="4"></td>

</tr>

<tr>

<td colspan="2"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Active residues for 3rd molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_ACTIVE_3" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Passive residues for 3rd molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_PASSIVE_3" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 3rd molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_3" value="C" size="4"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Active residues for 4th molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_ACTIVE_4" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Passive residues for 4th molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_PASSIVE_4" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 4th molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_4" value="D" size="4"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Active residues for 5th molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_ACTIVE_5" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Passive residues for 5th molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_PASSIVE_5" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 5th molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_5" value="E" size="4"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Active residues for 6th molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_ACTIVE_6" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Passive residues for 6th molecule:</td>

<td colspan="1" align="left"><input type="text" name="AIR_PASSIVE_6" value="" size="50"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Segid of 6th molecule:</td>

<td colspan="1" align="left"><input type="text" name="PROT_SEGID_6" value="F" size="4"></td>

</tr>

<tr>

<td colspan="2"></td>

</tr>

<tr rowspan="1" align="center">

<td colspan="1" align="left">Upper distance limit for AIRs:</td>

<td colspan="1" align="left"><input type="text" name="AIR_DIST" value="2.0" size="5"></td>

</tr>

</tbody>

</table>

<input type="SUBMIT" name="submit1" value="Generate AIR restraints"> <input type="RESET" value="Reset">

Use "cut and paste" or save the generated AIR restraints to disk using "File save as"

<br>

<font size="-1">

Please send any suggestions or enquiries to Alexandre Bonvin</font></form>

</td>

</tr>

</tbody>

</table>
