# Aula 06 - Projeto integrador end-to-end

Pack canonico para consolidar a disciplina em um fluxo unico: preparar dados, comparar candidatos, selecionar o modelo campeao e gerar um mini model card. A ideia e dar ao estudante um ponto de chegada estruturado para a fase de fundamentos.

## O que foi preservado

- comparacao entre familias de modelos no mesmo dataset;
- visao de pipeline completo, de dados ate artefato de comunicacao tecnica;
- organizacao por facade para esconder detalhes operacionais do fluxo.

## O que foi simplificado

- sem notebook pesado nem persistencia de artefatos em disco;
- sem tuning exaustivo ou dependencia de tracking externo;
- foco em uma experiencia local e rapida para fechamento da disciplina.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/aula06-projeto-integrador
python integrated_model_project.py
```

## Arquivos

- `integrated_model_project.py`: builder de configuracao e facade do fluxo end-to-end.

## Observacoes didaticas

- a aula mostra como organizar um estudo comparativo sem espalhar logica por varias celulas;
- o model card final ajuda a transformar experimento em comunicacao tecnica reutilizavel.