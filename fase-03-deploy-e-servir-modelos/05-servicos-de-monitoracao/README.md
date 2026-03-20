# 05 — Serviços de Monitoração

> 3h de vídeo · 3 aulas

## Por que esta disciplina importa

Nem todo contexto vai operar observabilidade com a mesma stack. Esta disciplina amplia a visão de monitoramento mostrando ferramentas e serviços diferentes, do ELK a ofertas gerenciadas de nuvem, para que o estudante entenda padrões e não fique preso a uma implementação única.

## O que você deve aprender

- revisar fundamentos de observabilidade aplicados a sistemas de ML;
- usar uma stack de logs e visualização como ELK;
- comparar serviços gerenciados de monitoramento em diferentes provedores;
- avaliar trade-offs entre operar a própria stack e consumir observabilidade gerenciada.

## Como usar este material

1. Use a aula introdutória para alinhar vocabulário e sinais operacionais.
2. Reproduza a stack ELK para observar o fluxo ponta a ponta de logs.
3. Estude a aula de cloud monitoring em chave comparativa e arquitetural.
4. Combine esta disciplina com Monitoração de Performance para formar uma visão mais completa de operação.

## Como referenciar esta disciplina no repositório

- O caminho principal é `fase-03-deploy-e-servir-modelos/05-servicos-de-monitoracao/`.
- Ao mencionar uma ferramenta específica, cite a aula correspondente e o artefato principal.
- O README oferece contexto de uso; a implementação está nas stacks, scripts e configs das aulas.
- A camada normativa segue separada na governança canônica do repositório principal.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Do ponto de vista executivo, a disciplina ajuda a decidir entre custo, controle operacional e velocidade de adoção. No ambiente acadêmico, permite comparar abordagens de observabilidade como escolhas de arquitetura e não apenas como detalhes de ferramenta.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-observabilidade-ml/) | Observabilidade para ML | notebook introdutório |
| [02](aula02-elk-stack/) | ELK Stack: Elasticsearch + Logstash + Kibana | `docker-compose.yml`, `logstash.conf` |
| [03](aula03-cloud-monitoring/) | CloudWatch, Stackdriver, Azure Monitor | scripts por provider |
