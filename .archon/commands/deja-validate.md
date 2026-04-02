# Déjà Validation

Run validation checks on the implementation.

## Checks to Run

### 1. Syntax Check
```bash
python3 -m py_compile deja
python3 -m py_compile lib/*.py
python3 -m py_compile lib/commands/*.py
```

### 2. Basic Functionality
```bash
./deja --help
./deja --limit 3
./deja projects
```

### 3. Run Tests (if they exist)
```bash
pytest tests/ -v
```
If no tests directory exists, note this and continue.

## Your Mission

1. Run all validation checks
2. Report any errors found
3. If errors exist, attempt to fix them
4. Re-run validation after fixes

## Output

Report the final status:
- Syntax: PASS/FAIL
- Basic functionality: PASS/FAIL
- Tests: PASS/FAIL/SKIPPED (no tests)

If any checks failed and couldn't be fixed, list the issues.
