# Copilot Instructions

<!-- managed:team-mapping-delegation:start -->
## Delegation Bootstrap
- Before delegating, always read `.github/instructions/team-mapping.instructions.md`.
- Use `.github/agents/data/team-mapping.md` as the canonical delegation registry.
- Delegate only to agents that exist under `.github/agents/` (including subdirectories) in the current workspace.
- Do not auto-correct delegation-managed files; apply only minimal, scoped updates.
- Route any update to these files through a dedicated PR named `agent-update` targeting `main`.
- Store temporary files only under `.tmp/`, remove them after related PRs complete, and never version them.
- Write UI/UX text, documentation, and related content in en-US.
<!-- managed:team-mapping-delegation:end -->
