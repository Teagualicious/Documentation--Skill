# Repository Inventory

Use `scripts/inventory_repository.py` before targeted repository analysis when a local checkout or extracted source archive is available.

## Purpose

The script creates a deterministic, metadata-first inventory. It identifies orientation files and likely entry points while avoiding unbounded content ingestion.

It never emits file contents. Sensitive paths are detected from names and directory segments and are not opened.

## Run

```bash
python scripts/inventory_repository.py /path/to/project \
  --output .project-guide/repository-inventory.json
```

Useful options:

```bash
--max-file-bytes 2000000
--max-files 50000
--exclude generated
--exclude 'examples/vendor-*'
--fail-on-sensitive
```

## Priority tiers

- **Priority 1** — orientation documents, manifests, deployment/infrastructure, project configuration, and likely entry points.
- **Priority 2** — source, tests, and secondary documentation.
- **Priority 3** — data, assets, and unknown files that should be opened only when a workflow requires them.

Priority is a reading order, not a statement of code importance.

## Sensitive-path behavior

The inventory records the path, sensitivity reason, and metadata but does not open the file. Examples include real `.env` files, private keys, credential stores, and files inside clearly sensitive directories.

Environment templates such as `.env.example` remain eligible because they should contain names and synthetic placeholders rather than live values. Verify that assumption before quoting examples.

## Output use

Start with `orientation.read_first`, then follow only the files needed to establish architecture and material workflows. Use `analysis_limitations` in the final guides when exclusions, file limits, oversized files, binary files, or inaccessible paths reduce coverage.

The full output contract is in `schemas/repository-inventory.schema.json`.
