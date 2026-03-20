# 05 — Governança e Compliance — LGPD/GDPR

> 4h de vídeo · 4 aulas

## Por que esta disciplina importa

Sistemas de ML operam sobre dados, pessoas e decisões com implicações regulatórias e reputacionais. Esta disciplina aborda a camada de responsabilidade do trabalho técnico: proteção de dados, fairness, documentação de modelo e mecanismos de privacidade que sustentam legitimidade e conformidade.

## O que você deve aprender

- interpretar implicações práticas de LGPD e GDPR em projetos de ML;
- auditar fairness com bibliotecas especializadas;
- produzir model cards e rastros de lineage para documentação responsável;
- aplicar noções de privacidade, anonimização e proteção adicional de dados.

## Como usar este material

1. Comece pelo enquadramento regulatório para entender o problema antes da ferramenta.
2. Avance para fairness e model cards como mecanismos de governança técnica.
3. Use a aula de privacidade para discutir limites do uso de dados e mitigação de risco.
4. Trate esta disciplina como apoio transversal para qualquer projeto com impacto sobre pessoas e dados pessoais.

## Como referenciar esta disciplina no repositório

- O caminho principal é `fase-04-monitoramento-e-governanca/05-governanca-compliance/`.
- Ao mencionar um tema específico, cite a aula correspondente para manter precisão do recorte.
- Este README organiza a leitura executiva e acadêmica; scripts e exemplos mostram a operacionalização técnica dos conceitos.
- A governança oficial do programa continua sendo a fonte de verdade para política e precedência documental.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Executivamente, essa disciplina ajuda a reduzir risco regulatório, reputacional e de produto. No plano acadêmico, ela introduz discussão crítica sobre responsabilidade algorítmica, documentação e limites éticos do uso de dados e modelos em contextos reais.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-lgpd-gdpr-ml/) | LGPD/GDPR em ML: exemplos práticos | `lgpd_compliance.py` |
| [02](aula02-fairness/) | Fairness: Fairlearn, AIF360 | `fairness_audit.py` |
| [03](aula03-model-cards/) | Model Cards + data lineage | `model_card_generator.py` |
| [04](aula04-privacidade/) | Privacidade: differential privacy, anonimização | `anonymization.py` |
