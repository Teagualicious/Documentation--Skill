# Source Priority Rules

Use these rules when evidence sources disagree or vary in authority.

## Current implementation

Use this default priority:

1. Executable code or exported workflow definitions
2. Tests and observed run results
3. Deployment, environment, and configuration files
4. Existing documentation
5. Comments, labels, and naming conventions
6. Model inference

Higher priority does not automatically mean correct in every context. A test fixture may describe a non-production path, and a workflow export may come from a development environment. Record environment and version before resolving a conflict.

## Intended behavior

Use this default priority:

1. Explicit project-owner or stakeholder answer
2. Approved requirements, acceptance criteria, or process specification
3. Existing documentation
4. Model inference

## Conflict handling

When credible sources disagree:

1. Record each source and its version.
2. State the specific disagreement.
3. Identify whether the sources describe different environments, versions, roles, or scopes.
4. Mark the claim `conflict` until resolved.
5. Ask the owner only when the resolution materially changes a guide.
6. Preserve current and intended behavior separately when both are relevant.

Never choose the most convenient source merely to complete a section.
