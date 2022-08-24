import xarray as xr
import datetime
import pandas as pd
import numpy as np
import cartopy
from erddapy import ERDDAP
from argopy import DataFetcher as ArgoDataFetcher


def init_erddap():
    # Setup initial ERDDAP connection
    e = ERDDAP(
        server="https://erddap.observations.voiceoftheocean.org/erddap",
        protocol="tabledap",
    )
    return e


def find_glider_datasets(nrt_only=True):
    """
    Find the dataset IDs of all glider datasets on the VOTO ERDDAP server
    nrt_only: if True, only returns nrt datasets
    """
    e = init_erddap()

    # Fetch dataset list

    e.response = "csv"
    e.dataset_id = "allDatasets"
    df_datasets = e.to_pandas()

    datasets = df_datasets.datasetID
    # Select only nrt datasets
    if nrt_only:
        datasets = datasets[datasets.str[:3] == "nrt"]
    return datasets.values


def download_glider_dataset(dataset_ids, variables=(
"latitude", "longitude", "salinity", "temperature", "time", "pressure", "oxygen_concentration", "chlorophyll",
)):
    """
    Download datasets from the VOT server using a supplied list of dataset IDs.
    variables: data variables to download
    """
    e = init_erddap()
    # Specify variables of interest
    e.variables = variables

    # Download each dataset and swhite gloves khruangbinave as xarray
    glider_datasets = {}
    for ds_name in dataset_ids:
        e.dataset_id = ds_name
        ds = e.to_xarray()
        glider_datasets[ds_name] = ds
    return glider_datasets


def format_difference(deg_e, deg_n, ns_ahead):
    """
    Pretty formatting for a lon, lat, time difference between two points
    """
    km_n = (111 * deg_n).round(1)
    km_e = (111 * deg_e * np.cos(np.deg2rad(deg_n))).round(1)
    h_ahead = (np.float64(ns_ahead) / (1e9 * 60 * 60)).round(1)
    if km_n > 0:
        north_str = f"{km_n} km N"
    else:
        north_str = f"{-km_n} km S"
    if km_e > 0:
        east_str = f"{km_e} km E"
    else:
        east_str = f"{-km_e} km W"
    if h_ahead > 0:
        time_str = f"{h_ahead} hours later"
    else:
        time_str = f"{-h_ahead} hours earlier"
    return east_str, north_str, time_str


def smhi_profiles_in_range(station_visit_df, lon, lat, time, lon_window, lat_window, time_window, min_depth=80):
    """
    Returns the station IDs of stations within a certain range of a point in space and time
    """
    min_lon = lon - lon_window
    max_lon = lon + lon_window
    min_lat = lat - lat_window
    max_lat = lat + lat_window
    min_time = time - time_window
    max_time = time + time_window
    lon_filter = np.logical_and(station_visit_df['Sample longitude (DD)'] > min_lon, station_visit_df['Sample longitude (DD)'] < max_lon)
    lat_filter = np.logical_and(station_visit_df['Sample latitude (DD)'] > min_lat, station_visit_df['Sample latitude (DD)'] < max_lat)
    time_filter = np.logical_and(station_visit_df['Sampling date'] > min_time, station_visit_df['Sampling date'] < max_time)
    df_in_range = station_visit_df[lon_filter & lat_filter & time_filter]
    # Filter out shallow stations
    df_in_range = df_in_range[df_in_range['Station water depth'] > min_depth]
    if df_in_range.empty:
        return None

    closest_arg = np.argmin(np.abs(df_in_range['Sampling date'] - time))
    closest_datasetid = df_in_range.index[closest_arg]
    return closest_datasetid


def nearest_smhi_station(df, station_visit_df, ds_glider, lat_window=0.5, lon_window=1, time_window=np.timedelta64(10, "D")):
    """
    Finds the nearest SMHI station profile to a supplied glidermission. Uses sharkweb data file
    """
    mean_lon = ds_glider.longitude.mean().values
    mean_lat = ds_glider.latitude.mean().values
    mean_time = ds_glider.time.mean().values
    nearest_profile = smhi_profiles_in_range(station_visit_df, mean_lon, mean_lat, mean_time, lat_window, lon_window, time_window)
    if nearest_profile:
        closest_station = station_visit_df[station_visit_df.index == nearest_profile]
        deg_e = mean_lon - closest_station['Sample longitude (DD)'].values[0]
        deg_n = mean_lat - closest_station['Sample latitude (DD)'].values[0]
        time_diff = mean_time - closest_station['Sampling date'].values[0]
        east_diff, north_diff, time_diff = format_difference(deg_e, deg_n, time_diff)
        loc_str = f"Nearest station profile is {east_diff}, {north_diff} & {time_diff} than mean of glider data"
        print(loc_str)
        df_nearest = df[df.station_visit == nearest_profile]
        return df_nearest
    else:
        print("No SMHI profiles found within tolerances")
        return None


def nearest_argo_profile(ds_glider, lat_window=0.5, lon_window=1, time_window=np.timedelta64(7, "D")):
    """
    Finds the nearest argo profile to a supplied glidermission. Uses ifremer ERDDAP
    """
    mean_lon = ds_glider.longitude.mean().values
    mean_lat = ds_glider.latitude.mean().values
    mean_time = ds_glider.time.mean().values
    max_pressure = ds_glider.pressure.values.max()
    min_time = str(mean_time - time_window)[:10]
    max_time = str(mean_time + time_window)[:10]
    search_region = [mean_lon - lon_window, mean_lon + lon_window,
                     mean_lat - lat_window, mean_lat + lat_window,
                     0, max_pressure,
                     min_time, max_time]
    try:
        ds = ArgoDataFetcher(src='erddap').region(search_region).to_xarray()
        ds2 = ds.argo.point2profile()
        closest_time_index = np.abs(ds2.TIME.values - mean_time).argmin()
        profile = ds2.isel({"N_PROF": closest_time_index})
        deg_n = profile.LATITUDE.values - np.nanmean(ds_glider.latitude)
        deg_e = profile.LONGITUDE.values - np.nanmean(ds_glider.longitude)
        ns_ahead = profile.TIME.values - ds_glider.time.mean()
        east_diff, north_diff, time_diff = format_difference(deg_e, deg_n, ns_ahead)
        loc_str = f"Nearest float is {east_diff}, {north_diff} & {time_diff} than mean of glider data"
        print(loc_str)
        return profile
    except:
        print("No floats found within tolerances")
        return None
