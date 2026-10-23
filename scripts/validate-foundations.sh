#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UV="${UV:-uv}"
PIP_AUDIT_RUNNER="${PIP_AUDIT_RUNNER:-}"

if [[ $# -eq 0 ]]; then
  projects=(accesshold curiolab nexttime harvestgrid roomsmith)
else
  projects=("$@")
fi

validate_node() {
  local project="$1"
  local directory="$ROOT/projects/$project"
  echo "==> $project: lint, typecheck, unit, contract, security/audit, build, fixture"
  make -C "$directory" lint typecheck test-unit test-contract test-security build dev
  if [[ "$project" == "curiolab" || "$project" == "roomsmith" ]]; then
    (cd "$directory" && corepack pnpm validate:content)
  fi
}

validate_python() {
  local project="$1"
  local directory="$ROOT/projects/$project"
  echo "==> $project: lint, typecheck, unit/coverage, contract, security/audit, build, fixture"
  make -C "$directory" UV="$UV" lint typecheck test-unit test-contract build
  if [[ -n "$PIP_AUDIT_RUNNER" ]]; then
    make -C "$directory" \
      UV="$UV" \
      PIP_AUDIT="$PIP_AUDIT_RUNNER" \
      PIP_AUDIT_ARGS="--path $directory/.venv/lib/python3.12/site-packages" \
      test-security
  else
    make -C "$directory" UV="$UV" test-security
  fi
  make -C "$directory" UV="$UV" dev
}

for project in "${projects[@]}"; do
  case "$project" in
    accesshold|curiolab|roomsmith) validate_node "$project" ;;
    nexttime|harvestgrid) validate_python "$project" ;;
    *) echo "Unknown foundation project: $project" >&2; exit 2 ;;
  esac
done

echo "==> Requested local foundation checks passed. Live integrations, devices, deployment, and release gates remain separate."
