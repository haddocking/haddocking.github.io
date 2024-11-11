### Local setup (on your own)

If you are installing HADDOCK3 on your own system, check the instructions and requirements below.


#### Installing HADDOCK3

To obtain HADDOCK3, 
fill the registration form, and then follow the [installation instructions](https://www.bonvinlab.org/haddock3/INSTALL.html)or navigate to [its GitHub repository](https://github.com/haddocking/haddock3).


#### Installing CNS

The other required piece of software to run HADDOCK is its computational engine,
CNS (Crystallography and NMR System – [https://cns-online.org](https://cns-online.org){:target="_blank"}).
CNS is freely available for non-profit organizations.
To get access to all features of HADDOCK you will need to compile CNS using the additional files provided in the HADDOCK distribution in the `extras/cns1.3` directory.
Compilation of CNS might be non-trivial. Some guidance on installing CNS is provided on the online HADDOCK3 documentation page [here](https://github.com/haddocking/haddock3/blob/main/docs/CNS.md).

Once CNS has been properly compiled, you will have create a symbolic link or copy the executable to `haddock3/bin/cns` and make sure it is executable and functional.
Try starting `cns` from the command line. You should see the following output:

<details style="background-color:#DAE4E7">
  <summary>
  <i>View CNS prompt output</i><i class="material-icons">expand_more</i>
 </summary>
<pre>
          ============================================================
          |                                                          |
          |            Crystallography & NMR System (CNS)            |
          |                         CNSsolve                         |
          |                                                          |
          ============================================================
           Version: 1.3 at patch level U
           Status: Special UU release with Rg, paramagnetic
                   and Z-restraints (A. Bonvin, UU 2013)
          ============================================================
           Written by: A.T.Brunger, P.D.Adams, G.M.Clore, W.L.DeLano,
                       P.Gros, R.W.Grosse-Kunstleve,J.-S.Jiang,J.M.Krahn,
                       J.Kuszewski, M.Nilges, N.S.Pannu, R.J.Read,
                       L.M.Rice, G.F.Schroeder, T.Simonson, G.L.Warren.
           Copyright (c) 1997-2010 Yale University
          ============================================================
           Running on machine: hostname unknown (Linux,64-bit)
           Program started by: l00902
           Program started at: 16:34:22 on 06-Dec-2023
          ============================================================

 FFT3C: Using FFTPACK4.1

CNSsolve>
</pre>
</details>
<br>
Exit the CNS command line by typing `stop`.
