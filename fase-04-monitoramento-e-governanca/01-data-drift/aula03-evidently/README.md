# Aula 03 - Evidently com fallback local

Pacote canonico leve para apresentar a ideia de relatórios de drift no estilo do Evidently sem tornar a aula dependente de uma versao especifica da biblioteca. O material roda localmente com `numpy` e `pandas` e usa um adaptador opcional quando `evidently` estiver instalado.

## Objetivo didatico

- mostrar como um fluxo de monitoramento separa coleta, avaliacao e publicacao de relatorio;
- comparar o caminho local deterministico com um caminho opcional compatível com Evidently;
- produzir um resumo testavel para smoke tests e exploracao em notebook ou terminal.

## O que foi preservado

- estrutura de Adapter para encapsular o backend de monitoramento;
- Template Method para manter a sequencia de referencia, lote atual e consolidacao do relatorio;
- indicadores simples por feature com status final legivel.

## O que foi simplificado

- sem dashboard web ou persistencia historica;
- sem depender da API exata de uma versao do Evidently;
- foco em um lote sintetico pequeno e totalmente deterministico.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/01-data-drift/aula03-evidently
python evidently_reports.py
```

## Arquivos

- `evidently_reports.py`: adaptadores local/opcional e fluxo fixo do relatorio.

## Observacoes didaticas

- quando `evidently` nao estiver instalado, o backend local continua gerando um resumo util;
- o adaptador existe para isolar a dependencia opcional e evitar acoplamento com a aula;
- o padrao e reutilizavel em pipelines que precisem alternar entre modo didatico e tool-specific.