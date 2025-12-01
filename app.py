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

    # Padronização mínima
    df_proficiencia["Disciplina"] = df_proficiencia["Disciplina"].str.upper()
    df_proficiencia["Serie"] = df_proficiencia["Serie"].astype(str)
    df_rendimento_fundamental.columns = df_rendimento_fundamental.columns.str.strip()
    df_rendimento_medio.columns = df_rendimento_medio.columns.str.strip()

    # -------------------------
    # Função auxiliar: normalizar proficiência pelos limites
    # -------------------------
    def normalizar_proficiencia(ano, disciplina, valor):
        linha = limites[(limites["Ano"] == ano) & (limites["Disciplina"] == disciplina)]
        if linha.empty or pd.isna(valor):
            return None
        lim_inf = linha["Lim_Inferior"].values[0]
        lim_sup = linha["Lim_Superior"].values[0]
        return ((valor - lim_inf) / (lim_sup - lim_inf)) * 10

    # -------------------------
    # Proficências normalizadas
    # -------------------------
    prof_lp_5_raw = df_proficiencia[(df_proficiencia["Disciplina"] == "LP") & (df_proficiencia["Serie"] == "5")]["Proficiencia"].mean()
    prof_mt_5_raw = df_proficiencia[(df_proficiencia["Disciplina"] == "MT") & (df_proficiencia["Serie"] == "5")]["Proficiencia"].mean()
    prof_lp_5 = normalizar_proficiencia("5EF", "LP", prof_lp_5_raw)
    prof_mt_5 = normalizar_proficiencia("5EF", "MT", prof_mt_5_raw)

    prof_lp_9_raw = df_proficiencia[(df_proficiencia["Disciplina"] == "LP") & (df_proficiencia["Serie"] == "9")]["Proficiencia"].mean()
    prof_mt_9_raw = df_proficiencia[(df_proficiencia["Disciplina"] == "MT") & (df_proficiencia["Serie"] == "9")]["Proficiencia"].mean()
    prof_lp_9 = normalizar_proficiencia("9EF", "LP", prof_lp_9_raw)
    prof_mt_9 = normalizar_proficiencia("9EF", "MT", prof_mt_9_raw)

    prof_lp_3_raw = df_proficiencia[(df_proficiencia["Disciplina"] == "LP") & (df_proficiencia["Serie"] == "3")]["Proficiencia"].mean()
    prof_mt_3_raw = df_proficiencia[(df_proficiencia["Disciplina"] == "MT") & (df_proficiencia["Serie"] == "3")]["Proficiencia"].mean()
    prof_lp_3 = normalizar_proficiencia("3EM", "LP", prof_lp_3_raw)
    prof_mt_3 = normalizar_proficiencia("3EM", "MT", prof_mt_3_raw)

    # -------------------------
    # Rendimentos por média harmônica
    # -------------------------
    def media_harmonica_percentuais(valores):
        vals = [v for v in valores if pd.notna(v)]
        if len(vals) == 0:
            return None
        inv_sum = sum(1.0 / v for v in vals)
        mh = len(vals) / inv_sum
        return mh / 100.0

    if not df_rendimento_fundamental.empty:
        linha_fund = df_rendimento_fundamental.iloc[0]
        rend_iniciais = media_harmonica_percentuais([linha_fund.get("1º Ano"), linha_fund.get("2º Ano"),
                                                     linha_fund.get("3º Ano"), linha_fund.get("4º Ano"),
                                                     linha_fund.get("5º Ano")])
        rend_finais = media_harmonica_percentuais([linha_fund.get("6º Ano"), linha_fund.get("7º Ano"),
                                                   linha_fund.get("8º Ano"), linha_fund.get("9º Ano")])
    else:
        rend_iniciais = None
        rend_finais = None

    if not df_rendimento_medio.empty:
        linha_medio = df_rendimento_medio.iloc[0]
        rend_medio = media_harmonica_percentuais([linha_medio.get("1ª série"), linha_medio.get("2ª série"),
                                                  linha_medio.get("3ª série")])
    else:
        rend_medio = None

    # -------------------------
    # IDERS por etapa (proficiências normalizadas × rendimento)
    # -------------------------
    if prof_lp_5 is not None and prof_mt_5 is not None and rend_iniciais is not None:
        indicadores["Anos Iniciais"] = round(((prof_lp_5 + prof_mt_5) / 2.0) * rend_iniciais, 2)
    else:
        indicadores["Anos Iniciais"] = None

    if prof_lp_9 is not None and prof_mt_9 is not None and rend_finais is not None:
        indicadores["Anos Finais"] = round(((prof_lp_9 + prof_mt_9) / 2.0) * rend_finais, 2)
    else:
        indicadores["Anos Finais"] = None

    if prof_lp_3 is not None and prof_mt_3 is not None and rend_medio is not None:
        indicadores["Ensino Médio"] = round(((prof_lp_3 + prof_mt_3) / 2.0) * rend_medio, 2)
    else:
        indicadores["Ensino Médio"] = None

    return indicadores
# -------------------------------
# Menu lateral
# -------------------------------

painel = st.sidebar.radio(
    "Escolha o painel:",
    [
        "📊 Painel de Desempenho SAERS - Habilidades",
        "📈 Painel de Indicadores",
        "🎯 Painel de Metas"
    ]
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
    
elif painel == "🎯 Painel de Metas":
    st.subheader("🎯 Metas por Etapa - IDERS 2024")

    # Criar DataFrame com as metas
    df_metas = pd.DataFrame({
        "Etapa": ["Anos Iniciais", "Anos Finais", "Ensino Médio"],
        "Meta": [5.43, 5.03, 4.66]
    })

    # Exibir tabela
    st.table(df_metas)


