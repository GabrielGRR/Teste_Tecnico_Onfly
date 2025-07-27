import pandas as pd
import matplotlib.pyplot as plt
import requests
import logging
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# NOTE: Usar Docker
# NOTE: Garantir que usei todas as bibliotecas
# NOTE: Limpar prints no final do código

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
Tipos: Lista de types do Pokémon (ex.: ["Eletric", "Flying"]).
HP: Valor da estatística "HP".
Ataque: Valor da estatística "Attack".
Defesa: Valor da estatística "Defense".'''

def get_pokemon_data(pokemon_url):
    try:
        response = requests.get(pokemon_url)
        pokemon_data = response.json()

        id = pokemon_data.get('id')
        name = pokemon_data.get('name').capitalize()
        xp = pokemon_data.get('base_experience')

        types = []
        for pokemon_type in pokemon_data['types']:
            types.append(pokemon_type['type']['name'])

        hp = None
        attack = None
        defense = None
        for pokemon_stat in pokemon_data['stats']:
            if pokemon_stat['stat']['name'] == 'hp':
                hp = pokemon_stat['base_stat']

            elif pokemon_stat['stat']['name'] == 'attack':
                attack = pokemon_stat['base_stat']

            elif pokemon_stat['stat']['name'] == 'defense':
                defense = pokemon_stat['base_stat']

        return [id,name,xp,types,hp,attack,defense]
    
    except requests.RequestException as e:
        print(f"Erro na requisição {pokemon_url}: {e}")
        return None

if __name__ == "__main__":
    start_time = time.perf_counter()

    ## Tarefa 1
    # Chamada de API
    url = "https://pokeapi.co/api/v2/pokemon?limit=100&offset=0"
    response = requests.get(url,timeout=15)
    pokemon_data = response.json()
    pokemons = pokemon_data['results']
    urls = [pokemon['url'] for pokemon in pokemons]

    pokemon_data = []
    operations = []
    # Paralelismo de requisições (Threading)
    with ThreadPoolExecutor(max_workers=5) as executor:
        for url in urls:
            operation = executor.submit(get_pokemon_data, url)
            operations.append(operation)

        for i, operation in enumerate(as_completed(operations), 1):
            result = operation.result()
            if result:
                pokemon_data.append(result)
                print(f"{i} - {result[1]}")

    # Construção do DataFrame
    df = pd.DataFrame(pokemon_data, columns=['ID','Nome','Experiência Base','Tipos', 'HP', 'Ataque', 'Defesa']).sort_values(by="ID")

    ## Tarefa 2
    # ADD coluna categoria
    df['Categoria'] = df['Experiência Base'].apply(lambda x: 'Fraco' if x < 50 else ('Médio' if x <= 100 else 'Forte'))
    print(df)

    # Criar DF com contagem dos tipos de pokemon
    tipo_dict = {}
    for tipos in df['Tipos']:
        for tipo in tipos:
            tipo_dict[tipo] = tipo_dict.get(tipo, 0) + 1

    print(tipo_dict)

    df_type_count = (pd.DataFrame.from_dict(tipo_dict, orient='index', columns=['Quantidade'])
                     .reset_index()
                     .rename(columns={'index': 'Tipo'})
                     .sort_values(by='Quantidade', ascending=False))
    print(df_type_count)

    # Gerar gráfico MatplotLib
    plt.figure(figsize=(12, 8))
    plt.bar(df_type_count['Tipo'], df_type_count['Quantidade'], color='skyblue', edgecolor='navy', alpha=0.7)
    plt.title('Distribuição de Pokémon por Tipo', fontsize=16, fontweight='bold')
    plt.xlabel('Tipo de Pokémon', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Salvar o gráfico como imagem
    plt.savefig('distribuicao_tipos_pokemon.png', dpi=300, bbox_inches='tight')




    elapsed = time.perf_counter() - start_time
    print(f"Tempo total: {elapsed:.2f} segundos")


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