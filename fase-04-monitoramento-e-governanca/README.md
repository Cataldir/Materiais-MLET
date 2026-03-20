# Fase 04 — Monitoramento e Governança

> ~28h de vídeo · 6 disciplinas · ~24 aulas

## Por que esta fase importa

Modelos úteis em produção precisam ser monitorados, explicados, auditados e corrigidos. Esta fase desloca a atenção do “subiu e funcionou” para o “continua correto, seguro e justificável ao longo do tempo”, cobrindo drift, validação, qualidade operacional, compliance e inferência causal como suporte a decisões mais maduras.

## Ao concluir esta fase, você deve ser capaz de

- detectar e interpretar sinais de degradação em dados e modelos;
- instrumentar ferramentas e serviços de monitoramento para workloads de ML;
- criar gates de qualidade e validação de dados em pipelines;
- aplicar noções de governança, fairness, privacidade e compliance em produtos de dados;
- usar inferência causal para apoiar diagnósticos e decisões prescritivas.

## Relação com o Tech Challenge

Nesta etapa, a qualidade da entrega depende de evidência operacional. O Tech Challenge passa a cobrar não apenas execução, mas mecanismos de controle: como detectar falhas, como responder a drift, como validar dados e como justificar tecnicamente decisões com impacto regulatório e de negócio.

## Como navegar nesta fase

1. Comece por Data Drift para entender degradação e reação.
2. Expanda para ferramentas e serviços de monitoramento para observar aplicações reais.
3. Use Validação de Dados e Governança para introduzir controles formais.
4. Feche com Inferência Causal para avançar de monitoramento descritivo para decisão orientada por efeito.
5. Para a camada oficial de regras, consulte o [governanca/README.md](../../../governanca/README.md) e o [Resumo dos Tech Challenges](../../../governanca/resumo-tech-challenges.md).

## Disciplinas

| # | Nome | Papel na fase | Aulas |
|---|------|---------------|-------|
| [01](01-data-drift/README.md) | Data Drift | detectar degradação estatística e conceitual | 8 |
| [02](02-ferramentas-monitoramento-modelos/README.md) | Ferramentas de Monitoramento de Modelos | aplicar ferramentas específicas de profiling e dashboards | 3 |
| [03](03-monitoramento-pipelines-infra/README.md) | Monitoramento de Pipelines e Infraestrutura | observar execução, recursos e alertas | 3 |
| [04](04-validacao-dados-qualidade/README.md) | Validação de Dados e Bibliotecas de Qualidade | formalizar qualidade antes do erro virar incidente | 4 |
| [05](05-governanca-compliance/README.md) | Governança e Compliance — LGPD/GDPR | conectar engenharia de ML a responsabilidade regulatória | 4 |
| [06](06-inferencia-causal/README.md) | Inferência Causal e Monitoramento Prescritivo | apoiar decisões além de correlação | 6 |

## Como usar o material da fase

- Priorize a sequência das disciplinas, porque a maturidade conceitual importa nesta fase.
- Use notebooks para entendimento e scripts para consolidação de fluxos operacionais.
- Trate esta fase como ponte entre execução técnica e responsabilização institucional.

## Setup

```bash
make install-fase04
# ou
uv pip install -e ".[fase04,dev]"
```
