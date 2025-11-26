import streamlit as st
import pandas as pd
import plotly.express as px

# Upload dos dados
diagnostica = pd.read_csv("df_diagnostico.csv", delimiter=";")
somativa = pd.read_csv("df_somativa.csv", delimiter=";")

# Filtrar habilidades com desempenho baixo
df_filtrado = diagnostica[diagnostica["HABILIDADE - FAIXA"].isin(["Baixo", "Médio Baixo"])]
df_filtrado = df_filtrado.sort_values("HABILIDADE - ACERTO %")

# Gráfico
fig = px.bar(
    df_filtrado,
    x="HABILIDADE - DESCRIÇÃO",
    y="HABILIDADE - ACERTO %",
    color="HABILIDADE - FAIXA",
    title="Habilidades que precisam ser melhoradas",
    text="HABILIDADE - ACERTO %"
)
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(xaxis_title="Habilidade", yaxis_title="Percentual de Acerto")

# Exibir no Streamlit
st.title("📊 Dashboard de Desempenho Escolar")
st.plotly_chart(fig, use_container_width=True)