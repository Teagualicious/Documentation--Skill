# Repository Analysis Mode

Use this workflow for a GitHub repository, local repository, or uploaded source archive.

## Goal

Build an evidence-backed model of the selected project scope without reading every file indiscriminately, then create the developer and user guides from that model.

## 1. Resolve repository scope

Record:

- Repository or local path
- Branch, tag, or commit
- Monorepo versus single-project structure
- Requested application, package, service, or workflow scope
- Existing documentation locations
- Generated or vendor directories to exclude
- Whether source changes are authorized; default to read-only

When scope is ambiguous, perform enough orientation analysis to propose a sensible boundary before asking the user.

## 2. Build a deterministic inventory

Run `scripts/inventory_repository.py` when available and read `references/repository-inventory.md` for its output and safety rules. Store the result as `.project-guide/repository-inventory.json` when the working environment permits file creation.

The inventory should identify:

- Orientation documents
- Dependency manifests
- Build and deployment configuration
- Environment templates
- Entry points
- Source files
- Tests and fixtures
- API or interface definitions
- Data models and migrations
- Workflow definitions
- Sensitive paths that must not be read or reproduced

Do not include generated directories, dependency caches, build output, or version-control internals unless they are specifically relevant.

## 3. Analyze by priority tier

### Tier 1 — Orientation

Inspect first:

- README and existing guides
- Dependency manifests
- Build configuration
- Deployment workflows
- Environment templates with values redacted
- Top-level tree
- Entry points
- Test configuration

Produce a provisional project boundary, technologies list, and candidate workflows.

### Tier 2 — Architecture

Inspect only the files needed to resolve:

- Public interfaces
- Core services and modules
- Data models
- Routes, commands, jobs, or event handlers
- External integrations
- Authentication and authorization
- Storage and state
- Logging and error handling

### Tier 3 — Workflow tracing

Trace each material user or system workflow from trigger to output. Follow direct imports, calls, routes, events, and dependencies. Stop when the workflow reaches a documented external boundary.

## 4. Extract component records

For each material component, capture:

- Stable component ID
- Name and type
- Purpose
- Inputs and outputs
- Dependencies
- Configuration
- Public interfaces
- Primary callers or triggers
- External systems
- Failure modes
- Logging and diagnostics
- Tests
- Source references
- Verification and implementation states

Do not create component records for trivial files that do not help explain the system.

## 5. Trace workflow records

For each material workflow, capture:

- Actor
- Preconditions
- Trigger
- Ordered steps
- Decision branches
- Data transformations
- External calls
- State changes
- Outputs
- Success criteria
- Failure states
- Retry and recovery behavior
- Escalation conditions
- Source references

## 6. Compare implementation with existing documentation

Treat existing documentation as evidence, not as automatic truth.

Record conflicts such as:

- README command not present in scripts or manifests
- Documented directory or interface that does not exist
- Test behavior that differs from user instructions
- Deployment documentation that targets another environment
- Current code that implements an unfinished or deprecated path

Preserve both sides of a conflict and ask the owner only when resolution affects the final guides.

## 7. Ask targeted questions

Ask after analysis. Good questions resolve:

- Which of several execution paths is production
- Which application in a monorepo is in scope
- Who owns an operational task that code cannot identify
- Whether a code/document mismatch is a defect or outdated expectation
- Which user roles receive outputs or alerts

Avoid questions about programming language, directory purpose, commands, or dependencies when the repository already answers them.

## 8. Generate both guides

Use the shared evidence record and standard templates.

Developer guide emphasis:

- Architecture and dependencies
- Setup and configuration
- Interfaces and data contracts
- Testing, deployment, monitoring, and maintenance
- Source version and evidence limitations

User guide emphasis:

- Access and prerequisites
- Normal workflow
- Expected results
- Common tasks
- Safe troubleshooting
- Escalation information

## 9. Validate

When deterministic scripts are available, validate path references, evidence structure, document consistency, and sensitive-value handling.

Record any areas that were not analyzed because of scope, file size, unavailable dependencies, access restrictions, or unsupported binary formats.
