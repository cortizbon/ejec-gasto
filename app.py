import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Ejecución presupuestal | Enero - Mayo")

df = pd.read_csv("ejecucion_enero_mayo.csv")
df.loc[::, ['APR. INICIAL', 'PAGOS']] = df.loc[::, ['APR. INICIAL', 'PAGOS']] / 1_000_000_000
rubros = df['DESCRIPCION'].unique().tolist()
sectores = df['Sector'].unique().tolist()

sector = st.selectbox("Seleccione el sector: ", sectores)

fil = df[df['Sector'] == sector]
entidades = fil['Entidad'].unique().tolist()

entidad = st.selectbox("Seleccione la entidad: ", entidades)

t_ent = (fil[fil['Entidad'] == entidad]
         .groupby(['Tipo de gasto', 'mes_num', 'mes'])['PAGOS']
         .sum()
         .reset_index()
         .sort_values(by='mes_num')
         .drop(columns='mes_num'))

tipo_gasto = st.selectbox("Seleccione el tipo de gasto: ", t_ent['Tipo de gasto'].unique().tolist())

piv_f = t_ent[t_ent['Tipo de gasto'] == tipo_gasto]
val = df[(df['Tipo de gasto'] == tipo_gasto) & (df['Entidad'] == entidad)].groupby(['mes_num','mes'])['APR. INICIAL'].sum().unique()[0]
fig = px.line(piv_f, x='mes', y='PAGOS')

fig.add_hline(y=val, line=dict(color='red', dash='dash'))
fig.update_layout(yaxis_tickformat='.0f')
st.plotly_chart(fig)


