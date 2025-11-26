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
    color_discrete_map={"Médio Alto":"#457b9d", "Alto":"#2a9d8f"}
)

fig_acima.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig_acima.update_layout(yaxis_title="Habilidade", xaxis_title="Percentual de Acerto", height=800, font=dict(size=12))

# Tabs para exibir os gráficos
tab1, tab2 = st.tabs(["🔴 Pontos a melhorar", "🟢 Pontos a manter"])

with tab1:
    st.plotly_chart(fig_abaixo, use_container_width=True)

with tab2:
    st.plotly_chart(fig_acima, use_container_width=True)


import pandas as pd
import streamlit as st

#-------------------------------
#     CÁLCULO DO IDERS 2023
#-------------------------------

# -------------------------------
# 1. Tabela de limites
# -------------------------------
limites = pd.DataFrame({
    "Ano": ["5EF","5EF","9EF","9EF","3EM","3EM"],
    "Disciplina": ["MT","PT","MT","PT","MT","PT"],
    "Lim_Inferior": [60,49,100,100,111,117],
    "Lim_Superior": [322,324,400,400,467,451]
})

# -------------------------------
# 2. Função para calcular proficiência média
# -------------------------------
def calcular_proficiencia(df, etapa, disciplina):
    dados = df[(df["Etapa"] == etapa) & (df["Componente Curricular"] == disciplina)]
    if dados.empty:
        return None
    # média ponderada pela quantidade de turmas
    prof_media = (dados["Proficiência Média"].sum()) / dados["Turmas"].sum()
    return prof_media

# -------------------------------
# 3. Função para calcular PMP
# -------------------------------
def calcular_pmp(prof_media, ano, disciplina):
    lim = limites[(limites["Ano"] == ano) & (limites["Disciplina"] == disciplina)].iloc[0]
    pmp = ((prof_media - lim["Lim_Inferior"]) / (lim["Lim_Superior"] - lim["Lim_Inferior"])) * 10
    return pmp

# -------------------------------
# 4. Funções de rendimento
# -------------------------------
def rendimento_anos_iniciais(df):
    tx = sum([1/df[col].iloc[0] for col in ["1º Ano","2º Ano","3º Ano","4º Ano","5º Ano"]])
    return 5/tx

def rendimento_anos_finais(df):
    tx = sum([1/df[col].iloc[0] for col in ["6º Ano","7º Ano","8º Ano","9º Ano"]])
    return 4/tx

def rendimento_ensino_medio(df):
    tx = sum([1/df[col].iloc[0] for col in ["1ª série","2ª série","3ª série"]])
    return 3/tx

# -------------------------------
# 5. Cálculo do IDERS
# -------------------------------
def calcular_iders(df_proficiencia, df_rendimento_fundamental, df_rendimento_medio):
    # Anos iniciais
    prof_lp = calcular_proficiencia(df_proficiencia, "ENSINO FUNDAMENTAL - 5º ANO", "LP")
    prof_mt = calcular_proficiencia(df_proficiencia, "ENSINO FUNDAMENTAL - 5º ANO", "MT")
    pmp_lp = calcular_pmp(prof_lp, "5EF", "PT")
    pmp_mt = calcular_pmp(prof_mt, "5EF", "MT")
    prof_iniciais = (pmp_lp + pmp_mt)/2
    rend_iniciais = rendimento_anos_iniciais(df_rendimento_fundamental)
    iders_iniciais = prof_iniciais * rend_iniciais

    # Anos finais
    prof_lp9 = calcular_proficiencia(df_proficiencia, "ENSINO FUNDAMENTAL - 9º ANO", "LP")
    prof_mt9 = calcular_proficiencia(df_proficiencia, "ENSINO FUNDAMENTAL - 9º ANO", "MT")
    pmp_lp9 = calcular_pmp(prof_lp9, "9EF", "PT")
    pmp_mt9 = calcular_pmp(prof_mt9, "9EF", "MT")
    prof_finais = (pmp_lp9 + pmp_mt9)/2
    rend_finais = rendimento_anos_finais(df_rendimento_fundamental)
    iders_finais = prof_finais * rend_finais

    # Ensino médio
    prof_lp3 = calcular_proficiencia(df_proficiencia, "ENSINO MEDIO - 3ª SERIE", "LP")
    prof_mt3 = calcular_proficiencia(df_proficiencia, "ENSINO MEDIO - 3ª SERIE", "MT")
    pmp_lp3 = calcular_pmp(prof_lp3, "3EM", "PT")
    pmp_mt3 = calcular_pmp(prof_mt3, "3EM", "MT")
    prof_medio = (pmp_lp3 + pmp_mt3)/2
    rend_medio = rendimento_ensino_medio(df_rendimento_medio)
    iders_medio = prof_medio * rend_medio

    return {
        "Anos Iniciais": iders_iniciais,
        "Anos Finais": iders_finais,
        "Ensino Médio": iders_medio
    }

# -------------------------------
# 6. Exibir no dashboard
# -------------------------------
# Exemplo de uso:
# df_proficiencia = pd.read_csv("df_proficiencia.csv")
# df_rendimento_fundamental = pd.read_csv("df_rendimento_fundamental.csv")
# df_rendimento_medio = pd.read_csv("df_rendimento_medio.csv")

# indicadores = calcular_iders(df_proficiencia, df_rendimento_fundamental, df_rendimento_medio)

# st.subheader("📈 Indicador Educacional da Escola (IDERS)")
# col1, col2, col3 = st.columns(3)
# col1.metric("Anos Iniciais", f"{indicadores['Anos Iniciais']:.2f}")
# col2.metric("Anos Finais", f"{indicadores['Anos Finais']:.2f}")
# col3.metric("Ensino Médio", f"{indicadores['Ensino Médio']:.2f}")

