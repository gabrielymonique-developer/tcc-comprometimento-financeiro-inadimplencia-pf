# IMPORTANDO BIBLIOTECAS
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import zscore
from matplotlib.lines import Line2D

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

df_modelo = pd.read_csv(arquivo_modelo)


# GRAFICO 1: Gráfico temporal
# ----------------------------------------------------------------------------------------------------------------------

# Garantir data em formato correto
df_modelo["dataref"] = pd.to_datetime(
    df_modelo["dataref"].astype(str),
    format="%Y%m"
)

# Ordenar base
df_modelo = (
    df_modelo
    .sort_values("dataref")
    .reset_index(drop=True)
)

# Variáveis do gráfico
variaveis = [
    "inadimplencia",
    "familias_endividadas",
    "taxa_juros",
    "carteira_over90"
]

# Criar base padronizada
df_z = df_modelo[["dataref"] + variaveis].copy()

for var in variaveis:
    df_z[var + "_z"] = zscore(df_z[var])

# Plotar gráfico
plt.figure(figsize=(12, 6))

plt.plot(
    df_z["dataref"],
    df_z["inadimplencia_z"],
    label="Inadimplência"
)

plt.plot(
    df_z["dataref"],
    df_z["familias_endividadas_z"],
    label="Famílias endividadas"
)

plt.plot(
    df_z["dataref"],
    df_z["taxa_juros_z"],
    label="Taxa média de juros PF"
)

plt.plot(
    df_z["dataref"],
    df_z["carteira_over90_z"],
    label="Carteira com atraso >90 dias"
)

# Período de impacto da pandemia
plt.axvspan(
    pd.to_datetime("2020-03-01"),
    pd.to_datetime("2021-12-31"),
    alpha=0.15,
    label="Período de impacto da pandemia"
)

plt.axhline(0, linewidth=1)

plt.title("Evolução temporal padronizada das variáveis")
plt.xlabel("Período")
plt.ylabel("Desvio em relação à média histórica (Z-score)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# GRAFICO 2: Gráficos de dispersão com reta de regressão linear
# ----------------------------------------------------------------------------------------------------------------------
def grafico_regressao(df, var_x, var_y, eixo_x):

    fig, ax = plt.subplots(figsize=(15, 10))

    sns.regplot(
        data=df,
        x=var_x,
        y=var_y,
        marker="o",
        ci=False,
        ax=ax,
        scatter_kws={
            "color": "navy",
            "alpha": 0.9,
            "s": 220
        },
        line_kws={
            "color": "grey",
            "linewidth": 5
        }
    )

    # Nome dos eixos
    ax.set_xlabel(eixo_x, fontsize=24)
    ax.set_ylabel("Inadimplência (%)", fontsize=24)

    # Tamanho dos valores dos eixos
    ax.tick_params(axis="both", labelsize=20)

    # Remove bordas superior e direita
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Mantém somente os eixos inferior e esquerdo
    ax.spines["bottom"].set_color("black")
    ax.spines["left"].set_color("black")

    ax.spines["bottom"].set_linewidth(1.5)
    ax.spines["left"].set_linewidth(1.5)

    # Legenda manual
    legenda = [
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="None",
            markerfacecolor="navy",
            markeredgecolor="navy",
            markersize=12,
            label="Valores observados"
        ),
        Line2D(
            [0],
            [0],
            color="grey",
            linewidth=5,
            label="Reta de regressão linear"
        )
    ]

    ax.legend(
        handles=legenda,
        fontsize=24,
        loc="upper left",
        frameon=False
    )

    plt.tight_layout()
    plt.show()


grafico_regressao(
    df_modelo,
    "familias_endividadas",
    "inadimplencia",
    "FE - famílias endividadas (%)"
)

grafico_regressao(
    df_modelo,
    "taxa_juros",
    "inadimplencia",
    "TJ - Taxa de juros (%)"
)

grafico_regressao(
    df_modelo,
    "carteira_over90",
    "inadimplencia",
    "CA90 - Carteira vencida acima de 90 dias (R$ milhões)"
)

grafico_regressao(
    df_modelo,
    "carteira_15a90",
    "inadimplencia",
    "CA15-90 - Carteira vencida entre 15 e 90 dias (R$ milhões)"
)

grafico_regressao(
    df_modelo,
    "familias_atraso",
    "inadimplencia",
    "FA - famílias em atraso (%)"
)