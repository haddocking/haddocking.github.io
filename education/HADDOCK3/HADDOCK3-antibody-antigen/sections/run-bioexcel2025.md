#### Execution of HADDOCK3 on the computers of the BioExcel 2025 summerschool

To execute the HADDOCK3 workflow on the computational resources provided for this workshop,
we will simply run in local mode, calling haddock3 with as argument the workflow you want to execute.

{% highlight shell %}
haddock3 <my-workflow-configuration-file>
{% endhighlight %}

Alternatively redirect the output to a log file and send haddock3 to the background.

As an indication, running locally on an Apple M2 laptop using 10 cores, this workflow completed in 7 minutes.
