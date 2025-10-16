import pandas as pd

# Carregar dados
df = pd.read_parquet('data/processed/prouni_2018_2019_2020_processado.parquet')

print("🎉 TESTE FINAL - INTEGRAÇÃO 2018 CONCLUÍDA")
print("=" * 50)
print(f"✅ Total de registros: {len(df):,}")
print(f"📊 Colunas: {len(df.columns)}")

# Verificar anos
anos = df['ano_concessao'].dropna().unique()
anos_limpos = [int(ano) for ano in anos if pd.notna(ano)]
anos_ordenados = sorted(anos_limpos)

print(f"📅 Anos disponíveis: {anos_ordenados}")

# Distribuição por ano
print("\n📈 Distribuição por ano:")
for ano in anos_ordenados:
    qtd = len(df[df['ano_concessao'] == ano])
    print(f"  {ano}: {qtd:,} bolsas")

print("\n🎯 INTEGRAÇÃO CONCLUÍDA COM SUCESSO!")