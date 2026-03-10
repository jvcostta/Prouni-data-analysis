import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
from pathlib import Path

# ============================================================================
# CONFIGURAÇÃO E CARREGAMENTO DE DADOS
# ============================================================================

# Inicializar aplicação Dash com tema Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "ProUni - Análise de Dados 2018-2020"

# Carregar dados processados
def carregar_dados_processados():
    """Carrega os dados já processados"""
    caminho_csv = Path('data/processed/prouni_2018_2020_processado.csv')
    caminho_parquet = Path('data/processed/prouni_2018_2020_processado.parquet')
    
    try:
        if caminho_parquet.exists():
            print("📂 Carregando dados do arquivo Parquet...")
            df = pd.read_parquet(caminho_parquet)
        elif caminho_csv.exists():
            print("📂 Carregando dados do arquivo CSV...")
            df = pd.read_csv(caminho_csv)
        else:
            print("❌ Nenhum arquivo de dados processados encontrado!")
            print("Execute primeiro: python src/data_processing/clean_data.py")
            return None
        
        print(f"✅ Dados carregados: {len(df):,} registros")
        return df
    
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return None

# Carregar dados
df = carregar_dados_processados()

if df is None:
    # Criar aplicação com mensagem de erro
    app.layout = dbc.Container([
        dbc.Alert(
            [
                html.H4("⚠️ Dados não encontrados!", className="alert-heading"),
                html.P("Execute o script de processamento de dados antes de iniciar o dashboard:"),
                html.Code("python src/data_processing/clean_data.py"),
            ],
            color="danger",
            className="mt-5"
        )
    ])
