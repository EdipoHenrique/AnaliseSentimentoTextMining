# -*- coding: utf-8 -*-
"""
Created on Sun May  7 00:19:10 2025

@author: Édipo
"""

import streamlit as st
import pandas as pd
import nltk
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

#%% Configurações da Página
st.set_page_config(page_title="Análise de Avaliações - Monte Olimpo / Axé Fit", layout="wide")

nltk.download('stopwords')
stop_words = set(stopwords.words('portuguese'))
nltk.download('punkt')

#%% Lista de palavras personalizadas que devem ser removidas da nuvem
stop_words_personalizadas = {
    "murcha", "molenga", "fria", "batata", "gelada", "coca-cola", "coca",
    "devaney", "alisson", "luciana", "letícia", "leticia", "alfredo",
    "jéssica", "jessica", "adrian"
}

#%% Cabeçalho visual
col1, col2 = st.columns(2)
with col1:
    st.image("monte_olimpo.jpg", caption="Hamburgueria Monte Olimpo", width=250)
with col2:
    st.image("axe_fit.jpg", caption="Academia Axé Fit", width=250)

st.title("📝 Análise de Avaliações Coletadas dos Clientes")
st.markdown("Este painel exibe uma nuvem de palavras, gráfico e tabela com os termos mais citados nas avaliações fornecidas pelos clientes ao final do atendimento.")

nltk.download('vader_lexicon')  # VADER necessário para análise de sentimento

#%% Upload do arquivo Excel
st.sidebar.header("Upload das Avaliações")
uploaded_file = st.sidebar.file_uploader("Faça upload do arquivo .xlsx exportado do Google Forms", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Identifica coluna de depoimentos
    col_depoimentos = [col for col in df.columns if "experiência" in col.lower()]
    if not col_depoimentos:
        st.error("Não foi possível encontrar a coluna de depoimentos automaticamente.")
        st.stop()

    col_depo = col_depoimentos[0]
    df.rename(columns={col_depo: "Texto_Cliente"}, inplace=True)
    df["Texto_Cliente"] = df["Texto_Cliente"].astype(str)

    # Tradução
    with st.spinner("Traduzindo os textos..."):
        df["Traduzido"] = df["Texto_Cliente"].apply(
            lambda x: GoogleTranslator(source='auto', target='en').translate(x)
        )

    # Análise de Sentimentos
    sia = SentimentIntensityAnalyzer()
    df["Pontuação"] = df["Traduzido"].apply(lambda x: sia.polarity_scores(x)["compound"])

    def classificar_sentimento(score):
        if score >= 0.05:
            return "positivo"
        elif score <= -0.05:
            return "negativo"
        else:
            return "neutro"

    df["Sentimento"] = df["Pontuação"].apply(classificar_sentimento)

    st.success("Análise concluída!")

    # Buscar por palavra-chave
    st.subheader("🔍 Buscar Depoimentos por Palavra")
    search_query = st.text_input("Digite uma palavra-chave:")
    if search_query:
        resultado = df[df["Texto_Cliente"].str.contains(search_query, case=False, na=False)]
        st.write(f"{len(resultado)} depoimento(s) encontrados:")
        st.dataframe(resultado[["Texto_Cliente", "Sentimento"]])

    # Gráfico de Sentimentos
    st.subheader("📊 Distribuição dos Sentimentos")
    fig_pie = px.pie(df, names="Sentimento", title="Proporção de Sentimentos", width=800, height=500)
    st.plotly_chart(fig_pie)

    # Função de Nuvem de Palavras
    st.subheader("☁️ Nuvens de Palavras por Sentimento")
    col1, col2 = st.columns(2)

    def gerar_wordcloud(textos, titulo, colormap):
        raw_text = " ".join(textos).lower()
        raw_text = raw_text.translate(str.maketrans("", "", string.punctuation))

        palavras = raw_text.split()
        palavras_filtradas = [
            word for word in palavras
            if word not in stop_words and word not in stop_words_personalizadas
        ]

        if not palavras_filtradas:
            if titulo.lower() == "negativo":
                st.success("🎉 Excelente! Nenhuma avaliação negativa encontrada. Isso demonstra um ótimo atendimento.")
            else:
                st.warning(f"Não há palavras suficientes para gerar a nuvem de palavras para: **{titulo}**")
            return

        text_filtrado = " ".join(palavras_filtradas)
        wc = WordCloud(width=600, height=300, background_color="white", colormap=colormap).generate(text_filtrado)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    with col1:
        st.markdown("**Depoimentos Positivos 😃**")
        gerar_wordcloud(df[df["Sentimento"] == "positivo"]["Texto_Cliente"], "Positivo", "YlGn")

    with col2:
        st.markdown("**Depoimentos Negativos 😡**")
        gerar_wordcloud(df[df["Sentimento"] == "negativo"]["Texto_Cliente"], "Negativo", "viridis")

    # Exibição Final
    st.subheader("📄 Tabela com Sentimentos")
    st.dataframe(df[["Texto_Cliente", "Traduzido", "Pontuação", "Sentimento"]])

    # Download do CSV
    st.download_button(
        label="📥 Baixar análise como CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="analise_sentimentos_clientes.csv",
        mime="text/csv"
    )

else:
    st.info("Por favor, faça upload de um arquivo .xlsx contendo os depoimentos dos clientes.")
