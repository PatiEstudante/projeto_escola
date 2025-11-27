import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# Tabela de limites (IDEB)

limites = pd.DataFrame({
    "Ano": ["5EF","5EF","9EF","9EF","3EM","3EM"],
    "Disciplina": ["MT","LP","MT","LP","MT","LP"],
    "Lim_Inferior": [60,49,100,100,111,117],
    "Lim_Superior": [322,324,400,400,467,451]
})


# 1. Função para quebrar texto longo (HABILIDADES)
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

#2. Função para calcular proficiência média

def calcular_proficiencia(df, etapa, disciplina):
    dados = df[(df["Etapa"] == etapa) & (df["Componente Curricular"] == disciplina)]
    if dados.empty:
        return None
    # Média simples entre as proficiências por turma
    return dados["Proficiência Média"].mean()

# 3. Função para calcular PMP

def calcular_pmp(prof_media, ano, disciplina):
    if prof_media is None:
        return None
    lim = limites[(limites["Ano"] == ano) & (limites["Disciplina"] == disciplina)]
    if lim.empty:
        return None  # evita IndexError
    lim = lim.iloc[0]
    return ((prof_media - lim["Lim_Inferior"]) / (lim["Lim_Superior"] - lim["Lim_Inferior"])) * 10

#4. Funções de rendimento

def _to_decimal(v):
    # aceita string com vírgula, porcentagem ou número
    if pd.isna(v):
        return None
    if isinstance(v, str):
        v = v.strip().replace('%', '').replace(',', '.')
    try:
        x = float(v)
    except:
        return None
    # se vier como 79.9 (0–100), converte para 0.799
    return x/100.0 if x > 1 else x

def _harmonic_mean(values):
    vals = [_to_decimal(v) for v in values]
    if any(v is None or v <= 0 for v in vals):
        return None
    return len(vals) / sum(1.0/v for v in vals)

def rendimento_anos_iniciais(df):
    cols = ["1º Ano","2º Ano","3º Ano","4º Ano","5º Ano"]
    return _harmonic_mean([df[c].iloc[0] for c in cols])

def rendimento_anos_finais(df):
    cols = ["6º Ano","7º Ano","8º Ano","9º Ano"]
    return _harmonic_mean([df[c].iloc[0] for c in cols])

def rendimento_ensino_medio(df):
    cols = ["1ª série","2ª série","3ª série"]
    return _harmonic_mean([df[c].iloc[0] for c in cols])


# 5. Cálculo do IDERS

def calcular_iders(df_proficiencia, df_rendimento_fundamental, df_rendimento_medio):
    # Anos iniciais
    prof_lp = calcular_proficiencia(df_proficiencia, "ENSINO FUNDAMENTAL - 5º ANO", "LP")
    prof_mt = calcular_proficiencia(df_proficiencia, "ENSINO FUNDAMENTAL - 5º ANO", "MT")
    pmp_lp = calcular_pmp(prof_lp, "5EF", "LP")
    pmp_mt = calcular_pmp(prof_mt, "5EF", "MT")

    if pmp_lp is not None and pmp_mt is not None:
        prof_iniciais = (pmp_lp + pmp_mt) / 2
        rend_iniciais = rendimento_anos_iniciais(df_rendimento_fundamental)
        iders_iniciais = prof_iniciais * rend_iniciais
    else:
        iders_iniciais = None

    # Anos finais
    prof_lp9 = calcular_proficiencia(df_proficiencia, "ENSINO FUNDAMENTAL - 9º ANO", "LP")
    prof_mt9 = calcular_proficiencia(df_proficiencia, "ENSINO FUNDAMENTAL - 9º ANO", "MT")
    pmp_lp9 = calcular_pmp(prof_lp9, "9EF", "LP")
    pmp_mt9 = calcular_pmp(prof_mt9, "9EF", "MT")

    if pmp_lp9 is not None and pmp_mt9 is not None:
        prof_finais = (pmp_lp9 + pmp_mt9) / 2
        rend_finais = rendimento_anos_finais(df_rendimento_fundamental)
        iders_finais = prof_finais * rend_finais
    else:
        iders_finais = None

    # Ensino médio
    prof_lp3 = calcular_proficiencia(df_proficiencia, "ENSINO MEDIO - 3ª SERIE", "LP")
    prof_mt3 = calcular_proficiencia(df_proficiencia, "ENSINO MEDIO - 3ª SERIE", "MT")
    pmp_lp3 = calcular_pmp(prof_lp3, "3EM", "LP")
    pmp_mt3 = calcular_pmp(prof_mt3, "3EM", "MT")

    if pmp_lp3 is not None and pmp_mt3 is not None:
        prof_medio = (pmp_lp3 + pmp_mt3) / 2
        rend_medio = rendimento_ensino_medio(df_rendimento_medio)
        iders_medio = prof_medio * rend_medio
    else:
        iders_medio = None

    return {
        "Anos Iniciais": iders_iniciais,
        "Anos Finais": iders_finais,
        "Ensino Médio": iders_medio
    }

