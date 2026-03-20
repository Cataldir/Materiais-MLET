# Aula 05 - Projeto de seguranca com politicas locais

Projeto integrador local com pipeline de enforcement, mascaramento simples de PII, verificacao de prompt injection e auditoria em memoria.

## Objetivo didatico

- aplicar politicas em cadeia antes da resposta final;
- gerar trilha de auditoria para cada decisao;
- discutir seguranca por desenho sem qualquer servico remoto.

## Execucao

```bash
cd fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula05-projeto-seguranca
python security_project.py
```

## Arquivos

- `security_project.py`: pipeline local de enforcement e auditoria.
- `05_projeto_seguranca_local.ipynb`: notebook fino reutilizando o mesmo fluxo.

## Observacoes didaticas

- a politica primeiro normaliza, depois detecta risco e so entao decide;
- logs de auditoria registram o motivo da decisao;
- o fluxo evita execucao de tools perigosas por regra estatica.