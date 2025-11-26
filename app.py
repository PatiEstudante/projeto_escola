import streamlit as st
import pandas as pd
import plotly.express as px

# Upload dos dados
diagnostica = pd.read_csv("df_diagnostico.csv")
somativa = pd.read_csv("df_somativa.csv")

# Filtrar habilidades com desempenho baixo
diag_habilidades_abaixo = diagnostica[diagnostica["HABILIDADE - FAIXA"].isin(["Baixo", "Médio Baixo"])]
diag_habilidades_abaixo = diag_habilidades_abaixo.sort_values("HABILIDADE - ACERTO %")
fig = px.bar(
    diag_habilidades_abaixo,
    x="HABILIDADE - DESCRIÇÃO",
    y="HABILIDADE - ACERTO %",
    color="HABILIDADE - FAIXA",
    title="Habilidades que precisam ser melhoradas",
    text="HABILIDADE - ACERTO %"
)

fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(xaxis_title="Habilidade", yaxis_title="Percentual de Acerto")

# Exibir no Streamlit
st.plotly_chart(fig, use_container_width=True)