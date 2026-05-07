# Materiais-MLET Repository Structure

## Public Intent

`Materiais-MLET` is the public student-reference repository for the Machine Learning Engineering program. It should make reusable phase, discipline, live-session, study-group, notebook, script, and challenge material easy to find without exposing private operations context or repository-maintenance scaffolding.

The repository is not scoped to a single cohort. Cohort labels can appear as provenance for dated sessions, but documentation should lead with reusable curriculum structure instead of a local cohort status narrative.

## Top-Level Layout

| Path | Purpose |
| --- | --- |
| `README.md` | Public entry point and phase table. |
| `CONTRIBUTING.md` | Rules for adding student-facing material safely. |
| `CHANGELOG.md` | Editorial history for the public repository. |
| `constraints/` | Phase-specific dependency baselines. |
| `docs/` | Navigation, coverage, and public readiness indexes. |
| `fase-*` | Curriculum phases, disciplines, lessons, lives, and study-group material. |

## Public/Private Boundary

| Repository | Responsibility | Examples |
| --- | --- | --- |
| Non-public course operations | Governance, approvals, scheduling context, evidence, and operational decisions. | Internal schedules, publication readiness evidence, and assignments. |
| `Materiais-MLET` | Public student reference material and student/professor navigation. | Phase READMEs, discipline READMEs, notebooks, scripts, challenges, phase-local live bundles, phase-local study-group bundles. |

## Documentation Rules

1. Use cohort labels only as provenance for dated sessions or cohort-specific evidence.
2. Prefer phase and discipline structure for reusable material navigation.
3. Keep private operations details out of public docs.
4. Avoid importing raw legacy folders when a smaller curated artifact is enough.
5. When coverage differs by cohort, document only the public material coverage gap.
6. Keep repository automation, tests, tools, agents, instructions, prompts, and workflow scaffolding out of this student-facing repository.

## Current Coverage Review

The first cross-cohort documentation review starts with MLET6 because its public live and study-group material is indexed across all five phases. Coverage pages now exist for MLET6 through MLET13 so later publication gaps are explicit instead of hidden behind a single-cohort delivery note.

See [`delivery-status.md`](delivery-status.md) for the reviewed coverage model and [`repository-readiness-audit.md`](repository-readiness-audit.md) for repository-wide content, execution, and publication gaps.

## Immediate Next Steps

1. Fill MLET7-MLET9 partial coverage only when reusable public material is available or approved.
2. Use MLET10-MLET13 pages as publication checklists when those cohorts start generating reusable material.
3. Resolve the readiness gaps listed in [`repository-readiness-audit.md`](repository-readiness-audit.md), starting with challenge coverage, notebook hygiene, and the remaining legacy `fase-04-validacao-de-dados` overlay.
4. Keep cohort pages focused on public material readiness.
5. Promote only curated reusable material into public phase and discipline paths.
