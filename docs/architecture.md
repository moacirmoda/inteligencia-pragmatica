# Arquitetura

## Limites

```text
agente / skill fina
        |
        v
CLI -> engine -> validador -> método YAML
        |
        v
documento YAML do objetivo (fora do repositório)
```

O repositório é a fonte de verdade do método, schemas, templates, renderizador, testes e avaliações.
O documento do objetivo pertence ao workspace hospedeiro. Nenhum módulo conhece Obsidian, empresas,
SaaS ou métricas específicas de negócio.

## Divisão de responsabilidade

- Código determinístico: parsing seguro, campos conhecidos, estados, transições, severidades,
  completude, escolha da próxima lacuna, DPA e Markdown.
- Especificação declarativa: fases, artefatos, critérios, roteamento, profundidade e modelos.
- Agente: busca de contexto, pesquisa, síntese, formulação, julgamento, perguntas mínimas e atualização.
- Usuário: direção, compromissos, decisões irreversíveis, autorização de escrita e validação final.

## Inspiração arquitetural

O Mirror foi usado apenas como referência: núcleo separado de interfaces finas, dados do usuário fora
do repositório e método declarativo com gates verificáveis. A v1 deliberadamente não replica banco,
memória, runtime, hooks, servidor ou abstrações de identidade do Mirror.

## Portabilidade

Os formatos são YAML e Markdown. `PRAGMATIC_METHOD` pode apontar para outra especificação compatível.
A CLI aceita qualquer caminho explícito, sem presumir onde o objetivo mora.
