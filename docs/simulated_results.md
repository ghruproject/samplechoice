# Simulated example results

The simulated input is:

`examples/simulated_june_priority.csv`

It contains 100 candidate isolates across five sentinel sites. The example asks
for 25 long-read isolates:

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
| AGROSAVIA | Colombia | 5 |
| CGPS | United Kingdom | 5 |
| IBADAN | Nigeria | 5 |
| KIMS | India | 5 |
| RITM | Philippines | 5 |

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
| 1 | SIM_AGR_036 | AGROSAVIA | Colombia | Tier1_CR | RP13 | PP12 | ST35 | Primary |
| 2 | SIM_CGPS_005 | CGPS | United Kingdom | Tier1_CR | RP7 | PP10 | ST15 | Primary |
| 3 | SIM_IBD_004 | IBADAN | Nigeria | Tier1_CR | RP3 | PP8 | ST307 | Primary |
| 4 | SIM_KIMS_003 | KIMS | India | Tier1_CR | RP5 | PP6 | ST48 | Primary |
| 5 | SIM_RITM_007 | RITM | Philippines | Tier1_CR | RP4 | PP14 | ST86 | Primary |
| 6 | SIM_IBD_009 | IBADAN | Nigeria | Tier1_CR | RP5 | PP3 | ST11 | Primary |
| 7 | SIM_KIMS_008 | KIMS | India | Tier1_CR | RP6 | PP1 | ST147 | Primary |
| 8 | SIM_RITM_032 | RITM | Philippines | Tier1_CR | RP6 | PP4 | ST17 | Primary |
| 9 | SIM_AGR_001 | AGROSAVIA | Colombia | Tier1_CR | RP21 | PP2 | ST101 | Primary |
| 10 | SIM_CGPS_015 | CGPS | United Kingdom | Tier1_CR | RP5 | PP15 | ST512 | Primary |
| 11 | SIM_AGR_011 | AGROSAVIA | Colombia | Tier1_CR | RP26 | PP7 | ST258 | Primary |
| 12 | SIM_CGPS_025 | CGPS | United Kingdom | Tier1_CR | RP4 | PP5 | ST45 | Primary |
| 13 | SIM_IBD_029 | IBADAN | Nigeria | Tier1_CR | RP7 | PP13 | ST23 | Primary |
| 14 | SIM_KIMS_013 | KIMS | India | Tier1_CR | RP4 | PP11 | ST395 | Primary |
| 15 | SIM_RITM_027 | RITM | Philippines | Tier1_CR | RP23 | PP9 | ST231 | Primary |
| 16 | SIM_AGR_016 | AGROSAVIA | Colombia | Tier1_CR | RP19 | PP2 | ST101 | Primary |
| 17 | SIM_CGPS_020 | CGPS | United Kingdom | Tier1_CR | RP6 | PP10 | ST15 | Primary |
| 18 | SIM_IBD_019 | IBADAN | Nigeria | Tier1_CR | RP4 | PP8 | ST307 | Primary |
| 19 | SIM_KIMS_023 | KIMS | India | Tier1_CR | RP7 | PP1 | ST147 | Primary |
| 20 | SIM_RITM_017 | RITM | Philippines | Tier1_CR | RP7 | PP4 | ST17 | Primary |
| 21 | SIM_AGR_021 | AGROSAVIA | Colombia | Tier1_CR | RP22 | PP12 | ST35 | Primary |
| 22 | SIM_CGPS_040 | CGPS | United Kingdom | Tier1_CR | RP18 | PP5 | ST45 | Primary |
| 23 | SIM_KIMS_028 | KIMS | India | Tier1_CR | RP3 | PP11 | ST395 | Primary |
| 24 | SIM_IBD_014 | IBADAN | Nigeria | Tier1_CR | RP24 | PP13 | ST23 | Primary |
| 25 | SIM_RITM_022 | RITM | Philippines | Tier1_CR | RP3 | PP14 | ST86 | Primary |

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
2. All five sentinel sites are equally represented in the 25-isolate selected
   set.
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

