# Documentation Quality Rubric

Use this rubric before finalizing documentation. Score each category from 0 to 2.

- `0` — missing, unsupported, or unsafe
- `1` — partially complete or contains material uncertainty
- `2` — complete for the documented scope and supported by evidence

## Categories

### Scope and version

The guides identify the documented project, scope, source type, environment, and version or explain why an exact version is unavailable.

### Evidence integrity

Material claims are supported, and inferred, unknown, or conflicting claims remain labeled.

### Current versus intended behavior

Differences are visible and not silently blended.

### Architecture and workflow

Components, boundaries, triggers, ordered steps, decisions, data movement, outputs, and failure paths are understandable.

### Setup and permissions

Prerequisites, configuration names, access requirements, ownership, and environment differences are clear without exposing secrets.

### End-user usability

The user guide leads with the normal workflow, explains success, uses plain language, and avoids unnecessary internal detail.

### Troubleshooting safety

Recovery steps reflect actual behavior, avoid duplicate or destructive actions, and define escalation conditions.

### Operations and maintenance

Monitoring, support ownership, deployment, rollback, change impact, and known limitations are covered when relevant.

### Cross-document consistency

Names, steps, inputs, outputs, owners, and limitations agree across both guides.

### Security and privacy

No secret values or unnecessary personal/customer data appear.

## Completion threshold

Do not present the documentation as complete unless every category scores at least `1` and the total is at least `17/20`.

Any score of `0` in evidence integrity, troubleshooting safety, or security and privacy blocks completion.
