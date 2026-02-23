#### Execution of HADDOCK3 on DISCOVERER (BioExcel Sofia May 2025 workshop)

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View execution instructions for running HADDOCK3 on DISCOVERER</i> <i class="material-icons">expand_more</i>
  </summary>

To execute the HADDOCK3 workflow on the computational resources provided for this workshop,
you should create an execution script contain specific requirements for the queueing system and the HADDOCK3 configuration and execution.
An example slurm script is provided with the data you unzipped:

{% highlight shell %}
run-haddock3-discoverer.sh
{% endhighlight %}


Here is an example of such an execution script (also provided in the `HADDOCK3-antibody-antigen` directory as `run-haddock3-discoverer.sh`):

{% highlight shell %}
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --account=school-01
#SBATCH --qos=school-01
#SBATCH --job-name "haddock3"
#SBATCH --tasks-per-node=50
#SBATCH --mem-per-cpu 1500
#SBATCH --time 04:00:00

module load python/3/3.12
module load haddock3/2025.5.0
haddock3 workflows/docking-antibody-antigen.cfg

{% endhighlight %}

This file should be submitted to the batch system using the `sbatch` command:

<a class="prompt prompt-cmd">
sbatch run-haddock3-discoverer.sh
</a>

And you can check the status in the queue using the `squeue`command.

This example run should take about 7 minutes to complete on a single node using 50 cores.

</details>
