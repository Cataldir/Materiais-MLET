# Aula 03 - Documentacao como ativo de engenharia

Pack canonico para mostrar que docstrings, navegacao de site e exemplos de uso fazem parte do produto interno, nao apenas do acabamento final. A aula transforma metadados do pacote em paginas de documentacao locais e consistentes.

## O que foi preservado

- relacao entre docstrings, API reference e navegacao de docs;
- uso de Template Method para padronizar a geracao de paginas;
- foco em documentacao consumivel por outro time, nao apenas pelo autor.

## O que foi simplificado

- sem subir MkDocs real nem depender de plugins externos;
- sem build de site em CI;
- foco no pipeline conceitual e na estrutura gerada localmente.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula03-documentacao
python documentation_pipeline.py
```

## Arquivos

- `documentation_pipeline.py`: gera arquivos de documentacao em memoria a partir de um manifesto simples.

## Observacoes didaticas

- documentacao boa reduz dependencia de conhecimento tacito entre squads;
- a mesma logica de template pode sustentar README, docs de API e onboarding tecnico.