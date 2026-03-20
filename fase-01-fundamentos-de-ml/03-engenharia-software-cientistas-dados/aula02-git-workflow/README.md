# Aula 02 - Git workflow para projetos de ML

Pack canonico para ensinar fluxo de branch, commit, PR e merge sem depender de um repositorio remoto real. A aula traduz o processo de colaboracao em comandos deterministas para que o aluno entenda estado, transicao e criterio de prontidao.

## O que foi preservado

- sequencia logica de branch feature, stage, commit, PR e merge;
- leitura de boas praticas de colaboracao para codigo de dados;
- uso do padrao Command para representar passos do workflow.

## O que foi simplificado

- sem chamada real a GitHub, GitLab ou DVC;
- sem side effects no repositorio do aluno;
- foco em estados e guardrails do fluxo, nao em integracoes externas.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/03-engenharia-software-cientistas-dados/aula02-git-workflow
python git_workflow_demo.py
```

## Arquivos

- `git_workflow_demo.py`: workflow local modelado por comandos executaveis em memoria.

## Observacoes didaticas

- a aula ajuda a enxergar Git como processo de colaboracao, nao apenas como lista de comandos;
- o mesmo raciocinio vale para notebooks, scripts e pipelines versionados em ML.