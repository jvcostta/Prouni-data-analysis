# 📊 Documentação dos Dados do ProUni

## 📁 Pasta: `data/raw/`
Contém os dados originais baixados do Portal de Dados Abertos do Governo Federal.

### 📋 Arquivos Disponíveis

| Arquivo | Ano | Descrição | Status |
|---------|-----|-----------|--------|
| `pda-prouni-2019.csv` | 2019 | Dados das bolsas do ProUni concedidas em 2019 | ✅ Disponível |
| `ProuniRelatorioDadosAbertos2020.csv` | 2020 | Dados das bolsas do ProUni concedidas em 2020 | ✅ Disponível |
| *(aguardando)* | 2018 | Dados das bolsas do ProUni concedidas em 2018 | ❌ Não encontrado |

### 🔍 Próximos Passos para Análise

1. **Exploração Inicial**: Verificar estrutura e qualidade dos dados
2. **Padronização**: Garantir que ambos os arquivos tenham a mesma estrutura
3. **Limpeza**: Tratar dados faltantes e inconsistências
4. **Unificação**: Combinar os dados em um dataset único

## 📁 Pasta: `data/processed/`
Destinada aos dados limpos e processados, prontos para análise e visualização.

### 🎯 Estrutura Esperada dos Dados

Com base nos dados do ProUni, esperamos encontrar colunas como:
- **Ano**: Ano da concessão da bolsa
- **UF**: Unidade Federativa
- **Município**: Município da instituição
- **IES**: Nome da Instituição de Ensino Superior
- **Curso**: Nome do curso
- **Modalidade**: Presencial/EAD
- **Turno**: Matutino/Vespertino/Noturno/Integral
- **Tipo de Bolsa**: Integral/Parcial
- **Número de Bolsas**: Quantidade de bolsas concedidas

## 📝 Observações

- Os arquivos estão em formato CSV com encoding UTF-8
- Possível necessidade de tratamento de caracteres especiais
- Verificar se há diferenças na estrutura entre os anos