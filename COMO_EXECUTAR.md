# 🚀 GUIA DE EXECUÇÃO - Dashboard ProUni

Este guia mostra como executar o projeto de análise de dados do ProUni (2018-2020).

## 📋 Pré-requisitos

- Python 3.8 ou superior instalado
- Git (opcional, para clonar o repositório)

## 🛠️ Instalação

### 1. Preparar o Ambiente Virtual

Abra o PowerShell ou Prompt de Comando na pasta do projeto e execute:

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (PowerShell)
.\venv\Scripts\Activate.ps1

# OU ativar ambiente virtual (CMD)
venv\Scripts\activate.bat
```

### 2. Instalar Dependências

Com o ambiente virtual ativado:

```powershell
pip install -r requirements.txt
```

## 📊 Executar o Projeto

### Opção 1: Usar os Scripts Batch (Recomendado para Windows)

#### Passo 1: Processar os Dados
```
1. Clique duas vezes em: processar_dados.bat
```

Este script irá:
- Carregar os dados brutos de 2018, 2019 e 2020
- Padronizar as colunas
- Limpar e validar os dados
- Unificar todos os anos em um único arquivo
- Salvar em `data/processed/`

#### Passo 2: Iniciar o Dashboard
```
2. Clique duas vezes em: iniciar_dashboard.bat
```

O dashboard será aberto automaticamente e estará disponível em:
**http://localhost:8050**

### Opção 2: Executar Manualmente via Terminal

#### Passo 1: Processar os Dados
```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Processar dados
python src\data_processing\clean_data.py
```

#### Passo 2: Iniciar o Dashboard
```powershell
# Com o ambiente virtual ativado
python app.py
```

Acesse: **http://localhost:8050**

## 🎯 Funcionalidades do Dashboard

### Filtros Disponíveis

1. **📅 Ano**: Selecione 2018, 2019, 2020 ou "Todos"
2. **🗺️ Estado (UF)**: Filtre por estado específico
3. **🎓 Tipo de Bolsa**: Integral, Parcial ou Todas
4. **📚 Modalidade**: Presencial, EAD, etc.
5. **🔍 Buscar Curso**: Digite o nome do curso

### Visualizações

- **Cards de Estatísticas**: Total de bolsas, integrais, parciais e instituições
- **Gráfico de Evolução**: Linha temporal mostrando a evolução ao longo dos anos
- **Distribuição por Estado**: Top 15 estados com mais bolsas
- **Top 15 Cursos**: Cursos mais procurados
- **Tipo de Bolsa**: Distribuição entre integrais e parciais
- **Tabela Detalhada**: Visualização dos dados filtrados

## 🔧 Resolução de Problemas

### Erro: "Dados não encontrados"
**Solução**: Execute primeiro o script de processamento de dados:
```powershell
python src\data_processing\clean_data.py
```

### Erro: "Module not found"
**Solução**: Instale as dependências:
```powershell
pip install -r requirements.txt
```

### Erro: "Permission denied" ao ativar venv
**Solução**: Execute o PowerShell como Administrador e rode:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Dashboard não abre no navegador
**Solução**: Abra manualmente: http://localhost:8050

## 📂 Estrutura de Dados

### Dados Brutos (input)
```
data/raw/
├── pda-prouni-2018.csv
├── pda-prouni-2019.csv
└── ProuniRelatorioDadosAbertos2020.csv
```

### Dados Processados (output)
```
data/processed/
├── prouni_2018_2020_processado.csv
└── prouni_2018_2020_processado.parquet
```

## 📊 Análise dos Dados

O script de processamento realiza:

1. ✅ Carregamento com encoding correto
2. ✅ Padronização de nomes de colunas
3. ✅ Limpeza de dados inconsistentes
4. ✅ Conversão de tipos de dados
5. ✅ Unificação dos três anos (2018-2020)
6. ✅ Geração de estatísticas

## 🎓 Colunas Disponíveis

- `ano_concessao`: Ano da bolsa
- `codigo_ies`: Código da instituição
- `nome_ies`: Nome da instituição
- `municipio_ies`: Município da IES
- `campus`: Campus da instituição
- `tipo_bolsa`: INTEGRAL ou PARCIAL
- `modalidade_ensino`: Modalidade do curso
- `nome_curso`: Nome do curso
- `turno`: Turno do curso
- `sexo_beneficiario`: Sexo do beneficiário
- `raca_beneficiario`: Raça/cor do beneficiário
- `data_nascimento`: Data de nascimento
- `idade_aproximada`: Idade calculada
- `deficiente_fisico`: Possui deficiência física
- `regiao_beneficiario`: Região do beneficiário
- `uf_beneficiario`: Estado do beneficiário
- `municipio_beneficiario`: Município do beneficiário

## ⚡ Dicas de Performance

- Use o arquivo `.parquet` para carregamento mais rápido
- Aplique filtros progressivamente (ano → estado → curso)
- Para análises de muitos dados, considere usar apenas anos específicos

## 🛑 Encerrar o Dashboard

- Pressione `CTRL + C` no terminal
- Ou feche a janela do terminal

## 📝 Notas

- O dashboard roda em modo debug por padrão
- Alterações no código recarregam automaticamente
- Os dados são carregados uma vez ao iniciar
- Filtros são aplicados em tempo real

## 🆘 Suporte

Em caso de problemas:
1. Verifique se o ambiente virtual está ativo
2. Confirme que os dados foram processados
3. Verifique a versão do Python (3.8+)
4. Reinstale as dependências se necessário

---

**Desenvolvido por**: João Victor Costa Andrade  
**Fonte dos Dados**: Portal de Dados Abertos do Governo Federal
