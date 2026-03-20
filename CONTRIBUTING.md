# Contribuindo com o Materiais-MLET

Este clone local está sendo usado para curadoria editorial da branch `canonica`, com foco em materiais executáveis e na normalização da primeira onda de ativos migrados.

## Escopo desta clone

- `canonica` é a linha de base editorial.
- `main` é downstream e não deve receber material bruto vindo da migração.
- O objetivo aqui é publicar o menor baseline reutilizável por aula, disciplina ou overlay de evento.

## Regras para ativos migrados

1. Preserve a taxonomia já existente por fase e aula.
2. Prefira mover apenas o baseline executável e compreensível, não o branch legado inteiro.
3. Se um ativo exigir contexto extra para ser entendido, ajuste o `README.md` mais próximo em vez de criar documentação paralela desnecessária.
4. Não promova caches, artefatos de treino, rastros de experimentos, checkpoints ou dados pesados como parte do baseline canônico.
5. Ao encontrar mais de uma variante do mesmo material, mantenha apenas a menor versão útil para curadoria inicial e deixe extensões para uma etapa posterior.

## Checklist mínimo antes de promover material

- [ ] O material foi encaixado em uma fase e aula já existentes.
- [ ] O caminho principal de execução está explícito no README da fase, disciplina ou aula.
- [ ] Não há resíduos locais de experimento, cache, modelos treinados ou dados pesados.
- [ ] O conteúdo alterado foi validado localmente com o fluxo leve abaixo.

## Validação leve

Use um destes caminhos antes de concluir a curadoria:

```bash
make validate-bootstrap
python tools/repo_tasks.py validate
```

ou, quando quiser validar somente os arquivos tocados:

```bash
python tools/repo_tasks.py validate README.md CONTRIBUTING.md .pre-commit-config.yaml Makefile
```

Para validar notebooks sem execução pesada:

```bash
make notebooks-check
python tools/repo_tasks.py notebooks-check
```

## O que não fazer nesta etapa

- Não reestruture o repositório inteiro.
- Não adicione CI pesada ou automações novas sem necessidade clara.
- Não use `main` como branch editorial.
- Não importe ativos legados com diretórios gerados apenas para "não perder nada".
