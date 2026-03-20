# Aula 02 - SRP e refatoracao incremental

Pack local para demonstrar como uma funcao de scoring em ML pode ser quebrada em responsabilidades menores sem alterar o resultado final. A aula usa Extract Method e Single Responsibility Principle para separar normalizacao, calculo de risco, classificacao e recomendacao.

## Objetivo didatico

- mostrar como uma funcao unica acumula regras demais rapidamente;
- preservar comportamento enquanto a estrutura fica mais legivel;
- evidenciar como pequenas funcoes facilitam teste, reuso e manutencao.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/01-clean-code-ml/aula02-srp-refatoracao
python srp_example.py
```

## Arquivos

- `srp_example.py`: compara a implementacao legada e a refatorada usando o mesmo caso de teste.

## Observacoes didaticas

- a refatoracao nao muda a regra de negocio, apenas sua organizacao;
- o ganho principal aqui e tornar cada etapa explicitamente nomeada;
- o mesmo padrao vale para preprocessing, validacao e regras de promocao de modelo.