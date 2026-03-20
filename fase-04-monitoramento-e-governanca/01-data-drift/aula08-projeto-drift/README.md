# Aula 08 - Projeto completo de drift

Pacote integrador notebook-first para consolidar deteccao, triagem e resposta a drift em um fluxo unico e local. O notebook usa um modulo auxiliar pequeno para montar o resumo executivo e manter o material executavel por smoke test sem depender de servicos externos.

## Objetivo didatico

- integrar monitoramento univariado, severidade operacional e recomendacao de resposta;
- praticar leitura de um resumo de projeto antes de expandir para dashboards completos;
- oferecer um notebook local como artefato principal da aula de projeto.

## O que foi preservado

- notebook como artefato central da aula;
- helper module local para manter a logica reutilizavel e testavel;
- janelas sinteticas com progressao de severidade e playbook de resposta.

## O que foi simplificado

- sem armazenamento historico nem rotas HTTP;
- sem dependencias obrigatorias alem de `numpy` e `pandas`;
- projeto reduzido a um ciclo deterministico de referencia, avaliacao e recomendacao.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/01-data-drift/aula08-projeto-drift
python drift_project.py
```

Abra tambem o notebook `08_projeto_drift_local.ipynb` para a versao guiada da mesma sequencia.

## Arquivos

- `drift_project.py`: helper module do projeto integrador.
- `08_projeto_drift_local.ipynb`: notebook principal da aula.

## Observacoes didaticas

- o projeto foi desenhado para ser pequeno o suficiente para testes, mas completo o bastante para discutir operacao;
- as janelas representam backlog de investigacao e resposta escalonada;
- o mesmo helper pode ser expandido para integrar ferramentas da disciplina anterior.