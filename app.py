import pandas as pd
import matplotlib.pyplot as plt
import requests
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# NOTE: Usar Docker
# NOTE: Usar logging
# NOTE: Garantir que usei todas as bibliotecas
# NOTE: Limpar prints no final do código

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

def extrair_pokemons():
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

    return pokemon_data

def construir_dataframe(pokemon_data):
    # Construção do DataFrame
    df = pd.DataFrame(pokemon_data, columns=['ID','Nome','Experiência Base','Tipos', 'HP', 'Ataque', 'Defesa']).sort_values(by="ID")

    ## Tarefa 2
    # ADD coluna categoria ao DF
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
    return df, df_type_count

def gerar_grafico(dataframe_tipo_pokemon):
    plt.figure(figsize=(12, 8))
    plt.bar(dataframe_tipo_pokemon['Tipo'], dataframe_tipo_pokemon['Quantidade'], color='skyblue', edgecolor='navy', alpha=0.7)
    plt.title('Distribuição de Pokémon por Tipo', fontsize=16, fontweight='bold')
    plt.xlabel('Tipo de Pokémon', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    plt.savefig('distribuicao_tipos_pokemon.png', dpi=300, bbox_inches='tight')

def gerar_relatorios(dataframe):

    # Os 5 Pokémon com maior experiência base
    top_5_xp = dataframe.nlargest(5, 'Experiência Base')[['Nome', 'Experiência Base', 'Tipos', 'HP', 'Ataque', 'Defesa']]
    top_5_xp.to_csv('top_5_pokemon_maior_experiencia.csv', index=False, encoding='utf-8')

    print("1. Top 5 Pokémon com maior Experiência Base:")
    print(top_5_xp.to_string(index=False),end="\n\n")

    # Média de HP, Ataque e Defesa por Tipo de Pokémon
    df_exploded = dataframe.explode('Tipos')

    stats_por_tipo = df_exploded.groupby('Tipos').agg({
        'HP': 'mean',
        'Ataque': 'mean',
        'Defesa': 'mean'
    }).round(2).sort_values(by='Tipos', ascending=True)
    stats_por_tipo.to_csv('medias_stats_por_tipo.csv', encoding='utf-8')

    print("2. Média de HP, Ataque e Defesa por Tipo de Pokémon:")
    print(stats_por_tipo)

if __name__ == "__main__":
    # start_time = time.perf_counter()
    # elapsed = time.perf_counter() - start_time
    # print(f"Tempo total: {elapsed:.2f} segundos")

    pokemons = extrair_pokemons()
    dataframe_completo, dataframe_tipos_pokemon = construir_dataframe(pokemons)
    gerar_grafico(dataframe_tipos_pokemon)
    gerar_relatorios(dataframe_completo)
    