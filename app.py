import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho do arquivo CSV
file_path = "INFLUD24-CE.csv"

try:
    df = pd.read_csv(file_path)

    # Dicionários de Substituição dos Dados
    substituicoes = {
        "VACINA": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "VACINA_COV": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "HOSPITAL": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "UTI": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "EVOLUCAO": {1: "Cura", 2: "Óbito", 3: "Óbito por outras causas", 9: "Ignorado"},
        "CLASSI_FIN": {
            1: "SRAG por influenza",
            2: "SRAG por outro vírus respiratório",
            3: "SRAG por outro agente etiológico",
            4: "SRAG não especificado",
            5: "SRAG por covid-19",
        },
        "AMOSTRA": {1: "Sim", 2: "Não", 9: "Ignorado"},
        "PCR_RESUL": {
            1: "Detectável",
            2: "Não Detectável",
            3: "Inconclusivo",
            4: "Não Realizado",
            5: "Aguardando Resultado",
            9: "Ignorado",
        },
        "PCR_ADENO": {1: "Marcado", 0: "Não Marcado"},
        "PCR_BOCA": {1: "Marcado", 0: "Não Marcado"},
        "PCR_METAP": {1: "Marcado", 0: "Não Marcado"},
        "PCR_RINO": {1: "Marcado", 0: "Não Marcado"},
        "PCR_PARA1": {1: "Marcado", 0: "Não Marcado"},
        "PCR_PARA2": {1: "Marcado", 0: "Não Marcado"},
        "PCR_PARA3": {1: "Marcado", 0: "Não Marcado"},
        "PCR_PARA4": {1: "Marcado", 0: "Não Marcado"},
        "PCR_SARS2": {1: "Marcado", 0: "Não Marcado"},
        "PCR_VSR": {1: "Marcado", 0: "Não Marcado"},
        "PCR_OUTRO": {1: "Marcado", 0: "Não Marcado"},
        "RES_AN": {
            1: "Positivo",
            2: "Negativo",
            3: "Inconclusivo",
            4: "Não Realizado",
            5: "Aguardando Resultado",
            9: "Ignorado",
        },
        "AN_ADENO": {1: "Marcado", 0: "Não Marcado"},
        "AN_PARA1": {1: "Marcado", 0: "Não Marcado"},
        "AN_PARA2": {1: "Marcado", 0: "Não Marcado"},
        "AN_PARA3": {1: "Marcado", 0: "Não Marcado"},
        "AN_SARS2": {1: "Marcado", 0: "Não Marcado"},
        "AN_VSR": {1: "Marcado", 0: "Não Marcado"},
        "AN_OUTRO": {1: "Marcado", 0: "Não Marcado"},
        "CRITERIO": {
            1: "Laboratorial",
            2: "Clínico Epidemiológico",
            3: "Clínico",
            4: "Clínico Imagem",
        },
        "TP_IDADE": {1: "Dia", 2: "Mês", 3: "Ano"},
        "CS_SEXO": {1: "Masculino", 2: "Feminino", 9: "Ignorado"},
    }

    # Aplicando as Substituições no DataFrame
    df.replace(substituicoes, inplace=True)

    # Substituindo Valores Nulos nas Colunas numéricas por 0
    df[df.select_dtypes(include=['number']).columns] = df.select_dtypes(
        include=['number']).fillna(0)
    
    # Substituindo Valores Nulos nas Colunas de Tipo Objeto por "Indefinido"
    df[df.select_dtypes(include=['object']).columns] = df.select_dtypes(
        include=['object']).fillna("Indefinido")

    # Substituindo Valores float por int
    df[df.select_dtypes(include=['float']).columns] = df.select_dtypes(
        include=['float']).astype('int')

    # Filtrando as linhas onde SG_UF_NOT é igual a 'CE'
    df_filtrado_regional = df.loc[df['ID_REGIONA']
                                  == '12 CRES ACARAU'].reset_index(drop=True)

    # Criando nova coluna 'QTD_HAT' com as quantidades de habitantes das cidades
    habitantes = {
        'BELA CRUZ': 32775,
        'CRUZ': 29761,
        'ACARAU': 64806
    }

    df_filtrado_regional['QTD_HAT'] = df_filtrado_regional['ID_MUNICIP'].map(
        habitantes)

    # Título do Painel
    st.title("Painel de Indicadores")

    if st.checkbox("Exibir Indicadores Epidemiológicos"):

        # Lista de Colunas a Manter para Epidemiológicos
        colunas_para_manter = [
            'ID_MUNICIP', 'CLASSI_FIN', 'CRITERIO', 'NU_IDADE_N', 'CS_SEXO',
            'VACINA', 'VACINA_COV', 'SEM_PRI', 'QTD_HAT'
        ]

        df_filtrado_Epidemiologicos = df_filtrado_regional[colunas_para_manter]

        # Contar as ocorrências de cada valor em 'ID_MUNICIP'
        municipios_count = df_filtrado_Epidemiologicos['ID_MUNICIP'].value_counts()

        # Definindo as faixas etárias Jovens (0-19), Adultos (20-59), Idosos (60+)
        bins = [0, 19, 59, 150]
        labels = ['Jovens', 'Adultos', 'Idosos']

        # Criando a nova coluna com a faixa etária
        df_filtrado_Epidemiologicos['FAIXA_ETARIA'] = pd.cut(
            df_filtrado_Epidemiologicos['NU_IDADE_N'], bins=bins, labels=labels)

        st.write('Casos de Gripe por Município')

        # Criando o gráfico (Casos de Gripe por Município)
        fig, ax = plt.subplots(figsize=(12, 6))
        municipios_count.plot(kind='bar', color='#377eb8', ax=ax)

        fig.patch.set_alpha(0) 
        ax.set_facecolor('none')

        ax.set_title('Casos de Gripe por Município', fontsize=16)
        ax.set_xlabel('Município')
        ax.set_ylabel('Quantidade de Casos')
        ax.set_xticklabels(municipios_count.index, rotation=20)

        st.pyplot(fig)

        # Calculando a Taxa de incidência por habitantes
        municipios = ['CRUZ', 'BELA CRUZ', 'ACARAU']
        incid_hab = [(215 / 29761), (113 / 32775), (2 / 64806)]

        df_indid_hab = pd.DataFrame({
            'MUNICIPIO': municipios,
            'INCIDENCIA POR HABITANTE': incid_hab
        })

        st.write('Taxa de incidência por habitantes')
        
        # Criando o gráfico ('Taxa de incidência por habitantes')
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(municipios, incid_hab, color='#377eb8')

        fig.patch.set_alpha(0)  
        ax.set_facecolor('none')

        # Configurar títulos e rótulos
        ax.set_title('Taxa de incidência por habitantes.', fontsize=16)
        ax.set_xlabel('Município', fontsize=12)
        ax.set_ylabel('Incidência por Habitante', fontsize=12)
        ax.tick_params(axis='x', rotation=20)  # Rotacionar os rótulos do eixo x

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

        st.write('Casos de Gripe por Sexo e Local da Residência')

        # Criando gráfico (Casos de Gripe por Sexo e Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_Epidemiologicos, 
                    x='ID_MUNICIP', hue='CS_SEXO', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)  
        ax.set_facecolor('none')  

        ax.set_title('Casos de Gripe por Sexo e Local da Residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade de Casos')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Sexo', frameon=False)

        st.pyplot(fig)

        st.write('Casos de Gripe por Faixa Etária e Local da Residência')

        # Criando o gráfico (Casos de Gripe por Faixa Etária e Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_Epidemiologicos, 
                    x='ID_MUNICIP', hue='FAIXA_ETARIA', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)  
        ax.set_facecolor('none')

        ax.set_title('Casos de Gripe por Faixa Etária e Local da Residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade de Casos')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Faixa Etária', frameon=False)

        st.pyplot(fig)

        st.write('Vacinação por local da residência')

        # Criando o gráfico (Vacinação por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_Epidemiologicos, 
                    x='ID_MUNICIP', hue='VACINA', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Vacinação por local da residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade Pessoas Vacidas')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Vacinação', frameon=False)

        st.pyplot(fig)

        st.write('Vacinação de COVID por local da residência')

        # Criando o gráfico (Vacinação de COVID por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_Epidemiologicos, 
                    x='ID_MUNICIP', hue='VACINA_COV', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Vacinação de COVID por local da residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade Pessoas Vacidas contra COVID')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Vacinação contra COVID', frameon=False)

        st.pyplot(fig)

        # Filtrando os dados para a cidade 'CRUZ'
        df_cruz = df_filtrado_Epidemiologicos[df_filtrado_Epidemiologicos['ID_MUNICIP'] == 'CRUZ']

        st.write('Casos de Gripe por Semana Epidemiológica Cruz (1 até 52)')

        # Criando gráfico (Casos de Gripe por Semana Epidemiológica Cruz (1 até 52))
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_cruz, 
                    x='ID_MUNICIP', hue='SEM_PRI', palette='Set1', ax=ax, legend=False)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Casos de Gripe por Semana Epidemiológica Cruz (1 até 52)', fontsize=16)
        ax.set_xlabel('Semana Epidemiológica')
        ax.set_ylabel('Quantidade de Casos')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)

        st.pyplot(fig)

        # Filtrando os dados para a cidade 'BELA CRUZ'
        df_belacruz = df_filtrado_Epidemiologicos[df_filtrado_Epidemiologicos['ID_MUNICIP'] == 'BELA CRUZ']

        st.write('Casos de Gripe por Semana Epidemiológica Bela Cruz (1 até 52)')

        # Criando gráfico (Casos de Gripe por Semana Epidemiológica (1 até 52))
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_belacruz, 
                    x='ID_MUNICIP', hue='SEM_PRI', palette='Set1', ax=ax, legend=False)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Casos de Gripe por Semana Epidemiológica Bela Cruz (1 até 52)', fontsize=16)
        ax.set_xlabel('Semana Epidemiológica')
        ax.set_ylabel('Quantidade de Casos')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)

        st.pyplot(fig)

        # Filtrando os dados para a cidade 'CRUZ'
        df_acarau = df_filtrado_Epidemiologicos[df_filtrado_Epidemiologicos['ID_MUNICIP'] == 'ACARAU']

        st.write('Casos de Gripe por Semana Epidemiológica Acaraú (1 até 52)')

        # Criando gráfico (Casos de Gripe por Semana Epidemiológica (1 até 52))
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_acarau, 
                    x='ID_MUNICIP', hue='SEM_PRI', palette='Set1', ax=ax, legend=False)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Casos de Gripe por Semana Epidemiológica Acaraú (1 até 52)', fontsize=16)
        ax.set_xlabel('Semana Epidemiológica')
        ax.set_ylabel('Quantidade de Casos')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)

        st.pyplot(fig)





    # Filtro de "Clínicos e Assistenciais"
    if st.checkbox("Exibir Indicadores Vigilância Laboratorial"):   

        # Lista de colunas a manter para Vigilância Laboratorial 
        colunas_para_manter = [
            'ID_MUNICIP', 'AMOSTRA', 'PCR_RESUL', 'RES_AN',
            'DT_COLETA', 'DT_PCR', 'DT_RES_AN'
        ]

        df_filtrado_vig_lab = df_filtrado_regional[colunas_para_manter]

        # Converte as colunas para o tipo datetime
        df_filtrado_vig_lab['DT_COLETA'] = pd.to_datetime(
            df_filtrado_vig_lab['DT_COLETA'], errors='coerce', format='%d/%m/%Y')
        df_filtrado_vig_lab['DT_PCR'] = pd.to_datetime(
            df_filtrado_vig_lab['DT_PCR'], errors='coerce', format='%d/%m/%Y')

        # Subtração das datas
        df_filtrado_vig_lab['DIFERENCA'] = df_filtrado_vig_lab['DT_PCR'] - df_filtrado_vig_lab['DT_COLETA']

        df_filtrado_vig_lab['DIFERENCA'] = df_filtrado_vig_lab['DIFERENCA'].dt.days

        st.write('Testes Realizados por Município')

        # Criando o gráfico (Testes Realizados por Município)
        fig, ax = plt.subplots(figsize=(12, 6))
        municipios_count.plot(kind='bar', color='#377eb8', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Testes Realizados por Município', fontsize=16)
        ax.set_xlabel('Município')
        ax.set_ylabel('Quantidade de Casos')
        ax.set_xticklabels(municipios_count.index, rotation=20)

        st.pyplot(fig)

        st.write('Resultado do Teste de RT-PCR por Local da Residência')

        # Criando gráfico (Resultado do Teste de RT-PCR por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_vig_lab, 
                    x='ID_MUNICIP', hue='PCR_RESUL', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Resultado do Teste de RT-PCR por Local da Residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade de Teste de RT-PCR')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Resultado do Teste de RT-PCR', frameon=False)

        st.pyplot(fig)

        st.write('Resultado do Teste Antigênico por Local da Residência')

        # Criando gráfico (Resultado do Teste Antigênico por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_vig_lab, 
                    x='ID_MUNICIP', hue='RES_AN', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Resultado do Teste Antigênico por Local da Residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade de Teste de Antigênico')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Resultado do Teste de Antigênico', frameon=False)

        st.pyplot(fig)

        diferenca_coleta_PCR = df_filtrado_vig_lab.groupby('ID_MUNICIP')['DIFERENCA'].mean().round()

        st.write('Tempo Médio entre Coleta e Resultado')

        # Criando o gráfico (Tempo Médio entre Coleta e Resultado)
        fig, ax = plt.subplots(figsize=(12, 6))
        diferenca_coleta_PCR.plot(kind='bar', color='#377eb8', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Tempo Médio entre Coleta e Resultado', fontsize=16)
        ax.set_xlabel('Município')
        ax.set_ylabel('Diferença de Dias')
        ax.set_xticklabels(diferenca_coleta_PCR.index, rotation=20)

        st.pyplot(fig)





    # Filtro de "Mortalidade"
    if st.checkbox("Exibir Indicadores de Mortalidade"):

        # Lista de colunas a manter para Mortalidade
        colunas_para_manter = [
            'ID_MUNICIP', 'CLASSI_FIN', 'EVOLUCAO'
        ]

        df_filtrado_mortalidade = df_filtrado_regional[colunas_para_manter]

        st.write('Desfechos Clínicos por Local da Residência')

        # Criando gráfico (Desfechos Clínicos por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_mortalidade, 
                    x='ID_MUNICIP', hue='EVOLUCAO', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Desfechos Clínicos por Local da Residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade de Cura, Óbito...')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Desfechos Clínicos', frameon=False)

        st.pyplot(fig)

        st.write('Número de óbitos Confirmados')

        # Filtrar dados de óbitos
        obito = df_filtrado_mortalidade.loc[
            (df_filtrado_mortalidade['EVOLUCAO'] == 'Óbito') | 
            (df_filtrado_mortalidade['EVOLUCAO'] == 'Óbito por outras causas')
        ]
        st.write(obito)





    # Filtro de "Clínicos e Assistenciais"
    if st.checkbox("Exibir Indicadores de Vacinação e Tempo de Resposta"):

        # Lista de colunas a manter para Clínicos e Assistenciais
        colunas_para_manter = [
            'ID_MUNICIP', 'HOSPITAL', 'UTI', 'EVOLUCAO'
        ]

        df_filtrado_clinico_assistencia = df_filtrado_regional[colunas_para_manter]

        st.write('Taxa de hospitalização por Local da Residência')

        # Criando gráfico (Taxa de hospitalização por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_clinico_assistencia, 
                    x='ID_MUNICIP', hue='HOSPITAL', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Taxa de hospitalização por Local da Residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade de hospitalização')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Taxa de hospitalização', frameon=False)

        st.pyplot(fig)

        st.write('Taxa de hospitalização em UTI por Local da Residência')

        # Criando gráfico (Taxa de hospitalização em UTI por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_clinico_assistencia, 
                    x='ID_MUNICIP', hue='UTI', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Taxa de hospitalização em UTI por Local da Residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade de hospitalização em UTI')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Taxa de hospitalização em UTI', frameon=False)

        st.pyplot(fig)

        st.write('Desfechos Clínicos por Local da Residência')

        # Criando gráfico (Desfechos Clínicos por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_clinico_assistencia, 
                    x='ID_MUNICIP', hue='EVOLUCAO', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Desfechos Clínicos por Local da Residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade de Cura, Óbito...')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Desfechos Clínicos', frameon=False)

        st.pyplot(fig)






    # Filtro de "Clínicos e Assistenciais"
    if st.checkbox("Exibir Indicadores Clínicos e Assistenciais"):

        # Lista de colunas a manter para Clínicos e Assistenciais
        colunas_para_manter = [
            'ID_MUNICIP', 'VACINA', 'VACINA_COV', 'DT_SIN_PRI', 'DT_NOTIFIC'
        ]

        df_filtrado_vacinacao_resposta = df_filtrado_regional[colunas_para_manter]

        st.write('Vacinação por local da residência')

        # Criando gráfico (Vacinação por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_vacinacao_resposta, 
                    x='ID_MUNICIP', hue='VACINA', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Vacinação por local da residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade Pessoas Vacidas')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Vacinação', frameon=False)

        st.pyplot(fig)

        st.write('Vacinação de COVID por local da residência')

        # Criando o gráfico (Vacinação de COVID por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(data=df_filtrado_vacinacao_resposta, 
                    x='ID_MUNICIP', hue='VACINA_COV', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_title('Vacinação de COVID por local da residência', fontsize=16)
        ax.set_xlabel('Local da Residência (Cidade)')
        ax.set_ylabel('Quantidade Pessoas Vacidas contra COVID')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
        ax.legend(title='Vacinação contra COVID', frameon=False)

        st.pyplot(fig)

        # Converte as colunas para o tipo datetime
        df_filtrado_vacinacao_resposta['DT_SIN_PRI'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_SIN_PRI'], errors='coerce', format='%d/%m/%Y')
        df_filtrado_vacinacao_resposta['DT_NOTIFIC'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_NOTIFIC'], errors='coerce', format='%d/%m/%Y')

        # Subtração das datas
        df_filtrado_vacinacao_resposta['DIFERENCA'] = df_filtrado_vacinacao_resposta['DT_NOTIFIC'] - \
            df_filtrado_vacinacao_resposta['DT_SIN_PRI']

        # Converte a diferença para o formato inteiro de dias
        df_filtrado_vacinacao_resposta['DIFERENCA'] = df_filtrado_vacinacao_resposta['DIFERENCA'].dt.days

        diferenca_NOTIFIC_SIN_PRI = df_filtrado_vacinacao_resposta.groupby(
            'ID_MUNICIP')['DIFERENCA'].mean().round()
        
        st.write('Tempo Médio de Sintomas até a Notificação')

        # Criando o gráfico (Tempo Médio de Sintomas até a Notificação)
        fig, ax = plt.subplots(figsize=(12, 6))
        diferenca_NOTIFIC_SIN_PRI.plot(kind='bar', color='#377eb8', ax=ax)

        fig.patch.set_alpha(0)  
        ax.set_facecolor('none')    
        
        ax.set_title('Tempo Médio de Sintomas até a Notificação', fontsize=16)
        ax.set_xlabel('Município')
        ax.set_ylabel('Diferença de Dias')
        ax.set_xticklabels(diferenca_NOTIFIC_SIN_PRI.index, rotation=20)

        st.pyplot(fig)

except FileNotFoundError:
    st.error(f"O arquivo no caminho '{
             file_path}' não foi encontrado. Verifique o caminho e tente novamente.")
