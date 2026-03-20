# Aula 06 - Projeto completo de inferencia causal

Pacote integrador notebook-first para consolidar DAG, uplift e prescricao em um fluxo unico. O notebook usa um modulo auxiliar pequeno para gerar um resumo executivo local, com artefatos suficientes para estudo, smoke tests e iteracao futura.

## Objetivo didatico

- integrar modelagem causal, efeito incremental e recomendacao operacional;
- fechar a disciplina com um artefato principal em notebook e um helper testavel;
- mostrar como traduzir resultado causal em backlog de acao e evidencia.

## O que foi preservado

- notebook como interface principal do projeto;
- helper module para consolidar o workflow causal;
- saida serializavel com prioridades e notas de governanca.

## O que foi simplificado

- sem pipeline de dados externo;
- sem dashboards ou servicos remotos;
- foco em um resumo deterministico e facil de expandir.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/06-inferencia-causal/aula06-projeto-completo
python causal_project.py
```

Abra tambem o notebook `06_projeto_completo_local.ipynb` para a sequencia guiada.

## Arquivos

- `causal_project.py`: helper module do projeto final.
- `06_projeto_completo_local.ipynb`: notebook principal.

## Observacoes didaticas

- o helper foi mantido local para reduzir friccao durante a aula;
- o projeto fecha a disciplina conectando modelagem, estimacao e acao;
- a nota de governanca reforca que evidencia e monitoramento devem acompanhar a decisao.