## Scoring workflow

## Defining a haddock3 configuration file

This example illustrates the use of Haddock3 for scoring purposes.
In contrast to HADDOCK2.X, Haddock3 can score a heterogenous set of complexes within one run/workflow.
In this example, four different types of complexes are scored within the same workflow:

- an ensemble of 5 models taken from CAPRI Target161
- a protein-DNA complex (model taken from our protein-DNA docking example)
- two models of a protein-protein complex (taken from our protein-protein docking example)
- a homotrimer model (taken from our protein-homotrimer docking examples)

Three scoring workflows are illustrated:

- [emscoring-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/scoring/emscoring-test.cfg): Only a short energy minimisation is performed on each model using `[emref]` module.
- [mdscoring-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/scoring/mdscoring-test.cfg): A short molecular dynamics simulation in explicit solvent (water) is performed on each model using `[mdref]` module. In that case contact AIRs (`contactairs = true`), dihedral angle restraints on secondary structure element (`ssdihed = alphabeta`) and DNA restraints (`dnarest_on = true`) are automatically defined.
- [capri-scoring-test.cfg](https://github.com/haddocking/haddock3/blob/main/examples/scoring/capri-scoring-test.cfg): An example scoring pipeline using in the CAPRI55 competition, where energy minimisation module (`[emref]`) is followed by FCC clustering (`[clustfcc]`) and selection of the top 2 models per cluster (`[seletopclusts]` with `top_models = 2`). Then a short molecular dynamics simulation in explicit solvent (water) is performed on each model using `[mdref]` module and the models are clustered again.

The model listings with their associated HADDOCK scores can be found in a `.tsv` file in the stage `01_xxx` directory of the respective runs.


### Using scoring command line


Haddock3 also contain a simple command line interface that allows you to score a single pdb file.
To do so, just run:
```bash
haddock3-score complex.pdb
```

This command is a short-cut to the following parameter file, and therefore can be really handy, as it simplify a lot the procedure, but is limitted to the scoring of a single model.
```toml
run_dir = "tmp_score"
molecules = "complex.pdb"
[topoaa]
[emscoring]
```

For more details on the `haddock3-score` CLI, please refere to [this section](../clis.md#haddock3-score).

