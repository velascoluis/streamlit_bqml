# ............................................................
# STREAMLIT App
# ............................................................

import streamlit as st 
import pandas as pd 
import pandas_gbq
import plotly.express as px 
import datetime, time
from google.cloud import bigquery

# .... Variables
PROJECT_ID='TO_DO_DEVELOPER'
DATASET_ID='TO_DO_DEVELOPER'
TABLE_ID='TO_DO_DEVELOPER'
NUM_CLUSTERS_MAX=10


# .... Helper functions
def read_table_dataframe():
    client = bigquery.Client()
    dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET_ID)
    table_ref = dataset_ref.table(TABLE_ID)
    table = client.get_table(table_ref)
    df = client.list_rows(table).to_dataframe()
    return df

def score_data(num_clusters):
  client = bigquery.Client()
  bqml_predict_model_sql = f"""
    SELECT
      * EXCEPT(NEAREST_CENTROIDS_DISTANCE)
    FROM
      ML.PREDICT(MODEL `{DATASET_ID}.customer_clusters_{num_clusters}`,
      (
        SELECT
          *
        FROM
          `{DATASET_ID}.{TABLE_ID}`))
    """
  df = client.query(bqml_predict_model_sql).to_dataframe()
  pandas_gbq.to_gbq(df, f'{DATASET_ID}.table_scored', project_id=PROJECT_ID,if_exists='replace')
  return df

def calulate_clusters(num_clusters):
    client = bigquery.Client()
    bqml_create_model_sql = f"""
      CREATE OR REPLACE MODEL
        `{DATASET_ID}.customer_clusters_{num_clusters}`
      OPTIONS
      ( MODEL_TYPE='KMEANS',
        NUM_CLUSTERS={num_clusters} ) AS
      SELECT
        *
    FROM `{DATASET_ID}.{TABLE_ID}`
    """
    job = client.query(bqml_create_model_sql)
    job_id = job.job_id
    job_state = job.state
    while  job_state == "RUNNING":
       time.sleep(5)
       job = client.get_job(job_id)
       job_state = job.state
       placeholder_job = st.empty()
       with placeholder_job.container():
        st.write(f"Job {job.job_id} is  {job_state} ...")
       
def export_cluster_to_table(cluster_export,table_export):
  client = bigquery.Client()
  dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET_ID)
  table_ref = dataset_ref.table('table_scored')
  table = client.get_table(table_ref)
  df_scored = client.list_rows(table).to_dataframe()
  df_scored_filtered = df_scored[df_scored['CENTROID_ID'] == cluster_export]
  pandas_gbq.to_gbq(df_scored_filtered, table_export, project_id=PROJECT_ID,if_exists='replace')
  st.write("Table loaded!")

# .... App

df = read_table_dataframe()

st.markdown('# Generador de audiencias basado en clustering con BQML')
st.markdown('### Datos crudos')
st.dataframe(df)
 
st.markdown('### Numero de clusters')
num_clusters = st.selectbox('Num clusters',[*range(1, NUM_CLUSTERS_MAX, 1)])
if st.button("Calcular clusters"):
    calulate_clusters(num_clusters)
    st.balloons()
if st.button("Score datos"):
  df_scored = score_data(num_clusters)
  st.markdown('### Datos crudos con cluster asociado')
  st.dataframe(df_scored)
  st.markdown('### Distribucion de clusters')
  df_plot = df_scored.groupby(['CENTROID_ID'])['CENTROID_ID'].count().reset_index(name='count')
  fig = px.pie(df_plot, values='count', names='CENTROID_ID', title='Clusters')
  st.write(fig)
cluster_export = st.selectbox('Cluster a exportar',[*range(1, num_clusters, 1)])
table_export = st.text_input("BQ tabla a export destino")
if st.button("Exportar cluster"):
   export_cluster_to_table(cluster_export,table_export)
        


