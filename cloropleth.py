import itertools
import json
from urllib.request import urlopen

import geopandas as gpd
import pandas as pd
import plotly.express as px


def read_data(fpath):
    df = pd.read_excel(fpath, skiprows=2)
    z = itertools.product(regions, m)
    colnames = ["quarter"] + ["_".join(map(str, x)) for x in z]
    df.columns = colnames
    qs = [f"{x.split()[1]}-{x.split()[0]}" for x in df["quarter"]]
    df["quarter"] = pd.PeriodIndex(qs, freq="Q").to_timestamp()
    return df


# North East
# Yorkshire and The Humber
# North West
# East Midlands
# West Midlands
# Eastern
# London
# South East
# South West
# Scotland
# Wales


regions = [
    "north",
    "yorks_hside",
    "north_west",
    "east_mids",
    "west_mids",
    "east_anglia",
    "outer_s_east",
    "outer_met",
    "london",
    "south_west",
    "wales",
    "scotland",
    "n_ireland",
    "uk",
]
m = ["price", "index"]


fpath = "Counties_and_Unitary_Authorities_(December_2020)_UK_BFC/Counties_and_Unitary_Authorities_(December_2020)_UK_BFC.shp"
geodf = gpd.read_file(fpath)
geodf.to_file("geojson.json", driver="GeoJSON")

with open("geojson.json") as geofile:
    json = json.load(geofile)


code = "CTYUA20CD"
counties = []
for i in json["features"]:
    counties.append(i["properties"][code])

url = "http://publicdata.landregistry.gov.uk/market-trend-data/house-price-index-data/Average-prices-2021-03.csv?utm_medium=GOV.UK&utm_source=datadownload&utm_campaign=average_price&utm_term=9.30_19_05_21"
df = pd.read_csv(url)
df = df[df['Date'] == '2021-01-01']

df = df[df["Area_Code"].isin(counties)]

fig = px.choropleth(geodf, geojson=geodf.geometry, locations=geodf['CTYUA20NM'], color="Shape__Len")
fig.update_geos(fitbounds="locations", visible=False)
fig.show()

# df = px.data.election()
# geo_df = gpd.GeoDataFrame.from_features(
#     px.data.election_geojson()["features"]
# ).merge(df, on="district").set_index("district")
# fig = px.choropleth(df, json, locations="Area_Code", featureidkey="properties.CTYUA20CD")

# uh = urlopen(url)

# import requests
# response = requests.get(url)
# todos = json.loads(response.text)

# for i in geojson['features']:
#     print(i['properties'])


# with urlopen(
#         "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/electoral/gb/eer.json"
# ) as response:
#     geojson = json.load(response)

# df = read_data("test.xls")

# df = df[[x for x in list(df) if 'price' in x]]
# df = df.T.reset_index()

# dict_items([('type', 'FeatureCollection'), ('features', [{'type': 'Feature', 'properties': {'GEO_ID': '0500000US01001', 'STATE': '01', 'COUNTY': '001'

# for i in geojson['features']:
#     print(i['properties']['EER13NM'])


# counties2['features'][0]['properties']
# px.cloropleth(df, json, featureidkey="properties.EER13NM")
