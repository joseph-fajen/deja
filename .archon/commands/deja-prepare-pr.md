# Prepare Déjà Pull Request

Create a pull request for the upstream Déjà repository.

## Task
$ARGUMENTS

## Your Mission

1. Review all commits on this branch
2. Understand the full scope of changes
3. Create a well-structured PR

## PR Structure

```bash
gh pr create --title "feat: <concise description>" --body "$(cat <<'EOF'
## Summary

<1-3 sentences describing what this PR does>

## Changes

- <Bullet point changes>
- <Include files modified/added>

## Testing

<How was this tested?>
- Manual testing steps taken
- Test suite results (if applicable)

## Notes for Reviewer

<Any context the reviewer should know>
EOF
)"
```

## Pre-PR Checklist

Before creating the PR:
- [ ] All changes committed
- [ ] Branch pushed to origin
- [ ] Validation passes
- [ ] Commit messages are clear

## Important

- Target the upstream repo: `kateleext/deja`
- If this is a fork, ensure your fork is synced first
- Use conventional commit style for PR title
