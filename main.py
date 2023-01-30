from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import numpy as np

# Construct a BigQuery client object.

storage_credentials = service_account.Credentials.from_service_account_file('ensai-2023-373710-4e0c22304fd9.json')
client = bigquery.Client(credentials=storage_credentials)
"""
# La SNCF Toujour en retard ? 	:train2:
By Nous
"""



query = """
    SELECT distinct gare_label from `ensai-2023-373710.grp.late`
"""
query_job = client.query(query)  # Make an API request.


makes = query_job.to_dataframe()['gare_label']
make_choice = st.sidebar.selectbox('Selectionne ta gare:', makes)

query = "SELECT * from `ensai-2023-373710.grp.late` where gare_label like '"+make_choice+"'"
print(query)

query_job2 = client.query(query) 
print(query_job2)
df= pd.DataFrame(query_job2.to_dataframe())
df_retard=df[df['retard'].gt(0)]
df_time=df[df['retard'].eq(0)]

st.dataframe(df)


df_count_time =  df_time.groupby(['name'])['name'].count()
df_count_retard =  df_retard.groupby(['name'])['name'].count()  
df_sum_retard =  df_retard.groupby(['name'])['retard'].sum()  

t1=pd.DataFrame({'Train':df_count_time.index, "Nombre train à l'heure":df_count_time.values})
t2=pd.DataFrame({'Train':df_count_retard.index, 'Nombre train en retard':df_count_retard.values})
t3=pd.merge(t1,t2,on="Train")
#st.dataframe(pd.DataFrame(df_count).transpose())
"""
### Nombre de trains à l'heures et en retards :steam_locomotive:
""" 
st.bar_chart(t3,x="Train",y=["Nombre train à l'heure","Nombre train en retard"],width=480, height=900)

t4=pd.DataFrame({'Train':df_sum_retard.index, 'Somme du retard':df_sum_retard.values})
t5=pd.merge(t4,t2,on="Train")
t5["Moyenne retard"] = t5["Somme du retard"]/t5["Nombre train en retard"]

st.dataframe(t5)

"""
### Nombre de train en retards par jour :train:
"""
options = df['name'].unique().tolist()
opt=st.multiselect('Train(s) à visualiser',options)
df_retard2=df[df["name"].isin(opt)]
test = df_retard2.groupby(["jour"])['jour'].count()  

t6=pd.DataFrame({'Jour':test.index , "Nombre train en retard": test.values})


st.line_chart(t6,x='Jour',y='Nombre train en retard')



# with st.echo(code_location='below'):
#     total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

#     Point = namedtuple('Point', 'x y')
#     data = []

#     points_per_turn = total_points / num_turns

#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))

#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q'))
