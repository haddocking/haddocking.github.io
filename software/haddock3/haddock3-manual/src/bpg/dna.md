## DNA and RNA

<p align="right">
  <img src="/software/bpg/bound_dna.png" />
</p>

<p style='text-align: right; font-family: "PT Sans"; font-weight: 600;'> <font  size="6" color="RED" >Best practice guide</font></p>


HADDOCK can perform docking of nucleic acids. Currently there are no tutorials focused on docking of nucleic acids into proteins, but we are working on it. The list of nucleic acid bases supported by HADDOCKis listed [here](https://wenmr.science.uu.nl/haddock2.4/library). This page consists of following chapters:
 

<hr>

### [Publications](/publications/)

* Z. Kurkcuoglu and **A.M.J.J. Bonvin**. [Pre- and post-docking sampling of conformational changes using ClustENM and HADDOCK for protein-protein and protein-DNA systems](https://doi.org/10.1002/prot.25802). _Proteins: Struc. Funct. &amp; Bioinformatics_, *88*, 292-306 (2020).

* R.V. Honorato, J. Roel-Touris and **A.M.J.J. Bonvin**. [MARTINI-based protein-DNA coarse-grained HADDOCKing](https://doi.org/10.3389/fmolb.2019.00102). _Frontiers in Molecular Biosciences_, *6*, 102 (2019).

* M. van Dijk, K. Visscher, P.L. Kastritis and **A.M.J.J. Bonvin**.
[Solvated protein-DNA docking using HADDOCK.](https://doi.org/doi:10.1007/s10858-013-9734-x)
_J. Biomol. NMR_, *56*, 51-63 (2013).


* M. van Dijk and **A.M.J.J. Bonvin**
[Pushing the limits of what is achievable in protein-DNA docking. Benchmarking HADDOCK's performance.](https://doi.org/doi:10.1093/nar/gkq222)_Nucl. Acid Res._, *38*, 5634-5647 (2010).

* M. van Dijk and **A.M.J.J. Bonvin**
[A protein-DNA docking benchmark.](https://doi.org/doi:10.1093/nar/gkn386)
_Nucl. Acids Res._ (2008), *36*, e88, doi: 10.1093/nar/gkn386.

* M. van Dijk, A.D.J. van Dijk, V. Hsu, R. Boelens and **A.M.J.J. Bonvin**
[Information-driven Protein-DNA Docking using HADDOCK: it is a matter of flexibility.](https://doi.org/doi:10.1093/nar/gkl412)
_Nucl. Acids Res._, *34* 3317-3325 (2006).

<HR>

### [Optimal settings for docking of nucleic acids](https://wenmr.science.uu.nl/haddock2.4/settings#nucleotides)

<style>
table, th, td {
    padding: 5px;
}
</style>


|<font size="4" color="#203A98">Parameter</font>|<font size="4" color="#203A98">run.cns name</font>| <font size="4" color="#203A98" >default value</font>|<font size="4" color="#203A98">optimal value</font> |
|-|:-:|:-:|:-:| 
|**Epsilon constant for the electrostatic energy term in it0** | <code>epsilon_0</code>|  10.0 | **78.0** |   
|**Epsilon constant for the electrostatic energy term in it1** | <code>epsilon_1</code>| 10.0| **78.0** |  


More about optimal settings for different docking scenarios can be found [here](https://wenmr.science.uu.nl/haddock2.4/settings#optimal).

<HR>

### [FAQ](/software/haddock2.4/faq/)

Any more questions about nucleic acids docking with HADDOCK? Have a look at our **[HADDOCK bioexcel forum](https://ask.bioexcel.eu/search?q=dna%20%23haddock)**  hosted by [<img width="70" src="/images/Bioexcel_logo.png">](https://bioexcel.eu). There is a very high chance that your problem has already been addressed. 
