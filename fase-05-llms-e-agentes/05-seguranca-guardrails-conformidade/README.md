# 05 — Segurança, Guardrails e Conformidade

> 5h de vídeo · 5 aulas

## Por que esta disciplina importa

Sistemas generativos ampliam superfície de ataque, risco de vazamento, comportamento inesperado e impacto regulatório. Esta disciplina fecha a trilha mostrando que segurança e conformidade não são acessórios de IA generativa, mas parte do desenho mínimo de uma solução confiável.

## O que você deve aprender

- reconhecer riscos específicos de LLMs e agentes, incluindo prompt injection;
- aplicar guardrails e mecanismos de contenção de comportamento;
- instrumentar logging de auditoria e detecção de PII;
- estruturar um projeto que trate segurança e conformidade como requisito de produto.

## Como usar este material

1. Comece pelo mapeamento de riscos para entender a superfície do problema.
2. Avance para guardrails e defesas específicas contra ataques e uso indevido.
3. Use a aula de compliance para conectar segurança técnica a obrigação institucional e regulatória.
4. Feche com o projeto integrador para consolidar uma postura de segurança por desenho.

## Como referenciar esta disciplina no repositório

- O caminho canônico é `fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/`.
- Ao mencionar um risco ou mecanismo específico, cite a aula correspondente.
- O README resume o racional da trilha; scripts e notebooks mostram a implementação e a simulação dos controles.
- A governança formal do programa e suas políticas continuam sendo a fonte oficial para precedência documental.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Na prática profissional, esta disciplina reduz exposição a incidentes técnicos, jurídicos e reputacionais em produtos baseados em LLMs. Academicamente, ela introduz uma visão crítica de segurança aplicada a sistemas generativos, articulando adversarialidade, compliance e governança de uso responsável.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-riscos-llms/) | Riscos e ataques em LLMs | `llm_risks.py` |
| [02](aula02-guardrails/) | Guardrails: NeMo, Guardrails AI | `guardrails_demo.py` |
| [03](aula03-prompt-injection/) | Prompt injection: ataques + defesas | `prompt_injection.py` |
| [04](aula04-compliance-pii/) | Compliance: audit logging + PII detection | `pii_detector.py` |
| [05](aula05-projeto-seguranca/) | Projeto segurança integrador | notebook |
