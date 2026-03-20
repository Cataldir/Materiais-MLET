# Aula 06 - Integracao entre sklearn, tracking e SDK interno

Pack canonico para fechar a disciplina mostrando como um pacote interno pode encapsular tracking e manter o pipeline de treino mais limpo. A aula usa um adapter de tracking com fallback local para nao bloquear execucao quando `mlflow` nao estiver instalado.

## O que foi preservado

- treino simples com `scikit-learn` e logging de parametros e metricas;
- facade para esconder detalhes do tracker usado;
- adapter que permite alternar entre MLflow e implementacao em memoria.

## O que foi simplificado

- sem servidor de tracking obrigatorio;
- sem persistencia de modelo em registry remoto;
- foco em integracao local e contrato do SDK.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula06-integracao-sklearn-mlflow
python sdk_integration_demo.py
```

## Arquivos

- `sdk_integration_demo.py`: pipeline sklearn com adapter de tracking e facade de execucao.

## Observacoes didaticas

- o SDK interno protege o pipeline de detalhes acidentais de observabilidade;
- fallback local ajuda a manter a aula executavel mesmo fora do ambiente completo do time.