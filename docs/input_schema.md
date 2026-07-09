# Integrated input dataframe schema

The script accepts CSV, TSV, XLS, and XLSX files. For the current June-style
workbook, see [June-style priority sheet input](june_priority_sheet_input.md).

For final decision-making, the preferred input is one isolate-level dataframe:
one row per short-read sequenced isolate. Join AST, short-read genotyping,
plasmid calls, sentinel-site metadata, and feasibility information before final
manual review.

Column names are treated case-insensitively. A header template is provided at:

`templates/longread_selection_dataframe_template.csv`

## Required columns

| Field | Accepted column names | Notes |
| --- | --- | --- |
| Isolate identifier | `isolate_id`, `accession_no`, `sample`, `sample_id` | Use `--id-column` if a different name is used. |
| Sentinel site | `sentinel_site_code`, `laboratory`, `site`, `sentinel_site` | Use `--site-column` if a different name is used. |

## Decision fields needed

These fields are not all mathematically required, but they are needed to make a
defensible long-read selection.

| Information block | Fields | Why it is needed |
| --- | --- | --- |
| Sentinel context | `country`, `sentinel_site_code`, `sentinel_site_name` | Country/site balance and one-per-site profile selection. |
| Isolate context | `specimen_date`, `specimen_type`, `age_group`, `neonate`, `species` | Survey interpretability and special subgroups. |
| Eligibility | `short_read_qc`, `isolate_available`, `dna_available` | Avoid selecting isolates that cannot be sequenced or assembled. |
| AST profile | `*_mic` or `*_disk` interpretation columns for the survey AST panel | Tier assignment and resistance-profile grouping. |
| AMR genotype | `carbapenemase_genes`, `esbl_genes`, `other_amr_genes` | Carbapenemase/ESBL plasmid objective and AST cross-check. |
| Virulence genotype | `virulence_genes` or marker-specific columns | Convergent-strain objective. |
| Plasmid signal | `plasmid_replicons`, optional `plasmid_mob_types`, optional `plasmid_cluster_ids` | Plasmid-profile diversity and possible transmission. |
| Plasmid set cover | optional `plasmid_set_cover_selected`, `plasmid_set_cover_step`, `plasmids_new_at_step`, `n_new_plasmids` | Minimum coverage of observed plasmid replicons. |
| Lineage | `st`, optional `cgmlst_cluster` | Deduplication and outbreak/transmission review. |
| Feasibility | `local_longread_capacity`, `notes` | Site sequencing route and support planning. |

## AST columns

AST interpretations should be coded as `S`, `I`, or `R`. The script accepts
either direct drug-code columns or MIC/disk interpretation columns:

| Drug | Accepted examples |
| --- | --- |
| Ertapenem | `ETP`, `etp`, `etp_mic`, `etp_disk` |
| Imipenem | `IPM`, `ipm_mic`, `ipm_disk` |
| Meropenem | `MEM`, `mem_mic`, `mem_disk` |
| Colistin | `COL`, `col_mic`, `col_disk` |

When both MIC and disk interpretation columns exist, MIC is used first and disk
is used only where MIC is missing.

## Optional precomputed columns

If an input file already contains `tier`, `rp_code`, `PP_code`, or
`resist_pattern`, those columns are retained for audit, but the script writes
fresh `computed_*` columns from the configured rules.

The June example workbooks contain useful precomputed priority fields and are a
supported script input. The richer integrated dataframe is still preferred for
final confirmation because it keeps ST, country, AMR/virulence, and feasibility
checks in the same row.
