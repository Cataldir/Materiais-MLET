# Aula 01 - LGPD e GDPR para fluxos de ML

Pacote canonico leve para abrir a disciplina de governanca e compliance com cenarios sinteticos de uso de dados em ML. A aula mostra como classificar casos entre permitido, revisao obrigatoria e bloqueio antes de entrar nas tecnicas especificas de fairness, model cards e privacidade.

## Objetivo didatico

- enquadrar compliance como parte do desenho do sistema e nao como etapa final;
- comparar cenarios de uso de dados com diferentes niveis de risco regulatorio;
- ligar base legal, minimizacao e explicabilidade a decisoes tecnicas concretas.

## O que foi preservado

- foco em casos proximos de credito, marketing e atendimento;
- leitura executiva sobre risco, revisao e bloqueio;
- conexao direta com os packs seguintes da disciplina.

## O que foi simplificado

- sem assessoria juridica real ou texto regulatorio completo como dependencia de execucao;
- sem integracao com banco, lineage ou workflow de aprovacao formal;
- exemplos pequenos para privilegiar entendimento e debate.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/05-governanca-compliance/aula01-lgpd-gdpr-ml
python lgpd_compliance.py
```

## Arquivos

- `lgpd_compliance.py`: avalia cenarios sinteticos sob regras minimas de compliance para ML.
- `01_lgpd_gdpr_ml_local.ipynb`: notebook local com a mesma classificacao dos casos.

## Observacoes didaticas

- esta aula abre a disciplina definindo fronteiras de uso aceitavel antes das ferramentas;
- a classificacao local nao substitui analise juridica, mas ajuda a transformar a exigencia regulatoria em regra operacional legivel.