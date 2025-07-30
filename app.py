import pandas as pd
import matplotlib.pyplot as plt
import requests
import logging
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# NOTE: Embelezar markdown jupyter notebook
print('teste')
def _setup_logging():
    os.makedirs('output', exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('output/pokemon_analysis.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def _make_api_request(url, timeout=15):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Levanta exceção para status HTTP de erro
        return response.json()
    except requests.exceptions.Timeout:
        logger.error(f"Timeout na requisição para {url}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Erro de conexão para {url}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erro HTTP {e.response.status_code} para {url}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição para {url}: {e}")
        return None
    except ValueError as e:
        logger.error(f"Erro ao decodificar JSON de {url}: {e}")
        return None

def get_pokemon_data(pokemon_url):
    pokemon_data = _make_api_request(pokemon_url)

    if not pokemon_data:
        return None

    try:
        id = pokemon_data.get('id')
        name = pokemon_data.get('name', '').capitalize()
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

        return [id, name, xp, types, hp, attack, defense]
    
    except (KeyError, TypeError) as e:
        logger.error(f"Erro ao processar dados do Pokémon de {pokemon_url}: {e}")
        return None

def extract_pokemons():
    logger.info("Iniciando extração de dados dos primeiros 100 Pokémon da PokéAPI")
    
    url = "https://pokeapi.co/api/v2/pokemon?limit=100&offset=0"
    pokemon_data = _make_api_request(url)
    
    if not pokemon_data:
        logger.error("Falha ao obter lista inicial de Pokémon")
        return []
    
    pokemons = pokemon_data.get('results', [])
    urls = [pokemon.get('url') for pokemon in pokemons if pokemon.get('url')]
    
    if not urls:
        logger.error("Nenhuma URL de Pokémon encontrada")
        return []

    pokemon_list = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(get_pokemon_data, url): url for url in urls}

        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            if result:
                pokemon_list.append(result)

            if i % 25 == 0:
                logger.info(f"{i}/100 Pokémons processados com sucesso")

    return pokemon_list

def build_dataframe(pokemon_list):
    logger.info("Construindo DataFrame e analisando dados dos Pokémon")
    
    df = pd.DataFrame(pokemon_list, columns=['ID','Nome','Experiência Base','Tipos', 'HP', 'Ataque', 'Defesa']).sort_values(by="ID")
    
    df['Categoria'] = df['Experiência Base'].apply(lambda x: 'Fraco' if x < 50 else ('Médio' if x <= 100 else 'Forte'))
    
    dict_type = {}
    for types in df['Tipos']:
        for type in types:
            dict_type[type] = dict_type.get(type, 0) + 1

    df_type_count = (pd.DataFrame.from_dict(dict_type, orient='index', columns=['Quantidade'])
                        .reset_index()
                        .rename(columns={'index': 'Tipo'})
                        .sort_values(by='Quantidade', ascending=False))

    return df, df_type_count

def generate_graphs(dataframe_tipo_pokemon):
    logger.info("Gerando gráfico de distribuição de Pokémon por tipo")
    
    plt.figure(figsize=(12, 8))
    plt.bar(dataframe_tipo_pokemon['Tipo'], dataframe_tipo_pokemon['Quantidade'], color='skyblue', edgecolor='navy', alpha=0.7)
    plt.title('Distribuição de Pokémon por Tipo', fontsize=16, fontweight='bold')
    plt.xlabel('Tipo de Pokémon', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('output/distribuicao_tipos_pokemon.png', dpi=300, bbox_inches='tight')
    
    logger.info("Gráfico salvo como 'output/distribuicao_tipos_pokemon.png'")
    # plt.show()

def generate_reports(dataframe):
    logger.info("Gerando relatórios de análise dos Pokémon")
    
    top_5_xp = dataframe.nlargest(5, 'Experiência Base')[['Nome', 'Experiência Base', 'Tipos', 'HP', 'Ataque', 'Defesa']]
    top_5_xp.to_csv('output/top_5_pokemon_maior_experiencia.csv', index=False, encoding='utf-8')
    logger.info("Relatório 'Top 5 Pokémon' salvo como 'output/top_5_pokemon_maior_experiencia.csv'")

    df_exploded = dataframe.explode('Tipos')
    stats_por_tipo = df_exploded.groupby('Tipos').agg({
        'HP': 'mean',
        'Ataque': 'mean',
        'Defesa': 'mean'
    }).round(2).sort_values(by='Tipos', ascending=True)
    stats_por_tipo.to_csv('output/medias_stats_por_tipo.csv', encoding='utf-8')
    logger.info("Relatório 'Médias por Tipo' salvo como 'output/medias_stats_por_tipo.csv'")

if __name__ == "__main__":
    start_time = time.perf_counter()
    logger = _setup_logging()
    logger.info("=== INICIANDO ANÁLISE DE POKÉMON ===")

    pokemons = extract_pokemons()
    
    elapsed = time.perf_counter() - start_time
    logger.info(f"Extração concluída em {elapsed:.2f} segundos")

    dataframe_completo, dataframe_tipos_pokemon = build_dataframe(pokemons)
    generate_graphs(dataframe_tipos_pokemon)
    generate_reports(dataframe_completo)
    
    total_time = time.perf_counter() - start_time
    logger.info(f"=== ANÁLISE CONCLUÍDA EM {total_time:.2f} SEGUNDOS ===")