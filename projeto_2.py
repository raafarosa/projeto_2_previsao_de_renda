import streamlit as st
import io

import numpy as np
import pandas as pd

from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree


st.set_page_config(
    page_title="Projeto - 02 Previsão de renda",
    page_icon="https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/regular_ebac-logo.ico",
    layout="wide",
    initial_sidebar_state="auto",
)

st.sidebar.markdown('''
<div style="text-align:center">
<img src="https://raw.githubusercontent.com/raafarosa/Ebac_Data_Scientist_General/main/utilities/newebac_logo_black_half.png" alt="ebac-logo" width=50%>
</div>

# **Profissão: Cientista de Dados**

**Por:** [Rafael Rosa Alves](https://www.linkedin.com/in/rafael-rosa-alves/)<br>
---
''', unsafe_allow_html=True)

with st.sidebar.expander("Bibliotecas/Pacotes", expanded=False):
    st.code('''
    import streamlit as st
    import io

    import numpy as np
    import pandas as pd

    from ydata_profiling import ProfileReport
    from streamlit_pandas_profiling import st_profile_report

    import matplotlib.pyplot as plt
    import seaborn as sns

    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeRegressor
    from sklearn import tree
    ''', language='python')


st.markdown('# <div style="text-align:center"> [Previsão de renda](https://github.com/raafarosa/projeto_2_previsao_de_renda) </div>',
            unsafe_allow_html=True)


st.divider()


st.markdown('''
## Etapa 1 CRISP - DM: Entendimento do negócio <a name="1"></a>
''', unsafe_allow_html=True)


st.markdown('''
Uma instituição financeira está interessada em aprofundar sua compreensão do perfil de renda de seus novos clientes para várias finalidades, como ajustar de forma mais precisa os limites de crédito dos cartões dos novos clientes, sem a necessidade de solicitar olerites ou documentação que possa afetar a experiência do cliente.

Com esse objetivo, realizou um estudo com alguns clientes, validando suas rendas por meio de olerites e outros documentos, e tem a intenção de desenvolver um modelo preditivo para prever essas rendas com base em algumas variáveis já presentes em seu banco de dados.
''')


st.markdown('''
## Etapa 2 Crisp-DM: Entendimento dos dados<a name="2"></a>
''', unsafe_allow_html=True)


st.markdown('''
### Dicionário de dados <a name="dicionario"></a>

| Variável              | Descrição                                                                                                  | Tipo             |
| --------------------- |:----------------------------------------------------------------------------------------------------------:| ----------------:|
| data_ref              | Data de referência de coleta das variáveis                                                                 | object           |
| id_cliente            | Código identificador exclusivo do cliente                                                                  | int              |
| sexo                  | Sexo do cliente (M = 'Masculino'; F = 'Feminino')                                                          | object (binária) |
| posse_de_veiculo      | Indica se o cliente possui veículo (True = 'Possui veículo'; False = 'Não possui veículo')                 | bool (binária)   |
| posse_de_imovel       | Indica se o cliente possui imóvel (True = 'Possui imóvel'; False = 'Não possui imóvel')                    | bool (binária)   |
| qtd_filhos            | Quantidade de filhos do cliente                                                                            | int              |
| tipo_renda            | Tipo de renda do cliente (Empresário, Assalariado, Servidor público, Pensionista, Bolsista)                | object           |
| educacao              | Grau de instrução do cliente (Primário, Secundário, Superior incompleto, Superior completo, Pós graduação) | object           |
| estado_civil          | Estado civil do cliente (Solteiro, União, Casado, Separado, Viúvo)                                         | object           |
| tipo_residencia       | Tipo de residência do cliente (Casa, Governamental, Com os pais, Aluguel, Estúdio, Comunitário)            | object           |
| idade                 | Idade do cliente em anos                                                                                   | int              |
| tempo_emprego         | Tempo no emprego atual                                                                                     | float            |
| qt_pessoas_residencia | Quantidade de pessoas que moram na residência                                                              | float            |
| **renda**             | Valor numérico decimal representando a renda do cliente em reais                                           | float            |
''', unsafe_allow_html=True)


