
# **MoneyBall Brasil - Análise de Dados no Futebol**

Este projeto aplica conceitos de análise estatística e machine learning no contexto do futebol brasileiro, inspirado pela filosofia "MoneyBall". O objetivo é identificar eficiência e oportunidades no mercado futebolístico, encontrando clubes e jogadores que se destacam em termos de desempenho e custo-benefício.

---

## **Objetivo do Projeto**
O foco é explorar a correlação entre valor de mercado e desempenho dos clubes, além de analisar dados que possam indicar:
- Jogadores promissores e subvalorizados.
- Clubes eficientes financeiramente.
- Sugestões de contratações baseadas em dados.

---

## **Etapas do Projeto**

### **1. Coleta de Dados**
- **Fontes:** Fbref, Sofascore, Transfermarkt.
- **Competições:** Campeonato Brasileiro Serie A.(Mais Ligas Futuramente)
- **Variáveis:** Gols, assistências, passes certos, interceptações, valor de mercado, minutos jogados, entre outros.

### **2. Análise Exploratória de Dados (EDA)**
- **Limpeza e Preparação:** Tratamento de dados faltantes e remoção de outliers.
- **Visualização Inicial:** Análise de distribuições e estatísticas dos jogadores e clubes.
- **Análise por Clubes e Ligas:** Identificar quais clubes conquistam mais pontos com menor gasto e avaliar o desempenho dos jogadores por posição.

### **3. Definição de Métricas Importantes**
- **Gols Esperados (xG)** e **Assistências Esperadas (xA)**.
- **Custo por Gol/Ponto:** Avaliação da eficiência financeira.
- **Índices Defensivos:** Passes e interceptações eficazes para defensores.

### **4. Modelagem Preditiva**
- **Regressão Linear / Ridge / Lasso:** Previsão de desempenho dos jogadores.
- **Clusterização:** Aplicação de K-Means para encontrar jogadores semelhantes.
- **Classificação:** Prever classificação de times ou a performance futura dos jogadores.

### **5. Desenvolvimento de Insights**
- Identificação de **jogadores subvalorizados**.
- Análise da **eficiência financeira** dos clubes.
- **Sugestões de Transferências Futuras** com base em dados históricos e eficiência estatística.

### **6. Visualização de Dados e Interface (Streamlit)**
- **Gráficos Interativos:** Comparação de jogadores e clubes.
- **Mapa de Calor:** Contribuições dos jogadores em campo.
- **Interface Intuitiva:** Exploração de dados e insights com filtros dinâmicos.

---

## **Configuração Adicional**
Para que o projeto funcione corretamente, é necessário criar e configurar um arquivo chamado `league_dict.json` no diretório:
```
SOCCERDATA_DIR/config/league_dict.json
```
Este arquivo deve conter um mapeamento entre um nome genérico para a liga e o identificador usado por cada fonte de dados. Abaixo está um exemplo da configuração para a liga customizada do **Brasileirão Série A**:

```json
{
  "BRA-Serie A": {
    "ClubElo": "BRA_1",
    "MatchHistory": "BSA",
    "SoFIFA": "[Brazil] Serie A",
    "FBref": "Campeonato Brasileiro Série A",
    "ESPN": "bra.1",
    "FiveThirtyEight": "serie-a-brazil",
    "WhoScored": "Brazil - Serie A",
    "Sofascore": "Brasileirão Série A"
  }
}
```

Essa configuração permite que dados do Campeonato Brasileiro sejam mapeados corretamente a partir das diferentes fontes suportadas.

---

## **Ferramentas e Tecnologias Utilizadas**
- **Python:** Linguagem de desenvolvimento.
- **Pandas** e **NumPy:** Manipulação de dados.
- **Matplotlib** e **Seaborn:** Visualização de dados.
- **Scikit-learn:** Modelagem preditiva e clusterização.
- **FuzzyWuzzy:** Normalização de dados textuais.
- **Streamlit:** Interface web interativa.

---

## **Instalação e Uso**
1. Clone este repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   ```
2. Instale as dependências:
   ```bash
   pip install soccerdata pandas numpy matplotlib seaborn scikit-learn fuzzywuzzy
   ```
3. Adicione o arquivo `league_dict.json` na pasta mencionada acima.
4. Execute o notebook em Jupyter ou VSCode.
5. Explore as análises e insights gerados.

---

## **Resultados Esperados**
- **Jogadores Subvalorizados:** Identificação de atletas com bom desempenho e baixo valor de mercado.
- **Eficiência Financeira dos Clubes:** Comparação de clubes em termos de desempenho e investimento.
- **Comparação de Jogadores:** Descoberta de jogadores com performance semelhante, mas grande diferença de valor de mercado.

---

## **Contribuições**
Sinta-se à vontade para sugerir melhorias ou adicionar novas funcionalidades ao projeto.

---

## **Licença**
Este projeto é de uso livre e aberto. Siga as boas práticas de atribuição ao reutilizar partes do código ou das análises.
