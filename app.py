import streamlit as st
import pandas as pd
import plotly.express as px

# Função para quebrar texto longo
def quebrar_texto(texto, limite=50):
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        if len(linha_atual) + len(palavra) < limite:
            linha_atual += palavra + " "
        else:
            linhas.append(linha_atual.strip())
            linha_atual = palavra + " "
    linhas.append(linha_atual.strip())
    return "\n".join(linhas)

# Título do dashboard
st.markdown("<h1 style='color:#1d3557;'>📊 Painel de Desempenho Escolar</h1>", unsafe_allow_html=True)

# Sidebar com filtro por turma
st.sidebar.title("🎯 Filtros")
turma_selecionada = st.sidebar.selectbox("Selecione a turma", ["Todas"] + list(pd.read_csv("df_diagnostico.csv")["ANO ESCOLAR"].unique()))

# Carregar dados
diagnostica = pd.read_csv("df_diagnostico.csv")
diagnostica.columns = diagnostica.columns.str.strip()
somativa = pd.read_csv("df_somativa.csv")

# Aplicar filtro de turma
if turma_selecionada != "Todas":
    diagnostica = diagnostica[diagnostica["ANO ESCOLAR"] == turma_selecionada]

# Separar habilidades por faixa
diag_habilidades_abaixo = diagnostica[diagnostica["HABILIDADE - FAIXA"].isin(["Baixo", "Médio Baixo"])]
diag_habilidades_acima = diagnostica[diagnostica["HABILIDADE - FAIXA"].isin(["Médio Alto", "Alto"])]

# Ordenar e quebrar texto
for df in [diag_habilidades_abaixo, diag_habilidades_acima]:
    df.sort_values("HABILIDADE - ACERTO %", inplace=True)
    df["HABILIDADE - DESCRIÇÃO"] = df["HABILIDADE - DESCRIÇÃO"].apply(quebrar_texto)

# Criar gráficos
fig_abaixo = px.bar(
    diag_habilidades_abaixo,
    x="HABILIDADE - ACERTO %",
    y="HABILIDADE - DESCRIÇÃO",
    color="HABILIDADE - FAIXA",
    orientation="h",
    hover_data=["COMPONENTE CURRICULAR"],
    title="🔴 Habilidades que precisam ser melhoradas",
    text="HABILIDADE - ACERTO %",
    color_discrete_map={"Baixo":"#e63946", "Médio Baixo":"#f4a261"}
)

fig_abaixo.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_abaixo.update_layout(yaxis_title="Habilidade", xaxis_title="Percentual de Acerto", height=800, font=dict(size=12))

fig_acima = px.bar(
    diag_habilidades_acima,
    x="HABILIDADE - ACERTO %",
    y="HABILIDADE - DESCRIÇÃO",
    color="HABILIDADE - FAIXA",
    orientation="h",
    hover_data=["COMPONENTE CURRICULAR"],
    title="🟢 Habilidades consolidadas",
    text="HABILIDADE - ACERTO %",
    color_discrete_map={"Médio Alto":"#2a9d8f", "Alto":"#1d3557"}
)

fig_acima.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_acima.update_layout(yaxis_title="Habilidade", xaxis_title="Percentual de Acerto", height=800, font=dict(size=12))

# Tabs para exibir os gráficos
tab1, tab2 = st.tabs(["🔴 A melhorar", "🟢 Consolidadas"])

with tab1:
    st.plotly_chart(fig_abaixo, use_container_width=True)

with tab2:
    st.plotly_chart(fig_acima, use_container_width=True)
