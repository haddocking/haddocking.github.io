# Generating restraints with Haddock3

Ambiguous (or not) restraints file must comply with the CNS syntax.
Generating them can be quite difficult, and for this reason we added a dedicated command line interface `haddock3-restraints`, allowing to perform several maniputation to generate restraints files to be used later in your docking experiment.

Usage:
```bash
haddock3-restraints <TASK_NAME> <TASK_ARGS>
```

For the list of available tasks, run:
```bash
haddock3-restraints -h
```

For the list of arguments for a given task, run:
```bash
haddock3-restraints <TASK_NAME> -h
```


This CLI holds multiple sub-commands, listed and explained below:
- [calc_accessibility](#calc-accessibility):
- [passive_from_active](#passive-form-active):
- [active_passive_to_ambig](#active-passive-to-ambig):
- [restrain_bodies](#restrain-bodies):
- [z_surface_restraints](#z-surface-restraints):
- [validate_tbl](#validate-tbl):


## Calc Accessibility


## Passive form active


## Active passive to ambig


## Restrain bodies


## Z surface restraints


## Validate tbl



# New version of the haddock-restraints

A new version of the haddock3-restraints is currently being developped.
This new implementation using *rust* will allow better maintainability as well as its deployment on various operating systems as well as on web-browser using WebAssembly.
Not yet part of the haddock3 intallation, you can already find it in its dedicated repository at [https://github.com/haddocking/haddock-restraints](https://github.com/haddocking/haddock-restraints).