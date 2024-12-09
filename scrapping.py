# Termos Gerais [v. cl 5]: https://www.sports-reference.com/termsofuse.html
# Termos de Webscrapping: https://www.sports-reference.com/bot-traffic.html

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Webcrawling será feito clicando no link de temporada anterior em cada página
# Seletor CSS pra voltar uma temporada: #meta .prevnext .button2.prev

# Webscrapping usando beautiful.soap

# URL da página
urlBase = "https://fbref.com/en/comps/24/schedule/Serie-A-Scores-and-Fixtures"

# Requisição para obter o conteúdo da página

response = requests.get(urlBase, verify=False)
if response.status_code == 200:
    ### Usando apenas o Pandas ###
    df = pd.read_html(response.content)
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)

    ### Usando apenas o BeautifulSoap ###
    # soup = BeautifulSoup(response.content, "html.parser")
    
    # # Localizar a tabela de resultados
    # table = soup.find("table", {"class": "stats_table"}) 
    # if table:
    #      rows = table.find_all("tr")
    #      data = []
    #      for row in rows:
    #          cols = [col.text.strip() for col in row.find_all(["th", "td"])]
    #          data.append(cols)
        
    #          df = pd.DataFrame(data[1:], columns=data[0]) 
    #      print(df)
    # else:
    #      print("Tabela não encontrada na página.")
else:
    print("Erro ao acessar a página:", response.status_code)


# 
