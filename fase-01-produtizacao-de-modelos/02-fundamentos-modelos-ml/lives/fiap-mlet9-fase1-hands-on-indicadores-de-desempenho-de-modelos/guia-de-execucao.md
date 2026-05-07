# Guia de Execução — 📺 INDICADORES DE DESEMPENHO DE MODELOS

## Quando usar

Use este guia quando a live envolver uma aplicação local com múltiplos passos, dependências próprias, variáveis de ambiente ou API. Ele complementa o [README local](README.md) e não substitui a leitura do código.

## Preparação

1. Crie um ambiente virtual isolado.
2. Instale dependências locais, quando houver `requirements.txt`.
3. Copie `.env.example` para `.env` somente se a aplicação precisar de variáveis de ambiente.
4. Nunca publique chaves, tokens ou respostas de provedores externos.

## Fluxo sugerido

1. Leia a arquitetura descrita no README.
2. Identifique os módulos de ingestão, recuperação, geração e avaliação.
3. Execute a menor parte possível antes de subir a aplicação completa.
4. Valide a resposta com critérios explícitos: relevância, rastreabilidade, latência e custo.
5. Registre limitações do julgamento automatizado e da base de conhecimento usada.

## Pontos de atenção em RAG e LLM-as-a-Judge

- A qualidade da resposta depende da qualidade dos chunks e da recuperação.
- Similaridade alta não garante resposta correta.
- Avaliação por LLM ajuda triagem, mas não substitui rubrica humana.
- Variáveis de ambiente e chaves devem ficar fora do Git.
- PDFs e bases externas precisam de licença compatível com uso didático.

## Evidência mínima

- Comando executado.
- Pergunta de teste.
- Resposta obtida.
- Fonte recuperada ou trecho usado.
- Avaliação qualitativa ou métrica.
- Próximo ajuste necessário.
