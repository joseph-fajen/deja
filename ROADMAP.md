# Déjà Roadmap

Improvement ideas for the Déjà episodic memory skill.

## High-Impact Improvements

### 1. Semantic/Vector Search
**Problem**: Search is keyword-based with Porter stemming. Fails when:
- You remember the concept but not exact words ("that auth discussion" won't find "authentication")
- Synonyms are used ("fix" vs "repair" vs "resolve")

**Solution**: Add embedding-based search for conceptual queries. Could use local embeddings (sentence-transformers) or API-based.

**Complexity**: Medium-high (new dependency, embedding storage, hybrid scoring)

**Dependency Impact**: ⚠️ **Clashes with zero-dep philosophy.** Requires either heavy ML stack (`sentence-transformers` ~2GB+) or API client + key management. See [Dependency Analysis](#dependency-analysis).

---

### 2. Session Continuity Detection
**Problem**: No way to know when sessions are continuations of each other. Starting fresh but picking up where you left off creates unlinked sessions.

**Solution**: Detect session relationships via:
- Same project + similar topics within time window
- Explicit "continue from session X" patterns in messages
- Overlapping file touches

**Complexity**: Medium (heuristics, optional linking UI)

---

### 3. Performance: Cache First-Match Location
**Problem**: In `search.py:23-54`, `_find_first_matching_turn()` re-parses the entire JSONL file for every search result to find where the match occurred. Expensive with many results.

**Solution**: Cache match locations during indexing, or at minimum cache parsed entries.

**Complexity**: Low-medium (index structure change)

---

### 4. Note Management (Edit/Delete) ✅ COMPLETED
**Problem**: Can only add notes, not edit or delete. Wrong breadcrumbs are stuck forever.

**Solution**: Add commands:
- `deja <session> -note N` to delete note N
- `deja <session> =note N "new text"` to edit

**Complexity**: Low (straightforward CRUD)

**Status**: Implemented via Archon workflow. PR merged.
- Commands: `=note N "text"` (edit), `-note N` (delete)
- 23 tests in `test_notes.py`
- Error handling: `NotesSaveError`, corrupt file backup
- Docs updated: README.md, SKILL.md

**Remaining polish** (see GitHub issues):
- [#2](https://github.com/joseph-fajen/deja/issues/2) `=note` missing text fallthrough
- [#3](https://github.com/joseph-fajen/deja/issues/3) CLI exit code 0 on failure
- [#4](https://github.com/joseph-fajen/deja/issues/4) Confusing error for empty sessions
- [#5](https://github.com/joseph-fajen/deja/issues/5) Summary line phrasing
- [#6](https://github.com/joseph-fajen/deja/issues/6) Module docstring for return convention
- [#7](https://github.com/joseph-fajen/deja/issues/7) Command wrapper tests
- [#8](https://github.com/joseph-fajen/deja/issues/8) Negative index tests

---

### 5. Test Suite ✓ IN PROGRESS
**Problem**: No tests in the repo. Regressions possible as features are added.

**Solution**: Add pytest tests for:
- Stemmer correctness
- Extraction from sample JSONL
- Search scoring logic
- Session ID resolution

**Complexity**: Low-medium (test infrastructure, fixtures)

**Status**: 82 tests passing
- `test_stemmer.py`: 28 tests (Porter Stemmer steps, public API)
- `test_extraction.py`: 31 tests (content extraction, activity signals, episodes)
- `test_notes.py`: 23 tests (CRUD operations, error handling, persistence)
- Remaining: cache, search, commands (require mocking - lower priority)

---

## Medium-Impact Improvements

### 6. Fuzzy Matching Option
**Problem**: Exact matching fails when you can't remember spelling.

**Solution**: Add `--fuzzy` flag using edit distance or phonetic matching.

**Complexity**: Low-medium (algorithm choice, integration with scoring)

**Dependency Impact**: ⚡ **Optional.** Pure Python Levenshtein is O(n×m) but workable for short queries. Libraries like `rapidfuzz` are faster but add a dependency. Recommend pure Python first.

---

### 7. Session Summarization
**Problem**: Reading a session shows raw messages. Hard to quickly understand "what happened."

**Solution**: Generate LLM summary of session on demand. Cache summaries.

**Complexity**: Medium (LLM integration, caching, cost considerations)

**Dependency Impact**: ⚠️ **Clashes with zero-dep philosophy.** Requires LLM API access. However, see [Leverage Claude](#option-2-leverage-claude-itself) - the agent using Déjà could do the summarization without the skill needing API access.

---

### 8. Cross-Session Analysis
**Problem**: No way to aggregate insights across sessions ("patterns in my auth work").

**Solution**: Query that spans multiple sessions and synthesizes findings.

**Complexity**: High (multi-session context, LLM synthesis)

**Dependency Impact**: ⚠️ **Clashes with zero-dep philosophy.** Same as Session Summarization - requires LLM. Could alternatively output structured data for Claude to synthesize.

---

### 9. Configurable Truncation
**Problem**: `TRUNCATE_LENGTH = 500` in `read.py` is hardcoded.

**Solution**: Make configurable via env var or config file.

**Complexity**: Low

---

## Dependency Analysis

Déjà follows a **zero-dependency philosophy** - pure Python stdlib only. This keeps the skill lightweight, avoids version conflicts, and simplifies installation (just clone and run).

### Compatibility Summary

| Item | Clashes? | Notes |
|------|----------|-------|
| Semantic/Vector Search | ⚠️ **Yes** | Heavy ML deps or API client required |
| Session Continuity | ✅ No | Pure heuristics on existing data |
| Cache First-Match | ✅ No | Internal optimization |
| Note Management | ✅ No | CRUD on JSON file |
| Test Suite | ✅ No | Dev dependency only (pytest) |
| Fuzzy Matching | ⚡ **Maybe** | Pure Python possible but slower |
| Session Summarization | ⚠️ **Yes** | Needs LLM API access |
| Cross-Session Analysis | ⚠️ **Yes** | Needs LLM API access |
| Configurable Truncation | ✅ No | Config/env vars |

### Resolution Options

#### Option 1: Optional Dependencies
Core functionality stays zero-dep. Advanced features (semantic search) require opt-in installation with graceful degradation:
```python
try:
    from sentence_transformers import SentenceTransformer
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False
```

#### Option 2: Leverage Claude Itself
For summarization and analysis, the skill outputs structured data that Claude (the agent using the skill) processes. No API call needed - Claude is already there interpreting the output.

Example: Instead of `deja summarize <session>` calling an LLM, `deja <session> --raw` outputs full content and Claude summarizes it in context.

#### Option 3: Pure Python Alternatives
- **Fuzzy matching**: Implement Levenshtein in pure Python. Slower but zero-dep. Query terms are short; performance is acceptable.
- **Semantic search**: Defer until value clearly justifies complexity, or explore lightweight approaches (word2vec with pre-computed vectors?).

#### Option 4: Defer High-Dependency Features
Keep semantic search aspirational. Focus on high-value zero-dep improvements first (note management, fuzzy matching, caching).

### Recommendation

**Prioritize zero-dep items first:**
1. Note Management (#4) - pure Python, high user value
2. Fuzzy Matching (#6) - pure Python implementation
3. Cache First-Match (#3) - performance win, pure Python
4. Configurable Truncation (#9) - trivial, pure Python

**Defer or redesign dependency-heavy items:**
- Semantic Search: Explore "leverage Claude" pattern or accept as future optional feature
- Session Summarization: Use "leverage Claude" pattern - output data, let Claude summarize
- Cross-Session Analysis: Same approach

---

## Implementation Notes

- Maintain backward compatibility with existing cache format
- Consider upstream PR viability for each change
- Test coverage before new features

## Selected Focus Areas

### Completed: Note Management (#4)
Edit and delete notes implemented. 7 polish issues tracked in GitHub.

### Current: Test Suite (#5)
Foundation work. Core modules (stemmer, extraction, notes) covered. 82 tests passing.

### Next Steps

**Recommended priority (zero-dep, high-value):**

1. **Fuzzy Matching (#6)** - Pure Python Levenshtein, user-visible improvement
2. **Cache First-Match (#3)** - Performance optimization for search
3. **Configurable Truncation (#9)** - Trivial, improves flexibility

**Polish work (from Note Management review):**
- Address MEDIUM issues: #2 (fallthrough bug), #3 (exit codes), #7 (wrapper tests)
- Address LOW issues: #4, #5, #6, #8

**Deferred (dependency concerns):**
- Semantic Search (#1) - Explore "leverage Claude" pattern
- Session Summarization (#7) - Use "leverage Claude" pattern
- Session Continuity (#2) - Medium complexity, requires design
