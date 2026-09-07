# IMPORTANDO BIBLIOTECAS
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from pathlib import Path


# CAMINHOS DO PROJETO
# ----------------------------------------------------------------------------------------------------------------------
RAIZ_PROJETO = Path(__file__).resolve().parents[1]

pasta_originais = (
    RAIZ_PROJETO
    / "Banco_dados"
    / "Originais"
)

pasta_processados = (
    RAIZ_PROJETO
    / "Banco_dados"
    / "Processados"
)

pasta_processados.mkdir(parents=True, exist_ok=True)


# 1 PASSO: Importando as bases de dados
# ----------------------------------------------------------------------------------------------------------------------
df_inadimplencia = pd.read_excel(pasta_originais / "tb_inadimplencia.xlsx")

df_familias = pd.read_excel(pasta_originais / "tb_familias_endividadas.xlsx")

df_juros = pd.read_excel(pasta_originais / "tb_taxa_juros.xlsx")

df_credito = pd.read_excel(pasta_originais / "tb_carteira_credito.xlsx")

# Base gerada pelo código 01
df_atraso = pd.read_csv(pasta_processados / "tb_carteira_atraso.csv")


# 2 PASSO: Verificando duplicações e tipos
# ----------------------------------------------------------------------------------------------------------------------
campo = "dataref"

print(f"Validação do dado - {campo}:")

print(
    "DF_INADIMPLENCIA:"
    "\nDuplicação:", df_inadimplencia[campo].duplicated().sum(),
    "\nTipo:", df_inadimplencia[campo].dtype
)

print(
    "\nDF_FAMILIAS:"
    "\nDuplicação:", df_familias[campo].duplicated().sum(),
    "\nTipo:", df_familias[campo].dtype
)

print(
    "\nDF_JUROS:"
    "\nDuplicação:", df_juros[campo].duplicated().sum(),
    "\nTipo:", df_juros[campo].dtype
)

print(
    "\nDF_CREDITO:"
    "\nDuplicação:", df_credito[campo].duplicated().sum(),
    "\nTipo:", df_credito[campo].dtype
)

print(
    "\nDF_ATRASO:"
    "\nDuplicação:", df_atraso[campo].duplicated().sum(),
    "\nTipo:", df_atraso[campo].dtype
)


# 3 PASSO: Consolidando as bases
# ----------------------------------------------------------------------------------------------------------------------
df_modelo = (
    df_inadimplencia
    .merge(
        df_familias[
            [
                "dataref",
                "familias_endividadas",
                "familias_atraso"
            ]
        ],
        on="dataref",
        how="left"
    )
    .merge(
        df_juros[
            [
                "dataref",
                "taxa_juros"
            ]
        ],
        on="dataref",
        how="left"
    )
    .merge(
        df_credito[
            [
                "dataref",
                "carteira"
            ]
        ],
        on="dataref",
        how="left"
    )
    .merge(
        df_atraso[
            [
                "dataref",
                "carteira_over90",
                "carteira_15a90"
            ]
        ],
        on="dataref",
        how="left"
    )
)

print("\nConsolidação realizada com SUCESSO")


# 4 PASSO: Validações finais
# ----------------------------------------------------------------------------------------------------------------------
# garantir coluna Ano como inteiro
df_modelo["ano"] = pd.to_datetime(df_modelo["ano"]).dt.year.astype(int)


print("\n\nValidação da BASE:"
    "\n________________________________________________________________________________")
df_modelo.info()

print("\nValidação dos NULOS:"
    "\n________________________________________________________________________________")
print(df_modelo.isnull().sum())


# 5 PASSO: Salvando a base consolidada
# ----------------------------------------------------------------------------------------------------------------------
arquivo_saida = pasta_processados / "tb_modelo_final.csv"

df_modelo.to_csv(
    arquivo_saida,
    index=False
)

print(f"\nArquivo salvo em: {arquivo_saida}")