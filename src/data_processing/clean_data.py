"""
Script para limpeza e padronização dos dados do ProUni

Este script faz:
1. Padronização dos nomes das colunas entre 2019 e 2020
2. Limpeza de dados inconsistentes
3. Conversão de tipos de dados
4. Unificação dos datasets
5. Salvamento dos dados processados

Autor: João Victor Costa Andrade
Data: Outubro 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def carregar_dados():
    """Carrega os dados do ProUni de 2019 e 2020 com tratamento de encoding"""
    
    print("🔄 Carregando dados...")
    
    # Carregar dados de 2019
    try:
        df_2019 = pd.read_csv('data/raw/pda-prouni-2019.csv', encoding='utf-8', sep=';')
        print(f"✅ ProUni 2019: {df_2019.shape[0]:,} registros carregados")
    except Exception as e:
        print(f"❌ Erro ao carregar dados de 2019: {e}")
        return None, None
    
    # Carregar dados de 2020
    try:
        df_2020 = pd.read_csv('data/raw/ProuniRelatorioDadosAbertos2020.csv', encoding='latin-1', sep=';')
        print(f"✅ ProUni 2020: {df_2020.shape[0]:,} registros carregados")
    except Exception as e:
        print(f"❌ Erro ao carregar dados de 2020: {e}")
        return None, None
    
    return df_2019, df_2020

def padronizar_colunas(df_2019, df_2020):
    """Padroniza os nomes das colunas entre os datasets de diferentes anos"""
    
    print("🔄 Padronizando nomes das colunas...")
    
    # Mapeamento de colunas para padronização
    # As colunas serão renomeadas para um padrão comum
    
    # Colunas padrão que queremos ter no dataset final
    colunas_padrao = {
        # Informações da bolsa
        'ano_concessao': 'ANO_CONCESSAO_BOLSA',
        'codigo_ies': 'CODIGO_EMEC_IES_BOLSA', 
        'nome_ies': 'NOME_IES_BOLSA',
        'municipio_ies': None,  # Não existe em 2019
        'campus': None,  # Não existe em 2019
        'tipo_bolsa': 'TIPO_BOLSA',
        'modalidade_ensino': 'MODALIDADE_ENSINO_BOLSA',
        'nome_curso': 'NOME_CURSO_BOLSA',
        'turno': 'NOME_TURNO_CURSO_BOLSA',
        
        # Informações do beneficiário
        'cpf_beneficiario': None,  # Precisa padronizar entre os anos
        'sexo_beneficiario': None,  # Precisa padronizar entre os anos
        'raca_beneficiario': None,  # Precisa padronizar entre os anos
        'data_nascimento': None,  # Precisa padronizar entre os anos
        'deficiente_fisico': 'BENEFICIARIO_DEFICIENTE_FISICO',
        'regiao_beneficiario': None,  # Precisa padronizar entre os anos
        'uf_beneficiario': None,  # Precisa padronizar entre os anos
        'municipio_beneficiario': None  # Precisa padronizar entre os anos
    }
    
    # Renomear colunas no dataset de 2019
    renomeacao_2019 = {
        'ANO_CONCESSAO_BOLSA': 'ano_concessao',
        'CODIGO_EMEC_IES_BOLSA': 'codigo_ies',
        'NOME_IES_BOLSA': 'nome_ies',
        'TIPO_BOLSA': 'tipo_bolsa',
        'MODALIDADE_ENSINO_BOLSA': 'modalidade_ensino',
        'NOME_CURSO_BOLSA': 'nome_curso',
        'NOME_TURNO_CURSO_BOLSA': 'turno',
        'CPF_BENEFICIARIO_BOLSA': 'cpf_beneficiario',
        'SEXO_BENEFICIARIO_BOLSA': 'sexo_beneficiario',
        'RACA_BENEFICIARIO_BOLSA': 'raca_beneficiario',
        'DT_NASCIMENTO_BENEFICIARIO': 'data_nascimento',
        'BENEFICIARIO_DEFICIENTE_FISICO': 'deficiente_fisico',
        'REGIAO_BENEFICIARIO_BOLSA': 'regiao_beneficiario',
        'SIGLA_UF_BENEFICIARIO_BOLSA': 'uf_beneficiario',
        'MUNICIPIO_BENEFICIARIO_BOLSA': 'municipio_beneficiario'
    }
    
    # Renomear colunas no dataset de 2020
    renomeacao_2020 = {
        'ANO_CONCESSAO_BOLSA': 'ano_concessao',
        'CODIGO_EMEC_IES_BOLSA': 'codigo_ies',
        'NOME_IES_BOLSA': 'nome_ies',
        'MUNICIPIO': 'municipio_ies',
        'CAMPUS': 'campus',
        'TIPO_BOLSA': 'tipo_bolsa',
        'MODALIDADE_ENSINO_BOLSA': 'modalidade_ensino',
        'NOME_CURSO_BOLSA': 'nome_curso',
        'NOME_TURNO_CURSO_BOLSA': 'turno',
        'CPF_BENEFICIARIO': 'cpf_beneficiario',
        'SEXO_BENEFICIARIO': 'sexo_beneficiario',
        'RACA_BENEFICIARIO': 'raca_beneficiario',
        'DATA_NASCIMENTO': 'data_nascimento',
        'BENEFICIARIO_DEFICIENTE_FISICO': 'deficiente_fisico',
        'REGIAO_BENEFICIARIO': 'regiao_beneficiario',
        'UF_BENEFICIARIO': 'uf_beneficiario',
        'MUNICIPIO_BENEFICIARIO': 'municipio_beneficiario'
    }
    
    # Aplicar renomeações
    df_2019_padronizado = df_2019.rename(columns=renomeacao_2019).copy()
    df_2020_padronizado = df_2020.rename(columns=renomeacao_2020).copy()
    
    # Adicionar colunas que não existem em 2019
    df_2019_padronizado['municipio_ies'] = None
    df_2019_padronizado['campus'] = None
    
    print("✅ Colunas padronizadas com sucesso")
    
    return df_2019_padronizado, df_2020_padronizado

def limpar_dados(df):
    """Limpa e padroniza os dados"""
    
    print(f"🔄 Limpando dados... (Shape inicial: {df.shape})")
    
    # 1. Converter ano para inteiro
    df['ano_concessao'] = pd.to_numeric(df['ano_concessao'], errors='coerce').astype('Int64')
    
    # 2. Padronizar tipo de bolsa
    df['tipo_bolsa'] = df['tipo_bolsa'].str.upper().str.strip()
    df['tipo_bolsa'] = df['tipo_bolsa'].replace({
        'BOLSA INTEGRAL': 'INTEGRAL',
        'BOLSA PARCIAL': 'PARCIAL'
    })
    
    # 3. Padronizar modalidade de ensino
    df['modalidade_ensino'] = df['modalidade_ensino'].str.upper().str.strip()
    
    # 4. Padronizar sexo
    df['sexo_beneficiario'] = df['sexo_beneficiario'].str.upper().str.strip()
    
    # 5. Padronizar região
    df['regiao_beneficiario'] = df['regiao_beneficiario'].str.upper().str.strip()
    
    # 6. Padronizar UF
    df['uf_beneficiario'] = df['uf_beneficiario'].str.upper().str.strip()
    
    # 7. Limpar e padronizar nomes (remover acentos e espaços extras)
    colunas_texto = ['nome_ies', 'nome_curso', 'municipio_beneficiario', 'municipio_ies', 'campus']
    for col in colunas_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace('nan', None)
    
    # 8. Converter data de nascimento para datetime
    df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], errors='coerce', dayfirst=True)
    
    # 9. Criar coluna de idade aproximada
    ano_atual = datetime.now().year
    df['idade_aproximada'] = ano_atual - df['data_nascimento'].dt.year
    
    # 10. Padronizar deficiência física
    df['deficiente_fisico'] = df['deficiente_fisico'].str.upper().str.strip()
    df['deficiente_fisico'] = df['deficiente_fisico'].map({'S': True, 'N': False})
    
    print(f"✅ Dados limpos (Shape final: {df.shape})")
    
    return df

def unificar_datasets(df_2019, df_2020):
    """Unifica os datasets de diferentes anos"""
    
    print("🔄 Unificando datasets...")
    
    # Garantir que ambos tenham as mesmas colunas
    colunas_finais = [
        'ano_concessao', 'codigo_ies', 'nome_ies', 'municipio_ies', 'campus',
        'tipo_bolsa', 'modalidade_ensino', 'nome_curso', 'turno',
        'cpf_beneficiario', 'sexo_beneficiario', 'raca_beneficiario', 
        'data_nascimento', 'idade_aproximada', 'deficiente_fisico',
        'regiao_beneficiario', 'uf_beneficiario', 'municipio_beneficiario'
    ]
    
    # Selecionar apenas as colunas finais
    df_2019_final = df_2019[colunas_finais].copy()
    df_2020_final = df_2020[colunas_finais].copy()
    
    # Unificar
    df_unificado = pd.concat([df_2019_final, df_2020_final], ignore_index=True)
    
    print(f"✅ Datasets unificados: {df_unificado.shape[0]:,} registros totais")
    
    return df_unificado

def gerar_estatisticas(df):
    """Gera estatísticas dos dados processados"""
    
    print("\\n" + "="*50)
    print("📊 ESTATÍSTICAS DOS DADOS PROCESSADOS")
    print("="*50)
    
    print(f"\\n📏 Dimensões: {df.shape[0]:,} registros x {df.shape[1]} colunas")
    
    print(f"\\n📅 Distribuição por ano:")
    print(df['ano_concessao'].value_counts().sort_index())
    
    print(f"\\n🎓 Distribuição por tipo de bolsa:")
    print(df['tipo_bolsa'].value_counts())
    
    print(f"\\n🏫 Distribuição por modalidade:")
    print(df['modalidade_ensino'].value_counts())
    
    print(f"\\n🗺️ Top 10 estados:")
    print(df['uf_beneficiario'].value_counts().head(10))
    
    print(f"\\n👥 Distribuição por sexo:")
    print(df['sexo_beneficiario'].value_counts())
    
    print(f"\\n🕳️ Dados faltantes por coluna:")
    nulos = df.isnull().sum()
    nulos_percent = (nulos / len(df)) * 100
    dados_faltantes = pd.DataFrame({
        'Valores_Nulos': nulos,
        'Percentual': nulos_percent.round(2)
    })
    dados_faltantes = dados_faltantes[dados_faltantes['Valores_Nulos'] > 0]
    print(dados_faltantes)

def main():
    """Função principal"""
    
    print("🚀 INICIANDO PROCESSAMENTO DOS DADOS DO PROUNI")
    print("="*50)
    
    # 1. Carregar dados
    df_2019, df_2020 = carregar_dados()
    if df_2019 is None or df_2020 is None:
        print("❌ Erro no carregamento dos dados. Encerrando...")
        return
    
    # 2. Padronizar colunas
    df_2019_padronizado, df_2020_padronizado = padronizar_colunas(df_2019, df_2020)
    
    # 3. Limpar dados
    df_2019_limpo = limpar_dados(df_2019_padronizado)
    df_2020_limpo = limpar_dados(df_2020_padronizado)
    
    # 4. Unificar datasets
    df_final = unificar_datasets(df_2019_limpo, df_2020_limpo)
    
    # 5. Gerar estatísticas
    gerar_estatisticas(df_final)
    
    # 6. Salvar dados processados
    print("\\n🔄 Salvando dados processados...")
    try:
        # Salvar como CSV
        df_final.to_csv('data/processed/prouni_2019_2020_processado.csv', index=False, encoding='utf-8')
        print("✅ Dados salvos em: data/processed/prouni_2019_2020_processado.csv")
        
        # Salvar também como Parquet (mais eficiente)
        df_final.to_parquet('data/processed/prouni_2019_2020_processado.parquet', index=False)
        print("✅ Dados salvos em: data/processed/prouni_2019_2020_processado.parquet")
        
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
    
    print("\\n🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("="*50)
    
    return df_final

if __name__ == "__main__":
    dados_processados = main()