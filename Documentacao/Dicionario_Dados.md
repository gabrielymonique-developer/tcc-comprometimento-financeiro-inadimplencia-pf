# Dicionário de Dados

Este documento apresenta a descrição das principais variáveis utilizadas na construção da base consolidada e nas análises econométricas do projeto.

A base principal utilizada nas análises encontra-se em:

`Banco_dados/Processados/tb_modelo_final.csv`

O período analisado compreende **janeiro de 2020 a dezembro de 2025**, totalizando **72 observações mensais**.

---

## 1. Variáveis de identificação temporal

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `Ano` | Inteiro | Ano correspondente à observação. | `2025` |
| `dataref` | Inteiro | Identificador mensal no formato `AAAAMM`. É utilizado como chave para consolidação das diferentes bases. | `202512` |
| `trimestre` | Texto | Identificação do trimestre e ano da observação. | `4T2025` |

---

## 2. Variável dependente

### `inadimplencia`

**Descrição:** percentual de inadimplência da carteira de crédito destinada a Pessoas Físicas.

**Unidade:** Percentual (%)

**Fonte:** Banco Central do Brasil (BCB)

**Papel no modelo:** variável dependente (`Y`) dos modelos econométricos.

**Abreviação utilizada no estudo:** Inadimplência PF.

---

## 3. Variáveis explicativas

### `familias_endividadas`

**Descrição:** percentual de famílias que declararam possuir algum tipo de dívida.

**Unidade:** Percentual (%)

**Fonte:** Pesquisa de Endividamento e Inadimplência do Consumidor (PEIC), da Confederação Nacional do Comércio de Bens, Serviços e Turismo (CNC).

**Abreviação utilizada no estudo:** `FE`

**Papel no estudo:** principal variável associada ao comprometimento financeiro das famílias.

---

### `familias_atraso`

**Descrição:** percentual de famílias que declararam possuir contas ou dívidas em atraso.

**Unidade:** Percentual (%)

**Fonte:** Pesquisa de Endividamento e Inadimplência do Consumidor (PEIC/CNC).

**Abreviação utilizada no estudo:** `FA`

**Papel no estudo:** variável utilizada nas análises preliminares e nos processos de seleção de variáveis.

---

### `taxa_juros`

**Descrição:** taxa média de juros das operações de crédito destinadas a Pessoas Físicas.

**Unidade:** Percentual (%)

**Fonte:** Banco Central do Brasil (BCB)

**Abreviação utilizada no estudo:** `TJ`

**Papel no estudo:** representa as condições de custo do crédito enfrentadas pelas famílias.

---

### `carteira`

**Descrição:** saldo total da carteira de crédito destinada a Pessoas Físicas.

**Unidade:** R$ milhões

**Fonte:** Banco Central do Brasil (BCB)

**Papel no estudo:** variável utilizada nas análises exploratórias e na construção inicial dos modelos.

---

### `carteira_over90`

**Descrição:** saldo da carteira de crédito de Pessoas Físicas vencida há mais de 90 dias.

**Unidade:** R$ milhões

**Fonte:** variável construída a partir dos arquivos públicos do SCR.data, disponibilizados pelo Banco Central do Brasil.

**Abreviação utilizada no estudo:** `CA90`

**Papel no estudo:** variável explicativa utilizada no modelo principal.

A variável é construída pelo script:

`Codigos/01_preparacao_carteira_atraso.py`

e armazenada na base:

`Banco_dados/Processados/tb_carteira_atraso.csv`

---

### `carteira_15a90`

**Descrição:** saldo da carteira de crédito de Pessoas Físicas vencida entre 15 e 90 dias.

**Unidade:** R$ milhões

**Fonte:** variável construída a partir dos arquivos públicos do SCR.data, disponibilizados pelo Banco Central do Brasil.

**Abreviação utilizada no estudo:** `CA15-90`

**Papel no estudo:** utilizada em modelo complementar para comparação com a carteira vencida acima de 90 dias.

A variável é construída pelo script:

`Codigos/01_preparacao_carteira_atraso.py`

---

## 4. Variável de identificação do público

### `tipo_pessoa`

**Descrição:** identifica o tipo de cliente considerado na análise.

**Valor utilizado:**

`PF`

correspondente a **Pessoa Física**.

Os arquivos do SCR são filtrados para considerar exclusivamente operações associadas a Pessoas Físicas.

---

## 5. Variável construída durante a modelagem

### `trend`

A variável `trend` **não está armazenada originalmente na base `tb_modelo_final.csv`**.

Ela é criada durante a execução do script:

`Codigos/03_modelagem_econometrica.py`

e representa a sequência cronológica das observações mensais:

```text
Janeiro/2020   → 1
Fevereiro/2020 → 2
Março/2020     → 3
...
Dezembro/2025  → 72
```

**Tipo:** Inteiro

**Intervalo:** 1 a 72

**Papel no estudo:** utilizada em análises complementares para avaliar a presença de tendência temporal nas séries.

---

## 6. Resumo das variáveis

| Variável | Abreviação | Unidade | Fonte | Utilização |
|---|---|---|---|---|
| `inadimplencia` | Y | % | BCB | Variável dependente |
| `familias_endividadas` | FE | % | CNC/PEIC | Modelo principal |
| `familias_atraso` | FA | % | CNC/PEIC | Análises preliminares |
| `taxa_juros` | TJ | % | BCB | Modelo principal |
| `carteira_over90` | CA90 | R$ milhões | SCR.data/BCB | Modelo principal |
| `carteira_15a90` | CA15-90 | R$ milhões | SCR.data/BCB | Modelo complementar |
| `carteira` | — | R$ milhões | BCB | Análises exploratórias |
| `trend` | — | Índice temporal | Construída no código | Análise complementar |

---

## 7. Observação sobre nomenclatura

Ao longo da documentação e da interpretação dos resultados, algumas variáveis são apresentadas por meio de abreviações para facilitar a leitura:

- **FE** = Famílias Endividadas;
- **FA** = Famílias em Atraso;
- **TJ** = Taxa de Juros;
- **CA90** = Carteira vencida acima de 90 dias;
- **CA15-90** = Carteira vencida entre 15 e 90 dias.

Nos códigos e bancos de dados, entretanto, são utilizados os nomes completos das respectivas variáveis.