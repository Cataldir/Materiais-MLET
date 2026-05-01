# Fase 02 — Containers e Ambientes Reprodutíveis

## Tech Challenge: Pipeline de Treinamento de Rede Neural Containerizado, Versionado e Reprodutível

Uma empresa de e-commerce precisa de um sistema de recomendação de produtos baseado no comportamento de navegação dos usuários. O modelo central é uma rede neural (MLP ou embedding-based) treinada com PyTorch, com pipeline containerizado em Docker, dados versionados com DVC, experimentos rastreados no MLflow e código seguindo padrões de clean code.

---

## Grupos de Estudo

| GE | Tema | Etapa do TC | Disciplinas |
|----|------|-------------|-------------|
| [GE 01](ge-01-clean-code-e-estrutura/) | Clean Code e Estrutura | Etapa 1 | Clean Code ML |
| [GE 02](ge-02-ambiente-e-dependencias/) | Ambiente e Dependências | Etapa 2 | Gerenciamento de Dependências |
| [GE 03](ge-03-containerizacao-e-versionamento/) | Containerização e Versionamento | Etapa 3 | Docker/K8s, DVC+MLflow |
| [GE 04](ge-04-rede-neural-registry-e-entrega/) | Rede Neural, Registry e Entrega | Etapa 4 | DVC+MLflow (Registry) |

---

## Entrega do Tech Challenge

- **Obrigatório:** Repositório GitHub + Vídeo de 5 minutos (método STAR)
- **Opcional:** Deploy em ambiente de produção em nuvem

## Bibliotecas Requeridas

- **PyTorch** — Rede neural para o modelo de recomendação
- **Scikit-Learn** — Pré-processamento e baselines
- **MLflow** — Tracking de experimentos e Model Registry
- **DVC** — Versionamento de dados e pipeline reprodutível

## Critérios de Avaliação

| Critério | Peso |
|----------|------|
| Clean code e estrutura | 15% |
| Reprodutibilidade | 15% |
| Docker | 15% |
| DVC + Pipeline | 15% |
| Rede neural (PyTorch) | 15% |
| MLflow + Registry | 10% |
| Vídeo STAR | 10% |
| Bônus: deploy em nuvem | 5% |
