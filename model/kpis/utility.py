import pandas as pd


def find_geo_zone_numbers(df):
    return df["Servicers"].apply(lambda x: pd.value_counts([y.geo_zone for y in x]))


def find_shutdown_services_number(df):
    return df["Services"].apply(lambda x: sum([y.shutdown for y in x]))
