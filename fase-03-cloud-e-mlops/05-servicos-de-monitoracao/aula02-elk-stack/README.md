# Aula 02 - ELK Stack para Logs de ML

Pacote canonico local para demonstrar coleta e visualizacao de logs de inferencia com Elasticsearch, Logstash e Kibana. A implementacao usa Docker Compose para subir a stack completa.

## Objetivo didatico

- configurar uma stack ELK para centralizar logs de inferencia;
- usar Logstash para ingestao estruturada de eventos de ML;
- visualizar padroes de uso e erros em Kibana.

## O que foi preservado

- stack completa com Elasticsearch, Logstash e Kibana;
- pipeline Logstash configurado para eventos de ML;
- health checks e dependencias entre servicos.

## O que foi simplificado

- sem autenticacao ou TLS (xpack.security desabilitado);
- sem integracao com aplicacao de inferencia real;
- foco na infraestrutura de coleta, nao no emissor.

## Execucao

```bash
cd fase-03-cloud-e-mlops/05-servicos-de-monitoracao/aula02-elk-stack
docker-compose up -d
# Kibana: http://localhost:5601
# Elasticsearch: http://localhost:9200
```

## Arquivos

- `docker-compose.yml`: stack ELK completa para logs de ML.
- `logstash.conf`: pipeline de ingestao de logs estruturados.

## Observacoes didaticas

- centralizar logs permite correlacionar erros de inferencia com padroes de uso;
- Logstash atua como ponte entre o emissor e o armazenamento indexado;
- Kibana oferece exploracao visual sem necessidade de queries manuais.
