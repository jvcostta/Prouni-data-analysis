# 📊 Análise Interativa de Dados do ProUni (2018-2020)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)
![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-Latest-orange.svg)
![NumPy](https://img.shields.io/badge/NumPy-Latest-lightblue.svg)

## 🎯 Objetivo do Projeto

Este projeto oferece uma **aplicação web interativa (dashboard)** para visualizar e filtrar dados sobre as bolsas do Programa Universidade para Todos (ProUni) dos anos **2018, 2019 e 2020**, permitindo a análise de tendências e padrões de forma visual e intuitiva.

## ✨ Principais Funcionalidades

- 📅 **Filtros por Ano**: Visualize dados de 2018, 2019, 2020 ou todos os anos juntos
- 🗺️ **Filtro Geográfico**: Analise por estado (UF)
- 🎓 **Tipo de Bolsa**: Compare bolsas integrais vs parciais
- � **Modalidade de Ensino**: Presencial, EAD, etc.
- 🔍 **Busca por Curso**: Encontre cursos específicos
- 📊 **Visualizações Interativas**: Gráficos dinâmicos e responsivos
- 📋 **Tabelas Detalhadas**: Explore os dados em formato tabular

## 🚀 Como Executar

### 1️⃣ Instalar Dependências

```powershell
# Criar e ativar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar pacotes
pip install -r requirements.txt
```

### 2️⃣ Processar os Dados

**Opção A - Usando script batch:**
```
Clique duas vezes em: processar_dados.bat
```

**Opção B - Via terminal:**
```powershell
python src\data_processing\clean_data.py
```

### 3️⃣ Iniciar o Dashboard

**Opção A - Usando script batch:**
```
Clique duas vezes em: iniciar_dashboard.bat
```

**Opção B - Via terminal:**
```powershell
python app.py
```

### 4️⃣ Acessar

Abra seu navegador em: **http://localhost:8050**

> 📖 Para mais detalhes, consulte [COMO_EXECUTAR.md](COMO_EXECUTAR.md)

## 📊 Fonte dos Dados

**Fonte Oficial**: [Portal de Dados Abertos do Governo Federal](https://dados.gov.br/)

### Datasets Utilizados
- ✅ **ProUni 2018**: Dados das bolsas concedidas em 2018
- ✅ **ProUni 2019**: Dados das bolsas concedidas em 2019
- ✅ **ProUni 2020**: Dados das bolsas concedidas em 2020

## 🗂️ Estrutura do Projeto

```
Prouni-data-analysis/
│
├── 📁 data/
│   ├── raw/                           # Dados originais (CSV)
│   │   ├── pda-prouni-2018.csv
│   │   ├── pda-prouni-2019.csv
│   │   └── ProuniRelatorioDadosAbertos2020.csv
│   ├── processed/                     # Dados processados
│   │   ├── prouni_2018_2020_processado.csv
│   │   └── prouni_2018_2020_processado.parquet
│   └── README.md
│
├── 📁 src/
│   └── data_processing/               # Scripts de processamento
│       ├── __init__.py
│       └── clean_data.py              # Script principal de limpeza
│
├── 📁 notebooks/                      # Jupyter notebooks para EDA
│   └── 01_exploratory_data_analysis.ipynb
│
├── 📁 assets/                         # CSS, imagens e recursos
│
├── � app.py                          # ⭐ Aplicação principal do dashboard
├── 📄 processar_dados.bat             # Script para processar dados (Windows)
├── 📄 iniciar_dashboard.bat           # Script para iniciar dashboard (Windows)
├── 📄 requirements.txt                # Dependências do projeto
├── 📄 COMO_EXECUTAR.md                # Guia detalhado de execução
├── 📄 README.md                       # Este arquivo
└── 📄 .gitignore                      # Arquivos ignorados pelo Git
```

## 🛠️ Stack Tecnológica

| Tecnologia | Propósito |
|------------|-----------|
| **Python 3.8+** | Linguagem principal |
| **Pandas** | Manipulação e análise de dados |
| **Plotly Dash** | Framework para dashboard web interativo |
| **Dash Bootstrap Components** | Componentes de UI responsivos |
| **NumPy** | Operações numéricas eficientes |
| **Matplotlib & Seaborn** | Análise exploratória (notebooks) |

## 📈 Visualizações Disponíveis

### Cards de Métricas
- Total de bolsas concedidas
- Total de bolsas integrais
- Total de bolsas parciais
- Número de instituições participantes

### Gráficos Interativos
- **Evolução Temporal**: Linha do tempo mostrando a evolução das bolsas
- **Distribuição Geográfica**: Top 15 estados com mais bolsas
- **Top Cursos**: 15 cursos mais procurados
- **Tipo de Bolsa**: Proporção entre integrais e parciais

### Tabela Detalhada
Visualização tabular com filtros aplicados, permitindo análise detalhada dos dados.

## 🤔 Perguntas Respondidas pelo Dashboard

1. **Como evoluiu o número de bolsas entre 2018 e 2020?**
2. **Quais estados concentram mais bolsas do ProUni?**
3. **Quais são os cursos mais procurados?**
4. **Qual a proporção entre bolsas integrais e parciais?**
5. **Como está a distribuição geográfica das bolsas?**
6. **Quais instituições mais participam do programa?**

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autor

**João Victor Costa Andrade** - [@jvcostta](https://github.com/jvcostta)

