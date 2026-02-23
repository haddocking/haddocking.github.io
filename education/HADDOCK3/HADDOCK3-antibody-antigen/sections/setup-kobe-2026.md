### ASM 2026 HPC/AI school, Kobe, Japan, February 2026


<details>
  <summary style="font-weight:bold; cursor:pointer;">
    <i>click to expand</i>
  </summary>
You can either:

 * make use of the Fugaku supercomputer for this tutorial, working at the command line,
 * or [start a Colab notebook](https://colab.research.google.com/github/haddocking/haddock3/blob/main/notebooks/HADDOCK3-antibody-antigen.ipynb){:target="_blank"} (provided you have Google credentials) and follow the instructions in that notebook (simpler).


If running on Fugaku, the software and data required for this tutorial have been pre-installed.
Please connect to Fugaku using your credentials either via ssh connection or from a web browser using OnDemand:

[https://ondemand.fugaku.r-ccs.riken.jp/](https://ondemand.fugaku.r-ccs.riken.jp/){:target="_blank"}

<a class="prompt prompt-info">
If using OnDemand, open then a terminal session, requiring one node and 48 processes and change the working directory to your directory under _/vol0300/data/hp250477/Students/..._.
</a>

In order to run the tutorial, go into you data directory, then copy and unzip the required data:

<a class="prompt prompt-cmd">
unzip /vol0300/data/hp250477/Materials/Life_Science/20260202-HADDOCK/HADDOCK3-antibody-antigen.zip
</a>

This will create the `HADDOCK3-antibody-antigen` directory with all necessary data and scripts and job examples ready for submission to the batch system.

HADDOCK3 has been pre-installed on the compute nodes. To test the installation, first create an interactive session on a node with:


<a class="prompt prompt-cmd">
pjsub \-\-interact \-L \"node=1\" \-L \"rscgrp=int\" \-L \"elapse=2:00:00\"  \-\-sparam \"wait-time=600\"  \-g hp250477 \-x PJM_LLIO_GFSCACHE=/vol0003:/vol0004
</a>

Once the session is active, activate HADDOCK3 with:

<a class="prompt prompt-cmd">
source /vol0300/data/hp250477/Materials/Life_Science/20260202-HADDOCK/haddock3/.venv/bin/activate<br>
</a>

You can then test that `haddock3` is indeed accessible with:

<a class="prompt prompt-cmd">
haddock3 -h
</a>

You should see a small help message explaining how to use the software.

<details style="background-color:#DAE4E7">
  <summary>
  <i>View output</i><i class="material-icons">expand_more</i>
 </summary>
<pre>
(haddock3)$ haddock3 -h
usage: haddock3 [-h] [--restart RESTART] [--extend-run EXTEND_RUN] [--setup]
                [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-v]
                recipe

positional arguments:
  recipe                The input recipe file path

optional arguments:
  -h, --help            show this help message and exit
  --restart RESTART     Restart the run from a given step. Previous folders from the
                        selected step onward will be deleted.
  --extend-run EXTEND_RUN
                        Start a run from a run directory previously prepared with the
                        `haddock3-copy` CLI. Provide the run directory created with
                        `haddock3-copy` CLI.
  --setup               Only setup the run, do not execute
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
  -v, --version         show version
</pre>
</details>
<br>
</details>
