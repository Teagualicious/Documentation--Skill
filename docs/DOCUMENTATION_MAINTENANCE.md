# Documentation Maintenance Contract

This file defines the required documentation practices for every implementation phase and every future change to the Project Documentation Builder skill.

## 1. Source-of-truth files

The following files have distinct responsibilities:

- `status.md` — authoritative project handoff, phase state, decisions, risks, next actions, and completion evidence.
- `README.md` — concise public orientation and current capabilities.
- `SKILL.md` — runtime routing and non-negotiable operating rules for the skill.
- `modes/*.md` — mode-specific execution workflows.
- `references/*.md` — detailed domain rules, quality standards, and platform guidance loaded only when relevant.
- `assets/*.md` — output templates and reusable document structures.
- `schemas/*.json` — machine-readable contracts for internal artifacts.
- `scripts/` and `tests/` — deterministic helpers and their verification.

Do not duplicate detailed rules across several files. Put each rule in its authoritative location and link to it elsewhere.

## 2. Same-change documentation rule

Any change that alters behavior, inputs, outputs, file structure, schemas, validation, troubleshooting, or supported platforms must update the affected documentation in the same commit.

At minimum, review:

1. `status.md`
2. `README.md`
3. `SKILL.md`
4. The affected mode or reference file
5. Output templates
6. Schemas and tests

A phase is not complete when implementation exists but its documentation remains aspirational or outdated.

## 3. Mandatory `status.md` update

Every phase commit must update `status.md` with:

- Date and phase state
- Work completed
- Files added or changed
- Validation performed and results
- Decisions made
- Known limitations or unresolved questions
- Exact next actions for a future developer or session
- Commit or branch evidence once available

Use only these phase states:

- `NOT STARTED`
- `IN PROGRESS`
- `BLOCKED`
- `COMPLETE`

Do not mark a phase `COMPLETE` until its completion criteria and validation checks pass.

## 4. Evidence-first documentation

Documentation must distinguish:

- **Confirmed** — directly supported by code, exported workflow definitions, tests, run results, or an explicit user answer.
- **Inferred** — strongly suggested by evidence but not explicitly confirmed.
- **Unknown** — required information is unavailable.
- **Conflict** — credible sources disagree.

Do not turn an inference into a fact merely to make a document appear complete. Preserve unknowns and conflicts in both the evidence record and the appropriate guide.

## 5. Current versus intended behavior

When source code, workflow exports, existing documentation, and stakeholder descriptions disagree, document both:

- **Current behavior** — what the implementation actually does.
- **Intended behavior** — what the project owner says it should do.

Ask whether the difference is an accepted limitation, unfinished work, defect, or outdated documentation. Never silently merge the two.

## 6. Two-document synchronization

`DEVELOPER_GUIDE.md` and `USER_GUIDE.md` must be generated from the same evidence record.

Before completion, confirm that:

- Project and workflow names match.
- The user workflow agrees with the technical flow.
- Inputs, outputs, and success states do not conflict.
- User troubleshooting does not require administrator-only actions.
- Owners and escalation paths match.
- Known limitations appear at the appropriate level in both documents.

The user guide is not a shortened developer guide. It must use a separate audience-appropriate structure.

## 7. Change-impact practice

Before editing documentation, identify which evidence and document sections are affected by the implementation change.

For refresh work:

1. Compare the previous source version with the new version.
2. Identify changed components, workflows, interfaces, or operations.
3. Re-analyze only the impacted areas plus their direct dependencies.
4. Update both documents together.
5. Record a concise documentation change summary in the manifest and `status.md`.

## 8. Security and privacy

Never copy the following into generated documentation, evidence records, examples, fixtures, logs, or status files:

- Passwords
- API tokens
- Private keys
- Connection strings
- Session cookies
- Production `.env` values
- Real customer or employee data unless strictly necessary and explicitly approved
- Power Platform connection secrets

Document secret *names*, ownership, required permissions, and safe configuration procedures without reproducing values.

Use synthetic values in examples and tests.

## 9. Deterministic validation

Prefer scripts for checks that can be objectively verified, including:

- Path existence
- Schema structure
- Duplicate evidence IDs
- Unsupported commands or action names
- Cross-document name consistency
- Sensitive-value detection
- Test and fixture validation

Do not rely only on a model’s final review when a deterministic check is possible.

## 10. Documentation style

Developer documentation must be precise, traceable, and implementation-oriented.

End-user documentation must:

- Use plain language.
- Lead with the normal workflow.
- Explain what success looks like.
- Provide only safe troubleshooting actions.
- State when to stop and escalate.
- Avoid internal architecture unless it helps the user recover safely.

Use exact names for paths, flows, actions, fields, and interfaces when confirmed. Label placeholders and assumptions explicitly.

## 11. Phase completion checklist

Before marking any phase complete:

- [ ] The phase completion criteria in `status.md` are satisfied.
- [ ] Implementation and documentation changed together.
- [ ] New behavior has tests or an explicit manual validation record.
- [ ] Evidence and schema changes remain compatible or include a migration note.
- [ ] Sensitive values were not introduced.
- [ ] `README.md` accurately reflects current—not planned—capabilities.
- [ ] `status.md` contains exact next steps for handoff.
- [ ] Known gaps are recorded instead of hidden.

## 12. Future-session pickup rule

A future developer or AI session should be able to begin by reading, in order:

1. `status.md`
2. `docs/DOCUMENTATION_MAINTENANCE.md`
3. `SKILL.md`
4. The mode file for the next active phase
5. Relevant schemas, scripts, and tests

If that sequence is insufficient to resume work without reconstructing prior decisions, the current phase is not properly handed off.
