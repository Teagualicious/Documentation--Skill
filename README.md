# Project Documentation Builder Skill

An evidence-backed Claude skill for producing two synchronized forms of project documentation:

1. **Developer / Builder documentation** for maintainers, engineers, administrators, and future project owners.
2. **Simplified end-user documentation** for day-to-day use, safe troubleshooting, and escalation.

The skill is designed for conventional GitHub or local codebases, low-code and no-code builds such as Power Automate, and hybrid systems that combine software, workflows, data sources, and manual operations.

## Current status

This repository is under an explicitly phased build. The authoritative implementation plan, decisions, phase state, and future-session handoff are maintained in [`status.md`](status.md).

The documentation-update contract is maintained in [`docs/DOCUMENTATION_MAINTENANCE.md`](docs/DOCUMENTATION_MAINTENANCE.md). A phase is not complete unless its implementation and affected documentation are updated together.

## Operating modes in the current scaffold

- **Repository Analysis Mode** — inspect a GitHub repository, local repository, or uploaded source archive; analyze first, then ask only questions that cannot be answered from the codebase.
- **Guided Build Mode** — document Power Automate, Power Apps, SharePoint, Excel/VBA, Zapier, Make, and other low-code or process-heavy projects through exports, screenshots, diagrams, descriptions, and adaptive clarification.
- **Hybrid Mode** — document the boundaries between conventional code, low-code workflows, external systems, and human review steps.
- **Refresh Mode** — compare a previously documented source version with the current implementation and update only the affected documentation sections.

## Primary outputs

- `DEVELOPER_GUIDE.md`
- `USER_GUIDE.md`

Internal support artifacts are used to keep those documents accurate and synchronized:

- `.project-guide/evidence.json`
- `.project-guide/open-questions.md`
- `.project-guide/documentation-manifest.json`

## Build principles

- Analyze available evidence before asking the user questions.
- Separate current implementation from intended behavior.
- Mark claims as confirmed, inferred, unknown, or conflicting.
- Never invent paths, commands, owners, interfaces, or troubleshooting steps.
- Keep user troubleshooting safe and role-appropriate.
- Never reproduce secrets, credentials, tokens, connection strings, or unnecessary personal data.
- Keep `status.md` current in the same commit as each phase change.

## Repository map

The current scaffold follows this structure:

```text
.
├── SKILL.md
├── status.md
├── modes/
├── references/
├── assets/
├── schemas/
├── scripts/
├── tests/
├── evals/
└── docs/
```

See [`status.md`](status.md) for the complete handoff and implementation phases.

## Current implementation

Phases 1 through 3 provide a valid `SKILL.md`, four mode workflows, audience-specific templates, low-code platform guidance, a versioned evidence model, JSON schemas, semantic validation, and a deterministic repository inventory. The inventory classifies files by analysis priority, excludes common generated/vendor directories, identifies likely entry points, and flags sensitive paths without reading or emitting their contents. Guided low-code intake and export parsing begin in Phase 4 and must not be treated as complete until `status.md` marks that phase complete.

## Validation

```bash
python -m unittest discover -s tests -v
python scripts/validate_evidence.py tests/fixtures/evidence_valid.json
python scripts/validate_evidence.py tests/fixtures/manifest_valid.json --kind manifest
python scripts/inventory_repository.py . \
  --output /tmp/documentation-skill-inventory.json
```

## License

No license has been selected for this repository yet. Do not assume that the source is licensed for redistribution until the owner adds an explicit license.
