#!/usr/bin/env python3
"""Greedy plasmid set cover for Abricate/PlasmidFinder summary tables."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd


MISSING = {"", ".", "NA", "N/A", "NAN", "NONE", "NULL", "-"}


def read_matrix(path: Path, sep: str | None) -> pd.DataFrame:
    if sep is None:
        sep = "\t" if path.suffix.lower() in {".tab", ".tsv"} else ","
    return pd.read_csv(path, sep=sep, dtype=str, keep_default_na=False)


def clean_matrix(raw: pd.DataFrame, id_column: str | None) -> pd.DataFrame:
    if raw.empty:
        raise SystemExit("Input matrix is empty")

    id_col = id_column or raw.columns[0]
    if id_col not in raw.columns:
        raise SystemExit(f"ID column not found: {id_col}")

    df = raw.copy()
    isolate_ids = df[id_col].map(lambda x: Path(str(x)).stem)
    df = df.drop(columns=[id_col])
    if "NUM_FOUND" in df.columns:
        df = df.drop(columns=["NUM_FOUND"])

    binary = df.apply(lambda col: col.map(lambda x: 0 if str(x).strip().upper() in MISSING else 1))
    binary.index = isolate_ids
    binary = binary.loc[:, binary.sum(axis=0) > 0]
    binary = binary.loc[binary.sum(axis=1) > 0, :]
    if binary.empty:
        raise SystemExit("No plasmid-positive isolates remain after cleaning")
    return binary


def collapse_duplicate_profiles(matrix: pd.DataFrame) -> pd.DataFrame:
    profile_key = matrix.astype(str).agg("-".join, axis=1)
    return matrix.loc[~profile_key.duplicated(), :]


def remove_dominated_profiles(matrix: pd.DataFrame) -> pd.DataFrame:
    values = matrix.to_numpy()
    keep = [True] * len(matrix)
    for i in range(len(matrix)):
        if not keep[i]:
            continue
        for j in range(len(matrix)):
            if i == j:
                continue
            contained = (values[i] <= values[j]).all()
            strictly_more = (values[j] > values[i]).any()
            if contained and strictly_more:
                keep[i] = False
                break
    return matrix.loc[keep, :]


def greedy_set_cover(matrix: pd.DataFrame) -> tuple[list[str], pd.DataFrame]:
    remaining = set(matrix.columns)
    selected: list[str] = []
    history = []

    step = 1
    while remaining:
        coverage = matrix[list(remaining)].sum(axis=1)
        best = coverage.sort_values(ascending=False).index[0]
        n_new = int(coverage.loc[best])
        if n_new == 0:
            break

        new_plasmids = sorted([p for p in remaining if matrix.loc[best, p] == 1])
        history.append(
            {
                "step": step,
                "isolate_id": best,
                "n_new_plasmids": n_new,
                "remaining_before": len(remaining),
                "plasmids_new_at_step": ";".join(new_plasmids),
            }
        )
        selected.append(best)
        remaining.difference_update(new_plasmids)
        step += 1

    return selected, pd.DataFrame(history)


def write_outputs(selected: list[str], history: pd.DataFrame, matrix: pd.DataFrame, prefix: Path) -> None:
    prefix.parent.mkdir(parents=True, exist_ok=True)
    history.to_csv(f"{prefix}_history.csv", index=False)
    matrix.loc[selected].to_csv(f"{prefix}_selected_matrix.csv")
    with open(f"{prefix}_selected_isolates.txt", "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["isolate_id"])
        for isolate_id in selected:
            writer.writerow([isolate_id])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Abricate/PlasmidFinder matrix")
    parser.add_argument("--output-prefix", required=True, type=Path, help="Prefix for output files")
    parser.add_argument("--id-column", help="ID column. Defaults to first column.")
    parser.add_argument("--sep", help="Input separator. Defaults to TSV for .tab/.tsv, otherwise CSV.")
    parser.add_argument(
        "--keep-dominated",
        action="store_true",
        help="Do not remove profiles fully contained by another profile before greedy cover.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw = read_matrix(args.input, args.sep)
    matrix = clean_matrix(raw, args.id_column)
    matrix = collapse_duplicate_profiles(matrix)
    if not args.keep_dominated:
        matrix = remove_dominated_profiles(matrix)

    selected, history = greedy_set_cover(matrix)
    write_outputs(selected, history, matrix, args.output_prefix)

    covered = matrix.loc[selected].sum(axis=0) > 0
    print(f"Selected {len(selected)} isolates from {len(matrix)} non-redundant profiles")
    print(f"Covered {int(covered.sum())}/{matrix.shape[1]} plasmids")
    print(f"Wrote outputs with prefix: {args.output_prefix}")


if __name__ == "__main__":
    main()
