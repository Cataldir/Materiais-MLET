# Aula 04 - CD e estrategias de deploy

Pacote canonico local para demonstrar deploy continuo com uma maquina de estados simples. O material compara fluxos blue-green e canary sem subir infraestrutura real.

## Objetivo didatico

- representar promocoes e rollback como estados bem definidos;
- mostrar diferenca entre blue-green e canary com a mesma estrutura de release;
- treinar tomada de decisao baseada em metricas locais de qualidade e erro.

## O que foi preservado

- etapa de validacao antes da promocao;
- possibilidade de rollback quando a saude do release degrada;
- comparacao entre dois modos comuns de deploy continuo.

## O que foi simplificado

- sem cluster, ingress, service mesh ou traffic split real;
- sem pipeline remoto ou registry externo;
- apenas simulacao deterministica com biblioteca padrao.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula04-cd-deploy
python release_state_machine.py
```

## Arquivos

- `release_state_machine.py`: executa fluxos locais de blue-green e canary como maquina de estados.

## Observacoes didaticas

- deploy continuo seguro depende de gates explicitos;
- rollback fica mais claro quando cada transicao e registrada;
- blue-green e canary compartilham a maior parte do fluxo, mas diferem na promocao.