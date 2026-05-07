# Contributing

Este repositório é uma superfície pública de referência para estudantes. Contribuições devem melhorar clareza, precisão ou organização de material didático sem adicionar contexto privado de operação, atalhos de validação ou scaffolding de manutenção do repositório.

## Placement Rules

1. Coloque material didático reutilizável no caminho da fase, disciplina e aula correspondente.
2. Coloque material de live dentro da disciplina que ele apoia, usando uma pasta local `lives/`.
3. Coloque material de grupos de estudo em `fase-*/grupos-de-estudo/`.
4. Mantenha navegação, cobertura por turma e índices públicos em `docs/`.
5. Mantenha o histórico editorial no arquivo raiz `CHANGELOG.md`.
6. Mantenha definições de agentes, automações de workflow, harnesses de teste e ferramentas de manutenção fora deste repositório público.

## Content Rules

1. Não publique agendas privadas, follow-up de professores, evidências de email, tickets, notas ou identificadores de estudantes.
2. Não promova caches, checkpoints, traces de experimento, binários de modelo ou artefatos gerados, exceto quando forem exemplos didáticos pequenos e explicitamente documentados.
3. Prefira o README mais próximo da fase, disciplina ou aula em vez de documentação paralela.
4. Use rótulos de turma como proveniência de sessões datadas, não como modelo primário de navegação.
5. Explique comandos executáveis perto do material que eles executam; evite atalhos globais na raiz.

## Pull Request Checklist

Antes de publicar uma mudança, confirme que:

1. os links relativos funcionam a partir do arquivo editado;
2. o material novo tem README local suficiente para orientar o estudante;
3. dependências novas estão documentadas na fase adequada;
4. não há dados privados, outputs grandes ou artefatos gerados sem curadoria;
5. mudanças editoriais relevantes foram registradas no [CHANGELOG.md](CHANGELOG.md).
