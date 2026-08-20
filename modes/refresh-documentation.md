# Refresh Documentation Mode

Use this mode when previous guides, an evidence record, a documentation manifest, or an earlier source version exists.

## Goal

Update only the documentation affected by implementation or workflow changes while preserving traceability and cross-document consistency.

## 1. Establish comparison points

Record:

- Previous source locator and revision
- Current source locator and revision
- Previous documentation generation date
- Previous schema version
- Requested refresh scope

If an exact prior revision is unavailable, state that the comparison is partial.

## 2. Identify changes

For repositories, compare commits, branches, tags, or file inventories.

For low-code projects, compare export packages, action lists, connection references, environment variables, screenshots, run behavior, or approved requirements.

Classify each change as:

- Component added, removed, or renamed
- Interface or data contract changed
- User workflow changed
- Configuration or permission changed
- Deployment or environment changed
- Failure handling changed
- Documentation-only correction

## 3. Map change impact

Link each change to affected:

- Evidence facts
- Components
- Workflows
- Developer-guide sections
- User-guide sections
- Troubleshooting entries
- Diagrams
- Open questions

Re-analyze direct dependencies when a boundary or interface changes.

## 4. Preserve history and verification state

Do not overwrite a prior confirmed fact without recording the replacement or deprecation.

Update source references and mark obsolete facts as `deprecated` when they remain useful for historical context. Remove stale claims from current instructions.

## 5. Regenerate affected sections

Update both guides together even when only one audience appears affected. Perform a cross-document review to confirm that names, steps, outputs, owners, and failure guidance remain synchronized.

## 6. Record the refresh

Update `.project-guide/documentation-manifest.json` with:

- New source revision
- Changed components and workflows
- Updated document sections
- Validation performed
- Remaining unknowns
- Concise change summary

## 7. Validate

Run source-reference, evidence, consistency, and sensitive-value checks when available.

Do not call the documentation fully refreshed when the source comparison was incomplete or required artifacts were unavailable.
