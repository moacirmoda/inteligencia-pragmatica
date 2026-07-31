# Decisões arquiteturais

## D1 — YAML é a fonte executável do método

Aceita. Evita depender da interpretação de um prompt e mantém regras inspecionáveis. Python interpreta
essas regras e complementa validações semânticas que não cabem bem em JSON Schema.

## D2 — Objetivos ficam fora do framework

Aceita. O template é distribuído aqui, mas `init` exige um destino explícito. Dados reais podem ficar
no workspace, em arquivo temporário ou em área privada ignorada.

## D3 — Skill fina

Aceita. `SKILL.md` coordena contexto, modo, pergunta mínima e CLI. Conteúdo do método é dividido em
referências; validação permanece no núcleo.

## D4 — Profundidade adaptativa

Aceita. `light`, `standard` e `deep` dependem de impacto e irreversibilidade. Tarefas curtas podem ir
direto para TATT; projetos relevantes recebem PMV; escolhas irreversíveis chegam a simulação.

## D5 — Desconhecido é dado, não falha do agente

Aceita. Valores desconhecidos permanecem nulos e ganham registros em `gaps`. Fatos, hipóteses,
decisões, compromissos e evidências são coleções distintas.

## D6 — DPA fecha o ciclo

Aceita. Uma sessão concluída precisa terminar em decisão, próxima ação ou arquivamento. Próxima ação
exige descrição, dono e prazo.
