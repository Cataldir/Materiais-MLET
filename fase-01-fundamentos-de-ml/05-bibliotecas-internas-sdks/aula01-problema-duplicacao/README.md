# Aula 01 - Por que duplicacao vira custo de plataforma

Pacote canonico leve para enquadrar o problema que antecede a criacao de bibliotecas internas. A aula mostra que duplicacao em pipelines, validacoes e contratos de inferencia aumenta custo de manutencao, desacelera correcao de bugs e dificulta padronizacao entre squads.

## Objetivo didatico

- identificar duplicacao estrutural antes de discutir empacotamento;
- conectar retrabalho tecnico a custo operacional e risco de inconsistencia;
- preparar o terreno para abstrair apenas o que tem valor recorrente.

## O que foi preservado

- exemplos proximos da rotina de ML com preprocessamento, treino e scoring;
- comparacao entre fluxos parecidos mantidos por times diferentes;
- leitura executiva do problema antes da solucao em pacote reutilizavel.

## O que foi simplificado

- sem build, distribuicao ou publicacao de biblioteca;
- sem multiplos repositorios ou dependencia de infraestrutura externa;
- foco no diagnostico do problema, nao na engenharia de release.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula01-problema-duplicacao
python duplication_problem.py
```

## Arquivos

- `duplication_problem.py`: identifica hotspots de duplicacao entre pipelines ficticios de ML.
- `01_problema_duplicacao_local.ipynb`: notebook local com a mesma leitura executiva do script.

## Observacoes didaticas

- o ganho executivo aparece quando o time reduz divergencia entre implementacoes quase identicas;
- a abstracao deve nascer de repeticao recorrente, nao de preferencia estetica.