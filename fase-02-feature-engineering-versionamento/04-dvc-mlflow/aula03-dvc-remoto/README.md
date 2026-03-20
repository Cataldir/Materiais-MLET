# Aula 03 - DVC remoto com fallback offline

Pack local para discutir configuracao de remoto no DVC sem depender de credenciais, bucket ou acesso de rede. O script usa Adapter para tratar backends diferentes e sempre produzir um fallback seguro para diretorio local.

## Objetivo didatico

- explicar o papel do remoto como extensao do versionamento local;
- diferenciar requisitos operacionais de `s3`, `gcs` e diretorio local;
- manter uma rota offline para estudo, debug e demonstracao em aula.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula03-dvc-remoto
python remote_setup.py
```

## Arquivos

- `remote_setup.py`: gera um plano de configuracao com fallback local.

## Observacoes didaticas

- o foco nao e autenticar em nuvem, e sim modelar a configuracao corretamente;
- todo backend remoto ganha um destino local previsivel para estudo e contingencia;
- isso reduz acoplamento entre aprendizado da ferramenta e disponibilidade de infraestrutura.