"""
Análise geográfica dos dados do ProUni

Este módulo contém análises relacionadas à distribuição geográfica
das bolsas, análise por estados, regiões e municípios.

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
        try:
            df = pd.read_csv('data/processed/prouni_2018_2019_2020_processado.csv')
            print(f"✅ Dados carregados via CSV: {df.shape[0]:,} registros")
            return df
        except Exception as e2:
            print(f"❌ Erro ao carregar dados: {e2}")
            return None

def analisar_distribuicao_regional(df):
    """Analisa a distribuição das bolsas por região"""
    
    print("🗺️ ANÁLISE REGIONAL")
    print("="*50)
    
    # 1. Distribuição por região
    dist_regiao = df['regiao_beneficiario'].value_counts()
    total = len(df)
    
    print(f"\n📊 Distribuição por região:")
    for regiao, qtd in dist_regiao.items():
        perc = (qtd / total) * 100
        print(f"  {regiao}: {qtd:,} bolsas ({perc:.1f}%)")
    
    # 2. Distribuição por região e ano
    print(f"\n📈 Distribuição por região e ano:")
    dist_regiao_ano = df.groupby(['regiao_beneficiario', 'ano_concessao']).size().unstack(fill_value=0)
    
    for regiao in dist_regiao_ano.index:
        print(f"\n  {regiao}:")
        total_regiao = dist_regiao_ano.loc[regiao].sum()
        for ano in dist_regiao_ano.columns:
            if pd.notna(ano):
                qtd = dist_regiao_ano.loc[regiao, ano]
                perc_ano = (qtd / total_regiao) * 100 if total_regiao > 0 else 0
                print(f"    {int(ano)}: {qtd:,} ({perc_ano:.1f}%)")
    
    # 3. Análise por tipo de bolsa por região
    print(f"\n🎓 Tipo de bolsa por região:")
    dist_regiao_tipo = df.groupby(['regiao_beneficiario', 'tipo_bolsa']).size().unstack(fill_value=0)
    
    for regiao in dist_regiao_tipo.index:
        print(f"\n  {regiao}:")
        total_regiao = dist_regiao_tipo.loc[regiao].sum()
        for tipo in dist_regiao_tipo.columns:
            qtd = dist_regiao_tipo.loc[regiao, tipo]
            perc = (qtd / total_regiao) * 100 if total_regiao > 0 else 0
            print(f"    {tipo}: {qtd:,} ({perc:.1f}%)")
    
    return {
        'dist_regiao': dist_regiao,
        'dist_regiao_ano': dist_regiao_ano,
        'dist_regiao_tipo': dist_regiao_tipo
    }

def analisar_distribuicao_estadual(df):
    """Analisa a distribuição das bolsas por estado"""
    
    print(f"\n🏛️ ANÁLISE ESTADUAL")
    print("="*50)
    
    # 1. Top 15 estados
    dist_uf = df['uf_beneficiario'].value_counts().head(15)
    total = len(df)
    
    print(f"\n🏆 Top 15 estados com mais bolsas:")
    for i, (uf, qtd) in enumerate(dist_uf.items(), 1):
        perc = (qtd / total) * 100
        print(f"  {i:2d}. {uf}: {qtd:,} bolsas ({perc:.1f}%)")
    
    # 2. Análise concentração vs dispersão
    # Calcular índice de concentração (% dos top 5 estados)
    top5_total = dist_uf.head(5).sum()
    concentracao = (top5_total / total) * 100
    
    print(f"\n📈 Índice de concentração:")
    print(f"  Top 5 estados concentram: {concentracao:.1f}% das bolsas")
    print(f"  Top 10 estados concentram: {dist_uf.head(10).sum()/total*100:.1f}% das bolsas")
    
    # 3. Distribuição por modalidade por estado (top 10)
    print(f"\n🏫 Modalidade por estado (Top 10):")
    top10_ufs = dist_uf.head(10).index
    
    dist_uf_modalidade = df[df['uf_beneficiario'].isin(top10_ufs)].groupby(['uf_beneficiario', 'modalidade_ensino']).size().unstack(fill_value=0)
    
    for uf in top10_ufs:
        print(f"\n  {uf}:")
        total_uf = dist_uf_modalidade.loc[uf].sum()
        for modalidade in dist_uf_modalidade.columns:
            qtd = dist_uf_modalidade.loc[uf, modalidade]
            perc = (qtd / total_uf) * 100 if total_uf > 0 else 0
            print(f"    {modalidade}: {qtd:,} ({perc:.1f}%)")
    
    return {
        'dist_uf': dist_uf,
        'dist_uf_modalidade': dist_uf_modalidade,
        'concentracao': concentracao
    }

def analisar_municipios(df):
    """Analisa a distribuição por municípios"""
    
    print(f"\n🏙️ ANÁLISE MUNICIPAL")
    print("="*50)
    
    # 1. Top 20 municípios
    dist_municipios = df['municipio_beneficiario'].value_counts().head(20)
    total = len(df)
    
    print(f"\n🏆 Top 20 municípios com mais bolsas:")
    for i, (municipio, qtd) in enumerate(dist_municipios.items(), 1):
        perc = (qtd / total) * 100
        print(f"  {i:2d}. {municipio}: {qtd:,} bolsas ({perc:.2f}%)")
    
    # 2. Análise por estado dos top municípios
    top_municipios_uf = df[df['municipio_beneficiario'].isin(dist_municipios.head(10).index)][['municipio_beneficiario', 'uf_beneficiario']].drop_duplicates()
    
    print(f"\n📍 Estados dos top 10 municípios:")
    for _, row in top_municipios_uf.iterrows():
        municipio = row['municipio_beneficiario']
        uf = row['uf_beneficiario']
        qtd = dist_municipios[municipio]
        print(f"  {municipio} ({uf}): {qtd:,} bolsas")
    
    return {
        'dist_municipios': dist_municipios,
        'top_municipios_uf': top_municipios_uf
    }

def analisar_migracao_educacional(df):
    """Analisa possível migração educacional comparando UF do beneficiário com localização da IES"""
    
    print(f"\n🎓 ANÁLISE DE MIGRAÇÃO EDUCACIONAL")
    print("="*50)
    
    # Para esta análise, precisaríamos dos dados de localização das IES
    # Como não temos essa informação nos dados atuais, faremos uma análise conceitual
    
    print(f"\n📝 Nota: Para análise completa de migração educacional seria necessário:")
    print("  - Localização (UF) das Instituições de Ensino Superior")
    print("  - Comparação entre UF do beneficiário vs UF da IES")
    print("  - Identificação de fluxos migratórios para educação")
    
    # Análise que podemos fazer: concentração de IES por código
    print(f"\n🏛️ Análise de concentração de IES:")
    
    ies_por_uf = df.groupby('uf_beneficiario')['codigo_ies'].nunique().sort_values(ascending=False)
    
    print(f"\nTop 10 UFs com mais IES participantes:")
    for i, (uf, qtd_ies) in enumerate(ies_por_uf.head(10).items(), 1):
        bolsas_uf = len(df[df['uf_beneficiario'] == uf])
        media_bolsas_ies = bolsas_uf / qtd_ies if qtd_ies > 0 else 0
        print(f"  {i:2d}. {uf}: {qtd_ies} IES, {bolsas_uf:,} bolsas (média: {media_bolsas_ies:.0f} bolsas/IES)")
    
    return {
        'ies_por_uf': ies_por_uf
    }

def gerar_visualizacoes_geograficas(dados_regionais, dados_estaduais, dados_municipais):
    """Gera visualizações para análise geográfica"""
    
    print(f"\n📊 Gerando visualizações geográficas...")
    
    # 1. Gráfico de pizza - distribuição regional
    fig_regiao = px.pie(
        values=dados_regionais['dist_regiao'].values,
        names=dados_regionais['dist_regiao'].index,
        title='Distribuição de Bolsas por Região'
    )
    fig_regiao.write_html('visualizacoes/distribuicao_regional.html')
    
    # 2. Gráfico de barras - top 15 estados
    top15_df = pd.DataFrame({
        'UF': dados_estaduais['dist_uf'].index,
        'Bolsas': dados_estaduais['dist_uf'].values
    })
    
    fig_estados = px.bar(
        top15_df,
        x='UF',
        y='Bolsas',
        title='Top 15 Estados - Número de Bolsas ProUni',
        labels={'Bolsas': 'Número de Bolsas'},
        color='Bolsas',
        color_continuous_scale='viridis'
    )
    fig_estados.update_layout(showlegend=False)
    fig_estados.write_html('visualizacoes/top_estados.html')
    
    # 3. Gráfico de barras - top 15 municípios
    top15_mun_df = pd.DataFrame({
        'Município': dados_municipais['dist_municipios'].head(15).index,
        'Bolsas': dados_municipais['dist_municipios'].head(15).values
    })
    
    fig_municipios = px.bar(
        top15_mun_df,
        x='Município',
        y='Bolsas',
        title='Top 15 Municípios - Número de Bolsas ProUni',
        labels={'Bolsas': 'Número de Bolsas'},
        color='Bolsas',
        color_continuous_scale='plasma'
    )
    fig_municipios.update_layout(showlegend=False, xaxis_tickangle=-45)
    fig_municipios.write_html('visualizacoes/top_municipios.html')
    
    # 4. Heatmap - região vs tipo de bolsa
    heatmap_data = dados_regionais['dist_regiao_tipo']
    
    fig_heatmap = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        title='Distribuição Tipo de Bolsa por Região',
        labels=dict(x="Tipo de Bolsa", y="Região", color="Quantidade"),
        color_continuous_scale='viridis'
    )
    fig_heatmap.write_html('visualizacoes/heatmap_regiao_tipo.html')
    
    print("✅ Visualizações geográficas salvas em visualizacoes/")
    
    return {
        'distribuicao_regional': fig_regiao,
        'top_estados': fig_estados,
        'top_municipios': fig_municipios,
        'heatmap_regiao_tipo': fig_heatmap
    }

def main():
    """Função principal da análise geográfica"""
    
    print("🚀 INICIANDO ANÁLISE GEOGRÁFICA DO PROUNI")
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
    dados_regionais = analisar_distribuicao_regional(df)
    dados_estaduais = analisar_distribuicao_estadual(df)
    dados_municipais = analisar_municipios(df)
    dados_migracao = analisar_migracao_educacional(df)
    
    # Gerar visualizações
    visualizacoes = gerar_visualizacoes_geograficas(dados_regionais, dados_estaduais, dados_municipais)
    
    print(f"\n🎉 ANÁLISE GEOGRÁFICA CONCLUÍDA!")
    print("="*50)
    
    return {
        'dados_regionais': dados_regionais,
        'dados_estaduais': dados_estaduais,
        'dados_municipais': dados_municipais,
        'dados_migracao': dados_migracao,
        'visualizacoes': visualizacoes
    }

if __name__ == "__main__":
    resultados = main()