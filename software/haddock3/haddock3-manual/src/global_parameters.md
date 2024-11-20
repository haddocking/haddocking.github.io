# Global parameters

Global parameters must be defined before any use of `[modules]`, as they will act on every downstream `[modules]`.

Three types of global parameters are defined:
- [**Mandatory**](#mandatory-global-parameters): These global parameters must be defined for a configuration file to be valid and properly executed.
- [**Execution**](#execution-global-parameters): The execution parameters are related to the execution mode of haddock3, enabling to either run with local cores, use schedulers (such as slurm or torque) or even spread the workload over multiple nodes using MPI.
- [**Optional**](#optional-global-parameters): These optional parameters are mostly related to pre- and post-processing of the results.


## Mandatory global parameters

Two mandatory parameters are required to perform a haddock3 run:

- `run_dir`: Define the directory path where the run will take place (e.g: `run_dir = "docking_run"`)
- `molecules`: A coma-separated list of paths to input molecules. Note that each input file can be a conformational ensemble of the same molecule. Currently limited to a maximum number of 20 input files. (e.g.: `molecules = ["receptor.pdb", "protein.pdb"]`)

## Execution global parameters

Various parameters are related to the execution modes:

- `ncores`: Maximum number of cores to be used by the haddock3 run. If set to a higher number of cores than the ones available on the system, it will be tuned down and limited to use all available cores.
- `max_cpus`: When set to `true`, uses all cores set by the `ncores` parameter. If `false`, remove 1 core from `ncores`, ensuring the computer to still be able to perform tasks outside of haddock3. The default is `true`.
- The `mode` parameter allows to define the execution mode of haddock3.
  - Using 'local', allows to run haddock3 using the local resources, bound to the operating system
  - In 'batch' mode, haddock3 will send jobs to the queue of your choice (defined by the `batch_type` and `queue` parameters). Note that when using the 'batch' mode, you should also define parameters such as (`batch_type`, `queue`, `queue_limit`, `concat`)
  - In 'mpi' mode, haddock3 will spread the workload over the available nodes.
- `batch_type`: defines which batch submission tool must be used, between 'slurm' and 'torque'. Note that this requires your computing engine to have access to such kind of queuing system.
- `queue`: name of the queue on which the submission should be performed. This allows to target queues that can process shorter / longer jobs. It requires you to have an estimation of how long your job will last.
- `queue_limit`: Sets the number of jobs to submit to the batch system. The default is 100.
- `concat`: Number of models to produce per job to send to the batch system. If set to a value above 1, multiple models can be calculated within one job. The default is 1.
- `self_contained`: When set to `true`, this option will copy the CNS scripts and executable to the run folder, making it a self-contained run. The default is `false`.
- `clean`: When set to `true`, clean the modules directory if the run succeeds by compressing or removing output files. The default is `true`.
- `offline`: When set to `true`, completely isolate the haddock3 run and results from internet. This option is useful when no internet connection is available. Default is `false`.
- `debug`: By setting it to `false`, reduces the amount of I/O operations, often speeding up the process. When set to `true`, input files, intermediate files and output files are generated and kept, which is useful when tracking potential errors. The default is `false`.


### Local mode

Often the prefered execution mode if you submit a haddock3 run to a queuing system or run on your own computer.
The `local` mode (targeted using the global parameter `mode = 'local'`), utilize the operating system device to perform the computations.
Setting the `ncores` parameter allows to tune the number of CPU cores to use during the run.
Note that if you set this value too high compared to your system capabilities, this value will be automatically scaled down to the maximum number of cores available on the machine.


### Batch mode

Utilise queuing system machinery to submit CNS runs.

- `batch_type`: defines which batch submission tool must be used, between 'slurm' and 'torque'. Note that this require your computing engine to have access to such kind of queuing system.
- `queue`: name of the queue on which the submission should be performed. This allows to target queues that can process shorter / longer jobs. It requires you to have an estimation of how long your job will last.
- `queue_limit`: Sets the number of jobs to submit to the batch system. Default is 100.
- `concat`: Number of models to produce per job to send to the batch system. If set to a value above 1, multiple models can be calculated within one job. The default is 1.

### MPI mode

Requires the installation of the `mpi4py` python library and `OpenMPI` to be installed on the operating system.


## Optional global parameters

- `postprocess`: When set to `true`, executes `haddock3-analyse` on the CAPRI folders at the end of the run. The default is `true`.
- `preprocess`: When set to `true`, tries to correct input PDBs before the workflow. The default is `false`.
