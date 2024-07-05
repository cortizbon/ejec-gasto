import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO

st.title("Ejecución presupuestal | Enero - Mayo")

df = pd.read_csv("ejecucion_enero_mayo.csv")

df2 = df.copy()
df2.loc[::, ['APR. VIGENTE', 'COMPROMISO']] = df2.loc[::, ['APR. VIGENTE', 'COMPROMISO']] / 1_000_000_000
rubros = df2['DESCRIPCION'].unique().tolist()
sectores = df2['Sector'].unique().tolist()

sector = st.selectbox("Seleccione el sector: ", sectores)

fil = df2[df2['Sector'] == sector]
entidades = fil['Entidad'].unique().tolist()

entidad = st.selectbox("Seleccione la entidad: ", entidades)

t_ent = (fil[fil['Entidad'] == entidad]
         .groupby(['Tipo de gasto', 'mes_num', 'mes'])['COMPROMISO']
         .sum()
         .reset_index()
         .sort_values(by='mes_num')
         .drop(columns='mes_num'))

tipo_gasto = st.selectbox("Seleccione el tipo de gasto: ", t_ent['Tipo de gasto'].unique().tolist())

piv_f = t_ent[t_ent['Tipo de gasto'] == tipo_gasto]
val = (df2[(df2['Tipo de gasto'] == tipo_gasto) & (df2['Entidad'] == entidad)]
       .groupby(['mes_num','mes'])['APR. VIGENTE']
       .sum()
       .unique()[4]
)
fig = px.line(piv_f, x='mes', y='COMPROMISO')

fig.add_hline(y=val, line=dict(color='red', dash='dash'))
fig.update_layout(yaxis_tickformat='.0f',
                  title=f'Ejecución por entidad ({entidad}) y tipo de gasto ({tipo_gasto}) <br><sup>Cifras en miles de millones de pesos</sup>')
st.plotly_chart(fig)


piv_f['Porcentaje'] = ((piv_f['COMPROMISO'] / val) * 100).round(1)

fig = px.line(piv_f, x='mes', y='Porcentaje')

fig.add_hline(y=100, line=dict(color='red', dash='dash'))
fig.update_layout(yaxis_tickformat='.0f',
                  title=f'Ejecución por entidad ({entidad}) y tipo de gasto ({tipo_gasto}) <br><sup>Poncentaje del total</sup>')
st.plotly_chart(fig)


binary_output = BytesIO()
df.to_excel(binary_output, index=False)
st.download_button(label = 'Descargar excel',
                    data = binary_output.getvalue(),
                    file_name = 'datos.xlsx')