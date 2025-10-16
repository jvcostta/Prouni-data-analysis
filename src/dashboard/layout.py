"""
Layouts do dashboard do ProUni

Define o layout principal e componentes do dashboard interativo.

Autor: João Victor Costa Andrade
Data: Outubro 2025
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def criar_layout_principal():
    """Cria o layout principal do dashboard"""
    
    layout = html.Div([
        # Header
        html.Div([
            html.H1("📊 Dashboard ProUni - Análise de Bolsas 2018-2020", 
                   className="header-title"),
            html.P("Análise interativa dos dados do Programa Universidade para Todos",
                   className="header-subtitle")
        ], className="header"),
        
        # Filtros
        html.Div([
            html.Div([
                html.Label("Ano:", className="filter-label"),
                dcc.Dropdown(
                    id='filtro-ano',
                    options=[{'label': 'Todos', 'value': 'todos'}], # será preenchido via callback
                    value='todos',
                    className="dropdown"
                )
            ], className="filter-item"),
            
            html.Div([
                html.Label("Região:", className="filter-label"),
                dcc.Dropdown(
                    id='filtro-regiao',
                    options=[],  # Será preenchido via callback
                    value='todas',
                    className="dropdown"
                )
            ], className="filter-item"),
            
            html.Div([
                html.Label("UF:", className="filter-label"),
                dcc.Dropdown(
                    id='filtro-uf',
                    options=[],  # Será preenchido via callback
                    value='todas',
                    className="dropdown"
                )
            ], className="filter-item"),
            
            html.Div([
                html.Label("Tipo de Bolsa:", className="filter-label"),
                dcc.Dropdown(
                    id='filtro-tipo-bolsa',
                    options=[],  # Será preenchido via callback
                    value='todos',
                    className="dropdown"
                )
            ], className="filter-item"),
            
            html.Div([
                html.Label("Modalidade:", className="filter-label"),
                dcc.Dropdown(
                    id='filtro-modalidade',
                    options=[],  # Será preenchido via callback
                    value='todas',
                    className="dropdown"
                )
            ], className="filter-item")
        ], className="filters-container"),
        
        # Cards de métricas principais
        html.Div([
            html.Div([
                html.H3(id="total-bolsas", children="0"),
                html.P("Total de Bolsas", className="metric-label")
            ], className="metric-card"),
            
            html.Div([
                html.H3(id="total-ies", children="0"),
                html.P("Instituições Participantes", className="metric-label")
            ], className="metric-card"),
            
            html.Div([
                html.H3(id="total-cursos", children="0"),
                html.P("Cursos Oferecidos", className="metric-label")
            ], className="metric-card"),
            
            html.Div([
                html.H3(id="percentual-integral", children="0%"),
                html.P("Bolsas Integrais", className="metric-label")
            ], className="metric-card")
        ], className="metrics-container"),
        
        # Abas do dashboard
        dcc.Tabs(id="tabs-dashboard", value='tab-visao-geral', children=[
            dcc.Tab(label='📊 Visão Geral', value='tab-visao-geral'),
            dcc.Tab(label='🗺️ Análise Geográfica', value='tab-geografica'),
            dcc.Tab(label='🎓 Cursos e IES', value='tab-cursos'),
            dcc.Tab(label='👥 Perfil dos Beneficiários', value='tab-perfil'),
            dcc.Tab(label='📈 Análise Temporal', value='tab-temporal')
        ], className="tabs"),
        
        # Conteúdo das abas
        html.Div(id='conteudo-tabs', className="tab-content"),
        
        # Footer
        html.Div([
            html.P("Desenvolvido com ❤️ usando Dash e Plotly | Dados: Portal de Dados Abertos MEC",
                   className="footer-text")
        ], className="footer")
        
    ], className="main-container")
    
    return layout

def criar_aba_visao_geral():
    """Cria o conteúdo da aba Visão Geral"""
    
    return html.Div([
        html.H2("📊 Visão Geral do ProUni", className="section-title"),
        
        # Gráficos principais
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-evolucao-anual', 
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half"),
            
            html.Div([
                dcc.Graph(id='grafico-distribuicao-tipo',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half")
        ], className="charts-row"),
        
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-distribuicao-modalidade',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half"),
            
            html.Div([
                dcc.Graph(id='grafico-distribuicao-regiao',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half")
        ], className="charts-row")
    ])

def criar_aba_geografica():
    """Cria o conteúdo da aba Análise Geográfica"""
    
    return html.Div([
        html.H2("🗺️ Análise Geográfica", className="section-title"),
        
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-mapa-estados',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-full")
        ], className="charts-row"),
        
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-top-estados',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half"),
            
            html.Div([
                dcc.Graph(id='grafico-top-municipios',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half")
        ], className="charts-row")
    ])

def criar_aba_cursos():
    """Cria o conteúdo da aba Cursos e IES"""
    
    return html.Div([
        html.H2("🎓 Cursos e Instituições", className="section-title"),
        
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-top-cursos',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half"),
            
            html.Div([
                dcc.Graph(id='grafico-areas-conhecimento',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half")
        ], className="charts-row"),
        
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-top-ies',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half"),
            
            html.Div([
                dcc.Graph(id='grafico-distribuicao-turnos',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half")
        ], className="charts-row")
    ])

def criar_aba_perfil():
    """Cria o conteúdo da aba Perfil dos Beneficiários"""
    
    return html.Div([
        html.H2("👥 Perfil dos Beneficiários", className="section-title"),
        
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-distribuicao-sexo',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half"),
            
            html.Div([
                dcc.Graph(id='grafico-distribuicao-raca',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half")
        ], className="charts-row"),
        
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-distribuicao-idade',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half"),
            
            html.Div([
                dcc.Graph(id='grafico-deficiencia',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half")
        ], className="charts-row")
    ])

def criar_aba_temporal():
    """Cria o conteúdo da aba Análise Temporal"""
    
    return html.Div([
        html.H2("📈 Análise Temporal", className="section-title"),
        
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-evolucao-temporal',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-full")
        ], className="charts-row"),
        
        html.Div([
            html.Div([
                dcc.Graph(id='grafico-evolucao-tipo-bolsa',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half"),
            
            html.Div([
                dcc.Graph(id='grafico-evolucao-modalidade',
                         config={'displayModeBar': False, 'responsive': True})
            ], className="chart-half")
        ], className="charts-row")
    ])

def obter_cores_tema():
    """Define paleta de cores do tema"""
    
    return {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e', 
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff7f0e',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40',
        'background': '#ffffff',
        'surface': '#f8f9fa'
    }

def aplicar_tema_grafico(fig, titulo=""):
    """Aplica tema consistente aos gráficos"""
    
    cores = obter_cores_tema()
    
    fig.update_layout(
        title=titulo,
        title_font_size=16,
        title_font_color=cores['dark'],
        paper_bgcolor=cores['background'],
        plot_bgcolor=cores['surface'],
        font_family="Arial, sans-serif",
        font_color=cores['dark'],
        margin=dict(l=50, r=50, t=50, b=50),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        # Fixar dimensões para evitar redimensionamento
        autosize=False,
        width=None,  # Permite que o container controle a largura
        height=400   # Altura fixa
    )
    
    # Atualizar eixos
    fig.update_xaxes(
        gridcolor='rgba(128,128,128,0.2)',
        showgrid=True,
        zeroline=False
    )
    
    fig.update_yaxes(
        gridcolor='rgba(128,128,128,0.2)',
        showgrid=True,
        zeroline=False
    )
    
    return fig