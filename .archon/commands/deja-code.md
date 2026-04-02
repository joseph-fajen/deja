# Déjà Code Implementation

You are implementing code for the Déjà episodic memory skill.

## Task
$ARGUMENTS

## Plan
$PLAN

## Implementation Guidelines

### Code Style
- Pure Python, no external dependencies
- Type hints on function signatures
- Docstrings on public functions
- Follow existing patterns in lib/

### Module Structure
- Commands go in lib/commands/
- Utilities go in appropriate lib/*.py files
- Entry point modifications go in deja (the main script)

### Key Patterns to Follow
- Commands return `(summary_line, data_dict)` tuples
- Use `ensure_cache_fresh()` before accessing cache
- Use `omit_empty()` for JSON output cleanup
- Constants at module level, not magic numbers in code

## Your Mission

1. Read the plan from the previous step
2. Implement the code following the guidelines
3. Make minimal, focused changes
4. Don't add features beyond what's requested

## Important

- Keep the zero-dependency philosophy
- Maintain backward compatibility with existing cache format
- Test your changes manually with `./deja --help` and basic commands
