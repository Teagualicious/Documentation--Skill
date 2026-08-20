# Evidence Model

The evidence record is the shared source for both `DEVELOPER_GUIDE.md` and `USER_GUIDE.md`. Build or update it before generating either document.

## Files

- `.project-guide/evidence.json` — project, source version, claims, components, workflows, and open questions.
- `.project-guide/open-questions.md` — human-readable unresolved questions and proposed assumptions.
- `.project-guide/documentation-manifest.json` — generated documents, source revision, validation, changed sections, and refresh history.

Use the JSON schemas in `schemas/` as the machine-readable contracts.

## Top-level evidence structure

```json
{
  "schema_version": "1.0.0",
  "project": {},
  "source_version": {},
  "facts": [],
  "components": [],
  "workflows": [],
  "open_questions": [],
  "analysis_limitations": []
}
```

## Project identity

Record:

- Stable project ID
- Display name
- Source type
- Documented scope
- Included systems
- Excluded systems
- Intended audiences
- Current maturity when known

Do not use a branch name or export filename as the stable project ID. Those values belong in `source_version`.

## Source version

A source-version record identifies exactly what was analyzed:

```json
{
  "source_type": "github_repository",
  "locator": "owner/repository",
  "ref": "main",
  "revision": "full-commit-sha",
  "environment": "production",
  "analyzed_at": "2026-08-20T17:00:00Z"
}
```

Use `unknown` for a field whose value cannot be established. Do not omit required fields merely because the source is description-only.

## Evidence facts

Use one fact for one material claim. Avoid large paragraphs containing several claims with different evidence.

```json
{
  "id": "FACT-001",
  "category": "deployment",
  "claim": "Production deployment runs through the release workflow.",
  "verification_state": "confirmed",
  "implementation_state": "current",
  "confidence": 1.0,
  "sources": [
    {
      "type": "repository_file",
      "location": ".github/workflows/release.yml",
      "version": "full-commit-sha",
      "lines": "1-78"
    }
  ],
  "used_in": [
    "developer-guide:deployment"
  ]
}
```

### Verification states

- `confirmed` — directly supported. At least one source is required.
- `inferred` — strongly suggested but not explicit. Include supporting sources or a rationale.
- `unknown` — unavailable. Include a rationale and create an open question when the gap is material.
- `conflict` — credible sources disagree. Include at least two sources and conflict details.

### Implementation states

- `current` — behavior present in the analyzed implementation.
- `intended` — owner-approved expected behavior that may differ from implementation.
- `planned` — future work not yet implemented.
- `deprecated` — retained for history but not current instructions.
- `unknown` — state cannot be established.

Never change `intended` or `planned` to `current` without new implementation evidence.

## Sources

A source records where a claim came from, not merely a source category.

Required fields:

- `type`
- `location`
- `version`

Optional fields include line range, artifact ID, environment, observation time, and notes.

Use synthetic identifiers in tests and examples. Never store secret values in a source note.

## Components

Create components only for material architectural units. A component should explain a responsibility or boundary, not represent every trivial file.

Record:

- Stable ID
- Name and type
- Purpose
- Inputs and outputs
- Dependencies
- Configuration names
- Interfaces
- Owners
- Failure modes
- Diagnostics
- Tests
- Verification and implementation states
- Sources

## Workflows

A workflow represents a user or system path from trigger to success or failure.

Record:

- Stable ID and name
- Actor
- Preconditions
- Trigger
- Ordered steps
- Branches and transformations
- External calls and state changes
- Outputs and success state
- Failure states
- Retry, duplicate, and recovery behavior
- Escalation conditions
- Sources

## Open questions

Create an open question only for a material unresolved fact. Each question should contain:

- Stable ID
- Question
- Why the answer matters
- Proposed assumption when safe
- Status
- Related fact, component, or workflow IDs

Statuses are `open`, `answered`, `deferred`, and `not_applicable`.

When answered, preserve the question for history, add the answer and source, and update the linked evidence item.

## Document usage links

Use `used_in` values to link facts to document sections. Recommended format:

- `developer-guide:architecture`
- `developer-guide:deployment`
- `user-guide:primary-workflow`
- `user-guide:troubleshooting`

These links support refresh impact analysis and cross-document validation.

## Refresh behavior

On refresh:

1. Preserve stable IDs when the same concept remains.
2. Add new evidence sources and source revisions.
3. Mark obsolete facts `deprecated` rather than rewriting history when the old fact remains relevant.
4. Update both documents for every changed fact used by both.
5. Record changed sections in the documentation manifest.

## Validation

Run:

```bash
python scripts/validate_evidence.py .project-guide/evidence.json
python scripts/validate_evidence.py .project-guide/documentation-manifest.json --kind manifest
```

The validator is intentionally standard-library-only. It checks the high-value semantic rules that generic JSON parsing does not enforce reliably, including unique IDs and evidence requirements by verification state.
