import numpy as np
import hist
import coffea.processor as processor
import awkward as ak
from coffea.nanoevents import schemas
import matplotlib.pyplot as plt
from dask.distributed import Client
import os


# This program plots an event-level variable (in this case, MET, but switching it is as easy as a dict-key change). It also demonstrates an easy use of the book-keeping cutflow tool, to keep track of the number of events processed.


# The processor class bundles our data analysis together while giving us some helpful tools.  It also leaves looping and chunks to the framework instead of us.
class Processor(processor.ProcessorABC):
    def __init__(self):
        # Bins and categories for the histogram are defined here. For format, see https://coffeateam.github.io/coffea/stubs/coffea.hist.hist_tools.Hist.html && https://coffeateam.github.io/coffea/stubs/coffea.hist.hist_tools.Bin.html
        dataset_axis = hist.axis.StrCategory(
            name="dataset", label="", categories=[], growth=True
        )
        MET_axis = hist.axis.Regular(
            name="MET", label="MET [GeV]", bins=50, start=0, stop=100
        )

        # The accumulator keeps our data chunks together for histogramming. It also gives us cutflow, which can be used to keep track of data.
        self.output = processor.dict_accumulator(
            {
                "MET": hist.Hist(dataset_axis, MET_axis),
                "cutflow": processor.defaultdict_accumulator(int),
            }
        )

    def process(self, events):
        # This is where we do our actual analysis. The dataset has columns similar to the TTree's; events.columns can tell you them, or events.[object].columns for deeper depth.
        dataset = events.metadata["dataset"]
        MET = events.MET.pt

        # We can define a new key for cutflow (in this case 'all events'). Then we can put values into it. We need += because it's per-chunk (demonstrated below)
        self.output["cutflow"]["all events"] += ak.size(MET)
        self.output["cutflow"]["number of chunks"] += 1

        # This fills our histogram once our data is collected. The hist key ('MET=') will be defined in the bin in __init__.
        self.output["MET"].fill(dataset=dataset, MET=MET)
        return self.output

    def postprocess(self, accumulator):
        pass


DASK_SCHEDULER_URI = os.getenv("DASK_SCHEDULER_URI", "tcp://127.0.0.1:8080")
client = Client(DASK_SCHEDULER_URI)

fileset = {
    "SingleMu": [
        "root://eospublic.cern.ch//eos/root-eos/benchmark/Run2012B_SingleMu.root"
    ]
}

executor = processor.DaskExecutor(client=client)

run = processor.Runner(
    executor=executor, schema=schemas.NanoAODSchema, savemetrics=True
)

output, metrics = run(fileset, "Events", processor_instance=Processor())

# Generates a 1D histogram from the data output to the 'MET' key. fill_opts are optional, to fill the graph (default is a line).
output["MET"].plot1d()


# Easy way to print all cutflow dict values. Can just do print(output['cutflow']["KEY_NAME"]) for one.
for key, value in output["cutflow"].items():
    print(key, value)

# Save the histogram plot to a file (e.g., 'histogram.png')
plt.savefig("histogram.png")
