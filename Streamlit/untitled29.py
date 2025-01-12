import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuração das colunas e pesos por posição
colunas_por_posicao = {
    "Goleiros": [
            "jogador", "time", "posicao", "Minutos", "GA", "SoTA", "Saves", "Saves%", "Clean Sheet", 
            "Clean Sheet%", "PSxG", "PSxG+/-", "Passes Att", "Passes Launch%", "Passes AvgLen", 
            "Crosses Opp", "Crosses Stp", "Crosses Stp%", "Sweeper #OPA", "Sweeper #OPA/90", "Sweeper AvgDist."
        ],
        "Meias Ofensivos": [
            "jogador", "time", "posicao", "Minutos", "xG", "xAG", "G-PK", "Assistencias", "PrgC", "PrgP", 
            "Key_Pass", "Passing 1/3", "Cross", "Dribles_Tentados", "Dribles_certos"
        ],
        "Pontas": [
            "jogador", "time", "posicao", "idade", "Minutos", "G-PK", "Assist", "xG", "xAG", "xG+xAg", 
            "Prgc", "PrgP", "Cross", "Faltas Sofridas", "KeyPass", "1/3", "passPA", "crossPA", 
            "Dribles tentados", "Dribles Certos", "Corridas 1/3", "Corridas PA", "PrgR"
        ],
        "Volantes": [
            "jogador", "time", "posicao", "idade", "Minutos", "Prgc", "PrgP", "Amarelo", "Vermelho", 
            "2 Amarelo", "Falta Cometida", "interceptacao", "recuperacoes", "Duelos Aereoes W", 
            "Duelos Aereoes L", "Duelos Aereoes W%", "Divididas Total", "Divididas Ganhas", "Clearence", "Erros"
        ],
        "Zagueiros": [
            "jogador", "time", "posicao", "Minutos", "Prgc", "PrgP", "Aerial Duel%", "Aerial Duel Won", 
            "Aerial Duel Lost", "Fouls", "Yellow Card", "Red Card", "2 Yellow Card", "Desarmes Certos", 
            "Desarmes Totais", "Desarmes%", "Interceptacao", "Erros"
        ],
        "Laterais": [
            "jogador", "time", "posicao", "idade", "Minutos", "Prgc", "PrgP", "xAG", "Aerial Duel%", 
            "Aerial Duel Won", "Aerial Duel Lost", "Fouls", "Yellow Card", "Red Card", "2 Yellow Card", "Cross", 
            "Desarmes Certos", "Desarmes Totais", "Desarmes%", "Interceptacao", "Erros"
        ],
        "Atacantes": [
            "jogador", "time", "posicao", "Minutos", "PrgR", "xG", "xAG", "G-PK", "Assistencias", 
            "Acoes Ofensivas", "Aerial Duel%"
        ]
    }

pesos_por_posicao = {
    "Goleiros": {
            'GA': -5,
            'Saves': 2,
            'Clean Sheet': 10,
            'PSxG': 5,
            'Passes Launch%': 3,
            'Crosses Stp%': 5,
            'Sweeper #OPA': 5
        },
        "Meias Ofensivos": {
            'xG': 1.1,
            'xAG': 1.85,
            'G-PK': 1.80,
            'Assistencias': 2,
            'Acoes Ofensivas': 1.2,
            'Key_Pass': 1.5,
            'Passing 1/3': 1.1,
            'Cross': 1.0,
            '%Dribles': 1.25
        },
        "Pontas": {
            'xG+xAg': 10,
            'KeyPass': 5,
            'Cross': 8,
            '1/3': 2,
            'Dribles Certos': 5,
            'Corridas 1/3': 2,
            'Corridas PA': 7,
            'passPA': 8,
            'crossPA': 8
        },
        "Volantes": {
            'Amarelo': -5,
            'Vermelho': -10,
            'Falta Cometida': -2,
            'interceptacao': 2,
            'recuperacoes': 2,
            'Duelos Aereoes W': 4,
            'Divididas Ganhas': 6,
            'Clearence': 5,
            'Erros': -1
        },
        "Zagueiros": {
            'Prgc': 2,
            'PrgP': 2,
            'Aerial Duel Won': 10,
            'Fouls': -3,
            'Yellow Card': -5,
            'Red Card': -10,
            'Desarmes Certos': 10,
            'Interceptacao': 5,
            'Erros': -2
        },
        "Laterais": {
            'Prgc': 2,
            'PrgP': 2,
            'xAG': 10,
            'Fouls': -3,
            'Yellow Card': -5,
            'Red Card': -10,
            'Cross': 10,
            'Desarmes Certos': 10,
            'Interceptacao': 5,
            'Erros': -2
        },
        "Atacantes": {
            'PrgR': 4,
            'xG': 5,
            'xAG': 4,
            'G-PK': 10.0,
            'Assistencias': 3,
            'Acoes Ofensivas': 2,
            'Aerial Duel%': 2
        }
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
            st.write(df_ordenado[['Ranking', 'jogador', 'time', 'Perfil', 'Pontuacao']])

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

                # Exibir tabela com dados dos jogadores selecionados
                st.write("### Estatísticas dos Jogadores Selecionados")
                tabela_metricas = df_ordenado[df_ordenado['jogador'].isin(jogadores_selecionados)][colunas_disponiveis]
                st.dataframe(tabela_metricas)
else:
    st.write("Por favor, carregue um arquivo CSV na barra lateral.")

