import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuração das colunas e pesos por posição
colunas_por_posicao = {
    "Goleiros": ["jogador", "time", "posicao", "GA", "Saves", "Clean Sheet", "PSxG", "Passes Launch%", "Crosses Stp%", "Sweeper #OPA"],
    "Meias Ofensivos": ["jogador", "time", "posicao", "xG", "xAG", "G-PK", "Assistencias", "Key_Pass", "Passing 1/3", "Cross", "%Dribles"],
    "Pontas": ["jogador", "time", "posicao", "xG+xAg", "KeyPass", "Cross", "1/3", "Dribles Certos", "Corridas 1/3", "Corridas PA", "passPA", "crossPA"],
    "Volantes": ["jogador", "time", "posicao", "Amarelo", "Vermelho", "Falta Cometida", "interceptacao", "recuperacoes", "Duelos Aereoes W", "Divididas Ganhas", "Clearence", "Erros"],
    "Zagueiros": ["jogador", "time", "posicao", "Aerial Duel Won", "Fouls", "Yellow Card", "Red Card", "Desarmes Certos", "Interceptacao", "Erros"],
    "Laterais": ["jogador", "time", "posicao", "xAG", "Fouls", "Yellow Card", "Red Card", "Cross", "Desarmes Certos", "Interceptacao", "Erros"],
    "Atacantes": ["jogador", "time", "posicao", "xG", "xAG", "G-PK", "Assistencias", "Acoes Ofensivas", "Aerial Duel%"]
}

# Função para calcular pontuação personalizada
def calcular_pontuacao(df, pesos):
    for coluna, peso in pesos.items():
        if coluna in df.columns:
            df[coluna + '_Pontuacao'] = df[coluna].fillna(0) * peso

    colunas_pontuacao = [coluna + '_Pontuacao' for coluna in pesos.keys() if coluna in df.columns]
    df['Pontuacao_Total'] = df[colunas_pontuacao].sum(axis=1)
    df['Pontuacao'] = (df['Pontuacao_Total'] - df['Pontuacao_Total'].min()) / (df['Pontuacao_Total'].max() - df['Pontuacao_Total'].min()) * 100
    return df

# Função para carregar múltiplos arquivos CSV de um repositório do GitHub
def carregar_dados_github():
    base_url = "https://raw.githubusercontent.com/ohallao/MoneyBall-Brasileirao/main/Output_Cluster/"
    arquivos = ["Gol_clusters_full.csv", "Mei_clusters_full.csv", "Ponta_clusters_full.csv", "vol_clusters_full.csv", "Zag_clusters_full.csv", "Lat_clusters_full.csv", "striker_clusters_full.csv"]
    
    dfs = []
    for arquivo in arquivos:
        url = base_url + arquivo
        try:
            df = pd.read_csv(url)
            dfs.append(df)
        except Exception as e:
            st.error(f"Erro ao carregar {arquivo}: {e}")
    
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

# Carregar os dados automaticamente do GitHub
df = carregar_dados_github()

st.title("MoneyBall Brasileirao - Análise por Posição")

if df.empty:
    st.error("Não foi possível carregar os dados. Verifique os arquivos no GitHub.")
else:
    st.write("### Dados do Arquivo")
    st.dataframe(df, height=300)

    # Filtro por posição
    posicao_escolhida = st.sidebar.selectbox("Escolha uma posição", options=colunas_por_posicao.keys())
    if posicao_escolhida:
        colunas = colunas_por_posicao[posicao_escolhida]
        df_filtrado = df[colunas].dropna()

        # Filtro por time
        times_disponiveis = df_filtrado['time'].unique()
        time_selecionado = st.sidebar.selectbox("Filtrar por time", options=["Todos"] + list(times_disponiveis))
        if time_selecionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado['time'] == time_selecionado]

        # Ajuste dinâmico dos pesos
        st.sidebar.subheader("Ajuste os Pesos")
        pesos_customizados = {}
        for coluna in colunas[3:]:
            pesos_customizados[coluna] = st.sidebar.slider(f"Peso para {coluna}", -10.0, 10.0, 1.0, 0.1)
        
        if st.sidebar.button("Redefinir Pesos"):
            pesos_customizados = {coluna: 1.0 for coluna in colunas[3:]}  # Redefinir para o valor padrão

        df_com_pontuacao = calcular_pontuacao(df_filtrado, pesos_customizados)
        df_ordenado = df_com_pontuacao.sort_values(by='Pontuacao', ascending=False)
        df_ordenado['Ranking'] = range(1, len(df_ordenado) + 1)

        st.write(f"### Ranking de jogadores para posição: {posicao_escolhida}")
        st.dataframe(df_ordenado[['Ranking', 'jogador', 'time', 'Pontuacao']])

        # Comparação entre jogadores
        st.header("Comparação de Jogadores - Gráfico de Radar")
        jogadores_selecionados = st.multiselect("Selecione jogadores:", df_ordenado['jogador'].unique())
        if jogadores_selecionados:
            st.write("### Estatísticas dos Jogadores Selecionados")
            st.dataframe(df_ordenado[df_ordenado['jogador'].isin(jogadores_selecionados)])
