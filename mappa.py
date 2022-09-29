import plotly.express as px
import pandas as pd
import utm

df = pd.read_csv('dati_mappa.csv')
df2 = pd.DataFrame()
df3 = pd.DataFrame(columns = ['X', 'Y', 'Z', 'Name', 'Confidence', 'N frame'])
df3 = [0]

j = 0
for i in range(len(df)-2):
    if((str(df.iloc[[i]]["Name"][i]) == str(df.iloc[[i+1]]["Name"][i+1])) and str(df.iloc[[i]]["N frame"][i]) == str(df.iloc[[i+1]]["N frame"][i+1]-1) or (str(df.iloc[[i]]["Name"][i]) == str(df.iloc[[i+1]]["Name"][i+1])) and str(df.iloc[[i]]["N frame"][i]) == str(df.iloc[[i+2]]["N frame"][i+2]-1)):
        df2 = df2.append(df.iloc[[i]])
        df2 = df2.append(df.iloc[[i+1]])
        df2.at[i,"Confidence"] = j  #trovo i segnali duplicati e faccio in modo
        df2.at[i+1,"Confidence"] = j  #che una colonna sia UGUALE (che non sia il nome) in modo da poter usare la group by
    else:
        df2 = df2.append(df3)
        j+=1
        
duplicati = df2.groupby(["Confidence", "Name"]).mean() #faccio la media dei miei segnali che sono duplicati

duplicati.reset_index(level=1, inplace=True)

df2.drop([0, 'Confidence'], axis = 1, inplace = True) #preparo i due array per essere mergiati eliminando
df.drop(['Confidence'], axis = 1, inplace = True)  #eliminando quelli presenti vicendevolemnte
unici = pd.merge(df,df2, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)

tutti= unici.append(duplicati)

df_converted = tutti

df_converted["X"],df_converted["Y"] = utm.to_latlon(tutti["X"], tutti["Y"], 33, 'T')

df_converted["Z"] = tutti['Z'] #mi servità per settare la dimensione dei cartelli
print("Getting data...")
df = px.data.carshare()
z = tutti["Z"].fillna(0)
#print(df['centroid_lon'])
fig = px.scatter_mapbox(
                        lon=df_converted['Y'],
                        lat=df_converted['X'],
                        color = df_converted['Name'],
                        zoom=15,
                        size= z,
                        width=1200,
                        height=900,
                        title='Map')

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
fig.show()
print("done")


