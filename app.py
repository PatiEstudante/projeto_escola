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

# -------------------------------
# Menu lateral
# -------------------------------
painel = st.sidebar.radio(
    "Escolha o painel:",
    ["📊 Painel de Desempenho Escolar", "📈 Painel de Indicadores"]
)

# -------------------------------
# Painel de Desempenho Escolar
# -------------------------------
if painel == "📊 Painel de Desempenho Escolar":
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
        fig_lp.updade_layout(yaxis_title=None)
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
        fig_mt.updade_layout(yaxis_title=None)
        fig_mt.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_mt, use_container_width=True)

# -------------------------------
# Painel de Indicadores
# -------------------------------
else:
    st.subheader("📈 Painel de Indicadores Educacionais - IDERS 2023")

    # Carregar dados
    df_proficiencia = pd.read_csv("df_proficiencia.csv")
    df_proficiencia["Etapa"] = (
        df_proficiencia["Etapa"]
        .str.replace(r"\s+", " ", regex=True)  # substitui múltiplos espaços por um só
        .str.strip()                           # remove espaços extras
        .str.upper()                           # coloca tudo em maiúsculo
    )

    df_rendimento_fundamental = pd.read_csv("df_rendimento_fundamental.csv")
    df_rendimento_fundamental.columns = df_rendimento_fundamental.columns.str.strip().str.lower()

    df_rendimento_medio = pd.read_csv("df_rendimento_medio.csv")
    df_rendimento_medio.columns = df_rendimento_medio.columns.str.strip().str.lower()

    # Calcular indicadores
    indicadores = calcular_iders(df_proficiencia, df_rendimento_fundamental, df_rendimento_medio)

    # Exibir métricas lado a lado
    col1, col2, col3 = st.columns(3)
    for i, etapa in enumerate(["Anos Iniciais", "Anos Finais", "Ensino Médio"]):
        valor = indicadores.get(etapa)
        if valor is None:
            [col1, col2, col3][i].warning(f"⚠️ Não foi possível calcular o IDERS para {etapa}.")
        else:
            [col1, col2, col3][i].metric(etapa, f"{valor:.2f}")
    
    st.image("indicadores.png", caption="Painel de Indicadores Educacionais - IDERS 2023", use_column_width=True)
    
    with open("explicacao_indicadores.pdf", "rb") as f:
        pdf_bytes = f.read()

    st.download_button(label="📄 Baixar PDF explicativo sobre os indicadores",
                       data=pdf_bytes,
                       file_name="indicadores_IDERS_IDEB.pdf",
                       mime="application/pdf")
