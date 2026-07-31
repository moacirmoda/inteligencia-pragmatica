# Contribuindo

Obrigado pelo interesse em contribuir. Mudanças devem preservar três propriedades do projeto:
independência de domínio, dados dos objetivos fora do repositório e validação determinística do método.

## Preparação

1. Faça um fork e crie uma branch curta a partir de `main`.
2. Instale o ambiente com `uv sync --extra dev`.
3. Mantenha mudanças focadas e adicione testes para comportamentos novos.
4. Não inclua objetivos reais, dados pessoais, textos extensos ou ilustrações do livro.

## Verificações obrigatórias

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
uv build
```

Ao alterar a especificação, atualize também `docs/coverage.md`, schemas, testes e referências da
skill que forem afetados. Ao alterar a skill, valide-a com o validador oficial de skills disponível
em seu ambiente.

## Pull requests

Explique o problema, a decisão tomada, o impacto e as verificações executadas. Prefira uma mudança
coesa por pull request. Discussões e propostas podem começar em uma issue.

Ao participar, você concorda em seguir o [Código de Conduta](CODE_OF_CONDUCT.md).
