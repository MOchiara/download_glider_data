# VOTO data download tutorials

These notebooks provide a starting point for researches wishing to explore and use VOTO glider data made available on our ERDDAP server.

### glider_data_download

A short tutorial on generating download links to download data from multiple gliders from the Voice of the Ocean ERDDAP server. Use if you have a list of glidermissions of interes and prefer to download data from your browser.

### metadata_dig

Query the ERDDAP for datasets within a region/timespan of interest, search for particular vartiables, extract sensor level metadata and more. Useful for generating a list of datasets that may contain data of interest.

### example_analysis

Walks through the process of downloading, slicing and plotting both near real time and delayed mode data. ALso includes recommendations for how and when to combine datasets. This notebook is a good starting point for scientific analysis once you have a list of datasets of interest.

### argo_compare

Download glider data from the VOTO ERDDAP server with [erddapy](https://github.com/ioos/erddapy) and compare it to the nearest available argo profile using [argopy](https://github.com/euroargodev/argopy).

### smhi_compare

Compare glider data to nearby CTD staation occupied by the [Swedish Meteorological and Hydrological Institute](https://www.smhi.se)

### cross_calibrate

A combination of the above two approaches

Try it out on Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/voto-ocean-knowledge/download_glider_data/HEAD?)

If you have any queries, requests or suggestions, please raise an Issue or PR or emaail me at callum.rollo@voiceoftheocean.org


------------------------------

### Acknowledements

This repo would not be possible without the excellend [erddapy](https://github.com/ioos/erddapy) library. These demos benefitted from the feedback and suggestions of [MartinMohrmann](https://github.com/MartinMohrmann)
