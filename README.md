# GHRU Klebsiella long-read sample choice

Lightweight SOP and helper script for selecting a subsample of short-read
sequenced `Klebsiella pneumoniae` survey isolates for long-read sequencing.

The procedure starts from one integrated isolate-level dataframe: one row per
short-read sequenced isolate, with sentinel-site metadata, AST interpretation,
short-read genotype calls, plasmid summaries, ST/cluster fields, and feasibility
flags in the same table. The helper script ranks that table; it is not intended
to make separate AST, plasmid, and metadata tables agree after the fact.

The procedure is designed to support the survey plasmid objectives:

- convergent strains carrying resistance and virulence signals;
- carbapenemase plasmid diversity within each country/site;
- possible plasmid transmission or repeated plasmid backgrounds across sites.

The strategy follows the June selection approach:

1. classify isolates into resistance tiers;
2. group isolates by resistance profile;
3. add plasmid-profile diversity when plasmid calls are available;
4. choose one primary isolate per site per resistance-profile/plasmid-profile
   combination;
5. deduplicate or review by sequence type, metadata completeness, and lab
   feasibility before confirming the final sequencing list.

## Quick start

Install the minimal Python dependencies in your preferred environment:

```bash
python3 -m pip install -r requirements.txt
```

The script accepts either:

- the June-style priority workbook/CSV, with columns such as `accession_no`,
  `laboratory`, `tier`, `rp_code`, `PP_code`, and `Plasmids`;
- a richer integrated dataframe using the template below.

Create the integrated dataframe using the template when preparing the final
decision table:

- [longread_selection_dataframe_template.csv](templates/longread_selection_dataframe_template.csv)

Run the selector on a CSV or Excel file:

```bash
python3 scripts/select_longread_samples.py \
  --input examples/example_isolates.csv \
  --output outputs/example_priority.csv
```

For June-style Excel input, the script automatically uses `1_Priority_Full` if
that sheet exists:

```bash
python3 scripts/select_longread_samples.py \
  --input isolate_priority_longread_2026-05-22.xlsx \
  --output outputs/priority.csv
```

Use `--sheet-name` only when you want a specific sheet:

```bash
python3 scripts/select_longread_samples.py \
  --input isolate_table.xlsx \
  --sheet-name "1_Priority_Full" \
  --output outputs/priority.csv
```

## Main documents

- [SOP: Long-read isolate subsampling](docs/long_read_subsampling_sop.md)
- [Integrated input dataframe schema](docs/input_schema.md)
- [June-style priority sheet input](docs/june_priority_sheet_input.md)
- [Optional plasmid set-cover layer](docs/plasmid_set_cover.md)
- [Drug-class configuration](config/antibiotic_classes.json)

## Optional plasmid set cover

To identify the minimum isolate set that covers all observed PlasmidFinder
replicons at least once:

```bash
python3 scripts/plasmid_set_cover.py \
  --input examples/example_plasmidfinder.tab \
  --output-prefix outputs/example_plasmid_cover
```

Use the resulting set-cover flags as review fields in the integrated dataframe;
do not use them as a replacement for AST tiering, site balance, ST review, and
feasibility checks.

## Assembly handoff

Confirmed isolates should be assembled with the GHRU assembly workflow:

<https://github.com/ghruproject/GHRU-assembly>

The current workflow supports long-read-only assemblies with Dragonflye and
hybrid assemblies with Unicycler from a samplesheet containing:

```text
sample_id,short_reads1,short_reads2,long_reads,genome_size
```