#----------------------------------------------
#             MENU DE SELEÇÃO
#----------------------------------------------

painel = st.sidebar.radio(
    "Escolha o painel:",
    ["📊 Painel de Desempenho Escolar", "📈 Painel de Indicadores"]
)

#------------------------------------------------
# PAINEL DE DESEMPENHO ESCOLAR
#-----------------------------------------------

if painel == "📊 Painel de Desempenho Escolar":
    diagnostica = pd.read_csv("df_diagnostico.csv")

    # Filtros e preparação
    diag_habilidades_abaixo = diagnostica[diagnostica["HABILIDADE - FAIXA"].isin(["Baixo", "Médio Baixo"])]
    diag_habilidades_acima = diagnostica[diagnostica["HABILIDADE - FAIXA"].isin(["Médio Alto", "Alto"])]

    for df in [diag_habilidades_abaixo, diag_habilidades_acima]:
        df.sort_values("HABILIDADE - ACERTO %", inplace=True)
        df["HABILIDADE - DESCRIÇÃO"] = df["HABILIDADE - DESCRIÇÃO"].apply(quebrar_texto)

# Gráfico habilidades abaixo
    fig_abaixo = px.bar(
        diag_habilidades_abaixo,
        x="HABILIDADE - ACERTO %",
        y="HABILIDADE - DESCRIÇÃO",
        color="HABILIDADE - FAIXA",
        orientation="h",
        title="🔴 Habilidades que precisam ser melhoradas",
        text="HABILIDADE - ACERTO %",
        color_discrete_map={"Baixo":"#e63946", "Médio Baixo":"#f4a261"}
    )
    fig_abaixo.update_traces(texttemplate='%{text:.1f}%', textposition='outside')

    # Gráfico habilidades acima
    fig_acima = px.bar(
        diag_habilidades_acima,
        x="HABILIDADE - ACERTO %",
        y="HABILIDADE - DESCRIÇÃO",
        color="HABILIDADE - FAIXA",
        orientation="h",
        title="🟢 Habilidades consolidadas",
        text="HABILIDADE - ACERTO %",
        color_discrete_map={"Médio Alto":"#457b9d", "Alto":"#2a9d8f"}
    )
    fig_acima.update_traces(texttemplate='%{text:.1f}%', textposition='outside')

    # Tabs
    tab1, tab2 = st.tabs(["🔴 A melhorar", "🟢 Consolidadas"])
    with tab1:
        st.plotly_chart(fig_abaixo, use_container_width=True)
    with tab2:
        st.plotly_chart(fig_acima, use_container_width=True)


# -------------------------------
# PAINEL DE INDICADORES
# -------------------------------
else:
    st.subheader("📈 Painel de Indicadores Educacionais - IDERS 2023")

    # Carregar dados
    df_proficiencia = pd.read_csv("df_proficiencia.csv")
    df_rendimento_fundamental = pd.read_csv("df_rendimento_fundamental.csv")
    df_rendimento_medio = pd.read_csv("df_rendimento_medio.csv")

# Calcular indicadores
indicadores = calcular_iders(df_proficiencia, df_rendimento_fundamental, df_rendimento_medio)

st.subheader("🔍 Verificação dos valores para Ensino Médio")
st.write({
    "Proficiência LP (média)": calcular_proficiencia(df_proficiencia, "ENSINO MEDIO - 3ª SERIE", "LP"),
    "Proficiência MT (média)": calcular_proficiencia(df_proficiencia, "ENSINO MEDIO - 3ª SERIE", "MT"),
    "PMP LP": calcular_pmp(265, "3EM", "LP"),
    "PMP MT": calcular_pmp(244, "3EM", "MT"),
    "Rendimento": rendimento_ensino_medio(df_rendimento_medio),
    "IDERS Ensino Médio": indicadores["Ensino Médio"]
})


for etapa, valor in indicadores.items():
    if valor is None:
        st.warning(f"⚠️ Não foi possível calcular o IDERS para {etapa}. Verifique os dados.")
    else:
        st.metric(etapa, f"{valor:.2f}")


    # Exibir métricas lado a lado
col1, col2, col3 = st.columns(3)

for i, etapa in enumerate(["Anos Iniciais", "Anos Finais", "Ensino Médio"]):
    valor = indicadores.get(etapa)
    if valor is None:
        [col1, col2, col3][i].warning(f"⚠️ Não foi possível calcular o IDERS para {etapa}. Verifique os dados.")
    else:
        [col1, col2, col3][i].metric(etapa, f"{valor:.2f}")



    # Opcional: gráfico comparativo
    st.bar_chart(pd.DataFrame.from_dict(indicadores, orient="index", columns=["IDERS 2023"]))
