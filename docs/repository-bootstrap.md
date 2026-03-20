# Materiais-MLET Repository Bootstrap

## Current Bootstrap Intent

This local clone is being prepared as the executable teaching-materials repository for MLET.

Working branch model:

1. `canonica` is the editorial branch for curated baseline materials.
2. `main` is the downstream aggregation branch for approved enrichments and approved solution-side overlays.

## Release-0 Scope

Release 0 is limited to bootstrap artifacts and branch preparation.

Included now:

1. editorial branch creation;
2. cross-repo architecture and migration planning documents in the governance repository;
3. first-pass legacy migration ledger;
4. phase-05 datathon business-case template.

Explicitly excluded now:

1. mass migration of legacy code;
2. repository-wide automation rollout;
3. large README rewrites across all phases;
4. direct publication of raw legacy material.

## Cross-Repo Relationship

| Repository | Responsibility |
| --- | --- |
| `mlet` | governance, intake, provenance, migration decisions, business-case framing |
| `Materiais-MLET` | executable notebooks, scripts, overlays, and curated teaching bundles |

## Immediate Next Steps

1. create row-level manifests for the first migration batch;
2. normalize one high-value branch family into a discipline-owned canonical notebook/script path;
3. promote only after the canonical baseline exists in `canonica`;
4. merge downstream into `main` only when approved enrichments exist.