st.markdown('''
### Carregando os dados <a name="dados"></a>
''', unsafe_allow_html=True)


# VERIFICAR ARQUIVOS LOCAIS:
# path_to_find = os.listdir()
# st.title(path_to_find)
filepath = './input/previsao_de_renda.csv'
renda = pd.read_csv(filepath_or_buffer=filepath)

buffer = io.StringIO()
renda.info(buf=buffer)
st.text(buffer.getvalue())
st.dataframe(renda)


st.table(renda.nunique()
              .to_frame()
              .reset_index()
              .rename(columns={'index': 'Variável',
                               0: 'Valores únicos'}))


renda.drop(columns=['Unnamed: 0', 'id_cliente'], inplace=True)
st.write('Quantidade total de linhas:',
         len(renda))
st.write('Quantidade de linhas duplicadas:',
         renda.duplicated().sum())
st.write('Quantidade após remoção das linhas duplicadas:',
         len(renda.drop_duplicates()))
renda.drop_duplicates(inplace=True, ignore_index=True)
buffer = io.StringIO()
renda.info(buf=buffer)
st.text(buffer.getvalue())


st.markdown('''
### Entendimento dos dados - Univariada <a name="univariada"></a>
''', unsafe_allow_html=True)


with st.expander("Pandas Profiling – Relatório interativo para análise exploratória de dados", expanded=True):
    prof = ProfileReport(df=renda,
                         minimal=False,
                         explorative=True,
                         dark_mode=True,
                         orange_mode=True)
    # st.components.v1.html(prof.to_html(), height=600, scrolling=True)
    st_profile_report(prof)


st.markdown('''
####  Estatísticas descritivas das variáveis quantitativas <a name="describe"></a>
''', unsafe_allow_html=True)


st.write(renda.describe().transpose())


st.markdown('''
### Entendimento dos dados - Bivariadas <a name="bivariada"></a>
''', unsafe_allow_html=True)


st.markdown('''
#### Matriz de correlação <a name="correlacao"></a>
''', unsafe_allow_html=True)


st.write((renda
          .iloc[:, 3:]
          .corr(numeric_only=True)
          .tail(n=1)
          ))


st.markdown('Com base na matriz de correlação, nota-se que a variável `tempo_emprego` exibe a maior associação com a variável `renda`, apresentando um coeficiente de correlação de 38,5%.')


st.markdown('''
#### Matriz de dispersão <a name="dispersao"></a>
''', unsafe_allow_html=True)


sns.pairplot(data=renda,
             hue='tipo_renda',
             vars=['qtd_filhos',
                   'idade',
                   'tempo_emprego',
                   'qt_pessoas_residencia',
                   'renda'],
             diag_kind='hist')
st.pyplot(plt)


st.markdown('Ao examinar o *pairplot*, que é uma representação gráfica na forma de matriz de dispersão, é perceptível a presença de alguns *outliers* na variável `renda`, os quais têm o potencial de influenciar os resultados da análise de tendência, embora sejam pouco frequentes. Ademais, nota-se uma correlação fraca entre praticamente todas as variáveis quantitativas, corroborando os achados da matriz de correlação.')


st.markdown('''
##### Clustermap <a name="clustermap"></a>
''', unsafe_allow_html=True)


cmap = sns.diverging_palette(h_neg=100,
                             h_pos=359,
                             as_cmap=True,
                             sep=1,
                             center='light')
ax = sns.clustermap(data=renda.corr(numeric_only=True),
                    figsize=(10, 10),
                    center=0,
                    cmap=cmap)
plt.setp(ax.ax_heatmap.get_xticklabels(), rotation=45)
st.pyplot(plt)


st.markdown('Ao analisar o *pairplot*, uma representação gráfica na forma de matriz de dispersão, é evidente a presença de alguns *outliers* na variável `renda`, os quais possuem o potencial de impactar os resultados da análise de tendência, apesar de sua baixa frequência. Além disso, observa-se uma correlação fraca entre praticamente todas as variáveis quantitativas, o que confirma os resultados obtidos na matriz de correlação.')


