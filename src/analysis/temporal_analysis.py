"""
Análise temporal dos dados do ProUni

Este módulo contém análises que envolvem comparações entre anos,
tendências temporais e evolução das bolsas ao longo do tempo.

Autor: João Victor Costa Andrade
Data: Outubro 2025
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def carregar_dados_processados():
    """Carrega os dados processados do ProUni"""
    try:
        df = pd.read_parquet('data/processed/prouni_2018_2019_2020_processado.parquet')
        print(f"✅ Dados carregados: {df.shape[0]:,} registros")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        try:
            df = pd.read_csv('data/processed/prouni_2018_2019_2020_processado.csv')
            print(f"✅ Dados carregados via CSV: {df.shape[0]:,} registros")
            return df
        except Exception as e2:
            print(f"❌ Erro ao carregar CSV: {e2}")
            return None

def analisar_evolucao_temporal(df):
    """Analisa a evolução temporal das bolsas ProUni"""
    
    print("📊 ANÁLISE TEMPORAL")
    print("="*50)
    
    # 1. Evolução geral por ano
    bolsas_por_ano = df.groupby('ano_concessao').size().reset_index(name='total_bolsas')
    
    print(f"\n📈 Evolução do número de bolsas:")
    for _, row in bolsas_por_ano.iterrows():
        ano = int(row['ano_concessao']) if pd.notna(row['ano_concessao']) else 'N/A'
        total = row['total_bolsas']
        print(f"  {ano}: {total:,} bolsas")
    
    # Calcular variação percentual
    if len(bolsas_por_ano) >= 2:
        variacao = ((bolsas_por_ano.iloc[1]['total_bolsas'] - bolsas_por_ano.iloc[0]['total_bolsas']) / 
                   bolsas_por_ano.iloc[0]['total_bolsas']) * 100
        print(f"  Variação 2019→2020: {variacao:.1f}%")
    
    # 2. Evolução por tipo de bolsa
    print(f"\n🎓 Evolução por tipo de bolsa:")
    evolucao_tipo = df.groupby(['ano_concessao', 'tipo_bolsa']).size().unstack(fill_value=0)
    
    for tipo in evolucao_tipo.columns:
        print(f"\n  {tipo}:")
        for ano in evolucao_tipo.index:
            if pd.notna(ano):
                valor = evolucao_tipo.loc[ano, tipo]
                print(f"    {int(ano)}: {valor:,}")
        
        # Calcular variação se temos dados de ambos os anos
        anos_validos = evolucao_tipo.index.dropna()
        if len(anos_validos) >= 2:
            ano1, ano2 = sorted(anos_validos)[:2]
            val1, val2 = evolucao_tipo.loc[ano1, tipo], evolucao_tipo.loc[ano2, tipo]
            if val1 > 0:
                var = ((val2 - val1) / val1) * 100
                print(f"    Variação: {var:.1f}%")
    
    # 3. Evolução por modalidade
    print(f"\n🏫 Evolução por modalidade:")
    evolucao_modalidade = df.groupby(['ano_concessao', 'modalidade_ensino']).size().unstack(fill_value=0)
    
    for modalidade in evolucao_modalidade.columns:
        print(f"\n  {modalidade}:")
        for ano in evolucao_modalidade.index:
            if pd.notna(ano):
                valor = evolucao_modalidade.loc[ano, modalidade]
                print(f"    {int(ano)}: {valor:,}")
        
        # Calcular variação
        anos_validos = evolucao_modalidade.index.dropna()
        if len(anos_validos) >= 2:
            ano1, ano2 = sorted(anos_validos)[:2]
            val1, val2 = evolucao_modalidade.loc[ano1, modalidade], evolucao_modalidade.loc[ano2, modalidade]
            if val1 > 0:
                var = ((val2 - val1) / val1) * 100
                print(f"    Variação: {var:.1f}%")
    
    return {
        'bolsas_por_ano': bolsas_por_ano,
        'evolucao_tipo': evolucao_tipo,
        'evolucao_modalidade': evolucao_modalidade
    }

def analisar_tendencias_demograficas(df):
    """Analisa tendências demográficas ao longo do tempo"""
    
    print(f"\n👥 ANÁLISE DEMOGRÁFICA TEMPORAL")
    print("="*50)
    
    # 1. Evolução por sexo
    print(f"\n♀️♂️ Distribuição por sexo ao longo do tempo:")
    dist_sexo = df.groupby(['ano_concessao', 'sexo_beneficiario']).size().unstack(fill_value=0)
    
    for ano in dist_sexo.index:
        if pd.notna(ano):
            print(f"\n  {int(ano)}:")
            total_ano = dist_sexo.loc[ano].sum()
            for sexo in dist_sexo.columns:
                valor = dist_sexo.loc[ano, sexo]
                perc = (valor / total_ano) * 100 if total_ano > 0 else 0
                print(f"    {sexo}: {valor:,} ({perc:.1f}%)")
    
    # 2. Evolução por raça/cor
    print(f"\n🌈 Distribuição por raça/cor ao longo do tempo:")
    dist_raca = df.groupby(['ano_concessao', 'raca_beneficiario']).size().unstack(fill_value=0)
    
    for ano in dist_raca.index:
        if pd.notna(ano):
            print(f"\n  {int(ano)}:")
            total_ano = dist_raca.loc[ano].sum()
            # Mostrar top 5 por ano
            top_racas = dist_raca.loc[ano].sort_values(ascending=False).head(5)
            for raca, valor in top_racas.items():
                perc = (valor / total_ano) * 100 if total_ano > 0 else 0
                print(f"    {raca}: {valor:,} ({perc:.1f}%)")
    
    # 3. Análise de idade
    print(f"\n🎂 Análise de idade dos beneficiários:")
    
    # Filtrar apenas registros com idade válida
    df_idade = df[df['idade_aproximada'].between(15, 80)].copy()
    
    for ano in df_idade['ano_concessao'].dropna().unique():
        dados_ano = df_idade[df_idade['ano_concessao'] == ano]
        idade_media = dados_ano['idade_aproximada'].mean()
        idade_mediana = dados_ano['idade_aproximada'].median()
        
        print(f"\n  {int(ano)}:")
        print(f"    Idade média: {idade_media:.1f} anos")
        print(f"    Idade mediana: {idade_mediana:.1f} anos")
        
        # Distribuição por faixas etárias
        faixas = pd.cut(dados_ano['idade_aproximada'], 
                       bins=[15, 20, 25, 30, 35, 50, 80], 
                       labels=['15-20', '21-25', '26-30', '31-35', '36-50', '51+'])
        dist_faixas = faixas.value_counts().sort_index()
        
        print("    Distribuição por faixa etária:")
        total = len(dados_ano)
        for faixa, qtd in dist_faixas.items():
            perc = (qtd / total) * 100
            print(f"      {faixa}: {qtd:,} ({perc:.1f}%)")
    
    return {
        'dist_sexo': dist_sexo,
        'dist_raca': dist_raca,
        'analise_idade': df_idade
    }

def gerar_visualizacoes_temporais(dados_temporais, dados_demograficos):
    """Gera visualizações para análise temporal"""
    
    print(f"\n📈 Gerando visualizações temporais...")
    
    # 1. Gráfico de evolução geral
    fig_evolucao = px.bar(
        dados_temporais['bolsas_por_ano'],
        x='ano_concessao',
        y='total_bolsas',
        title='Evolução do Número de Bolsas ProUni (2019-2020)',
        labels={'ano_concessao': 'Ano', 'total_bolsas': 'Total de Bolsas'},
        color='total_bolsas',
        color_continuous_scale='viridis'
    )
    fig_evolucao.update_layout(showlegend=False)
    fig_evolucao.write_html('visualizacoes/evolucao_bolsas.html')
    
    # 2. Gráfico por tipo de bolsa
    evolucao_tipo_df = dados_temporais['evolucao_tipo'].reset_index()
    evolucao_tipo_melted = evolucao_tipo_df.melt(
        id_vars=['ano_concessao'], 
        var_name='tipo_bolsa', 
        value_name='quantidade'
    )
    
    fig_tipo = px.bar(
        evolucao_tipo_melted,
        x='ano_concessao',
        y='quantidade',
        color='tipo_bolsa',
        title='Evolução por Tipo de Bolsa',
        labels={'ano_concessao': 'Ano', 'quantidade': 'Quantidade de Bolsas'},
        barmode='group'
    )
    fig_tipo.write_html('visualizacoes/evolucao_tipo_bolsa.html')
    
    # 3. Gráfico por modalidade
    evolucao_mod_df = dados_temporais['evolucao_modalidade'].reset_index()
    evolucao_mod_melted = evolucao_mod_df.melt(
        id_vars=['ano_concessao'], 
        var_name='modalidade', 
        value_name='quantidade'
    )
    
    fig_modalidade = px.bar(
        evolucao_mod_melted,
        x='ano_concessao',
        y='quantidade',
        color='modalidade',
        title='Evolução por Modalidade de Ensino',
        labels={'ano_concessao': 'Ano', 'quantidade': 'Quantidade de Bolsas'},
        barmode='group'
    )
    fig_modalidade.write_html('visualizacoes/evolucao_modalidade.html')
    
    print("✅ Visualizações salvas em visualizacoes/")
    
    return {
        'evolucao_geral': fig_evolucao,
        'evolucao_tipo': fig_tipo,
        'evolucao_modalidade': fig_modalidade
    }

def main():
    """Função principal da análise temporal"""
    
    print("🚀 INICIANDO ANÁLISE TEMPORAL DO PROUNI")
    print("="*50)
    
    # Carregar dados
    df = carregar_dados_processados()
    if df is None:
        print("❌ Não foi possível carregar os dados. Encerrando...")
        return
    
    # Criar diretório para visualizações
    import os
    os.makedirs('visualizacoes', exist_ok=True)
    
    # Realizar análises
    dados_temporais = analisar_evolucao_temporal(df)
    dados_demograficos = analisar_tendencias_demograficas(df)
    
    # Gerar visualizações
    visualizacoes = gerar_visualizacoes_temporais(dados_temporais, dados_demograficos)
    
    print(f"\n🎉 ANÁLISE TEMPORAL CONCLUÍDA!")
    print("="*50)
    
    return {
        'dados_temporais': dados_temporais,
        'dados_demograficos': dados_demograficos,
        'visualizacoes': visualizacoes
    }

if __name__ == "__main__":
    resultados = main()