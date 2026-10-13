# Convenção: o ticket do Linear guarda o raciocínio

Texto canônico. Cada repo copia o bloco abaixo para o seu `CLAUDE.md` (e o resumo para o `AGENTS.md`, se tiver um). Quando mudar aqui, propague.

O PR mostra o que mudou; o commit, quando. Nenhum dos dois mostra o que foi medido, tentado e descartado — e é no ticket que alguém volta meses depois.

## Bloco para o `CLAUDE.md`

```markdown
## Linear: o ticket guarda o raciocínio

Ao terminar trabalho ligado a um ticket (investigação, bugfix, feature), deixe um comentário **no issue do Linear**: pelo MCP do Linear na sessão interativa, ou `linear.py comment <ID> "<markdown>"` em CI (via `Talqover/.github/actions/linear@v1`). Texto canônico: `Talqover/.github/docs/linear-ticket-comments.md`.

- **Comenta quando** a investigação produziu algo que não está no diff: número medido, causa descartada, decisão com alternativa rejeitada, premissa do ticket que se mostrou errada.
- **Não comenta quando** o PR já conta a história inteira (mudança pequena, óbvia, sem decisão no caminho). Ruído faz as pessoas pararem de ler — e aí nem os comentários bons são lidos. Um comentário por marco, não um por sessão.
- **Formato curto e sempre o mesmo**, três blocos:
    - **Medido** — o número e de onde veio (query, réplica, log, período).
    - **Decidido** — e a alternativa descartada, com o motivo.
    - **Não verificado** — o limite honesto do que se sabe.
- **Nunca entra** (o comentário é legível pelo workspace inteiro): credencial de qualquer tipo (senha, chave, connection string, token); PII de produção (telefone, nome, documento — nem em exemplo de query); cliente identificado sem autorização. Query de diagnóstico pode; o resultado bruto dela com dado pessoal, não.
- Comentários automáticos de CI (deploy, resumo de review) são rede de proteção, não substituto — "review feita" não é raciocínio.
```

## Resumo para o `AGENTS.md`

```markdown
- **Linear ticket keeps the reasoning** (canonical: `Talqover/.github/docs/linear-ticket-comments.md`): when work tied to a ticket ends, post a comment on the Linear issue (Linear MCP interactively, `linear.py comment` in CI) — only when the work produced something the diff doesn't show (a measured number, a discarded cause, a decision with a rejected alternative, a ticket premise proven wrong); skip it when the PR already tells the whole story; one comment per milestone, not per session. Fixed short format: **Medido** (number + source), **Decidido** (+ discarded alternative and why), **Não verificado** (honest limits). Never include credentials, production PII (phone, name, document — not even in a sample query) or an unauthorized identified customer — a diagnostic query is fine, its raw result with personal data is not. Automatic CI comments are a safety net, not a substitute.
```
