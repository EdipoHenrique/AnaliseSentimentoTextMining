# Análise de Sentimentos dos Depoimentos de Clientes

Este é um aplicativo desenvolvido em **Streamlit** para realizar análise de sentimentos em depoimentos coletados via Google Forms. O sistema utiliza VADER (via NLTK) com tradução automática, gera visualizações como nuvens de palavras, gráficos de pizza e permite busca textual, além de exportação dos resultados.

## Funcionalidades

- Upload de arquivos `.xlsx` extraídos do Google Forms
- Tradução automática dos textos do português para o inglês
- Análise de sentimento com VADER (compound)
- Classificação em positivo, negativo e neutro
- Nuvem de palavras com remoção de pontuação, stopwords e nomes próprios
- Proteção contra erros quando não há avaliações negativas ou positivas
- Gráfico de pizza com proporção dos sentimentos
- Busca por palavra-chave nos depoimentos
- Exportação final da base em formato Excel
- Interface adaptada para leigos com mensagens amigáveis

## Como executar

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

2. Ative o ambiente:
   - No Windows:
     ```bash
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o app:
   ```bash
   streamlit run app_streamlit_monitor_offline_v5.py
   ```

## Autor

Desenvolvido por Édipo Henrique Teles Leite como parte de projeto analítico com foco em qualidade de atendimento e visualização de insights textuais.
