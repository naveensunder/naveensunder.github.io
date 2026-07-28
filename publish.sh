#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "This folder is not a git repository yet. Run git init and add the GitHub remote first." >&2
  exit 1
fi

./scripts/sync_latest_cv.sh

git add .

if git diff --cached --quiet; then
  echo "No new local changes to commit."
else
  message="${1:-Update website}"
  git commit -m "$message"
fi

branch="$(git branch --show-current)"
if [ -z "$branch" ]; then
  branch="main"
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "No origin remote is configured. Add origin before publishing." >&2
  exit 1
fi

git push -u origin "$branch"
