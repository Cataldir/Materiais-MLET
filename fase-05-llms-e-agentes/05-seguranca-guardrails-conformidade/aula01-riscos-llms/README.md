# Aula 01 - Riscos e ataques em sistemas com LLMs

Pacote canonico leve para abrir a disciplina de seguranca com uma taxonomia de riscos em LLMs e agentes. A aula organiza os cenarios entre vazamento, prompt injection, automacao indevida e alucinacao operacional para justificar os controles que aparecem nas aulas seguintes.

## Objetivo didatico

- mapear os riscos mais recorrentes em sistemas generativos de forma operavel;
- priorizar ataques e falhas por severidade e explorabilidade;
- criar uma ponte clara entre risco percebido e guardrails tecnicos.

## O que foi preservado

- cenarios proximos da realidade de assistentes internos e copilots;
- leitura executiva de impacto, explorabilidade e prioridade;
- alinhamento direto com guardrails, prompt injection e compliance.

## O que foi simplificado

- sem red-team externo, benchmark adversarial ou integracao com provedores reais;
- sem pentest ou stack de seguranca completa como requisito de execucao;
- foco em classificacao e priorizacao local para facilitar discussao e debug.

## Execucao

```bash
cd fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula01-riscos-llms
python llm_risks.py
```

## Arquivos

- `llm_risks.py`: prioriza cenarios de risco por impacto, explorabilidade e necessidade de controle.
- `01_riscos_llms_local.ipynb`: notebook local com a mesma priorizacao.

## Observacoes didaticas

- esta aula funciona como mapa de ameacas para o restante da disciplina;
- risco alto sem controle observavel deve virar prioridade de arquitetura, nao apenas nota de documentacao.