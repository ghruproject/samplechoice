# Optional plasmid set-cover layer

Angela Garcia shared an R script that implements a greedy minimum plasmid set
cover from an Abricate/PlasmidFinder matrix. The core idea is useful for this
SOP, but it should be used as a plasmid-diversity layer rather than as the whole
long-read selection strategy.

## What it answers

Given a binary isolate-by-plasmid matrix, identify a small set of isolates that
covers every observed plasmid replicon at least once.

This helps answer:

- which isolates are required to avoid missing rare plasmid replicon types;
- how much plasmid diversity is captured after each additional selected isolate;
- whether the tier/profile ranking has accidentally skipped a plasmid type.

## How it fits the SOP

Use set cover after building the integrated isolate dataframe and before final
manual review.

1. Run PlasmidFinder/Abricate on the short-read assemblies.
2. Convert the PlasmidFinder summary table to a binary isolate-by-plasmid matrix.
3. Run the set-cover script.
4. Add these fields back to the integrated dataframe:
   - `plasmid_set_cover_selected`: `yes`/`no`;
   - `plasmid_set_cover_step`: greedy selection step;
   - `plasmids_new_at_step`: plasmids first covered by that isolate;
   - `n_new_plasmids`: number of newly covered plasmids.
5. In final review, check that all set-cover isolates are either selected or
   have a documented reason for exclusion.

Set cover does not replace resistance tiering, country/site representation, ST
deduplication, or feasibility checks. A low-priority isolate may be retained if
it is the only isolate covering a rare plasmid, but that should be a visible
manual decision.

## Run the helper script

```bash
python3 scripts/plasmid_set_cover.py \
  --input examples/example_plasmidfinder.tab \
  --output-prefix outputs/example_plasmid_cover
```

Outputs:

- `*_history.csv`: greedy selection steps and newly covered plasmids;
- `*_selected_isolates.txt`: selected isolate IDs;
- `*_selected_matrix.csv`: binary matrix for the selected isolates.

