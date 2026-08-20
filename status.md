# Project Documentation Builder — Status and Handoff

**Repository:** `Teagualicious/Documentation--Skill`  
**Active build branch:** `build/project-documentation-skill`  
**Last updated:** 2026-08-20  
**Overall state:** `IN PROGRESS`  
**Current phase:** Phase 0 — Foundation and governance

---

## TL;DR

This repository is being built into an evidence-backed Claude skill that documents both conventional software and low-code/process-heavy projects.

The skill will produce two synchronized outputs:

1. `DEVELOPER_GUIDE.md` — technical documentation for engineers, builders, administrators, maintainers, and future owners.
2. `USER_GUIDE.md` — simplified instructions for normal use, safe troubleshooting, and escalation.

It will support repository analysis, guided low-code intake, hybrid systems, and later documentation refreshes. The central design decision is to analyze or interview once, create a structured evidence record, resolve material gaps, and generate both documents from that same verified record.

Start every future session by reading this file and `docs/DOCUMENTATION_MAINTENANCE.md`.

---

## Origin and rationale

The design is based on the conceptual workflow in `sojohnnysaid/project-guide`:

1. Inventory a project.
2. Analyze files and directories.
3. Collect findings.
4. Synthesize a developer guide.

That prototype established a useful direction, but the new skill should not be a direct wrapper around its Python script. The prototype uses unbounded recursive text-file analysis, free-form findings, hard-coded model/API behavior, a single generic developer output, and no source-traceability or low-code interview path.

This implementation keeps the useful staged-analysis concept and replaces the weak points with:

- Targeted evidence collection
- Structured findings
- Clarification after analysis rather than before it
- Two audience-specific guides
- Repository, guided-build, hybrid, and refresh modes
- Source versioning
- Deterministic validation
- Explicit current-versus-intended behavior
- Security and privacy controls

No code from the source prototype is being copied into this repository. Its licensing status should be verified separately before any direct reuse.

---

## Product definition

### Skill name

**Display name:** Project Documentation Builder  
**Skill identifier:** `project-documentation-builder`

### Operating modes

#### 1. Repository Analysis Mode

Accept:

- GitHub repository URL or `owner/repository`
- Local repository directory
- Uploaded source archive
- Optional branch, tag, commit, package, application, or documentation scope

Behavior:

- Establish source version and scope.
- Inspect orientation files before recursively reading source.
- Build a targeted inventory.
- Trace components and workflows.
- Ask only questions that cannot be resolved from the repository.
- Remain read-only unless repository changes are separately authorized.

#### 2. Guided Build Mode

Accept:

- Written descriptions
- Screenshots
- Diagrams
- Screen recordings or transcripts
- Power Automate or Power Apps exports
- Run-history exports
- Forms and sample inputs
- Error messages
- Existing SOPs

Supported project types should include:

- Power Automate
- Power Apps
- SharePoint workflows
- Excel/VBA utilities
- Zapier
- Make
- Internal manual/automated processes
- Other low-code or no-code builds

Behavior:

- Examine supplied artifacts first.
- Build a formal workflow blueprint.
- Ask adaptive clarification questions only for material gaps.
- Document permissions, connections, failure handling, ownership, and operations—not only the happy path.

#### 3. Hybrid Mode

Use when a project combines conventional code with low-code workflows, data stores, dashboards, external services, or human approvals.

Document component boundaries and the complete chain from software to automation to human action.

#### 4. Refresh Mode

Use when prior documentation and a previous source version exist.

Compare versions, identify impacted components, re-analyze affected areas, update both guides together, and preserve a change summary.

---

## Required outputs

### Primary documents

- `DEVELOPER_GUIDE.md`
- `USER_GUIDE.md`

For low-code projects, the displayed developer-document title may be **Builder and Administrator Guide**, while still fulfilling the developer-document requirement.

### Internal support artifacts

- `.project-guide/evidence.json`
- `.project-guide/open-questions.md`
- `.project-guide/documentation-manifest.json`

These support accuracy and refreshes; they are not additional user-facing documentation products.

---

## Shared evidence model

