
## BONUS 5: Introduction to the haddock3 webapp

In addition to the command line interface of haddock3, we are currently developing a new dedicated web application enabling the use of haddock3 under a graphical user interface, directly linking the software functionalities and computed results in an interactive manner.
While not yet deployed as a web service, the application is already available for local installations.


### Intallation procedure

The current version requires [docker](https://www.docker.com/) to build the web application.
Once docker is installed on your computer, deploying the webapp is as simple as following the next 3 command lines.

**Note** that for the sake of this tutorial, the webapp was already built on your computer, and you can simply access it using the following url: [http://localhost:8080](http://localhost:8080)


<details style="background-color:#DAE4E7">
  <summary>
    <b><i>How to build the webapp</i></b> <i class="material-icons">expand_more</i>
  <br>
  </summary>
First, download the haddock3 webapp:

<a class="prompt prompt-cmd">git clone https://github.com/i-VRESSE/haddock3-webapp.git</a>

Then copy a compiled CNS executable in the `deploy/` directory.
**Note** that the container is running under Linux, therfore a Linux-compiled version (compatible with your CPU architecture) of CNS is required here. Instructions on how to compile CNS are available in the [haddock3 documentation](https://github.com/haddocking/haddock3/blob/main/docs/CNS.md)

<b style="color: red;">As this is still in heavy development, the instructions on how to build the web-app is not yet trivial. Better instructions will be written onces it will be in production.</b>
</details>


### Creating an account

For the sake of this tutorial, we have already created accounts:
* **email**: summerschool@bioexcel.eu
* **password**: haddock3

<details style="background-color:#DAE4E7">
  <summary>
    <b><i>How to create an account</i></b> <i class="material-icons">expand_more</i>
  <br>
  </summary>
To create a new account, add your email adresse and choose a password.

<br>
Right after its creation, you will be able to login, but before you can definitely use all the functionalities of the webapp, your account must be validated by an adminitrator that will grant you priviledges.

**Note** that with the current implementation, the first user to register comes the administrator.

</details>


### Running this tutorial

Once logged in, click on the `build` menu to start the creation of a custom workflow.
You will land on the workflow-builder page, where you can interactively build your haddock3 scenario by combining the available modules.
This page is subdivided into three areas described below.

<figure style="text-align: center;">
  <img width="75%" src="./haddock3-webapp-workflow-builder.png">
</figure>

On the left is presented the list of modules.
To add a module to the workflow, just click on it, and it will be automatically added at the bottom of the configuration file.
Alternatively, you can drag-and-drop (using the dots) it to the central panel, at the location where you wish to place it.

The set of modules defining your current workflow is presented on the central panel.
You can switch between interactive (click on “Visual” tab under the Workflow section) and textual (click on “Text” tab) forms of it.
You can configure the parameters of each module by clicking on this module (inside the central panel).

Initially, default parameters are set for each module.
Parameters are sub-categorized based on their properties.
Unfold a property by clicking on it, and discover the set of related parameters.
**Note** that you should always click the `save` button after modifying a parameter value for it to be taken into consideration.

Finally, once you configured your workflow, click on `submit` to launch the corresponding haddock3 run.


<details style="background-color:#DAE4E7">
  <summary>
    <b><i>Display available modules</i></b> <i class="material-icons">expand_more</i>
  <br>
  </summary>

* **Topology modules**
    * `topoaa`: *Generates the all-atom topologies for the CNS engine.*

* **Sampling modules**
    * `rigidbody`: *Performs rigid body energy minimization with CNS (`it0` in haddock2.x).*
    * `lightdock`: *Third-party glow-worm swam optimization docking software.*

* **Model refinement modules**
    * `flexref`: *Performs semi-flexible refinement using a simulated annealing protocol through molecular dynamics simulations in torsion angle space (`it1` in haddock2.x).*
    * `emref`: *Performs refinement by energy minimisation (`itw` EM only in haddock2.4).*
    * `mdref`: *Performs refinement by a short molecular dynamics simulation in explicit solvent (`itw` in haddock2.X).*

* **Scoring modules**
    * `emscoring`: *Performs scoring of a complex performing a short EM (builds the topology and all missing atoms).*
    * `mdscoring`: *Performs scoring of a complex performing a short MD in explicit solvent + EM (builds the topology and all missing atoms).*

* **Analysis modules**
    * `alascan`: *Performs a systematic (or user-define) alanine scanning mutagenesis of interface residues.*
    * `caprieval`: *Calculates CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ) with respect to the top scoring model or reference structure if provided.*
    * `clustfcc`: *Clusters models based on the fraction of common contacts (FCC)*
    * `clustrmsd`: *Clusters models based on pairwise RMSD matrix calculated with the `rmsdmatrix` module.*
    * `contactmap`: *Generate contact matrices of both intra- and intermolecular contacts and a chordchart of intermolecular contacts.*
    * `rmsdmatrix`: *Calculates the pairwise RMSD matrix between all the models generated in the previous step.*
    * `ilrmsdmatrix`: *Calculates the pairwise interface-ligand-RMSD (il-RMSD) matrix between all the models generated in the previous step.*
    * `seletop`: *Selects the top N models from the previous step.*
    * `seletopclusts`: *Selects top N clusters from the previous step.*

</details>

<br>

**Note** that you can also upload a zip archive of a workflow containing a configuration file named `workflow.cfg` and all corresponding files (e.g.: pdb structures, restraints files, topological parameters, etc.). Workflow archives presented in this tutorial are available in `workflows/webapp-workflows/`.


### Loading haddock3 runs

The webapp also allows you to upload a pre-computed run, so you can navigate through the docking results with ease thanks to the graphical interface.
Under the `Upload` menu, you can upload two types of zip archives:

* **Workflow**: a zip archive containing a configuration file named `workflow.cfg` and all corresponding files (e.g.: pdb structures, restraints files, topological parameters, etc.)
* **Run**: a zip archive of the run.

<details style="background-color:#DAE4E7">
 <summary>
  <b><i>How to generate a zip archive of a run?</i></b> <i class="material-icons">expand_more</i>
 </summary>
<br>

First go to the run directory containing all the generated data<br>
<a class="prompt prompt-cmd">cd run_dir</a><br>
Create the zip archive<br>
<a class="prompt prompt-cmd">zip -r run.zip .</a>

</details>

<br>

**Note** that the archives of workflows are available in `workflows/webapp-workflows/`, and archives of pre-computed runs are stored in `runs/webapp_runs/`.


### Navigating throught the results

On the `Manage` page, a table displays all the haddock3 runs performed by one user.
This table contains the job status (queued, running, error, ok), its name, creation date and modification date.
On the right side of the table, actions can be performed.
The current implementation allows to rename a run or to delete it.

<figure style="text-align: center;">
  <img width="75%" src="./haddock3-webapp-manage-run-access.png">
</figure>

To access the content of a run, click on its name to be directed to the haddock3 webapp results page.
You will land on the analysis page, which summarizes the performance of the models obtained at the last stage.
This is similar to the previous method of opening the `report.html` file (see above), which contains various plots displaying the HADDOCK score and its components against different CAPRI metrics.
In this case, because a reference was provided during the `caprieval` module, performance is evaluated based on this structure.

In addition, you can click on the `browse` button, which will let you access all the files of the run.


### Running a scoring scenario

In this scenario, we want to score the various models obtained at the previous stages (ensemble docking and AlphaFold predictions) and observe if the HADDOCK scoring function is able to detect the quality of the models.

In this scenario, we want to:
- Start by generating the topologies for the various models.
- Cluster the models using Fraction of Common Contacts:
  - set the parameter `min_population` to 1 so that all models, including singletons (models that do not cluster with any others), will be forwarded to the next steps.
  - set the parameter `plot_matrix` to true to generate a matrix of the clusters for a visual representation.
- Add the Energy Minimisation module to score all complexes.
- End the scenario with a comparison of the models with the reference complex `4G6M_matched.pdb` using CAPRI criteria.

For this, two ensembles must be scored and one structure will be used as a reference. You can find them in the `pdbs/` directory:
- `07_emref_and_top5af2_ensemble.pdb`: An ensemble of models obtained from the ensemble run, combined with top5 AlphaFold2 predictions.
- `af3server_15052024_top5ens.pdb`: An ensemble of top5 AlphaFold3 predictions.
- `4G6M_matched.pdb`: The reference structure for quality assessments.


<a class="prompt prompt-info">
Generate a simple scoring configuration file scenario using the workflow builder.
</a>


{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen 
# ====================================================================
run_dir = "scoring-haddock3-alphafold2and3-ensemble"

molecules =  [
    "07_emref_and_top5af2_ensemble.pdb",
    "af3server_15052024_top5ens.pdb",
    ]

# ====================================================================
# Parameters for each stage are defined below
# ====================================================================

# Start by generating the topologies
[topoaa]

# Cluster structures to observe similarities
[clustfcc]
# Reducing min_population to define a cluster to 1 so even complexes
#  that do not cluster with any other will define singlotons
min_population = 1
# Generate a matrix of the clusters
plot_matrix = true

# Run the Energy Minimisation Scoring module
[emscoring]


# Evaluate the models with the CAPRI criterions
[caprieval]
reference_fname = "4G6M_matched.pdb"

# ====================================================================

{% endhighlight %}


To simplify the tutorial, scoring scenario configuration files are provided in the `workflow/` directory, precomputed results in the `runs/` directory and finally archives for the haddock3-webapp upload section in `workflow/webapp/scoring-*.cfg`.

<a class="prompt prompt-question">
How are scoring the AlphaFold predictions?
</a>

<a class="prompt prompt-question">
Can the HADDOCK scoring function identify the best models?
</a>
