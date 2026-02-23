#### Execution of HADDOCK3 on Fugaku (ASM 2026 HPC/AI school, Kobe Japan)

<details style="background-color:#DAE4E7">
  <summary style="bold">
    <i>View execution instructions for running HADDOCK3 on Fugaku</i> <i class="material-icons">expand_more</i>
  </summary>

To execute the workflow on Fugaku, you can either start an interactive session or create a job file that will execute HADDOCK3 on a node,
with HADDOCK3 running in local mode (the setup in the above configuration file with <i>mode="local"</i>) and harvesting all core of that node (<i>ncores=48</i>).
<br>
<br>
<b>Interactive session on a node:</b>
<br>
{% highlight shell %}
pjsub -x PJM_LLIO_GFSCACHE=/vol0003:/vol0004 -g "hp250477" --interact -L "node=1" - -L "rscgrp=int" -L "elapse=2:00:00" --sparam "wait-time=600"
{% endhighlight %}

Once the session is active, activate HADDOCK3 with:

{% highlight shell %}
source /vol0300/data/hp250477/Materials/Life_Science/20250202_Bonvin/haddock3/.venv/bin/activate<br>
{% endhighlight %}

You can then run the workflow with:

{% highlight shell %}
haddock3 ./workflows/docking-antibody-antigen.cfg
{% endhighlight %}
<b>Job submission to the batch system:</b>
<br>
<br>
For this execution mode you should create an execution script contain specific requirements for the queueing system and the HADDOCK3 configuration and execution.
Here is an example of such an execution script (also provided in the <i>HADDOCK3-antibody-antigen</i> directory as <i>run-haddock3-fugaku.sh</i>):

{% highlight shell %}
#!/bin/sh -x
#PJM -L  "node=1"                           # Assign node 1 node
#PJM -L  "rscgrp=small"                     # Specify resource group
#PJM -L  "elapse=02:00:00"                  # Elapsed time limit 1 hour
#PJM -g hp250477                            # group name
#PJM -x PJM_LLIO_GFSCACHE=/vol0003:/vol0004 # volume names that job uses
#PJM -s                                     # Statistical information output

source /vol0300/data/hp250477/Materials/Life_Science/20260202-HADDOCK/haddock3/.venv/bin/activate
haddock3 ./workflows/docking-antibody-antigen.cfg

{% endhighlight %}

This file should be submitted to the batch system using the <i>pjsub</i> command:

{% highlight shell %}
pjsub run-haddock3-fugaku.sh
{% endhighlight %}

<br>

And you can check the status in the queue using <i>pjstat</i>.

This run should take about 25 minutes to complete on a single node using 48 arm cores.

</details>
