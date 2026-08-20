# Workflow Diagram Template

```mermaid
flowchart TD
    S([Start]) --> T[Trigger]
    T --> V{Inputs valid?}
    V -- No --> E[Return validation guidance]
    V -- Yes --> P[Process or transform]
    P --> X[External action]
    X --> R{Succeeded?}
    R -- Yes --> O[Store or deliver output]
    R -- No --> F[Record failure and notify owner]
    O --> D([Done])
    F --> M[Manual recovery or escalation]
```

## Rules

- Use exact action names only when confirmed.
- Include material branches, loops, approvals, and external actions.
- Show failure and recovery paths, not only the happy path.
- Identify where retries may create duplicates.
