import plotly.express as px
import pandas as pd
import utm
import numpy as np

df = pd.read_csv('dati_mappa.csv').dropna(axis = 0, how = 'any').reset_index(drop=True)
totale = df
print(df)
df2 = pd.DataFrame()
df3 = pd.DataFrame(columns = ['X', 'Y', 'Z', 'Name', 'Confidence', 'N frame'])
df3 = [0]

j = 0
for i in range(len(df)-2):
    if(((str(df.iloc[[i]]["Name"][i]) == str(df.iloc[[i+1]]["Name"][i+1])) and (df.iloc[[i]][['X','Y','Z']].mean(axis = 1)[i]  - df.iloc[[i+1]][['X','Y','Z']].mean(axis = 1)[i+1]) < 10) or ((str(df.iloc[[i]]["Name"][i]) == str(df.iloc[[i+2]]["Name"][i+2])) and  (df.iloc[[i]][['X','Y','Z']].mean(axis = 1)[i]  - df.iloc[[i+2]][['X','Y','Z']].mean(axis = 1)[i+2]) < 10)):
        df2 = df2.append(df.iloc[[i]])
        df2 = df2.append(df.iloc[[i+1]])
        df2.at[i,"Confidence"] = j  #trovo i segnali duplicati e faccio in modo
        df2.at[i+1,"Confidence"] = j  #che una colonna sia UGUALE (che non sia il nome) in modo da poter usare la group by
    else:
        df2 = df2.append(df3)
        j+=1
        
duplicati = df2.groupby(["Confidence", "Name"]).mean() #faccio la media dei miei segnali che sono duplicati


duplicati.reset_index(level=1, inplace=True)


#df2.drop([0, 'Confidence'], axis = 1, inplace = True) #preparo i due array per essere mergiati eliminando (exclusive join)
df.drop(['Confidence'], axis = 1, inplace = True)  #eliminando quelli presenti vicendevolemnte
unici = pd.merge(df,df2, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
s_unici = unici
tutti= unici.append(duplicati)

tutti_2 = tutti['N frame'].round().astype(str).str[:-3]
tutti_2 = tutti_2.to_frame()
tutti_2 = tutti_2.reset_index()
tutti_2 = tutti_2.rename(columns={'N frame': 'proximity'})

#mm = triplicati.reset_index().round()
tutti[0] = tutti_2['proximity']

   
triplicati = tutti.groupby([0, "Name"]).mean() #faccio la media dei miei segnali che sono duplicati

#---------

df_converted = triplicati
#df_converted = totale
#----------

df_converted['Name'] = df_converted.index
c = df_converted["Name"]

df_converted["X"],df_converted["Y"] = utm.to_latlon(df_converted["X"], df_converted["Y"], 33, 'T')
print(df_converted)
print("Getting data...")

z = df_converted["Z"].fillna(0)
z = np.where(z>200 , 200, z)
#print(df['centroid_lon'])
fig = px.scatter_mapbox(
                        lon=df_converted['Y'],
                        lat=df_converted['X'],
                        color = c,
                        zoom=15,
                        size= z,
                        width=1200,
                        height=900,
                        title='Map')

'''fig = px.scatter_mapbox(
                        lon=df_converted['Y'],
                        lat=df_converted['X'],
                        zoom=15,
                        width=1200,
                        height=900,
                        title='Map')'''

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
fig.show()
print("done")


