# Fontes dos Dados

Este documento apresenta as fontes utilizadas na construção da base de dados do projeto, bem como informações sobre periodicidade, período analisado e procedimentos necessários para reprodução das etapas de preparação dos dados.

O estudo utiliza informações públicas referentes ao período de **janeiro de 2020 a dezembro de 2025**, com periodicidade mensal.

---

## 1. Inadimplência de Pessoas Físicas

**Arquivo disponível no repositório:**

`Banco_dados/Originais/tb_inadimplencia.xlsx`

**Fonte:** Banco Central do Brasil (BCB)

**Periodicidade:** Mensal

**Período utilizado:** Janeiro/2020 a Dezembro/2025

**Variável utilizada:**

- `inadimplencia`: percentual de inadimplência da carteira de crédito destinada a Pessoas Físicas (PF).

A variável é utilizada como variável dependente dos modelos econométricos desenvolvidos no projeto.

---

## 2. Famílias Endividadas e Famílias com Contas em Atraso

**Arquivo disponível no repositório:**

`Banco_dados/Originais/tb_familias_endividadas.xlsx`

**Fonte:** Confederação Nacional do Comércio de Bens, Serviços e Turismo (CNC)

**Pesquisa:** Pesquisa de Endividamento e Inadimplência do Consumidor (PEIC)

**Periodicidade:** Mensal

**Período utilizado:** Janeiro/2020 a Dezembro/2025

**Variáveis utilizadas:**

- `familias_endividadas`: percentual de famílias que declararam possuir algum tipo de dívida;
- `familias_atraso`: percentual de famílias com contas ou dívidas em atraso.

As informações são utilizadas como indicadores do comprometimento financeiro das famílias brasileiras.

---

## 3. Taxa de Juros para Pessoas Físicas

**Arquivo disponível no repositório:**

`Banco_dados/Originais/tb_taxa_juros.xlsx`

**Fonte:** Banco Central do Brasil (BCB)

**Periodicidade:** Mensal

**Período utilizado:** Janeiro/2020 a Dezembro/2025

**Variável utilizada:**

- `taxa_juros`: taxa média de juros das operações de crédito destinadas a Pessoas Físicas.

A variável é utilizada como indicador das condições de crédito enfrentadas pelas famílias no período analisado.

---

## 4. Carteira de Crédito para Pessoas Físicas

**Arquivo disponível no repositório:**

`Banco_dados/Originais/tb_carteira_credito.xlsx`

**Fonte:** Banco Central do Brasil (BCB)

**Periodicidade:** Mensal

**Período utilizado:** Janeiro/2020 a Dezembro/2025

**Variável utilizada:**

- `carteira`: saldo da carteira de crédito destinada a Pessoas Físicas.

A variável foi utilizada durante as etapas exploratórias e de construção das bases do estudo.

---

## 5. Carteira com Atraso entre 15 e 90 dias e acima de 90 dias

As informações utilizadas para construção das variáveis de carteira em atraso foram obtidas por meio dos arquivos públicos do **SCR.data**, disponibilizados pelo Banco Central do Brasil.

### 5.1 Dados brutos

Os arquivos originais utilizados nessa etapa possuem elevado volume de armazenamento. Para o período de janeiro de 2020 a dezembro de 2025, foram utilizados **72 arquivos mensais em formato CSV**, totalizando aproximadamente **6,29 GB**.

Por esse motivo, os arquivos brutos do SCR **não são disponibilizados diretamente neste repositório**.

O usuário que desejar reproduzir integralmente essa etapa deve obter os arquivos na fonte oficial e armazená-los no seguinte diretório:

`Banco_dados/Originais/SCR_carteira_atraso/`

A estrutura esperada é semelhante a:

```text
SCR_carteira_atraso/
├── scrdata_202001.csv
├── scrdata_202002.csv
├── ...
└── scrdata_202512.csv
```

---

### 5.2 Processamento

O tratamento dos arquivos é realizado pelo script:

`Codigos/01_preparacao_carteira_atraso.py`

O código:

1. localiza os arquivos CSV do SCR;
2. seleciona apenas registros referentes a Pessoas Físicas (`PF`);
3. seleciona os campos referentes às faixas de atraso;
4. consolida os valores por mês;
5. converte os valores para milhões de reais;
6. gera a base processada utilizada nas etapas seguintes.

---

### 5.3 Base processada disponibilizada

Para permitir a reprodução das análises sem a necessidade de baixar os aproximadamente **6,29 GB** de arquivos brutos, a base resultante desse processamento é disponibilizada no repositório:

`Banco_dados/Processados/tb_carteira_atraso.csv`

**Variáveis principais:**

- `carteira_15a90`: saldo da carteira vencida entre 15 e 90 dias;
- `carteira_over90`: saldo da carteira vencida acima de 90 dias.

Os valores são apresentados em **R$ milhões**.

---

## 6. Base Consolidada do Modelo

Após a preparação das bases individuais, os dados são consolidados por meio do script:

`Codigos/02_consolidacao_base.py`

O resultado é armazenado em:

`Banco_dados/Processados/tb_modelo_final.csv`

Essa base contém as variáveis utilizadas nas análises exploratórias e nos modelos econométricos do estudo.

O processo de consolidação utiliza o campo:

`dataref`

como chave temporal para combinação das diferentes bases.

---

## 7. Período de Análise

Todas as séries utilizadas no modelo principal foram organizadas em periodicidade mensal, abrangendo:

**Janeiro de 2020 a Dezembro de 2025**

Totalizando:

**72 observações mensais**

---

## 8. Observações sobre Reprodutibilidade

Os arquivos disponibilizados neste repositório possuem finalidade acadêmica e foram obtidos a partir de fontes públicas.

Para reproduzir as análises:

1. disponibilize os arquivos necessários nas pastas indicadas;
2. instale as dependências descritas no arquivo `requirements.txt`;
3. execute os códigos conforme a sequência apresentada no `README.md`.

A sequência principal de execução é:

```text
01_preparacao_carteira_atraso.py
        ↓
tb_carteira_atraso.csv

02_consolidacao_base.py
        ↓
tb_modelo_final.csv

03_modelagem_econometrica.py
        ↓
Modelos e testes estatísticos

04_objetos_visuais.py
        ↓
Visualizações utilizadas nas análises
```
