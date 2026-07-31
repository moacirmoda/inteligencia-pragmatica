# Inteligência Pragmática

[![CI](https://github.com/moacirmoda/inteligencia-pragmatica/actions/workflows/ci.yml/badge.svg)](https://github.com/moacirmoda/inteligencia-pragmatica/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Framework local-first e independente de domínio para transformar objetivos em planos vivos e
sessões de execução. O método fica declarativo; a CLI cuida de estrutura, estados, validação,
próxima ação e renderização; o agente pesquisa, entende, sintetiza e julga sem inventar lacunas.

Os documentos dos objetivos pertencem ao workspace do usuário, não a este repositório.

> [!IMPORTANT]
> Este é um projeto independente e não oficial, inspirado nos conceitos do livro
> *Inteligência Pragmática*, de Max Peters. Não possui afiliação ou endosso do autor ou da
> editora e não substitui a obra original. O repositório não contém o texto nem as ilustrações
> do livro.

## O que o projeto oferece

- especificação declarativa das fases Definir, Planejar, Executar e Revisar;
- modelo canônico de objetivo em YAML;
- PGG, 4Cs, 3Is, PMV, 8Rs e seis habilidades pragmáticas;
- profundidade adaptativa para não forçar o método inteiro em tarefas pequenas;
- validações determinísticas com cinco níveis de severidade;
- fechamento de ciclos em Decisão, Próxima Ação ou Arquivamento (DPA);
- CLI local e skill fina para agentes compatíveis com `SKILL.md`;
- schemas, testes unitários e avaliações comportamentais.

## Instalação para desenvolvimento

Requer [Python 3.11 ou superior](https://www.python.org/) e
[`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/moacirmoda/inteligencia-pragmatica.git
cd inteligencia-pragmatica
uv sync --extra dev
uv run pragmatic --help
```

Para instalar somente a CLI em um ambiente isolado:

```bash
uv tool install git+https://github.com/moacirmoda/inteligencia-pragmatica.git
pragmatic --help
```

## Uso mínimo

Crie o documento em seu próprio workspace:

```bash
uv run pragmatic init ./objetivos/aprender-piano.yaml \
  --title "Aprender piano" \
  --depth light \
  --workspace ./objetivos
```

Consulte e valide o estado:

```bash
uv run pragmatic validate ./objetivos/aprender-piano.yaml
uv run pragmatic status ./objetivos/aprender-piano.yaml
uv run pragmatic next ./objetivos/aprender-piano.yaml
uv run pragmatic render ./objetivos/aprender-piano.yaml --output ./objetivos/aprender-piano.md
```

`validate` usa códigos de saída: `0` sem bloqueios, `1` para erro estrutural e `2` para
lacuna que impede a transição atual. Alertas, recomendações e informações adiadas não quebram
o comando.

### Profundidade

| Valor | Quando usar |
| --- | --- |
| `light` | Tarefa pequena, de baixo impacto e facilmente reversível |
| `standard` | Projeto relevante, com impacto ou reversibilidade moderados |
| `deep` | Objetivo de alto impacto ou decisão difícil de reverter |

## Uso com agentes

A skill está em `.agents/skills/aplicar-inteligencia-pragmatica`. Em um agente compatível,
invoque-a explicitamente:

```text
Use $aplicar-inteligencia-pragmatica para transformar “aprender piano” em um PGG.
```

Ela também reconhece pedidos para montar um PMV, escolher a próxima Sessão Pragmática, revisar
progresso ou aplicar o método completo. A skill consulta contexto existente antes de perguntar e
formula somente a menor pergunta necessária para desbloquear o trabalho.

## Arquitetura

```text
agente / skill fina
        |
        v
CLI -> engine -> validador -> método YAML
        |
        v
documento YAML do objetivo (fora do repositório)
```

- [`method/inteligencia-pragmatica.yaml`](method/inteligencia-pragmatica.yaml): fonte executável do método.
- [`templates/objective.yaml`](templates/objective.yaml): modelo canônico de objetivo.
- [`src/pragmatic/`](src/pragmatic/): CLI, validação, roteamento e renderização.
- [`schemas/`](schemas/): contratos JSON Schema.
- [`docs/coverage.md`](docs/coverage.md): rastreabilidade entre conceitos, artefatos e testes.
- [`evals/cases.yaml`](evals/cases.yaml): avaliações realistas de adaptação ao contexto.

Consulte também as [decisões arquiteturais](docs/decisions.md) e a
[visão detalhada da arquitetura](docs/architecture.md).

## Desenvolvimento

```bash
uv sync --extra dev
uv run ruff format --check .
uv run ruff check .
uv run pytest
uv build
```

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para o fluxo de contribuição e
[SECURITY.md](SECURITY.md) para relatar vulnerabilidades.

## Limitações da v1

- YAML e Markdown locais; sem banco, servidor, embeddings ou memória própria.
- A CLI não cria conteúdo substantivo nem chama modelos; valida o que o agente ou usuário escreveu.
- Migrações entre versões de schema ainda não existem.
- O JSON Schema documenta o envelope; regras semânticas mais ricas ficam no método e no validador.
- Datas, donos, métricas e evidências dependem do contexto fornecido ou encontrado no workspace.

## Licença e atribuição

O código e a documentação originais deste repositório são disponibilizados sob a
[licença MIT](LICENSE). Conceitos, nomes, marcas e materiais de terceiros continuam pertencendo
aos respectivos titulares. Consulte [NOTICE](NOTICE) para detalhes de atribuição.
