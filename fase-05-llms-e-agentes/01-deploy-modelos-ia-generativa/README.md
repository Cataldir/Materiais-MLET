# 01 — Deploy de Modelos de IA Generativa

> 3h de vídeo · 3 aulas

## Por que esta disciplina importa

Modelos generativos trazem capacidades novas, mas também novos custos, requisitos de infraestrutura e decisões de serving. Esta disciplina introduz o deploy de LLMs como um problema de engenharia: capacidade, otimização, empacotamento e compatibilidade entre qualidade de resposta e restrição operacional.

## O que você deve aprender

- revisar fundamentos que afetam serving de LLMs, como tokenização e sampling;
- usar stacks de serving como vLLM e TGI;
- aplicar técnicas de otimização, quantização e adaptação eficiente;
- entender o impacto dessas decisões em custo, latência e footprint computacional.

## Como usar este material

1. Comece pelos fundamentos para não tratar serving como caixa-preta.
2. Avance para vLLM e TGI observando diferenças de operação e configuração.
3. Use a aula de otimização para avaliar quais compromissos fazem sentido em produção.
4. Consulte o pacote adicional para conectar a trilha de LLMs com pipelines clássicos de NLP.

## Como referenciar esta disciplina no repositório

- O caminho oficial é `fase-05-llms-e-agentes/01-deploy-modelos-ia-generativa/`.
- Ao citar um padrão de serving ou otimização, referencie a aula correspondente e o arquivo central.
- Este README fornece o enquadramento da trilha; scripts, Dockerfiles e referências mostram a implementação concreta.
- Aspectos normativos e critérios formais continuam fora desta pasta, na governança central do programa.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Na prática profissional, esta disciplina ajuda a separar entusiasmo por IA generativa de decisões sustentáveis de infraestrutura. No plano acadêmico, ela reforça a análise de trade-offs entre arquitetura, compressão, eficiência e qualidade de resposta em sistemas probabilísticos de larga escala.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-fundamentos-llms/) | Fundamentos LLMs: arquitetura, tokenização, sampling | `llm_fundamentals.py` |
| [02](aula02-serving-vllm-tgi/) | Serving com vLLM e TGI | `vllm_serve.py`, `Dockerfile.vllm` |
| [03](aula03-otimizacao-quantizacao/) | Otimização: GPTQ, AWQ, bitsandbytes, LoRA | `quantization.py`, `lora_finetuning.py` |

## Pacotes canônicos adicionais

| Pacote | Origem | Objetivo |
|------|------|---------|
| [referencia-nlp-preprocessamento-sentimento](referencia-nlp-preprocessamento-sentimento/README.md) | `origin/nlp-lectures` | Pack leve de preprocessamento e baseline de sentimento para comparar pipelines classicos com a trilha de LLMs |
