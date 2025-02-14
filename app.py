import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho do arquivo CSV
file_path = "dados_combinados.csv"
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
    df_filtrado_regional = df

    # Título do Painel
    st.title("Painel de Indicadores")

    if st.checkbox("Exibir Indicadores Epidemiológicos - 2024"):

        # Lista de Colunas a Manter para Epidemiológicos
        colunas_para_manter = [
            'CLASSI_FIN', 'CRITERIO', 'NU_IDADE_N', 'CS_SEXO', 'SEM_PRI', 'ID_MN_RESI'
        ]

        df_filtrado_Epidemiologicos = df_filtrado_regional[colunas_para_manter]

        # Contar as ocorrências de cada valor em 'ID_MUNICIP'
        municipios_count = df_filtrado_Epidemiologicos['ID_MN_RESI'].value_counts(
        )

        municipio_CRUZ = municipios_count.index[0] 
        ocorrencia_CRUZ = municipios_count.iloc[0]  

        municipio_BELACRUZ = municipios_count.index[1]  
        ocorrencia_BELACRUZ = municipios_count.iloc[1]  

        municipio_ITAREMA = municipios_count.index[2]  
        ocorrencia_ITAREMA = municipios_count.iloc[2]  

        municipio_MARCO = municipios_count.index[3]  
        ocorrencia_MARCO = municipios_count.iloc[3]  

        municipio_ACARAU = municipios_count.index[4] 
        ocorrencia_ACARAU = municipios_count.iloc[4] 

        municipio_MORRINHOS = municipios_count.index[5]  
        ocorrencia_MORRINHOS = municipios_count.iloc[5]  

        municipio_JIJOCA = municipios_count.index[6]  
        ocorrencia_JIJOCA = municipios_count.iloc[6]  

        # Definindo as faixas etárias Jovens (0-19), Adultos (20-59), Idosos (60+)
        bins = [0, 19, 59, 150]
        labels = ['Jovens', 'Adultos', 'Idosos']

        # Criando a nova coluna com a faixa etária
        df_filtrado_Epidemiologicos['FAIXA_ETARIA'] = pd.cut(
            df_filtrado_Epidemiologicos['NU_IDADE_N'], bins=bins, labels=labels)

        
        st.write('Casos de Síndrome Respiratória Aguda Grave por Município')

        # Criando o gráfico (Casos de Gripe por Município)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = municipios_count.plot(kind='bar', color='#377eb8', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Município', color='grey')
        ax.set_ylabel('Quantidade de Casos', color='grey')
        ax.set_xticklabels(municipios_count.index, rotation=20, color='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write(f"""
        O Município de {municipio_CRUZ} teve {ocorrencia_CRUZ} Ocorrências de Síndrome Respiratória Aguda Grave.  
        O Município de {municipio_BELACRUZ} teve {ocorrencia_BELACRUZ} Ocorrências de Síndrome Respiratória Aguda Grave.  
        O Município de {municipio_ITAREMA} teve {ocorrencia_ITAREMA} Ocorrências de Síndrome Respiratória Aguda Grave.  
        O Município de {municipio_MARCO} teve {ocorrencia_MARCO} Ocorrências de Síndrome Respiratória Aguda Grave.  
        O Município de {municipio_ACARAU} teve {ocorrencia_ACARAU} Ocorrências de Síndrome Respiratória Aguda Grave.  
        O Município de {municipio_MORRINHOS} teve {ocorrencia_MORRINHOS} Ocorrências de Síndrome Respiratória Aguda Grave.  
        O Município de {municipio_JIJOCA} teve {ocorrencia_JIJOCA} Ocorrências de Síndrome Respiratória Aguda Grave.
        """)

        # Calculando a Taxa de incidência por habitantes
        municipios = ['ACARAU', 'BELA CRUZ', 'CRUZ', 'ITAREMA', 'JIJOCA', 'MARCO', 'MORRINHOS']
        incid_hab = [round((ocorrencia_ACARAU / 64806) * 100000, 2),
             round((ocorrencia_BELACRUZ / 32775) * 100000, 2),
             round((ocorrencia_CRUZ / 29761) * 100000, 2),
             round((ocorrencia_ITAREMA / 42957) * 100000, 2),
             round((ocorrencia_JIJOCA / 25555) * 100000, 2),
             round((ocorrencia_MARCO / 25799) * 100000, 2),
             round((ocorrencia_MORRINHOS / 22753) * 100000, 2)]

        df_indid_hab = pd.DataFrame({
            'MUNICIPIO': municipios,
            'TAXA DE INCIDÊNCIA': incid_hab
            
        })

        st.write('Taxa de incidência por 100.0000 habitantes')

        df_indid_hab

        st.write('Casos de Síndrome Respiratória Aguda Grave por Sexo e Local da Residência')

        # Criando gráfico (Casos de Gripe por Sexo e Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.countplot(data=df_filtrado_Epidemiologicos,
                            x='ID_MN_RESI', hue='CS_SEXO', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Local da Residência (Cidade)', color='grey')
        ax.set_ylabel('Quantidade de Casos', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.legend(title='Sexo', frameon=False, fontsize=12,
                title_fontsize='13', loc='upper right', labelcolor='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write('Casos de Síndrome Respiratória Aguda Grave por Faixa Etária e Local da Residência')

        # Criando o gráfico (Casos de Gripe por Faixa Etária e Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.countplot(data=df_filtrado_Epidemiologicos,
                      x='ID_MN_RESI', hue='FAIXA_ETARIA', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Local da Residência (Cidade)', color='grey')
        ax.set_ylabel('Quantidade de Casos', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.legend(title='Faixa Etária', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write('Casos por Semana Epidemiológica Geral (1 até 52)')

        # Exemplo de como pode ser feito, agrupando os dados pela semana epidemiológica
        df_filtrado_Semana_Epidemiologicos_geral = df_filtrado_Epidemiologicos.groupby('SEM_PRI').size().reset_index(name='quant_casos')

        # Plotando o gráfico geral
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.barplot(x='SEM_PRI', y='quant_casos', data=df_filtrado_Semana_Epidemiologicos_geral, palette='Set1', ax=ax, width=1.0)

        # Estilização do gráfico
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Semana Epidemiológica', color='grey')
        ax.set_ylabel('Quantidade de Casos', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')
        
        st.pyplot(fig)
        

    if st.checkbox("Exibir Indicadores Vigilância Laboratorial - 2024"):

        # Lista de colunas a manter para Vigilância Laboratorial
        colunas_para_manter = [
            'ID_MUNICIP', 'AMOSTRA', 'PCR_RESUL', 'RES_AN',
            'DT_COLETA', 'DT_PCR', 'DT_RES_AN', 'ID_MN_RESI'
        ]

        df_filtrado_vig_lab = df_filtrado_regional[colunas_para_manter]

        # Contar total de testes PCR por município
        total_pcr = df_filtrado_vig_lab.groupby('ID_MN_RESI')['PCR_RESUL'].count()

        # Contar testes PCR com resultado "Não Realizado" por município
        nao_realizado_pcr = df_filtrado_vig_lab[df_filtrado_vig_lab['PCR_RESUL'] == "Não Realizado"].groupby('ID_MN_RESI')['PCR_RESUL'].count()

        # Subtrair o total pelos testes "Não Realizado"
        resultado_final_pcr = total_pcr - nao_realizado_pcr

        municipio_CRUZ_pcr = resultado_final_pcr.index[0] 
        resultado_CRUZ_pcr = resultado_final_pcr.iloc[0]  

        municipio_BELACRUZ_pcr = resultado_final_pcr.index[1]  
        resultado_BELACRUZ_pcr = resultado_final_pcr.iloc[1]  

        municipio_ITAREMA_pcr = resultado_final_pcr.index[2]  
        resultado_ITAREMA_pcr = resultado_final_pcr.iloc[2]  

        municipio_MARCO_pcr = resultado_final_pcr.index[3]  
        resultado_MARCO_pcr = resultado_final_pcr.iloc[3]  

        municipio_ACARAU_pcr = resultado_final_pcr.index[4] 
        resultado_ACARAU_pcr = resultado_final_pcr.iloc[4] 

        municipio_MORRINHOS_pcr = resultado_final_pcr.index[5]  
        resultado_MORRINHOS_pcr = resultado_final_pcr.iloc[5]  

        municipio_JIJOCA_pcr = resultado_final_pcr.index[6]  
        resultado_JIJOCA_pcr = resultado_final_pcr.iloc[6] 


        # Contar total de testes Antigênico por município
        total_antigenico = df_filtrado_vig_lab.groupby('ID_MN_RESI')['RES_AN'].count()

        # Contar testes Antigênico com resultado "Não Realizado" por município
        nao_realizado_antigenico = df_filtrado_vig_lab[df_filtrado_vig_lab['RES_AN'] == "Não Realizado"]\
                                    .groupby('ID_MN_RESI')['RES_AN'].count()

        # Garantir que os municípios sem "Não Realizado" apareçam, preenchendo com 0
        nao_realizado_antigenico = nao_realizado_antigenico.reindex(total_antigenico.index, fill_value=0)

        # Subtrair o total pelos testes "Não Realizado"
        resultado_final_antigenico = total_antigenico - nao_realizado_antigenico


        municipio_CRUZ_antigenico = resultado_final_antigenico.index[0] 
        resultado_CRUZ_antigenico = resultado_final_antigenico.iloc[0]  

        municipio_BELACRUZ_antigenico = resultado_final_antigenico.index[1]  
        resultado_BELACRUZ_antigenico = resultado_final_antigenico.iloc[1]  

        municipio_ITAREMA_antigenico = resultado_final_antigenico.index[2]  
        resultado_ITAREMA_antigenico = resultado_final_antigenico.iloc[2]  

        municipio_MARCO_antigenico = resultado_final_antigenico.index[3]  
        resultado_MARCO_antigenico = resultado_final_antigenico.iloc[3]  

        municipio_ACARAU_antigenico = resultado_final_antigenico.index[4] 
        resultado_ACARAU_antigenico = resultado_final_antigenico.iloc[4] 

        municipio_MORRINHOS_antigenico = resultado_final_antigenico.index[5]  
        resultado_MORRINHOS_antigenico = resultado_final_antigenico.iloc[5]  

        municipio_JIJOCA_antigenico = resultado_final_antigenico.index[6]  
        resultado_JIJOCA_antigenico = resultado_final_antigenico.iloc[6] 

        st.write('Resultado do Teste de RT-PCR por Local da Residência')

        # Criando gráfico (Resultado do Teste de RT-PCR por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.countplot(data=df_filtrado_vig_lab,
                      x='ID_MN_RESI', hue='PCR_RESUL', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Local da Residência (Cidade)', color='grey')
        ax.set_ylabel('Quantidade de Teste de RT-PCR', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.legend(title='Resultado do Teste de RT-PCR', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write(f"""
        O Município de {municipio_ACARAU_pcr} teve {resultado_ACARAU_pcr} Testes de Antigênico Realizados.      
        O Município de {municipio_BELACRUZ_pcr} teve {resultado_BELACRUZ_pcr} Testes de Antigênico  Realizados.     
        O Município de {municipio_CRUZ_pcr} teve {resultado_CRUZ_pcr} Testes de Antigênico  Realizados.     
        O Município de {municipio_ITAREMA_pcr} teve {resultado_ITAREMA_pcr} Testes de Antigênico Realizados.        
        O Município de {municipio_JIJOCA_pcr} teve {resultado_JIJOCA_pcr} Testes de Antigênico Realizados.            
        O Município de {municipio_MARCO_pcr} teve {resultado_MARCO_pcr} Testes de Antigênico Realizados.        
        O Município de {municipio_MORRINHOS_pcr} teve {resultado_MORRINHOS_pcr} Testes de Antigênico Realizados.    
        """)
        
        st.write('Resultado do Teste Antigênico por Local da Residência')

        # Criando gráfico (Resultado do Teste Antigênico por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.countplot(data=df_filtrado_vig_lab,
                      x='ID_MN_RESI', hue='RES_AN', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Local da Residência (Cidade)', color='grey')
        ax.set_ylabel('Quantidade de Teste de Antigênico', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.legend(title='Resultado do Teste de Antigênico', frameon=False,
                  fontsize=12, title_fontsize='13', loc='upper right', labelcolor='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write(f"""
        O Município de {municipio_ACARAU_antigenico} teve {resultado_ACARAU_antigenico} Testes de Antigênico Realizados.        
        O Município de {municipio_BELACRUZ_antigenico} teve {resultado_BELACRUZ_antigenico} Testes de Antigênico  Realizados.       
        O Município de {municipio_CRUZ_antigenico} teve {resultado_CRUZ_antigenico} Testes de Antigênico  Realizados.         
        O Município de {municipio_ITAREMA_antigenico} teve {resultado_ITAREMA_antigenico} Testes de Antigênico Realizados.      
        O Município de {municipio_JIJOCA_antigenico} teve {resultado_JIJOCA_antigenico} Testes de Antigênico Realizados.           
        O Município de {municipio_MARCO_antigenico} teve {resultado_MARCO_antigenico} Testes de Antigênico Realizados.      
        O Município de {municipio_MORRINHOS_antigenico} teve {resultado_MORRINHOS_antigenico} Testes de Antigênico Realizados.        
        """)

    # Filtro de "Mortalidade"
    if st.checkbox("Exibir Indicadores de Mortalidade - 2024"):

        # Lista de colunas a manter para Mortalidade
        colunas_para_manter = [
            'ID_MUNICIP', 'CLASSI_FIN', 'EVOLUCAO', 'ID_MN_RESI'
        ]

        df_filtrado_mortalidade = df_filtrado_regional[colunas_para_manter]

        # Contar quantidade de óbitos por município
        total_obito = df_filtrado_mortalidade[df_filtrado_mortalidade['EVOLUCAO'].isin(["Óbito", "Óbito por outras causas"])]\
                .groupby('ID_MN_RESI')['EVOLUCAO'].count()

        # Preencher NaN com zero (caso algum município não tenha óbitos)
        resultado_final_obito = total_obito.fillna(0)

        municipio_CRUZ_obito = resultado_final_obito.index[2] 
        resultado_CRUZ_obito = resultado_final_obito.iloc[2]  

        municipio_BELACRUZ_obito = resultado_final_obito.index[1]  
        resultado_BELACRUZ_obito = resultado_final_obito.iloc[1]  

        municipio_ITAREMA_obito = resultado_final_obito.index[3]  
        resultado_ITAREMA_obito = resultado_final_obito.iloc[3]   

        municipio_ACARAU_obito = resultado_final_obito.index[0] 
        resultado_ACARAU_obito = resultado_final_obito.iloc[0] 

        municipio_MORRINHOS_obito = resultado_final_obito.index[5]  
        resultado_MORRINHOS_obito = resultado_final_obito.iloc[5]  

        municipio_JIJOCA_obito = resultado_final_obito.index[4]  
        resultado_JIJOCA_obito = resultado_final_obito.iloc[4] 
        
        st.write('Desfechos Clínicos por Local da Residência')

        # Criando gráfico (Desfechos Clínicos por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.countplot(data=df_filtrado_mortalidade,
                      x='ID_MN_RESI', hue='EVOLUCAO', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Local da Residência (Cidade)', color='grey')
        ax.set_ylabel('Quantidade de Cura, Óbito...', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.legend(title='Desfechos Clínicos', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write('Número de óbitos Confirmados por Síndrome Respiratória Aguda Grave ou por Ocorrência de Complicações: ')

        st.write(f"""
        O Município de {municipio_ACARAU_obito} teve {resultado_ACARAU_obito} Óbitos.        
        O Município de {municipio_BELACRUZ_obito} teve {resultado_BELACRUZ_obito} Óbitos.       
        O Município de {municipio_CRUZ_obito} teve {resultado_CRUZ_obito} Óbitos.         
        O Município de {municipio_ITAREMA_obito} teve {resultado_ITAREMA_obito} Óbitos.      
        O Município de {municipio_JIJOCA_obito} teve {resultado_JIJOCA_obito} Óbitos.           
        O Município de MARCO teve 0 Óbitos.           
        O Município de {municipio_MORRINHOS_obito} teve {resultado_MORRINHOS_obito} Óbitos.        
        """)

    # Filtro de "Clínicos e Assistenciais"
    if st.checkbox("Exibir Indicadores de Hospitalização e UTI - 2024"):

        # Lista de colunas a manter para Clínicos e Assistenciais
        colunas_para_manter = [
            'ID_MUNICIP', 'HOSPITAL', 'UTI', 'EVOLUCAO', 'ID_MN_RESI'
        ]

        df_filtrado_clinico_assistencia = df_filtrado_regional[colunas_para_manter]

        # Contando a quantidade de hospitalização
        hospitalizacao = df_filtrado_clinico_assistencia[df_filtrado_clinico_assistencia['HOSPITAL'] == "Sim"].groupby('ID_MN_RESI')['HOSPITAL'].count()
        total_casos_hospitalizacao = df_filtrado_clinico_assistencia.groupby('ID_MN_RESI')['HOSPITAL'].count()
        
        # Contando a quantidade de hospitalização em UTI
        uti = df_filtrado_clinico_assistencia[df_filtrado_clinico_assistencia['UTI'] == "Sim"].groupby('ID_MN_RESI')['UTI'].count()
        total_casos_uti = df_filtrado_clinico_assistencia.groupby('ID_MN_RESI')['UTI'].count()
    

        # Extraindo os índices e resultados
        municipio_CRUZ_hospitalizacao = hospitalizacao.index[2] 
        resultado_CRUZ_hospitalizacao = hospitalizacao.iloc[2]  
        resultado_CRUZ_total_casos_hospitalizacao = total_casos_hospitalizacao.iloc[2]  

        municipio_BELACRUZ_hospitalizacao = hospitalizacao.index[1]  
        resultado_BELACRUZ_hospitalizacao = hospitalizacao.iloc[1]  
        resultado_BELACRUZ_total_casos_hospitalizacao = total_casos_hospitalizacao.iloc[1]  

        municipio_ITAREMA_hospitalizacao = hospitalizacao.index[3]  
        resultado_ITAREMA_hospitalizacao = hospitalizacao.iloc[3]   
        resultado_ITAREMA_total_casos_hospitalizacao = total_casos_hospitalizacao.iloc[3]

        municipio_ACARAU_hospitalizacao = hospitalizacao.index[0] 
        resultado_ACARAU_hospitalizacao = hospitalizacao.iloc[0] 
        resultado_ACARAU_total_casos_hospitalizacao = total_casos_hospitalizacao.iloc[0]

        municipio_MORRINHOS_hospitalizacao = hospitalizacao.index[6]  
        resultado_MORRINHOS_hospitalizacao = hospitalizacao.iloc[6]
        resultado_MORRINHOS_total_casos_hospitalizacao = total_casos_hospitalizacao.iloc[6]  

        municipio_JIJOCA_hospitalizacao = hospitalizacao.index[4]  
        resultado_JIJOCA_hospitalizacao = hospitalizacao.iloc[4] 
        resultado_JIJOCA_total_casos_hospitalizacao = total_casos_hospitalizacao.iloc[4] 

        municipio_MARCO_hospitalizacao = hospitalizacao.index[5]  
        resultado_MARCO_hospitalizacao = hospitalizacao.iloc[5]  
        resultado_MARCO_total_casos_hospitalizacao = total_casos_hospitalizacao.iloc[5]  
        
        # Extraindo os índices e resultados
        municipio_CRUZ_uti = uti.index[2] 
        resultado_CRUZ_uti = uti.iloc[2]
        resultado_CRUZ_total_casos_uti = total_casos_uti.iloc[2]  

        municipio_BELACRUZ_uti = uti.index[1]  
        resultado_BELACRUZ_uti = uti.iloc[1]  
        resultado_BELACRUZ_total_casos_uti = total_casos_uti.iloc[1]

        municipio_ITAREMA_uti = uti.index[3]  
        resultado_ITAREMA_uti = uti.iloc[3]   
        resultado_ITAREMA_total_casos_uti = total_casos_uti.iloc[3]   

        municipio_ACARAU_uti = uti.index[0] 
        resultado_ACARAU_uti = uti.iloc[0] 
        resultado_ACARAU_total_casos_uti = total_casos_uti.iloc[0] 

        municipio_MORRINHOS_uti = uti.index[6]  
        resultado_MORRINHOS_uti = uti.iloc[6]   
        resultado_MORRINHOS_total_casos_uti = total_casos_uti.iloc[6]  

        municipio_JIJOCA_uti = uti.index[4]  
        resultado_JIJOCA_uti = uti.iloc[4] 
        resultado_JIJOCA_total_casos_uti = total_casos_uti.iloc[4] 

        municipio_MARCO_uti = uti.index[5]  
        resultado_MARCO_uti = uti.iloc[5]   
        resultado_MARCO_total_casos_uti = total_casos_uti.iloc[5]  
  
        percentual_ACARAU_hospitalizacao = round(((resultado_ACARAU_hospitalizacao / resultado_ACARAU_total_casos_hospitalizacao) * 100), 2)
        percentual_CRUZ_hospitalizacao = round(((resultado_CRUZ_hospitalizacao / resultado_CRUZ_total_casos_hospitalizacao) * 100), 2)
        percentual_ITAREMA_hospitalizacao = round(((resultado_ITAREMA_hospitalizacao / resultado_ITAREMA_total_casos_hospitalizacao) * 100), 2)
        percentual_BELACRUZ_hospitalizacao = round(((resultado_BELACRUZ_hospitalizacao / resultado_BELACRUZ_total_casos_hospitalizacao) * 100), 2)
        percentual_MORRINHOS_hospitalizacao = round(((resultado_MORRINHOS_hospitalizacao / resultado_MORRINHOS_total_casos_hospitalizacao) * 100), 2)
        percentual_MARCO_hospitalizacao = round(((resultado_MARCO_hospitalizacao / resultado_MARCO_total_casos_hospitalizacao) * 100), 2)
        percentual_JIJOCA_hospitalizacao = round(((resultado_JIJOCA_hospitalizacao / resultado_JIJOCA_total_casos_hospitalizacao) * 100), 2)

        percentual_ACARAU_uti = round(((resultado_ACARAU_uti / resultado_ACARAU_total_casos_uti) * 100), 2)
        percentual_CRUZ_uti = round(((resultado_CRUZ_uti / resultado_CRUZ_total_casos_uti) * 100), 2)
        percentual_ITAREMA_uti = round(((resultado_ITAREMA_uti / resultado_ITAREMA_total_casos_uti) * 100), 2)
        percentual_BELACRUZ_uti = round(((resultado_BELACRUZ_uti / resultado_BELACRUZ_total_casos_uti) * 100), 2)
        percentual_MORRINHOS_uti = round(((resultado_MORRINHOS_uti / resultado_MORRINHOS_total_casos_uti) * 100), 2)
        percentual_MARCO_uti = round(((resultado_MARCO_uti / resultado_MARCO_total_casos_uti) * 100), 2)
        percentual_JIJOCA_uti = round(((resultado_JIJOCA_uti / resultado_JIJOCA_total_casos_uti) * 100), 2)
        
        st.write('Taxa de hospitalização por Ocorrência de Complicações por Local da Residência')

        # Criando gráfico (Taxa de hospitalização por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.countplot(data=df_filtrado_clinico_assistencia,
                      x='ID_MN_RESI', hue='HOSPITAL', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Local da Residência (Cidade)', color='grey')
        ax.set_ylabel('Quantidade de hospitalização', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.legend(title='Taxa de hospitalização', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write(f"""
        O Município de {municipio_ACARAU_hospitalizacao} teve {resultado_ACARAU_hospitalizacao} Hospitalização, esses números representam {percentual_ACARAU_hospitalizacao}% do total de pacientes.                   
        O Município de {municipio_BELACRUZ_hospitalizacao} teve {resultado_BELACRUZ_hospitalizacao} Hospitalização, esses números representam {percentual_BELACRUZ_hospitalizacao}% do total de pacientes.                   
        O Município de {municipio_CRUZ_hospitalizacao} teve {resultado_CRUZ_hospitalizacao} Hospitalização, esses números representam {percentual_CRUZ_hospitalizacao}% do total de pacientes.                     
        O Município de {municipio_ITAREMA_hospitalizacao} teve {resultado_ITAREMA_hospitalizacao} Hospitalização, esses números representam {percentual_ITAREMA_hospitalizacao}% do total de pacientes.          
        O Município de {municipio_JIJOCA_hospitalizacao} teve {resultado_JIJOCA_hospitalizacao} Hospitalização, esses números representam {percentual_JIJOCA_hospitalizacao}% do total de pacientes.              
        O Município de {municipio_MARCO_hospitalizacao} teve {resultado_MARCO_hospitalizacao} Hospitalização, esses números representam {percentual_MARCO_hospitalizacao}% do total de pacientes.          
        O Município de {municipio_MORRINHOS_hospitalizacao} teve {resultado_MORRINHOS_hospitalizacao} Hospitalização, esses números representam {percentual_MORRINHOS_hospitalizacao}% do total de pacientes.          
        """)

        st.write('Taxa de hospitalização em UTI por Ocorrência de Complicações por Local da Residência')

        # Criando gráfico (Taxa de hospitalização em UTI por Local da Residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.countplot(data=df_filtrado_clinico_assistencia,
                      x='ID_MN_RESI', hue='UTI', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Local da Residência (Cidade)', color='grey')
        ax.set_ylabel('Quantidade de hospitalização em UTI', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.legend(title='Taxa de hospitalização em UTI', frameon=False,
                  fontsize=12, title_fontsize='13', loc='upper right', labelcolor='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write(f"""
        O Município de {municipio_ACARAU_uti} teve {resultado_ACARAU_uti} Hospitalização em UTI, esses números representam {percentual_ACARAU_uti}% do total de pacientes.                   
        O Município de {municipio_BELACRUZ_uti} teve {resultado_BELACRUZ_uti} Hospitalização em UTI, esses números representam {percentual_BELACRUZ_uti}% do total de pacientes.                      
        O Município de {municipio_CRUZ_uti} teve {resultado_CRUZ_uti} Hospitalização em UTI, esses números representam {percentual_CRUZ_uti}% do total de pacientes.                   
        O Município de {municipio_ITAREMA_uti} teve {resultado_ITAREMA_uti} Hospitalização em UTI, esses números representam {percentual_ITAREMA_uti}% do total de pacientes.               
        O Município de {municipio_JIJOCA_uti} teve {resultado_JIJOCA_uti} Hospitalização em UTI, esses números representam {percentual_JIJOCA_uti}% do total de pacientes.         
        O Município de {municipio_MARCO_uti} teve {resultado_MARCO_uti} Hospitalização em UTI, esses números representam {percentual_MARCO_uti}% do total de pacientes.                        
        O Município de {municipio_MORRINHOS_uti} teve {resultado_MORRINHOS_uti} Hospitalização em UTI, esses números representam {percentual_MORRINHOS_uti}% do total de pacientes.                     
        """)

    if st.checkbox("Exibir Indicadores de Vacinação e Tempo de Resposta - 2024"):

        # Lista de colunas a manter para Clínicos e Assistenciais
        colunas_para_manter = [
            'ID_MUNICIP', 'VACINA', 'VACINA_COV', 'DT_SIN_PRI', 'DT_NOTIFIC', 
            'DT_COLETA', 'DT_PCR', 'ID_MN_RESI'
        ]

        df_filtrado_vacinacao_resposta = df_filtrado_regional[colunas_para_manter]

        # Contando a quantidade de pessoas vacinadas
        vacina = df_filtrado_vacinacao_resposta[df_filtrado_vacinacao_resposta['VACINA'] == "Sim"].groupby('ID_MN_RESI')['VACINA'].count()
        total_vacina = df_filtrado_vacinacao_resposta.groupby('ID_MN_RESI')['VACINA'].count()

        # Contando a quantidade de pessoas vacinadas COVID
        vacina_COV = df_filtrado_vacinacao_resposta[df_filtrado_vacinacao_resposta['VACINA_COV'] == "Sim"].groupby('ID_MN_RESI')['VACINA_COV'].count()
        total_vacina_COV = df_filtrado_vacinacao_resposta.groupby('ID_MN_RESI')['VACINA_COV'].count()

        # Preenchendo valores faltantes com 0 para garantir que todos os municípios estejam presentes
        vacina = vacina.reindex(total_vacina.index, fill_value=0)
        vacina_COV = vacina_COV.reindex(total_vacina_COV.index, fill_value=0)

        # Extraindo os índices e resultados        
        municipio_CRUZ_vacina = vacina.index[2] 
        resultado_CRUZ_vacina = vacina.iloc[2]  
        total_casos_CRUZ_vacina = total_vacina.iloc[2]  

        municipio_BELACRUZ_vacina = vacina.index[1]  
        resultado_BELACRUZ_vacina = vacina.iloc[1]  
        total_casos_BELACRUZ_vacina = total_vacina.iloc[1]  

        municipio_ITAREMA_vacina = vacina.index[3]  
        resultado_ITAREMA_vacina = vacina.iloc[3]   
        total_casos_ITAREMA_vacina = total_vacina.iloc[3]   

        municipio_ACARAU_vacina = vacina.index[0] 
        resultado_ACARAU_vacina = vacina.iloc[0] 
        total_casos_ACARAU_vacina = total_vacina.iloc[0] 

        municipio_MORRINHOS_vacina = vacina.index[6]  
        resultado_MORRINHOS_vacina = vacina.iloc[6]  
        total_casos_MORRINHOS_vacina = total_vacina.iloc[6]  

        municipio_JIJOCA_vacina = vacina.index[4]  
        resultado_JIJOCA_vacina = vacina.iloc[4] 
        total_casos_JIJOCA_vacina = total_vacina.iloc[4] 

        municipio_MARCO_vacina = vacina.index[5]  
        resultado_MARCO_vacina = vacina.iloc[5] 
        total_casos_MARCO_vacina = total_vacina.iloc[5] 

        # Extraindo os índices e resultados
        municipio_CRUZ_vacina_COV = vacina_COV.index[2] 
        resultado_CRUZ_vacina_COV = vacina_COV.iloc[2]  
        total_casos_CRUZ_vacina_COV = total_vacina_COV.iloc[2]  

        municipio_BELACRUZ_vacina_COV = vacina_COV.index[1]  
        resultado_BELACRUZ_vacina_COV = vacina_COV.iloc[1]  
        total_casos_BELACRUZ_vacina_COV = total_vacina_COV.iloc[1]  

        municipio_ITAREMA_vacina_COV = vacina_COV.index[3]  
        resultado_ITAREMA_vacina_COV = vacina_COV.iloc[3]   
        total_casos_ITAREMA_vacina_COV = total_vacina_COV.iloc[3]   

        municipio_ACARAU_vacina_COV = vacina_COV.index[0] 
        resultado_ACARAU_vacina_COV = vacina_COV.iloc[0] 
        total_casos_ACARAU_vacina_COV = total_vacina_COV.iloc[0] 

        municipio_MORRINHOS_vacina_COV = vacina_COV.index[6]  
        resultado_MORRINHOS_vacina_COV = vacina_COV.iloc[6]  
        total_casos_MORRINHOS_vacina_COV = total_vacina_COV.iloc[6]  

        municipio_JIJOCA_vacina_COV = vacina_COV.index[4]  
        resultado_JIJOCA_vacina_COV = vacina_COV.iloc[4] 
        total_casos_JIJOCA_vacina_COV = total_vacina_COV.iloc[4] 

        municipio_MARCO_vacina_COV = vacina_COV.index[5]  
        resultado_MARCO_vacina_COV = vacina_COV.iloc[5]
        total_casos_MARCO_vacina_COV = total_vacina_COV.iloc[5]

        percentual_ACARAU_vacina = round(((resultado_ACARAU_vacina / total_casos_ACARAU_vacina) * 100), 2)
        percentual_CRUZ_vacina = round(((resultado_CRUZ_vacina / total_casos_CRUZ_vacina) * 100), 2)
        percentual_ITAREMA_vacina = round(((resultado_ITAREMA_vacina / total_casos_ITAREMA_vacina) * 100), 2)
        percentual_BELACRUZ_vacina = round(((resultado_BELACRUZ_vacina / total_casos_BELACRUZ_vacina) * 100), 2)
        percentual_MORRINHOS_vacina = round(((resultado_MORRINHOS_vacina / total_casos_MORRINHOS_vacina) * 100), 2)
        percentual_JIJOCA_vacina = round(((resultado_JIJOCA_vacina / total_casos_JIJOCA_vacina) * 100), 2)
        percentual_MARCO_vacina = round(((resultado_MARCO_vacina / total_casos_MARCO_vacina) * 100), 2)

        percentual_ACARAU_vacina_COV = round(((resultado_ACARAU_vacina_COV / total_casos_ACARAU_vacina_COV) * 100), 2)
        percentual_CRUZ_vacina_COV = round(((resultado_CRUZ_vacina_COV / total_casos_CRUZ_vacina_COV) * 100), 2)
        percentual_ITAREMA_vacina_COV = round(((resultado_ITAREMA_vacina_COV / total_casos_ITAREMA_vacina_COV) * 100), 2)
        percentual_BELACRUZ_vacina_COV = round(((resultado_BELACRUZ_vacina_COV / total_casos_BELACRUZ_vacina_COV) * 100), 2)
        percentual_MORRINHOS_vacina_COV = round(((resultado_MORRINHOS_vacina_COV / total_casos_MORRINHOS_vacina_COV) * 100), 2)
        percentual_MARCO_vacina_COV = round(((resultado_MARCO_vacina_COV / total_casos_MARCO_vacina_COV) * 100), 2)
        percentual_JIJOCA_vacina_COV = round(((resultado_JIJOCA_vacina_COV / total_casos_JIJOCA_vacina_COV) * 100), 2)

        st.write('Vacinação por local da residência')

        # Criando gráfico (Vacinação por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.countplot(data=df_filtrado_vacinacao_resposta,
                      x='ID_MN_RESI', hue='VACINA', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Local da Residência (Cidade)', color='grey')
        ax.set_ylabel('Quantidade Pessoas Vacidas', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.legend(title='Vacinação', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write(f"""

        O Município de {municipio_ACARAU_vacina} teve {resultado_ACARAU_vacina} Aplicações da Vacina contra SARG, esses números representam {percentual_ACARAU_vacina}% do total de pacientes.        
        O Município de {municipio_BELACRUZ_vacina} teve {resultado_BELACRUZ_vacina} Aplicações da Vacina contra SARG, esses números representam {percentual_BELACRUZ_vacina}% do total de pacientes.       
        O Município de {municipio_CRUZ_vacina} teve {resultado_CRUZ_vacina} Aplicações da Vacina contra SARG, esses números representam {percentual_CRUZ_vacina}% do total de pacientes.         
        O Município de {municipio_ITAREMA_vacina} teve {resultado_ITAREMA_vacina} Aplicações da Vacina contra SARG, esses números representam {percentual_ITAREMA_vacina}% do total de pacientes.      
        O Município de {municipio_JIJOCA_vacina} teve {resultado_JIJOCA_vacina} Aplicações da Vacina contra SARG, esses números representam {percentual_JIJOCA_vacina}% do total de pacientes.  
        O Município de {municipio_MARCO_vacina} teve {resultado_MARCO_vacina} Aplicações da Vacina contra SARG, esses números representam {percentual_MARCO_vacina}% do total de pacientes.           
        O Município de {municipio_MORRINHOS_vacina} teve {resultado_MORRINHOS_vacina} Aplicações da Vacina contra SARG, esses números representam {percentual_MORRINHOS_vacina}% do total de pacientes.        """)

        st.write('Vacinação de COVID por local da residência')

        # Criando o gráfico (Vacinação de COVID por local da residência)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = sns.countplot(data=df_filtrado_vacinacao_resposta,
                      x='ID_MN_RESI', hue='VACINA_COV', palette='Set1', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Local da Residência (Cidade)', color='grey')
        ax.set_ylabel('Quantidade Pessoas Vacidas contra COVID', color='grey')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, color='grey')
        ax.legend(title='Vacinação contra COVID', frameon=False, fontsize=12,
                  title_fontsize='13', loc='upper right', labelcolor='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write(f"""
        O Município de {municipio_ACARAU_vacina_COV} teve {resultado_ACARAU_vacina_COV} Aplicações da Vacina de COVID, esses números representam {percentual_ACARAU_vacina_COV}% do total de pacientes.        
        O Município de {municipio_BELACRUZ_vacina_COV} teve {resultado_BELACRUZ_vacina_COV} Aplicações da Vacina de COVID, esses números representam {percentual_BELACRUZ_vacina_COV}% do total de pacientes.       
        O Município de {municipio_CRUZ_vacina_COV} teve {resultado_CRUZ_vacina_COV} Aplicações da Vacina de COVID, esses números representam {percentual_CRUZ_vacina_COV}% do total de pacientes.         
        O Município de {municipio_ITAREMA_vacina_COV} teve {resultado_ITAREMA_vacina_COV} Aplicações da Vacina de COVID, esses números representam {percentual_ITAREMA_vacina_COV}% do total de pacientes.      
        O Município de {municipio_JIJOCA_vacina_COV} teve {resultado_JIJOCA_vacina_COV} Aplicações da Vacina de COVID, esses números representam {percentual_JIJOCA_vacina_COV}% do total de pacientes.  
        O Município de {municipio_MARCO_vacina_COV} teve {resultado_MARCO_vacina_COV} Aplicações da Vacina de COVID, esses números representam {percentual_MARCO_vacina_COV}% do total de pacientes.           
        O Município de {municipio_MORRINHOS_vacina_COV} teve {resultado_MORRINHOS_vacina_COV} Aplicações da Vacina de COVID, esses números representam {percentual_MORRINHOS_vacina_COV}% do total de pacientes.        
        """)


        # Converte as colunas para o tipo datetime
        df_filtrado_vacinacao_resposta['DT_SIN_PRI'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_SIN_PRI'], errors='coerce', format='%d/%m/%Y')
        df_filtrado_vacinacao_resposta['DT_NOTIFIC'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_NOTIFIC'], errors='coerce', format='%d/%m/%Y')
        df_filtrado_vacinacao_resposta['DT_COLETA'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_COLETA'], errors='coerce', format='%d/%m/%Y')
        df_filtrado_vacinacao_resposta['DT_PCR'] = pd.to_datetime(
            df_filtrado_vacinacao_resposta['DT_PCR'], errors='coerce', format='%d/%m/%Y')

        # Subtração das datas
        df_filtrado_vacinacao_resposta['DIFERENCA_NOTIFIC_SIN_PRI'] = df_filtrado_vacinacao_resposta['DT_NOTIFIC'] - \
            df_filtrado_vacinacao_resposta['DT_SIN_PRI']
        df_filtrado_vacinacao_resposta['DIFERENCA_NOTIFIC_SIN_PRI'] = df_filtrado_vacinacao_resposta['DIFERENCA_NOTIFIC_SIN_PRI'].dt.days        
        
        df_filtrado_vacinacao_resposta['DIFERENCA_test_result'] = df_filtrado_vacinacao_resposta['DT_PCR'] - \
            df_filtrado_vacinacao_resposta['DT_COLETA']
        df_filtrado_vacinacao_resposta['DIFERENCA_test_result'] = df_filtrado_vacinacao_resposta['DIFERENCA_test_result'].dt.days
        
        
        diferenca_NOTIFIC_SIN_PRI = df_filtrado_vacinacao_resposta.groupby('ID_MN_RESI')['DIFERENCA_NOTIFIC_SIN_PRI'].mean().round()
        diferenca_coleta_PCR = df_filtrado_vacinacao_resposta.groupby('ID_MN_RESI')['DIFERENCA_test_result'].mean().round()
 
        # Extraindo os índices e resultados
        municipio_CRUZ_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.index[2] 
        resultado_CRUZ_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.iloc[2]  

        municipio_BELACRUZ_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.index[1]  
        resultado_BELACRUZ_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.iloc[1]  

        municipio_ITAREMA_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.index[3]  
        resultado_ITAREMA_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.iloc[3]   

        municipio_ACARAU_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.index[0] 
        resultado_ACARAU_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.iloc[0] 

        municipio_MORRINHOS_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.index[6]  
        resultado_MORRINHOS_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.iloc[6]  

        municipio_JIJOCA_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.index[4]  
        resultado_JIJOCA_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.iloc[4] 

        municipio_MARCO_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.index[5]  
        resultado_MARCO_diferenca_NOTIFIC_SIN_PRI = diferenca_NOTIFIC_SIN_PRI.iloc[5]  

        # Extraindo os índices e resultados
        municipio_CRUZ_diferenca_coleta_PCR = diferenca_coleta_PCR.index[2] 
        resultado_CRUZ_diferenca_coleta_PCR = diferenca_coleta_PCR.iloc[2]  

        municipio_BELACRUZ_diferenca_coleta_PCR = diferenca_coleta_PCR.index[1]  
        resultado_BELACRUZ_diferenca_coleta_PCR = diferenca_coleta_PCR.iloc[1]  

        municipio_ITAREMA_diferenca_coleta_PCR = diferenca_coleta_PCR.index[3]  
        resultado_ITAREMA_diferenca_coleta_PCR = diferenca_coleta_PCR.iloc[3]   

        municipio_ACARAU_diferenca_coleta_PCR = diferenca_coleta_PCR.index[0] 
        resultado_ACARAU_diferenca_coleta_PCR = diferenca_coleta_PCR.iloc[0] 

        municipio_MORRINHOS_diferenca_coleta_PCR = diferenca_coleta_PCR.index[6]  
        resultado_MORRINHOS_diferenca_coleta_PCR = diferenca_coleta_PCR.iloc[6]  

        municipio_JIJOCA_diferenca_coleta_PCR = diferenca_coleta_PCR.index[4]  
        resultado_JIJOCA_diferenca_coleta_PCR = diferenca_coleta_PCR.iloc[4] 

        municipio_MARCO_diferenca_coleta_PCR = diferenca_coleta_PCR.index[5]  
        resultado_MARCO_diferenca_coleta_PCR = diferenca_coleta_PCR.iloc[5]

        st.write('Tempo Médio entre o aparecimento de sintomas e a notificação.')

        # Criando o gráfico (Tempo Médio de Sintomas até a Notificação)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = diferenca_NOTIFIC_SIN_PRI.plot(kind='bar', color='#377eb8', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Município', color='grey')
        ax.set_ylabel('Diferença de Dias', color='grey')
        ax.set_xticklabels(diferenca_NOTIFIC_SIN_PRI.index,
                           rotation=20, color='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write(f"""
        O Município de {municipio_ACARAU_diferenca_NOTIFIC_SIN_PRI} teve um tempo médio de {resultado_ACARAU_diferenca_NOTIFIC_SIN_PRI} dias até a notificação.          
        O Município de {municipio_BELACRUZ_diferenca_NOTIFIC_SIN_PRI} teve um tempo médio de {resultado_BELACRUZ_diferenca_NOTIFIC_SIN_PRI} dias até a notificação.           
        O Município de {municipio_CRUZ_diferenca_NOTIFIC_SIN_PRI} teve um tempo médio de {resultado_CRUZ_diferenca_NOTIFIC_SIN_PRI} dias até a notificação.          
        O Município de {municipio_ITAREMA_diferenca_NOTIFIC_SIN_PRI} teve um tempo médio de {resultado_ITAREMA_diferenca_NOTIFIC_SIN_PRI} dias até a notificação.          
        O Município de {municipio_JIJOCA_diferenca_NOTIFIC_SIN_PRI} teve um tempo médio de {resultado_JIJOCA_diferenca_NOTIFIC_SIN_PRI} dias até a notificação.      
        O Município de {municipio_MARCO_diferenca_NOTIFIC_SIN_PRI} teve um tempo médio de {resultado_MARCO_diferenca_NOTIFIC_SIN_PRI} dias até a notificação.           
        O Município de {municipio_MORRINHOS_diferenca_NOTIFIC_SIN_PRI} teve um tempo médio de {resultado_MORRINHOS_diferenca_NOTIFIC_SIN_PRI} dias até a notificação.        
        """)

        st.write('Tempo Médio entre a coleta do teste e o resultado.')

        # Criando o gráfico (Tempo Médio de Sintomas até a Notificação)
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = diferenca_coleta_PCR.plot(kind='bar', color='#377eb8', ax=ax)

        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        ax.set_xlabel('Município', color='grey')
        ax.set_ylabel('Diferença de Dias', color='grey')
        ax.set_xticklabels(diferenca_NOTIFIC_SIN_PRI.index,
                           rotation=20, color='grey')
        ax.tick_params(axis='x', colors='grey')
        ax.tick_params(axis='y', colors='grey')

        # Adicionando rótulos nas barras
        for container in bars.containers:
            ax.bar_label(container, color='grey')

        st.pyplot(fig)

        st.write(f"""
        O Município de {municipio_ACARAU_diferenca_coleta_PCR} teve um tempo médio de {resultado_ACARAU_diferenca_coleta_PCR} dias entre a coleta do teste e o resultado.           
        O Município de {municipio_BELACRUZ_diferenca_coleta_PCR} teve um tempo médio de {resultado_BELACRUZ_diferenca_coleta_PCR} dias entre a coleta do teste e o resultado.           
        O Município de {municipio_CRUZ_diferenca_coleta_PCR} teve um tempo médio de {resultado_CRUZ_diferenca_coleta_PCR} dias entre a coleta do teste e o resultado.           
        O Município de {municipio_ITAREMA_diferenca_coleta_PCR} teve um tempo médio de {resultado_ITAREMA_diferenca_coleta_PCR} dias entre a coleta do teste e o resultado.          
        O Município de JIJOCA teve um tempo médio de {resultado_JIJOCA_diferenca_coleta_PCR} dias entre a coleta do teste e o resultado.   
        O Município de {municipio_MARCO_diferenca_coleta_PCR} teve um tempo médio de {resultado_MARCO_diferenca_coleta_PCR} dias entre a coleta do teste e o resultado.               
        O Município de {municipio_MORRINHOS_diferenca_coleta_PCR} teve um tempo médio de {resultado_MORRINHOS_diferenca_coleta_PCR} dias entre a coleta do teste e o resultado.            
        """)

except FileNotFoundError:
    st.error(f"O arquivo no caminho '{
             file_path}' não foi encontrado. Verifique o caminho e tente novamente.")
