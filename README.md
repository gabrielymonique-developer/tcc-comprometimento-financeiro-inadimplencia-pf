# TCC – Inadimplência e comprometimento financeiro das famílias: abordagem de Data Science aplicada ao risco de crédito

Este repositório contém os bancos de dados, códigos e documentação utilizados no desenvolvimento do Trabalho de Conclusão de Curso (TCC) **“Inadimplência e comprometimento financeiro das famílias: abordagem de Data Science aplicada ao risco de crédito”**, desenvolvido no MBA em Data Science e Analytics.

O objetivo deste ambiente é permitir a **consulta, rastreabilidade e reprodução das análises realizadas no estudo**.

O período analisado compreende **janeiro de 2020 a dezembro de 2025**, totalizando **72 observações mensais**.

---

## 1. Estrutura do Repositório

```text
TCC_GitHub/
│
├── Banco_dados/
│   │
│   ├── Originais/
│   │   ├── SCR_carteira_atraso/
│   │   ├── tb_carteira_credito.xlsx
│   │   ├── tb_familias_endividadas.xlsx
│   │   ├── tb_inadimplencia.xlsx
│   │   └── tb_taxa_juros.xlsx
│   │
│   └── Processados/
│       ├── tb_carteira_atraso.csv
│       └── tb_modelo_final.csv
│
├── Codigos/
│   ├── 01_preparacao_carteira_atraso.py
│   ├── 02_consolidacao_base.py
│   ├── 03_modelagem_econometrica.py
│   └── 04_objetos_visuais.py
│
├── Documentacao/
│   ├── Fontes_Dados.md
│   └── Dicionario_Dados.md
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 2. Bancos de Dados

Os dados utilizados no estudo são provenientes de fontes públicas e foram organizados em duas categorias.

### Dados originais

Disponíveis em: `Banco_dados/Originais/`

Essa pasta contém as bases utilizadas como entrada para construção da base consolidada do modelo.

Entre as principais fontes estão:

- Banco Central do Brasil (BCB);
- Sistema de Informações de Crédito – SCR.data;
- Pesquisa de Endividamento e Inadimplência do Consumidor (PEIC), da Confederação Nacional do Comércio de Bens, Serviços e Turismo (CNC).

Informações detalhadas sobre as fontes estão disponíveis em:

`Documentacao/Fontes_Dados.md`

---

### Dados processados

Disponíveis em: `Banco_dados/Processados/`

Essa pasta contém as bases geradas durante o processamento dos dados.

**Principais arquivos:**
#### `tb_carteira_atraso.csv`

Base construída a partir dos arquivos mensais do SCR.data, contendo principalmente: carteira vencida entre 15 e 90 dias e carteira vencida acima de 90 dias.

#### `tb_modelo_final.csv`

Base consolidada utilizada nas análises exploratórias e nos modelos econométricos.


---

## 3. Observação sobre os Arquivos do SCR.data

Os arquivos brutos do SCR utilizados para construção das variáveis de carteira em atraso totalizam aproximadamente **6,29 GB**, considerando os 72 arquivos mensais utilizados no estudo.

Por esse motivo, esses arquivos **não são armazenados neste repositório**.

O usuário que desejar reproduzir integralmente essa etapa deverá obter os arquivos na fonte oficial e armazená-los em:

`Banco_dados/Originais/SCR_carteira_atraso/`

Após a inclusão dos arquivos, execute:

`Codigos/01_preparacao_carteira_atraso.py`

O script gerará:

`Banco_dados/Processados/tb_carteira_atraso.csv`

Para permitir a reprodução das etapas seguintes sem a necessidade de processamento dos 72 arquivos originais, a base `tb_carteira_atraso.csv` já processada é disponibilizada neste repositório.

---

## 4. Códigos

Os códigos foram organizados conforme a sequência de execução do projeto.

### 01 – Preparação da carteira em atraso

`Codigos/01_preparacao_carteira_atraso.py`

Responsável por:

- leitura dos arquivos mensais do SCR.data;
- seleção das operações referentes a Pessoas Físicas;
- consolidação das faixas de atraso;
- construção das variáveis de carteira vencida;
- geração da base `tb_carteira_atraso.csv`.

---

### 02 – Consolidação da base

`Codigos/02_consolidacao_base.py`

Responsável pela combinação das diferentes fontes de dados utilizando `dataref` como chave temporal.

O script gera:

`Banco_dados/Processados/tb_modelo_final.csv`

---

### 03 – Modelagem econométrica

`Codigos/03_modelagem_econometrica.py`

Contém as principais análises estatísticas e econométricas utilizadas no estudo, incluindo:

- análise de correlação;
- diagnóstico de multicolinearidade por VIF;
- estimação dos modelos por OLS;
- seleção de variáveis por Backward Elimination;
- análise complementar com tendência temporal;
- teste de normalidade dos resíduos;
- teste de heterocedasticidade de Breusch-Pagan;
- análise de autocorrelação serial;
- estimação do modelo principal com erros-padrão robustos HAC/Newey-West;
- modelo complementar utilizando a carteira vencida entre 15 e 90 dias.

---

### 04 – Objetos visuais

`Codigos/04_objetos_visuais.py`

Responsável pela geração das principais visualizações utilizadas nas análises, incluindo:

- evolução temporal padronizada das variáveis por Z-score;
- gráficos de dispersão;
- retas de regressão linear.

---

## 5. Ordem de Execução

Para reprodução completa do fluxo:

```text
01_preparacao_carteira_atraso.py
        ↓
