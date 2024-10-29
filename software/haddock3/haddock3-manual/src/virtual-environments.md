## Virtual environments

Haddock3 makes use of system variables as well as external libraries.
To ensure a reproducible and stable functional version of haddock3, we strongly advise to intall it using a virual environment.
When used from within a virtual environment, common installation tools such as `pip` will install Python packages into a virtual environment, limiting conflicts with other tools already installed on your computing engine.

Two major environments managing system are effective and capable of installing haddock3, namely 
[venv](https://docs.python.org/3/library/venv.html)
and [conda/mini-conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
Below you will find the instructions on how to install them and set up a proper haddock3 environment.


### venv

As the `venv` library is part of the python3 standard library, hence there is no need to install it, considering python3 is installed on your machine.
By using `venv`, you will be able to set the python3 version you want (>=3.9 for haddock3).

For more details and troubleshooting with the `venv` library, have a look at [its documentation](https://docs.python.org/3/library/venv.html)

Then create a new clean environment with the following command:
```bash
python3.9 -m venv .haddock3-env
# or
python3.10 -m venv .haddock3-env
# or
python3.11 -m venv .haddock3-env
# or
python3.12 -m venv .haddock3-env
```

Finally, you should activate the environment, and you are ready for the next steps
```bash
source .haddock3-env/bin/activate
```

### Anaconda / miniconda

For more details and troubleshooting with the `conda` library, have a look at [its documentation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

Then create a new `haddock3-env` environment with the following command:
```bash
conda create -n haddock3-env python=3.9
# or
conda create -n haddock3-env python=3.10
# or
conda create -n haddock3-env python=3.11
# or
conda create -n haddock3-env python=3.12
```

Finally, you should activate the environment, and you are ready for the next steps
```bash
conda activate haddock3-env
```
