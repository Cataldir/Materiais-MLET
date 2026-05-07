# Repository Readiness Audit

> Reviewed: 2026-05-06. Scope: public `Materiais-MLET` repository readiness as reusable teaching material, not private course operations.

## Executive Finding

The repository is structurally usable and the main public live index is internally consistent. It is not yet content-complete across all cohorts or all phases. The strongest coverage is MLET6. Later cohorts have schedules in the private operations repository, but reusable public bundles are partial or absent.

Readiness therefore splits into two tracks:

1. repository mechanics and navigation are in good shape;
2. teaching-content completeness, challenge coverage, notebook hygiene, and cohort publication still need work.

## Audit Snapshot

| Area | Evidence | Readiness |
| --- | --- | --- |
| Live index integrity | Cross-cohort index moved to `docs/live-session-index.md`; material links now point to phase-local folders. | Ready |
| Live folder coverage | Live material folders now live under phase-local `lives/` folders or study-group-local `lives/` folders. | Ready structurally |
| Cohort documentation | Coverage pages exist for MLET6 through MLET13. | Ready as documentation |
| Cohort public material | MLET6 has 35 entries; MLET7 has 25; MLET8 has 19; MLET9 has 7; MLET10-MLET13 have 0. | Not content-complete |
| Discipline structure | F01-F05 canonical phase folders have all immediate discipline READMEs. | Ready structurally |
| Challenge coverage | 6 `desafio.md` files: 1 in F02, 5 in F03, none in F01/F04/F05. | Incomplete |
| Notebook hygiene | Notebook structural validation now passes across 44 notebooks and 155 code cells; 7 notebooks still contain outputs/execution counts. | Needs cleanup |
| Data/model artifact size | No files over 5 MB found in the public tree; one notebook is close at roughly 4.8 MB. | Low immediate size risk |
| Dependency reproducibility | Constraints exist for `fase01` through `fase05`; root dev constraints and Makefile shortcuts were removed from the student-facing tree. | Ready structurally |
| Validation surface | Repository tests, tool scripts, workflow automation, and validation shortcut files were removed from the student-facing tree. | Removed from public student surface |
| Public/private boundary | No obvious exposed support-ticket or email ledger content found in public materials; keep operations evidence private. | Good, keep monitoring |

## Phase Inventory

| Phase path | Discipline dirs | Discipline READMEs missing | Challenges | Notebooks | Python files | Total files | Finding |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `fase-01-produtizacao-de-modelos` | 5 | 0 | 0 | 4 | 34 | 63 | Discipline structure is present; challenge coverage is missing. |
| `fase-02-containers-e-ambientes-reprodutiveis` | 4 | 0 | 1 | 2 | 27 | 74 | Discipline structure is present; challenge coverage is partial. |
| `fase-03-cloud-e-mlops` | 6 | 0 | 5 | 4 | 24 | 77 | Best challenge coverage; check whether one discipline intentionally has no challenge. |
| `fase-04-monitoramento-e-governanca` | 6 | 0 | 0 | 16 | 44 | 121 | Strong executable asset count; challenge coverage is missing. |
| `fase-04-validacao-de-dados` | 0 | 0 | 0 | 8 | 0 | 23 | Separate legacy/overlay tree; classify or migrate into canonical phase structure. |
| `fase-05-deploy-avancado-de-ia-generativa` | 5 | 0 | 0 | 10 | 26 | 64 | Discipline structure is present; challenge coverage is missing. |

## Cohort Coverage

| Cohort | Public entries | Public phases | Content readiness |
| --- | ---: | --- | --- |
| MLET6 | 35 | F01, F02, F03, F04, F05 | Public content baseline ready. |
| MLET7 | 25 | F01, F02, F03, F04 | Partial; phase 04 completion and phase 05 need publication/index review. |
| MLET8 | 19 | F01, F02, F03 | Partial; phase 03 completion, phase 04, and phase 05 need publication/index review. |
| MLET9 | 7 | F01 | Partial; phase 02 onward not publicly indexed yet. |
| MLET10 | 0 | None | No public indexed reusable material yet. |
| MLET11 | 0 | None | No public indexed reusable material yet. |
| MLET12 | 0 | None | No public indexed reusable material yet. |
| MLET13 | 0 | None | No public indexed reusable material yet. |

## Existing Challenge Files

| Path | Phase |
| --- | --- |
| `fase-02-containers-e-ambientes-reprodutiveis/02-gerenciamento-dependencias/desafio.md` | F02 |
| `fase-03-cloud-e-mlops/02-integracao-cicd/desafio.md` | F03 |
| `fase-03-cloud-e-mlops/03-pipeline-treino-deploy-automatico/desafio.md` | F03 |
| `fase-03-cloud-e-mlops/04-monitoracao-performance/desafio.md` | F03 |
| `fase-03-cloud-e-mlops/05-servicos-de-monitoracao/desafio.md` | F03 |
| `fase-03-cloud-e-mlops/06-latencia-performance/desafio.md` | F03 |

## Notebook Cleanup Targets

