### Cluster statistics

Let us now analyse the docking results. Use for that either your own run or a pre-calculated run provided in the `runs` directory.
Go into the `analysis/10_caprieval_analysis` directory of the respective run directory  (if needed copy the run or that directory to your local computer) and open in a web browser the `report.html` file. Be patient as this page contains interactive plots that may take some time to generate.

On the top of the page, you will see a table that summarises the cluster statistics (taken from the `capri_clt.tsv` file).
The columns (corresponding to the various clusters) are sorted by default on the cluster rank, which is based on the HADDOCK score (found on the 4th row of the table).
As this is an interactive table, you can sort it as you wish by using the arrows present in the first column.
Simply click on the arrows of the term you want to use to sort the table (and you can sort it in ascending or descending order).
A snapshot of this table is shown below:

<figure style="text-align: center;">
    <img width="75%" src="/education/HADDOCK3/HADDOCK3-antibody-antigen/images/caprieval_analysis-table.png">
</figure>

You can also view this report online [here](plots/report.html){:target="_blank"}

*__Note__* that in case the PDB files are still compressed (gzipped) the download links will not work. Also online visualisation is not enabled. To overcome this disk space storge solution, consider adding the global parameter `clean = true` at the begining of your configuration file.


<a class="prompt prompt-info">Inspect the final cluster statistics</a>

<a class="prompt prompt-question">How many clusters have been generated?</a>

<a class="prompt prompt-question">Look at the score of the first few clusters: Are they significantly different if you consider their average scores and standard deviations?</a>

Since for this tutorial we have at hand the crystal structure of the complex, we provided it as reference to the `caprieval` modules.
This means that the iRMSD, lRMSD, Fnat and DockQ statistics report on the quality of the docked model compared to the reference crystal structure.

<a class="prompt prompt-question">How many clusters of acceptable or better quality have been generate according to CAPRI criteria?</a>

<a class="prompt prompt-question">What is the rank of the best cluster generated?</a>

<a class="prompt prompt-question">What is the rank of the first acceptable of better cluster generated?</a>
