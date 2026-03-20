# 01 — Deploy em Nuvem

> 3h de vídeo · 3 aulas

## Por que esta disciplina importa

Treinar um bom modelo localmente é insuficiente quando o objetivo é colocá-lo a serviço de usuários, processos ou produtos. Esta disciplina apresenta a lógica de deploy em nuvem como escolha arquitetural: plataforma, padrão de serving, acoplamento com o restante do sistema e trade-offs de operação.

## O que você deve aprender

- revisar conceitos fundamentais de cloud aplicados a ML;
- comparar serviços gerenciados e padrões serverless para deploy de inferência;
- entender diferenças práticas entre opções em AWS, GCP e Azure;
- reconhecer critérios de escolha como latência, elasticidade, custo e integração com pipelines.

## Como usar este material

1. Comece pela aula conceitual para alinhar padrões de deployment.
2. Use as aulas por provedor como estudo comparativo, não como prescrição única.
3. Observe como o mesmo problema técnico assume formas diferentes em plataformas distintas.
4. Reaproveite esse repertório ao estudar CI/CD e pipelines automáticos nas próximas disciplinas.

## Como referenciar esta disciplina no repositório

- A trilha está concentrada em `fase-03-deploy-e-servir-modelos/01-deploy-em-nuvem/`.
- Cite a aula por provedor quando a discussão exigir um exemplo concreto de serviço ou padrão de deploy.
- Este README contextualiza decisões; os scripts por nuvem mostram a implementação inicial de cada abordagem.
- Processos oficiais e regras de avaliação vivem fora desta pasta.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Do ponto de vista executivo, entender deploy em nuvem ajuda a escolher caminhos tecnicamente viáveis e economicamente sustentáveis. No campo acadêmico, a disciplina reforça comparação entre arquiteturas de serving e evidencia como o ambiente operacional influencia o desenho experimental e a entrega do sistema.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-conceitos-cloud/) | Conceitos de cloud para ML | `cloud_inference_patterns.py`, notebook |
| [02](aula02-aws-sagemaker/) | AWS: SageMaker + Lambda | `sagemaker_deploy.py`, `lambda_handler.py` |
| [03](aula03-gcp-azure/) | GCP (Cloud Run, Vertex AI) + Azure | `gcp_deploy.py`, `azure_deploy.py` |
