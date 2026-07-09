#!/usr/bin/env python3
"""Rank Klebsiella survey isolates for long-read sequencing."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd


TIER_ORDER = {
    "Tier1_CR": 1,
    "Tier2_MDR": 2,
    "Tier3_nonMDR_resistant": 3,
    "Tier4_pansusceptible": 4,
    "Tier_unclassified": 9,
}

TRUE_MISSING = {"", "NA", "N/A", "NAN", "NONE", "NULL", "-"}


def read_table(path: Path, sheet_name: str | None) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        xl = pd.ExcelFile(path)
        chosen_sheet = sheet_name or choose_excel_sheet(xl.sheet_names)
        print(f"INFO: reading Excel sheet: {chosen_sheet}", file=sys.stderr)
        return pd.read_excel(path, sheet_name=chosen_sheet)
    if suffix == ".tsv":
        return pd.read_csv(path, sep="\t")
    return pd.read_csv(path)


def choose_excel_sheet(sheet_names: list[str]) -> str:
    preferred = ["1_Priority_Full", "Priority_Full", "priority_full", "Sheet1"]
    by_lower = {name.lower(): name for name in sheet_names}
    for name in preferred:
        if name.lower() in by_lower:
            return by_lower[name.lower()]
    return sheet_names[0]


def find_column(columns: list[str], candidates: list[str], required: bool = False) -> str | None:
    exact = {c.lower(): c for c in columns}
    for candidate in candidates:
        if candidate.lower() in exact:
            return exact[candidate.lower()]
    if required:
        raise SystemExit(f"Missing required column. Tried: {', '.join(candidates)}")
    return None


def norm_call(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    text = str(value).strip().upper()
    if text in TRUE_MISSING:
        return None
    if text in {"S", "I", "R"}:
        return text
    return None


def choose_ast_call(row: pd.Series, columns_by_lower: dict[str, str], drug: str) -> str | None:
    keys = [f"{drug.lower()}_mic", f"{drug.lower()}_disk", drug.lower()]
    for key in keys:
        col = columns_by_lower.get(key)
        if col:
            call = norm_call(row.get(col))
            if call:
                return call
    return None


def is_nonsusceptible(drug: str, call: str | None, for_profile: bool = False) -> bool:
    if call not in {"R", "I"}:
        return False
    if drug == "COL" and call == "I":
        return False
    return True


def profile_token(drug: str, call: str) -> str:
    return drug if call == "R" else drug.lower()


def normalise_plasmids(value: Any) -> str:
    if value is None:
        return "NO_PLASMID_CALL"
    if isinstance(value, float) and math.isnan(value):
        return "NO_PLASMID_CALL"
    text = str(value).strip()
    if text.upper() in TRUE_MISSING:
        return "NO_PLASMID_CALL"
    parts = [p.strip() for p in re.split(r"[;,|]", text) if p.strip()]
    if not parts:
        return "NO_PLASMID_CALL"
    return ", ".join(sorted(set(parts), key=lambda x: x.upper()))


def has_signal(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, float) and math.isnan(value):
        return False
    text = str(value).strip().upper()
    return text not in TRUE_MISSING


def assign_codes(values: pd.Series, prefix: str) -> dict[str, str]:
    counts = Counter(values.fillna("").astype(str))
    ordered = sorted(counts, key=lambda v: (-counts[v], v))
    return {value: f"{prefix}{i + 1}" for i, value in enumerate(ordered)}


def build_priority_table(df: pd.DataFrame, config: dict[str, Any], args: argparse.Namespace) -> pd.DataFrame:
    columns = list(df.columns)
    lower = {c.lower(): c for c in columns}
    input_mode = detect_input_mode(columns)
    if input_mode == "june_priority":
        print(
            "INFO: detected June-style priority sheet; using precomputed tier/RP/PP fields where needed",
            file=sys.stderr,
        )

    id_col = args.id_column or find_column(columns, ["isolate_id", "accession_no", "sample", "sample_id"], True)
    site_col = args.site_column or find_column(
        columns, ["sentinel_site_code", "laboratory", "site", "sentinel_site"], True
    )
    st_col = args.st_column or find_column(columns, ["st", "mlst", "sequence_type"])
    plasmid_col = args.plasmid_column or find_column(columns, ["Plasmids", "plasmids", "plasmid_replicons"])
    country_col = args.country_column or find_column(columns, ["country"])
    input_tier_col = find_column(columns, ["tier"])
    input_resist_pattern_col = find_column(columns, ["resist_pattern"])
    input_rp_col = find_column(columns, ["rp_code"])
    input_pp_col = find_column(columns, ["PP_code", "pp_code"])

    validation_warnings = validate_integrated_dataframe(
        columns=columns,
        ast_drugs=list(config["drug_classes"]),
        id_col=id_col,
        site_col=site_col,
        country_col=country_col,
        st_col=st_col,
        plasmid_col=plasmid_col,
        input_mode=input_mode,
    )
    for warning in validation_warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    drug_classes = config["drug_classes"]
    tier1_carbapenems = set(config["tier1_carbapenems"])
    intrinsic_exclude = set(config["intrinsic_exclude_from_tier"])
    profile_exclude = set(config["exclude_from_profiles_by_default"])
    threshold = float(args.profile_tested_fraction or config["profile_tested_fraction_threshold"])

    ast_by_drug: dict[str, list[str | None]] = {drug: [] for drug in drug_classes}
    for _, row in df.iterrows():
        for drug in drug_classes:
            ast_by_drug[drug].append(choose_ast_call(row, lower, drug))
    table_has_ast = any(call is not None for calls in ast_by_drug.values() for call in calls)

    n_rows = len(df)
    profile_drugs = []
    for drug, calls in ast_by_drug.items():
        tested_fraction = sum(call is not None for call in calls) / n_rows if n_rows else 0
        if tested_fraction >= threshold and drug not in profile_exclude:
            profile_drugs.append(drug)

    records: list[dict[str, Any]] = []
    for idx, row in df.iterrows():
        ast = {drug: ast_by_drug[drug][idx] for drug in drug_classes}
        row_has_ast = any(call is not None for call in ast.values())

        carb_nonsus = any(is_nonsusceptible(drug, ast.get(drug)) for drug in tier1_carbapenems)
        colistin_r = ast.get("COL") == "R"

        nonsus_classes = set()
        nonsus_drugs_for_profile = []
        for drug, class_name in drug_classes.items():
            call = ast.get(drug)
            if is_nonsusceptible(drug, call):
                if drug not in intrinsic_exclude:
                    nonsus_classes.add(class_name)
                if drug in profile_drugs:
                    nonsus_drugs_for_profile.append(profile_token(drug, call or ""))

        if not row_has_ast and input_tier_col and has_signal(row.get(input_tier_col)):
            tier = str(row.get(input_tier_col)).strip()
        elif carb_nonsus:
            tier = "Tier1_CR"
        elif colistin_r or len(nonsus_classes) >= 3:
            tier = "Tier2_MDR"
        elif len(nonsus_classes) in {1, 2}:
            tier = "Tier3_nonMDR_resistant"
        elif any(call is not None for call in ast.values()):
            tier = "Tier4_pansusceptible"
        else:
            tier = "Tier_unclassified"

        plasmid_profile = normalise_plasmids(row.get(plasmid_col)) if plasmid_col else "NO_PLASMID_CALL"
        if not row_has_ast and input_resist_pattern_col and has_signal(row.get(input_resist_pattern_col)):
            resistance_pattern = str(row.get(input_resist_pattern_col)).strip()
        else:
            resistance_pattern = ";".join(nonsus_drugs_for_profile) or "PANSUSCEPTIBLE_OR_NO_PROFILE_DRUGS"

        carb_gene_col = find_column(columns, ["carbapenemase_genes", "carb_genes"])
        esbl_col = find_column(columns, ["esbl_genes"])
        vir_col = find_column(columns, ["virulence_genes", "yersiniabactin", "aerobactin", "salmochelin", "rmpA", "rmpA2"])

        resistance_gene_signal = has_signal(row.get(carb_gene_col)) or has_signal(row.get(esbl_col))
        virulence_signal = has_signal(row.get(vir_col))

        metadata_fields = [id_col, site_col, country_col, st_col]
        metadata_complete = sum(1 for c in metadata_fields if c and has_signal(row.get(c)))
        metadata_score = metadata_complete / sum(1 for c in metadata_fields if c)

        records.append(
            {
                "isolate_id": row.get(id_col),
                "site": row.get(site_col),
                "country": row.get(country_col) if country_col else "",
                "st": row.get(st_col) if st_col else "",
                "computed_tier": tier,
                "computed_resist_pattern": resistance_pattern,
                "computed_plasmid_profile": plasmid_profile,
                "carb_nonsus": carb_nonsus,
                "colistin_r": colistin_r,
                "mdr_class_count": len(nonsus_classes),
                "resistance_gene_signal": resistance_gene_signal,
                "virulence_signal": virulence_signal,
                "convergent_signal": resistance_gene_signal and virulence_signal,
                "metadata_score": round(metadata_score, 3),
            }
        )

    out = pd.DataFrame.from_records(records)
    if not table_has_ast and input_rp_col:
        out["computed_rp_code"] = df[input_rp_col].astype(str).values
    else:
        rp_map = assign_codes(out["computed_tier"] + "|" + out["computed_resist_pattern"], "RP")
        out["computed_rp_code"] = (out["computed_tier"] + "|" + out["computed_resist_pattern"]).map(rp_map)

    if input_pp_col:
        out["computed_pp_code"] = df[input_pp_col].astype(str).values
    else:
        pp_map = assign_codes(out["computed_plasmid_profile"], "PP")
        out["computed_pp_code"] = out["computed_plasmid_profile"].map(pp_map)
    out["selection_key"] = out["site"].astype(str) + "|" + out["computed_rp_code"] + "|" + out["computed_pp_code"]

    combo_counts = out.groupby(["computed_rp_code", "computed_pp_code"], dropna=False).agg(
        combo_n_isolates=("isolate_id", "count"),
        combo_n_sites=("site", "nunique"),
    )
    out = out.merge(combo_counts, on=["computed_rp_code", "computed_pp_code"], how="left")

    out["selection_batch"] = "Secondary"
    first_idx = (
        out.sort_values(
            by=[
                "computed_tier",
                "convergent_signal",
                "resistance_gene_signal",
                "metadata_score",
                "isolate_id",
            ],
            key=lambda s: s.map(TIER_ORDER) if s.name == "computed_tier" else s,
            ascending=[True, False, False, False, True],
        )
        .groupby("selection_key", dropna=False)
        .head(1)
        .index
    )
    out.loc[first_idx, "selection_batch"] = "Primary"

    out = out.sort_values(
        by=[
            "computed_tier",
            "selection_batch",
            "combo_n_sites",
            "combo_n_isolates",
            "convergent_signal",
            "resistance_gene_signal",
            "metadata_score",
            "isolate_id",
        ],
        key=lambda s: s.map(TIER_ORDER) if s.name == "computed_tier" else s.map({"Primary": 0, "Secondary": 1}) if s.name == "selection_batch" else s,
        ascending=[True, True, False, False, False, False, False, True],
    ).reset_index(drop=True)
    out.insert(0, "priority_rank", range(1, len(out) + 1))

    original_cols_to_keep = [
        c for c in ["tier", "rp_code", "PP_code", "resist_pattern", "qc_status"] if c in df.columns
    ]
    if original_cols_to_keep:
        audit = df[[id_col] + original_cols_to_keep].rename(columns={id_col: "isolate_id"})
        out = out.merge(audit, on="isolate_id", how="left", suffixes=("", "_input"))

    if args.n_select:
        out = apply_balanced_cutoff(out, args.n_select)

    return out


def apply_balanced_cutoff(priority: pd.DataFrame, n_select: int) -> pd.DataFrame:
    if n_select < 1:
        raise SystemExit("--n-select must be at least 1")

    out = priority.copy()
    out["selected_for_sequencing"] = "no"
    out["selection_rank"] = 0
    out["selection_reason"] = ""

    remaining = set(out.index)
    selected: list[int] = []
    site_counts: Counter[str] = Counter()
    site_tier_counts: Counter[tuple[str, str]] = Counter()
    plasmid_counts: Counter[str] = Counter()
    rp_pp_counts: Counter[tuple[str, str]] = Counter()
    st_counts: Counter[str] = Counter()

    while remaining and len(selected) < min(n_select, len(out)):
        scored = []
        for idx in remaining:
            row = out.loc[idx]
            tier = str(row["computed_tier"])
            site = str(row["site"])
            pp = str(row["computed_pp_code"])
            rp = str(row["computed_rp_code"])
            st = str(row["st"]) if has_signal(row.get("st")) else "NO_ST"
            batch = str(row["selection_batch"])
            scored.append(
                (
                    (
                        TIER_ORDER.get(tier, 9),
                        0 if batch == "Primary" else 1,
                        site_counts[site],
                        site_tier_counts[(site, tier)],
                        plasmid_counts[pp],
                        rp_pp_counts[(rp, pp)],
                        st_counts[st],
                        -int(row["combo_n_sites"]),
                        -int(row["combo_n_isolates"]),
                        0 if bool(row["convergent_signal"]) else 1,
                        0 if bool(row["resistance_gene_signal"]) else 1,
                        -float(row["metadata_score"]),
                        str(row["isolate_id"]),
                    ),
                    idx,
                )
            )

        _, chosen_idx = min(scored)
        chosen = out.loc[chosen_idx]
        selected.append(chosen_idx)
        remaining.remove(chosen_idx)

        tier = str(chosen["computed_tier"])
        site = str(chosen["site"])
        pp = str(chosen["computed_pp_code"])
        rp = str(chosen["computed_rp_code"])
        st = str(chosen["st"]) if has_signal(chosen.get("st")) else "NO_ST"

        site_counts[site] += 1
        site_tier_counts[(site, tier)] += 1
        plasmid_counts[pp] += 1
        rp_pp_counts[(rp, pp)] += 1
        st_counts[st] += 1

        rank = len(selected)
        out.at[chosen_idx, "selected_for_sequencing"] = "yes"
        out.at[chosen_idx, "selection_rank"] = rank
        out.at[chosen_idx, "selection_reason"] = (
            f"{tier}; {chosen['selection_batch']}; balanced site {site}; "
            f"plasmid profile {pp}; RP {rp}; ST {st}"
        )

    out["selection_rank_sort"] = out["selection_rank"].map(lambda x: int(x) if int(x) > 0 else 999999)
    out = out.sort_values(
        by=["selected_for_sequencing", "selection_rank_sort", "priority_rank"],
        ascending=[False, True, True],
    ).drop(columns=["selection_rank_sort"])
    return out


def write_output(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        df.to_excel(path, index=False)
    else:
        df.to_csv(path, index=False, quoting=csv.QUOTE_MINIMAL)


def validate_integrated_dataframe(
    columns: list[str],
    ast_drugs: list[str],
    id_col: str | None,
    site_col: str | None,
    country_col: str | None,
    st_col: str | None,
    plasmid_col: str | None,
    input_mode: str,
) -> list[str]:
    lower = {c.lower() for c in columns}
    warnings = []

    if not id_col:
        warnings.append("no isolate identifier column found")
    if not site_col:
        warnings.append("no sentinel site/laboratory column found")
    if input_mode == "june_priority":
        if not plasmid_col and "pp_code" not in lower:
            warnings.append(
                "June-style sheet has no plasmid column or PP_code; selection will use resistance profiles only"
            )
        return warnings

    if not country_col:
        warnings.append("no country column found; country balance must be reviewed outside the script")
    if not st_col:
        warnings.append("no ST/lineage column found; ST deduplication must be done outside the script")
    if not plasmid_col:
        warnings.append("no plasmid replicon/profile column found; selection will fall back to resistance profiles only")

    ast_columns_found = []
    for drug in ast_drugs:
        for key in [drug.lower(), f"{drug.lower()}_mic", f"{drug.lower()}_disk"]:
            if key in lower:
                ast_columns_found.append(drug)
                break
    if not ast_columns_found and not {"tier", "resist_pattern"}.issubset(lower):
        warnings.append("no AST interpretation columns or precomputed tier/resist_pattern columns found")

    recommended_groups = {
        "eligibility": ["short_read_qc", "qc_status", "isolate_available", "dna_available"],
        "AMR genes": ["carbapenemase_genes", "carb_genes", "esbl_genes", "other_amr_genes"],
        "virulence": ["virulence_genes", "yersiniabactin", "aerobactin", "salmochelin", "rmpa", "rmpa2"],
        "feasibility": ["local_longread_capacity", "sequencing_site", "support_route"],
    }
    for label, candidates in recommended_groups.items():
        if not any(candidate in lower for candidate in candidates):
            warnings.append(f"no {label} field found; this should be added to the integrated selection dataframe")

    return warnings


def detect_input_mode(columns: list[str]) -> str:
    lower = {c.lower() for c in columns}
    june_markers = {"priority_rank", "selection_batch", "tier", "rp_code", "resist_pattern"}
    if len(june_markers.intersection(lower)) >= 3:
        return "june_priority"
    return "integrated"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Input CSV/TSV/XLSX isolate table")
    parser.add_argument("--output", required=True, type=Path, help="Output CSV/XLSX priority table")
    parser.add_argument("--sheet-name", help="Excel sheet name. Defaults to first sheet.")
    parser.add_argument("--config", type=Path, default=Path("config/antibiotic_classes.json"))
    parser.add_argument("--id-column")
    parser.add_argument("--site-column")
    parser.add_argument("--country-column")
    parser.add_argument("--st-column")
    parser.add_argument("--plasmid-column")
    parser.add_argument("--profile-tested-fraction", type=float)
    parser.add_argument(
        "--n-select",
        type=int,
        help="Number of isolates to flag for sequencing after prioritisation and balanced cutoff.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with args.config.open() as handle:
        config = json.load(handle)
    df = read_table(args.input, args.sheet_name)
    priority = build_priority_table(df, config, args)
    write_output(priority, args.output)
    print(f"Wrote {len(priority)} ranked isolates to {args.output}")
    print(priority["selection_batch"].value_counts().to_string())
    print(priority["computed_tier"].value_counts().to_string())
    if args.n_select:
        print(priority["selected_for_sequencing"].value_counts().to_string())


if __name__ == "__main__":
    main()
