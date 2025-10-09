# 📊 Análise Interativa de Dados do ProUni (2023-2025)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)
![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-Latest-orange.svg)
![NumPy](https://img.shields.io/badge/NumPy-Latest-lightblue.svg)

## 🎯 Objetivo do Projeto

Este projeto tem como objetivo construir uma **aplicação web interativa (dashboard)** para visualizar e filtrar dados sobre as bolsas do Programa Universidade para Todos (ProUni), permitindo a análise de tendências e padrões ao longo do período de 2023 a 2025.

## 🚀 Stack Tecnológica

| Tecnologia | Propósito | Justificativa |
|------------|-----------|---------------|
| **Python** | Linguagem principal | Ecosistema robusto para análise de dados |
| **Pandas** | Análise e manipulação de dados | Padrão da indústria para manipulação de dados |
| **Plotly Dash** | Dashboard interativo e visualizações | Permite criar aplicações web usando apenas Python |
| **NumPy** | Cálculos numéricos | Suporte eficiente para operações matemáticas |

### Por que essa stack?

- **Simplicidade**: Desenvolvimento 100% em Python, sem necessidade de HTML, CSS ou JavaScript
- **Eficiência**: Pandas é otimizado para grandes volumes de dados
- **Interatividade**: Plotly Dash oferece componentes interativos nativos
- **Produtividade**: Foco na análise de dados, não na infraestrutura web

## 📋 Funcionalidades Planejadas

### Filtros Interativos
- 📅 **Seleção por Ano**: Análise temporal (2023-2025)
- 🗺️ **Filtro por Estado (UF)**: Visualização regional
- 🎓 **Tipo de Bolsa**: Integral vs. Parcial
- 🔍 **Busca por Curso**: Localização de cursos específicos
- 🏫 **Busca por Instituição**: Análise por IES

### Visualizações
- 📊 Gráficos de barras interativos
- 📈 Análises de tendências temporais
- 🗺️ Mapas de distribuição geográfica
- 📋 Tabelas dinâmicas com dados detalhados

## 🛠️ Configuração do Ambiente

### Pré-requisitos
- Python 3.8 ou superior
- Git

### Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/jvcostta/Prouni-data-analysis.git
   cd Prouni-data-analysis
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   # Windows (PowerShell)
   py -m venv venv
   venv\Scripts\Activate.ps1
   
   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

### Dependências Principais
```txt
pandas>=1.5.0
dash>=2.14.0
plotly>=5.15.0
numpy>=1.24.0
dash-bootstrap-components>=1.4.0
```

## 📊 Fonte dos Dados

**Fonte Oficial**: [Portal de Dados Abertos do Governo Federal](https://dados.gov.br/)

### Datasets Utilizados
- **ProUni 2023**: Dados das bolsas concedidas em 2023
- **ProUni 2024**: Dados das bolsas concedidas em 2024  
- **ProUni 2025**: Dados das bolsas concedidas em 2025 (quando disponível)

**Formato**: CSV (Comma Separated Values)

## 🗂️ Estrutura do Projeto

```
Prouni-data-analysis/
│
├── 📁 data/
│   ├── raw/                    # Dados originais (CSV)
│   ├── processed/              # Dados limpos e processados
│   └── README.md              # Documentação dos dados
│
├── 📁 src/
│   ├── data_processing/        # Scripts de limpeza de dados
│   ├── analysis/              # Análises exploratórias
│   ├── dashboard/             # Código do dashboard Dash
│   └── utils/                 # Funções auxiliares
│
├── 📁 notebooks/              # Jupyter notebooks para EDA
├── 📁 assets/                 # CSS, imagens e outros recursos
├── 📁 tests/                  # Testes unitários
│
├── .gitignore
├── requirements.txt
├── README.md
└── app.py                     # Aplicação principal do dashboard
```

## 🏗️ Plano de Execução

### ✅ Fase 0: Preparação e Configuração do Ambiente
- [x] Instalação do Python
- [x] Criação do ambiente virtual
- [x] Instalação das bibliotecas necessárias
- [x] Configuração do Git e .gitignore

### 📍 Fase 1: Coleta e Exploração Inicial dos Dados
- [ ] Localização e download dos datasets do ProUni
- [ ] Carregamento dos dados com Pandas
- [ ] Análise exploratória inicial (EDA)
- [ ] Identificação da estrutura dos dados

### 🧹 Fase 2: Limpeza e Pré-processamento dos Dados
- [ ] Tratamento de dados faltantes
- [ ] Correção de tipos de dados
- [ ] Padronização de dados textuais
- [ ] Feature engineering
- [ ] Unificação dos datasets de diferentes anos

### 🔍 Fase 3: Análise Aprofundada e Geração de Insights
- [ ] Definição das perguntas de negócio
- [ ] Agregação e análise dos dados
- [ ] Criação de visualizações estáticas
- [ ] Documentação dos insights encontrados

### 🎨 Fase 4: Desenvolvimento do Dashboard Interativo
- [ ] Estruturação do layout da aplicação
- [ ] Implementação dos componentes interativos
- [ ] Desenvolvimento dos callbacks do Dash
- [ ] Criação dos gráficos interativos
- [ ] Testes e refinamentos

## 🤔 Perguntas de Pesquisa

### Principais questões que o dashboard deve responder:

1. **Evolução Temporal**: Como o número de bolsas evoluiu entre 2023-2025?
2. **Distribuição Geográfica**: Quais estados/regiões concentram mais bolsas?
3. **Análise por Curso**: Quais cursos têm maior demanda por bolsas?
4. **Tipo de Bolsa**: Qual a proporção entre bolsas integrais e parciais?
5. **Instituições**: Quais IES mais participam do programa?

### Exemplos de análises específicas:
- "Evolução do número de bolsas para Engenharia de Software no DF (2023-2025)"
- "Comparação entre bolsas integrais vs. parciais por região"
- "Top 10 cursos com mais bolsas em 2024"

## 🚀 Como Executar

### Desenvolvimento
```bash
# Ativar ambiente virtual
venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate   # Linux/macOS

# Executar o dashboard
python app.py
```

### Acesso
Abra seu navegador e acesse: `http://localhost:8050`

## 🧪 Testes

```bash
# Executar todos os testes
python -m pytest tests/

# Executar testes com cobertura
python -m pytest tests/ --cov=src/
```

## 📈 Roadmap Futuro

- [ ] **Fase 5**: Deploy da aplicação (Heroku/Streamlit Cloud)
- [ ] **Fase 6**: Adição de mais anos de dados (2026+)
- [ ] **Fase 7**: Implementação de machine learning para previsões
- [ ] **Fase 8**: API REST para consumo dos dados processados
- [ ] **Fase 9**: Exportação de relatórios em PDF

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