Both repository analysis and guided-build interviews must populate the same project record before either guide is generated.

Each material claim must have:

- Stable ID
- Category
- Claim text
- Implementation state
- Verification state
- Confidence
- Sources
- Document sections that use the claim

### Verification states

- `confirmed` — directly supported by code, exported definitions, tests, run results, or an explicit owner answer.
- `inferred` — strongly suggested but not explicitly confirmed.
- `unknown` — required information is unavailable.
- `conflict` — credible sources disagree.

### Implementation states

- `current`
- `intended`
- `planned`
- `deprecated`
- `unknown`

The skill must never silently combine current and intended behavior.

### Source authority for current implementation

1. Executable code or exported workflow definition
2. Tests and observed run results
3. Deployment and configuration files
4. Existing documentation
5. Comments and naming conventions
6. Model inference

### Source authority for intended behavior

1. Explicit owner or stakeholder answer
2. Approved requirements or process specification
3. Existing documentation
4. Inference

---

## Repository Analysis Mode — target workflow

### Step 1: Establish scope and version

Capture repository, branch or commit, monorepo scope, requested applications, existing documentation, and generated-file exclusions.

### Step 2: Build a targeted inventory

Read in priority tiers rather than immediately reading every file.

**Tier 1 — Orientation**

- README and existing docs
- Dependency manifests
- Build configuration
- Deployment workflows
- Environment templates
- Top-level tree
- Entry points
- Tests and test configuration

**Tier 2 — Architecture**

- Public interfaces
- Core services and modules
- Data models
- API routes
- External integrations
- Authentication and authorization
- Storage and state management
- Logging and error handling

**Tier 3 — Workflow tracing**

Follow imports, calls, routes, events, and dependencies only for workflows that require documentation.

### Step 3: Extract components

Record purpose, inputs, outputs, dependencies, configuration, public interfaces, callers, external systems, failure modes, diagnostics, tests, and sources.

### Step 4: Trace workflows

Record actor, preconditions, trigger, processing sequence, branches, external calls, transformations, outputs, success criteria, failures, and recovery.

### Step 5: Ask unresolved questions

Ask only after analysis. Use batches of three to five questions. Explain why each answer matters and offer a proposed assumption when safe.

---

## Guided Build Mode — target workflow

### Preferred evidence order for Power Automate

1. Solution export
2. Non-solution flow export
3. Run-history CSV
4. Screenshots of trigger, actions, conditions, and settings
5. User description
6. Skill inference

Document connection and variable names, but never secret values.

### Adaptive interview groups

1. Purpose and audience
2. Trigger
3. Inputs and sources
4. Processing and decisions
5. Outputs
6. Connections and permissions
7. Failure handling
8. Ownership, environments, deployment, monitoring, and change control

The skill should fill what artifacts already establish and ask only unresolved, material questions.

---

## Developer / Builder guide requirements

Required sections:

1. Project overview
2. System context
3. Architecture
4. Workflow and data flow
5. Setup and configuration
6. Interfaces and contracts
7. Testing and validation
8. Deployment and release
9. Security
10. Monitoring and troubleshooting
11. Maintenance and change impact
12. Evidence, assumptions, conflicts, and unresolved questions

The document must be implementation-oriented, source-aware, and explicit about current maturity and known gaps.

---

## End-user guide requirements

Required sections:

1. What the tool does
2. Who should use it
3. Before you begin
4. Primary workflow
5. Expected results
6. Common tasks
7. Simplified troubleshooting
8. What users should not change
9. Getting help
10. Quick reference

The user guide is not a shortened developer guide. It must prioritize normal use, visible success states, safe recovery, and escalation. Administrative actions such as replacing connectors, changing credentials, deleting production records, or forcing reruns belong only in the developer/administrator guide.

---

## Validation gates

### Evidence validation

- Every architectural component exists in the evidence record.
- Every path, command, action, interface, and connection name is supported or explicitly labeled as an assumption.
- Inferences remain labeled.
- Conflicts remain visible.

### Cross-document validation

- Names match.
- User steps agree with technical workflows.
- Troubleshooting aligns with actual failure handling.
- User actions remain role-appropriate.
- Owners and escalation paths match.

