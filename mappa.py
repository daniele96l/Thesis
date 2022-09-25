import plotly.express as px
import pandas as pd


df = pd.read_csv('/Users/danieleligato/Desktop/Thesis/point_projection/example.csv')  

print("Getting data...")
df = px.data.carshare()
print(df['centroid_lon'])
fig = px.scatter_mapbox(
                        lon=df['centroid_lon'],
                        lat=df['centroid_lat'],
                        zoom=3,
                        width=1200,
                        height=900,
                        title='Map')

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
fig.show()
print("done")


