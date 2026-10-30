# Convenção: o piso de uma issue no Linear

Texto canônico. Cada repo copia o bloco abaixo para o seu `CLAUDE.md` (e o resumo para o `AGENTS.md`, se tiver um). Quando mudar aqui, propague.

Issue mal escrita vira interpretação de quem pega. O problema não é falta de template — os templates do time existem e são abertos em branco, com o texto-guia no lugar da resposta. Formulário longo não é preenchido; o que funciona é um piso curto, que vale para qualquer tipo de issue, e procurar antes de abrir — duplicata custa mais que falta de detalhe.

Agente que abre issue pelo MCP (`save_issue` com `description`) **substitui o corpo do template**: só label e defaults sobrevivem. Por isso o piso mora aqui, e não só no template.

## O piso

1. **Hoje** — o estado atual, com evidência: print, log, linha de código, número do banco. Não "está com problema".
2. **Deveria** — o estado desejado, em uma frase.
3. **Pronto quando** — critério verificável. Não "funcionando".

**Bug** soma o mínimo para reproduzir: URL ou UUID (chamada, environment, campanha) e o que foi feito, em passos.

Texto-guia do template deixado no corpo conta como campo vazio. Seção que não se aplica, apague.

## Antes de abrir, procurar

Buscar o termo **em todos os times, incluindo arquivadas e concluídas**. Já existe → comentar ou reabrir lá, e não abrir outra nem reescrever o corpo dela. Parece parecido mas é diferente → abrir e relacionar (`related`), dizendo em uma linha a diferença.

## Quem garante

Quem tria. Issue que não passa no piso **não sai de Triage**: volta para quem abriu com um comentário dizendo o que falta — sem reescrever por ele. Não há automação; medir por amostra das issues abertas depois da convenção, não por impressão.

## Bloco para o `CLAUDE.md`

```markdown
## Linear: o piso de uma issue

Vale para toda issue que você abrir ou reescrever no Linear (MCP `save_issue`). Texto canônico: `Talqover/.github/docs/linear-issue-minimum.md`.

- **Procure antes de abrir**: `list_issues` com `query: <termo>` e `includeArchived: true`, sem `team` (todos os times, concluídas inclusas). Já existe → comente ou reabra lá; não reescreva o corpo de issue alheia. Parecida mas diferente → abra e relacione (`relatedTo`), dizendo a diferença em uma linha.
- **O corpo traz sempre três coisas**, qualquer que seja o tipo:
    - **Hoje** — o estado atual com evidência (arquivo:linha, log, query e o número que ela deu, print). Não "está com problema".
    - **Deveria** — o estado desejado, em uma frase.
    - **Pronto quando** — critério verificável. Não "funcionando".
- **Bug** soma a reprodução: URL ou UUID (chamada, environment, campanha) e os passos.
- `save_issue` com `template` **e** `description` descarta o corpo do template — escreva o piso você mesmo. Texto-guia de template deixado no corpo conta como vazio; seção que não se aplica, apague.
- **Nunca entra** (a issue é legível pelo workspace inteiro): credencial de qualquer tipo; PII de produção (telefone, nome, documento — nem em exemplo); cliente identificado sem autorização.
- **Triando** uma issue que não passa no piso: ela não sai de Triage — comente o que falta e devolva a quem abriu; não preencha por ele.
```

## Resumo para o `AGENTS.md`

```markdown
- **Linear issue floor** (canonical: `Talqover/.github/docs/linear-issue-minimum.md`): before opening an issue, search with `list_issues` (`query: <term>`, `includeArchived: true`, no `team`) — if it exists, comment or reopen there, never rewrite someone else's body; if it's similar but different, open it with `relatedTo`, stating the difference in one line. Every issue body carries three things: **Hoje** (current state with evidence — file:line, log, query + its number, screenshot; never "it's broken"), **Deveria** (desired state, one sentence), **Pronto quando** (verifiable acceptance criterion, never "working"). Bugs add reproduction: URL or UUID (call, environment, campaign) and the steps. `save_issue` with both `template` and `description` drops the template body — write the floor yourself; leftover template guide text counts as empty, delete sections that don't apply. Never include credentials, production PII, or an unauthorized identified customer. When triaging, an issue that misses the floor stays in Triage: comment what's missing and hand it back — don't fill it in for the author.
```
