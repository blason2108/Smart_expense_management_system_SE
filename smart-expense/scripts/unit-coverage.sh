#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
report_dir=${1:-unit-results}
mkdir -p "$report_dir"
export COVERAGE_FILE="$report_dir/.coverage"

python -m pytest -o addopts='' tests/unit \
  --cov --cov-branch --cov-report=term-missing \
  --cov-report="xml:$report_dir/coverage.xml" \
  --junitxml="$report_dir/test-results.xml"
python -m coverage html --title "Unit Test Coverage" -d "$report_dir/html"
