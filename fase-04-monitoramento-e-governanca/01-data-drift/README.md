# 01 — Data Drift

> 8h de vídeo · 8 aulas

## Por que esta disciplina importa

Um modelo em produção degrada mesmo quando o código não muda. Esta disciplina torna explícito o problema da mudança de distribuição, do comportamento do usuário e do contexto operacional, ensinando como detectar, interpretar e reagir a drift de forma estruturada.

## O que você deve aprender

- diferenciar data drift, concept drift e label drift;
- aplicar testes estatísticos e indicadores de mudança de distribuição;
- usar ferramentas como Evidently e NannyML para relatórios e monitoramento;
- estruturar pipelines de alerta e estratégias de retraining;
- consolidar um projeto de drift como parte do sistema de produção.

## Como usar este material

1. Siga a sequência das aulas, porque a disciplina progride do conceito ao sistema operacionalizado.
2. Use os scripts estatísticos e dashboards para comparar abordagens de detecção.
3. Trate a aula de pipeline e alertas como ponte entre análise e resposta operacional.
4. Feche com o projeto integrador para enxergar drift como processo contínuo.

## Como referenciar esta disciplina no repositório

- O índice canônico está em `fase-04-monitoramento-e-governanca/01-data-drift/`.
- Cite a aula específica ao mencionar técnicas, ferramentas ou estratégias de resposta.
- Este README organiza o percurso e o propósito; scripts, notebooks e pipeline mostram a implementação prática.
- Regras de governança formal sobre operação e evidência devem ser consultadas no repositório principal.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Executivamente, drift é uma das causas mais frequentes de queda silenciosa de valor em produtos de ML. No ambiente acadêmico, a disciplina aproxima teoria estatística, observabilidade e desenho experimental contínuo, ajudando a tratar modelos como sistemas dinâmicos sujeitos a mudança de contexto.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-tipos-drift/) | Data/concept/label drift | `drift_simulator.py`, notebook |
| [02](aula02-testes-estatisticos/) | Testes estatísticos: KS, PSI, Chi², JS | `statistical_tests.py` |
| [03](aula03-evidently/) | Evidently: reports + dashboards | `evidently_reports.py` |
| [04](aula04-nannyml/) | NannyML: CBPE, estimativa sem labels | `nannyml_demo.py` |
| [05](aula05-drift-multivariado/) | Drift multivariado: MMD, autoencoder | `multivariate_drift.py` |
| [06](aula06-pipeline-alertas/) | Pipeline automatizado + alertas | `README.md`, `drift_pipeline.py`, notebook |
| [07](aula07-retraining/) | Retraining: periódico e trigger-based | `retraining_strategy.py` |
| [08](aula08-projeto-drift/) | Projeto completo de drift | notebook integrador |