The following notebooks still contain outputs or execution counts. They should be reviewed before treating notebook hygiene as complete.

| Notebook | Finding |
| --- | --- |
| `fase-04-validacao-de-dados/aula_01/fundamentos_validacao.ipynb` | Saved outputs/execution counts present. |
| `fase-04-validacao-de-dados/aula_02/dimensoes_qualidade.ipynb` | Saved outputs/execution counts present. |
| `fase-04-validacao-de-dados/aula_03/deduplicacao_e_imputacao.ipynb` | Saved outputs/execution counts present. |
| `fase-04-validacao-de-dados/aula_04/monitoramento_drift.ipynb` | Saved outputs/execution counts present; large notebook around 4.8 MB. |
| `fase-04-validacao-de-dados/aula_05/validacao_schema_contratos_dados.ipynb` | Saved outputs/execution counts present. |
| `fase-04-validacao-de-dados/aula_06/deteccao_outliers_anomalias.ipynb` | Saved outputs/execution counts present. |
| `fase-04-validacao-de-dados/aula_07/frameworks_qualidade_dados.ipynb` | Saved outputs/execution counts present. |

Notebook structural validation was corrected for two Python parsing blockers caused by notebook magic lines in `aula_02/dimensoes_qualidade.ipynb` and `aula_04/monitoramento_drift.ipynb`. The current structural check passes cleanly across 44 notebooks and 155 code cells.

## Current Cleanup Results

| Cleanup area | Result |
| --- | --- |
| `.github/` | Removed from the current working tree. History purge still requires an explicit history-rewrite operation. |
| `tests/` and `tools/` | Removed from the current working tree. |
| Root validation shortcuts | `Makefile`, `.pre-commit-config.yaml`, `.markdownlint-cli2.jsonc`, and `constraints/dev.txt` removed from the current working tree. |
| Root navigation docs | Root README reduced to a short phase-first entry point; navigation, contribution notes, and changelog now live under `docs/`. |
| Top-level `lives/` and `grupos-de-estudo/` | Removed from the current working tree after moving contents into phase-local paths. |

## Characteristics Still To Review

### Public Index Integrity

The main live index now lives in `docs/live-session-index.md`. Keep it as a lightweight cross-cohort index while the actual material stays under phase-local folders.

Acceptance criteria:

1. every `docs/live-session-index.md` material link points to an existing phase-local folder;
2. every phase-local live material folder is linked from the index;
3. each linked folder has a useful README and clear execution path.

### Discipline Completeness

The phase and discipline skeleton is present, but completeness should be checked at the discipline level, not only by directory count.

Acceptance criteria:

1. each discipline README explains purpose, learner outcomes, use path, references, and executable entry points;
2. every lesson folder has enough local context to run or inspect the material;
3. references are current and separated from private governance.

### Challenge Coverage

Challenge material is the largest visible gap. F01, F04, and F05 currently have no `desafio.md` files in canonical phase folders.

Acceptance criteria:

1. each phase has a public challenge or an explicit note explaining why the challenge belongs elsewhere;
2. each challenge defines scenario, inputs, deliverables, constraints, and success criteria;
3. challenge files do not expose private student data, private company data, or internal operations notes.

### Executability

Executable assets should be reviewable by students without repository-level test harnesses or hidden maintenance scripts.

Acceptance criteria:

1. each lesson README explains what can be run directly;
2. notebooks run top-to-bottom or are clearly marked as static/reference notebooks;
3. runnable commands live near the lesson they support, not in a root shortcut layer.

### Dependency Reproducibility

The per-phase constraints exist. The next review should verify that each constraint file still matches the imported notebooks and scripts.

Acceptance criteria:

1. `constraints/fase01.txt` through `constraints/fase05.txt` match phase optional dependencies;
2. phase dependency notes avoid root-level shortcut workflows;
3. heavy optional dependencies are isolated to the phase that needs them.

### Data, Privacy, And Licensing

No large public data/model files were found in the quick size scan, but source and license clarity still needs a content-level review.

Acceptance criteria:

1. every dataset has a source and allowed educational use;
2. no student identifiers, tickets, grades, emails, or RM numbers are present;
3. generated outputs, caches, checkpoints, and model binaries are excluded unless intentionally curated.

### Public/Private Boundary

The quick scan did not show a public support-ticket ledger, but this should remain a release gate.

Acceptance criteria:

1. public docs describe material, not professor follow-up;
2. private operations stay in `mlet`;
3. cohort pages report public material readiness, not internal escalation status.

## Recommended Next Work

1. Clean or classify `fase-04-validacao-de-dados` so it is either migrated into `fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade` or documented as a legacy overlay.
2. Add missing challenge coverage for F01, F04, and F05, and decide whether F03/01 intentionally has no `desafio.md`.
3. Clear outputs and execution counts from the seven dirty notebooks, especially the 4.8 MB drift notebook.
4. Review MLET7-MLET9 missing public bundles against the private schedule and publish only reusable approved material.
5. Treat MLET10-MLET13 pages as future publication checklists, not as proof that public material exists.
