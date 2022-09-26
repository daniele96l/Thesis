import plotly.express as px
import pandas as pd

import utm



df = pd.read_csv('/Users/danieleligato/Desktop/Thesis/point_projection/example.csv')
df_converted = df

#3.62952577e+05,5.10747292e+06,1.86774772e+02,information--pedestrians-crossing--g1,0.38,621
#print(utm.to_latlon(362805.9, 5108178.297, 33, 'T'))


df_converted["X"],df_converted["Y"] = utm.to_latlon(df["X"], df["Y"], 33, 'T')

print(df_converted)




print("Getting data...")
df = px.data.carshare()
print(df['centroid_lon'])
fig = px.scatter_mapbox(
                        lon=df_converted['Y'],
                        lat=df_converted['X'],
                        color = df_converted['Name'],
                        zoom=15,
                        size = df_converted["Confidence"]/2,
                        width=1200,
                        height=900,
                        title='Map')

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
fig.show()
print("done")


