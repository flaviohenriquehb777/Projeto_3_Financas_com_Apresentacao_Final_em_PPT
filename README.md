# Análise Financeira com Apresentação Executiva (Sam's Club - Walmart)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Projeto de consultoria financeira para o Sam's Club - Walmart, com o objetivo de gerar insights a partir de dados de vendas e apresentá-los de forma executiva.**

## Sumário
- [Visão Geral do Projeto](#visão-geral-do-projeto)
- [Objetivos da Análise](#objetivos-da-análise)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Base de Dados](#base-de-dados)
- [Metodologia de Análise](#metodologia-de-análise)
- [Resultados Chave e Apresentação](#resultados-chave-e-apresentação)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Uso](#instalação-e-uso)
- [Licença](#licença)
- [Contato](#contato)

## Visão Geral do Projeto:

Este projeto consiste em uma consultoria financeira abrangente para o Sam's Club - Walmart, com foco na análise de dados de vendas para responder a questões de negócio cruciais. A análise detalhada é realizada em um notebook Jupyter, e os principais insights são consolidados em uma apresentação executiva formatada para decisão.

## Objetivos da Análise:

A análise financeira foi guiada pelas seguintes perguntas chave, visando fornecer informações acionáveis para a gestão:

1.  **Como foi o desempenho de vendas da empresa no período analisado?**
2.  **Qual foi a categoria de produtos mais vendida?**
3.  **Qual foi o item (produto específico) mais vendido?**

## Estrutura do Projeto:

Este repositório está organizado para facilitar a compreensão e replicação do projeto:

-   `dados/`:
    -   `criando_uma_apresentacao_executiva.csv`: A base de dados bruta utilizada para a análise.
-   `notebooks/`:
    -   `Calculos_Financeiros_Empresa.ipynb`: O notebook Jupyter que contém toda a análise de dados, desde a importação e tratamento até a geração dos gráficos e cálculos para os insights.
-   `ppt/`:
    -   `Apresentacao_Executiva.pptx`: A apresentação em PowerPoint com os resultados e insights consolidados para uma audiência executiva.
-   `README.md`: Este arquivo, fornecendo uma visão geral do projeto.
-   `LICENSE.md`: Arquivo contendo os termos da licença do projeto (MIT).
-   `requirements.txt`: Lista das bibliotecas Python e suas versões necessárias para executar o notebook.

## Base de Dados:

O projeto utiliza o arquivo `criando_uma_apresentacao_executiva.csv`, localizado na pasta `dados/`. Este dataset contém informações detalhadas sobre as vendas, incluindo datas, valores, categorias e nomes de produtos, permitindo uma análise aprofundada do desempenho financeiro.

## Metodologia de Análise:

A análise foi conduzida de forma meticulosa, seguindo os seguintes passos no notebook `Calculos_Financeiros_Empresa.ipynb`:

1.  **Configuração do Ambiente:** Importação das bibliotecas necessárias e configuração inicial.
2.  **Importação e Visualização da Base:** Carregamento do dataset e uma primeira inspeção dos dados.
3.  **Pré-processamento de Dados:**
    * Filtragem de registros irrelevantes.
    * Agrupamento de dados para sumarização de vendas por categoria, produto, mês e ano.
    * Transformação de tipos de dados para garantir a consistência e permitir operações analíticas.
4.  **Cálculos e Transformações:** Realização de cálculos financeiros para derivar métricas de desempenho.
5.  **Visualização de Dados:** Geração de gráficos (com bibliotecas como Matplotlib e Seaborn) para ilustrar tendências de vendas, desempenho de categorias e identificar os produtos mais vendidos.
6.  **Extração de Insights:** Identificação das respostas para as perguntas chave do projeto, baseadas nas análises e visualizações.

## Resultados Chave e Apresentação:

Os resultados detalhados podem ser encontrados no notebook, mas os principais insights foram sintetizados na `Apresentacao_Executiva.pptx`, disponível na pasta `ppt/`. Esta apresentação visa comunicar de forma clara e concisa o desempenho de vendas, as categorias e produtos de maior destaque, e outras observações relevantes para a tomada de decisões estratégicas.

## Tecnologias Utilizadas:

-   Python
-   Pandas (para manipulação e análise de dados)
-   Numpy (para operações numéricas)
-   Matplotlib (para visualização de dados)
-   Seaborn (para visualizações estatísticas)
-   Jupyter Notebook / Jupyter Lab
-   Microsoft PowerPoint (para a apresentação executiva)

## Instalação e Uso:

Para replicar a análise e visualizar a apresentação, siga os passos abaixo:

1.  **Pré-requisitos:**
    * Python 3.8+
    * `pip` (gerenciador de pacotes do Python)
    * Jupyter Lab ou Jupyter Notebook
    * Um visualizador de arquivos `.pptx` (como Microsoft PowerPoint, Google Slides, LibreOffice Impress).

2.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/Projeto_3_Financas_com_Apresentacao_Final_em_PPT.git](https://github.com/seu-usuario/Projeto_3_Financas_com_Apresentacao_Final_em_PPT.git)
    cd Projeto_3_Financas_com_Apresentacao_Final_em_PPT
    ```
    *(Lembre-se de substituir `seu-usuario` pelo seu nome de usuário do GitHub.)*

3.  **Crie o arquivo `requirements.txt`:**
    * Dentro do terminal do Jupyter Lab (ou em um terminal Git Bash na raiz do projeto), execute:
        ```bash
        pip freeze > requirements.txt
        ```
    *(**Importante:** Faça isso *depois* de ter todas as bibliotecas necessárias instaladas no seu ambiente Python.)*

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Acesse o Projeto:**
    * Inicie o Jupyter Lab na raiz do projeto:
        ```bash
        jupyter lab
        ```
    * Abra o notebook `notebooks/Calculos_Financeiros_Empresa.ipynb` para executar a análise de dados.
    * Abra o arquivo `ppt/Apresentacao_Executiva.pptx` para revisar a apresentação executiva.

## Licença:

Este projeto está licenciado sob a Licença MIT. Para mais detalhes, consulte o arquivo [LICENSE.md](LICENSE.md) na raiz do repositório.

## Contato:

Se tiver alguma dúvida, sugestão ou quiser colaborar, sinta-se à vontade para entrar em contato:
-   **Nome:** Flávio Henrique Barbosa
-   **LinkedIn:** [Flávio Henrique Barbosa | LinkedIn](https://www.linkedin.com/in/fl%C3%A1vio-henrique-barbosa-38465938)
-   **Email:** flaviohenriquehb777@outlook.com