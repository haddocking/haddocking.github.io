## Glycans

<p align="right">
  <img src="/software/bpg/bound_glycan.png" />
</p>

<p style='text-align: right; font-family: "PT Sans"; font-weight: 600;'> <font  size="6" color="RED" >Best practice guide</font></p>

HADDOCK2.4 now supports docking of carbohydrates, however it has not been tested properly yet. It is in an experimental intense-development phase.
A list of glycan residues supported by HADDOCK can be found [here](https://wenmr.science.uu.nl/haddock2.4/library). This page consists of following chapters:


<hr>

### [Tutorials](/education/)

<HR>

### [Publications](/publications/)


<hr>

### [Optimal settings for docking of glycans](https://wenmr.science.uu.nl/haddock2.4/settings#glycans)

<style>
table, th, td {
    padding: 5px;
  table-layout: fixed ;
  width: 100% ;
}
</style>


|<font size="4" color="#203A98">Parameter</font>|<font size="4" color="#203A98">run.cns name</font>| <font size="4" color="#203A98">default value</font>|<font size="4" color="#203A98">optimal value</font> |
|-|:-:|:-:|:-:| 
|**Clustering method** | <code> clust_meth</code>| FCC | **RMSD** |   
|**Cutoff for clustering** | <code> clust_cutoff </code>| 0.6 | **2.5** |  

More about optimal settings for different docking scenarios can be found [here](https://wenmr.science.uu.nl/haddock2.4/settings#optimal).


<hr>

### [FAQ](/software/haddock2.4/faq/)

Any more questions about glycan docking with HADDOCK? Have a look at our **[HADDOCK bioexcel forum](https://ask.bioexcel.eu/search?q=glycan%20category%3A6)**  hosted by [<img width="70" src="/images/Bioexcel_logo.png">](https://bioexcel.eu). There is a very high chance that your problem has already been addressed. 
