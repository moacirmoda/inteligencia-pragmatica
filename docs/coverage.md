# Cobertura do método

Esta matriz transforma os conceitos em operações sem reproduzir o texto do livro. “Spec” refere-se a
`method/inteligencia-pragmatica.yaml`; “doc” ao modelo canônico; “teste” aos arquivos em `tests/` e
`evals/`.

| Conceito | Definição declarativa | Referência operacional | Campo/artefato | Regra | Teste/avaliação |
| --- | --- | --- | --- | --- | --- |
| Definir | converter desejo em objetivo verificável | `definition-and-pgg.md` | `pgg` | saída distingue resultado e controle | `test_four_cs` |
| Planejar | criar PMV proporcional | `planning-and-8rs.md` | `pmv` | 8Rs conforme profundidade | `test_eight_rs_by_depth` |
| Executar | produzir progresso tangível | `execution-skills.md` | `execution.current_cycle` | TATT e DPA | `test_next_action` |
| Revisar | usar feedback para atualizar o plano | `review-and-feedback.md` | `review_history` | próxima ação tem dono/prazo | `test_completed_cycle_requires_dpa` |
| PGG | ganhar aprendizado/conexões mesmo sem o resultado | definição/PGG | `pgg.win_even_if_fail` | alerta se não formulado | evals de piano/livro |
| Conciso | prazo curto e claro | definição/PGG | `pgg.deadline` | alerta se ausente | `test_four_cs` |
| Corajoso | impacto que amplia limites | definição/PGG | `four_cs.courageous` | status enumerado | `test_four_cs` |
| Controlável | esforço sob controle do responsável | definição/PGG | `controllable_measure` | bloqueia Definir | `test_incomplete_document` |
| Comprometido | custo externo de desistir | definição/PGG | `commitments` | compromisso prioriza esforço | evals de piano/livro |
| 3Is | ampliar impacto, superlativo, integrar interesses | definição/PGG | `three_is` | opcional por contexto | `test_method_parsing` |
| Compromissos social/financeiro/ambiental | elevar custo de abandonar | definição/PGG | `commitments[].type` | recomendação qualitativa | evals |
| Resultado vs esforço | separar efeito desejado de ação controlável | definição/PGG | `desired_outcome`, `controllable_measure` | ambos bloqueiam avanço | `test_incomplete_document` |
| PMV/8Rs | oito perguntas mínimas para projeto | planejamento/8Rs | `pmv` | completo em standard/deep | `test_eight_rs_by_depth` |
| Resultado | alvo do plano | planejamento/8Rs | `pmv.result` | obrigatório | testes PMV |
| Razão | motivo dominante/contexto | planejamento/8Rs | `pmv.reason`, `dominant_reason` | obrigatório | testes PMV |
| Referência/PEGE | princípios, exemplos, guias, experts | planejamento/8Rs | `pmv.reference` | adiado em light | testes PMV |
| Rumo | etapas, ideias e perguntas convertidas em ação | planejamento/8Rs | `pmv.direction` | obrigatório | testes PMV |
| Recursos | tempo, dinheiro, materiais, pessoas, informação | planejamento/8Rs | `pmv.resources` | requerido standard/deep | testes PMV |
| Restrições/antimetas | limites e sacrifícios inaceitáveis | planejamento/8Rs | `pmv.constraints` | requerido standard/deep | evals moradia/livro |
| Riscos | ameaças externas combinadas a vulnerabilidades | planejamento/8Rs | `pmv.risks` | deep exige mitigação/Plano B | `test_deep_risk_requires_plan_b` |
| Responsabilidade | dono único e donos das etapas | planejamento/8Rs | `pmv.responsibility` | dono bloqueia avanço | testes de transição |
| Premortem | imaginar fracasso e derivar prevenção | planejamento/8Rs | riscos/mitigações | extra em deep | eval liderança/moradia |
| Plano vivo | atualizar com nova informação | revisão/feedback | `review_history` | preservar histórico | `test_render_idempotent` |
| Focar/RID | aumentar recompensas, remover inércia e distrações | execução | skill `focus` | roteado quando ação trava | eval sessão curta |
| TATT | tarefa, alvo, tangível e tempo | execução | `tatt` | tarefa/tangível/tempo obrigatórios | `test_execution_requires_tatt` |
| Pesquisar/PERG | perguntar, explorar, revisar e guardar | execução | skill `research` | rigor proporcional | evals |
| Expansão/solução | descobrir espaço e então resolver | execução | política de pesquisa | solução é padrão | evals |
| Entender | factual, conceitual e procedural | execução | skill `understand` | declarar tipo útil | evals |
| DEAP | definir, explicar, aplicar e prever | execução | modelo `DEAP` | critério qualitativo | evals |
| Escrever/testar/condensar | externalizar, buscar feedback e simplificar | execução | processo de entender | recomendação | eval piano/livro |
| Idear | combinar conhecimento, referências, restrições e reframes | execução | skill `ideate` | separar geração e seleção | evals |
| 4Is | identificar, idear, incubar e instituir | execução | modelo `4Is` | instituir é opcional | `test_method_parsing` |
| Decidir | avaliar processo, não confundir com resultado | execução | skill `decide` | registra hipótese/evidência | eval moradia |
| 3Ps de decisão | potencial, período e pessoas | execução | `high_impact` | prioriza grande dominó | evals |
| CAA | critérios, alternativas e análise | execução | modelo `CAA` | evita binário | eval moradia/contratação |
| Regra 2–25 | expandir alternativas em decisões relevantes | execução | `alternative_rule` | adaptativa | eval moradia |
| Níveis de análise | espontânea, planilha, simulação | execução | `analysis_levels` | aumenta com irreversibilidade | `test_depth_routing_spec` |
| Comunicar | alinhar consumidor, comunicador, canal e conteúdo | execução | skill `communicate` | objetivo informar/persuadir | evals |
| PROBLEM | pesquisar destinatário | execução | `audience_model` | usar em persuasão relevante | `test_method_parsing` |
| 3Ps de acompanhamento | progresso, problemas, prioridade | execução | `follow_up_3Ps` | formato de revisão curta | eval revisão |
| 6Ps de vendas | atenção até objeções | execução | `sales_6Ps` | apenas persuasão | teste spec |
| ABCCC | mensagem curta persuasiva | execução | `ABCCC` | apenas canal adequado | teste spec |
| Objetivo→informação→ação | fluxo pragmático | spec `principle` | ciclo | ação sem informação vira lacuna | `test_next_action` |
| Pesquisa→entendimento→ideias→decisão→comunicação | metaprocesso cognitivo | roteamento | `execution_skills` | foco envolve todas | `test_method_parsing` |
| DPA | decisão, próxima ação ou arquivamento | revisão | `dpa` | obrigatório ao concluir | `test_completed_cycle_requires_dpa` |
| Feedback | erro de previsão atualiza entendimento/plano | revisão | evidências e histórico | revisão registra mudança | eval revisão |
| Dono e prazo | tornar ação executável | revisão | `next_action` | ambos obrigatórios | teste DPA |
| Medidas de resultado/controláveis | medir efeito e esforço separadamente | qualidade | `metrics` | coleções distintas | avaliação privada |
| Aplicação parcial | usar só a etapa necessária | roteamento | modo/depth | short task usa TATT | `test_light_does_not_force_all_8rs` |