### Security validation

- No secrets or production credentials
- No private keys or real `.env` values
- No unnecessary personal/customer data
- No unsafe production modification instructions

### Completeness validation

Both guides must cover purpose, audience, happy path, inputs, outputs, prerequisites, failure behavior, troubleshooting, ownership, known gaps, and source version.

---

## Planned repository structure

```text
project-documentation-builder/
├── SKILL.md
├── status.md
├── README.md
├── docs/
│   └── DOCUMENTATION_MAINTENANCE.md
├── modes/
│   ├── repository-analysis.md
│   ├── guided-build.md
│   ├── hybrid-analysis.md
│   └── refresh-documentation.md
├── references/
│   ├── evidence-model.md
│   ├── source-priority-rules.md
│   ├── clarification-question-bank.md
│   ├── documentation-quality-rubric.md
│   ├── developer-guide-requirements.md
│   ├── user-guide-requirements.md
│   └── platform-profiles/
│       ├── generic-low-code.md
│       └── power-automate.md
├── assets/
│   ├── developer-guide-template.md
│   ├── user-guide-template.md
│   ├── troubleshooting-matrix-template.md
│   ├── architecture-diagram-template.md
│   └── workflow-diagram-template.md
├── schemas/
│   ├── project-evidence.schema.json
│   ├── component.schema.json
│   ├── workflow.schema.json
│   └── documentation-manifest.schema.json
├── scripts/
│   ├── inventory_repository.py
│   ├── validate_evidence.py
│   ├── validate_source_references.py
│   ├── validate_document_consistency.py
│   ├── detect_sensitive_values.py
│   └── compare_documentation_versions.py
├── tests/
└── evals/
```

---

## Phase plan

| Phase | Name | State | Completion criteria |
|---|---|---:|---|
| 0 | Foundation and governance | `IN PROGRESS` | Handoff, README, documentation contract, branch, and phase rules are committed. |
| 1 | Skill scaffold | `NOT STARTED` | Valid `SKILL.md`, all mode files, output templates, platform profiles, and quality references exist. |
| 2 | Evidence layer | `NOT STARTED` | Evidence and manifest schemas exist; validation catches missing fields, invalid states, and unsupported confirmed facts. |
| 3 | Repository analysis MVP | `NOT STARTED` | Deterministic targeted inventory works, excludes noise, flags sensitive paths, and passes tests. |
| 4 | Guided-build MVP | `NOT STARTED` | Adaptive low-code intake and Power Automate profile can produce a complete workflow blueprint with visible unknowns. |
| 5 | Document generation | `NOT STARTED` | Both guides can be generated from one evidence record and pass cross-document checks. |
| 6 | Deterministic validation | `NOT STARTED` | Source-reference, consistency, and sensitive-value validators are implemented and tested. |
| 7 | Evaluation and hardening | `NOT STARTED` | Repository, misleading-docs, monorepo, Power Automate, description-only, hybrid, refresh, and security cases are evaluated. |

---

## Phase-by-phase implementation detail

### Phase 0 — Foundation and governance

Deliverables:

- Expanded `README.md`
- This `status.md`
- `docs/DOCUMENTATION_MAINTENANCE.md`
- Feature branch

Completion gate:

- A future developer can understand the product, phases, rules, and next action without reconstructing the prior conversation.

### Phase 1 — Skill scaffold

Deliverables:

- `SKILL.md`
- Four mode files
- Developer and user templates
- Diagram and troubleshooting templates
- Source-priority, question-bank, guide-requirement, and quality-rubric references
- Generic low-code and Power Automate profiles

Completion gate:

- The skill can route repository, guided-build, hybrid, and refresh requests and has explicit output contracts.

### Phase 2 — Evidence layer

Deliverables:

- Project evidence schema
- Component schema
- Workflow schema
- Documentation manifest schema
- Evidence validation script and tests

Completion gate:

- Invalid verification states, duplicate IDs, missing sources for confirmed facts, and incomplete source version records are rejected.

### Phase 3 — Repository analysis MVP

