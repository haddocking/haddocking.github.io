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

#### `defaults.yaml`

This file contains all the parameter names and their default values.
It also explains:
- the `default` value to be used if the parameter is not defined in the configuration file.
- the `type` of value to expect: string, integer, float, boolean, list
- the allowed value range: `choices`, `minchars / maxchars`, `min / max`, `precision` (number of digits for floating points)
- a description of the parameter: its `title`, and `long` and `short` description.
- a group (`group`): used to group parameters together.
- the `explevel` expertise level: `easy`, `expert`, `guru`, `hidden`

This file is used to build the documentation and the web-app.

**Note** the `explevel` attribute to each parameter, allowing us to display (or not), parameters depending on the expertise level of the user. While this is not used for local installation of haddock3, it is used at the web-application level to hide too techincal parameters to beginers (with `easy` expertise level).

#### `__init__.py`

bla

### Tests

- [Unity tests](#unity-tests)
- [Integration tests](#integration-tests)
- [End-to-end tests](#end-to-end-tests)

#### Unity tests


#### Integration tests


#### End-to-end tests


