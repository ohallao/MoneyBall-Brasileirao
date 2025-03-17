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

# Função para carregar múltiplos arquivos CSV de um repositório do GitHub
def carregar_dados_github():
    base_url = "https://github.com/ohallao/MoneyBall-Brasileirao/tree/main/Output_Cluster"
    arquivos = ["Gol_clusters_full.csv", "Mei_clusters_full.csv", "Ponta_clusters_full.csv", "vol_clusters_full.csv", "Zag_clusters_full.csv", "Lat_clusters_full.csv", "striker_clusters_full.csv"]
    
    dfs = []
    for arquivo in arquivos:
        url = base_url + arquivo
        df = pd.read_csv(url)
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)

# Carregar os dados automaticamente do GitHub
df = carregar_dados_github()

st.title("MoneyBall Brasileirao - Análise por Posição")

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

    df_com_pontuacao = calcular_pontuacao(df_filtrado, pesos_customizados)
    df_ordenado = df_com_pontuacao.sort_values(by='Pontuacao', ascending=False)
    df_ordenado['Ranking'] = range(1, len(df_ordenado) + 1)

    st.write(f"### Ranking de jogadores para posição: {posicao_escolhida}")
    st.dataframe(df_ordenado[['Ranking', 'jogador', 'time', 'Pontuacao']])

    # Histograma de pontuação
    st.header("Distribuição de Pontuação")
    fig, ax = plt.subplots()
    ax.hist(df_ordenado['Pontuacao'], bins=20, edgecolor='black')
    ax.set_xlabel("Pontuação")
    ax.set_ylabel("Quantidade de Jogadores")
    ax.set_title("Distribuição de Pontuação por Posição")
    st.pyplot(fig)

    # Comparação entre jogadores
    st.header("Comparação de Jogadores - Gráfico de Radar")
    jogadores_selecionados = st.multiselect("Selecione jogadores:", df_ordenado['jogador'].unique())
    if jogadores_selecionados:
        num_vars = len(pesos_customizados)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        for jogador in jogadores_selecionados:
            jogador_dados = df_ordenado[df_ordenado['jogador'] == jogador]
            valores = [jogador_dados[col].values[0] for col in pesos_customizados.keys()]
            valores = [(v - min(valores)) / (max(valores) - min(valores) + 1e-5) for v in valores]
            valores += valores[:1]
            ax.plot(angles, valores, label=jogador)
            ax.fill(angles, valores, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(pesos_customizados.keys(), fontsize=10, color='blue')
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
        plt.title("Comparação de Jogadores", size=15)
        st.pyplot(fig)
