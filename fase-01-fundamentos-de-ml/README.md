# Fase 01 — Fundamentos de ML

> ~26h de vídeo · 5 disciplinas · ~26 aulas

## Por que esta fase importa

Esta fase constrói a base que separa experimentação casual de engenharia de ML de fato. O estudante começa entendendo problema de negócio, hipóteses, dados, modelos e critérios de qualidade, e termina com repertório suficiente para estruturar soluções que já nascem com preocupação de reprodutibilidade, APIs e reutilização de código.

## Ao concluir esta fase, você deve ser capaz de

- explicar o ciclo de vida completo de um modelo, do entendimento do problema à operação inicial;
- selecionar e comparar abordagens clássicas de modelagem com critérios técnicos defensáveis;
- aplicar fundamentos de engenharia de software a projetos de ciência de dados;
- expor inferência por APIs e organizar código reutilizável em bibliotecas e SDKs;
- preparar a base técnica que será endurecida nas fases seguintes em versionamento, deploy e governança.

## Relação com o Tech Challenge

A Fase 01 prepara o aluno para transformar um problema mal definido em uma solução minimamente estruturada, com baseline, hipótese explícita e artefatos compreensíveis por terceiros. Esse é o primeiro passo para um Tech Challenge sólido: antes de automatizar, é preciso saber o que resolver, como medir sucesso e como empacotar a lógica principal com clareza.

## Como navegar nesta fase

1. Comece por Ciclo de Vida de Modelos para alinhar produto, dados e operação.
2. Avance para Fundamentos de Modelos de ML para consolidar repertório técnico de modelagem.
3. Use Engenharia de Software, APIs e SDKs como ponte entre notebook exploratório e material reutilizável.
4. Desça para as aulas quando precisar executar scripts, notebooks e exemplos específicos.
5. Para regras institucionais de material e referência, consulte o [Guia 007](../../../governanca/04-guias/07-guia-de-materiais-tecnico-pedagogicos-executaveis.md) e o [Guia 008](../../../governanca/04-guias/08-guia-de-referenciais-teoricos-por-disciplina.md).

## Disciplinas

| # | Nome | Papel na fase | Aulas |
|---|------|---------------|-------|
| [01](01-ciclo-de-vida-de-modelos/README.md) | Ciclo de Vida de Modelos | conectar negócio, dados, experimentação e operação | 5 |
| [02](02-fundamentos-modelos-ml/README.md) | Fundamentos de Modelos de ML | consolidar bases estatísticas e algorítmicas | 6 |
| [03](03-engenharia-software-cientistas-dados/README.md) | Engenharia de Software para Cientistas de Dados | profissionalizar código analítico | 5 |
| [04](04-apis-inferencia-modelos/README.md) | APIs para Inferência de Modelos | expor modelos como serviço | 4 |
| [05](05-bibliotecas-internas-sdks/README.md) | Bibliotecas Internas e SDKs | transformar soluções em ativos reaproveitáveis | 6 |

## Cobertura editorial disponível

- [01](01-ciclo-de-vida-de-modelos/README.md): trilha de entendimento de negócio, experimentos, pipelines, deploy batch e real-time, drift e introdução a CI/CD.
- [02](02-fundamentos-modelos-ml/README.md): fundamentos de regressão, ensembles, métricas, validação e referências adicionais para supervisionado e clustering.
- [03](03-engenharia-software-cientistas-dados/README.md): exemplos de SOLID, testes, qualidade, gestão de dependências e CLI.
- [04](04-apis-inferencia-modelos/README.md): APIs introdutórias e fluxo completo de serving com testes.
- [05](05-bibliotecas-internas-sdks/README.md): empacotamento de utilitários, documentação, versionamento e integração com fluxos de ML.

## Setup

```bash
make install-fase01
# ou
uv pip install -e ".[fase01,dev]"
```

## Datasets desta fase

- **Titanic**: classificação tabular e exemplos introdutórios.
- **California Housing**: regressão com dataset público do `sklearn`.
- **Iris**: baseline clássico para classificação multiclasse.
