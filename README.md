# REANA example - Dask and Coffea

[![image](https://github.com/reanahub/reana-demo-dask-coffea/workflows/CI/badge.svg)](https://github.com/reanahub/reana-demo-dask-coffea/actions)
[![image](https://img.shields.io/badge/discourse-forum-blue.svg)](https://forum.reana.io)
[![image](https://img.shields.io/github/license/reanahub/reana-demo-dask-coffea.svg)](https://github.com/reanahub/reana-demo-dask-coffea/blob/master/LICENSE)
[![image](https://www.reana.io/static/img/badges/launch-on-reana-at-cern.svg)](https://reana.cern.ch/launch?url=https%3A%2F%2Fgithub.com%2Freanahub%2Freana-demo-dask-coffea&specification=reana.yaml&name=reana-demo-dask-coffea)

## About

This [REANA](http://www.reana.io/) reproducible analysis example provides a
simple example how to run Dask workflows using Coffea. The example was adapted
from
[Coffea Casa tutorials](https://github.com/CoffeaTeam/coffea-casa-tutorials/blob/master/examples/example1.ipynb)
repository.

## Analysis structure

Making a research data analysis reproducible basically means to provide
"runnable recipes" addressing (1) where is the input data, (2) what software was
used to analyse the data, (3) which computing environments were used to run the
software and (4) which computational workflow steps were taken to run the
analysis. This will permit to instantiate the analysis on the computational
cloud and run the analysis to obtain (5) output results.

### 1. Input data

In this example, we are using a single CMS open data set file
`Run2012B_SingleMu.root` which is hosted at EOSPUBLIC XRootD server.

### 2. Analysis code

The analysis code consists of a single Python file called `analysis.py` which
connects to a Dask cluster and then conducts the analysis and prints MET
histogram.

### 3. Compute environment

In order to be able to rerun the analysis even several years in the future, we
need to "encapsulate the current compute environment". We shall achieve this by
preparing a [Docker](https://www.docker.com/) container image for our analysis
steps.

This example makes use of the Coffea platform image with the specific version
0.7.22. The container image can be found on Docker Hub at
[docker.io/coffeateam/coffea-dask-cc7:0.7.22-py3.10-g7f049](https://hub.docker.com/r/coffeateam/coffea-dask-cc7).

### 4. Analysis workflow

The analysis workflow is simple and consists of a single command. We simply run
the script `python analysis.py` to run the example. The command will then use
the Dask behind the scenes to possibly launch parallel computations. As a user,
we do not have to specify the computational graph ourselves; the Dask library
will take care of dispatching computations.

### 5. Output results

The example produces the following MET event-level histogram as an output.

![](https://github.com/user-attachments/assets/e52c2391-626d-4556-90ca-75248516cc95)

## Running the example on REANA cloud

There are two ways to execute this analysis example on REANA.

If you would like to simply launch this analysis example on the REANA instance
at CERN and inspect its results using the web interface, please click on the
following badge:

[![Launch on REANA@CERN badge](https://www.reana.io/static/img/badges/launch-on-reana-at-cern.svg)](https://reana.cern.ch/launch?url=https://github.com/reanahub/reana-demo-dask-coffea&specification=reana.yaml&name=reana-demo-dask-coffea)

If you would like a step-by-step guide on how to use the REANA command-line
client to launch this analysis example, please read on.

We start by creating a [reana.yaml](reana.yaml) file describing the above
analysis structure with its inputs, code, runtime environment, computational
workflow steps and expected outputs:

```yaml
inputs:
  files:
    - analysis.py
workflow:
  type: serial
  resources:
    dask:
      image: docker.io/coffeateam/coffea-dask-cc7:0.7.22-py3.10-g7f049
  specification:
    steps:
      - name: process
        environment: docker.io/coffeateam/coffea-dask-cc7:0.7.22-py3.10-g7f049
        commands:
          - python analysis.py
outputs:
  files:
    - histogram.png
tests:
  files:
    - tests/log-messages.feature
    - tests/workspace-files.feature
```

In this example we are using a simple Serial workflow engine to launch our
Dask-based computations.

We can now install the REANA command-line client, run the analysis and download
the resulting plots:

```console
$ # create new virtual environment
$ virtualenv ~/.virtualenvs/reana
$ source ~/.virtualenvs/reana/bin/activate
$ # install REANA client
$ pip install reana-client
$ # connect to some REANA cloud instance
$ export REANA_SERVER_URL=https://reana.cern.ch/
$ export REANA_ACCESS_TOKEN=XXXXXXX
$ # create new workflow
$ reana-client create -n myanalysis
$ export REANA_WORKON=myanalysis
$ # upload input code, data and workflow to the workspace
$ reana-client upload
$ # start computational workflow
$ reana-client start
$ # ... should be finished in about 5 minutes
$ reana-client status
$ # list workspace files
$ reana-client ls
$ # download output results
$ reana-client download
```

Please see the [REANA-Client](https://reana-client.readthedocs.io/)
documentation for more detailed explanation of typical `reana-client` usage
scenarios.
