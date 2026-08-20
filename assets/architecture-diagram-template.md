# Architecture Diagram Template

Use a portable text diagram or Mermaid when rendering support is appropriate.

```mermaid
flowchart LR
    U[User or upstream actor] --> A[Entry point]
    A --> B[Core component]
    B --> D[(Data store)]
    B --> X[External system]
    B --> W[Workflow or job]
    W --> H[Human review]
    H --> O[Output or notification]
```

## Rules

- Show only material components.
- Label boundaries and external systems.
- Show direction of data or control flow.
- Do not include secret values or sensitive record examples.
- Mark inferred components or connections in accompanying text.
