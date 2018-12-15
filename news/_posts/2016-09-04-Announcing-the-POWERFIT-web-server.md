---
layout: news
title: Announcing the POWERFIT web server
date: 2016-09-04
excerpt: PowerFit fits your 3D structures in any map
tags: [HADDOCK, POWERFIT, Utrecht University, Alexandre Bonvin, Docking]
image:
  feature:
---

We are glad to announce the release of our [POWERFIT web server](http://milou.science.uu.nl/services/POWERFIT). 

PowerFit automatically fits high-resolution atomic structures in cryo-EM densities. To this end it performs a full-exhaustive 6-dimensional cross-correlation search between the atomic structure and the density. It takes as input an atomic structure in PDB-format and a cryo-EM density with its resolution; and outputs positions and rotations of the atomic structure corresponding to high correlation values. PowerFit uses the local cross-correlation function as its base score, enhanced by a Laplace pre-filter and/or core-weighting to minimize overlapping densities from neighboring subunits.

<figure align="center">
    <img src="/images/posts/powerfit.png">
</figure>

Read more about PowerFit in the following publications:

* G.C.P. van Zundert and **A.M.J.J. Bonvin**.
[Fast and sensitive rigid-body fitting into cryo-EM density maps with PowerFit](https://doi.org/doi:10.3934/biophy.2015.2.73).
_AIMS Biophysics_. *2*, 73-87 (2015).

* G.C.P van Zundert and  **A.M.J.J. Bonvin**.
[Defining the limits and reliability of rigid-body fitting in cryo-EM maps using multi-scale image pyramids](https://doi.org/10.1016/j.jsb.2016.06.011).
_J. Struct. Biol._, *195*, 252-258 (2016).
	
POWERFIT is also freely available for local installation through our GitHub repository: [https://github.com/haddocking/powerfit](https://github.com/haddocking/powerfit). 
A Docker container is available from the [INDIGO-Datacloud](http://www.indigo-datacloud.eu) repository: [https://github.com/indigo-dc/docker-powerfit](https://github.com/indigo-dc/docker-powerfit).

The POWERFIT web server is powered by EGI ([www.egi.eu](http://www.egi.eu)) GPGPU HTC resources. 


Its development was made possible with support from various grants: 

 - Netherlands Organization for Scientific Research (NWO), ECHO grant no.711.011.009
 - European H2020 e-Infrastructure grant, [EGI-Engage](http://www.egi.eu), grant no. 654142
 - European H2020 e-Infrastructure grant, [INDIGO-DataCloud](http://www.indigo-datacloud.eu), grant no. 653549
 - European H2020 e-Infrastructure grant, [West-Life VRE](http://www.westlife.eu), grant no. 675858
 - European H2020 e-Infrastructure grant, [BioExcel](http://www.bioexcle.eu), grant no. 675728
