# Haddock3 source code

Haddock3 is an open source software, and its source code can be downloaded from our [haddocking/haddock3 GitHub repository](https://github.com/haddocking/haddock3/).


## Haddock3 source code structure

```
haddock3
|-- src/haddock
|   |-- clis
|   |   `-- cli*.py
|   `-- core
|   |   `-- *.py
|   `-- gears
|   |   `-- *.py
|   `-- libs
|   |   `-- lib*.py
|   `-- modules
|       |-- topology
|       |-- sampling
|       |-- refinement
|       |-- scoring
|       `-- analysis
`-- tests
|   |-- test_*.py
|   `-- golden_data
|       |-- *.pdb
|       |-- *.tsv
|       |-- *.tbl
`-- integration_tests
|   |-- test_*.py
|   |-- golden_data
|       |-- *.pdb
|       |-- *.tsv
|       |-- *.tbl
`-- examples
 |-- docking-examples
 |-- worflow.cfg
 `-- data
 |-- structure*.pdb
 |-- airs.tbl
 `-- reference_structure.pdb
```


### Modules structure

- [`__init__.py`](#__init__py)
- [`*.py`](#python3-scripts-py)
- [`defaults.yaml`](#defaultsyaml)
- [`cns/` directory](#cns-directory)

#### `defaults.yaml`

This file contains all the parameter names and their default values.
It also explains:
- the `default` value to be used if the parameter is not defined in the configuration file.
- the `type` of value to expect: string, integer, float, boolean, list
- the allowed value range: `choices`, `minchars / maxchars`, `min / max`, `precision` (number of digits for floating points)
- a description of the parameter: its `title`, and a `long` and `short` descriptions.
- a `group`: used to group parameters together.
- the `explevel` expertise level: `easy`, `expert`, `guru`, `hidden`

This file is also used to build the documentation and the web-app.

##### Notes on expertise level

Note the `explevel` attribute to each parameter, allowing us to display (or not), parameters depending on the expertise level of the user.
While this is not used for local installation of haddock3, it is used at the [web-application](./webapp.md) level to hide too techincal parameters to beginers (with `easy` expertise level).

#### `__init__.py`

Holds the module execution machinery.

#### `cns/` directory

Contains CNS scripts related to the module: `*.cns`

#### python3 scripts `*.py`

Holds the module classes, methods, and functions related to the logic for the computation.

### Tests

- [Unity tests](#unity-tests)
- [Integration tests](#integration-tests)
- [End-to-end tests](#end-to-end-tests)

#### Unity tests

All unity tests scripts are located in the `tests/` directory.
Each script starts with a `test_` prefix.
They are supposed to be executed by `pytest`.

#### Integration tests

All integration tests scripts are located in the `integration_tests/` directory.
Each script starts with a `test_` prefix.
They are supposed to be executed by `pytest`.

#### End-to-end tests

The end-to-end tests are also examples that we provide to the users, to guide and help them understand how to use a module.
They also consist of predefined docking scenarios.
End-to-end tests are located in the `examples/` directory.
We run on a daily basis most of the tests configuration files `*-test.cfg` present, tracking potential errors, hens making sure that haddock3 is functional after a new update.
