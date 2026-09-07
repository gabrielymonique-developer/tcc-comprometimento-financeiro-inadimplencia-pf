# IMPORTANDO BIBLIOTECAS
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from pathlib import Path

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import statsmodels.api as sm
import networkx as nx

from scipy.stats import shapiro
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

warnings.filterwarnings("ignore")


# CAMINHOS DO PROJETO
# ----------------------------------------------------------------------------------------------------------------------
RAIZ_PROJETO = Path(__file__).resolve().parents[1]

arquivo_modelo = (
    RAIZ_PROJETO
    / "Banco_dados"
    / "Processados"
    / "tb_modelo_final.csv"
)


# 1 PASSO: Importando base de dados
# ----------------------------------------------------------------------------------------------------------------------
df_modelo = pd.read_csv(arquivo_modelo)

# 1.1 Criando variável de tendência temporal
# A variável trend representa a ordem cronológica das observações mensais, assumindo valores de 1 a 72.
df_modelo['dataref'] = pd.to_numeric(df_modelo['dataref'])
df_modelo = df_modelo.sort_values('dataref')
df_modelo = df_modelo.reset_index(drop=True)
df_modelo['trend'] = range(1, len(df_modelo)+1)

# 1.2 Validando base de dados
print("Detalhes do banco de dados___________________________________________________")
print("BASE: \n", df_modelo)
print("ANALISE GERAL: \n", df_modelo.describe(), "\n\nCAMPOS:")
print(df_modelo.info(), "\n")


# # 2 PASSO: ANÁLISES PRELIMINARES
# # ----------------------------------------------------------------------------------------------------------------------
# 2.1 Matriz de correlacao
print("Testes: Matriz de Correlação")
corr = df_modelo.select_dtypes(include=np.number).corr()
print(corr)

plt.figure(figsize=(10,6))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.show()
print("\n")


# 2.2 Multicolinearidade (VIF)
print("Testes: Multicolinearidade (VIF)")
X = df_modelo[[
    'familias_endividadas',
    'carteira_over90',
    # 'carteira_15a90',
    'taxa_juros',
    'familias_atraso',
    # 'trend'
    # 'carteira'
    # 'taxa_desemprego'
]]

X = sm.add_constant(X)
vif = pd.DataFrame()
vif['variavel'] = X.columns
vif['VIF'] = [
    variance_inflation_factor(X.values, i)
    for i in range(X.shape[1])
]
print(vif, "\n")


# 2.3 Matriz e rede de correlação entre variáveis explicativas
correlation_matrix = df_modelo[[
    # 'inadimplencia',
    'familias_endividadas',
    'carteira_over90',
    # 'carteira_15a90',
    'taxa_juros',
    'familias_atraso',
]].corr()

plt.figure(figsize=(15, 10))
heatmap = sns.heatmap(correlation_matrix, annot=True, fmt=".4f",
                      cmap=plt.cm.viridis_r,
                      annot_kws={'size': 25}, vmin=-1, vmax=1)
heatmap.set_xticklabels(heatmap.get_xticklabels(), fontsize=15)
heatmap.set_yticklabels(heatmap.get_yticklabels(), fontsize=15)
cbar = heatmap.collections[0].colorbar
cbar.ax.tick_params(labelsize=17)
plt.show()

G = nx.DiGraph()

for variable in correlation_matrix.columns:
    G.add_node(variable)

for i, variable1 in enumerate(correlation_matrix.columns):
    for j, variable2 in enumerate(correlation_matrix.columns):
        if i != j:
            correlation = correlation_matrix.iloc[i, j]
            if abs(correlation) > 0:
                G.add_edge(variable1, variable2, weight=correlation)

correlations = [d["weight"] for _, _, d in G.edges(data=True)]
node_size = 2700
node_color = 'black'
cmap = plt.colormaps.get_cmap('coolwarm_r')
edge_widths = [abs(d["weight"]) * 10 for _, _, d in G.edges(data=True)]
pos = nx.spring_layout(G, k=0.75)

