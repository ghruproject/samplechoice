# June-style priority sheet input

The selector is intended to accept the June workbook format directly as CSV or
Excel. This is the practical input style for the current sampling work.

## Expected shape

One row per isolate, with columns like:

- `accession_no`
- `laboratory`
- `tier`
- `rp_code`
- `resist_pattern`
- optional `PP_code`
- optional `Plasmids`
- optional `selection_batch`
- optional `priority_rank`

If raw AST columns such as `etp_mic`, `ipm_mic`, and `mem_mic` are present, the
script recomputes tier/profile fields from those calls. If raw AST columns are
absent, the script uses the precomputed `tier`, `rp_code`, and
`resist_pattern` fields from the sheet.

If `PP_code` or `Plasmids` is present, the script uses plasmid profile coverage.
If neither is present, it falls back to one isolate per site per resistance
profile.

## Excel use

For Excel workbooks, the script automatically uses `1_Priority_Full` when that
sheet exists. This means the June workbook can be run without specifying a
sheet:

```bash
python3 scripts/select_longread_samples.py \
  --input isolate_priority_longread_2026-05-22.xlsx \
  --output outputs/priority.csv
```

You can still choose a sheet explicitly:

```bash
python3 scripts/select_longread_samples.py \
  --input isolate_priority_longread_2026-05-22.xlsx \
  --sheet-name "2_Primary_Batch" \
  --output outputs/primary_batch_reranked.csv
```

## Limitations

The June-style sheet is enough to reproduce the tier/profile/plasmid-profile
ranking. It is not enough by itself for final confirmation unless ST, country,
AMR gene, virulence, culture/DNA availability, and sequencing feasibility have
also been joined or checked elsewhere.

