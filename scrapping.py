# Termos Gerais [v. cl 5]: https://www.sports-reference.com/termsofuse.html
# Termos de Webscrapping: 
# Arquivo robots: https://www.sports-reference.com/robots.txt

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import urllib3
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Suprime aviso de segurança por não usar certificado
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

#### FUNÇÕES ####

def accessPage(url):
    response = requests.get(urlBase, verify=False)
    if response.status_code == 200:
        return response.content
    else:
        print("Erro ao acessar a página:", response.status_code)    

def htmlToDataFrame(html):
    ### Usando apenas o BeautifulSoap ###
    soup = BeautifulSoup(html, "html.parser")
    
    # Localizar a tabela de resultados
    table = soup.find("table", {"class": "stats_table"}) 
    if table:
         rows = table.find_all("tr")
         data = []
         for row in rows:
             cols = [col.text.strip() for col in row.find_all(["th", "td"])]
             data.append(cols)
        
             df = pd.DataFrame(data[1:], columns=data[0]) 
         return df
    else:
         print("Tabela não encontrada na página.")

def calc_result(jogo):
    if jogo['HomeScore'] > jogo['AwayScore']:
        return 'Home'
    elif jogo['HomeScore'] < jogo['AwayScore']:
        return 'Away'
    else
        return 'Draw'

#### /FUNÇÕES ####


# Webcrawling pode ser feito obtendo no link da temporada anterior em cada página
# Seletor CSS pra voltar uma temporada: #meta .prevnext .button2.prev

# Webscrapping usando beautiful.soap

# URL da página
urlBase = "https://fbref.com/en/comps/24/schedule/Serie-A-Scores-and-Fixtures"

# Requisição para obter o conteúdo da página
html = accessPage(urlBase)

### Usando apenas o Pandas ###
df = pd.read_html(html)[0]

### TRATAMENTO DE DADOS ###
# Substitui valores em branco por NaN
df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

# Remove linhas em branco
df.dropna(subset=['Wk'], inplace=True) # Coluna Wk (rodada) é obrigatória, em branco é uma linha inválida

# Remove colunas com todos os valores em branco
df.dropna(axis='columns', how='all', inplace=True)

# Remove colunas não aplicáveis (e.g. links no site)
df.drop(columns=['Match Report'], inplace=True)

# Coluna placar: dividir em duas colunas do tipo int
df[['HomeScore', 'AwayScore']] = df['Score'].str.split('–', expand=True)
df['HomeScore'] = df['HomeScore'].astype(int)
df['AwayScore'] = df['AwayScore'].astype(int)

# Ordenar por rodada
df.sort_values(by="Wk", inplace=True)

### TRATAMENTO BÁSICO ###
df['Wk'] = df['Wk'].astype('category') # Wk é uma categoria (dado que não é quantitativo)
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df['TotalScore'] = df['HomeScore'] + df['AwayScore']
df['categoria_encoded'] = encoder.fit_transform(df['categoria'])
df['Result'] = df.apply(calc_result, axis=1)

### ANÁLISE BÁSICA ###

# Observação estatística geral
print(df.describe())

df.info()

# # Criar gráfico com jogos por mês
# df['Month'] = df['DateTime'].dt.month_name()
# jogos_mes = df.groupby('Month')['Wk'].count()
# plt.figure(figsize=(10, 6))
# jogos_mes.plot(kind='bar', color='skyblue')
# plt.title('Número de Jogos por Mês', fontsize=16)
# plt.xlabel('Mês', fontsize=12)
# plt.ylabel('Número de Jogos', fontsize=12)
# plt.xticks(rotation=45)  # Rotacionar os nomes dos meses para melhor visualização
# plt.tight_layout()

# # Criar gráfico com média de gols por mês
# gols_mes = df.groupby('Month')['TotalScore'].mean()
# plt.figure(figsize=(10, 6))
# gols_mes.plot(kind='bar', color='skyblue')
# plt.title('Número de Gols por Mês', fontsize=16)
# plt.xlabel('Mês', fontsize=12)
# plt.ylabel('Número de Gols', fontsize=12)
# plt.xticks(rotation=45)  # Rotacionar os nomes dos meses para melhor visualização
# plt.tight_layout()
# plt.show()

# Normalizar as colunas:

# Imprimir todos os dados
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df)

# print(df)
df.to_csv('extracao.csv')