# Análise de Pokémon - Teste Técnico OnFly

Este projeto é uma aplicação Python que realiza um ETL, extraindo, tratando e carregando dados dos primeiros 100 Pokémon da [PokéAPI](https://pokeapi.co/), desenvolvido como teste técnico para a vaga de **Desenvolvedor RPA** na OnFly.

## 📋 Sobre o Projeto

A aplicação realiza:
- **Extração de dados** dos primeiros 100 Pokémon via API
- **Tratamento** dos dados coletados
- **Geração de outputs** visuais (gráficos) e tabulares (CSV)
- **Processamento concorrente** para otimizar performance
- **Containerização** com Docker para portabilidade

### 📈 Outputs Gerados
- `top_5_pokemon_maior_experiencia.csv` - Ranking dos 5 Pokémon com maior XP
- `medias_stats_por_tipo.csv` - Estatísticas médias agrupadas por tipo
- `distribuicao_tipos_pokemon.png` - Gráfico de barras da distribuição
- `pokemon_analysis.log` - Log completo da execução

## 🛠️ Tecnologias Utilizadas

- **Python 3.11** - Linguagem principal
- **Pandas** - Manipulação e análise de dados
- **Matplotlib** - Geração de gráficos
- **Requests** - Requisições HTTP à API
- **Docker** - Containerização
- **ThreadPoolExecutor** - Processamento concorrente

## ⚡ Como Executar

### 🐳 Opção 1: Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/GabrielGRR/Teste_Tecnico_Onfly.git
cd teste_tecnico_onfly

# Execute com Docker
docker-compose build
docker-compose up
```

### 🐍 Opção 2: Python Local

```bash
# Instale as dependências
pip install -r requirements.txt

# Execute o script
python app.py
```

## 📁 Estrutura do Projeto

```
teste_tecnico_onfly/
├── app.py                      # Código principal
├── requirements.txt            # Dependências Python
├── Dockerfile                  # Configuração Docker
├── docker-compose.yml          # Orquestração Docker
├── output/                     # Arquivos gerados
│   ├── top_5_pokemon_maior_experiencia.csv
│   ├── medias_stats_por_tipo.csv
│   ├── distribuicao_tipos_pokemon.png
│   └── pokemon_analysis.log
└── README.md                   # Este arquivo
```

## 👨‍💻 Autor

**Gabriel Guimarães** - Desenvolvedor RPA / Engenheiro de dados  
Teste técnico para vaga de Desenvolvedor RPA - OnFly

---