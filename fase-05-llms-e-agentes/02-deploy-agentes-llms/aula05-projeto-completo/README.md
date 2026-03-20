# Aula 05 - Projeto completo local de assistente

Projeto integrador local com planner por regras, recuperacao documental simples, tool use deterministico e notebook fino apontando para o mesmo caminho de execucao.

## Objetivo didatico

- compor planner, retriever e tools em um assistente unico;
- manter todo o fluxo reproduzivel e seguro para uso offline;
- mostrar como um projeto end-to-end pode nascer sem depender de SaaS.

## Execucao

```bash
cd fase-05-llms-e-agentes/02-deploy-agentes-llms/aula05-projeto-completo
python assistant_project.py
```

## Arquivos

- `assistant_project.py`: assistente end-to-end com componentes locais.
- `05_projeto_completo_local.ipynb`: notebook fino reutilizando o mesmo modulo.

## Observacoes didaticas

- o planner decide se a consulta exige politica, agenda ou calculo operacional;
- o retriever consulta fatos internos curtos e controlados;
- tools sao explicitamente registradas para evitar execucao arbitraria.