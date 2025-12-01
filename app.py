import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------------------------------
# Tabela de limites (IDEB)
# -------------------------------
limites = pd.DataFrame({
    "Ano": ["5EF","5EF","9EF","9EF","3EM","3EM"],
    "Disciplina": ["MT","LP","MT","LP","MT","LP"],
    "Lim_Inferior": [60,49,100,100,111,117],
    "Lim_Superior": [322,324,400,400,467,451]
})

# -------------------------------
# Funções auxiliares
# -------------------------------
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

def calcular_proficiencia(df, etapa, disciplina):
    dados = df[(df["Etapa"] == etapa) & (df["Componente Curricular"] == disciplina)]
    if dados.empty:
        return None
    return dados["Proficiência Média"].mean()

def calcular_pmp(prof_media, ano, disciplina):
    if prof_media is None:
        return None
    lim = limites[(limites["Ano"] == ano) & (limites["Disciplina"] == disciplina)]
    if lim.empty:
        return None
    lim = lim.iloc[0]
    return ((prof_media - lim["Lim_Inferior"]) / (lim["Lim_Superior"] - lim["Lim_Inferior"])) * 10

def rendimento_ensino_medio(df):
    cols = ["1ª série","2ª série","3ª série"]
    valores = [float(df[c].iloc[0]) for c in cols]
    hm = len(valores) / sum(1.0/v for v in valores)
    return hm / 100.0

def rendimento_anos_iniciais(df):
    cols = ["1º ano","2º ano","3º ano","4º ano","5º ano"]
    valores = [float(df[c].iloc[0]) for c in cols]
    hm = len(valores) / sum(1.0/v for v in valores)
    return hm / 100.0

def rendimento_anos_finais(df):
    cols = ["6º ano","7º ano","8º ano","9º ano"]
    valores = [float(df[c].iloc[0]) for c in cols]
    hm = len(valores) / sum(1.0/v for v in valores)
    return hm / 100.0

def calcular_iders(df_proficiencia, df_rendimento_fundamental, df_rendimento_medio):
    indicadores = {}
# ANOS INICIAIS:
    prof_lp_5 = df_proficiencia[(df_proficiencia["Disciplina"] == "LP") & (df_proficiencia["Serie"] == "5")]["Proficiencia"].mean()
    prof_mt_5 = df_proficiencia[(df_proficiencia["Disciplina"] == "MT") & (df_proficiencia["Serie"] == "5")]["Proficiencia"].mean()

    if not pd.isna(prof_lp_5) and not pd.isna(prof_mt_5):
        prof_iniciais = (prof_lp_5 + prof_mt_5) / 2
        rend_iniciais = df_rendimento_fundamental.loc[:, ["1º Ano","2º Ano","3º Ano","4º Ano","5º Ano"]].mean(axis=1).iloc[0] / 100
        indicadores["Anos Iniciais"] = prof_iniciais * rend_iniciais
    else:
        indicadores["Anos Iniciais"] = None


    # Anos finais
    prof_lp_9 = df_proficiencia[(df_proficiencia["Disciplina"] == "LP") & (df_proficiencia["Serie"] == "9")]["Proficiencia"].mean()
    prof_mt_9 = df_proficiencia[(df_proficiencia["Disciplina"] == "MT") & (df_proficiencia["Serie"] == "9")]["Proficiencia"].mean()

    if not pd.isna(prof_lp_9) and not pd.isna(prof_mt_9):
        prof_finais = (prof_lp_9 + prof_mt_9) / 2
        rend_finais = df_rendimento_fundamental.loc[:, ["6º Ano","7º Ano","8º Ano","9º Ano"]].mean(axis=1).iloc[0] / 100
        indicadores["Anos Finais"] = prof_finais * rend_finais
    else:
        indicadores["Anos Finais"] = None


    # Ensino médio
   prof_lp_3 = df_proficiencia[(df_proficiencia["Disciplina"] == "LP") & (df_proficiencia["Serie"] == "3")]["Proficiencia"].mean()
    prof_mt_3 = df_proficiencia[(df_proficiencia["Disciplina"] == "MT") & (df_proficiencia["Serie"] == "3")]["Proficiencia"].mean()

    if not pd.isna(prof_lp_3) and not pd.isna(prof_mt_3):
        prof_medio = (prof_lp_3 + prof_mt_3) / 2
        rend_medio = df_rendimento_medio.loc[:, ["1ª série","2ª série","3ª série"]].mean(axis=1).iloc[0] / 100
        indicadores["Ensino Médio"] = prof_medio * rend_medio
    else:
        indicadores["Ensino Médio"] = None

    return indicadores

