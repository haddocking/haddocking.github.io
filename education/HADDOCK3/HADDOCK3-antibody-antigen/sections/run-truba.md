#### Execution of HADDOCK3 on the TRUBA resources (EuroCC Istanbul April 2024 workshop)

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View execution instructions for running HADDOCK3 the TRUBA resources</i> <i class="material-icons">expand_more</i>
  </summary>

To execute the HADDOCK3 workflow on the computational resources provided for this workshop,
you should create an execution script contain specific requirements for the queueing system and the HADDOCK3 configuration and execution.
Two scripts are provided with the data you unzipped, one for execution on the hamsri cluster and one for the barbun cluster:

{% highlight shell %}
run-haddock3-barbun.sh
run-haddock3-hamsri.sh
{% endhighlight %}

Here is an example of such an execution script (also provided in the <i>HADDOCK3-antibody-antigen</i> directory as <i>run-haddock3-hamsri.sh</i>):

{% highlight shell %}
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=54
#SBATCH -C weka
#SBATCH -p hamsi
#SBATCH --time 00:30:00

source ~egitim/HADDOCK/haddock3/.venv/bin/activate
haddock3 workflows/docking-antibody-antigen.cfg
{% endhighlight %}

This file should be submitted to the batch system using the <i>sbatch</i> command:

{% highlight shell %}
sbatch run-haddock3-hamsri.sh
{% endhighlight %}

<b><i>Note</i></b> that batch submission is only possible from the <i>scratch</i> partition (<i>/arf/scratch/my-home-directory</i>)

And you can check the status in the queue using the <i>squeue</i>command.

This example run should take about 7 minutes to complete on a single node using 50 cores.

</details>
