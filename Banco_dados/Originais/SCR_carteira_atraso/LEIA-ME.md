# Arquivos Brutos do SCR.data

Este diretório é destinado ao armazenamento dos arquivos mensais brutos do **SCR.data**, disponibilizados pelo Banco Central do Brasil.

Os arquivos foram utilizados para construção das variáveis referentes à carteira de crédito de Pessoas Físicas em atraso.

---

## Arquivos utilizados no estudo

O período analisado compreende:

**Janeiro de 2020 a Dezembro de 2025**

Foram utilizados **72 arquivos mensais em formato CSV**, seguindo estrutura semelhante a:

```text
scrdata_202001.csv
scrdata_202002.csv
scrdata_202003.csv
...
scrdata_202512.csv
```

O conjunto utilizado no estudo possui aproximadamente **6,29 GB**.

Por esse motivo, os arquivos brutos **não são armazenados neste repositório**.

---

## Como reproduzir esta etapa

Para executar o processamento completo da carteira em atraso:

1. obtenha os arquivos mensais do SCR.data na fonte oficial;
2. armazene os arquivos `.csv` neste diretório;
3. execute o script:

`Codigos/01_preparacao_carteira_atraso.py`

O script localizará automaticamente os arquivos presentes nesta pasta e realizará o tratamento necessário.

---

## Arquivo gerado

Após o processamento, será criada a base:

`Banco_dados/Processados/tb_carteira_atraso.csv`

Essa base contém, entre outras informações:

- carteira vencida entre 15 e 90 dias;
- carteira vencida acima de 90 dias.

Os valores são consolidados mensalmente para **Pessoas Físicas (PF)** e expressos em **R$ milhões**.

---

## Alternativa para reprodução

Caso o objetivo seja reproduzir apenas a consolidação, modelagem econométrica e análises posteriores, não é necessário processar os arquivos brutos do SCR.

A base já processada é disponibilizada diretamente no repositório:
`Banco_dados/Processados/tb_carteira_atraso.csv`