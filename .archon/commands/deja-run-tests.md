# Run Déjà Tests

Run the test suite and fix any failures.

## Run Tests

```bash
pytest tests/ -v
```

## Your Mission

1. Run the full test suite
2. If tests fail:
   - Analyze the failure
   - Fix the test OR the code (whichever is wrong)
   - Re-run to verify
3. Continue until all tests pass

## Common Issues

### Import errors
- Check that lib/ is in the Python path
- May need to add `sys.path` manipulation in tests

### Mock issues
- Ensure mock targets the right module path
- Mock where the function is used, not where it's defined

### Fixture issues
- Check fixture scope (function vs module vs session)
- Ensure fixtures return appropriate data types

## Output

Report final test results:
- Total tests
- Passed
- Failed (if any remain)
