---
name: aplicar-inteligencia-pragmatica
description: Aplicar o framework local Inteligência Pragmática a qualquer objetivo, criando ou retomando PGG, Plano Mínimo Viável com 8Rs, Sessões Pragmáticas, decisões e revisões. Usar quando o usuário pedir para definir um objetivo, transformar algo em PGG, montar PMV/8Rs, escolher a próxima sessão ou ação pragmática, revisar progresso ou aplicar o método completo sem restringir o domínio.
---

# Aplicar Inteligência Pragmática

## Princípio de operação

Usar este repositório como fonte do método e a CLI como autoridade estrutural. Manter objetivos e dados
reais no workspace hospedeiro. Nunca inventar informação: registrar lacuna, hipótese, fato, decisão,
compromisso e evidência separadamente.

## Preparar

1. Localizar a raiz do framework a partir desta skill.
2. Ler `method/inteligencia-pragmatica.yaml` para regras atuais.
3. Procurar primeiro um documento de objetivo existente no contexto ou no caminho informado.
4. Ler o `AGENTS.md` do workspace hospedeiro e respeitar suas convenções e permissões.
5. Não escrever arquivo quando o usuário pediu somente uma aplicação conversacional.

## Detectar o modo

- **Definir:** transformar desejo/objetivo em PGG.
- **Planejar:** criar ou melhorar PMV/8Rs.
- **Executar:** escolher e estruturar a próxima Sessão Pragmática.
- **Revisar:** incorporar feedback e atualizar o plano.
- **Completo:** iniciar/retomar o ciclo inteiro.

Se o pedido nomear o modo, obedecer. Caso contrário, consultar
[`references/routing.md`](references/routing.md) e escolher a menor intervenção suficiente.

## Executar o fluxo

1. Carregar contexto já disponível antes de perguntar.
2. Rodar `pragmatic status <objetivo.yaml>` e `pragmatic next <objetivo.yaml>` quando houver documento.
3. Ler apenas as referências pertinentes ao modo:
   - Definir: [`definition-and-pgg.md`](references/definition-and-pgg.md)
   - Planejar: [`planning-and-8rs.md`](references/planning-and-8rs.md)
   - Executar: [`execution-skills.md`](references/execution-skills.md)
   - Revisar: [`review-and-feedback.md`](references/review-and-feedback.md)
   - Qualidade/artefatos: [`quality-and-artifacts.md`](references/quality-and-artifacts.md)
4. Se faltar informação necessária, formular a menor pergunta que desbloqueia o próximo gate. Não pedir
   dados adiados para a fase atual.
5. Distinguir explicitamente resultado desejado de esforço controlável.
6. Ajustar profundidade a impacto e irreversibilidade. Não forçar 4Cs ou 8Rs completos em tarefa curta.
7. Atualizar o YAML somente com autorização de escrita; preservar histórico de revisões.
8. Rodar `pragmatic validate`, corrigir erros estruturais e expor lacunas bloqueantes sem preenchê-las.
9. Encerrar cada ciclo em DPA: decisão, próxima ação com dono e prazo, ou arquivamento.
10. Renderizar com `pragmatic render` quando o usuário quiser uma versão legível.

## Comandos

```bash
uv run --project <raiz-framework> pragmatic init <destino.yaml> --title "..." --workspace <workspace>
uv run --project <raiz-framework> pragmatic validate <objetivo.yaml>
uv run --project <raiz-framework> pragmatic status <objetivo.yaml>
uv run --project <raiz-framework> pragmatic next <objetivo.yaml>
uv run --project <raiz-framework> pragmatic render <objetivo.yaml> --output <plano.md>
```

Tratar código `1` de validação como erro estrutural e `2` como lacuna bloqueante. Alertas não autorizam
o agente a inventar respostas.
