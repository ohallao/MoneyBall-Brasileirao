import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuração das colunas e pesos por posição
colunas_por_posicao = {
    "Goleiros": [...],
    "Meias Ofensivos": [...],
    "Pontas": [...],
    "Volantes": [...],
    "Zagueiros": [...],
    "Lat": [...],
    "Atacantes": [...]
}

pesos_por_posicao = {
    "Goleiros": {...},
    "Meias Ofensivos": {...},
    "Pontas": {...},
    "Volantes": {...},
    "Zagueiros": {...},
    "Lat": {...},
    "Atacantes": {...}
}

# Função para normalizar uma métrica
def normalizar(coluna):
    return coluna / coluna.max()

# Função para calcular pontuação com base nos pesos
def calcular_pontuacao(df, pesos):
    for coluna, peso in pesos.items():
        if coluna in df.columns:
            df[coluna + '_Pontuacao'] = df[coluna] * peso

    colunas_pontuacao = [coluna + '_Pontuacao' for coluna in pesos.keys() if coluna in df.columns]
    df['Pontuacao_Total'] = df[colunas_pontuacao].sum(axis=1)
    
    # Normalizar pontuação total
    min_pontuacao = df['Pontuacao_Total'].min()
    max_pontuacao = df['Pontuacao_Total'].max()
    df['Pontuacao'] = (
        (df['Pontuacao_Total'] - min_pontuacao) / (max_pontuacao - min_pontuacao)
    ) * 100
    return df

# Função para exibir gráfico de radar
def radar_chart_por_jogadores(jogadores_selecionados, df, metrics):
    jogadores_filtrados = df[df['jogador'].isin(jogadores_selecionados)]

    if jogadores_filtrados.empty:
        st.write("Nenhum jogador encontrado nos nomes fornecidos.")
        return

    num_vars = len(metrics)

    jogadores_normalizados = jogadores_filtrados.copy()
    for metrica in metrics:
        min_val = df[metrica].min()
        max_val = df[metrica].max()
        jogadores_normalizados[metrica] = (jogadores_filtrados[metrica] - min_val) / (max_val - min_val)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for _, row in jogadores_normalizados.iterrows():
        valores = row[metrics].tolist()
        valores += valores[:1]
        ax.plot(angles, valores, label=row['jogador'])
        ax.fill(angles, valores, alpha=0.25)

    ax.set_yticks([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    plt.title("Comparação de Jogadores Selecionados", size=20, color='black', y=1.1)

    st.pyplot(fig)

# Streamlit UI
st.title("MoneyBall Brasileirao - Análise por Posição")

# Upload do CSV
st.sidebar.header("Upload do Arquivo")
uploaded_file = st.sidebar.file_uploader("Carregar arquivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Dados do Arquivo")
    st.dataframe(df, height=300)

    # Seleção de posição
    st.sidebar.header("Seleção de Posição")
    posicao_escolhida = st.sidebar.selectbox("Escolha uma posição", options=colunas_por_posicao.keys())

    if posicao_escolhida:
        colunas = colunas_por_posicao[posicao_escolhida]
        pesos = pesos_por_posicao[posicao_escolhida]

        # Verificar colunas disponíveis no DataFrame
        colunas_disponiveis = [col for col in colunas if col in df.columns]

        if not colunas_disponiveis:
            st.error(f"Nenhuma coluna válida encontrada para a posição: {posicao_escolhida}")
        else:
            # Filtrar colunas específicas da posição
            df_filtrado = df[colunas_disponiveis]

            # Calcular pontuação
            df_com_pontuacao = calcular_pontuacao(df_filtrado, pesos)

            # Ordenar e ranquear jogadores
            df_ordenado = df_com_pontuacao.sort_values(by='Pontuacao', ascending=False)
            df_ordenado['Ranking'] = range(1, len(df_ordenado) + 1)

            st.write(f"### Ranking de jogadores para posição: {posicao_escolhida}")
            st.write(df_ordenado[['Ranking', 'jogador', 'time', 'Pontuacao']])

            # Download do CSV
            csv = df_ordenado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar ranking como CSV",
                data=csv,
                file_name=f'ranking_{posicao_escolhida}.csv',
                mime='text/csv',
            )

            # Gráfico de Radar
            st.header("Comparação de Jogadores - Gráfico de Radar")

            jogadores_selecionados = st.multiselect(
                "Selecione os jogadores para comparar:", df_ordenado['jogador'].unique()
            )

            if jogadores_selecionados:
                radar_chart_por_jogadores(jogadores_selecionados, df_ordenado, list(pesos.keys()))
else:
    st.write("Por favor, carregue um arquivo CSV na barra lateral.")