st.markdown('''
#####  Linha de tendência <a name="tendencia"></a>
''', unsafe_allow_html=True)


plt.figure(figsize=(16, 9))
sns.scatterplot(x='tempo_emprego',
                y='renda',
                hue='tipo_renda',
                size='idade',
                data=renda,
                alpha=0.4)
sns.regplot(x='tempo_emprego',
            y='renda',
            data=renda,
            scatter=False,
            color='.3')
st.pyplot(plt)


st.markdown('Apesar de não ser tão alta, a correlação entre a variável `tempo_emprego` e a variável `renda` revela claramente uma covariância positiva, evidenciada pela inclinação da linha de tendência.')


st.markdown('''
#### Análise das variáveis qualitativas <a name="qualitativas"></a>
''', unsafe_allow_html=True)


with st.expander("Análise de relevância preditiva com variáveis booleanas", expanded=True):
    plt.rc('figure', figsize=(12, 4))
    fig, axes = plt.subplots(nrows=1, ncols=2)
    sns.pointplot(x='posse_de_imovel',
                  y='renda',
                  data=renda,
                  dodge=True,
                  ax=axes[0])
    sns.pointplot(x='posse_de_veiculo',
                  y='renda',
                  data=renda,
                  dodge=True,
                  ax=axes[1])
    st.pyplot(plt)

    st.markdown('Ao contrastar os gráficos acima, é evidente que a variável `posse_de_veículo` é mais relevante na predição de renda, como indicado pela maior disparidade entre os intervalos de confiança para aqueles que possuem e não possuem veículo. Em contrapartida, a variável `posse_de_imóvel` não mostra diferença significativa entre as diferentes condições de posse imobiliária.')


with st.expander("Análise das variáveis qualitativas ao longo do tempo", expanded=True):
    renda['data_ref'] = pd.to_datetime(arg=renda['data_ref'])
    qualitativas = renda.select_dtypes(include=['object', 'boolean']).columns
    plt.rc('figure', figsize=(16, 4))
    for col in qualitativas:
        fig, axes = plt.subplots(nrows=1, ncols=2)
        fig.subplots_adjust(wspace=.6)
        tick_labels = renda['data_ref'].map(
            lambda x: x.strftime('%b/%Y')).unique()
        # barras empilhadas:
        renda_crosstab = pd.crosstab(index=renda['data_ref'],
                                     columns=renda[col],
                                     normalize='index')
        ax0 = renda_crosstab.plot.bar(stacked=True,
                                      ax=axes[0])
        ax0.set_xticklabels(labels=tick_labels, rotation=45)
        axes[0].legend(bbox_to_anchor=(1, .5), loc=6, title=f"'{col}'")
        # perfis médios no tempo:
        ax1 = sns.pointplot(x='data_ref', y='renda', hue=col,
                            data=renda, dodge=True, ci=95, ax=axes[1])
        ax1.set_xticklabels(labels=tick_labels, rotation=45)
        axes[1].legend(bbox_to_anchor=(1, .5), loc=6, title=f"'{col}'")
        st.pyplot(plt)


st.markdown('''
## Etapa 3 Crisp-DM: Preparação dos dados<a name="3"></a>
''', unsafe_allow_html=True)


renda.drop(columns='data_ref', inplace=True)
renda.dropna(inplace=True)
st.table(pd.DataFrame(index=renda.nunique().index,
                      data={'tipos_dados': renda.dtypes,
                            'qtd_valores': renda.notna().sum(),
                            'qtd_categorias': renda.nunique().values}))


with st.expander("Conversão das variáveis categóricas em variáveis numéricas (dummies)", expanded=True):
    renda_dummies = pd.get_dummies(data=renda)
    buffer = io.StringIO()
    renda_dummies.info(buf=buffer)
    st.text(buffer.getvalue())

    st.table((renda_dummies.corr()['renda']
              .sort_values(ascending=False)
              .to_frame()
              .reset_index()
              .rename(columns={'index': 'var',
                               'renda': 'corr'})
              .style.bar(color=['darkred', 'darkgreen'], align=0)
              ))


