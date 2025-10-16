"""
Análise de cursos e instituições do ProUni

Este módulo contém análises relacionadas aos cursos mais procurados,
instituições com mais bolsas, análise por área de conhecimento.

Autor: João Victor Costa Andrade
Data: Outubro 2025
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

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

def analisar_cursos_populares(df):
    """Analisa os cursos mais populares no ProUni"""
    
    print("🎓 ANÁLISE DE CURSOS")
    print("="*50)
    
    # 1. Top 20 cursos mais procurados
    cursos_populares = df['nome_curso'].value_counts().head(20)
    total = len(df)
    
    print(f"\n🏆 Top 20 cursos com mais bolsas:")
    for i, (curso, qtd) in enumerate(cursos_populares.items(), 1):
        perc = (qtd / total) * 100
        print(f"  {i:2d}. {curso}: {qtd:,} bolsas ({perc:.2f}%)")
    
    # 2. Análise por tipo de bolsa nos top cursos
    print(f"\n🎯 Tipo de bolsa nos top 10 cursos:")
    top10_cursos = cursos_populares.head(10).index
    
    for curso in top10_cursos:
        dados_curso = df[df['nome_curso'] == curso]
        dist_tipo = dados_curso['tipo_bolsa'].value_counts()
        total_curso = len(dados_curso)
        
        print(f"\n  {curso} ({total_curso:,} bolsas):")
        for tipo, qtd in dist_tipo.items():
            perc = (qtd / total_curso) * 100
            print(f"    {tipo}: {qtd:,} ({perc:.1f}%)")
    
    # 3. Análise por modalidade nos top cursos
    print(f"\n🏫 Modalidade nos top 10 cursos:")
    
    for curso in top10_cursos:
        dados_curso = df[df['nome_curso'] == curso]
        dist_modalidade = dados_curso['modalidade_ensino'].value_counts()
        total_curso = len(dados_curso)
        
        print(f"\n  {curso}:")
        for modalidade, qtd in dist_modalidade.items():
            perc = (qtd / total_curso) * 100
            print(f"    {modalidade}: {qtd:,} ({perc:.1f}%)")
    
    return {
        'cursos_populares': cursos_populares,
        'top10_cursos': top10_cursos
    }

def categorizar_areas_conhecimento(df):
    """Categoriza cursos por área de conhecimento"""
    
    print(f"\n📚 CATEGORIZAÇÃO POR ÁREA DE CONHECIMENTO")
    print("="*50)
    
    # Dicionário de categorização baseado em palavras-chave
    areas_conhecimento = {
        'Saúde': ['medicina', 'enfermagem', 'farmacia', 'odontologia', 'fisioterapia', 
                 'nutrição', 'psicologia', 'biomedicina', 'saude', 'veterinaria'],
        
        'Engenharia e Tecnologia': ['engenharia', 'tecnologia', 'tecnologo', 'sistemas', 
                                   'computacao', 'informatica', 'eletronica', 'mecanica'],
        
        'Ciências Humanas': ['pedagogia', 'historia', 'geografia', 'filosofia', 'sociologia',
                           'letras', 'literatura', 'educacao', 'licenciatura'],
        
        'Ciências Sociais e Jurídicas': ['direito', 'administracao', 'economia', 'contabeis',
                                        'gestao', 'marketing', 'recursos humanos', 'comercio'],
        
        'Comunicação e Artes': ['comunicacao', 'jornalismo', 'publicidade', 'design', 
                               'arquitetura', 'arte', 'musica', 'teatro'],
        
        'Ciências Exatas': ['matematica', 'fisica', 'quimica', 'estatistica', 'biologicas']
    }
    
    # Função para categorizar um curso
    def categorizar_curso(nome_curso):
        if pd.isna(nome_curso):
            return 'Outros'
        
        nome_lower = nome_curso.lower()
        
        for area, palavras_chave in areas_conhecimento.items():
            for palavra in palavras_chave:
                if palavra in nome_lower:
                    return area
        
        return 'Outros'
    
    # Aplicar categorização
    df_copy = df.copy()
    df_copy['area_conhecimento'] = df_copy['nome_curso'].apply(categorizar_curso)
    
    # Análise por área
    dist_areas = df_copy['area_conhecimento'].value_counts()
    total = len(df_copy)
    
    print(f"\n📊 Distribuição por área de conhecimento:")
    for area, qtd in dist_areas.items():
        perc = (qtd / total) * 100
        print(f"  {area}: {qtd:,} bolsas ({perc:.1f}%)")
    
    # Análise por área e tipo de bolsa
    print(f"\n🎓 Tipo de bolsa por área de conhecimento:")
    dist_area_tipo = df_copy.groupby(['area_conhecimento', 'tipo_bolsa']).size().unstack(fill_value=0)
    
    for area in dist_area_tipo.index:
        print(f"\n  {area}:")
        total_area = dist_area_tipo.loc[area].sum()
        for tipo in dist_area_tipo.columns:
            qtd = dist_area_tipo.loc[area, tipo]
            perc = (qtd / total_area) * 100 if total_area > 0 else 0
            print(f"    {tipo}: {qtd:,} ({perc:.1f}%)")
    
    # Análise por área e modalidade
    print(f"\n🏫 Modalidade por área de conhecimento:")
    dist_area_modalidade = df_copy.groupby(['area_conhecimento', 'modalidade_ensino']).size().unstack(fill_value=0)
    
    for area in dist_area_modalidade.index:
        print(f"\n  {area}:")
        total_area = dist_area_modalidade.loc[area].sum()
        for modalidade in dist_area_modalidade.columns:
            qtd = dist_area_modalidade.loc[area, modalidade]
            perc = (qtd / total_area) * 100 if total_area > 0 else 0
            print(f"    {modalidade}: {qtd:,} ({perc:.1f}%)")
    
    return {
        'df_categorizado': df_copy,
        'dist_areas': dist_areas,
        'dist_area_tipo': dist_area_tipo,
        'dist_area_modalidade': dist_area_modalidade
    }

def analisar_instituicoes(df):
    """Analisa as instituições de ensino superior"""
    
    print(f"\n🏛️ ANÁLISE DE INSTITUIÇÕES")
    print("="*50)
    
    # 1. Top 20 IES com mais bolsas
    ies_populares = df['nome_ies'].value_counts().head(20)
    total = len(df)
    
    print(f"\n🏆 Top 20 IES com mais bolsas:")
    for i, (ies, qtd) in enumerate(ies_populares.items(), 1):
        perc = (qtd / total) * 100
        print(f"  {i:2d}. {ies}: {qtd:,} bolsas ({perc:.2f}%)")
    
    # 2. Análise de concentração
    top5_total = ies_populares.head(5).sum()
    concentracao = (top5_total / total) * 100
    
    print(f"\n📈 Índice de concentração por IES:")
    print(f"  Top 5 IES concentram: {concentracao:.1f}% das bolsas")
    print(f"  Top 10 IES concentram: {ies_populares.head(10).sum()/total*100:.1f}% das bolsas")
    print(f"  Top 20 IES concentram: {ies_populares.head(20).sum()/total*100:.1f}% das bolsas")
    
    # 3. Análise por tipo de bolsa nas top IES
    print(f"\n🎓 Tipo de bolsa nas top 10 IES:")
    top10_ies = ies_populares.head(10).index
    
    for ies in top10_ies:
        dados_ies = df[df['nome_ies'] == ies]
        dist_tipo = dados_ies['tipo_bolsa'].value_counts()
        total_ies = len(dados_ies)
        
        print(f"\n  {ies} ({total_ies:,} bolsas):")
        for tipo, qtd in dist_tipo.items():
            perc = (qtd / total_ies) * 100
            print(f"    {tipo}: {qtd:,} ({perc:.1f}%)")
    
    # 4. Análise de diversidade de cursos por IES
    print(f"\n📚 Diversidade de cursos nas top 10 IES:")
    
    for ies in top10_ies:
        dados_ies = df[df['nome_ies'] == ies]
        num_cursos = dados_ies['nome_curso'].nunique()
        total_bolsas = len(dados_ies)
        media_bolsas_curso = total_bolsas / num_cursos
        
        print(f"  {ies}:")
        print(f"    Cursos oferecidos: {num_cursos}")
        print(f"    Média bolsas/curso: {media_bolsas_curso:.1f}")
        
        # Top 3 cursos da IES
        top_cursos_ies = dados_ies['nome_curso'].value_counts().head(3)
        print(f"    Top 3 cursos:")
        for curso, qtd in top_cursos_ies.items():
            perc = (qtd / total_bolsas) * 100
            print(f"      {curso}: {qtd} ({perc:.1f}%)")
    
    return {
        'ies_populares': ies_populares,
        'concentracao_ies': concentracao,
        'top10_ies': top10_ies
    }

def analisar_turnos(df):
    """Analisa a distribuição por turnos"""
    
    print(f"\n🕐 ANÁLISE POR TURNO")
    print("="*50)
    
    # 1. Distribuição geral por turno
    dist_turnos = df['turno'].value_counts()
    total = len(df)
    
    print(f"\n📊 Distribuição por turno:")
    for turno, qtd in dist_turnos.items():
        perc = (qtd / total) * 100
        print(f"  {turno}: {qtd:,} bolsas ({perc:.1f}%)")
    
    # 2. Turno por modalidade
    print(f"\n🏫 Turno por modalidade:")
    dist_turno_modalidade = df.groupby(['turno', 'modalidade_ensino']).size().unstack(fill_value=0)
    
    for turno in dist_turno_modalidade.index:
        print(f"\n  {turno}:")
        total_turno = dist_turno_modalidade.loc[turno].sum()
        for modalidade in dist_turno_modalidade.columns:
            qtd = dist_turno_modalidade.loc[turno, modalidade]
            perc = (qtd / total_turno) * 100 if total_turno > 0 else 0
            print(f"    {modalidade}: {qtd:,} ({perc:.1f}%)")
    
    return {
        'dist_turnos': dist_turnos,
        'dist_turno_modalidade': dist_turno_modalidade
    }

def gerar_visualizacoes_cursos(dados_cursos, dados_areas, dados_ies, dados_turnos):
    """Gera visualizações para análise de cursos e instituições"""
    
    print(f"\n📊 Gerando visualizações de cursos e instituições...")
    
    # 1. Top 15 cursos
    top15_cursos_df = pd.DataFrame({
        'Curso': dados_cursos['cursos_populares'].head(15).index,
        'Bolsas': dados_cursos['cursos_populares'].head(15).values
    })
    
    fig_cursos = px.bar(
        top15_cursos_df,
        x='Bolsas',
        y='Curso',
        orientation='h',
        title='Top 15 Cursos - Número de Bolsas ProUni',
        labels={'Bolsas': 'Número de Bolsas'},
        color='Bolsas',
        color_continuous_scale='viridis'
    )
    fig_cursos.update_layout(height=600, showlegend=False)
    fig_cursos.write_html('visualizacoes/top_cursos.html')
    
    # 2. Distribuição por área de conhecimento
    fig_areas = px.pie(
        values=dados_areas['dist_areas'].values,
        names=dados_areas['dist_areas'].index,
        title='Distribuição de Bolsas por Área de Conhecimento'
    )
    fig_areas.write_html('visualizacoes/distribuicao_areas.html')
    
    # 3. Top 15 IES
    top15_ies_df = pd.DataFrame({
        'IES': dados_ies['ies_populares'].head(15).index,
        'Bolsas': dados_ies['ies_populares'].head(15).values
    })
    
    fig_ies = px.bar(
        top15_ies_df,
        x='Bolsas',
        y='IES',
        orientation='h',
        title='Top 15 IES - Número de Bolsas ProUni',
        labels={'Bolsas': 'Número de Bolsas'},
        color='Bolsas',
        color_continuous_scale='plasma'
    )
    fig_ies.update_layout(height=600, showlegend=False)
    fig_ies.write_html('visualizacoes/top_ies.html')
    
    # 4. Distribuição por turno
    fig_turnos = px.bar(
        x=dados_turnos['dist_turnos'].index,
        y=dados_turnos['dist_turnos'].values,
        title='Distribuição de Bolsas por Turno',
        labels={'x': 'Turno', 'y': 'Número de Bolsas'},
        color=dados_turnos['dist_turnos'].values,
        color_continuous_scale='blues'
    )
    fig_turnos.update_layout(showlegend=False)
    fig_turnos.write_html('visualizacoes/distribuicao_turnos.html')
    
    # 5. Heatmap área x modalidade
    heatmap_data = dados_areas['dist_area_modalidade']
    
    fig_heatmap = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        title='Distribuição Modalidade por Área de Conhecimento',
        labels=dict(x="Modalidade", y="Área de Conhecimento", color="Quantidade"),
        color_continuous_scale='viridis'
    )
    fig_heatmap.write_html('visualizacoes/heatmap_area_modalidade.html')
    
    print("✅ Visualizações de cursos e IES salvas em visualizacoes/")
    
    return {
        'top_cursos': fig_cursos,
        'distribuicao_areas': fig_areas,
        'top_ies': fig_ies,
        'distribuicao_turnos': fig_turnos,
        'heatmap_area_modalidade': fig_heatmap
    }

def main():
    """Função principal da análise de cursos e instituições"""
    
    print("🚀 INICIANDO ANÁLISE DE CURSOS E INSTITUIÇÕES")
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
    dados_cursos = analisar_cursos_populares(df)
    dados_areas = categorizar_areas_conhecimento(df)
    dados_ies = analisar_instituicoes(df)
    dados_turnos = analisar_turnos(df)
    
    # Gerar visualizações
    visualizacoes = gerar_visualizacoes_cursos(dados_cursos, dados_areas, dados_ies, dados_turnos)
    
    print(f"\n🎉 ANÁLISE DE CURSOS E INSTITUIÇÕES CONCLUÍDA!")
    print("="*50)
    
    return {
        'dados_cursos': dados_cursos,
        'dados_areas': dados_areas,
        'dados_ies': dados_ies,
        'dados_turnos': dados_turnos,
        'visualizacoes': visualizacoes
    }

if __name__ == "__main__":
    resultados = main()