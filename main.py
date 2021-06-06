import pandas as pd
import requests
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def read_data(fpath):
    df = pd.read_excel(fpath, skiprows=2)
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
    z = itertools.product(regions, m)
    colnames = ["quarter"] + ["_".join(map(str, x)) for x in z]
    df.columns = colnames
    qs = [f"{x.split()[1]}-{x.split()[0]}" for x in df["quarter"]]
    df["quarter"] = pd.PeriodIndex(qs, freq="Q").to_timestamp()
    return df


fpath = "test.xls"
url = "https://www.nationwide.co.uk/-/media/MainSite/documents/about/house-price-index/downloads/all-prop.xls"
resp = requests.get(url)
with open(fpath, "wb") as output:
    output.write(resp.content)

df = read_data(fpath)


fig = px.line(df, x="quarter", y="north_price")
# fig.update_yaxes(ticklabelposition="inside top", title=None)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=3, label="1Q", step="month", stepmode="backward"),
            dict(count=4, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig.show()

# np.tile(regions, m)

# # url = "https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv"
# urllib.request.urlretrieve(url, "test.xls")
# # For Python 3s = requests.get(url).content
# c = pd.read_excel(io.StringIO(s.decode("ISO-8859-1")))
