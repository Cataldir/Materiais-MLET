# Fase 05 — LLMs e Agentes

> ~22h de vídeo · 5 disciplinas · ~22 aulas

## Por que esta fase importa

Esta fase fecha a jornada aplicando fundamentos de engenharia de ML a sistemas generativos, agentes e fluxos orientados por modelos de linguagem. O foco não é tratar LLM como exceção mágica, mas como mais uma classe de sistema que precisa de serving, avaliação, observabilidade, escalabilidade e segurança.

## Ao concluir esta fase, você deve ser capaz de

- servir modelos generativos com critérios explícitos de custo, latência e capacidade;
- estruturar agentes com ferramentas, memória, RAG e APIs de produção;
- projetar aplicações avançadas com escalabilidade e controle de estado;
- avaliar sistemas generativos com métricas apropriadas e observabilidade dedicada;
- reduzir risco com guardrails, mecanismos de segurança e conformidade.

## Relação com o Tech Challenge

O desafio final exige maturidade acumulada das fases anteriores: empacotar, servir, observar e governar um sistema mais incerto e probabilístico. A fase mostra como transformar protótipos de IA generativa em produtos defensáveis do ponto de vista técnico, operacional e reputacional.

## Como navegar nesta fase

1. Comece por Deploy de Modelos de IA Generativa para entender serving e otimização.
2. Avance para Agentes com LLMs para orquestração, ferramentas e integração.
3. Use Aplicações Avançadas e Escalabilidade para tratar estado, concorrência e arquitetura.
4. Feche com Avaliação/Observabilidade e Segurança/Conformidade para completar o ciclo de LLMOps.
5. Para regras institucionais e critérios formais, use o [Resumo dos Tech Challenges](../../../governanca/resumo-tech-challenges.md) e a governança canônica do repositório principal.

## Disciplinas

| # | Nome | Papel na fase | Aulas |
|---|------|---------------|-------|
| [01](01-deploy-modelos-ia-generativa/README.md) | Deploy de Modelos de IA Generativa | servir e otimizar modelos generativos | 3 |
| [02](02-deploy-agentes-llms/README.md) | Deploy de Agentes com LLMs | operacionalizar agentes com tools e RAG | 5 |
| [03](03-aplicacoes-avancadas-escalabilidade/README.md) | Aplicações Avançadas e Escalabilidade | escalar fluxos multiagente e stateful | 4 |
| [04](04-avaliacao-observabilidade-llmops/README.md) | Avaliação e Observabilidade em LLMOps | medir qualidade, custo e rastreabilidade | 5 |
| [05](05-seguranca-guardrails-conformidade/README.md) | Segurança, Guardrails e Conformidade | controlar risco técnico e regulatório | 5 |

## Cobertura editorial disponível

- [01](01-deploy-modelos-ia-generativa/README.md): fundamentos de LLMs, serving com vLLM/TGI e otimização.
- [02](02-deploy-agentes-llms/README.md): agentes ReAct, LangChain/LangGraph, RAG, tools e API.
- [03](03-aplicacoes-avancadas-escalabilidade/README.md): multiagentes, memória, estado e escala.
- [04](04-avaliacao-observabilidade-llmops/README.md): métricas, avaliação automatizada, tracing e custo/latência.
- [05](05-seguranca-guardrails-conformidade/README.md): riscos, guardrails, prompt injection e compliance com PII.

## Setup

```bash
make install-fase05
# ou
uv pip install -e ".[fase05,dev]"
```

## Requisitos de hardware

- Deploy de LLMs: GPU recomendada para cenários locais mais pesados.
- Agentes e aplicações avançadas: CPU adequada pode ser suficiente quando os modelos estão por API.
- Avaliação e observabilidade: acesso de rede e credenciais de APIs podem ser necessários em alguns exemplos.
