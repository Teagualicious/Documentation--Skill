# Project Documentation Builder — Status and Handoff

**Repository:** `Teagualicious/Documentation--Skill`  
**Active branch:** `build/project-documentation-skill`  
**Last updated:** 2026-08-20  
**Overall state:** `IN PROGRESS`  
**Current phase:** Phase 2 — Evidence layer

## TL;DR

This repository is being built into an evidence-backed Claude skill that documents conventional software, low-code/no-code automations, and hybrid systems. It produces two synchronized documents from one structured evidence record:

1. `DEVELOPER_GUIDE.md` — technical documentation for engineers, builders, administrators, maintainers, and future owners.
2. `USER_GUIDE.md` — simplified instructions for normal use, safe troubleshooting, and escalation.

The conceptual starting point was `sojohnnysaid/project-guide`: inventory, analyze, collect findings, and synthesize documentation. This is a clean implementation rather than a wrapper or code copy. It replaces unbounded recursive summarization, free-form findings, a hard-coded model dependency, and a single generic guide with targeted analysis, structured evidence, adaptive clarification, two audience-specific outputs, source versioning, and deterministic validation.

A future developer or session should read, in order:

1. This file
2. `docs/DOCUMENTATION_MAINTENANCE.md`
3. `SKILL.md`
4. The mode file for the active phase
5. Relevant schemas, scripts, and tests

## Product contract

### Operating modes

- **Repository Analysis Mode** — accepts a GitHub repository, local repository, or source archive; analyzes first and asks only questions the codebase cannot answer.
- **Guided Build Mode** — accepts descriptions, screenshots, diagrams, exports, run history, forms, errors, and SOPs for Power Automate, Power Apps, SharePoint, Excel/VBA, Zapier, Make, and other low-code or process-heavy projects.
- **Hybrid Mode** — documents boundaries among conventional code, workflows, data stores, external platforms, dashboards, and human review.
- **Refresh Mode** — compares prior and current source versions, re-analyzes affected areas, and updates both guides together.

### Primary outputs

- `DEVELOPER_GUIDE.md`
- `USER_GUIDE.md`

For low-code projects, the displayed title of the developer document may be **Builder and Administrator Guide** while retaining the standard filename.

### Internal support artifacts

- `.project-guide/evidence.json`
- `.project-guide/open-questions.md`
- `.project-guide/documentation-manifest.json`

These are the shared source for both documents and support later refreshes.

## Evidence model

Every material claim must include a stable ID, category, claim text, implementation state, verification state, confidence, sources, and the document sections that use it.

Verification states:

- `confirmed` — directly supported by code, exported definitions, tests, run results, or an explicit owner answer.
- `inferred` — strongly suggested but not explicitly confirmed.
- `unknown` — required information is unavailable.
- `conflict` — credible sources disagree.

Implementation states:

- `current`
- `intended`
- `planned`
- `deprecated`
- `unknown`

Current and intended behavior must never be silently combined.

Default source priority for current behavior:

1. Executable code or exported workflow definitions
2. Tests and observed run results
3. Deployment and configuration
4. Existing documentation
5. Comments and naming
6. Inference

Default source priority for intended behavior:

1. Explicit owner or stakeholder answer
2. Approved requirements
3. Existing documentation
4. Inference

## Required guide coverage

### Developer / builder guide

1. Project overview, scope, maturity, source version, and status
2. System context and external boundaries
3. Architecture and component responsibilities
4. Workflow and data flow
5. Setup, installation/import, and configuration
6. Interfaces and data contracts
7. Security, permissions, credential ownership, and data handling
8. Testing and validation
9. Deployment, promotion, release verification, and rollback
10. Monitoring, diagnostics, failure modes, and recovery
11. Maintenance, common changes, technical debt, and limitations
12. Evidence, assumptions, conflicts, and unresolved questions

### End-user guide