else:
    # ============================================================================
    # LAYOUT DO DASHBOARD
    # ============================================================================
    
    app.layout = dbc.Container([
        # Cabeçalho
        dbc.Row([
            dbc.Col([
                html.H1("📊 ProUni - Dashboard de Análise de Dados", 
                       className="text-center text-primary mb-3 mt-4"),
                html.H5("Análise de Bolsas do Programa Universidade para Todos (2018-2020)", 
                       className="text-center text-muted mb-4"),
                html.Hr()
            ])
        ]),
        
        # Filtros
        dbc.Row([
            dbc.Col([
                html.Label("📅 Ano:", className="fw-bold"),
                dcc.Dropdown(
                    id='filtro-ano',
                    options=[{'label': 'Todos', 'value': 'Todos'}] + 
                            [{'label': str(ano), 'value': ano} 
                             for ano in sorted(df['ano_concessao'].dropna().unique())],
                    value='Todos',
                    clearable=False
                )
            ], width=2),
            
            dbc.Col([
                html.Label("🗺️ Estado (UF):", className="fw-bold"),
                dcc.Dropdown(
                    id='filtro-uf',
                    options=[{'label': 'Todos', 'value': 'Todos'}] + 
                            [{'label': uf, 'value': uf} 
                             for uf in sorted(df['uf_beneficiario'].dropna().unique())],
                    value='Todos',
                    clearable=False
                )
            ], width=2),
            
            dbc.Col([
                html.Label("🎓 Tipo de Bolsa:", className="fw-bold"),
                dcc.Dropdown(
                    id='filtro-bolsa',
                    options=[{'label': 'Todas', 'value': 'Todas'}] + 
                            [{'label': tipo, 'value': tipo} 
                             for tipo in sorted(df['tipo_bolsa'].dropna().unique())],
                    value='Todas',
                    clearable=False
                )
            ], width=2),
            
            dbc.Col([
                html.Label("📚 Modalidade:", className="fw-bold"),
                dcc.Dropdown(
                    id='filtro-modalidade',
                    options=[{'label': 'Todas', 'value': 'Todas'}] + 
                            [{'label': mod, 'value': mod} 
                             for mod in sorted(df['modalidade_ensino'].dropna().unique())],
                    value='Todas',
                    clearable=False
                )
            ], width=3),
            
            dbc.Col([
                html.Label("🔍 Buscar Curso:", className="fw-bold"),
                dcc.Input(
                    id='filtro-curso',
                    type='text',
                    placeholder='Digite o nome do curso...',
                    className='form-control',
                    debounce=True
                )
            ], width=3),
        ], className="mb-4"),
        
        # Cards com Estatísticas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📊 Total de Bolsas", className="card-title text-center"),
                        html.H2(id='card-total', className="text-center text-primary")
                    ])
                ], color="light")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🎓 Bolsas Integrais", className="card-title text-center"),
                        html.H2(id='card-integral', className="text-center text-success")
                    ])
                ], color="light")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📝 Bolsas Parciais", className="card-title text-center"),
                        html.H2(id='card-parcial', className="text-center text-warning")
                    ])
                ], color="light")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🏫 Instituições", className="card-title text-center"),
                        html.H2(id='card-ies', className="text-center text-info")
                    ])
                ], color="light")
            ], width=3),
        ], className="mb-4"),
        
        # Gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Evolução de Bolsas por Ano"),
                    dbc.CardBody([
                        dcc.Graph(id='grafico-evolucao')
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🗺️ Distribuição por Estado (Top 15)"),
                    dbc.CardBody([
                        dcc.Graph(id='grafico-estados')
                    ])
                ])
            ], width=6),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📚 Top 15 Cursos Mais Procurados"),
                    dbc.CardBody([
                        dcc.Graph(id='grafico-cursos')
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🎯 Distribuição por Tipo de Bolsa"),
                    dbc.CardBody([
                        dcc.Graph(id='grafico-tipo-bolsa')
                    ])
                ])
            ], width=6),
        ], className="mb-4"),
        
        # Tabela de Dados
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📋 Visualização Detalhada dos Dados"),
                    dbc.CardBody([
                        dash_table.DataTable(
                            id='tabela-dados',
                            columns=[
                                {'name': 'Ano', 'id': 'ano_concessao'},
                                {'name': 'UF', 'id': 'uf_beneficiario'},
                                {'name': 'Instituição', 'id': 'nome_ies'},
                                {'name': 'Curso', 'id': 'nome_curso'},
                                {'name': 'Tipo Bolsa', 'id': 'tipo_bolsa'},
                                {'name': 'Modalidade', 'id': 'modalidade_ensino'},
                            ],
                            page_size=10,
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'textAlign': 'left',
                                'padding': '10px',
                                'fontSize': '14px'
                            },
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                }
                            ]
                        )
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Rodapé
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P("📊 Dashboard desenvolvido para análise de dados do ProUni", 
                      className="text-center text-muted"),
                html.P("Fonte: Portal de Dados Abertos do Governo Federal", 
                      className="text-center text-muted small")
            ])
        ])
        
    ], fluid=True)
    
    # ============================================================================
    # CALLBACKS
    # ============================================================================
    
    @callback(
        [
            Output('card-total', 'children'),
            Output('card-integral', 'children'),
            Output('card-parcial', 'children'),
            Output('card-ies', 'children'),
            Output('grafico-evolucao', 'figure'),
            Output('grafico-estados', 'figure'),
            Output('grafico-cursos', 'figure'),
            Output('grafico-tipo-bolsa', 'figure'),
            Output('tabela-dados', 'data'),
        ],
        [
            Input('filtro-ano', 'value'),
            Input('filtro-uf', 'value'),
            Input('filtro-bolsa', 'value'),
            Input('filtro-modalidade', 'value'),
            Input('filtro-curso', 'value'),
        ]
    )
    def atualizar_dashboard(ano, uf, tipo_bolsa, modalidade, curso):
        """Atualiza todos os componentes do dashboard com base nos filtros"""
        
        # Aplicar filtros
        df_filtrado = df.copy()
        
        if ano != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['ano_concessao'] == ano]
        
        if uf != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['uf_beneficiario'] == uf]
        
        if tipo_bolsa != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['tipo_bolsa'] == tipo_bolsa]
        
        if modalidade != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['modalidade_ensino'] == modalidade]
        
        if curso:
            df_filtrado = df_filtrado[
                df_filtrado['nome_curso'].str.contains(curso, case=False, na=False)
            ]
        
        # Calcular estatísticas dos cards
        total_bolsas = f"{len(df_filtrado):,}"
        total_integral = f"{len(df_filtrado[df_filtrado['tipo_bolsa'] == 'INTEGRAL']):,}"
        total_parcial = f"{len(df_filtrado[df_filtrado['tipo_bolsa'] == 'PARCIAL']):,}"
        total_ies = f"{df_filtrado['nome_ies'].nunique():,}"
        
        # Gráfico de evolução por ano
        evolucao = df_filtrado.groupby('ano_concessao').size().reset_index(name='quantidade')
        fig_evolucao = px.line(
            evolucao, 
            x='ano_concessao', 
            y='quantidade',
            markers=True,
            title='',
            labels={'ano_concessao': 'Ano', 'quantidade': 'Quantidade de Bolsas'}
        )
        fig_evolucao.update_traces(line_color='#1f77b4', marker_size=10)
        fig_evolucao.update_layout(hovermode='x unified')
        
        # Gráfico por estado
        estados = df_filtrado['uf_beneficiario'].value_counts().head(15).reset_index()
        estados.columns = ['uf', 'quantidade']
        fig_estados = px.bar(
            estados,
            x='quantidade',
            y='uf',
            orientation='h',
            title='',
            labels={'uf': 'Estado', 'quantidade': 'Quantidade de Bolsas'},
            color='quantidade',
            color_continuous_scale='Blues'
        )
        fig_estados.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
        
        # Gráfico de cursos
        cursos = df_filtrado['nome_curso'].value_counts().head(15).reset_index()
        cursos.columns = ['curso', 'quantidade']
        fig_cursos = px.bar(
            cursos,
            x='quantidade',
            y='curso',
            orientation='h',
            title='',
            labels={'curso': 'Curso', 'quantidade': 'Quantidade'},
            color='quantidade',
            color_continuous_scale='Greens'
        )
        fig_cursos.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
        
        # Gráfico de tipo de bolsa
        tipo_bolsa_count = df_filtrado['tipo_bolsa'].value_counts().reset_index()
        tipo_bolsa_count.columns = ['tipo', 'quantidade']
        fig_tipo_bolsa = px.pie(
            tipo_bolsa_count,
            values='quantidade',
            names='tipo',
            title='',
            color_discrete_sequence=['#2ecc71', '#f39c12']
        )
        fig_tipo_bolsa.update_traces(textposition='inside', textinfo='percent+label')
        
        # Preparar dados para tabela
        colunas_tabela = ['ano_concessao', 'uf_beneficiario', 'nome_ies', 
                         'nome_curso', 'tipo_bolsa', 'modalidade_ensino']
        dados_tabela = df_filtrado[colunas_tabela].head(100).to_dict('records')
        
        return (
            total_bolsas, total_integral, total_parcial, total_ies,
            fig_evolucao, fig_estados, fig_cursos, fig_tipo_bolsa,
            dados_tabela
        )

# ============================================================================
# EXECUTAR APLICAÇÃO
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Iniciando Dashboard ProUni")
    print("="*60)
    print("📍 Acesse o dashboard em: http://localhost:8050")
    print("⚠️  Pressione CTRL+C para encerrar")
    print("="*60 + "\n")
    
    app.run(debug=True, port=8050)
