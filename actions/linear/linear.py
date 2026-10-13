#!/usr/bin/env python3
"""Linear helper shared by the GitHub workflows.

Two jobs only: pull issue identifiers out of text, and post a comment on an
issue (or keep one comment per subject up to date, so a PR reviewed seven
times leaves one comment on the ticket, not seven). Issue STATUS is
deliberately not handled here — the Linear GitHub integration already attaches
the PR and moves the issue per each team's git automations, and a second actor
doing the same thing raced it on every merge.

The workspace has several teams (TAL, PLAT, DTECH, INFRA, ...) and any repo
can carry any team's issue, so the identifier is whatever the branch carries
and Linear resolves it; an identifier that is not in Linear is reported as
SKIP, and Linear being down or refusing the key is a warning — neither ever
fails the workflow.

This is the single copy: workflows get it through the composite action next to
it (`uses: Talqover/.github/actions/linear@v1`), which puts it on PATH and
exports LINEAR_PY. It replaced the per-repo copies in .github/scripts/, which
had already drifted apart.

Auth: LINEAR_API_KEY in the environment (a personal API key; Linear takes it
bare in the Authorization header, no "Bearer"). Without it the script warns
and exits 0 — the sync is a courtesy, not a gate.

Usage:
  linear.py extract [--branch] < text      # identifiers, one per line
  linear.py comment DTECH-6 "markdown"
  linear.py comment DTECH-6 "markdown" --replace-prefix "Claude review — PR #12:"
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.linear.app/graphql"


class LinearUnavailable(Exception):
    """Linear could not be reached or refused the call (bad key, 5xx, timeout)."""

# Only the workspace's real team keys count. A generic `[A-Za-z]{2,5}-N`
# pattern turned ordinary slugs into tickets — `fix/http-500-retry` → HTTP-500,
# `utf-8`, `phase-06` — which then won over the real ID in the PR title.
# Add a key here when a team is created in Linear.
TEAM_KEYS = ("DTECH", "TAL", "PLAT", "INFRA", "CS", "COM", "MKT", "BOA")
_KEYS = "|".join(TEAM_KEYS)

# Commit subjects and PR bodies are prose, so only the conventional uppercase
# spelling counts there. Branch names are what Linear itself generates
# (matheus/dtech-6-...), hence the lowercase form is accepted for them.
ID_STRICT = re.compile(rf"\b((?:{_KEYS})-[0-9]+)\b")
ID_BRANCH = re.compile(rf"(?<![A-Za-z0-9])((?:{_KEYS})-[0-9]+)(?![A-Za-z0-9])", re.IGNORECASE)


def extract(text: str, branch: bool = False) -> list[str]:
    pattern = ID_BRANCH if branch else ID_STRICT
    seen: list[str] = []
    for match in pattern.findall(text or ""):
        ident = match.upper()
        if ident not in seen:
            seen.append(ident)
    return seen


def gql(query: str, variables: dict) -> dict:
    key = os.environ.get("LINEAR_API_KEY", "")
    if not key:
        raise SystemExit("LINEAR_API_KEY is not set")
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.load(resp)
    except urllib.error.HTTPError as e:
        raise LinearUnavailable(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}") from e
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
        # URLError: DNS/connection; ValueError: a non-JSON body.
        raise LinearUnavailable(f"{type(e).__name__}: {e}") from e
    if body.get("errors"):
        # "Entity not found" is the normal answer for an identifier that is
        # not in Linear: callers treat an empty result as "skip", so it is
        # not raised here.
        return {"errors": body["errors"], "data": body.get("data") or {}}
    return body


def find(identifier: str) -> dict | None:
    body = gql(
        "query($id: String!) { issue(id: $id) { id identifier url } }",
        {"id": identifier},
    )
    return (body.get("data") or {}).get("issue") or None


def comment(issue: dict, markdown: str) -> None:
    body = gql(
        "mutation($issueId: String!, $body: String!) {"
        "  commentCreate(input: {issueId: $issueId, body: $body}) { success }"
        "}",
        {"issueId": issue["id"], "body": markdown},
    )
    ok = ((body.get("data") or {}).get("commentCreate") or {}).get("success")
    print(f"COMMENT | {issue['identifier']} | {'ok' if ok else body.get('errors')}")


def upsert(issue: dict, markdown: str, prefix: str) -> None:
    """Edit the issue's comment whose body starts with `prefix`, else create one.

    Match on a plain-text prefix: Linear re-serialises markdown (bold, links)
    when it stores a body, so a markdown prefix may not survive the round trip.
    """
    body = gql(
        "query($id: String!) { issue(id: $id) { comments(first: 250) { nodes { id body } } } }",
        {"id": issue["id"]},
    )
    nodes = (((body.get("data") or {}).get("issue") or {}).get("comments") or {}).get("nodes") or []
    existing = next((c for c in nodes if (c.get("body") or "").startswith(prefix)), None)
    if not existing:
        comment(issue, markdown)
        return
    body = gql(
        "mutation($id: String!, $body: String!) {"
        "  commentUpdate(id: $id, input: {body: $body}) { success }"
        "}",
        {"id": existing["id"], "body": markdown},
    )
    ok = ((body.get("data") or {}).get("commentUpdate") or {}).get("success")
    print(f"UPDATE | {issue['identifier']} | {'ok' if ok else body.get('errors')}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("extract")
    p.add_argument("--branch", action="store_true")

    p = sub.add_parser("comment")
    p.add_argument("identifier")
    p.add_argument("markdown")
    p.add_argument("--replace-prefix", default="")

    args = parser.parse_args(argv)

    if args.cmd == "extract":
        for ident in extract(sys.stdin.read(), branch=args.branch):
            print(ident)
        return 0

    # No key means the sync is not wired up (or the secret was removed). That
    # is a warning on the run, not a red check on the PR.
    if not os.environ.get("LINEAR_API_KEY"):
        print("::warning::LINEAR_API_KEY is not set — skipping Linear comment", file=sys.stderr)
        return 0

    # A Linear outage or a revoked key must not turn the caller red: release
    # workflows run this AFTER the release is published, where a failed step
    # also skipped the label step behind it and a re-run could not recover.
    try:
        issue = find(args.identifier)
        if not issue:
            print(f"SKIP | {args.identifier} | not found in Linear")
            return 0
        if args.replace_prefix:
            upsert(issue, args.markdown, args.replace_prefix)
        else:
            comment(issue, args.markdown)
    except LinearUnavailable as e:
        print(f"::warning::Linear unavailable — skipping comment on {args.identifier}: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
