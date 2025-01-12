import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para normalizar uma métrica com base no valor máximo
def normalizar(coluna):
    return coluna / coluna.max()

# Função para gerar gráfico de radar
def radar_chart_por_jogadores(jogadores_selecionados, df, metrics):
    jogadores_filtrados = df[df['jogador'].isin(jogadores_selecionados)]

    if jogadores_filtrados.empty:
        st.write("Nenhum jogador encontrado nos nomes fornecidos.")
        return

    # Ângulos para o gráfico radar
    num_vars = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Fechar o círculo

    # Criar o gráfico
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for _, row in jogadores_filtrados.iterrows():
        valores = row[metrics].tolist()
        valores += valores[:1]  # Fechar o círculo
        ax.plot(angles, valores, label=row['jogador'])
        ax.fill(angles, valores, alpha=0.25)

    ax.set_yticks([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    plt.title("Comparação de Jogadores Selecionados", size=20, color='black', y=1.1)

    st.pyplot(fig)

# Configuração inicial do Streamlit
st.title("MoneyBall Brasileirao")

# Configuração da posição no menu lateral
st.sidebar.header("Configuração da Posição")
posicao_escolhida = st.sidebar.selectbox(
    "Selecione a posição:", 
    ["Goleiros", "Meias Ofensivos", "Pontas", "Volantes", "Zagueiros", "Laterais", "Atacantes"]
)

# Upload do arquivo CSV
st.sidebar.header("Upload do Arquivo")
uploaded_file = st.sidebar.file_uploader(f"Carregar arquivo CSV para {posicao_escolhida}", type=["csv"])

if uploaded_file is not None:
    # Leitura do arquivo CSV
    df = pd.read_csv(uploaded_file)

    st.write(f"### Dados do Arquivo ({posicao_escolhida})")
    st.dataframe(df, height=300)  # Tornar a tabela rolável

    # Configuração de métricas específicas por posição
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
            'Erros': 1
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

    if posicao_escolhida in pesos_por_posicao:
        pesos = pesos_por_posicao[posicao_escolhida]
        pontuacoes = []

        # Calcula a pontuação total para cada jogador
        for _, row in df.iterrows():
            pontuacao = 0
            for metrica, peso in pesos.items():
                if metrica in df.columns:
                    pontuacao += row[metrica] * peso
            pontuacoes.append(pontuacao)

        df["Pontuacao_Total"] = pontuacoes
        ranking = df.sort_values(by="Pontuacao_Total", ascending=False)

        # Exibir ranking
        st.write(f"### Ranking de Jogadores ({posicao_escolhida})")
        st.write(ranking[colunas_por_posicao[posicao_escolhida] + ["Pontuacao_Total"]])

        # Opção para baixar o ranking como CSV
        csv_ranking = ranking[colunas_por_posicao[posicao_escolhida] + ["Pontuacao_Total"]].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Baixar Ranking como CSV",
            data=csv_ranking,
            file_name=f"ranking_{posicao_escolhida}.csv",
            mime="text/csv",
        )

        # Gráfico de Radar
        st.header("Comparação de Jogadores - Gráfico de Radar")
        jogadores_selecionados = st.multiselect(
            "Selecione os jogadores para comparar:", df["jogador"].unique()
        )
        if jogadores_selecionados:
            radar_chart_por_jogadores(jogadores_selecionados, df, list(pesos.keys()))
    else:
        st.write("Não há métricas definidas para esta posição.")