# -------------------------------
# Menu lateral
# -------------------------------
painel = st.sidebar.radio(
    "Escolha o painel:",
    ["📊 Painel de Desempenho SAERS - Habilidades", "📈 Painel de Indicadores"]
)

# -------------------------------
# Painel de Desempenho Escolar
# -------------------------------
if painel == "📊 Painel de Desempenho SAERS - Habilidades":
    df_diagnostico = pd.read_csv("df_diagnostico.csv")

    etapa_selecionada = st.sidebar.selectbox(
        "Selecione a etapa:",
        df_diagnostico["ANO ESCOLAR"].unique()
    )
    df_etapa = df_diagnostico[df_diagnostico["ANO ESCOLAR"] == etapa_selecionada]

    col_lp, col_mt = st.columns(2)

    with col_lp:
        fig_lp = px.bar(
            df_etapa[df_etapa["COMPONENTE CURRICULAR"] == "LP"],
            x="HABILIDADE - ACERTO %",
            y="HABILIDADE - DESCRIÇÃO",
            color="HABILIDADE - FAIXA",
            orientation="h",
            title=f"LP - {etapa_selecionada}",
            text="HABILIDADE - ACERTO %",
            color_discrete_map={"Baixo":"#FF0000","Médio Baixo":"#FFA500","Médio Alto":"#FFFF00","Alto":"#008000"}
        )
        fig_lp.update_layout(yaxis_title=None)
        fig_lp.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_lp, use_container_width=True)

    with col_mt:
        fig_mt = px.bar(
            df_etapa[df_etapa["COMPONENTE CURRICULAR"] == "MT"],
            x="HABILIDADE - ACERTO %",
            y="HABILIDADE - DESCRIÇÃO",
            color="HABILIDADE - FAIXA",
            orientation="h",
            title=f"MT - {etapa_selecionada}",
            text="HABILIDADE - ACERTO %",
            color_discrete_map={"Baixo":"#FF0000","Médio Baixo":"#FFA500","Médio Alto":"#FFFF00","Alto":"#008000"}
        )
        fig_mt.update_layout(yaxis_title=None)
        fig_mt.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_mt, use_container_width=True)

# -------------------------------
# Painel de Indicadores – IDERS 2024
# -------------------------------
else:
    st.subheader("📊 Painel de Indicadores Educacionais - IDERS 2024")

    # Carregar dados atualizados
    df_proficiencia = pd.read_csv("df_proficiencias24.csv")
    df_proficiencia["Disciplina"] = df_proficiencia["Disciplina"].str.upper()
    df_proficiencia["Serie"] = df_proficiencia["Serie"].astype(str)

    df_rendimento_fundamental = pd.read_csv("df_rendimento_fundamental_24.csv")
    df_rendimento_fundamental.columns = df_rendimento_fundamental.columns.str.strip()

    df_rendimento_medio = pd.read_csv("df_rendimento_medio24.csv")
    df_rendimento_medio.columns = df_rendimento_medio.columns.str.strip()

    # Calcular indicadores com a função revisada
    indicadores = calcular_iders(df_proficiencia, df_rendimento_fundamental, df_rendimento_medio)

    # 1️⃣ Métricas
    col1, col2, col3 = st.columns(3)
    for i, etapa in enumerate(["Anos Iniciais", "Anos Finais", "Ensino Médio"]):
        valor = indicadores.get(etapa)
        if valor is None:
            [col1, col2, col3][i].warning(f"⚠️ Não foi possível calcular o IDERS para {etapa}.")
        else:
            [col1, col2, col3][i].metric(etapa, f"{valor:.2f}")

    # 2️⃣ Imagem explicativa
    st.image("indicadores.png", caption="Entendendo os indicadores", use_column_width=True)

    # 3️⃣ Botão para download do PDF
    with open("explicacao_indicadores.pdf", "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="📄 Baixar PDF explicativo sobre os indicadores",
        data=pdf_bytes,
        file_name="indicadores_IDERS_2024.pdf",
        mime="application/pdf"
    )
