### BioExcel summerschool, Pula, Sardinia June 2025

<details>
  <summary style="font-weight:bold; cursor:pointer;">
    <i>click to expand</i>
  </summary>
    <p>
      We will be making use of the local computers for this tutorial.
      The software and data required for this tutorial have been pre-installed.
    </p>

    <p>
      In order to run the tutorial, go into the
      <code>HADDOCK3-antibody-antigen</code> directory and activate the HADDOCK3 environment:
    </p>

    <a class="prompt prompt-cmd">cd ~/BioExcel_SS_2025/HADDOCK/HADDOCK3-antibody-antigen</a>

    <p>
      This directory contains all necessary data and scripts to run this tutorial.
      To activate the HADDOCK3 environment type:
    </p>

    <a class="prompt prompt-cmd">haddock3env</a>

    <p>
      which is an alias for:<br>
      <code>source ~/BioExcel_SS_2025/HADDOCK/haddock3/.venv/bin/activate</code>
    </p>

    <p>
      You can then test that <code>haddock3</code> is accessible with:
    </p>

    <a class="prompt prompt-cmd">haddock3 -h</a>
  You should see a small help message explaining how to use the software.

    <details style="background-color:#DAE4E7">
      <summary>
      <i>View output</i><i class="material-icons">expand_more</i>
    </summary>
      <pre>
      (haddock3)$ haddock3 -h
      usage: haddock3 [-h] [--restart RESTART] [--extend-run EXTEND_RUN] [--setup]
                      [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-v]
                      recipe

      positional arguments:
        recipe                The input recipe file path

      optional arguments:
        -h, --help            show this help message and exit
        --restart RESTART     Restart the run from a given step. Previous folders from the
                              selected step onward will be deleted.
        --extend-run EXTEND_RUN
                              Start a run from a run directory previously prepared with the
                              `haddock3-copy` CLI. Provide the run directory created with
                              `haddock3-copy` CLI.
        --setup               Only setup the run, do not execute
        --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
        -v, --version         show version
      </pre>
    </details>
  <br>
  </details>