pos["familias_endividadas"] = (pos["familias_endividadas"][0], pos["familias_endividadas"][1] + 1.8)
pos["carteira_over90"] = (pos["carteira_over90"][0], pos["carteira_over90"][1])
# pos["carteira_15a90"] = (pos["carteira_15a90"][0], pos["carteira_15a90"][1])
pos["taxa_juros"] = (pos["taxa_juros"][0], pos["taxa_juros"][1] + 1.8)
pos["familias_atraso"] = (pos["familias_atraso"][0], pos["familias_atraso"][1] + 1.8)


nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color)
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=correlations,
                       edge_cmap=cmap, alpha=0.7)

labels = {node: node for node in G.nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=7.5, font_color='white')
ax = plt.gca()
ax.margins(0.1)
plt.axis("off")
smp = cm.ScalarMappable(cmap=cmap)
smp.set_array([min(correlations), max(correlations)])
cbar = plt.colorbar(smp, ax=ax, label='Correlação')
cbar.set_ticks(np.arange(round(min(correlations),0) - 0.1,
                         max(correlations) + 0.1, 0.1))

plt.show()


# 3 PASSO: MODELOS DE REGRESSÃO
# ----------------------------------------------------------------------------------------------------------------------
# 3.1 MODELO 1 - Modelo completo
print("\n\nOLS 1 - ESTIMAÇÃO DO MODELO COMPLETO:")
modelo_full = sm.OLS.from_formula('inadimplencia ~ familias_endividadas + carteira_over90 + taxa_juros + familias_atraso', df_modelo).fit()
print(modelo_full.summary())


# 3.2 MODELO 2 - StepWise (Backward Elimination)
X = df_modelo[[
    'familias_endividadas',
    'carteira_over90',
    'taxa_juros',
    'familias_atraso'
]]
y = df_modelo['inadimplencia']
X = sm.add_constant(X)
variaveis = list(X.columns)

while len(variaveis) > 0:
    # Ajusta modelo
    modelo = sm.OLS(y, X[variaveis]).fit()

    # Pega maior p-valor
    pvalues = modelo.pvalues
    maior_pvalor = pvalues.max()

    # Variável com maior p-valor
    variavel_remover = pvalues.idxmax()

    # Critério de remoção
    if maior_pvalor > 0.05: # remove a variável com maior p-valor enquanto p > 0,05.
        print(f'Removendo variável: {variavel_remover} | p-valor: {maior_pvalor:.4f}')
        variaveis.remove(variavel_remover)
    else:
        break

print("\n\nOLS 2 - STEP WISE:")
print("\nVariáveis finais:", variaveis)

modelo_step = sm.OLS(y, X[variaveis]).fit()
print(modelo_step.summary())


# 3.3: MODELO 3 - Estimação Isolando familias endividadas
print("\n\nOLS 3 - FAMILIAS ENDIVIDADAS:")
modelo_familias = sm.OLS.from_formula('inadimplencia ~ familias_endividadas', df_modelo).fit()
print(modelo_familias.summary())


# 3.4 MODELO 4 - Modelo com tendência temporal (trend)
print("\n\nOLS 4 - TREND (SERIE TEMPORAL):")
modelo_trend = sm.OLS.from_formula('inadimplencia ~ familias_endividadas + carteira_over90 + taxa_juros + trend', df_modelo).fit()
print(modelo_trend.summary())


# 3.5 MODELO 5 - Backward Elimination com tendência temporal
X = df_modelo[[
    'familias_endividadas',
    'carteira_over90',
    'taxa_juros',
    'familias_atraso',
    'trend'
]]
y = df_modelo['inadimplencia']
X = sm.add_constant(X)
variaveis = list(X.columns)

while len(variaveis) > 0:
    # Ajusta modelo
    modelo = sm.OLS(y, X[variaveis]).fit()

    # Pega maior p-valor
    pvalues = modelo.pvalues
    maior_pvalor = pvalues.max()

    # Variável com maior p-valor
    variavel_remover = pvalues.idxmax()

    # Critério de remoção
    if maior_pvalor > 0.05:
        print(f'Removendo variável: {variavel_remover} | p-valor: {maior_pvalor:.4f}')
        variaveis.remove(variavel_remover)
    else:
        break

print("\n\nOLS 5 - STEP WISE + TREND:")
print("\nVariáveis finais:", variaveis)