tb_carteira_atraso.csv
        ↓
02_consolidacao_base.py
        ↓
tb_modelo_final.csv
        ↓
03_modelagem_econometrica.py
        ↓
Modelos e testes estatísticos
        ↓
04_objetos_visuais.py
        ↓
Visualizações das análises
```

### Reprodução sem os arquivos brutos do SCR

Como `tb_carteira_atraso.csv` já está disponibilizada na pasta de dados processados, o usuário pode iniciar a reprodução a partir de: `02_consolidacao_base.py`, sem executar o Código 01.

---

## 6. Ambiente de Execução

O projeto foi desenvolvido e validado utilizando:

- **Python 3.14**
- ambiente virtual Python (`venv`)
- sistema operacional Windows

As principais dependências utilizadas estão registradas no arquivo:

`requirements.txt`

---

## 7. Instalação das Dependências

Recomenda-se criar um ambiente virtual antes da instalação das bibliotecas.

Após configurar o ambiente Python, execute:

```bash
pip install -r requirements.txt
```

As versões utilizadas durante a validação deste repositório estão fixadas no arquivo `requirements.txt`.

---

## 8. Principais Variáveis

Entre as principais variáveis utilizadas no estudo estão:

| Variável | Abreviação | Descrição |
|---|---|---|
| `inadimplencia` | Y | Inadimplência da carteira de Pessoas Físicas |
| `familias_endividadas` | FE | Percentual de famílias endividadas |
| `familias_atraso` | FA | Percentual de famílias com contas ou dívidas em atraso |
| `taxa_juros` | TJ | Taxa média de juros para Pessoas Físicas |
| `carteira_over90` | CA90 | Carteira vencida acima de 90 dias |
| `carteira_15a90` | CA15-90 | Carteira vencida entre 15 e 90 dias |
| `carteira` | — | Saldo da carteira de crédito de Pessoas Físicas |

Para detalhes adicionais, consulte: `Documentacao/Dicionario_Dados.md`

---

## 9. Documentação Complementar

Informações adicionais estão disponíveis nos seguintes documentos:

### Fontes dos dados

`Documentacao/Fontes_Dados.md`

Apresenta as fontes utilizadas, periodicidade, período analisado e informações necessárias para reprodução da coleta e preparação dos dados.

### Dicionário de dados

`Documentacao/Dicionario_Dados.md`

Apresenta a descrição, unidade, origem e utilização das principais variáveis do estudo.

---

## 10. Finalidade

Este repositório foi desenvolvido como material complementar ao Trabalho de Conclusão de Curso e possui finalidade **acadêmica e de reprodutibilidade científica**.

Os dados utilizados são provenientes de fontes públicas, conforme detalhado na documentação do projeto.