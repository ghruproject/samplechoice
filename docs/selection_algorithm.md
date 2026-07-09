# Selection algorithm

The selector ranks the whole input table, then optionally flags the first `N`
isolates for sequencing with `--n-select`.

The intended decision order is:

1. **AST tier first.** Apply the June tier definitions: Tier1_CR before
   Tier2_MDR, then Tier3_nonMDR_resistant, then Tier4_pansusceptible.
2. **Primary profile coverage before duplicates.** Prefer the first isolate for
   each sentinel-site `RP x PP` combination before repeated candidates.
3. **Sentinel-site balance.** Within the same tier and batch, choose from sites
   with fewer selected isolates so one high-volume site does not consume the
   list.
4. **Plasmid-profile diversity.** Prefer plasmid profiles and `RP x PP`
   combinations not already selected.
5. **Biological flags.** Prefer convergent isolates and AMR-gene-positive
   isolates when those fields are available.
6. **Metadata completeness.** Prefer rows with country/site/ST fields present.
7. **ST only as a late tie-breaker.** Prefer STs not already selected, but do
   not let ST override tier, sentinel balance, or plasmid-profile diversity.

The output keeps all isolates. When `--n-select` is used, selected isolates have:

- `selected_for_sequencing = yes`;
- `selection_rank`;
- `selection_reason`.

This keeps the cutoff auditable. The unselected rows remain available as
alternates if cultures fail or extra sequencing capacity becomes available.

## Plasmid profile reconstruction

If the input has `PP_code`, the script treats that as the June plasmid profile.
If `PP_code` is absent but a plasmid column such as `Plasmids` or
`plasmid_replicons` is present, the script reconstructs profiles by:

1. splitting plasmid names on commas, semicolons, or pipes;
2. trimming whitespace;
3. deduplicating repeated names within an isolate;
4. sorting plasmid names alphabetically;
5. assigning `PP1`, `PP2`, etc. by descending profile frequency.

Rows with no plasmid call are coded as `NO_PLASMID_CALL`. This means missing
plasmid data are visible and do not get interpreted as true plasmid absence.

