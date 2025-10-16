"""
Callbacks do dashboard do ProUni

Define os callbacks para interatividade do dashboard.

Autor: João Victor Costa Andrade
Data: Outubro 2025
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, callback, State
from src.dashboard.layout import aplicar_tema_grafico, obter_cores_tema
import dash

# Variável global para armazenar os dados
dados_prouni = None

def carregar_dados():
    """Carrega os dados processados do ProUni"""
    global dados_prouni
    
    if dados_prouni is None:
        try:
            dados_prouni = pd.read_parquet('data/processed/prouni_2018_2019_2020_processado.parquet')
            print(f"✅ Dados carregados para dashboard: {dados_prouni.shape[0]:,} registros")
        except Exception as e:
            try:
                dados_prouni = pd.read_csv('data/processed/prouni_2018_2019_2020_processado.csv')
                print(f"✅ Dados carregados via CSV: {dados_prouni.shape[0]:,} registros")
            except Exception as e2:
                print(f"❌ Erro ao carregar dados: {e2}")
                dados_prouni = pd.DataFrame()
    
    return dados_prouni

def filtrar_dados(ano='todos', regiao='todas', uf='todas', tipo_bolsa='todos', modalidade='todas'):
    """Aplica filtros aos dados"""
    
    df = carregar_dados().copy()
    
    if df.empty:
        return df
    
    # Filtro por ano
    if ano != 'todos' and ano is not None:
        df = df[df['ano_concessao'] == ano]
    
    # Filtro por região
    if regiao != 'todas' and regiao is not None:
        df = df[df['regiao_beneficiario'] == regiao]
    
    # Filtro por UF
    if uf != 'todas' and uf is not None:
        df = df[df['uf_beneficiario'] == uf]
    
    # Filtro por tipo de bolsa
    if tipo_bolsa != 'todos' and tipo_bolsa is not None:
        df = df[df['tipo_bolsa'] == tipo_bolsa]
    
    # Filtro por modalidade
    if modalidade != 'todas' and modalidade is not None:
        df = df[df['modalidade_ensino'] == modalidade]
    
    return df

# Callback para popular os dropdowns
@callback(
    [Output('filtro-regiao', 'options'),
     Output('filtro-uf', 'options'),
     Output('filtro-tipo-bolsa', 'options'),
     Output('filtro-modalidade', 'options')],
    Input('filtro-ano', 'value')
)
def atualizar_opcoes_filtros(ano_selecionado):
    """Atualiza as opções dos filtros baseado no ano selecionado"""
    
    print(f"🔍 DEBUG: Ano selecionado = {ano_selecionado}")
    
    df = filtrar_dados(ano=ano_selecionado)
    
    print(f"🔍 DEBUG: Dados filtrados = {len(df):,} registros")
    print(f"🔍 DEBUG: Anos disponíveis = {sorted(df['ano_concessao'].unique()) if not df.empty else 'Nenhum'}")
    
    if df.empty:
        return [], [], [], []
    
    # Opções de região
    regioes = sorted(df['regiao_beneficiario'].dropna().unique())
    opcoes_regiao = [{'label': 'Todas', 'value': 'todas'}] + [{'label': r, 'value': r} for r in regioes]
    
    # Opções de UF
    ufs = sorted(df['uf_beneficiario'].dropna().unique())
    opcoes_uf = [{'label': 'Todas', 'value': 'todas'}] + [{'label': u, 'value': u} for u in ufs]
    
    # Opções de tipo de bolsa
    tipos = sorted(df['tipo_bolsa'].dropna().unique())
    opcoes_tipo = [{'label': 'Todos', 'value': 'todos'}] + [{'label': t, 'value': t} for t in tipos]
    
    # Opções de modalidade
    modalidades = sorted(df['modalidade_ensino'].dropna().unique())
    opcoes_modalidade = [{'label': 'Todas', 'value': 'todas'}] + [{'label': m, 'value': m} for m in modalidades]
    
    return opcoes_regiao, opcoes_uf, opcoes_tipo, opcoes_modalidade

# Callback para atualizar UF baseado na região
@callback(
    Output('filtro-uf', 'options', allow_duplicate=True),
    Input('filtro-regiao', 'value'),
    prevent_initial_call=True
)
def atualizar_uf_por_regiao(regiao_selecionada):
    """Atualiza as opções de UF baseado na região selecionada"""
    
    df = filtrar_dados(regiao=regiao_selecionada)
    
    if df.empty:
        return [{'label': 'Todas', 'value': 'todas'}]
    
    ufs = sorted(df['uf_beneficiario'].dropna().unique())
    opcoes_uf = [{'label': 'Todas', 'value': 'todas'}] + [{'label': u, 'value': u} for u in ufs]
    
    return opcoes_uf

# Callback para atualizar métricas
@callback(
    [Output('total-bolsas', 'children'),
     Output('total-ies', 'children'),
     Output('total-cursos', 'children'),
     Output('percentual-integral', 'children')],
    [Input('filtro-ano', 'value'),
     Input('filtro-regiao', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-tipo-bolsa', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_metricas(ano, regiao, uf, tipo_bolsa, modalidade):
    """Atualiza as métricas principais do dashboard"""
    
    df = filtrar_dados(ano, regiao, uf, tipo_bolsa, modalidade)
    
    if df.empty:
        return "0", "0", "0", "0%"
    
    total_bolsas = len(df)
    total_ies = df['nome_ies'].nunique()
    total_cursos = df['nome_curso'].nunique()
    
    # Calcular percentual de bolsas integrais
    bolsas_integrais = len(df[df['tipo_bolsa'] == 'INTEGRAL'])
    perc_integral = (bolsas_integrais / total_bolsas * 100) if total_bolsas > 0 else 0
    
    return f"{total_bolsas:,}", f"{total_ies:,}", f"{total_cursos:,}", f"{perc_integral:.1f}%"

# Callback para conteúdo das abas
@callback(
    Output('conteudo-tabs', 'children'),
    Input('tabs-dashboard', 'value')
)
def atualizar_conteudo_aba(aba_ativa):
    """Atualiza o conteúdo baseado na aba ativa"""
    
    from src.dashboard.layout import (
        criar_aba_visao_geral, criar_aba_geografica, criar_aba_cursos,
        criar_aba_perfil, criar_aba_temporal
    )
    
    if aba_ativa == 'tab-visao-geral':
        return criar_aba_visao_geral()
    elif aba_ativa == 'tab-geografica':
        return criar_aba_geografica()
    elif aba_ativa == 'tab-cursos':
        return criar_aba_cursos()
    elif aba_ativa == 'tab-perfil':
        return criar_aba_perfil()
    elif aba_ativa == 'tab-temporal':
        return criar_aba_temporal()
    else:
        return criar_aba_visao_geral()

# Callbacks para gráficos da aba Visão Geral
@callback(
    Output('grafico-evolucao-anual', 'figure'),
    [Input('filtro-regiao', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-tipo-bolsa', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_grafico_evolucao_anual(regiao, uf, tipo_bolsa, modalidade):
    """Gráfico de evolução anual"""
    
    df = filtrar_dados('todos', regiao, uf, tipo_bolsa, modalidade)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Evolução Anual de Bolsas")
    
    evolucao = df.groupby('ano_concessao').size().reset_index(name='total')
    
    fig = px.bar(evolucao, x='ano_concessao', y='total',
                title="Evolução Anual de Bolsas",
                labels={'ano_concessao': 'Ano', 'total': 'Número de Bolsas'})
    
    return aplicar_tema_grafico(fig, "Evolução Anual de Bolsas")

@callback(
    Output('grafico-distribuicao-tipo', 'figure'),
    [Input('filtro-ano', 'value'),
     Input('filtro-regiao', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_grafico_distribuicao_tipo(ano, regiao, uf, modalidade):
    """Gráfico de distribuição por tipo de bolsa"""
    
    df = filtrar_dados(ano, regiao, uf, 'todos', modalidade)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Distribuição por Tipo de Bolsa")
    
    dist_tipo = df['tipo_bolsa'].value_counts()
    
    fig = px.pie(values=dist_tipo.values, names=dist_tipo.index,
                title="Distribuição por Tipo de Bolsa")
    
    return aplicar_tema_grafico(fig, "Distribuição por Tipo de Bolsa")

@callback(
    Output('grafico-distribuicao-modalidade', 'figure'),
    [Input('filtro-ano', 'value'),
     Input('filtro-regiao', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-tipo-bolsa', 'value')]
)
def atualizar_grafico_distribuicao_modalidade(ano, regiao, uf, tipo_bolsa):
    """Gráfico de distribuição por modalidade"""
    
    df = filtrar_dados(ano, regiao, uf, tipo_bolsa, 'todas')
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Distribuição por Modalidade")
    
    dist_modalidade = df['modalidade_ensino'].value_counts()
    
    fig = px.bar(x=dist_modalidade.index, y=dist_modalidade.values,
                title="Distribuição por Modalidade",
                labels={'x': 'Modalidade', 'y': 'Número de Bolsas'})
    
    return aplicar_tema_grafico(fig, "Distribuição por Modalidade")

@callback(
    Output('grafico-distribuicao-regiao', 'figure'),
    [Input('filtro-ano', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-tipo-bolsa', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_grafico_distribuicao_regiao(ano, uf, tipo_bolsa, modalidade):
    """Gráfico de distribuição por região"""
    
    df = filtrar_dados(ano, 'todas', uf, tipo_bolsa, modalidade)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Distribuição por Região")
    
    dist_regiao = df['regiao_beneficiario'].value_counts()
    
    fig = px.pie(values=dist_regiao.values, names=dist_regiao.index,
                title="Distribuição por Região")
    
    return aplicar_tema_grafico(fig, "Distribuição por Região")

# Callbacks para gráficos da aba Geográfica
@callback(
    Output('grafico-top-estados', 'figure'),
    [Input('filtro-ano', 'value'),
     Input('filtro-regiao', 'value'),
     Input('filtro-tipo-bolsa', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_grafico_top_estados(ano, regiao, tipo_bolsa, modalidade):
    """Gráfico dos top estados"""
    
    df = filtrar_dados(ano, regiao, 'todas', tipo_bolsa, modalidade)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Top 10 Estados")
    
    top_estados = df['uf_beneficiario'].value_counts().head(10)
    
    fig = px.bar(x=top_estados.values, y=top_estados.index, orientation='h',
                title="Top 10 Estados",
                labels={'x': 'Número de Bolsas', 'y': 'Estado'})
    
    return aplicar_tema_grafico(fig, "Top 10 Estados")

@callback(
    Output('grafico-top-municipios', 'figure'),
    [Input('filtro-ano', 'value'),
     Input('filtro-regiao', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-tipo-bolsa', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_grafico_top_municipios(ano, regiao, uf, tipo_bolsa, modalidade):
    """Gráfico dos top municípios"""
    
    df = filtrar_dados(ano, regiao, uf, tipo_bolsa, modalidade)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Top 10 Municípios")
    
    top_municipios = df['municipio_beneficiario'].value_counts().head(10)
    
    fig = px.bar(x=top_municipios.values, y=top_municipios.index, orientation='h',
                title="Top 10 Municípios",
                labels={'x': 'Número de Bolsas', 'y': 'Município'})
    
    return aplicar_tema_grafico(fig, "Top 10 Municípios")

# Callbacks para gráficos da aba Cursos
@callback(
    Output('grafico-top-cursos', 'figure'),
    [Input('filtro-ano', 'value'),
     Input('filtro-regiao', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-tipo-bolsa', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_grafico_top_cursos(ano, regiao, uf, tipo_bolsa, modalidade):
    """Gráfico dos top cursos"""
    
    df = filtrar_dados(ano, regiao, uf, tipo_bolsa, modalidade)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Top 10 Cursos")
    
    top_cursos = df['nome_curso'].value_counts().head(10)
    
    fig = px.bar(x=top_cursos.values, y=top_cursos.index, orientation='h',
                title="Top 10 Cursos",
                labels={'x': 'Número de Bolsas', 'y': 'Curso'})
    
    return aplicar_tema_grafico(fig, "Top 10 Cursos")

@callback(
    Output('grafico-top-ies', 'figure'),
    [Input('filtro-ano', 'value'),
     Input('filtro-regiao', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-tipo-bolsa', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_grafico_top_ies(ano, regiao, uf, tipo_bolsa, modalidade):
    """Gráfico das top IES"""
    
    df = filtrar_dados(ano, regiao, uf, tipo_bolsa, modalidade)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Top 10 Instituições")
    
    top_ies = df['nome_ies'].value_counts().head(10)
    
    fig = px.bar(x=top_ies.values, y=top_ies.index, orientation='h',
                title="Top 10 Instituições",
                labels={'x': 'Número de Bolsas', 'y': 'Instituição'})
    
    # Ajustar altura para acomodar nomes longos
    fig.update_layout(height=500)
    
    return aplicar_tema_grafico(fig, "Top 10 Instituições")

# Callbacks para gráficos da aba Perfil
@callback(
    Output('grafico-distribuicao-sexo', 'figure'),
    [Input('filtro-ano', 'value'),
     Input('filtro-regiao', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-tipo-bolsa', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_grafico_distribuicao_sexo(ano, regiao, uf, tipo_bolsa, modalidade):
    """Gráfico de distribuição por sexo"""
    
    df = filtrar_dados(ano, regiao, uf, tipo_bolsa, modalidade)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Distribuição por Sexo")
    
    dist_sexo = df['sexo_beneficiario'].value_counts()
    
    fig = px.pie(values=dist_sexo.values, names=dist_sexo.index,
                title="Distribuição por Sexo")
    
    return aplicar_tema_grafico(fig, "Distribuição por Sexo")

@callback(
    Output('grafico-distribuicao-raca', 'figure'),
    [Input('filtro-ano', 'value'),
     Input('filtro-regiao', 'value'),
     Input('filtro-uf', 'value'),
     Input('filtro-tipo-bolsa', 'value'),
     Input('filtro-modalidade', 'value')]
)
def atualizar_grafico_distribuicao_raca(ano, regiao, uf, tipo_bolsa, modalidade):
    """Gráfico de distribuição por raça/cor"""
    
    df = filtrar_dados(ano, regiao, uf, tipo_bolsa, modalidade)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Nenhum dado disponível", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return aplicar_tema_grafico(fig, "Distribuição por Raça/Cor")
    
    dist_raca = df['raca_beneficiario'].value_counts()
    
    fig = px.bar(x=dist_raca.index, y=dist_raca.values,
                title="Distribuição por Raça/Cor",
                labels={'x': 'Raça/Cor', 'y': 'Número de Bolsas'})
    
    return aplicar_tema_grafico(fig, "Distribuição por Raça/Cor")

@callback(
    Output('filtro-ano', 'options'),
    Input('filtro-ano', 'id')
)
def atualizar_opcoes_ano(_):
    df = carregar_dados()
    anos = sorted(df['ano_concessao'].dropna().unique())
    opcoes = [{'label': 'Todos', 'value': 'todos'}] + [{'label': str(ano), 'value': int(ano)} for ano in anos]
    return opcoes