st.markdown('''
## Etapa 4 Crisp-DM: Modelagem <a name="4"></a>
''', unsafe_allow_html=True)


st.markdown('Optamos pelo DecisionTreeRegressor como técnica, dada sua aptidão para lidar com problemas de regressão, como a previsão de renda dos clientes. Além disso, as árvores de decisão são de fácil interpretação e possibilitam a identificação dos atributos mais relevantes para a previsão da variável-alvo, o que a torna uma escolha sólida para o projeto.')


st.markdown('''
### Divisão da base em treino e teste <a name="train_test"></a>
''', unsafe_allow_html=True)


X = renda_dummies.drop(columns='renda')
y = renda_dummies['renda']
st.write('Quantidade de linhas e colunas de X:', X.shape)
st.write('Quantidade de linhas de y:', len(y))
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
st.write('X_train:', X_train.shape)
st.write('X_test:', X_test.shape)
st.write('y_train:', y_train.shape)
st.write('y_test:', y_test.shape)


st.markdown('''
### Seleção de hiperparâmetros do modelo com for loop <a name="for_loop"></a>
''', unsafe_allow_html=True)


score = pd.DataFrame(columns=['max_depth', 'min_samples_leaf', 'score'])
for x in range(1, 21):
    for y in range(1, 31):
        reg_tree = DecisionTreeRegressor(random_state=42,
                                         max_depth=x,
                                         min_samples_leaf=y)
        reg_tree.fit(X_train, y_train)
        score = pd.concat(objs=[score,
                                pd.DataFrame({'max_depth': [x],
                                              'min_samples_leaf': [y],
                                              'score': [reg_tree.score(X=X_test,
                                                                       y=y_test)]})],
                          axis=0,
                          ignore_index=True)
st.dataframe(score.sort_values(by='score', ascending=False))


st.markdown('''
### Rodando o modelo <a name="rodando"></a>
''', unsafe_allow_html=True)


reg_tree = DecisionTreeRegressor(random_state=42,
                                 max_depth=8,
                                 min_samples_leaf=4)
# reg_tree.fit(X_train, y_train)
st.text(reg_tree.fit(X_train, y_train))


with st.expander("Visualização gráfica da árvore com plot_tree", expanded=True):
    plt.figure(figsize=(18, 9))
    tree.plot_tree(decision_tree=reg_tree,
                   feature_names=X.columns,
                   filled=True)
    st.pyplot(plt)


with st.expander("Visualização impressa da árvore", expanded=False):
    text_tree_print = tree.export_text(decision_tree=reg_tree)
    st.text(text_tree_print)


st.markdown('''
## Etapa 5 Crisp-DM: Avaliação dos resultados <a name="5"></a>
''', unsafe_allow_html=True)


r2_train = reg_tree.score(X=X_train, y=y_train)
r2_test = reg_tree.score(X=X_test, y=y_test)
template = 'O coeficiente de determinação (𝑅2) da árvore com profundidade = {0} para a base de {1} é: {2:.2f}'
st.write(template.format(reg_tree.get_depth(),
                         'treino',
                         r2_train)
         .replace(".", ","))
st.write(template.format(reg_tree.get_depth(),
                         'teste',
                         r2_test)
         .replace(".", ","))


renda['renda_predict'] = np.round(reg_tree.predict(X), 2)
st.dataframe(renda[['renda', 'renda_predict']])


st.markdown('''
## Etapa 6 Crisp-DM: Implantação <a name="6"></a>
''', unsafe_allow_html=True)

st.markdown('Neste cenário foi desenvolvida uma calculadora simples para a simulação das condições de crédito, baseando-se em todo o entendimento que foi feito sobre este modelo ao longo da trajetória da analise. Que pode ser visto no menu de navegação lateral nomeado como "Simulacao"')

'---'