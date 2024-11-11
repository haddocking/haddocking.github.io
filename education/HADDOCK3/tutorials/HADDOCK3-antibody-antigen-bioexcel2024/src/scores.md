### Visualizing the scores and their components


Next to the cluster statistic table shown above, the `report.html` file also contains a variety of plots displaying the HADDOCK score 
and its components against various CAPRI metrics (i-RMSD, l-RMSD,  Fnat, Dock-Q) with a color-coded representation of the clusters.
These are interactive plots. A menu on the top right of the first row (you might have to scroll to the rigth to see it) 
allows you to zoom in and out in the plots and turn on and off clusters. 

<figure style="text-align: center;">
    <img width="100%" src="caprieval_analysis-plots.png">
</figure>

As a reminder, you can also view this report online [here](plots/report.html){:target="_blank"}

<a class="prompt prompt-info">
Examine the plots (remember here that higher DockQ values and lower i-RMSD values correspond to better models)
</a>


Finally, the report also shows plots of the cluster statistics (distributions of values per cluster ordered according to their HADDOCK rank):

<figure style="text-align: center;">
    <img width="100%" src="caprieval_analysis-distributions.png">
</figure>

<a class="prompt prompt-question">For this antibody-antigen case, which of the score components correlates best with the quality of the models?</a>
