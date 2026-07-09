# SOP: Long-read isolate subsampling for Klebsiella survey isolates

## 1. Purpose

This SOP defines how to select a practical, diversity-focused subset of
short-read sequenced `Klebsiella pneumoniae` survey isolates for long-read
sequencing. The aim is not exhaustive sampling. The aim is to capture enough
phenotypic, genotypic, plasmid, site, and feasibility diversity to support
plasmid analysis of carbapenemases, ESBLs, virulence-associated convergence,
and possible plasmid transmission.

## 2. Scope

Use this SOP after short-read sequencing and initial QC are complete. The SOP
applies to structured survey isolates from Agrosavia, RITM, KIMS, Ibadan, and
CGPS-supported analyses where long-read sequencing will be used to resolve
plasmids and mobile genetic elements.

## 3. Integrated input dataframe

For scripting, the input may be either the June-style priority sheet or a richer
integrated isolate dataframe. The June-style sheet is sufficient to reproduce
the tier/profile/plasmid-profile prioritisation. The richer dataframe is
preferred for final confirmation because each row carries the metadata needed
for ST review, country/site balance, AMR/virulence interpretation, and
sequencing feasibility.

Do not confirm the final sequencing list from separate AST, plasmid, and
sentinel metadata files unless they have first been joined or checked against
the same isolate identifiers.

Minimum columns:

- isolate identifier;
- country and sentinel site code/name;
- AST interpretation data or derived genomic AMR profile;
- short-read AMR, virulence, plasmid, and ST calls where available;
- short-read QC pass/fail status.

Recommended input:

- specimen date/type and patient subgroup fields needed for survey review;
- sequence type and cgMLST cluster;
- carbapenemase, ESBL, and other AMR genes;
- virulence markers relevant to convergent `Klebsiella`;
- plasmid replicon/profile calls, MOB type, and plasmid cluster if available;
- isolate availability, DNA availability, and local long-read capacity.

The purpose of this integrated table is to make each selection decision
auditable from one row: why the isolate is in a tier, what plasmid signal it
adds, whether it duplicates an ST/profile already represented, and whether the
site can sequence it.

## 4. Resistance-tier definitions

Assign one tier per isolate using the rules below. Apply the first matching tier
in order.

| Tier | Definition | Priority |
| --- | --- | --- |
| Tier1_CR | Carbapenem non-susceptible: `R` or `I` to ertapenem, imipenem, or meropenem. Carbapenem `I` is included as a possible carbapenemase signal under CLSI `K. pneumoniae` breakpoints. | Highest |
| Tier2_MDR | Not Tier 1, and either colistin resistant (`COL = R`) or MDR: non-susceptible to at least one drug in at least three antibiotic classes. Ampicillin is excluded from MDR class counting because resistance is intrinsic in `K. pneumoniae`. Colistin `I` is not counted as MDR or profile non-susceptibility. | High |
| Tier3_nonMDR_resistant | Not Tier 1 or 2, and non-susceptible to at least one drug in one or two antibiotic classes. | Moderate |
| Tier4_pansusceptible | Susceptible to all counted drugs tested. Ampicillin is ignored for this classification. | Control/background |

## 5. Profile construction

Create two diversity profiles when data are available.

### 5.1 Resistance profile

1. Use MIC interpretation where present; use disk interpretation only where MIC
   is missing.
2. Exclude drugs tested in fewer than 80% of eligible isolates from the
   resistance-profile string, unless the group agrees otherwise.
3. Exclude `SAM`, `CTT`, and `TGC` by default, matching the June example.
4. Retain ampicillin in the audit profile if present, but do not use it for
   tier assignment or MDR class counting.
5. Encode the profile as the ordered list of non-susceptible drugs and assign
   `RP1`, `RP2`, etc. within tier by descending isolate count.

### 5.2 Plasmid profile

1. Normalise plasmid replicon calls by trimming whitespace, deduplicating names,
   and sorting names alphabetically.
2. Isolates with no plasmid call should be coded as `NO_PLASMID_CALL`, not
   treated as biologically plasmid-free.
3. Assign `PP1`, `PP2`, etc. by descending profile count.
4. Use plasmid profile to avoid repeatedly long-read sequencing isolates with
   the same site, resistance profile, and plasmid profile unless there is a
   clear ST, outbreak, or metadata reason.

### 5.3 Optional plasmid set cover

Run a greedy plasmid set-cover check when an Abricate/PlasmidFinder matrix is
available. This identifies the minimum non-redundant isolate set required to
cover every observed plasmid replicon at least once.

Use the set-cover output as a review layer:

- flag set-cover isolates in the integrated dataframe;
- check whether each set-cover isolate is already in the primary sequencing
  set;
- if a set-cover isolate is not selected, document whether its plasmid is
  already covered by a higher-priority isolate, whether the isolate failed
  feasibility checks, or whether the plasmid call is too weak to drive
  sequencing.

Set cover must not override Tier1_CR priority, country/site balance, ST
deduplication, or feasibility review by itself.

## 6. Primary selection rule

The primary sequencing set should contain one isolate per site per
`resistance profile x plasmid profile` combination across all tiers.

If plasmid profiles are not yet available, use one isolate per site per
resistance profile as the fallback rule and rerun the selection when plasmid
profiles become available.

Additional isolates with an already covered site/profile combination are
secondary candidates. They may be selected if sequencing capacity allows or if
manual review identifies a specific plasmid-analysis reason.

## 7. Ranking order

Rank candidates in this order. When a fixed sequencing capacity is provided,
apply the cutoff with the same order and keep unselected rows as alternates:

1. tier: Tier1_CR, then Tier2_MDR, then Tier3_nonMDR_resistant, then
   Tier4_pansusceptible;
2. primary candidates before secondary candidates;
3. sentinel-site balance, giving priority to sites with fewer already selected
   isolates within the same tier/batch;
4. plasmid-profile diversity, giving priority to plasmid profiles and `RP x PP`
   combinations not already represented;
5. wider profile distribution, using the number of sites and isolates sharing
   the same resistance/plasmid combination;
6. convergent signal: resistance genes plus virulence markers;
7. carbapenemase or ESBL gene signal;
8. metadata completeness and sequencing feasibility;
9. ST as a late tie-breaker, only after tier, site balance, plasmid profile,
   and biological flags have been considered.

## 8. Human review and deduplication

After scripted ranking, the site and CGPS bioinformatics leads must review the
candidate list before sequencing is confirmed.

Required review checks:

- country/site representation is appropriate for the survey objective;
- Tier1_CR isolates are sufficiently represented for plasmid diversity;
- convergent strains are not lost during deduplication;
- repeated ST/profile combinations are not over-sampled unless they support
  plasmid transmission analysis;
- each selected isolate has sufficient metadata and culture/DNA availability;
- each site can either run the GHRU assembly workflow locally or has an agreed
  central support route.

## 9. Outputs

The confirmed selection package should contain:

- versioned SOP or meeting-approved criteria;
- ranked candidate table;
- confirmed selected isolate list;
- metadata completeness check;
- sequencing timetable;
- GHRU assembly samplesheet for selected isolates;
- first assembly outputs and QC summary;
- log of unresolved pipeline or metadata issues.

## 10. Assembly handoff

Run selected isolates through the GHRU assembly workflow:

<https://github.com/ghruproject/GHRU-assembly>

For hybrid assembly, prepare a samplesheet with:

```text
sample_id,short_reads1,short_reads2,long_reads,genome_size
```

Use the site-approved Nextflow/Docker route where available. Sites unable to run
the workflow locally should record the central-support handoff route before
sequencing begins.
