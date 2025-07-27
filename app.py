import pandas as pd
import matplotlib
import requests
import logging

# NOTE: Usar Docker
# NOTE: Garantir que usei todas as bibliotecas

'''
Tarefa 1: Extração de Dados
1. Consumo de Dados:

Acesse a PokeAPI na rota /pokemon?limit=100&offset=0 para obter uma lista de 100 Pokémon.
Para cada Pokémon, obtenha detalhes adicionais consultando a rota /pokemon/{id}.

2. Estruturação com pandas:
Construa um DataFrame com as seguintes colunas:

ID: Identificador único do Pokémon.
Nome: Nome do Pokémon (normalizado para título, ex.: "PIKACHU" → "Pikachu").
Experiência Base: Valor do campo base_experience.
Tipos: Lista de tipos do Pokémon (ex.: ["Eletric", "Flying"]).
HP: Valor da estatística "HP".
Ataque: Valor da estatística "Attack".
Defesa: Valor da estatística "Defense".'''

url = "https://pokeapi.co/api/v2/pokemon?limit=100&offset=0"

response = requests.get(url)
response_data = response.json()
teste_pokemon = response_data['results'][5]

print(teste_pokemon)

response = requests.get(teste_pokemon['url'])
response_data = response.json()
print(response_data['id'])
print(response_data['name'].capitalize())
print(response_data['base_experience'])

for pokemon_type in response_data['types']:
    print(pokemon_type['type']['name'])

hp = 0
for pokemon_stat in response_data['stats']:
    if pokemon_stat['stat']['name'] == 'hp':
        hp = pokemon_stat['base_stat']

print(hp)

attack = 0
for pokemon_stat in response_data['stats']:
    if pokemon_stat['stat']['name'] == 'attack':
        attack = pokemon_stat['base_stat']
print(attack)
defense = 0

for pokemon_stat in response_data['stats']:
    if pokemon_stat['stat']['name'] == 'defense':
        defense = pokemon_stat['base_stat']
print(defense)




'''
Tarefa 2: Transformação de Dados
1. Categorização:
Adicione uma coluna chamada Categoria que classifique os Pokémon em:
"Fraco": Experiência base < 50.
"Médio": Experiência base entre 50 e 100.
"Forte": Experiência base > 100.

2. Transformações de Tipos:
Crie um novo DataFrame que contenha a contagem de Pokémon por tipo.
Gere um gráfico de barras com matplotlib ou seaborn mostrando a distribuição de Pokémon por tipo.

3. Análise Estatística:
Calcule e exiba:
A média de ataque, defesa e HP por tipo de Pokémon.
Os 5 Pokémon com maior experiência base.'''

'''
Tarefa 3: Relatório e Exportação

1. Relatório com pandas:
Gere um relatório consolidado contendo os seguintes elementos:
Tabela dos 5 Pokémon com maior experiência base.
Tabela com a média de ataque, defesa e HP por tipo.
Gráfico de distribuição de Pokémon por tipo.

2. Exportação:
Salve o relatório em formato CSV e o gráfico gerado como uma imagem (.png).'''


'''
Tarefa 4: Pipeline Automatizado
1. Automatize o Processo:
Crie um script Python modular que execute as tarefas acima em sequência:
Extração dos dados.
Transformação e categorização.
Geração e exportação do relatório.

2. Logs e Erros:
Implemente logs utilizando a biblioteca logging para acompanhar o progresso do pipeline.
Garanta o tratamento adequado de erros, como falhas na API ou dados faltantes.'''