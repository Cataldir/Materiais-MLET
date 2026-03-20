# 01 — Ciclo de Vida de Modelos

> 5h de vídeo · 5 aulas

## Por que esta disciplina importa

Grande parte dos problemas em ML nasce antes do algoritmo. Esta disciplina mostra que um modelo útil depende de contexto de negócio, qualidade de dados, baseline, critério de avaliação, estratégia de deploy e mecanismo de acompanhamento após a publicação. Ela introduz a visão sistêmica que sustenta todo o restante da formação.

## O que você deve aprender

- traduzir uma necessidade de negócio em hipótese de modelagem e critérios de sucesso;
- montar baselines e registrar experimentos de forma comparável;
- estruturar pipelines de treino e documentação mínima de modelo;
- diferenciar padrões de deploy batch e real-time;
- reconhecer sinais iniciais de drift e a necessidade de monitoramento contínuo.

## Como usar este material

1. Comece pela aula de entendimento de negócio para alinhar problema, dados e métrica.
2. Siga para experimentos e pipeline para entender como a solução amadurece tecnicamente.
3. Use as aulas de deploy e drift como ponte entre modelagem e operação.
4. Trate scripts e notebooks como exemplos de raciocínio operacional, não apenas de execução isolada.

## Como referenciar esta disciplina no repositório

- Use este README como índice principal da disciplina dentro da Fase 01.
- Ao citar o conteúdo da disciplina, aponte para a pasta `fase-01-fundamentos-de-ml/01-ciclo-de-vida-de-modelos/`.
- Quando a referência for uma prática específica, cite a aula correspondente, porque cada pasta representa um recorte claro do ciclo de vida.
- Regras acadêmicas, rubricas e processos não vivem aqui; para isso, consulte a governança canônica do repositório principal.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

No cotidiano profissional, essa disciplina ajuda a evitar times que otimizam modelos sem clareza de objetivo, sem baseline e sem plano de operação. Em termos acadêmicos, ela consolida a noção de pipeline sociotécnico: modelagem é apenas uma etapa dentro de um sistema maior, cujo desempenho depende de desenho experimental, rastreabilidade e critérios explícitos de validação.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-entendimento-negocio/) | ML Canvas e Data Readiness | `ml_canvas_exercicio.py`, notebook |
| [02](aula02-experimentos/) | Baseline Models e Experiment Tracking | `baseline_model.py`, `experiment_logging.py`, notebook |
| [03](aula03-pipeline-otimizacao/) | Pipeline Sklearn, Otimização, Model Card | `pipeline_sklearn.py`, `model_card_template.py`, notebook |
| [04](aula04-deploy-batch-realtime/) | Deploy Batch e Real-Time, Canary, A/B | `batch_inference.py`, `realtime_inference.py` |
| [05](aula05-drift-cicd/) | Drift Conceitual, Monitoramento, CI/CD Intro | `drift_detection.py`, `simulate_drift.py` |
