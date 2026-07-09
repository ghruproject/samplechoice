# Worked simulated example

This example demonstrates the intended workflow on a small June-style input
table:

`examples/simulated_june_priority.csv`

The table contains:

- AST interpretation columns, so tiers can be recomputed from AST;
- sentinel-site codes across five sites;
- June-style `tier`, `rp_code`, `PP_code`, and `Plasmids` columns;
- ST, AMR gene, virulence, and QC fields;
- 20 candidate isolates, more than the example sequencing capacity.

## Run the example

```bash
python3 scripts/select_longread_samples.py \
  --input examples/simulated_june_priority.csv \
  --n-select 10 \
  --output outputs/simulated_priority.csv
```

Expected summary:

```text
Wrote 20 ranked isolates to outputs/simulated_priority.csv
selection_batch
Primary      18
Secondary     2
computed_tier
Tier1_CR                  8
Tier2_MDR                 5
Tier4_pansusceptible      4
Tier3_nonMDR_resistant    3
selected_for_sequencing
yes    10
no     10
```

The selected rows are the first practical sequencing set. The remaining rows are
ranked alternates.

In this simulated run the selected set is:

| Rank | Isolate | Site | Tier | Plasmid profile | ST |
| --- | --- | --- | --- | --- | --- |
| 1 | SIM_AGR_001 | AGROSAVIA | Tier1_CR | PP1 | ST307 |
| 2 | SIM_RITM_001 | RITM | Tier1_CR | PP2 | ST147 |
| 3 | SIM_KIMS_002 | KIMS | Tier1_CR | PP5 | ST231 |
| 4 | SIM_CGPS_001 | CGPS | Tier1_CR | PP4 | ST15 |
| 5 | SIM_IBD_001 | IBADAN | Tier1_CR | PP3 | ST101 |
| 6 | SIM_KIMS_001 | KIMS | Tier1_CR | PP1 | ST231 |
| 7 | SIM_RITM_002 | RITM | Tier1_CR | PP2 | ST147 |
| 8 | SIM_AGR_002 | AGROSAVIA | Tier1_CR | PP1 | ST307 |
| 9 | SIM_CGPS_002 | CGPS | Tier2_MDR | PP10 | ST35 |
| 10 | SIM_IBD_002 | IBADAN | Tier2_MDR | PP9 | ST17 |

## Why the selected set is balanced

With `--n-select 10`, the script:

1. takes Tier1_CR isolates first;
2. spreads those Tier1_CR choices across sentinel sites before taking site
   duplicates;
3. prefers different plasmid profiles within the same tier/site balance;
4. only then moves into Tier2_MDR;
5. uses ST as a late tie-breaker if there is still a choice.

For a real run, change only the input and requested sequencing capacity:

```bash
python3 scripts/select_longread_samples.py \
  --input isolate_priority_longread_2026-05-22.xlsx \
  --n-select 96 \
  --output outputs/longread_selection_96.csv
```
