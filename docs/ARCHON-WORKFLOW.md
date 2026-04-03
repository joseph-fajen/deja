# Archon Workflow Guide for Déjà

**Last Updated**: 2026-04-02

This document explains how to work with Archon CLI and Web UI for Déjà development, including a decision framework for choosing the optimal workflow.

---

## Workflow Selection Guide

Déjà has access to **two sets of workflows**:
1. **Déjà-specific** (`deja-*`) — Custom workflows in `.archon/workflows/` optimized for this project
2. **Archon defaults** (`archon-*`) — General-purpose workflows loaded via `loadDefaultWorkflows: true`

### Decision Matrix

| Task Type | Recommended Workflow | Rationale |
|-----------|---------------------|-----------|
| **Fix GitHub issue** | `archon-fix-github-issue` | Full pipeline: investigate → fix → PR → review → auto-fix. Posts updates to GitHub. |
| **Add test coverage** | `deja-add-tests` | Purpose-built for test-only additions. Knows Déjà patterns. |
| **Small bug fix** (no issue) | `deja-implement` | Faster, enforces zero-dep philosophy. |
| **New feature** (well-defined) | `deja-implement` | Knows Déjà patterns, enforces conventions. |
| **New feature** (needs exploration) | `archon-piv-loop` | Interactive Plan-Implement-Validate with human-in-the-loop. |
| **PR review** | `archon-smart-pr-review` | Multi-agent review, adapts to complexity, auto-fixes. |
| **Safe refactoring** | `archon-refactor-safely` | Behavior preservation with hooks, read-only verification. |
| **Documentation only** | Manual or `deja-implement` | Trivial changes don't need full workflow. |
| **Build app from scratch** | `archon-adversarial-dev` | GAN-inspired adversarial development. |

### When to Use Déjà-Specific Workflows

**Use `deja-implement`** when:
- Task is well-defined (clear scope, known files)
- Enforcing zero-dependency philosophy matters
- You want faster execution (fewer steps)
- No GitHub issue to link
- You'll create PR manually or use `deja-create-pr`

**Use `deja-add-tests`** when:
- Adding tests only (no production code changes)
- Want test-focused analysis and generation

**Pros of Déjà workflows:**
- Enforces zero-dependency philosophy in prompts
- Knows the `(summary_line, data_dict)` return convention
- Faster execution (5 steps vs 8-11)
- Lower token cost

**Cons:**
- No automated code review
- No GitHub issue integration
- Manual PR creation

### When to Use Archon Default Workflows

**Use `archon-fix-github-issue`** when:
- Fixing a tracked GitHub issue
- Want end-to-end automation (issue → PR)
- Want automated code review + auto-fix
- Want updates posted to GitHub

**Use `archon-piv-loop`** when:
- Feature needs exploration before implementation
- Want human-in-the-loop at each phase
- Building something complex or ambiguous
- Want iterative plan refinement

**Use `archon-smart-pr-review`** when:
- PR exists and needs review
- Want multi-agent parallel review
- Want automatic CRITICAL/HIGH fixes

**Use `archon-refactor-safely`** when:
- Splitting large files
- Moving code between modules
- Need behavior preservation verification
- Want hook-enforced validation after every edit

**Pros of Archon workflows:**
- Full GitHub integration (posts to issues/PRs)
- Multi-agent code review catches more issues
- Auto-fixes review findings
- DAG-based parallel execution
- Syncs with main before review

