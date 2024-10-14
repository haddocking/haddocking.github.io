# Global parameters

Global parameters must be defined before any use of `[modules]`, as they will act on every downstream `[modules]`.

Three types of global parameters are defined:
- [**Mandatory**](#mandatory-global-parameters): These global parameters must be defined for a configuration file to be valid and properly exectued.
- [**Execution**](#execution-global-parameters): The execution parameters are related to the exeuction mode of haddock3, enabling to either run with local cores, use schedulers (such as slurm or torque) or even spread the workload over multiple nodes using MPI.
- [**Optional**](#optional-global-parameters): These optional parameters are mostly related to pre and post processing of the results.


## Mandatory global parameters

- `run_dir`: Define directory path where the run will take place.
- `molecules`: List of path to input molecules. Note that each input file can be an conformational ensemble of the same molecule. Currently limited to a maximum number of 20 input files.

## Execution global parameters

- `ncores`: Maximum number of cores to be used by the haddock3 run. If set to a higher number of cores than the ones available on the system, it will be tuned down and limmited to use all available cores.
- `max_cpus`: ??
- The `mode` parameter allows to define the execution mode of haddock3.
  - Using 'local', allows to run haddock3 using the local resources, bound to the operating system
  - In 'batch' mode, haddock3 will send jobs to the queue of your choice (defined by the `batch_type` and `queue` parameters). Note that when using the 'batch' mode, you should also define parameters such as (`batch_type`, `queue`, `queue_limit`, `concat`)
- `batch_type`: defines which batch submission tool must be used, between 'slurm' and 'torque'. Note that this require your computing engine to have access to such kind of queuing system.
- `queue`: name of the queue on which the submission should be performed. This allows to target queues that can process shorter / longer jobs. It requires you to have an estimation of how long your job will last.
- `queue_limit` = 100  # $min 1 / $max 9999 / $title Number of jobs to submit to the batch system / $short Number of jobs to submit to the batch system / $group execution
- `concat` = 1  # $min 1 / $max 9999 / $precision 0 / $title Number of models to produce per job. / $short Multiple models can be calculated within one job / $group execution
- `self_contained` = false  # $title Create a self-contained run / $short This option will copy the CNS scripts and executable to the run folder. / $group execution
- `clean` = true  # $title Clean the module output files. / $short Clean the module if run succeeds by compressing or removing output files. / $group clean
- `offline` = false  # $title Isolate haddock3 from internet. / $short Completely isolate the haddock3 run & results from internet. / $group execution
- `debug` = true  # $title Reduce the amount of I/O operations. / $short Reduce the amount of I/O operations. / $group execution



### Local mode

The local mode (targeted using the global parameter `mode = 'local'`), utilize the operating system device to perform the computations.
Setting the `ncores` parameter allows to tune the number of CPU cores to use during the run.
Note that if you set this value to high compared to your system capabilities, this value will be automatically lowered to the maximum number of cores available on the computer.


### Batch mode

- `batch_type`: defines which batch submission tool must be used, between 'slurm' and 'torque'. Note that this require your computing engine to have access to such kind of queuing system.
- `queue`: name of the queue on which the submission should be performed. This allows to target queues that can process shorter / longer jobs. It requires you to have an estimation of how long your job will last.
- `queue_limit` = 100  # $min 1 / $max 9999 / $title Number of jobs to submit to the batch system / $short Number of jobs to submit to the batch system / $group execution
- `concat` = 1  # $min 1 / $max 9999 / $precision 0 / $title Number of models to produce per job. / $short Multiple models can be calculated within one job / $group execution


### MPI mode

Requires the intallation of the `mpi4py` python library and `OpenMPI` to be installed on the operating system.


## Optional global parameters

