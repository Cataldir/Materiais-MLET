# Aula 05 - Formatacao e naming como contrato coletivo

Pack canonico para mostrar que padroes de formatacao nao servem apenas para estilo, mas para reduzir atrito de revisao e facilitar manutencao. A aula aplica um conjunto pequeno de comandos transformadores sobre snippets de codigo problematico.

## O que foi preservado

- leitura de PEP 8, snake_case e higiene de whitespace;
- raciocinio de automacao com comandos encadeados;
- comparacao antes e depois da padronizacao.

## O que foi simplificado

- sem rodar black ou ruff format de verdade dentro do exemplo;
- sem AST complexo ou reescrita completa de arquivos;
- foco em principios de normalizacao e legibilidade.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula05-formatacao
python formatting_workflow.py
```

## Arquivos

- `formatting_workflow.py`: aplica uma fila de comandos de formatacao sobre snippets locais.

## Observacoes didaticas

- formatacao padronizada libera energia do time para discutir arquitetura e comportamento;
- naming bom e parte do design da API interna, nao apenas cosmetica.