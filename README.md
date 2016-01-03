# quantius-plot

Parse and plot Quantius data.

## Getting started

* Clone this repository.
* Install Plotly with `pip install plotly`.
* Get a Quantius JSON file (or use the included sample data in `sampledata.json`).

## Usage

    $ python quantius-plot.py -f sampledata.json -o imagesfolder

`sampledata.json` is a Quantius data file. It contains an item for each 
Quantius annotation in the file.

A Quantius annotation is a single worker's analysis of a single image. 
So, if multiple workers analyzed the same image, there will be multiple 
annotations for the same image. (At some point, this script will be able to 
overlay multiple annotations of the same image.)

`imagesfolder` is the folder where plot images will be stored.

## Limits

* This script only works for images and annotations that are 512px square.
* This script won't detect multiple annotations for the same image.
* This script can't handle data from the Quantius crosshair tool.

These will be fixed soon.
