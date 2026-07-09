# Simulated example results

The simulated input is:

`examples/simulated_june_priority.csv`

It contains 20 candidate isolates across five sentinel sites. The example asks
for 10 long-read isolates:

```bash
python3 scripts/select_longread_samples.py \
  --input examples/simulated_june_priority.csv \
  --n-select 10 \
  --output outputs/simulated_priority.csv
```

## Overall result

| selected_for_sequencing | isolates |
| ----------------------- | -------- |
| yes | 10 |
| no | 10 |

The selected set is balanced across all five sentinel sites:

| site | country | selected |
| --- | --- | --- |
| AGROSAVIA | Colombia | 2 |
| CGPS | United Kingdom | 2 |
| IBADAN | Nigeria | 2 |
| KIMS | India | 2 |
| RITM | Philippines | 2 |

The selected set is dominated by Tier1_CR, as intended:

| tier | selected |
| --- | --- |
| Tier1_CR | 8 |
| Tier2_MDR | 2 |

No Tier3 or Tier4 isolate is selected in this 10-isolate example because the
Tier1 and Tier2 candidates fill the available capacity. If the capacity is
increased, lower tiers enter as ranked alternates after higher-priority
profiles have been represented.

## Selected isolates

| selection_rank | isolate_id | site | country | computed_tier | computed_rp_code | computed_pp_code | st | selection_batch |
| -------------- | ---------- | ---- | ------- | ------------- | ---------------- | ---------------- | -- | --------------- |
| 1 | SIM_AGR_001 | AGROSAVIA | Colombia | Tier1_CR | RP3 | PP1 | ST307 | Primary |
| 2 | SIM_RITM_001 | RITM | Philippines | Tier1_CR | RP4 | PP2 | ST147 | Primary |
| 3 | SIM_KIMS_002 | KIMS | India | Tier1_CR | RP2 | PP5 | ST231 | Primary |
| 4 | SIM_CGPS_001 | CGPS | United Kingdom | Tier1_CR | RP7 | PP4 | ST15 | Primary |
| 5 | SIM_IBD_001 | IBADAN | Nigeria | Tier1_CR | RP6 | PP3 | ST101 | Primary |
| 6 | SIM_KIMS_001 | KIMS | India | Tier1_CR | RP2 | PP1 | ST231 | Primary |
| 7 | SIM_RITM_002 | RITM | Philippines | Tier1_CR | RP4 | PP2 | ST147 | Secondary |
| 8 | SIM_AGR_002 | AGROSAVIA | Colombia | Tier1_CR | RP3 | PP1 | ST307 | Secondary |
| 9 | SIM_CGPS_002 | CGPS | United Kingdom | Tier2_MDR | RP12 | PP10 | ST35 | Primary |
| 10 | SIM_IBD_002 | IBADAN | Nigeria | Tier2_MDR | RP10 | PP9 | ST17 | Primary |

## What this demonstrates

The simulated result shows the intended behaviour:

1. Tier1_CR isolates are selected before lower tiers.
2. All five sentinel sites are represented before the script gives a third slot
   to any site.
3. Plasmid profiles are considered before ST duplication becomes relevant.
4. ST does not override the higher-priority AST, site, and plasmid-profile
   criteria.
5. The output keeps alternates, so failed cultures can be replaced without
   rerunning the whole decision process.

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

