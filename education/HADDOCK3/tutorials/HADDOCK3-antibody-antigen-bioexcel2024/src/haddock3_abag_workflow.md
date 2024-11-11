## Setting up and running the docking with HADDOCK3

Now that we have all required files at hand (PDB and restraints files), it is time to setup our docking protocol. In this tutorial, considering we have rather good information about the paratope and epitope, we will execute a fast HADDOCK3 docking workflow, reducing the non-negligible computational cost of HADDOCK by decreasing the sampling, without impacting too much the accuracy of the resulting models.



<hr>

### HADDOCK3 workflow definition

The first step is to create a HADDOCK3 configuration file that will define the docking workflow. 
We will follow a classic HADDOCK workflow consisting of rigid body docking, semi-flexible refinement and final energy minimisation followed by clustering.

We will also integrate two analysis modules in our workflow: 

- `caprieval` will be used at various stages to compare models to either the best scoring model (if no reference is given) or a reference structure, which in our case we have at hand (`pdbs/4G6M_matched.pdb`). This will directly allow us to assess the performance of the protocol. In the absence of a reference, `caprieval` is still usefull to assess the convergence of a run and analyse the results. 
- `contactmap` added as last module will generate contact matrices of both intra- and intermolecular contacts and a chordchart of intermolecular contacts for each cluster.


Our workflow consists of the following modules:

1. **`topoaa`**: *Generates the topologies for the CNS engine and builds missing atoms*
2. **`rigidbody`**: *Preforms rigid body energy minimisation (`it0` in haddock2.x)*
3. **`caprieval`**: *Calculates CAPRI metrics (i-RMSD, l-RMSD, Fnat, DockQ) with respect to the top scoring model or reference structure if provided*
4. **`seletop`** : *Selects the top X models from the previous module*
5. **`flexref`**: *Preforms semi-flexible refinement of the interface (`it1` in haddock2.4)*
6. **`caprieval`**
7. **`emref`**: *Final refinement by energy minimisation (`itw` EM only in haddock2.4)*
8. **`caprieval`**
9. **`clustfcc`**: *Clustering of models based on the fraction of common contacts (FCC)*
10. **`seletopclusts`**: *Selects the top models of all clusters*
11. **`caprieval`**
12. **`contactmap`**: *Contacts matrix and a chordchart of intermolecular contacts*


The corresponding toml configuration file (provided in `workflows/docking-antibody-antigen-CDR-NMR-CSP.cfg`) looks like:

{% highlight toml %}
# ====================================================================
# Antibody-antigen docking example with restraints from the antibody
# paratope to the NMR-identified epitope on the antigen 
# ====================================================================

# Directory in which the scoring will be done
run_dir = "run1-CDR-NMR-CSP"

# Compute mode
mode = "local"
ncores = 50

# Self contained rundir (to avoid problems with long filename paths)
self_contained = true

# Post-processing to generate statistics and plots
postprocess = true
clean = true

molecules =  [
    "pdbs/4G6K_clean.pdb",
    "pdbs/4I1B_clean.pdb"
    ]

# ====================================================================
# Parameters for each stage are defined below, prefer full paths
# ====================================================================
[topoaa]

[rigidbody]
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"
sampling = 50

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[seletop]
# Selection of the top 40 best scoring complexes
select = 40

[flexref]
tolerance = 5
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[emref]
tolerance = 5
# CDR to NMR epitope ambig restraints
ambig_fname = "restraints/ambig-paratope-NMR-epitope.tbl"
# Restraints to keep the antibody chains together
unambig_fname = "restraints/antibody-unambig.tbl"

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[clustfcc]
plot_matrix = true

[seletopclusts]
# Selection of the top 4 best scoring complexes from each cluster
top_models = 4

[caprieval]
reference_fname = "pdbs/4G6M_matched.pdb"

[contactmap]

# ====================================================================

{% endhighlight %}


In this case, since we have information for both interfaces we use a low-sampling configuration file, which takes only a small amount of computational resources to run. From the sampling parameters in the above config file, you can see we are sampling only 50 models at each stage of the docking: 

The initial `sampling` parameter at the rigid-body energy minimization (*rigidbody*) module is set to 50 models, of which only best the 40 are passed to the flexible refinement (*flexref*) module with the *seletop* module.
The subsequence flexible refinement (*flexref* module) and energy minimisation (*emref*) modules will use all models passed by the *seletop* module.
FCC clustering (*clustfcc*) is then applied to group together models sharing a consistent fraction of the interface contacts.
The top 4 models of each cluster are saved to disk (*seletopclusts*).
Multiple *caprieval* modules are executed at different stages of the workflow to check how the quality (and rankings) of the models change throughout the protocol.

To get a list of all possible parameters that can be defined in a specific module (and their default values) you can use the following command:

<a class="prompt prompt-cmd">
haddock3-cfg -m \<module\-name\>
</a>

Add the `-d` option to get a more detailed description of parameters and use the `-h` option to see a list of arguments and options.

<a class="prompt prompt-question">
In the above workflow we see in three modules a *tolerance* parameter defined. Using the *haddock3-cfg* command try to figure out what this parameter does.
</a>


*__Note__* that, in contrast to HADDOCK2.X, we have much more flexibility in defining our workflow.
As an example, we could use this flexibility by introducing a clustering step after the initial rigid-body docking stage, selecting a given number of models per cluster and refining all of those.
For an example of this strategy see the BONUS 3 section about ensemble docking.
