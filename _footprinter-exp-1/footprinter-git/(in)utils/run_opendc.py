import subprocess



def runOpenDC(tracePath, topologyPath, OutputPath):

    opendc_run = f"./OpenDC/bin/footprinter --topology-path Input/topologies/{topologyPath}.txt --trace-path Input/input_traces/{tracePath} --output {OutputPath}"

    subprocess.run(opendc_run, shell=True, check=True)