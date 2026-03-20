# Aula 04 - NannyML para monitoramento sem labels

Pacote canonico leve para demonstrar o raciocinio de monitoramento sem labels inspirado no NannyML. O material usa estrategias locais para estimar degradacao com base em confianca e distribuicao de predições, mantendo um adaptador opcional quando `nannyml` existir no ambiente.

## Objetivo didatico

- ilustrar o problema de monitorar performance quando o target demora a chegar;
- comparar estrategias de estimativa sem labels em um lote sintetico estavel e outro degradado;
- mostrar como um Adapter permite trocar backend sem alterar o contrato do pack.

## O que foi preservado

- foco em no-label monitoring e proxies de performance;
- Strategy para trocar a heuristica de estimacao;
- Adapter para representar o caminho opcional da ferramenta.

## O que foi simplificado

- sem dependencia obrigatoria do stack oficial;
- sem ingestao remota, dashboards ou jobs agendados;
- uso de um dataset sintetico pequeno e totalmente reprodutivel.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/01-data-drift/aula04-nannyml
python nannyml_demo.py
```

## Arquivos

- `nannyml_demo.py`: estrategias locais de monitoramento sem labels e adaptador opcional.

## Observacoes didaticas

- a estimativa nao substitui o label real, mas ajuda a priorizar investigacao;
- a degradacao pode aparecer por queda de confianca ou por mudanca na mistura de classes previstas;
- o mesmo contrato pode ser usado em backfills posteriores com labels reais.