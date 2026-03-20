# Aula 03 - GCP e Azure para deploy de modelos

Pacote canonico local para comparar dois provedores cloud com o mesmo contrato de deploy. O foco e mostrar como um adaptador comum ajuda a trocar detalhes de provedor sem mudar o fluxo principal da aplicacao.

## Objetivo didatico

- comparar mapeamentos equivalentes entre servicos gerenciados de GCP e Azure;
- destacar contrato compartilhado de deploy, observabilidade e armazenamento de artefatos;
- manter tudo local e deterministicamente simulavel, sem credenciais ou chamadas externas.

## O que foi preservado

- visao comparativa entre provedores;
- preocupacoes de compute, storage, autoscaling e observabilidade;
- um contrato unico que permite trocar o provider por adaptador.

## O que foi simplificado

- sem deploy real, CLI cloud ou provisionamento remoto;
- sem custo variavel por consumo real;
- sem dependencia alem da biblioteca padrao.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/01-deploy-em-nuvem/aula03-gcp-azure
python cloud_provider_adapter.py
```

## Arquivos

- `cloud_provider_adapter.py`: compara planos equivalentes para GCP e Azure usando o mesmo contrato.

## Observacoes didaticas

- o adaptador evita espalhar condicionais de provider pela aplicacao;
- o contrato comum ajuda a comparar trade-offs de servico e operacao;
- o exercicio local prepara o aluno para migracoes e multi-cloud sem custo adicional.