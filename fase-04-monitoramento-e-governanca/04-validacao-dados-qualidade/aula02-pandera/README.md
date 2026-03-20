# Aula 02 - Pandera para contratos tipados de DataFrame

Pacote canonico leve para apresentar validacao de dados com Pandera em um pipeline local de ML. O material continua funcional mesmo quando a biblioteca nao esta instalada, permitindo explorar o fluxo e os testes sem bloquear a aula.

## Objetivo didatico

- definir schemas tipados para dados de entrada e para predições;
- comparar exemplos validos e invalidos com a mesma estrutura de DataFrame;
- demonstrar fallback amigavel quando `pandera` nao estiver disponivel no ambiente.

## O que foi preservado

- schemas por coluna com checks simples e legiveis;
- validacao lazy para agregar erros quando Pandera esta instalado;
- versoes em script e notebook para execucao local.

## O que foi simplificado

- sem datasets externos ou integracao com pipeline remoto;
- sem dependencia obrigatoria de `pandera` para abrir o material;
- foco em poucos exemplos para facilitar depuracao e smoke tests.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula02-pandera
python pandera_schemas.py
```

## Arquivos

- `pandera_schemas.py`: cria schemas, gera exemplos validos/invalidos e executa validacao com fallback.
- `02_pandera_local.ipynb`: notebook didatico com os mesmos exemplos do script.

## Observacoes didaticas

- `pandera[pandas]` e a instalacao recomendada para o backend `pandas`;
- quando a dependencia nao existe, o script registra aviso e retorna resultados falsos em vez de quebrar;
- esse padrao e util para gates locais de qualidade e smoke tests em ambientes enxutos.