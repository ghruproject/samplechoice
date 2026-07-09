#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs

python3 scripts/select_longread_samples.py \
  --input examples/simulated_june_priority.csv \
  --n-select 25 \
  --output outputs/simulated_priority.csv

python3 scripts/plasmid_set_cover.py \
  --input examples/example_plasmidfinder.tab \
  --output-prefix outputs/example_plasmid_cover

echo
echo "Demo outputs:"
echo "  outputs/simulated_priority.csv"
echo "  outputs/example_plasmid_cover_history.csv"
echo "  outputs/example_plasmid_cover_selected_isolates.txt"
