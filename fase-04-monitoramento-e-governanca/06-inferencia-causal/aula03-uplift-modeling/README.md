# Aula 03 - Uplift modeling com estrategias locais

Pacote canonico leve para demonstrar uplift modeling sem depender de bibliotecas dedicadas. O material compara duas estrategias simples sobre um conjunto sintetico com efeito heterogeneo de tratamento por segmento.

## Objetivo didatico

- distinguir previsao de resposta geral de previsao de efeito incremental;
- comparar estrategias leves de ranking por uplift;
- usar um Template Method para manter o fluxo de geracao, estimacao e ranking.

## O que foi preservado

- Strategy para comparar estimadores de uplift;
- Template Method para padronizar geracao do experimento e avaliacao;
- segmentos com efeito heterogeneo que justificam ranking de campanha.

## O que foi simplificado

- sem CausalML ou EconML como dependencia obrigatoria;
- sem treinamento supervisionado pesado;
- foco em ranking deterministico por segmento.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/06-inferencia-causal/aula03-uplift-modeling
python uplift_model.py
```

## Arquivos

- `uplift_model.py`: gera segmentos sinteticos e compara estrategias de uplift.

## Observacoes didaticas

- uplift e sobre diferenca entre tratar e nao tratar, nao apenas probabilidade de conversao;
- segmentos pequenos podem mostrar efeito mais instavel, mesmo quando parecem promissores;
- o ranking final ajuda a conectar causalidade com priorizacao operacional.