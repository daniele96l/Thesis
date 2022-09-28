import plotly.express as px
import pandas as pd
import utm

df = pd.read_csv('dati_mappa.csv')
df2 = pd.DataFrame()
df3 = pd.DataFrame(columns = ['X', 'Y', 'Z', 'Name', 'Confidence', 'N frame'])
df3 = [0]

j = 0
for i in range(len(df)-1):
    if((str(df.iloc[[i]]["Name"][i]) == str(df.iloc[[i+1]]["Name"][i+1])) and str(df.iloc[[i]]["N frame"][i]) == str(df.iloc[[i+1]]["N frame"][i+1]-1)):
        df2 = df2.append(df.iloc[[i]])
        df2 = df2.append(df.iloc[[i+1]])
        df2.at[i,"Confidence"] = j 
        df2.at[i+1,"Confidence"] = j 
    else:
        df2 = df2.append(df3)
        j+=1
        
duplicati = df2.groupby(["Confidence", "Name"]).mean()

duplicati.reset_index(level=1, inplace=True)

unici = (pd.merge(df,df2, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1))

df2.drop([0, 'Confidence'], axis = 1, inplace = True) 
df.drop(['Confidence'], axis = 1, inplace = True) 
unici = pd.merge(df,df2, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)

tutti= unici.append(duplicati)

df_converted = tutti


#3.62952577e+05,5.10747292e+06,1.86774772e+02,information--pedestrians-crossing--g1,0.38,621
#print(utm.to_latlon(362805.9, 5108178.297, 33, 'T'))

df_converted["X"],df_converted["Y"] = utm.to_latlon(tutti["X"], tutti["Y"], 33, 'T')

print(unici)

df_converted["N frame"] = 2
print("Getting data...")
df = px.data.carshare()
#print(df['centroid_lon'])
fig = px.scatter_mapbox(
                        lon=df_converted['Y'],
                        lat=df_converted['X'],
                        color = df_converted['Name'],
                        zoom=15,
                        size= df_converted["N frame"],
                        width=1200,
                        height=900,
                        title='Map')

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
fig.show()
print("done")


