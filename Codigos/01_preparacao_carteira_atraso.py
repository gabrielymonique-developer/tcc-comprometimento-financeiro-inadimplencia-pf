# IMPORTANDO BIBLIOTECAS
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from pathlib import Path


# CAMINHOS DO PROJETO
# ----------------------------------------------------------------------------------------------------------------------
RAIZ_PROJETO = Path(__file__).resolve().parents[1]

pasta_scr = (
    RAIZ_PROJETO
    / "Banco_dados"
    / "Originais"
    / "SCR_carteira_atraso"
)

pasta_processados = (
    RAIZ_PROJETO
    / "Banco_dados"
    / "Processados"
)

pasta_processados.mkdir(parents=True, exist_ok=True)


# 1 PASSO: Importando base de dados
# ----------------------------------------------------------------------------------------------------------------------
arquivos = sorted(pasta_scr.rglob("*.csv"))

print(f"Quantidade de arquivos encontrados: {len(arquivos)}")


# 2 PASSO: Selecionando apenas as colunas necessárias
# ----------------------------------------------------------------------------------------------------------------------
colunas = [
    "data_base",
    "cliente",
    "vencido_de_15_ate_90_dias",
    "vencido_acima_de_90_dias"
]


# 3 PASSO: Lendo, filtrando e sumarizando cada arquivo
# ----------------------------------------------------------------------------------------------------------------------
lista_resumo = []

for i, arquivo in enumerate(arquivos, start=1):

    print(f"Processando {i}/{len(arquivos)}: {arquivo.name}")

    df_temp = pd.read_csv(
        arquivo,
        sep=";",
        encoding="utf-8",
        usecols=colunas,
        decimal=",",
        low_memory=False
    )

    # Mantendo somente Pessoa Física
    df_temp = df_temp[df_temp["cliente"] == "PF"]

    # Somando os valores de atraso para cada mês
    resumo_mes = (
        df_temp
        .groupby("data_base", as_index=False)[
            [
                "vencido_de_15_ate_90_dias",
                "vencido_acima_de_90_dias"
            ]
        ]
        .sum()
    )

    lista_resumo.append(resumo_mes)

    # Libera o arquivo grande da memória
    del df_temp


# 4 PASSO: Consolidando os resultados mensais
# ----------------------------------------------------------------------------------------------------------------------
df_carteira_atraso = pd.concat(
    lista_resumo,
    ignore_index=True
)

# Caso exista mais de um arquivo referente à mesma data-base
df_carteira_atraso = (
    df_carteira_atraso
    .groupby("data_base", as_index=False)[
        [
            "vencido_de_15_ate_90_dias",
            "vencido_acima_de_90_dias"
        ]
    ]
    .sum()
    .sort_values("data_base")
    .reset_index(drop=True)
)


# 5 PASSO: Tratando campos temporais e identificadores
# ----------------------------------------------------------------------------------------------------------------------
df_carteira_atraso["data_base"] = pd.to_datetime(
    df_carteira_atraso["data_base"]
)

# Ano: 2020
df_carteira_atraso["Ano"] = (
    df_carteira_atraso["data_base"]
    .dt.year
    .astype(int)
)

# Data de referência: 202001
df_carteira_atraso["dataref"] = (
    df_carteira_atraso["data_base"]
    .dt.strftime("%Y%m")
    .astype(int)
)

# Trimestre: 1T2020
df_carteira_atraso["trimestre"] = (
    df_carteira_atraso["data_base"].dt.quarter.astype(str)
    + "T"
    + df_carteira_atraso["data_base"].dt.year.astype(str)
)

# Tipo de pessoa
df_carteira_atraso["tipo_pessoa"] = "PF"


# 6 PASSO: Organizando as colunas
# ----------------------------------------------------------------------------------------------------------------------
df_rename_coluns = df_carteira_atraso.rename(
    columns={
        "vencido_de_15_ate_90_dias": "carteira_15a90",
        "vencido_acima_de_90_dias": "carteira_over90"
    }
)

# Convertendo valores para milhões de reais
df_rename_coluns["carteira_15a90"] = (
    df_rename_coluns["carteira_15a90"] / 1_000_000
)

df_rename_coluns["carteira_over90"] = (
    df_rename_coluns["carteira_over90"] / 1_000_000
)

# Ordem das colunas
df_final = df_rename_coluns[
    [
        "dataref",
        "Ano",
        "trimestre",
        "carteira_15a90",
        "carteira_over90",
        "tipo_pessoa"
    ]
]


# 7 PASSO: Validações
# ----------------------------------------------------------------------------------------------------------------------
print(df_final.head())
print(df_final.tail())

print("\nDimensão:", df_final.shape)
print("Quantidade de meses:", df_final["dataref"].nunique())
print("Data mínima:", df_final["dataref"].min())
print("Data máxima:", df_final["dataref"].max())


# 8 PASSO: Salvando a base processada
# ----------------------------------------------------------------------------------------------------------------------
arquivo_saida = pasta_processados / "tb_carteira_atraso.csv"

df_final.to_csv(
    arquivo_saida,
    index=False
)

print(f"\nArquivo salvo em: {arquivo_saida}")