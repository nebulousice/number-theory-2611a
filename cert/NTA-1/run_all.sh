#!/usr/bin/env bash
# Run the NTA-1 certificates and archive outputs with headers.
# Usage (from anywhere): bash targets/number-theory-2611a/cert/NTA-1/run_all.sh [NEXTRA]
# Writes out/NTA-1.out, out/NTA-1_x.out, out/compare.out next to this script.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
nextra="${1:-3}"
out="$here/out"; mkdir -p "$out"
root="$(git -C "$here" rev-parse --show-toplevel)"
commit="$(git -C "$here" rev-parse HEAD)"
dirty="$(git -C "$root" status --porcelain -- "$here" | grep -v ' out/' | tr '\n' ';')"
header() {  # $1 = command
  echo "command: $1"
  echo "cwd: $here"
  echo "date (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "commit: $commit"
  echo "uncommitted files under cert/NTA-1 at run time: ${dirty:-none}"
  echo "sha256: $(cd "$here" && sha256sum NTA-1.py NTA-1_x.mjs compare.py run_all.sh | tr '\n' ' ')"
  echo "python: $(python --version 2>&1); python-flint $(python -c 'import flint;print(flint.__version__)'); node $(node --version)"
  echo "host: $(uname -srm)"
  echo "----"
}
run() {  # $1 = outfile, rest = command
  local f="$1"; shift
  { header "$*"; } > "$f"
  local t0=$(date +%s.%N)
  ( cd "$here" && "$@" ) >> "$f" 2>&1
  local rc=$?
  local t1=$(date +%s.%N)
  echo "----" >> "$f"
  echo "exit code: $rc; wall time: $(python -c "print(round($t1-$t0,2))") s" >> "$f"
  tail -3 "$f"
}
run "$out/NTA-1.out"   python NTA-1.py "$nextra"
run "$out/NTA-1_x.out" node NTA-1_x.mjs "$nextra"
run "$out/compare.out" python compare.py out/NTA-1.out out/NTA-1_x.out
