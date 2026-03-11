#### Execution of HADDOCK3 on ADD Ljubljana (BioExcel Adriatic edition 2026, Ljubljana, Slovenia)

To execute the workflow, you can either start an interactive session or create a job file that will execute HADDOCK3 on a node,
with HADDOCK3 running in local mode (the setup in the above configuration file with <i>mode="local"</i>) and harvesting all core of that node (<i>ncores=16</i>).
<br>
<br>
<b>Start an interactive session on a node:</b>
<br>
{% highlight shell %}
salloc --job-name=interactive_haddock3 --partition=amd --nodes=1 --cpus-per-task=16 --time-min=120
{% endhighlight %}

Once the session is active, activate HADDOCK3 with:

{% highlight shell %}
source /home/vreys/haddock3/.haddock3-env/bin/activate<br>
{% endhighlight %}

You can then follow the tutorial and run all the commands present in it, such as starting a haddock3 docking workflow with:

{% highlight shell %}
haddock3 ./workflows/docking-antibody-antigen.cfg
{% endhighlight %}
<b>Job submission to the batch system:</b>
<br>
<br>
For this execution mode you should create an execution script contain specific requirements for the queueing system and the HADDOCK3 configuration and execution.
Here is an example of such an execution script (that can be saved under the name <i>run-haddock3-slurm.sh</i>):

{% highlight shell %}
#!/bin/bash
#SBATCH --partition=amd
#SBATCH --job-name=haddock3_run
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --time-min=120
#SBATCH --output="haddock3_run_log.txt"

# Source the environement
source /home/vreys/haddock3/.haddock3-env/bin/activate

# Go to the appropriate directory
cd ~/HADDOCK3-antibody-antigen

# Launch haddock3
haddock3 workflows/docking-antibody-antigen.cfg


{% endhighlight %}

This file should be submitted to the batch system using the <i>sbatch</i> command:

{% highlight shell %}
sbatch run-haddock3-slurm.sh
{% endhighlight %}

<br>

And you can check the status in the queue using <i>squeue -u Username</i>.

Also, you can follow the state of your run by looking a the content of either the log file or the slurm output using:

{% highlight shell %}
tail -f haddock3_run_log.txt
{% endhighlight %}

This run should take around 20 minutes to complete on a single node using 16 arm cores.