**Cons:**
- Slower (more steps, more agents)
- Higher token cost
- Generic prompts (doesn't know Déjà-specific patterns)
- May suggest patterns that violate Déjà's philosophy

### Quick Decision Flowchart

```
Is there a GitHub issue?
├── YES → archon-fix-github-issue
└── NO
    ├── Is it test-only?
    │   └── YES → deja-add-tests
    └── NO
        ├── Is scope clear and well-defined?
        │   └── YES → deja-implement
        └── NO
            └── archon-piv-loop (interactive exploration)
```

---

## Architecture Overview

Déjà is a pure Python CLI skill with no runtime server. Development uses Archon for workflow automation:

```
┌─────────────────────────────────────────────────────────┐
│                    Archon Web UI                        │
│              (Vite dev server on port 5173)             │
│         http://localhost:5173                           │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTP/SSE
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Archon Server                         │
│              (Hono API on port 3090)                    │
│         Stores data in ~/.archon/archon.db              │
└──────────────────────────┬──────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌────────┐  ┌──────────┐  ┌────────┐
         │  CLI   │  │ Worktree │  │ Claude │
         └────────┘  └──────────┘  │  Code  │
                                   └────────┘
```

**Port Summary:**
| Service | Port | URL |
|---------|------|-----|
| Archon API | 3090 | http://localhost:3090 |
| Archon Web UI | 5173 | http://localhost:5173 |

**Key insight**: Déjà has no server of its own. You only need Archon services when you want workflow monitoring via Web UI.

---

## Two Modes of Operation

### Mode 1: CLI Only (Recommended for Quick Work)

Run workflows directly without any server:
```bash
archon workflow run deja-implement --branch feat/fuzzy-match "Add fuzzy matching option"
```

The CLI:
1. Creates an isolated worktree in `~/.archon/worktrees/`
2. Spawns Claude Code to execute workflow steps
3. Writes run data to `~/.archon/archon.db`
4. Streams output to terminal

**Web UI is NOT required.** The workflow runs fine without it.

### Mode 2: CLI + Web UI (Full Visibility)

To monitor workflows in the Web UI:
1. Start the Archon server (serves API on port 3090)
2. Start the Web UI (Vite dev server on port 5173)
3. Both CLI runs and Web UI interactions appear in the dashboard

---

## Starting Archon Services

### For CLI-Only Work (No Setup Needed)

Just run workflows directly:
```bash
cd ~/git/deja
archon workflow run deja-implement --branch feat/my-feature "description"
```

### For Web UI Monitoring

**Terminal 1** — Archon server + Web UI:
```bash
cd ~/git/remote-coding-agent
PORT=3090 bun run dev
# → API server: http://localhost:3090
# → Web UI: http://localhost:5173
```

**Terminal 2** — Run workflows:
```bash
cd ~/git/deja
archon workflow run deja-implement --branch feat/my-feature "description"
```

**Browser**: http://localhost:5173 — Archon workflow monitoring

---

## Available Workflows

### `deja-implement` — Feature Implementation

**Use for**: Implementing features from ROADMAP.md or PRDs

```bash
archon workflow run deja-implement --branch feat/fuzzy-match "Add --fuzzy flag for search"
```

**Steps executed:**
1. `deja-plan` — Read context, create implementation plan
2. `deja-code` — Implement following the plan
3. `deja-test` — Add pytest tests if applicable
4. `deja-validate` — Syntax check, functionality test, run tests
5. `deja-commit` — Create conventional commit

**Produces**: Implementation + tests + commit ready for PR

### `deja-validate` — Validation Only

**Use for**: Before creating a PR, after manual changes

```bash
archon workflow run deja-validate --no-worktree
```

**Checks:**
- Python syntax compilation
- Basic CLI functionality (`./deja --help`, `./deja --limit 3`)
- Pytest test suite

### `deja-create-pr` — Pull Request Creation

**Use for**: When feature is complete and tested

```bash
archon workflow run deja-create-pr "Add fuzzy matching for search"
```

**Produces**: GitHub PR to upstream

---

## Workflow Guidelines

### Code Style (enforced by `deja-code`)
- Pure Python, **no external dependencies**
- Type hints on function signatures
- Docstrings on public functions
- Follow existing patterns in `lib/`

### Key Patterns
- Commands return `(summary_line, data_dict)` tuples
- Use `ensure_cache_fresh()` before accessing cache
- Use `omit_empty()` for JSON output cleanup
- Constants at module level, not magic numbers

### Commit Style (enforced by `deja-commit`)
- `feat:` for new features
- `fix:` for bug fixes
- `test:` for test additions
- `refactor:` for refactoring
- `docs:` for documentation

---

## Troubleshooting

### Git Remote Configuration (Critical for `gh` CLI)

Archon workflows use the `gh` CLI for GitHub operations. The `gh` CLI determines which repository to use by looking at the git remote named `origin`. **If `origin` points to a repo you don't own, workflows will fail.**

**Required configuration for fork workflows:**

| Remote | Should Point To | Purpose |
|--------|-----------------|---------|
| `origin` | Your fork (`joseph-fajen/deja`) | Push access, issues, PRs |
| `upstream` | Original repo (`kateleext/deja`) | Sync with upstream |

**Check your configuration:**
```bash
git remote -v
# Should show:
# origin    https://github.com/joseph-fajen/deja.git (fetch/push)
# upstream  https://github.com/kateleext/deja.git (fetch/push)
```

**Fix if misconfigured:**
```bash
# If origin points to upstream (common when you clone upstream first):
git remote rename origin upstream
git remote rename fork origin

# Or if you need to add remotes from scratch:
git remote set-url origin https://github.com/joseph-fajen/deja.git
git remote add upstream https://github.com/kateleext/deja.git
```

**Why this matters:**
- `gh issue view 2` → looks for issue #2 in `origin`'s repo
- `git push origin HEAD` → pushes to `origin`
- `gh pr create` → creates PR in `origin`'s repo

If `origin` points to a repo where you don't have push access or where the issues don't exist, Archon workflows will fail at the `fetch-issue` or `git push` steps.

**Note:** Git worktrees share remote configuration with the main repo. Once fixed in `~/git/deja`, all future Archon worktrees will inherit the correct configuration.

---

### Workflows Not Appearing in Web UI

| Issue | Check | Fix |
|-------|-------|-----|
| Web UI won't connect | Is server running on :3090? | `PORT=3090 bun run dev:server` from Archon repo |
| Workflows not visible | Is project registered? | Click **+** in Web UI sidebar, add `/Users/josephfajen/git/deja` |
| Stale data | Server restarted? | Refresh browser, check project filter |

### Worktree Issues

```bash
# List active worktrees
archon isolation list

# Clean up merged worktrees
archon isolation cleanup --merged

# Check workflow status
archon workflow status
```

### Validation Failures

```bash
# Run validation manually
python3 -m py_compile deja
python3 -m py_compile lib/*.py lib/commands/*.py
./deja --help
pytest tests/ -v
```

---

## File Locations

| Item | Path |
|------|------|
| Archon repo | `~/git/remote-coding-agent` |
| CLI binary | `~/.bun/bin/archon` → symlinked to repo |
| Global config | `~/.archon/config.yaml` |
| Database | `~/.archon/archon.db` |
| Worktrees | `~/.archon/worktrees/` |
| **Déjà project config** | `~/git/deja/.archon/config.yaml` |
| **Déjà workflows** | `~/git/deja/.archon/workflows/` |
| **Déjà commands** | `~/git/deja/.archon/commands/` |

---

## Quick Reference

### Run a Feature Implementation
```bash
cd ~/git/deja
archon workflow run deja-implement --branch feat/NAME "description"
```

### Validate Current State
```bash
cd ~/git/deja
archon workflow run deja-validate --no-worktree
```

### Create PR After Completion
```bash
cd ~/git/deja
archon workflow run deja-create-pr "PR title"
```

### Monitor in Web UI
```bash
# Terminal 1
cd ~/git/remote-coding-agent && PORT=3090 bun run dev

# Terminal 2
cd ~/git/deja && archon workflow run ...

# Browser: http://localhost:5173
```

---

## Current Task Backlog

From ROADMAP.md, prioritized for Archon workflows:

**Zero-dep, high-value:**
1. Fuzzy Matching (#6) — `archon workflow run deja-implement --branch feat/fuzzy-match "Pure Python Levenshtein fuzzy matching"`
2. Cache First-Match (#3) — `archon workflow run deja-implement --branch perf/cache-first-match "Cache match locations during indexing"`
3. Configurable Truncation (#9) — `archon workflow run deja-implement --branch feat/config-truncation "Make TRUNCATE_LENGTH configurable"`

**Polish (GitHub issues):**
- Issue #2: `=note` missing text fallthrough
- Issue #3: CLI exit code 0 on failure ✅ DONE (PR #9)
- Issue #4: Confusing error for empty sessions
- Issue #5-8: Various minor improvements

---

## Archon Default Workflows Reference

These workflows are available in any project with `loadDefaultWorkflows: true`.

### Issue & Bug Workflows

| Workflow | Use Case | Key Features |
|----------|----------|--------------|
| `archon-fix-github-issue` | Fix a GitHub issue end-to-end | Investigate → fix → PR → review → auto-fix. Posts to GitHub. |
| `archon-issue-review-full` | Comprehensive fix + review | Full pipeline with 5 parallel review agents. |
| `archon-create-issue` | Report a bug as GitHub issue | Auto-reproduces issue, captures evidence, creates issue. |

### Feature Development Workflows

| Workflow | Use Case | Key Features |
|----------|----------|--------------|
| `archon-piv-loop` | Interactive Plan-Implement-Validate | Human-in-the-loop at each phase. Iterative exploration → plan → implement → validate. |
| `archon-idea-to-pr` | End-to-end from idea | Plan → setup → confirm → implement → validate → PR → review → fix → summary. |
| `archon-feature-development` | Implement from existing plan | For when plan already exists. Implement → PR. |
| `archon-plan-to-pr` | Execute a plan file | Takes path to `.plan.md`, executes it. |

### Code Review Workflows

| Workflow | Use Case | Key Features |
|----------|----------|--------------|
| `archon-smart-pr-review` | Efficient PR review | Classifies complexity, runs only relevant agents, auto-fixes. |
| `archon-comprehensive-pr-review` | Full PR review | All 5 agents in parallel, synthesize, auto-fix. |
| `archon-validate-pr` | Validate PR readiness | Type-check, lint, tests, format. |

### Refactoring & Architecture

| Workflow | Use Case | Key Features |
|----------|----------|--------------|
| `archon-refactor-safely` | Safe code refactoring | Behavior preservation, hooks enforce type-check after every edit, read-only verification. |
| `archon-architect` | Architecture improvement | Complexity reduction, codebase health sweeps. |
| `archon-resolve-conflicts` | Merge conflict resolution | Resolves conflicts, validates, commits. |

### Special Purpose

| Workflow | Use Case | Key Features |
|----------|----------|--------------|
| `archon-adversarial-dev` | Build app from scratch | GAN-inspired: Planner → Generator ↔ Evaluator loop. |
| `archon-test-loop` | Iterative test fixing | Fix failing tests in a loop until green. |
| `archon-assist` | General assistance | Open-ended help, exploration, Q&A. |

### Workflow Comparison: Déjà vs Archon Defaults

| Aspect | Déjà (`deja-*`) | Archon (`archon-*`) |
|--------|-----------------|---------------------|
| **Steps** | 5 (plan→code→test→validate→commit) | 5-11 depending on workflow |
| **PR Creation** | Separate workflow | Built into most workflows |
| **Code Review** | None | Multi-agent parallel review |
| **Auto-fix** | None | Fixes CRITICAL/HIGH findings |
| **GitHub Integration** | Manual | Posts to issues/PRs automatically |
| **Complexity** | Simple, linear | DAG-based, conditional routing |
| **Project Knowledge** | Déjà patterns baked in | Generic, discovers patterns |
| **Token Cost** | Lower | Higher |
| **Execution Time** | Faster | Slower |

---

## Example Commands for GitHub Issues

### Using Archon Default (Recommended for GitHub Issues)

```bash
# Fix issue #2 with full pipeline
archon workflow run archon-fix-github-issue --branch fix/note-edit-fallthrough "#2"

# Or with description
archon workflow run archon-fix-github-issue --branch fix/note-edit-fallthrough \
  "Fix #2: =note with missing text silently falls through"
```

### Using Déjà Custom (Faster, No Review)

```bash
# Fix issue #2 with Déjà workflow
archon workflow run deja-implement --branch fix/note-edit-fallthrough \
  "Fix #2: Add guard for =note with missing text, print helpful error and exit 1"
```

### Post-Implementation Review

```bash
# After deja-implement, add code review
archon workflow run archon-smart-pr-review "Review the fix for #2"
```
