# Checklist de Engenharia — 📺 Monitoração de Performance + Serviços de Monitoração

## Escopo

Use este checklist para verificar se o material `📺 Monitoração de Performance + Serviços de Monitoração` foi aplicado com disciplina de Machine Learning Engineering. Ele deve apoiar revisão por pares e preparação para entrega.

## Reprodutibilidade

- [ ] O ambiente necessário está documentado perto do material.
- [ ] Entradas, saídas e dependências estão explícitas.
- [ ] O grupo consegue repetir a execução ou a análise sem estado oculto.

## Qualidade de Código

- [ ] O código ou desenho de solução separa responsabilidades.
- [ ] Nomes de arquivos, funções e variáveis ajudam a leitura.
- [ ] Erros esperados e limitações são tratados ou documentados.

## Dados e Validação

- [ ] A origem dos dados é conhecida e permitida para uso didático.
- [ ] Há critério de qualidade antes de usar dados em modelo, pipeline ou demo.
- [ ] Dados sensíveis, credenciais e artefatos gerados não foram publicados indevidamente.

## Modelo e Métricas

- [ ] Métricas fazem sentido para o problema e para o usuário final.
- [ ] Existe baseline, comparação ou justificativa quando houver modelo.
- [ ] Limitações do modelo ou abordagem foram registradas.

## API, Pipeline ou Deploy

- [ ] O caminho de execução está descrito de forma local e reproduzível.
- [ ] A solução indica como seria empacotada, publicada ou monitorada quando aplicável.
- [ ] Falhas operacionais prováveis têm plano de resposta inicial.

## Observabilidade

- [ ] Logs, métricas, outputs ou evidências são suficientes para depurar a atividade.
- [ ] O grupo sabe o que observar depois da primeira execução.
- [ ] Há indicação de alerta, threshold ou sinal de revisão quando aplicável.

## Segurança e Governança

- [ ] Não há segredos, tokens, dados privados ou informações pessoais no material público.
- [ ] Riscos de privacidade, fairness, compliance ou uso indevido foram considerados quando relevantes.
- [ ] A documentação diferencia hipótese, evidência e decisão.

## Documentação Pública

- [ ] O README local aponta para os artefatos certos.
- [ ] A decisão técnica pode ser entendida por estudante que não participou da live.
- [ ] O material mantém foco em orientação e não em respostas finais.

## Itens Fora de Escopo

- escolher arquitetura de nuvem sem justificar custo, latência e responsabilidade operacional.
- automatizar deploy sem gates de qualidade e rollback.
- monitorar apenas disponibilidade, ignorando qualidade de predição e deriva.