Deliverables:

- Deterministic repository inventory script
- Default exclusions
- File classification and priority
- Sensitive-path flags without reading or exposing values
- Tests using synthetic fixtures

Completion gate:

- The inventory is deterministic, excludes common generated directories, identifies orientation files, and passes tests without external dependencies.

### Phase 4 — Guided-build MVP

Deliverables:

- Workflow blueprint procedure
- Adaptive interview logic
- Power Automate artifact map
- Connection, permission, ownership, error-handling, and operational questions
- Description-only fallback

Completion gate:

- A Power Automate export and a description-only workflow can both be documented while unresolved facts stay explicit.

### Phase 5 — Document generation

Deliverables:

- Evidence-to-developer-guide workflow
- Evidence-to-user-guide workflow
- Architecture and workflow diagram rules
- Simplified troubleshooting generation
- Source metadata and assumptions section

Completion gate:

- Both documents describe the same system accurately for different audiences.

### Phase 6 — Deterministic validation

Deliverables:

- Source-reference validator
- Cross-document consistency validator
- Sensitive-value detector
- Documentation version comparison
- Tests and quality command

Completion gate:

- Validators reject nonexistent references, conflicting instructions, mismatched names, and secret-like content.

### Phase 7 — Evaluation and hardening

Initial evaluation cases:

1. Small Python repository
2. Repository with misleading README
3. Large monorepo
4. Power Automate solution export
5. Description-only automation
6. Hybrid software/workflow project
7. Security and secret-handling case
8. Documentation refresh case

Completion gate:

- Test prompts, expected outputs, assertions, qualitative review, and benchmark notes are stored and the skill performs materially better than an unstructured baseline.

---

## Documentation update rules

The full contract is in `docs/DOCUMENTATION_MAINTENANCE.md`. The rules below are mandatory:

1. Update `status.md` in the same commit as every phase change.
2. Update implementation and affected documentation together.
3. Do not mark a phase complete until its completion criteria and validation pass.
4. Record completed work, validation, decisions, limitations, and exact next actions.
5. Keep `README.md` limited to current capabilities; planned behavior belongs here.
6. Generate both guides from the same evidence record.
7. Preserve confirmed, inferred, unknown, and conflict states.
8. Separate current behavior from intended behavior.
9. Use synthetic values and never place secrets in documentation, tests, or examples.
10. Prefer deterministic validation wherever a claim can be checked programmatically.
11. Record source versions and change impact for refreshes.
12. Keep future-session pickup instructions accurate.

---

## Current decisions

- Build on a feature branch rather than the default branch.
- Use a clean implementation inspired by the source prototype rather than copying its code.
- Keep the runtime skill model-provider-independent; no direct Anthropic SDK dependency in the core skill.
- Keep deterministic helpers standard-library-first where practical.
- Treat the evidence record as the shared source for both documents.
- Ask clarification questions only after analyzing available evidence.
- Do not choose a repository license without the owner’s explicit decision.

---

## Known risks and unresolved decisions

- Exact packaging and distribution path for installing the skill in Claude has not yet been selected.
- License is not selected.
- Power Automate export formats may require more than one parser/profile because solution and non-solution packages differ.
- Large monorepos need scope controls and token-budget rules beyond the deterministic inventory.
- The eventual diagram format must balance portability with rendering support; Mermaid is the initial likely default but is not yet locked.
- Refresh-mode version comparison must work with both Git commits and low-code export versions.

---

## Validation record

No executable validation exists yet. Phase 0 validation is a manual handoff completeness review.

---

## Change log

### 2026-08-20 — Phase 0 started

- Created the feature branch.
- Added the full product handoff and phased implementation plan.
- Added mandatory documentation-maintenance rules.
- Expanded the repository README.

---

## Exact next actions

1. Complete and commit Phase 0.
2. Create `SKILL.md` with mode routing and evidence-first rules.
3. Add all four mode workflows.
4. Add developer and user guide templates.
5. Add low-code and Power Automate profiles.
6. Update this file to mark Phase 0 complete and Phase 1 in progress in the same commit as the Phase 1 scaffold.
