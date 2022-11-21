# VOTO data download tutorials

These notebooks provide a starting point for researches wishing to explore and use VOTO glider data made available on our ERDDAP server.

Try it out on Binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/voto-ocean-knowledge/download_glider_data/HEAD?)

------------------------

# Main notebooks

### glider_data_download

A short tutorial on generating download links to download data from multiple gliders from the Voice of the Ocean ERDDAP server. Use if you have a list of glidermissions of interes and prefer to download data from your browser.

### metadata_dig

Query the ERDDAP for datasets within a region/timespan of interest, search for particular variables, extract sensor level metadata and more. Useful for generating a list of datasets that may contain data of interest.

### example_analysis

Walks through the process of downloading, slicing and plotting both near real time and delayed mode data. ALso includes recommendations for how and when to combine datasets. This notebook is a good starting point for scientific analysis once you have a list of datasets of interest.

### argo_compare

Download glider data from the VOTO ERDDAP server with [erddapy](https://github.com/ioos/erddapy) and compare it to the nearest available argo profile using [argopy](https://github.com/euroargodev/argopy).

### smhi_compare

Compare glider data to nearby CTD staation occupied by the [Swedish Meteorological and Hydrological Institute](https://www.smhi.se)

### cross_calibrate

A combination of the above two approaches

### quality_control_flags

Eaplains the by-variables quality control flags supplied as part of the dataset. This notebook covers how to apply the existing flags, and how to produce new flags using the IOOS QARTOD toolbox with user-defined threshold values.

------------------------------


# Misc notebooks

### mission_filter

More ways to get a list of missions of intereste by project, basin of the Baltic, timespan etc.

### more_smhi_data

Downloading more data from SMHI's sharkweb datastore, subsetting requests by year


------------------------------

If you have any queries, requests or suggestions, please raise an Issue or PR or emaail me at callum.rollo@voiceoftheocean.org

### Acknowledements

This repo would not be possible without the excellent [erddapy](https://github.com/ioos/erddapy) library. These notebooks have benefitted from the feedback and suggestions of [MartinMohrmann](https://github.com/MartinMohrmann), [Chiara Monforte](https://github.com/MOchiara) and Joanna Paczkowska.