modelo_step_trend = sm.OLS(y, X[variaveis]).fit()
print(modelo_step_trend.summary())


# 4 PASSO: ANÁLISES FINAIS
# ----------------------------------------------------------------------------------------------------------------------
# 4.1 Teste de normalidade dos resíduos - Shapiro-Wilk
print("\n\nTeste: Shapiro Wilk:")
teste_shapiro = shapiro(modelo_step.resid)
print('Estatística do teste:', teste_shapiro.statistic)
print('P-value:', teste_shapiro.pvalue)

if teste_shapiro.pvalue > 0.05:
    print('Os resíduos seguem distribuição normal')
else:
    print('Os resíduos NÃO seguem distribuição normal')


# 4.2 Teste Heterocedasticidade (Breusch-Pagan)
print("\nTeste: Heterocedasticidade:")
teste_bp = het_breuschpagan(modelo_step.resid, modelo_step.model.exog)

labels = ['LM Statistic',
          'LM-Test p-value',
          'F-Statistic',
          'F-Test p-value']
for i, j in zip(labels, teste_bp):
    print(i, ':', j)


# 4.3 Teste de autocorrelação serial - Durbin-Watson
print("\nTeste Durbin-Watson:")
dw = durbin_watson(modelo_step.resid)
print("Estatística Durbin-Watson:", dw)


# 5 PASSO: MODELO PRINCIPAL COM ERROS-PADRÃO ROBUSTOS HAC/NEWEY-WEST
# ----------------------------------------------------------------------------------------------------------------------
print("\nOLS 6 - MODELO FINAL:")
X_final = df_modelo[[
    'familias_endividadas',
    'carteira_over90',
    'taxa_juros'
]]
X_final = sm.add_constant(X_final)
y = df_modelo['inadimplencia']

modelo_step_hac = sm.OLS(y, X_final).fit(cov_type='HAC', cov_kwds={'maxlags':1})
print(modelo_step_hac.summary())


# 6 PASSO: MODELO COMPLEMENTAR - CARTEIRA COM ATRASO ENTRE 15 E 90 DIAS
# Utilizado como análise complementar ao modelo principal com carteira Over 90
# ----------------------------------------------------------------------------------------------------------------------
print("\n\nOLS 7 - MODELO COMPLEMENTAR: CARTEIRA 15 A 90 DIAS")
X_15a90 = df_modelo[[
    'familias_endividadas',
    'carteira_15a90',
    'taxa_juros'
]]

X_15a90 = sm.add_constant(X_15a90)
y = df_modelo['inadimplencia']

modelo_15a90 = sm.OLS(y, X_15a90).fit()
print("\nMODELO 7 - OLS CONVENCIONAL:")
print(modelo_15a90.summary())


# 6.2 Teste de normalidade dos resíduos - Shapiro-Wilk
print("\nTeste Shapiro-Wilk - Modelo 7:")
teste_shapiro_15a90 = shapiro(modelo_15a90.resid)

print("Estatística do teste:", teste_shapiro_15a90.statistic)
print("P-value:", teste_shapiro_15a90.pvalue)

if teste_shapiro_15a90.pvalue > 0.05:
    print("Os resíduos seguem distribuição aproximadamente normal")
else:
    print("Os resíduos NÃO seguem distribuição aproximadamente normal")


# 6.3 Teste de heterocedasticidade - Breusch-Pagan
print("\nTeste Breusch-Pagan - Modelo 7:")

teste_bp_15a90 = het_breuschpagan(
    modelo_15a90.resid,
    modelo_15a90.model.exog
)

labels = [
    'LM Statistic',
    'LM-Test p-value',
    'F-Statistic',
    'F-Test p-value'
]

for i, j in zip(labels, teste_bp_15a90):
    print(i, ':', j)


# 6.4 Modelo com erros-padrão robustos HAC / Newey-West
print("\nMODELO 7 - HAC/NEWEY-WEST:")

modelo_15a90_hac = sm.OLS(
    y,
    X_15a90
).fit(
    cov_type='HAC',
    cov_kwds={'maxlags': 1}
)

print(modelo_15a90_hac.summary())
