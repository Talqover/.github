# Convenção: ao pegar uma issue do Linear

Texto canônico. Cada repo copia o bloco abaixo para o seu `CLAUDE.md` (e o resumo para o `AGENTS.md`, se tiver um). Quando mudar aqui, propague.

`linear-issue-minimum.md` diz o que quem **escreve** a issue precisa trazer. Este diz o que quem **executa** faz antes de começar, por tipo de issue — o pedaço de prompt que antes vivia, quando vivia, na cabeça de quem abriu.

Mora aqui e não no corpo do template porque `save_issue` com `template` + `description` descarta o corpo: issue criada por agente nunca carrega o que estiver só no template. O template leva uma versão curta, para quem abre e executa pela UI.

## Para qualquer issue

1. **Leia a issue inteira**: corpo, comentários e issues relacionadas. Decisão costuma estar num comentário, não no corpo.
2. **Piso faltando → pergunte antes de executar**, a quem abriu ou no ticket. Sem "Pronto quando" verificável, quem executa inventa um — é exatamente a interpretação que o piso evita.
3. **Confirme o "Hoje" antes de mudar qualquer coisa**: veja no código, no banco ou na tela. Se a premissa da issue estiver errada, diga no ticket — é um comentário de **Decidido** (ver `linear-ticket-comments.md`), não um desvio silencioso.
4. **Escopo é o da issue.** Achou outra coisa no caminho → issue nova (com o piso), não escopo extra no mesmo PR.

## Por tipo

| Tipo (template) | Antes de começar | Pronto quando, além do critério da issue |
| -- | -- | -- |
| **Bug** | Reproduza ou localize o comportamento atual e cite arquivo:linha **antes** de propor correção. Separe causa de sintoma. Não reproduziu → diga o que tentou; não corrija no escuro. | Um teste cobre o bug — falha sem a correção (no CI, ou explicado no PR) — ou o motivo de não haver teste está no PR. |
| **Tarefa técnica** | Leia "Fora de escopo" e respeite. Verifique se muda regra de negócio documentada. | Cada critério de aceite verificado e listado no PR; o que não foi verificado, dito. |
| **Discovery** | A saída é uma decisão, não um resumo. Separe o que foi ouvido ou medido do que é interpretação. | Documento de uma página com recomendação e a decisão que ela destrava, linkado na issue. |
| **Entregável** | Confirme quem usa e onde vai ficar. | "Onde fica" com o link; quem usa foi avisado. |

Meta de ciclo (CRM) e Experimento de canal não têm linha: são trabalho comercial, não executado por agente. Valem os quatro passos gerais.

## Bloco para o `CLAUDE.md`

```markdown
## Linear: ao pegar uma issue

Antes de executar uma issue do Linear. Texto canônico: `Talqover/.github/docs/linear-issue-pickup.md`.

- **Leia corpo, comentários e relacionadas** (`get_issue` com `includeRelations: true` + `list_comments`). Decisão costuma estar num comentário.
- **Piso faltando** (sem Hoje com evidência, Deveria ou Pronto quando verificável) → pergunte antes de executar (ao usuário, se houver um na sessão; senão no ticket); não invente o critério.
- **Confirme o "Hoje"** no código, banco ou tela antes de mudar algo. Premissa errada → diga no ticket (bloco **Decidido**), não desvie em silêncio.
- **Escopo é o da issue**; o que aparecer no caminho vira issue nova, com o piso.
- **Por tipo**:
    - **Bug** — reproduza ou cite arquivo:linha do comportamento atual **antes** de propor correção; separe causa de sintoma; não reproduziu → diga o que tentou. Teste que cobre o bug — falha sem a correção (no CI, ou explicado no PR) — ou o motivo de não ter no PR.
    - **Tarefa técnica** — respeite "Fora de escopo"; cheque regra de negócio afetada; cada critério de aceite verificado e listado no PR.
    - **Discovery** — a saída é uma decisão com recomendação, não um resumo; separe medido de interpretado. Pronto: documento de uma página linkado na issue, com a decisão que destrava.
    - **Entregável** — confirme antes quem usa e onde vai ficar. Pronto: "Onde fica" com link; quem usa avisado.
```

## Resumo para o `AGENTS.md`

```markdown
- **Picking up a Linear issue** (canonical: `Talqover/.github/docs/linear-issue-pickup.md`): read body, comments and related issues first (decisions often live in a comment). If the floor is missing (no Hoje with evidence, Deveria or verifiable Pronto quando), ask before executing (the user if there's one in the session, otherwise on the ticket) — don't invent the criterion. Confirm the current state in code, DB or UI before changing anything; a wrong premise goes on the ticket as **Decidido**, never a silent deviation. Scope is the issue's; anything found on the way becomes a new issue. By type — **Bug**: reproduce or cite file:line of the current behavior before proposing a fix, separate cause from symptom, say what you tried if it doesn't reproduce; a test that covers the bug — fails without the fix (in CI, or explained in the PR) — or the reason there isn't one in the PR. **Tarefa técnica**: respect "Fora de escopo", check affected business rules, list each acceptance criterion as verified in the PR. **Discovery**: the output is a decision with a recommendation, not a summary; separate measured from interpreted; done = a one-page document linked on the issue, with the decision it unlocks. **Entregável**: confirm first who uses it and where it will live; done = "Onde fica" linked, users notified.
```

## Texto para os templates (UI)

Colar no topo do corpo de **todos os seis** templates:

```markdown
> **Piso** — Hoje (com evidência) · Deveria · Pronto quando (verificável). Procurou se já existe, incluindo arquivadas? Texto-guia deixado aqui conta como vazio; seção que não se aplica, apague.
```

E no fim de **Bug**, **Tarefa técnica**, **Discovery** e **Entregável**, a seção `## Para quem executa` com a linha da tabela acima correspondente ao tipo.
