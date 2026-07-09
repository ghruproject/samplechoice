# Worked simulated example

This example demonstrates the intended workflow on a small June-style input
table:

`examples/simulated_june_priority.csv`

The table contains:

- AST interpretation columns, so tiers can be recomputed from AST;
- sentinel-site codes across five sites;
- June-style `tier`, `rp_code`, `PP_code`, and `Plasmids` columns;
- ST, AMR gene, virulence, and QC fields;
- 100 candidate isolates, more than the example sequencing capacity.

## Run the example

```bash
python3 scripts/select_longread_samples.py \
  --input examples/simulated_june_priority.csv \
  --n-select 25 \
  --output outputs/simulated_priority.csv
```

Expected summary:

```text
Wrote 100 ranked isolates to outputs/simulated_priority.csv
selection_batch
Primary      88
Secondary    12
computed_tier
Tier1_CR                  36
Tier2_MDR                 35
Tier4_pansusceptible      19
Tier3_nonMDR_resistant    10
selected_for_sequencing
no     75
yes    25
```

The selected rows are the first practical sequencing set. The remaining rows are
ranked alternates.

In this simulated run the selected set is:

| Rank | Isolate | Site | Tier | Plasmid profile | ST |
| --- | --- | --- | --- | --- | --- |
| 1 | SIM_AGR_036 | AGROSAVIA | Tier1_CR | PP12 | ST35 |
| 2 | SIM_CGPS_005 | CGPS | Tier1_CR | PP10 | ST15 |
| 3 | SIM_IBD_004 | IBADAN | Tier1_CR | PP8 | ST307 |
| 4 | SIM_KIMS_003 | KIMS | Tier1_CR | PP6 | ST48 |
| 5 | SIM_RITM_007 | RITM | Tier1_CR | PP14 | ST86 |
| 6 | SIM_IBD_009 | IBADAN | Tier1_CR | PP3 | ST11 |
| 7 | SIM_KIMS_008 | KIMS | Tier1_CR | PP1 | ST147 |
| 8 | SIM_RITM_032 | RITM | Tier1_CR | PP4 | ST17 |
| 9 | SIM_AGR_001 | AGROSAVIA | Tier1_CR | PP2 | ST101 |
| 10 | SIM_CGPS_015 | CGPS | Tier1_CR | PP15 | ST512 |
| 11 | SIM_AGR_011 | AGROSAVIA | Tier1_CR | PP7 | ST258 |
| 12 | SIM_CGPS_025 | CGPS | Tier1_CR | PP5 | ST45 |
| 13 | SIM_IBD_029 | IBADAN | Tier1_CR | PP13 | ST23 |
| 14 | SIM_KIMS_013 | KIMS | Tier1_CR | PP11 | ST395 |
| 15 | SIM_RITM_027 | RITM | Tier1_CR | PP9 | ST231 |
| 16 | SIM_AGR_016 | AGROSAVIA | Tier1_CR | PP2 | ST101 |
| 17 | SIM_CGPS_020 | CGPS | Tier1_CR | PP10 | ST15 |
| 18 | SIM_IBD_019 | IBADAN | Tier1_CR | PP8 | ST307 |
| 19 | SIM_KIMS_023 | KIMS | Tier1_CR | PP1 | ST147 |
| 20 | SIM_RITM_017 | RITM | Tier1_CR | PP4 | ST17 |
| 21 | SIM_AGR_021 | AGROSAVIA | Tier1_CR | PP12 | ST35 |
| 22 | SIM_CGPS_040 | CGPS | Tier1_CR | PP5 | ST45 |
| 23 | SIM_KIMS_028 | KIMS | Tier1_CR | PP11 | ST395 |
| 24 | SIM_IBD_014 | IBADAN | Tier1_CR | PP13 | ST23 |
| 25 | SIM_RITM_022 | RITM | Tier1_CR | PP14 | ST86 |

## Why the selected set is balanced

With `--n-select 25`, the script:

1. takes Tier1_CR isolates first;
2. spreads those Tier1_CR choices across sentinel sites before taking site
   duplicates;
3. prefers different plasmid profiles within the same tier/site balance;
4. does not move into Tier2_MDR because the Tier1_CR candidates fill the
   25-isolate capacity;
5. uses ST as a late tie-breaker if there is still a choice.

For a real run, change only the input and requested sequencing capacity:

```bash
python3 scripts/select_longread_samples.py \
  --input isolate_priority_longread_2026-05-22.xlsx \
  --n-select 96 \
  --output outputs/longread_selection_96.csv
```
