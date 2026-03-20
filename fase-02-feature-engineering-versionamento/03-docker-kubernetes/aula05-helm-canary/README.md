# Aula 05 - Helm, canary e rollout local

Pack leve para estudar rollout progressivo sem depender de cluster, Helm instalado ou registry externo. O script usa Builder para compor um bundle de manifests e um plano de rollout que pode ser inspecionado localmente.

## Objetivo didatico

- mostrar a logica de rollout canario antes da execucao em infraestrutura real;
- explicitar como chart, values e pipeline de entrega se relacionam;
- treinar leitura critica de manifests com risco operacional controlado.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/03-docker-kubernetes/aula05-helm-canary
python helm_canary_builder.py
```

## Arquivos

- `helm_canary_builder.py`: gera o plano e os manifests do demonstrador.
- `helm/`: chart minimo com deployment estavel, deployment canario e service.
- `skaffold.yaml`: exemplo de loop local para renderizacao e deploy controlado.

## Observacoes didaticas

- o objetivo aqui e entender rollout, nao executar um deploy real;
- os manifests sao intencionalmente pequenos para caber em aula e revisao;
- o plano de trafego pode ser validado lendo YAML, sem necessidade de cluster.