"""
Dashboard ProUni - Aplicação Principal

Dashboard interativo para análise dos dados do Programa Universidade para Todos (ProUni).
Permite exploração interativa dos dados de bolsas concedidas em 2018, 2019 e 2020.

Funcionalidades:
- Filtros interativos por ano, região, UF, tipo de bolsa e modalidade
- Métricas principais em tempo real
- Análise geográfica com mapas e gráficos
- Análise de cursos e instituições
- Perfil demográfico dos beneficiários
- Análise temporal comparativa

Autor: João Victor Costa Andrade
Data: Outubro 2025
"""

import dash
from dash import dcc, html
import sys
import os

# Adicionar o diretório src ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importar componentes do dashboard
from src.dashboard.layout import criar_layout_principal
from src.dashboard import callbacks

# Configurar a aplicação Dash
app = dash.Dash(
    __name__,
    title="Dashboard ProUni - Análise de Bolsas 2018-2020",
    update_title="Carregando...",
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"},
        {"name": "description", "content": "Dashboard interativo para análise dos dados do ProUni 2018-2020"},
        {"name": "author", "content": "João Victor Costa Andrade"},
        {"name": "keywords", "content": "ProUni, bolsas, educação, dashboard, análise, dados"}
    ]
)

# Configurar o servidor
server = app.server

# Suprimir callbacks de exceção para desenvolvimento
app.config.suppress_callback_exceptions = True

# Definir o layout da aplicação
app.layout = criar_layout_principal()

def verificar_dados():
    """Verifica se os dados processados existem"""
    
    import os
    
    arquivos_dados = [
        'data/processed/prouni_2018_2019_2020_processado.parquet',
        'data/processed/prouni_2018_2019_2020_processado.csv'
    ]
    
    for arquivo in arquivos_dados:
        if os.path.exists(arquivo):
            print(f"✅ Arquivo de dados encontrado: {arquivo}")
            return True
    
    print("❌ Nenhum arquivo de dados processado encontrado!")
    print("Execute primeiro o script de limpeza de dados:")
    print("python src/data_processing/clean_data.py")
    return False

def main():
    """Função principal para executar o dashboard"""
    
    print("🚀 INICIANDO DASHBOARD PROUNI")
    print("="*50)
    
    # Verificar se os dados existem
    if not verificar_dados():
        print("\\nPor favor, execute o processamento dos dados primeiro.")
        return
    
    # Configurações do servidor
    debug_mode = False  # Desabilitado para evitar recarregamentos
    host = '127.0.0.1'  # Localhost
    port = 8050
    
    print(f"\\n🌐 Dashboard disponível em: http://{host}:{port}")
    print("\\n📊 Funcionalidades disponíveis:")
    print("  • Filtros interativos por ano, região, UF, tipo de bolsa e modalidade")
    print("  • Métricas principais em tempo real")
    print("  • Análise geográfica detalhada")
    print("  • Top cursos e instituições")
    print("  • Perfil demográfico dos beneficiários")
    print("  • Análise temporal comparativa")
    
    print("\\n💡 Dicas de uso:")
    print("  • Use os filtros no topo para segmentar os dados")
    print("  • Navegue pelas abas para diferentes análises")
    print("  • Gráficos são interativos - clique, zoom e explore!")
    print("  • Pressione Ctrl+C para encerrar o servidor")
    
    print("\\n" + "="*50)
    
    try:
        # Executar o servidor
        app.run(
            debug=debug_mode,
            host=host,
            port=port,
            dev_tools_hot_reload=False,  # Desabilitar hot reload
            dev_tools_ui=False,          # Desabilitar UI de desenvolvimento
            threaded=True
        )
    except KeyboardInterrupt:
        print("\\n\\n🛑 Dashboard encerrado pelo usuário")
    except Exception as e:
        print(f"\\n❌ Erro ao executar dashboard: {e}")
        print("\\nVerifique se:")
        print("  • A porta 8050 não está sendo usada por outro processo")
        print("  • Os dados processados existem")
        print("  • Todas as dependências estão instaladas")

if __name__ == "__main__":
    main()