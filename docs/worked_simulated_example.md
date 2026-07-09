# Worked simulated example

This example demonstrates the intended workflow on a single-partner June-style
input table:

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
| 1 | SIM_KIMS_S1_036 | KIMS_S1 | Tier1_CR | PP12 | ST35 |
| 2 | SIM_KIMS_S2_007 | KIMS_S2 | Tier1_CR | PP14 | ST86 |
| 3 | SIM_KIMS_S3_003 | KIMS_S3 | Tier1_CR | PP6 | ST48 |
| 4 | SIM_KIMS_S4_004 | KIMS_S4 | Tier1_CR | PP8 | ST307 |
| 5 | SIM_KIMS_S5_005 | KIMS_S5 | Tier1_CR | PP10 | ST15 |
| 6 | SIM_KIMS_S2_032 | KIMS_S2 | Tier1_CR | PP4 | ST17 |
| 7 | SIM_KIMS_S3_008 | KIMS_S3 | Tier1_CR | PP1 | ST147 |
| 8 | SIM_KIMS_S4_009 | KIMS_S4 | Tier1_CR | PP3 | ST11 |
| 9 | SIM_KIMS_S1_001 | KIMS_S1 | Tier1_CR | PP2 | ST101 |
| 10 | SIM_KIMS_S5_015 | KIMS_S5 | Tier1_CR | PP15 | ST512 |
| 11 | SIM_KIMS_S1_011 | KIMS_S1 | Tier1_CR | PP7 | ST258 |
| 12 | SIM_KIMS_S2_027 | KIMS_S2 | Tier1_CR | PP9 | ST231 |
| 13 | SIM_KIMS_S3_013 | KIMS_S3 | Tier1_CR | PP11 | ST395 |
| 14 | SIM_KIMS_S4_029 | KIMS_S4 | Tier1_CR | PP13 | ST23 |
| 15 | SIM_KIMS_S5_025 | KIMS_S5 | Tier1_CR | PP5 | ST45 |
| 16 | SIM_KIMS_S1_016 | KIMS_S1 | Tier1_CR | PP2 | ST101 |
| 17 | SIM_KIMS_S2_017 | KIMS_S2 | Tier1_CR | PP4 | ST17 |
| 18 | SIM_KIMS_S3_023 | KIMS_S3 | Tier1_CR | PP1 | ST147 |
| 19 | SIM_KIMS_S4_019 | KIMS_S4 | Tier1_CR | PP8 | ST307 |
| 20 | SIM_KIMS_S5_020 | KIMS_S5 | Tier1_CR | PP10 | ST15 |
| 21 | SIM_KIMS_S1_021 | KIMS_S1 | Tier1_CR | PP12 | ST35 |
| 22 | SIM_KIMS_S3_028 | KIMS_S3 | Tier1_CR | PP11 | ST395 |
| 23 | SIM_KIMS_S5_040 | KIMS_S5 | Tier1_CR | PP5 | ST45 |
| 24 | SIM_KIMS_S2_022 | KIMS_S2 | Tier1_CR | PP14 | ST86 |
| 25 | SIM_KIMS_S4_014 | KIMS_S4 | Tier1_CR | PP13 | ST23 |

## Why the selected set is balanced

With `--n-select 25`, the script:

1. takes Tier1_CR isolates first;
2. spreads those Tier1_CR choices across the partner's sentinel sites before
   taking site duplicates;
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
