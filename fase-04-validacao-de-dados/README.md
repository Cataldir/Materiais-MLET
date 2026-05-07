# Validação de Dados em ML — material complementar

Este diretório contém um conjunto complementar de notebooks e exemplos sobre validação de dados em ML. Ele ainda está separado da trilha canônica da Fase 04, por isso deve ser usado como apoio adicional, não como ponto principal de navegação.

## Caminho recomendado

1. Comece pela fase canônica em [Fase 04 — Monitoramento e Governança](../fase-04-monitoramento-e-governanca/README.md).
2. Estude a disciplina [Validação de Dados e Bibliotecas de Qualidade](../fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/README.md).
3. Use os notebooks deste diretório para aprofundar fundamentos, qualidade, deduplicação, drift, contratos, outliers, frameworks e validação contínua.

## Aulas complementares

| Aula | Tema |
| --- | --- |
| [aula_01](aula_01/) | Fundamentos de validação de dados |
| [aula_02](aula_02/) | Dimensões de qualidade |
| [aula_03](aula_03/) | Deduplicação e imputação |
| [aula_04](aula_04/) | Monitoramento de drift |
| [aula_05](aula_05/) | Schema e contratos de dados |
| [aula_06](aula_06/) | Outliers e anomalias |
| [aula_07](aula_07/) | Frameworks de qualidade |
| [aula_08](aula_08/) | Validação contínua em MLOps |

## Setup local

Quando precisar executar estes notebooks, use o arquivo de dependências local deste complemento.

```bash
python -m pip install -r fase-04-validacao-de-dados/requirements.txt
```

## Observações

- Alguns notebooks podem conter saídas salvas para fins de demonstração; antes de publicar versões finais, prefira notebooks limpos e executáveis de cima para baixo.
- Este complemento possui [licença local](LICENSE). Confira o arquivo antes de reutilizar o conteúdo fora do contexto didático.
- Uma futura curadoria pode migrar estes exemplos para a disciplina canônica de validação de dados da Fase 04.