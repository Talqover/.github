# Talqover/.github

Shared GitHub tooling for the Talqover repos. **This repository is public** — never commit secrets, customer names or internal URLs here.

## `actions/linear`

One copy of `linear.py`, the Linear helper the workflows use to pull ticket IDs out of branch names / PR titles and to comment on the issue. It replaces the per-repo `.github/scripts/linear.py` copies, which had drifted apart.

```yaml
- uses: Talqover/.github/actions/linear@v1   # puts linear.py on PATH, exports LINEAR_PY

- run: |
    TICKET=$(printf '%s' "$BRANCH" | linear.py extract --branch | head -1)
    linear.py comment "$TICKET" "Deployed in release v$VERSION"
    # one comment per subject, edited in place on later runs:
    linear.py comment "$TICKET" "Claude review — PR #12: …" --replace-prefix "Claude review — PR #12:"
  env:
    LINEAR_API_KEY: ${{ secrets.LINEAR_API_KEY }}   # only on the steps that comment
```

Never fails the caller: no key → warning, unknown ID → `SKIP`, Linear down → warning. Inline Python can `import linear` from `$(dirname "$LINEAR_PY")`.

Versioning: callers pin `@v1`. A compatible change moves the `v1` tag; a breaking one ships as `v2`.

Tests: `python -m unittest discover -s actions/linear -p 'test_*.py'` (also in CI).

## `docs/linear-ticket-comments.md`

Canonical text of the convention "work tied to a ticket leaves a comment on the Linear issue with what was measured, decided and not verified", with the blocks each repo copies into its `CLAUDE.md` / `AGENTS.md`.

## `docs/linear-issue-minimum.md`

Canonical text of the convention "every Linear issue carries a short floor — current state with evidence, desired state, verifiable done criterion — and is searched for before it is opened", with the blocks each repo copies into its `CLAUDE.md` / `AGENTS.md`. It lives here and not only in the Linear templates because an issue created through the MCP with a `description` drops the template body.

## `docs/linear-issue-pickup.md`

The reader side of the issue floor: what whoever executes a Linear issue does before starting, generically and per issue type (Bug, Tarefa técnica, Discovery, Entregável), plus the short text pasted into the Linear templates through the UI. Same `CLAUDE.md` / `AGENTS.md` blocks pattern.
