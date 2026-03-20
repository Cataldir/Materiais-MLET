# 03 — Docker e Kubernetes

> 5h de vídeo · 5 aulas

## Por que esta disciplina importa

Modelos e APIs de ML precisam sair do ambiente do autor e entrar em ambientes reproduzíveis, transportáveis e operáveis. Esta disciplina mostra como contêineres e orquestração ajudam a padronizar execução, reduzir dependência do host local e preparar workloads para deploy e escala.

## O que você deve aprender

- construir imagens Docker adequadas a serviços e jobs de ML;
- usar multi-stage build e imagens especializadas, inclusive para cenários com GPU;
- compor serviços com Docker Compose;
- entender objetos essenciais de Kubernetes para publicar workloads;
- reconhecer estratégias de rollout e empacotamento com Helm e Skaffold.

## Como usar este material

1. Comece pelos fundamentos de Docker e só depois avance para cenários mais ricos.
2. Reproduza o `docker-compose.yml` para entender integração entre componentes.
3. Use a pasta `k8s/` como transição entre conteinerização local e operação em cluster.
4. Trate a última aula como introdução a rollout controlado e não como checklist cego de YAML.

## Como referenciar esta disciplina no repositório

- A referência principal está em `fase-02-feature-engineering-versionamento/03-docker-kubernetes/`.
- Cite a aula específica quando o foco for build, compose, Kubernetes ou rollout.
- Este README é a camada de orientação; Dockerfiles, manifests e charts são a evidência executável.
- Para políticas do curso, use a camada canônica de governança em vez de reproduzir regra localmente.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Executivamente, a disciplina ajuda a reduzir atrito entre desenvolvimento, operação e ciência de dados ao padronizar empacotamento e publicação. Academicamente, ela introduz infraestrutura como parte do sistema de ML, algo essencial para analisar confiabilidade, portabilidade e custo de execução.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-fundamentos-docker/) | Fundamentos Docker | `Dockerfile`, `.dockerignore`, `app.py` |
| [02](aula02-multistage-gpu/) | Multi-stage build, imagem GPU | `Dockerfile.multistage`, `Dockerfile.gpu` |
| [03](aula03-docker-compose/) | Docker Compose: API + Model + DB | `docker-compose.yml` |
| [04](aula04-kubernetes/) | K8s: deployment, service, HPA, ConfigMap | `k8s/` |
| [05](aula05-helm-canary/) | Canary, rolling update, Helm, Skaffold | `helm/`, `skaffold.yaml` |
