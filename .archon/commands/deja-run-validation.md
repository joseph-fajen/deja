# Déjà Full Validation

Run comprehensive validation on the Déjà codebase.

## Validation Steps

### 1. Python Syntax Check
```bash
python3 -m py_compile deja
python3 -m py_compile lib/*.py
python3 -m py_compile lib/commands/*.py
```

### 2. CLI Functionality
```bash
./deja --help
./deja --limit 2
./deja projects
```

### 3. Test Suite (if exists)
```bash
if [ -d "tests" ]; then
    pytest tests/ -v
else
    echo "No tests directory found"
fi
```

### 4. Search Functionality (if conversations exist)
```bash
./deja "test"
```

## Report Format

Provide a summary:

```
Déjà Validation Report
======================

Syntax Check:     PASS/FAIL
CLI Help:         PASS/FAIL
CLI List:         PASS/FAIL
CLI Projects:     PASS/FAIL
Test Suite:       PASS/FAIL/SKIPPED
Search:           PASS/FAIL

Overall:          PASS/FAIL
```

If any check fails, provide details about what went wrong.
