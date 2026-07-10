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
  --tier-targets Tier1_CR=10,Tier2_MDR=8,Tier3_nonMDR_resistant=3,Tier4_pansusceptible=4 \
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
| 11 | SIM_KIMS_S2_012 | KIMS_S2 | Tier2_MDR | PP9 | ST231 |
| 12 | SIM_KIMS_S3_063 | KIMS_S3 | Tier2_MDR | PP11 | ST147 |
| 13 | SIM_KIMS_S1_046 | KIMS_S1 | Tier2_MDR | PP7 | ST35 |
| 14 | SIM_KIMS_S4_049 | KIMS_S4 | Tier2_MDR | PP13 | ST11 |
| 15 | SIM_KIMS_S5_045 | KIMS_S5 | Tier2_MDR | PP5 | ST15 |
| 16 | SIM_KIMS_S1_051 | KIMS_S1 | Tier2_MDR | PP2 | ST258 |
| 17 | SIM_KIMS_S3_053 | KIMS_S3 | Tier2_MDR | PP6 | ST395 |
| 18 | SIM_KIMS_S4_054 | KIMS_S4 | Tier2_MDR | PP8 | ST23 |
| 19 | SIM_KIMS_S5_080 | KIMS_S5 | Tier3_nonMDR_resistant | PP15 | ST45 |
| 20 | SIM_KIMS_S2_077 | KIMS_S2 | Tier3_nonMDR_resistant | PP9 | ST86 |
| 21 | SIM_KIMS_S3_073 | KIMS_S3 | Tier3_nonMDR_resistant | PP1 | ST48 |
| 22 | SIM_KIMS_S2_072 | KIMS_S2 | Tier4_pansusceptible | PP14 | ST17 |
| 23 | SIM_KIMS_S1_086 | KIMS_S1 | Tier4_pansusceptible | PP12 | ST101 |
| 24 | SIM_KIMS_S4_089 | KIMS_S4 | Tier4_pansusceptible | PP3 | ST307 |
| 25 | SIM_KIMS_S5_100 | KIMS_S5 | Tier4_pansusceptible | PP10 | ST512 |

## Why the selected set is balanced

With `--n-select 25` and explicit tier targets, the script:

1. selects the requested number from each resistance tier;
2. spreads choices within each tier across the partner's sentinel sites before
   taking site duplicates;
3. prefers different plasmid profiles within the same tier/site balance;
4. uses ST as a late tie-breaker if there is still a choice.

For a real run, change only the input and requested sequencing capacity:

```bash
python3 scripts/select_longread_samples.py \
  --input isolate_priority_longread_2026-05-22.xlsx \
  --n-select 96 \
  --tier-targets Tier1_CR=40,Tier2_MDR=32,Tier3_nonMDR_resistant=12,Tier4_pansusceptible=12 \
  --output outputs/longread_selection_96.csv
```
