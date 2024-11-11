## BONUS 1: Does the antibody bind to a known interface of interleukin? ARCTIC-3D analysis

Gevokizumab is a highly specific antibody that targets an allosteric site of Interleukin-1β (IL-1β) in PDB file *4G6M*, thus reducing its binding affinity for its substrate, interleukin-1 receptor type I (IL-1RI). Canakinumab, another antibody binding to IL-1β, has a different mode of action, as it competes directly with the binding site of IL-1RI (in PDB file *4G6J*). For more details please check [this article](https://www.sciencedirect.com/science/article/abs/pii/S0022283612007863?via%3Dihub){:target="_blank"}.

We will now use our new software, [ARCTIC-3D](https://www.nature.com/articles/s42003-023-05718-w){:target="_blank"}, to visualize the binding interfaces formed by IL-1β. First, the program retrieves all the existing binding surfaces formed by IL-1β from the [PDBe website](https://www.ebi.ac.uk/pdbe/){:target="_blank"}. Then, these binding surfaces are compared and clustered together if they span a similar region of the selected protein (IL-1β in our case).

We will run an ARCTIC-3D job targeting the uniprot ID of human Interleukin-1 beta, namely [P01584](https://www.uniprot.org/uniprotkb/P01584/entry){:target="_blank"}.

For this first open the ARCTIC-3D web-server page [here](https://wenmr.science.uu.nl/arctic3d/){:target="_blank"}. 

<a class="prompt prompt-info">
Insert the selected UniProt ID in the **UniprotID** field.
</a>

<a class="prompt prompt-info">
Leave the other parameters as they are and click on **Submit**.
</a>

Wait a few seconds for the job to complete or access a precalculated run [here](https://wenmr.science.uu.nl/arctic3d/example-P01584){:target="_blank"}.

<a class="prompt prompt-question">
How many interface clusters were found for this protein?
</a>

Once you download the output archive, you can find the clustering information presented in the dendrogram:

<figure style="text-align: center;">
<img width="75%" src="dendrogram_average_P01584.png">
</figure>

We can see how the two *4G6M* antibody chains are recognized as a unique cluster, clearly separated from the other binding surfaces and, in particular, from those proper to IL-1RI (uniprot ID P14778).

<a class="prompt prompt-info">
Re-run ARCTIC-3D with a clustering threshold equal to 0.95
</a>

This means that the clustering will be looser, therefore lumping more dissimilar surfaces into the same object.

You can inspect a precalculated run [here](https://wenmr.science.uu.nl/arctic3d/example-P01584-095){:target="_blank"}.

<a class="prompt prompt-question">
How do the results change? Are gevokizumab or canakinumab PDB files being clustered with any IL-1RI-related interface?
</a>
