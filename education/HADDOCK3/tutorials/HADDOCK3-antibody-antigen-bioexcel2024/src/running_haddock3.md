
### Running HADDOCK3

In in the first section of the workflow above we have a parameter `mode` defining the execution mode. HADDOCK3 currently supports three difference execution modes:

- **local** : In this mode, HADDOCK3 will run on the current system, using the defined number of cores (`ncores`) in the config file to a maximum of the total number of available cores on the system.
- **batch**: In this mode, HADDOCK3 will typically be started on your local server (e.g. the login node) and will dispatch jobs to the batch system of your cluster (slurm and torque are currently supported).
- **mpi**: HADDOCK3 also supports a pseudo parallel MPI implementation, which allows to harvest the power of multiple nodes to distribute the computations (functional but still very experimental at this stage).


<hr>

#### Learn about the various execution modes of haddock3

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Execution of Fugaku using a full node (EU-ASEAN HPC School)</i></b> <i class="material-icons">expand_more</i>
  </summary>
To execute the workflow on Fugaku, we will create a job file that will execute HADDOCK3 on a node, with HADDOCK3 running in local mode (the setup in the above configuration file with `mode="local"`) and harvesting all core of that node (`ncores=50`).

Here is an example of such an execution script (also provided in the `workflows` directory as `run-haddock3-fugaku.sh`):

{% highlight shell %}
#!/bin/sh
#PJM -g ra022304
#PJM -L "rscgrp=small"
#PJM -L "node=1"
#PJM -L "elapse=01:00:00"
#PJM -x PJM_LLIO_GFSCACHE=/vol0004:/vol0003
#PJM -s # Statistical information output

source /vol0300/share/ra022304/LifeScience/20231213_Bonvin/miniconda3/etc/profile.d/conda.sh
conda activate haddock3

haddock3 docking-antibody-antigen-CDR-NMR-CSP.cfg

{% endhighlight %}

This file should be submitted to the batch system using the `pjsub` command:

<a class="prompt prompt-cmd">
pjsub workflows/run-haddock3-fugaku.sh
</a>
<br>

This run should take about 20 minutes to complete on a single node using 50 arm cores.
</details>


<hr>


<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Local execution</i></b> <i class="material-icons">expand_more</i>
  </summary>

In this mode HADDOCK3 will run on the current system, using the defined number of cores (`ncores`) in the config file to a maximum of the total number of available cores on the system minus one. An example of the relevant parameters to be defined in the first section of the config file is:

{% highlight toml %}
# compute mode
mode = "local"
#  1 nodes x 50 ncores
ncores = 50
{% endhighlight %}

In this mode HADDOCK3 can be started from the command line with as argument the configuration file of the defined workflow.

<a class="prompt prompt-cmd">
haddock3 \<my-workflow-configuration-file\>
</a>

Alternatively redirect the output to a log file and send haddock3 to the background.


As an indication, running locally on an Apple M2 laptop using 10 cores, this workflow completed in 7 minutes.


<a class="prompt prompt-cmd">
haddock3 \<my-workflow-configuration-file\> \> haddock3.log &
</a>

_**Note**_: This is also the execution mode that should be used for example when submitting the HADDOCK3 job to a node of a cluster, requesting X number of cores.

</details>

<hr>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Exection in batch mode using slurm</i></b> <i class="material-icons">expand_more</i>
  </summary>

  Here is an example script for submitting via the slurm batch system:

  {% highlight shell %}
  #!/bin/bash
  #SBATCH --nodes=1
  #SBATCH --tasks-per-node=50
  #SBATCH -J haddock3
  #SBATCH --partition=medium

  # activate the haddock3 conda environment
  source $HOME/miniconda3/etc/profile.d/conda.sh
  conda activate haddock3

  # go to the run directory
  cd $HOME/HADDOCK3-antibody-antigen

  # execute
  haddock3 \<my-workflow-configuration-file\>
  {% endhighlight %}
  <br>


  In this mode HADDOCK3 will typically be started on your local server (e.g. the login node) and will dispatch jobs to the batch system of your cluster. Two batch systems are currently supported: `slurm` and `torque` (defined by the `batch_type` parameter). In the configuration file you will
have to define the `queue` name and the maximum number of concurrent jobs sent to the queue (`queue_limit`). 

  Since HADDOCK3 single model calculations are quite fast, it is recommended to calculate multiple models within one job submitted to the batch system. The number of model per job is defined by the `concat` parameter in the configuration file. You want to avoid sending thousands of very short jobs to the batch system if you want to remain friend with your system administrators...

  An example of the relevant parameters to be defined in the first section of the config file is:

  {% highlight toml %}
  # compute mode
  mode = "batch"
  # batch system
  batch_type = "slurm"
  # queue name
  queue = "short"
  # number of concurrent jobs to submit to the batch system
  queue_limit = 100
  # number of models to produce per submitted job
  concat = 10
  {% endhighlight %}

  In this mode HADDOCK3 can be started from the command line as for the local mode.
</details>

<hr>

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <b><i>Exection in MPI mode</i></b> <i class="material-icons">expand_more</i>
  </summary>


HADDOCK3 supports a parallel pseudo-MPI implementation (functional but still very experimental at this stage). For this to work, the `mpi4py` library must have been installed at installation time. Refer to the [MPI-related instructions](https://www.bonvinlab.org/haddock3/tutorials/mpi.html){:target="_blank"}.

The execution mode should be set to `mpi` and the total number of cores should match the requested resources when submitting to the batch system.

An example of the relevant parameters to be defined in the first section of the config file is:

{% highlight toml %}
# compute mode
mode = "mpi"
#  5 nodes x 50 tasks = ncores = 250
ncores = 250
{% endhighlight %}

In this execution mode the HADDOCK3 job should be submitted to the batch system requesting the corresponding number of nodes and cores per node.


  {% highlight shell %}
  #!/bin/bash
  #SBATCH --nodes=5
  #SBATCH --tasks-per-node=50
  #SBATCH -J haddock3mpi

  # Make sure haddock3 is activated
  source $HOME/miniconda3/etc/profile.d/conda.sh
  conda activate haddock3

  # go to the run directory
  # edit if needed to specify the correct location
  cd $HOME/HADDOCK3-antibody-antigen

  # execute
  haddock3 \<my-workflow-configuration-file\>
  {% endhighlight %}
  <br>
</details>

<br>