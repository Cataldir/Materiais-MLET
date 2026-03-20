# Aula 02 - Guardrails para reduzir risco operacional

Pacote canonico leve para apresentar guardrails como camada de controle em sistemas com LLMs e agentes. A aula mostra como regras simples de entrada e saida ajudam a conter pedidos indevidos, vazamento de PII e respostas fora de politica antes de discutir stacks mais completas.

## Objetivo didatico

- explicar o papel de guardrails como defesa pragmatica em fluxos generativos;
- diferenciar bloqueio, sanitizacao e liberacao monitorada;
- conectar seguranca de prompt a valor executivo de confianca e conformidade.

## O que foi preservado

- cenarios reais de prompt injection, PII e pedido fora de escopo;
- leitura operacional de decisao por politica aplicada ao request;
- foco em controles de entrada e saida como requisito de produto.

## O que foi simplificado

- sem dependencia de provedores externos, modelos hospedados ou frameworks de guardrail;
- sem classificadores complexos ou moderacao baseada em API;
- regras locais e explicaveis para facilitar teste e debate.

## Execucao

```bash
cd fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula02-guardrails
python guardrails_demo.py
```

## Arquivos

- `guardrails_demo.py`: aplica politicas locais de bloqueio e sanitizacao a prompts sinteticos.
- `02_guardrails_local.ipynb`: notebook local para testar cenarios de allow, sanitize e block.
- `guardrails_debug_walkthrough.py`: roteiro com checkpoints para uso em grupo de estudo e depuracao guiada.

## Observacoes didaticas

- guardrail bom nao substitui arquitetura segura, mas reduz superficie de falha previsivel;
- o controle precisa ser observavel para auditoria, ajuste e prestacao de contas.

## Exercicios progressivos

- Iniciante: acrescente um prompt claramente seguro e outro claramente malicioso e preveja o resultado antes de executar.
- Intermediario: crie um prompt util com CPF e justifique por que `sanitize` e melhor do que `block` nesse caso.
- Avancado: introduza um estado `review` para prompts ambiguos e desenhe uma regra simples de escalonamento humano.

## Caminho de debug

- Rode `python guardrails_debug_walkthrough.py` para seguir o fluxo de classificacao prompt a prompt.
- Checkpoint 1: inspecionar `lowered` e a politica acionada.
- Checkpoint 2: observar a lista incremental de decisoes.
- Checkpoint 3: comparar saida final, justificativa e redacao sanitizada.