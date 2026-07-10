# Simulated example results

The simulated input is:

`examples/simulated_june_priority.csv`

It represents one KIMS partner run with 100 candidate isolates across five KIMS
sentinel sites. The example asks for 25 long-read isolates:

```bash
python3 scripts/select_longread_samples.py \
  --input examples/simulated_june_priority.csv \
  --n-select 25 \
  --tier-targets Tier1_CR=10,Tier2_MDR=8,Tier3_nonMDR_resistant=3,Tier4_pansusceptible=4 \
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

The selected set deliberately includes all four resistance tiers:

| tier | selected |
| --- | --- |
| Tier1_CR | 10 |
| Tier2_MDR | 8 |
| Tier3_nonMDR_resistant | 3 |
| Tier4_pansusceptible | 4 |

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
| 11 | SIM_KIMS_S2_012 | KIMS_S2 | India | Tier2_MDR | RP9 | PP9 | ST231 | Primary |
| 12 | SIM_KIMS_S3_063 | KIMS_S3 | India | Tier2_MDR | RP8 | PP11 | ST147 | Primary |
| 13 | SIM_KIMS_S1_046 | KIMS_S1 | India | Tier2_MDR | RP2 | PP7 | ST35 | Primary |
| 14 | SIM_KIMS_S4_049 | KIMS_S4 | India | Tier2_MDR | RP11 | PP13 | ST11 | Primary |
| 15 | SIM_KIMS_S5_045 | KIMS_S5 | India | Tier2_MDR | RP11 | PP5 | ST15 | Primary |
| 16 | SIM_KIMS_S1_051 | KIMS_S1 | India | Tier2_MDR | RP8 | PP2 | ST258 | Primary |
| 17 | SIM_KIMS_S3_053 | KIMS_S3 | India | Tier2_MDR | RP15 | PP6 | ST395 | Primary |
| 18 | SIM_KIMS_S4_054 | KIMS_S4 | India | Tier2_MDR | RP2 | PP8 | ST23 | Primary |
| 19 | SIM_KIMS_S5_080 | KIMS_S5 | India | Tier3_nonMDR_resistant | RP17 | PP15 | ST45 | Primary |
| 20 | SIM_KIMS_S2_077 | KIMS_S2 | India | Tier3_nonMDR_resistant | RP16 | PP9 | ST86 | Primary |
| 21 | SIM_KIMS_S3_073 | KIMS_S3 | India | Tier3_nonMDR_resistant | RP12 | PP1 | ST48 | Primary |
| 22 | SIM_KIMS_S2_072 | KIMS_S2 | India | Tier4_pansusceptible | RP1 | PP14 | ST17 | Primary |
| 23 | SIM_KIMS_S1_086 | KIMS_S1 | India | Tier4_pansusceptible | RP1 | PP12 | ST101 | Primary |
| 24 | SIM_KIMS_S4_089 | KIMS_S4 | India | Tier4_pansusceptible | RP1 | PP3 | ST307 | Primary |
| 25 | SIM_KIMS_S5_100 | KIMS_S5 | India | Tier4_pansusceptible | RP1 | PP10 | ST512 | Primary |

## Plasmid-profile coverage in the selected set

| plasmid_profile | selected |
| --- | --- |
| PP12 | 2 |
| PP14 | 2 |
| PP6 | 2 |
| PP8 | 2 |
| PP10 | 2 |
| PP1 | 2 |
| PP3 | 2 |
| PP2 | 2 |
| PP15 | 2 |
| PP9 | 2 |
| PP4 | 1 |
| PP11 | 1 |
| PP7 | 1 |
| PP13 | 1 |
| PP5 | 1 |

## What this demonstrates

The simulated result shows the intended behaviour:

1. All four resistance tiers are represented according to explicit tier targets.
2. All five KIMS sentinel sites are equally represented in the 25-isolate
   selected set.
3. Plasmid profiles are considered before ST duplication becomes relevant.
4. ST does not override the higher-priority tier, site, and plasmid-profile
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
