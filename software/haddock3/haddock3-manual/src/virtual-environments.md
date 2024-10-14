## Virtual environments

Haddock3 makes use of system variables as well as external libraries.
To ensure a reproducible and stable functional version of haddock3, we strongly advise to intall it using a virual environment.
When used from within a virtual environment, common installation tools such as `pip` will install Python packages into a virtual environment without needing to be told to do so explicitly.

Two major environment managing system are effective and capable of installing haddock3, namely 
[venv](https://docs.python.org/3/library/venv.html)
and [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
Below you will find the instruction on how to install them and setup a proper haddock3 environment.


### venv

As the `venv` library is part of the python3 standard library, hence there is no need to installing it, considering python3 is installed on your machine.
By using `venv`, you will be able to set the python3 version you want (>=3.9 for haddock3).

For more details and troubleshooting with the `venv` library, have a look at [its documentation](https://docs.python.org/3/library/venv.html)

### Anaconda / miniconda

For more details and troubleshooting with the `conda` library, have a look at [its documentation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)