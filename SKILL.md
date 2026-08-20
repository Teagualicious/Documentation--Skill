---
name: project-documentation-builder
description: Analyze software repositories, low-code or no-code automations, workflow exports, screenshots, diagrams, and project descriptions to create synchronized developer or administrator documentation and simplified end-user instructions with safe troubleshooting. Use this skill whenever the user asks for project documentation, a technical handoff, architecture documentation, onboarding material, a runbook, an SOP, a user guide, debugging documentation, Power Automate documentation, workflow documentation, documentation refreshes, or documentation for a GitHub codebase—even when they do not explicitly call it a skill.
---

# Project Documentation Builder

Create two synchronized documentation products from one evidence record:

1. `DEVELOPER_GUIDE.md`
2. `USER_GUIDE.md`

For a low-code project, the first document may use the displayed title **Builder and Administrator Guide**, but keep the filename `DEVELOPER_GUIDE.md` unless the user requests another name.

## Select the operating mode

Use the input evidence—not only the user's wording—to select a mode.

- Read `modes/repository-analysis.md` for a GitHub repository, local repository, or source archive.
- Read `modes/guided-build.md` for descriptions, screenshots, exports, diagrams, run history, or low-code/no-code projects.
- Read `modes/hybrid-analysis.md` when conventional code, low-code workflows, external systems, and human steps form one solution.
- Read `modes/refresh-documentation.md` when previous documentation or an earlier source version exists.

When two modes apply, use hybrid mode as the coordinator and read the relevant supporting mode files.

## Mandatory workflow

### 1. Establish scope and source version

Record the project name, source type, source locator, branch/export/version when available, requested scope, included systems, excluded systems, and intended audiences.

Do not silently document an entire monorepo when the request concerns one application or workflow.

### 2. Analyze available evidence before asking questions

Inspect supplied files, repositories, exports, screenshots, descriptions, tests, run results, and existing documentation first.

Do not ask the user for facts already present in the evidence.

### 3. Build the shared evidence record

Create or update:

- `.project-guide/evidence.json`
- `.project-guide/open-questions.md`
- `.project-guide/documentation-manifest.json`

Read `references/evidence-model.md` when that file is available. Follow the schemas in `schemas/` when present.

Classify every material claim as:

- `confirmed`
- `inferred`
- `unknown`
- `conflict`

Classify implementation state as:

- `current`
- `intended`
- `planned`
- `deprecated`
- `unknown`

Never combine current and intended behavior without disclosing the difference.

### 4. Resolve material gaps

Ask clarification questions only when the answer changes setup, architecture, user steps, permissions, failure recovery, ownership, or another material part of the guides.

Ask no more than five questions in one batch. For each question:

- State the missing fact.
- Explain why it matters.
- Offer a proposed assumption when one is safe.

Read `references/clarification-question-bank.md` for reusable question patterns.

If the user cannot answer, preserve the item as `unknown` rather than inventing a conclusion.

### 5. Generate the developer or administrator guide

Read:

- `references/developer-guide-requirements.md`
- `assets/developer-guide-template.md`

Make the guide implementation-oriented and traceable. Include setup, architecture, workflows, interfaces, security, validation, deployment, monitoring, troubleshooting, maintenance, evidence limitations, and unresolved questions when applicable.

### 6. Generate the end-user guide

Read:

- `references/user-guide-requirements.md`
- `assets/user-guide-template.md`
- `assets/troubleshooting-matrix-template.md`

Write for the actual user role. Lead with the normal workflow, explain what success looks like, include only safe recovery steps, and state when to stop and escalate.

Do not turn the developer guide into a shorter user guide. Use the user guide's separate information architecture.

### 7. Validate before completion

Read `references/documentation-quality-rubric.md`.

At minimum, verify:

- Both guides use the same project and workflow names.
- User steps agree with the technical workflow.
- Every exact path, command, action, interface, and setting is supported or labeled.
- Troubleshooting matches actual failure behavior.
- User actions do not require administrator permissions unless clearly labeled.
- Current and intended behavior remain distinct.
- Unknowns and conflicts remain visible.
- No secrets, credentials, tokens, private keys, connection strings, or unnecessary personal data appear.

Run deterministic helpers in `scripts/` when the environment supports them.

### 8. Report completion honestly

Summarize:

- Documents produced or updated
- Source version analyzed
- Validation performed
- Material assumptions
- Remaining unknowns or conflicts

Do not claim full coverage when scope, evidence, or validation was partial.

## Source and evidence rules

Read `references/source-priority-rules.md` before resolving conflicting sources.

General priority for current behavior:

1. Executable code or exported workflow definitions
2. Tests and observed run results
3. Deployment and configuration
4. Existing documentation
5. Comments and naming
6. Inference

General priority for intended behavior:

1. Explicit owner or stakeholder answer
2. Approved requirements
3. Existing documentation
4. Inference

## Security rules

Never reproduce secret values. Document secret names, ownership, location, rotation responsibility, and safe setup procedures only.

Use synthetic examples. Redact real customer, employee, financial, health, authentication, and connection data unless the user explicitly requires a necessary field and sharing it is safe.

## Repository safety

Repository analysis is read-only by default. Do not create branches, commits, pull requests, issues, or file changes unless the user separately authorizes those actions.

## Output rules

Unless the user explicitly limits the request, produce both primary documents.

Use exact filenames:

- `DEVELOPER_GUIDE.md`
- `USER_GUIDE.md`

Keep internal support artifacts under `.project-guide/`.

When the user requests another artifact format, retain the evidence workflow and two-audience separation even if the final files are PDF, DOCX, HTML, or another format.