1. What the tool does
2. Who should use it and when not to use it
3. Before you begin
4. Primary workflow
5. Expected results and visible success state
6. Common tasks
7. Simplified troubleshooting
8. What users should not change
9. Getting help and information to collect
10. Quick reference and user-relevant limitations

The user guide is not a shortened developer guide. It must provide only safe role-appropriate recovery actions. Connector replacement, credential changes, production edits, record deletion, and forced reruns remain administrator-only.

## Current repository structure

```text
.
├── SKILL.md
├── README.md
├── status.md
├── docs/
│   └── DOCUMENTATION_MAINTENANCE.md
├── modes/
│   ├── repository-analysis.md
│   ├── guided-build.md
│   ├── hybrid-analysis.md
│   └── refresh-documentation.md
├── references/
│   ├── source-priority-rules.md
│   ├── clarification-question-bank.md
│   ├── documentation-quality-rubric.md
│   ├── developer-guide-requirements.md
│   ├── user-guide-requirements.md
│   └── platform-profiles/
│       ├── generic-low-code.md
│       └── power-automate.md
└── assets/
    ├── developer-guide-template.md
    ├── user-guide-template.md
    ├── troubleshooting-matrix-template.md
    ├── architecture-diagram-template.md
    └── workflow-diagram-template.md
```

Schemas, deterministic scripts, tests, and evaluations are added in later phases and must not be treated as complete until the phase table says so.

## Phase plan

| Phase | Name | State | Completion criteria |
|---|---|---:|---|
| 0 | Foundation and governance | `COMPLETE` | Handoff, README, documentation contract, branch, and phase rules are committed. |
| 1 | Skill scaffold | `COMPLETE` | Valid `SKILL.md`, all mode files, output templates, platform profiles, and quality references exist. |
| 2 | Evidence layer | `IN PROGRESS` | Evidence and manifest schemas exist; validation rejects invalid states, duplicate IDs, incomplete source versions, and unsupported confirmed facts. |
| 3 | Repository analysis MVP | `NOT STARTED` | Targeted inventory excludes noise, classifies files, flags sensitive paths, and passes tests. |
| 4 | Guided-build MVP | `NOT STARTED` | Adaptive low-code intake and Power Automate guidance produce a workflow blueprint with visible unknowns. |
| 5 | Document generation | `NOT STARTED` | Both guides can be generated from one evidence record and pass consistency checks. |
| 6 | Deterministic validation | `NOT STARTED` | Source-reference, cross-document, and sensitive-value validators are implemented and tested. |
| 7 | Evaluation and hardening | `NOT STARTED` | Repository, misleading-docs, monorepo, Power Automate, description-only, hybrid, refresh, and security cases are evaluated. |

## Phase deliverables

### Phase 0 — Foundation and governance

Delivered:

- Expanded `README.md`
- Full handoff and phase plan in `status.md`
- Mandatory documentation rules in `docs/DOCUMENTATION_MAINTENANCE.md`
- Feature branch

Commit: `b954a3d9042faad30626da32980a5c75823256a2`

### Phase 1 — Skill scaffold

Delivered:

- Runtime `SKILL.md`
- Repository, guided-build, hybrid, and refresh workflows
- Developer and user templates
- Architecture, workflow, and troubleshooting templates
- Source-priority, clarification, guide-requirement, and quality references
- Generic low-code and Power Automate platform profiles

Validation:

- `SKILL.md` contains required frontmatter and mode routing.
- All local Markdown links in the scaffold resolve.
- Both output structures are separate and explicit.
- Security, evidence, clarification, and repository read-only rules are present.

### Phase 2 — Evidence layer

Next deliverables:

- `references/evidence-model.md`
- `schemas/project-evidence.schema.json`
- `schemas/component.schema.json`
- `schemas/workflow.schema.json`
- `schemas/documentation-manifest.schema.json`
- `scripts/validate_evidence.py`
- Synthetic evidence fixtures and tests

