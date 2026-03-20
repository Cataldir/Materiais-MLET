# Aula 05 - Monitoramento prescritivo

Pacote canonico leve para conectar sinais causais a acoes recomendadas. O material usa estrategias de decisao por segmento e um fluxo observer-like para distribuir recomendacoes a papeis operacionais sem depender de sistemas externos.

## Objetivo didatico

- transformar observacoes causais em recomendacoes de acao;
- separar estrategia de prescricao da notificacao dos interessados;
- manter um fluxo pequeno, testavel e adequado para discutir playbooks.

## O que foi preservado

- Strategy para decidir o tipo de intervencao;
- Observer-like flow para publicar recomendacoes a consumidores distintos;
- segmentos e prioridades com racional causal simplificado.

## O que foi simplificado

- sem filas, webhooks ou sistemas de incidentes reais;
- sem otimizacao matematica pesada;
- foco em recomendacoes deterministicas e explicaveis.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/06-inferencia-causal/aula05-monitoramento-prescritivo
python prescriptive_monitoring.py
```

## Arquivos

- `prescriptive_monitoring.py`: estrategia de prescricao e observadores locais.

## Observacoes didaticas

- prescrever nao e apenas alertar, e sugerir a melhor proxima acao;
- observers diferentes consomem a mesma decisao com formatos distintos;
- esse padrao ajuda a desacoplar analise causal da operacao do dia a dia.