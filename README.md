# GHRU Klebsiella long-read sample choice

SOP, demonstration data, and helper scripts for selecting a subsample of
short-read sequenced `Klebsiella pneumoniae` survey isolates for long-read
sequencing.

This repository is intended to be readable by project leads as well as analysts.
The core question is:

> Given a short-read isolate table and a fixed long-read sequencing capacity,
> which isolates should be selected first, and why?

The answer is produced as an auditable ranked table. The script keeps all input
isolates, flags the selected subset, and records a short reason for each
selected isolate.

The procedure is designed to support the survey plasmid objectives:

- convergent strains carrying resistance and virulence signals;
- carbapenemase plasmid diversity within each country/site;
- possible plasmid transmission or repeated plasmid backgrounds across sites.

The strategy follows the June selection approach:

1. classify isolates into resistance tiers;
2. group isolates by resistance profile;
3. balance representation across sentinel sites;
4. add plasmid-profile diversity when plasmid calls are available;
5. choose one primary isolate per site per resistance-profile/plasmid-profile
   combination;
6. use sequence type only as a late tie-breaker;
7. review metadata completeness and lab feasibility before confirming the final
   sequencing list.

## For Project Leads

Start with:

- [Manager briefing](docs/manager_briefing.md)
- [Simulated example results](docs/simulated_results.md)
- [SOP: Long-read isolate subsampling](docs/long_read_subsampling_sop.md)

These documents explain the rationale, show the simulated selection result, and
describe what still requires human approval.

## Quick start

Install the minimal Python dependencies in your preferred environment:

```bash
python3 -m pip install -r requirements.txt
```

Run the simulated end-to-end demo:

```bash
bash scripts/run_demo.sh
```

This writes a ranked long-read selection from
`examples/simulated_june_priority.csv` and a plasmid set-cover demonstration to
`outputs/`.

The simulated selection asks for 25 isolates from 100 candidates. The selected
set contains 25 Tier1_CR isolates, balanced as 5 isolates from each of 5
sentinel sites.

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
  --input examples/simulated_june_priority.csv \
  --n-select 25 \
  --output outputs/simulated_priority.csv
```

For June-style Excel input, the script automatically uses `1_Priority_Full` if
that sheet exists:

```bash
python3 scripts/select_longread_samples.py \
  --input isolate_priority_longread_2026-05-22.xlsx \
  --n-select 96 \
  --output outputs/priority.csv
```

Omit `--n-select` when you want the full ranked table without a fixed cutoff.

Use `--sheet-name` only when you want a specific sheet:

```bash
python3 scripts/select_longread_samples.py \
  --input isolate_table.xlsx \
  --sheet-name "1_Priority_Full" \
  --output outputs/priority.csv
```

## Main documents

- [Manager briefing](docs/manager_briefing.md)
- [Simulated example results](docs/simulated_results.md)
- [SOP: Long-read isolate subsampling](docs/long_read_subsampling_sop.md)
- [Selection algorithm](docs/selection_algorithm.md)
- [Worked simulated example](docs/worked_simulated_example.md)
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
