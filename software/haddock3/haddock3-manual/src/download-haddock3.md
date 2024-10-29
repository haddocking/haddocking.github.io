## Install via the Python Package Index (PyPI)

We have simplified the installation of Haddock3 by adding it to the Python Package Index.

Therefore, the only command you should run is the following:

```bash
# Activate your haddock3 virtual env
# ...
# run pip install haddock3
pip install haddock3
```

**Note** that by running `pip install haddock3`, you will be able to use haddock3, but the examples will not be provided.
To obtain them, you should [install haddock3 from the source code (as described below)](#download-haddock3-source-code).

**DISCLAMER**:
By running this command, you will download a compiled executable of CNS (Crystallographic and NMR System) which is free of use for non-profit applications.
For commercial use, it is your own responsibility to have a proper license.
For details refer to [the DISCLAIMER file](https://github.com/haddocking/haddock3/blob/main/DISCLAIMER.md) in the HADDOCK3 repository.

## Download haddock3 source code

Haddock3 is an open source software and therefore its source code can be downloaded at any time.
We are hosting the code on a dedicated [GitHub repository](https://github.com/haddocking/haddock3/), allowing for better version control, code development and maintainability.

For usage tracking purposes (to avoid counting robots downloading the tool), we advise users to download it from our [lab page](https://www.bonvinlab.org/software/haddock3/#haddock3-distribution-download), as it eases the reporting tasks to authorities supporting the development of this project with grants.


To install haddock3 from the source, we suggest running the following commands:

```bash
# First, download the source code:
git clone https://github.com/haddocking/haddock3.git
cd haddock3

# Setup the virtural environnement:
python3.9 -m venv .haddock3-env
source .haddock3-env/bin/activate

# Install haddock3
pip install .
# DISCLAMER
# By running this command, you will download a compiled executable 
# of CNS (Crystallographic and NMR System) which is free of use
# for non-profit applications.
# For commercial use it is your own responsibility to have a proper license.
# For details refer to the DISCLAIMER file in the HADDOCK3 repository.
# here -> https://github.com/haddocking/haddock3/blob/main/DISCLAIMER.md
```

### Development version

To install the development version of haddock3, you should add extra arguments to the `pip install` commands, so other libraries will be downloaded too:

```bash
# First, download the source code:
git clone https://github.com/haddocking/haddock3.git
cd haddock3

# Setup the virtural environnement:
python3.9 -m venv .haddock3-env
source .haddock3-env/bin/activate

# Install haddock3
pip install -e '.[dev,docs]'
```

A complete guide on how to setup an adequate development environment can be found here: [DEVELOPMENT.md](https://github.com/haddocking/haddock3/blob/main/DEVELOPMENT.md)
