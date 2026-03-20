# Aula 04 - Gerenciamento de dependencias sem surpresa operacional

Pack canonico para mostrar como o mesmo perfil de dependencias pode ser materializado por ferramentas diferentes sem perder clareza de ambiente. O objetivo e comparar escolhas como `venv`, Poetry e `uv` a partir de um contrato unico de projeto.

## O que foi preservado

- traducao do mesmo conjunto de dependencias para multiplos formatos;
- discussao sobre reproducibilidade, ambiente local e configuracao por `.env`;
- uso de Factory Method para separar ferramenta de build do perfil da aplicacao.

## O que foi simplificado

- sem instalacao real de dependencias durante a aula;
- sem lockfiles extensos ou multiplos sistemas operacionais;
- foco no desenho de manifestos e nas decisoes de engenharia.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/03-engenharia-software-cientistas-dados/aula04-gerenciamento-deps
python dependency_factory_demo.py
```

## Arquivos

- `dependency_factory_demo.py`: gera manifestos equivalentes para `venv`, Poetry e `uv`.

## Observacoes didaticas

- a ferramenta muda, mas o contrato do projeto deve continuar legivel e previsivel;
- escolher um gerenciador de dependencias tambem e escolher como reduzir atrito do time.