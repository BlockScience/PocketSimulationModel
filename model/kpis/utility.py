import pandas as pd

def find_geo_zone_numbers(df):
    return df['Servicers'].apply(lambda x: pd.value_counts([y.geo_zone for y in x]))