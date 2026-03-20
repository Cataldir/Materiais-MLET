# Aula 03 - Model cards para documentacao responsavel

Pacote canonico leve para apresentar model cards como artefato de governanca tecnica. A aula conecta contexto de negocio, dados, metricas, limites e riscos em um documento curto o bastante para circular entre times e robusto o bastante para apoiar auditoria e decisao.

## Objetivo didatico

- explicar o papel do model card como contrato de transparencia para modelos de ML;
- organizar informacoes essenciais de uso, metricas, limites e risco residual;
- preparar o aluno para documentacao responsavel sem repetir toda a disciplina de compliance.

## O que foi preservado

- foco em publico misto: produto, risco, dados e engenharia;
- ligacao entre performance, caso de uso e restricoes declaradas;
- linguagem de governanca aplicada a um artefato tecnico concreto.

## O que foi simplificado

- sem integracao com registry, lineage real ou banco de metadados;
- sem template institucional extenso ou fluxo formal de aprovacao;
- exemplo pequeno para priorizar clareza e leitura executiva.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/05-governanca-compliance/aula03-model-cards
python model_card_generator.py
```

## Arquivos

- `model_card_generator.py`: gera um model card em Markdown a partir de metadados simples.
- `03_model_cards_local.ipynb`: notebook local para revisar o artefato por perspectiva tecnica e executiva.
- `model_card_debug_walkthrough.py`: roteiro com checkpoints para walkthrough em grupo de estudo.

## Observacoes didaticas

- model card util precisa explicar onde o modelo ajuda e onde ele nao deve ser usado;
- documentacao boa reduz ruído entre aprovacao executiva e manutencao tecnica.

## Exercicios progressivos

- Iniciante: remova um campo de `MODEL_CARD` e identifique qual secao minima de governanca fica incompleta.
- Intermediario: adicione um campo como `owner` ou `publico_afetado` e estenda o render para explicitar accountability.
- Avancado: valide automaticamente se toda secao minima exigida aparece no texto renderizado antes da publicacao.

## Caminho de debug

- Rode `python model_card_debug_walkthrough.py` para inspecionar o dicionario de entrada, o contrato de secoes minimas e o Markdown final.
- Checkpoint 1: revisar os metadados brutos antes do render.
- Checkpoint 2: confirmar as secoes exigidas antes da validacao.
- Checkpoint 3: comparar card renderizado com a saida validada.