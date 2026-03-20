# Aula 04 - Projeto completo de refatoracao

Pack comparativo para discutir um workflow legado de classificacao de carteira e sua versao refatorada. O foco e mostrar como um facade ajuda a expor a mesma capacidade operacional enquanto o codigo interno fica menos acoplado.

## Objetivo didatico

- comparar um fluxo legado monolitico com uma versao modularizada;
- mostrar como um facade protege quem consome o workflow durante a migracao;
- destacar que refatoracao boa preserva contrato observavel.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/01-clean-code-ml/aula04-projeto-refatoracao
python refactor_facade.py
```

## Arquivos

- `legacy/customer_risk_workflow.py`: versao concentrada do fluxo.
- `refactored/customer_risk_workflow.py`: workflow modular com facade explicita.
- `refactor_facade.py`: compara as duas versoes e resume equivalencia funcional.

## Observacoes didaticas

- a comparacao usa dados pequenos e deterministas para facilitar inspeção;
- o facade permite trocar implementacao sem forcar chamadores a reescrever integracoes;
- o objetivo nao e sofisticar o modelo, e reduzir fragilidade estrutural.