# Simulated example results

The simulated input is:

`examples/simulated_june_priority.csv`

It represents one KIMS partner run with 100 candidate isolates across five KIMS
sentinel sites. The example asks for 25 long-read isolates:

```bash
python3 scripts/select_longread_samples.py \
  --input examples/simulated_june_priority.csv \
  --n-select 25 \
  --output outputs/simulated_priority.csv
```

## Overall result

| selected_for_sequencing | isolates |
| --- | --- |
| no | 75 |
| yes | 25 |

The selected set is balanced across all five sentinel sites:

| site | country | selected |
| --- | --- | --- |
| KIMS_S1 | India | 5 |
| KIMS_S2 | India | 5 |
| KIMS_S3 | India | 5 |
| KIMS_S4 | India | 5 |
| KIMS_S5 | India | 5 |

The input contains candidates across all four tiers after AST tiering is
computed:

| tier | input_candidates |
| --- | --- |
| Tier1_CR | 36 |
| Tier2_MDR | 35 |
| Tier4_pansusceptible | 19 |
| Tier3_nonMDR_resistant | 10 |

The selected set contains only Tier1_CR isolates because the requested 25 slots
are filled before the Tier1_CR candidates are exhausted:

| tier | selected |
| --- | --- |
| Tier1_CR | 25 |

## Selected isolates

| selection_rank | isolate_id | site | country | computed_tier | computed_rp_code | computed_pp_code | st | selection_batch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIM_KIMS_S1_036 | KIMS_S1 | India | Tier1_CR | RP13 | PP12 | ST35 | Primary |
| 2 | SIM_KIMS_S2_007 | KIMS_S2 | India | Tier1_CR | RP4 | PP14 | ST86 | Primary |
| 3 | SIM_KIMS_S3_003 | KIMS_S3 | India | Tier1_CR | RP5 | PP6 | ST48 | Primary |
| 4 | SIM_KIMS_S4_004 | KIMS_S4 | India | Tier1_CR | RP3 | PP8 | ST307 | Primary |
| 5 | SIM_KIMS_S5_005 | KIMS_S5 | India | Tier1_CR | RP7 | PP10 | ST15 | Primary |
| 6 | SIM_KIMS_S2_032 | KIMS_S2 | India | Tier1_CR | RP6 | PP4 | ST17 | Primary |
| 7 | SIM_KIMS_S3_008 | KIMS_S3 | India | Tier1_CR | RP6 | PP1 | ST147 | Primary |
| 8 | SIM_KIMS_S4_009 | KIMS_S4 | India | Tier1_CR | RP5 | PP3 | ST11 | Primary |
| 9 | SIM_KIMS_S1_001 | KIMS_S1 | India | Tier1_CR | RP21 | PP2 | ST101 | Primary |
| 10 | SIM_KIMS_S5_015 | KIMS_S5 | India | Tier1_CR | RP5 | PP15 | ST512 | Primary |
| 11 | SIM_KIMS_S1_011 | KIMS_S1 | India | Tier1_CR | RP26 | PP7 | ST258 | Primary |
| 12 | SIM_KIMS_S2_027 | KIMS_S2 | India | Tier1_CR | RP23 | PP9 | ST231 | Primary |
| 13 | SIM_KIMS_S3_013 | KIMS_S3 | India | Tier1_CR | RP4 | PP11 | ST395 | Primary |
| 14 | SIM_KIMS_S4_029 | KIMS_S4 | India | Tier1_CR | RP7 | PP13 | ST23 | Primary |
| 15 | SIM_KIMS_S5_025 | KIMS_S5 | India | Tier1_CR | RP4 | PP5 | ST45 | Primary |
| 16 | SIM_KIMS_S1_016 | KIMS_S1 | India | Tier1_CR | RP19 | PP2 | ST101 | Primary |
| 17 | SIM_KIMS_S2_017 | KIMS_S2 | India | Tier1_CR | RP7 | PP4 | ST17 | Primary |
| 18 | SIM_KIMS_S3_023 | KIMS_S3 | India | Tier1_CR | RP7 | PP1 | ST147 | Primary |
| 19 | SIM_KIMS_S4_019 | KIMS_S4 | India | Tier1_CR | RP4 | PP8 | ST307 | Primary |
| 20 | SIM_KIMS_S5_020 | KIMS_S5 | India | Tier1_CR | RP6 | PP10 | ST15 | Primary |
| 21 | SIM_KIMS_S1_021 | KIMS_S1 | India | Tier1_CR | RP22 | PP12 | ST35 | Primary |
| 22 | SIM_KIMS_S3_028 | KIMS_S3 | India | Tier1_CR | RP3 | PP11 | ST395 | Primary |
| 23 | SIM_KIMS_S5_040 | KIMS_S5 | India | Tier1_CR | RP18 | PP5 | ST45 | Primary |
| 24 | SIM_KIMS_S2_022 | KIMS_S2 | India | Tier1_CR | RP3 | PP14 | ST86 | Primary |
| 25 | SIM_KIMS_S4_014 | KIMS_S4 | India | Tier1_CR | RP24 | PP13 | ST23 | Primary |

## Plasmid-profile coverage in the selected set

| plasmid_profile | selected |
| --- | --- |
| PP12 | 2 |
| PP10 | 2 |
| PP8 | 2 |
| PP14 | 2 |
| PP1 | 2 |
| PP4 | 2 |
| PP2 | 2 |
| PP5 | 2 |
| PP13 | 2 |
| PP11 | 2 |
| PP6 | 1 |
| PP3 | 1 |
| PP15 | 1 |
| PP7 | 1 |
| PP9 | 1 |

## What this demonstrates

The simulated result shows the intended behaviour:

1. Tier1_CR isolates are selected before lower tiers.
2. All five KIMS sentinel sites are equally represented in the 25-isolate
   selected set.
3. Plasmid profiles are considered before ST duplication becomes relevant.
4. ST does not override the higher-priority AST, site, and plasmid-profile
   criteria.
5. The output keeps the remaining 75 isolates as ranked alternates.

## Plasmid set-cover demonstration

The demo also runs:

```bash
python3 scripts/plasmid_set_cover.py \
  --input examples/example_plasmidfinder.tab \
  --output-prefix outputs/example_plasmid_cover
```

This small example selects 3 non-redundant isolate profiles and covers 5 of 5
observed plasmids. In a real run, this is used as a check that rare plasmid
signals have not been missed by the main tier/site/profile selection.