Completion gate:

- Invalid verification or implementation states, duplicate IDs, missing sources for confirmed facts, and incomplete source-version records are rejected.

### Phase 3 — Repository analysis MVP

Planned deliverables:

- `scripts/inventory_repository.py`
- Default exclusions
- Orientation-file classification and priority
- Sensitive-path flags without exposing contents
- Standard-library tests with synthetic fixtures

### Phase 4 — Guided-build MVP

Planned deliverables:

- Formal workflow blueprint procedure
- Adaptive interview coverage
- Power Automate artifact map
- Connection, permission, ownership, reliability, and operations coverage
- Description-only fallback

### Phase 5 — Document generation

Planned deliverables:

- Evidence-to-guide generation workflow
- Diagram rules
- Simplified troubleshooting generation
- Source metadata, assumptions, and limitations

### Phase 6 — Deterministic validation

Planned deliverables:

- Source-reference validator
- Cross-document consistency validator
- Sensitive-value detector
- Documentation comparison helper

### Phase 7 — Evaluation and hardening

Initial evaluation cases:

1. Small Python repository
2. Repository with misleading documentation
3. Large monorepo
4. Power Automate solution export
5. Description-only automation
6. Hybrid software/workflow project
7. Security and secret-handling case
8. Documentation refresh case

## Mandatory documentation practices

The full contract is in `docs/DOCUMENTATION_MAINTENANCE.md`. These rules are non-negotiable:

1. Update `status.md` in the same commit as every phase change.
2. Update behavior and affected documentation together.
3. Do not mark a phase complete until its criteria and validation pass.
4. Record work completed, files changed, validation, decisions, limitations, and exact next actions.
5. Keep `README.md` limited to current capabilities; planned work belongs here.
6. Generate both guides from the same evidence record.
7. Preserve confirmed, inferred, unknown, and conflict states.
8. Separate current behavior from intended behavior.
9. Never place secrets or real sensitive data in documentation, evidence, tests, fixtures, logs, or examples.
10. Prefer deterministic validation whenever a claim can be checked programmatically.
11. Record source versions and change impact for refreshes.
12. Keep the future-session pickup sequence accurate.

## Current decisions

- Build on a feature branch rather than `main`.
- Use a clean implementation inspired by the source prototype rather than copying its code.
- Keep runtime instructions model-provider-independent; no direct Anthropic SDK dependency.
- Keep deterministic helpers standard-library-first where practical.
- Analyze evidence before asking questions.
- Use one evidence record for both guides.
- Keep repository analysis read-only unless writes are separately authorized.
- Do not choose a repository license without the owner’s explicit decision.
- Use Mermaid as the initial diagram format where rendering support exists, with text fallback.

## Known risks and unresolved decisions

- Installation and distribution packaging for Claude has not been selected.
- Repository license is not selected.
- Power Automate solution and non-solution exports may require separate parsing paths.
- Large monorepos need scope and analysis-budget controls beyond deterministic inventory.
- Refresh comparison must support both Git revisions and low-code export versions.
- Diagram portability must be verified across target documentation formats.

## Change log

### 2026-08-20 — Phase 1 completed

- Added the runtime skill scaffold and all four mode workflows.
- Added audience-specific templates and low-code platform guidance.
- Added source-priority, clarification, quality, security, and safety rules.
- Updated `README.md` and this handoff in the same phase change.

### 2026-08-20 — Phase 0 completed

- Created the feature branch.
- Added the original handoff, phased plan, README, and documentation contract.

## Exact next actions

1. Implement the evidence model reference.
2. Add project-evidence, component, workflow, and manifest schemas.
3. Add a standard-library evidence validator.
4. Add synthetic valid and invalid fixtures plus tests.
5. Run all Phase 2 checks.
6. Update this file in the Phase 2 commit to mark Phase 2 complete and Phase 3 in progress.
